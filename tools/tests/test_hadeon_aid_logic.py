"""Exercise aid source with delayed native-resource mocks; not an engine test."""
import re
import unittest
import test_beginner_rescue_logic as rescue

ROOT = rescue.ROOT


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class HadeonAidLogic(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua
    def test_aid_ramp_resources_and_withdrawal(self):
        source = (ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        fn = source.split('-- Hadeon aid is driven', 1)[1].split('-- Beginner rescue:', 1)[0]
        fn = '-- Hadeon aid is driven' + fn
        names = set(re.findall(r'(?:env|act)\((\w+)', fn)) - {'10000'}
        bindings = '\n'.join(f'{name}="{name}"' for name in names)
        harness = r'''
TRUE=1;FALSE=0;FP=0x148;FP_MAX=0x14C
local effects, current, maximum, base, auraAdds, lag, age, damage, freeze
function reset()
 effects={};current={500,100,100};maximum={500,100,100};base={500,100,100}
 auraAdds=0;lag=0;age=0;damage=nil;freeze=false
 sovereignAidPermissionGrace=0;sovereignAidCalls=0;sovereignAidStage=-1;sovereignAidTimer=0;sovereignAidDirection=0
 sovereignAidInterval=.5;sovereignAidPending=false;sovereignAidFractions={0,0,0}
end
function GetDeltaTime() return .05 end
function env(key,...)
 local args={...};local id=args[1]
 if key==GetHP then return current[1] end
 if key==GetFP then return current[2] end
 if key==GetStamina then return current[3] end
 if key==GetMaxStamina then return maximum[3] end
 if key==GetSpEffectID then return effects[id] and TRUE or FALSE end
 if key==TraversePointerChain then
  if args[#args]==0x13C then return maximum[1] end
  if args[#args]==FP_MAX then return maximum[2] end
 end
 error('Unknown env '..tostring(key))
end
function act(key,...)
 local args={...};local id=args[1]
 if key==AddSpEffect then effects[id]=true;if id==1627131 then auraAdds=auraAdds+1 end;return end
 if key==ClearSpEffect then effects[id]=nil;return end
 if key==ChangeHP then current[1]=current[1]+id;return end
 if key==10000 then
  if args[#args]==FP then current[2]=args[3] else assert(args[#args]==0x154);current[3]=args[3] end
  return
 end
 error('Unknown act '..tostring(key))
end
function native()
 local stage=0;local count=0
 for i=1,20 do if effects[1627140+i] then stage=i;count=count+1 end end
 assert(count<=1,'Stacked tiers')
 if sovereignAidPending then age=age+.05 else age=0 end
 if not freeze and age>=lag then
  for i=1,3 do maximum[i]=math.floor(base[i]*(1+.05*stage)+.00001);current[i]=math.min(current[i],maximum[i]) end
 end
 if damage then for i=1,3 do current[i]=current[i]-damage[i] end;damage=nil end
end
function frame() native();ModHadeonAid() end
function advance(s) for i=1,math.floor(s/.05+.5) do frame() end end
function near(a,b) assert(math.abs(a-b)<=1,'Expected '..b..', got '..a) end

-- Inactive aid survives the actual missing-global fallback and reads only permission.
reset();frame();local realEnv=env;local reads=0
function env(key,id,...)
 assert(key==GetSpEffectID and id==1627130,'Inactive aid did extra native work')
 reads=reads+1;return FALSE
end
for i=1,300 do ModHadeonAid() end
assert(reads==300 and sovereignAidStage==0 and not sovereignAidPending)
env=realEnv
-- A script recreated with an existing tier must still finish its withdrawal.
reset();effects[1627145]=true;effects[1627131]=true;advance(10.3)
assert(sovereignAidStage==0 and not effects[1627131])

reset();effects[1627130]=true;advance(10.5)
assert(sovereignAidStage==20 and auraAdds==1)
assert(maximum[1]==1000 and maximum[2]==200 and maximum[3]==200)
for i=1,3 do assert(current[i]==maximum[i]) end
advance(2);assert(auraAdds==1)
effects[1627130]=nil;advance(10.5)
assert(sovereignAidStage==0 and not effects[1627131]);assert(current[1]==500)

-- Short permission gaps must not restart the ramp, even before its first tier.
reset()
for i=1,220 do
 effects[1627130]=(i%7<6) and true or nil
 frame()
end
assert(sovereignAidStage==20 and maximum[1]==1000)
-- Real departure expires grace, then safely withdraws; it cannot keep the aura alive.
effects[1627130]=nil;advance(10.5)
assert(sovereignAidStage==0 and not effects[1627131] and sovereignAidPermissionGrace==0)

-- Preserve partial bars and resource spending between snapshot and recalculation.
reset();current={250,50,30};effects[1627130]=true;advance(10.5)
near(current[1],500);near(current[2],100);near(current[3],60)
advance(2);near(current[1],500);near(current[2],100);near(current[3],60)
effects[1627130]=nil;advance(10.5)
near(current[1],250);near(current[2],50);near(current[3],30)
reset();effects[1627130]=true
while not sovereignAidPending do frame() end
damage={70,10,20};frame()
assert(current[1]==455 and current[2]==95 and current[3]==85)

-- Partial exit drains over ten seconds, reentry cannot refill the bars.
reset();effects[1627130]=true;advance(5.2);local start=sovereignAidStage
assert(start==10);current={200,20,20};effects[1627130]=nil;advance(5)
assert(sovereignAidStage>0 and sovereignAidStage<start)
effects[1627130]=true;advance(10.5);assert(sovereignAidStage==20);assert(current[1]<=270)
effects[1627130]=nil;advance(10.5);assert(current[1]<=140)

-- Withdrawal may lower maxima, but never kills a living player or revives a dead one.
reset();effects[1627130]=true;advance(10.5);current={1,0,0};effects[1627130]=nil
advance(10.5);assert(current[1]==1 and current[2]==0 and current[3]==0)
reset();effects[1627130]=true;advance(5.2);current[1]=0;advance(1);assert(current[1]==0)
effects={};current={500,100,100};frame();assert(sovereignAidStage==0)
assert(not effects[1627131])

-- Deferred maxima are awaited. A mismatching maximum never authorizes stale writes.
reset();lag=.15;effects[1627130]=true;advance(10.4);assert(current[1]==1000)
reset();freeze=true;effects[1627130]=true;advance(1);assert(current[1]==500)
assert(not sovereignAidPending)

-- Equipment-only FP/stamina changes must not receive blessing scaling.
for resource=2,3 do
 reset();current={250,50,50};effects[1627130]=true
 while not sovereignAidPending do frame() end
 base[resource]=120;frame()
 assert(current[resource]==50 and sovereignAidFractions[resource]==0)
 assert(current[1]==262)
 local other=5-resource;assert(current[other]==52)
 -- Subsequent ordinary steps work from the new maximum without a catch-up refill.
 advance(.5);assert(current[resource]==52)
 reset();current={250,50,50};effects[1627130]=true
 while not sovereignAidPending do frame() end
 base[resource]=80;frame()
 assert(current[resource]==50 and sovereignAidFractions[resource]==0)
 -- During withdrawal, skip the unrelated change but keep ordinary native clamping.
 reset();effects[1627130]=true;advance(10.5);effects[1627130]=nil
 current={375,75,75}
 while not sovereignAidPending do frame() end
 base[resource]=80;frame()
 assert(current[resource]==75)
end
'''
        fallback = source[source.rindex('global = {}'):]
        self.run_lua(bindings + '\n' + fn + '\n' + fallback + '\n' + harness)

    def test_effective_hp_markers_preserve_oath_and_curse_behavior(self):
        source = (ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        body = source.split('function ModHPStateInfo()', 1)[1].split(
            '-- Helper function for fetching maximum HP', 1)[0]
        harness = r'''
GetHP='hp';AddSpEffect='add';lastHP=9999;lastEffectiveHPMax=nil
hpEffectMap={hpMap={}};for i=0,9 do hpEffectMap.hpMap[i*10]=230+i end
local hp,effective,base=250,750,500
local updates,rolls=0,0
function env() return hp end
function ModGetHPMax() return base end
function ModGetEffectiveHPMax() return effective end
function act(_,id) observed=id;updates=updates+1 end
function ModFrenziedFlameCurse() rolls=rolls+1 end
ModHPStateInfo()
assert(observed==233 and maxHP==500 and rolls==1 and updates==1)
ModHPStateInfo();assert(rolls==1 and updates==1)
effective=500;ModHPStateInfo()
assert(observed==235 and maxHP==500 and rolls==1 and updates==2)
hp=240;ModHPStateInfo();assert(observed==234 and rolls==2)
hp=750;effective=750;ModHPStateInfo();assert(observed==239 and maxHP==500)
effective=0;ModHPStateInfo();assert(observed==239 and maxHP==500)
effective=nil;ModHPStateInfo();assert(observed==239 and maxHP==500)
'''
        self.run_lua('function ModHPStateInfo()' + body + harness)
