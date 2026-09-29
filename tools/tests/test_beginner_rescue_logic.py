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
        deaths = 'function ModHadeonAidDeaths()' + source.split(
            'function ModHadeonAidDeaths()', 1)[1].split('function ModHadeonAidCap()', 1)[0]
        body = source.split('function ModBeginnerRescue(lethal)', 1)[1].split('function ExecDeath()', 1)[0]
        fn = deaths + 'function ModBeginnerRescue(lethal)' + body
        names = set(re.findall(r'(?:env|act)\((\w+)', fn))
        names |= {'CONDITION_TYPE_STONE', 'CONDITION_TYPE_CRYSTAL', 'DAMAGE_TYPE_DEATH_FALLING'}
        bindings = '\n'.join(f'{name}="{name}"' for name in names)
        harness = r'''
TRUE=1; FALSE=0
local effects, flags, hp, maxhp, values, healed
function reset()
 effects={[1627122]=true};flags={};hp=100;maxhp=500;values={};healed=0
end
function ModGetEffectiveHPMax() return maxhp end
function env(key,arg)
 if key==GetSpEffectID then return effects[arg] and TRUE or FALSE end
 if key==GetEventFlag then return flags[arg] and TRUE or FALSE end
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
-- The first room attempt blocks both threshold and lethal rescue, without
-- consuming cooldowns; leaving the arena restores ordinary rescue behavior.
reset();flags['1055425223']=true;assert(ModBeginnerRescue(FALSE)==FALSE)
assert(not effects[1627126] and not effects[1627127])
hp=0;assert(ModBeginnerRescue(TRUE)==FALSE and healed==0)
flags['1055425223']=nil;hp=100;assert(ModBeginnerRescue(FALSE)==TRUE)
reset();flags['1055425223']=true;hp=0;assert(ModBeginnerRescue(TRUE)==FALSE)
flags['1055425223']=nil;assert(ModBeginnerRescue(TRUE)==TRUE)
reset();assert(ModBeginnerRescue(FALSE)==TRUE);assert(hp==500 and healed==1)
assert(effects[1627125] and effects[1627126] and effects[1627127] and effects[1627124])
hp=-10;assert(ModBeginnerRescue(TRUE)==FALSE);assert(healed==1)
-- Once the shared floor expires, the chosen 40-second cooldown still blocks.
effects[1627126]=nil;hp=100;assert(ModBeginnerRescue(FALSE)==FALSE)
effects[1627123]=true;flags['1055425233']=true
assert(ModBeginnerRescue(FALSE)==FALSE)
effects[1627127]=nil;assert(ModBeginnerRescue(FALSE)==TRUE and healed==2)
assert(effects[1627127]) -- Zero deaths still use the global 40-second default.
-- Admission plus one through ten counted deaths selects 38 through 20 seconds.
for count=1,10 do
 reset();flags['1055425233']=true
 for death=1,count do
  local id=death<=5 and 1055420929+death or 1055420946+death
  flags[tostring(id)]=true
 end
 assert(ModBeginnerRescue(FALSE)==TRUE)
 assert(effects[1627160+count] and not effects[1627127])
 effects[1627126]=nil;hp=100;flags['1055425233']=nil
 assert(ModBeginnerRescue(FALSE)==FALSE) -- Leaving cannot shorten the active timer.
 flags['1055425233']=true
 assert(ModBeginnerRescue(FALSE)==FALSE) -- Re-entry cannot restart it.
 effects[1627160+count]=nil
 assert(ModBeginnerRescue(FALSE)==TRUE)
end
-- Without arena admission, saved losses do not shorten the global default.
reset();flags['1055420930']=true;assert(ModBeginnerRescue(FALSE)==TRUE)
assert(effects[1627127] and not effects[1627161])
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
