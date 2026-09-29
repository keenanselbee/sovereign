"""Mocked diagnostic behavior; not an HKS engine qualification."""
import unittest
import test_beginner_rescue_logic as rescue


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class HadeonDialogueTrace(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua

    def test_transitions_death_errors_and_reversible_limit(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        block = source.split('-- BEGIN REVERSIBLE HADEON DIALOGUE TRACE', 1)[1].split('-- END REVERSIBLE HADEON DIALOGUE TRACE', 1)[0]
        self.assertEqual(source.count('    ModHadeonDialogueTrace()'), 1)
        harness = r'''
FALSE=0; IsCOMPlayer='npc'; IsGhost='ghost'; GetEventFlag='flag'; GetHP='hp'
local npc, ghost, hp = 0, 0, 500
local flags={['1055420940']=1,['1055425201']=1,['1055422946']=1,
 ['1055425100']=1,['1055425195']=1,['1055425265']=1,
 ['1055425275']=1,['1055425277']=1,['1055425279']=1,['1055425280']=1}
local lightReads=0
local text, opens, flushes, closes = '', 0, 0, 0
local throwRead, throwWrite = false, false
sovereignMovementCapture={path='session'}
function GetDeltaTime() return .11 end
function env(key,id)
 if key=='npc' then return npc end
 if key=='ghost' then return ghost end
 if key=='hp' then return hp end
 assert(key=='flag' and type(id)=='string' and #id==10)
 assert(id:sub(1,6)=='105542')
 local suffix=tonumber(id:sub(7))
 if suffix>=5100 and suffix<=5195 then lightReads=lightReads+1 end
 assert((suffix>=940 and suffix<=951) or (suffix>=5200 and suffix<=5222)
   or suffix==2946 or suffix==938 or suffix==5042 or suffix==935
   or (suffix>=5100 and suffix<=5195) or (suffix>=5262 and suffix<=5297)
   or suffix==5253 or suffix==5254 or suffix==5258 or suffix==5259
   or suffix==2997 or suffix==915 or suffix==918)
 if throwRead then error('read failed') end
 return flags[id] or 0
end
io={open=function(path,mode)
 assert(path=='session.dialogue.log' and mode=='a'); opens=opens+1
 return {write=function(self,s) if throwWrite then error('disk failure') end; text=text..s end,
 flush=function() flushes=flushes+1 end,close=function() closes=closes+1 end}
end}
sovereignDialogueTraceEnabled=false; ModHadeonDialogueTrace(); assert(opens==0)
sovereignDialogueTraceEnabled=true; npc=1; ModHadeonDialogueTrace(); assert(opens==0)
npc=0; ghost=1; ModHadeonDialogueTrace(); assert(opens==0)
ghost=0; ModHadeonDialogueTrace(); assert(opens==1 and flushes==1)
assert(text:find('lights=2 lightTier=3 lightReady=0',1,true)); assert(text:find('entrance=1000',1,true)); assert(text:find('selected=0100000000000000',1,true))
assert(lightReads==96)
assert(text:find('vortexArmed=0 vortexCooldownReset=0 vortexCue=1 vortexInvalidArena=0 vortexNoLanding=1 vortexSuccess=0',1,true))
assert(text:find('vortexWorkerReady=1 vortexLiveSeen=1 vortexCueSeen=0',1,true))
assert(text:find('periodicRequest=0 periodicAck=0 periodicTimer=0 periodicExpired=0',1,true))
assert(text:find('vortexQueued=0 vortexNextActivate=0',1,true))
ModHadeonDialogueTrace(); assert(flushes==1 and lightReads==96)
flags['1055420940']=0; flags['1055420941']=1; flags['1055425201']=0; flags['1055425202']=1
ModHadeonDialogueTrace(); assert(flushes==2)
assert(text:find('previous={entrance=1000',1,true)); assert(text:find('current={entrance=0100',1,true))
hp=0; flags['1055420938']=1; ModHadeonDialogueTrace()
assert(text:find('deathReload=1',1,true) and text:find('dead=true',1,true))
sovereignDialogueTrace.limit=4; hp=500; ModHadeonDialogueTrace(); assert(closes==1)
flags['1055420941']=0; ModHadeonDialogueTrace(); assert(opens==1 and sovereignDialogueTrace.rows==4)
sovereignDialogueTrace={time=0,next=0,rows=0,limit=1024,previous='unobserved',file=nil,failed=false}
throwRead=true; ModHadeonDialogueTrace(); assert(sovereignDialogueTrace.failed and opens==1)
sovereignDialogueTrace={time=0,next=0,rows=0,limit=1024,previous='unobserved',file=nil,failed=false}
throwRead=false; throwWrite=true; ModHadeonDialogueTrace(); assert(sovereignDialogueTrace.failed)
assert(closes==2)
sovereignDialogueTrace={time=0,next=0,rows=0,limit=1024,previous='unobserved',file=nil,failed=false}
io.open=function() return {write=function() return nil,'disk full' end,flush=function() end,close=function() closes=closes+1 end} end
ModHadeonDialogueTrace(); assert(sovereignDialogueTrace.failed and closes==3)
'''
        self.run_lua(block + '\n' + harness)


if __name__ == '__main__':
    unittest.main()
