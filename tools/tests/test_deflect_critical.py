"""Exercise the actual critical HKS helpers with mocks; not engine qualification."""
import re
import unittest
import test_beginner_rescue_logic as rescue


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class DeflectCritical(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua

    def test_snapshot_consumption_and_complete_animation_cleanup(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        helpers = source[source.index('sovereignDeflectCriticalInitialized = false'):source.index('function ThrowBackStab_Activate()')]
        hooks = '\n'.join(re.search(r'function ' + name + r'\(\)\n.*?\nend', source, re.S).group()
                          for name in ['ThrowAtk_onActivate', 'ThrowDef_onActivate', 'Throw_Deactivate'])
        harness = r'''
TRUE=1; FALSE=0; GetThrowAnimID='animation'; GetSpEffectID='effect'; GetHP='hp'
ClearSpEffect='clear'; AddSpEffect='add'; RequestThrowAnimInterrupt='interrupt'
local effects, animation, hp, grants = {}, 31700, 500, 0
function env(key,id)
 if key=='animation' then return animation end
 if key=='hp' then return hp end
 if key=='effect' then return effects[id] and 1 or 0 end
 error('Unexpected read')
end
function act(key,id)
 if key=='clear' then effects[id]=nil
 elseif key=='add' then effects[id]=true; grants=grants+1
 else assert(key=='interrupt') end
end
function Replanning() end
for _, id in ipairs({31700,31710,31720,31730,31750,31760}) do
 for tier=1,4 do
  effects={}; animation=id; effects[102006+tier]=true
  ThrowAtk_onActivate()
  assert(effects[1627610+tier])
  for charge=102007,102010 do assert(not effects[charge]) end
  -- Original charge expiration and multiple damage hits do not resnapshot.
  for hit=1,3 do assert(effects[1627610+tier]) end
  Throw_Deactivate()
  for buff=1627611,1627614 do assert(not effects[buff]) end
 end
end
for _, id in ipairs({-1,0,40090,45080,45180,12345}) do
 effects={[102010]=true}; animation=id; local before=grants
 ThrowAtk_onActivate(); assert(effects[102010] and grants==before)
end
animation=31700; effects={}; local before=grants
ThrowAtk_onActivate(); assert(grants==before)
effects={[102007]=true,[102010]=true}; ThrowAtk_onActivate()
assert(effects[1627614] and not effects[1627611])
ThrowDef_onActivate(); assert(not effects[1627614])
effects={[1627613]=true}; sovereignDeflectCriticalInitialized=false
if not sovereignDeflectCriticalInitialized then ModDeflectCriticalClear() end
assert(not effects[1627613] and sovereignDeflectCriticalInitialized)
hp=0; effects={[102010]=true}; before=grants
ThrowAtk_onActivate(); assert(effects[102010] and grants==before)
'''
        self.run_lua(helpers + '\n' + hooks + '\n' + harness)
        self.assertNotIn('ModDeflectCriticalStart()', source.split('function ThrowBackStab_Activate()', 1)[1].split('function Throw_Activate()', 1)[0])


if __name__ == '__main__':
    unittest.main()
