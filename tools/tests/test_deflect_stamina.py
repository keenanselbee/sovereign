"""Exercise deflect routing/floor with mocked game calls, not engine proof."""
import re
import unittest
import test_beginner_rescue_logic as rescue


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class DeflectStamina(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua

    def test_depleted_timed_guard_and_success_floor(self):
        source = (rescue.ROOT/'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        def function(name):
            return re.search(r'^function ' + name + r'\([^\n]*\)[\s\S]*?(?=^function )',
                             source, re.MULTILINE).group()
        functions = function('ModDeflectDamageType') + function('SetJustGuardSucceedEffect')
        names = set(re.findall(r'(?:env|act)\((\w+)', functions))
        bindings = '\n'.join(f'{name}="{name}"' for name in names)
        harness = r'''
TRUE=1; FALSE=0
DAMAGE_TYPE_GUARDBREAK=1001; DAMAGE_TYPE_GUARD=3
HAND_RIGHT_BOTH=3;c_Style=1
local effects, hp, stamina, guard, changes
function reset()
 effects={[102001]=true};hp=100;stamina=0;guard=3;changes=0
end
function env(key,arg)
 if key==GetSpEffectID then return effects[arg] and TRUE or FALSE end
 if key==GetHP then return hp end
 if key==GetStamina then return stamina end
 if key==GetGuardLevelAction then return guard end
 if key==GetStateChangeType then return FALSE end
 error('Unknown env '..tostring(key))
end
function act(key,arg)
 if key==ChangeStamina then stamina=stamina+arg;changes=changes+1;return end
 if key==AddSpEffect then effects[arg]=true;return end
 error('Unknown act '..tostring(key))
end
for _,marker in ipairs({102001,102011,102013,102015}) do
 reset();effects={[marker]=true}
 assert(ModDeflectDamageType(1001,FALSE,FALSE)==3)
 assert(stamina==0 and changes==0,'Routing alone must not grant stamina')
 SetJustGuardSucceedEffect(2)
 assert(stamina==1 and changes==1 and effects[102019])
 -- Another successful depleted hit can be defended; it does not refill the bar.
 stamina=0;SetJustGuardSucceedEffect(2);assert(stamina==1 and changes==2)
end
for _,kind in ipairs({'ordinary','positive','zero-level','dead','parry','shield-poke','175','176'}) do
 reset();local parry=FALSE;local poke=FALSE
 if kind=='ordinary' then effects={} end
 if kind=='positive' then stamina=10 end
 if kind=='zero-level' then guard=0 end
 if kind=='dead' then hp=0 end
 if kind=='parry' then parry=TRUE end
 if kind=='shield-poke' then poke=TRUE end
 if kind=='175' then effects[175]=true end
 if kind=='176' then effects[176]=true end
 assert(ModDeflectDamageType(1001,parry,poke)==1001,kind)
 assert(changes==0,kind)
end
-- Direct damage, wall recoil and special break types are never reclassified.
for _,kind in ipairs({0,1,2,3,4,5,1000,1002,1003,1004,1005}) do
 reset();assert(ModDeflectDamageType(kind,FALSE,FALSE)==kind);assert(changes==0)
end
for _,value in ipairs({1,5,50,100}) do
 reset();stamina=value;SetJustGuardSucceedEffect(1)
 assert(stamina==value and changes==0,'No ordinary-cost refund')
end
reset();stamina=-3;SetJustGuardSucceedEffect(1);assert(stamina==1 and changes==1)
reset();hp=0;SetJustGuardSucceedEffect(1);assert(stamina==0 and changes==0)
'''
        self.run_lua(bindings + '\n' + functions + '\n' + harness)

    def test_router_precedes_break_dispatch(self):
        source = (rescue.ROOT/'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        body = source.split('function ExecDamage(is_parry, is_attackwhileguard)', 1)[1]
        body = body.split('\nfunction ', 1)[0]
        route = 'damage_type = ModDeflectDamageType(damage_type, is_parry, is_attackwhileguard)'
        self.assertEqual(body.count(route), 1)
        self.assertLess(body.index(route), body.index('if damage_type >= DAMAGE_TYPE_GUARDED'))
        self.assertLess(body.index(route), body.index('elseif damage_type == DAMAGE_TYPE_GUARD then'))


if __name__ == '__main__':
    unittest.main()
