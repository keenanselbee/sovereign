"""Run the isolated Lua rescue function with mocked game calls, not an HKS qualification.

Uses the workstation's existing ModEngine Lua DLL. No game process is touched.
"""
import ctypes
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
LUA = Path(os.environ.get('SOVEREIGN_TEST_LUA_DLL',
    'Z:/Modding/Elden Ring/Tools/ModEngine/modengine2/bin/lua.dll'))

@unittest.skipUnless(LUA.is_file(), 'Existing Lua runtime is unavailable')
class RescueLogic(unittest.TestCase):
    def run_lua(self, script):
        dll = ctypes.CDLL(str(LUA))
        dll.luaL_newstate.restype = ctypes.c_void_p
        dll.luaL_openlibs.argtypes = [ctypes.c_void_p]
        dll.luaL_loadstring.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        dll.lua_pcallk.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                 ctypes.c_int, ctypes.c_ssize_t, ctypes.c_void_p]
        dll.lua_tolstring.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
        dll.lua_tolstring.restype = ctypes.c_char_p
        dll.lua_close.argtypes = [ctypes.c_void_p]
        state = dll.luaL_newstate()
        try:
            dll.luaL_openlibs(state)
            rc = dll.luaL_loadstring(state, script.encode())
            if rc == 0:
                rc = dll.lua_pcallk(state, 0, 0, 0, 0, None)
            self.assertEqual(rc, 0, (dll.lua_tolstring(state, -1, None) or b'').decode())
        finally:
            dll.lua_close(state)

    def test_cooldown_consumption_and_death_exclusions(self):
        source = (ROOT/'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        body = source.split('function ModBeginnerRescue(lethal)', 1)[1].split('function ExecDeath()', 1)[0]
        fn = 'function ModBeginnerRescue(lethal)' + body
        names = set(re.findall(r'(?:env|act)\((\w+)', fn))
        names |= {'CONDITION_TYPE_STONE', 'CONDITION_TYPE_CRYSTAL', 'DAMAGE_TYPE_DEATH_FALLING'}
        bindings = '\n'.join(f'{name}="{name}"' for name in names)
        harness = r'''
TRUE=1; FALSE=0
local effects, hp, maxhp, values, healed
function reset()
 effects={[1627122]=true};hp=100;maxhp=500;values={};healed=0
end
function ModGetEffectiveHPMax() return maxhp end
function env(key,arg)
 if key==GetSpEffectID then return effects[arg] and TRUE or FALSE end
 if key==GetHP then return hp end
 if key==GetFallHeight then return values[key] or 0 end
 if key==GetStateChangeType then return values[arg] or FALSE end
 if key==HasReceivedAnyDamage then return values[key] or TRUE end
 return values[key] or FALSE
end
function act(key,arg)
 if key==AddSpEffect then effects[arg]=true end
 if key==ChangeHP then hp=hp+arg;healed=healed+1 end
end
reset();assert(ModBeginnerRescue(FALSE)==TRUE);assert(hp==500 and healed==1)
assert(effects[1627125] and effects[1627126] and effects[1627127] and effects[1627124])
hp=-10;assert(ModBeginnerRescue(TRUE)==FALSE);assert(healed==1)
-- 15s elapsed: outside remains on cooldown, entering the arena uses the same timer.
effects[1627126]=nil;hp=100;assert(ModBeginnerRescue(FALSE)==FALSE)
effects[1627123]=true;assert(ModBeginnerRescue(FALSE)==TRUE);assert(healed==2)
-- Leaving/re-entering cannot clear the newly consumed cooldown.
effects[1627123]=nil;effects[1627123]=true;hp=100
assert(ModBeginnerRescue(FALSE)==FALSE)
-- 30s elapsed, either location can use the allowance.
effects[1627126]=nil;effects[1627127]=nil;effects[1627123]=nil
assert(ModBeginnerRescue(FALSE)==TRUE)
reset();hp=-200;assert(ModBeginnerRescue(TRUE)==TRUE and hp==500)
reset();hp=151;assert(ModBeginnerRescue(FALSE)==FALSE)
hp=150;assert(ModBeginnerRescue(FALSE)==TRUE)
reset();maxhp=750;hp=220;assert(ModBeginnerRescue(FALSE)==TRUE and hp==750)
reset();hp=1;assert(ModBeginnerRescue(FALSE)==FALSE)
reset();hp=0;assert(ModBeginnerRescue(FALSE)==FALSE)
reset();hp=0;values[HasReceivedAnyDamage]=FALSE;assert(ModBeginnerRescue(TRUE)==FALSE)
for _,effect in ipairs({100690,9621,19700,102351,9913}) do
 reset();hp=0;effects[effect]=true;assert(ModBeginnerRescue(TRUE)==FALSE)
end
for _,key in ipairs({IsOnLadder,IsOnMount,CONDITION_TYPE_STONE,CONDITION_TYPE_CRYSTAL,GetDamageSpecialAttribute}) do
 reset();hp=0;values[key]=TRUE;assert(ModBeginnerRescue(TRUE)==FALSE)
end
reset();hp=0;values[GetReceivedDamageType]=DAMAGE_TYPE_DEATH_FALLING;assert(ModBeginnerRescue(TRUE)==FALSE)
reset();hp=0;values[GetFallHeight]=2000;assert(ModBeginnerRescue(TRUE)==FALSE)
reset();effects[1627122]=nil;assert(ModBeginnerRescue(FALSE)==FALSE)
'''
        self.run_lua(bindings+'\n'+fn+'\n'+harness)

if __name__ == '__main__':
    unittest.main()
