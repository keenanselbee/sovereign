"""Source-level diagnostic failure tests; not an HKS engine qualification."""
import unittest
import test_beginner_rescue_logic as rescue


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class PlayerDiagnostics(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua

    def test_heartbeat_isolation_errors_and_limits(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        trace = source.split('-- Temporary player-only diagnostics.', 1)[1].split('function Update()', 1)[0]
        harness = r'''
TRUE=1;FALSE=0;IsCOMPlayer='npc';IsGhost='ghost';GetHP='hp';GetSpEffectID='effect'
GetFP='fp';GetStamina='stamina';GetMaxStamina='staminaMax';TraversePointerChain='pointer'
local npc,ghost,hp=1,0,500
local opened,files,errors=0,{},0
local throwRead,throwWrite,throwOpen=false,false,false
function env(key,id)
 if key=='npc' then return npc elseif key=='ghost' then return ghost elseif key=='hp' then return hp end
 if key=='effect' then return id==1627130 and 1 or 0 end
 if key=='fp' and throwRead then error('FP read failed') end
 if key=='pointer' and throwRead then return nil,'native pointer unavailable' end
 return 100
end
function GetDeltaTime() return .5 end
function GetVariable() return 1 end
function GetLocomotionState() return 0 end
function GetHalfBlendInfo() return 0,0 end
function ModGetEffectiveHPMax()
 -- The startup heartbeat was flushed before the first optional resource read.
 assert(files['Sovereign-hadeon-aid.log'].flushed:find('diagnostic started',1,true))
 return 500
end
function act() errors=errors+1 end
io={open=function(path)
 if throwOpen then return nil,'permission denied' end
 opened=opened+1
 local file={text='',flushed='',closed=false}
 function file:write(text)
  if throwWrite then error('write failed') end
  self.text=self.text..text
 end
 function file:flush() self.flushed=self.text end
 function file:close() self.closed=true end
 files[path]=file;return file
end}
ModPlayerDiagnostics();assert(opened==0)
npc=0;ghost=1;ModPlayerDiagnostics();assert(opened==0)
ghost=0;hp=0;ModPlayerDiagnostics();assert(opened==0)
hp=500;throwRead=true;sovereignUpdateCheckpoint='ModJump'
assert(not sovereignMovementTrace.enabled)
ModPlayerDiagnostics();assert(opened==2)
ModMotionTrace('callback','Idle_onUpdate');ModMotionTrace('gate','Idle:ExecPassiveAction')
assert(sovereignMotion.callback=='Idle_onUpdate' and sovereignMotion.callbackAt>=0)
local aid=files['Sovereign-hadeon-aid.log'].flushed
assert(aid:find('FP read failed',1,true) and aid:find('native pointer unavailable',1,true))
assert(aid:find('staminaMax=100',1,true) and aid:find('checkpoint=ModJump',1,true))
assert(files['Sovereign-movement.log'].flushed:find('input=1',1,true))
throwRead=false
for i=1,3050 do ModPlayerDiagnostics() end
assert(opened==2 and sovereignMovementTrace.samples==3000 and sovereignAidTrace.samples==600)
assert(files['Sovereign-movement.log'].closed and files['Sovereign-hadeon-aid.log'].closed)
assert(files['Sovereign-hadeon-aid.log'].flushed:find('fp=100',1,true))
assert(files['Sovereign-movement.log'].flushed:find('callback=Idle_onUpdate',1,true))
assert(not sovereignMovementTrace.enabled)
ModMotionTrace('callback','should_not_record');assert(sovereignMotion.callback=='Idle_onUpdate')
-- I/O failures never escape into the gameplay callback; fallback is bounded.
sovereignMovementTrace={path='unwritable',limit=3000,enabled=false,time=0,next=0,samples=0,buffer=''}
throwOpen=true;assert(pcall(ModPlayerDiagnostics));assert(sovereignMovementTrace.samples==3000 and errors==1)
throwOpen=false;throwWrite=true
sovereignMovementTrace={path='writefail',limit=3000,enabled=false,time=0,next=0,samples=0,buffer=''}
assert(pcall(ModPlayerDiagnostics));assert(sovereignMovementTrace.samples==3000 and errors==2)
assert(files['writefail'].closed)
'''
        aid_state = source[source.index('sovereignAidPermissionGrace = 0'):source.index('function ModAidResources()')]
        fallback = source[source.rindex('global = {}'):]
        self.run_lua(aid_state + '-- Temporary player-only diagnostics.' + trace + fallback + '\n' + harness)

    def test_logging_precedes_update_and_preserves_checkpoints(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        update = source.split('function Update()', 1)[1].split('\nfunction ', 1)[0]
        self.assertLess(update.index('ModPlayerDiagnostics()'), update.index('GetConstVariable()'))
        self.assertEqual(update.count('ModPlayerDiagnostics()'), 1)
        for name in ('ModJump', 'ModUltimateAttack', 'ModAnimationControl',
                     'ModMovementMultiplier', 'ModDisableMaleniaDeflectLifesteal',
                     'ModHadeonAid', 'ModBeginnerRescue', 'ModHPStateInfo',
                     'ModDefaultMagicSlot', 'ModButtonHold'):
            self.assertLess(update.index('sovereignUpdateCheckpoint = "' + name + '"'),
                            update.index(name + '('))
        self.assertIn('sovereignUpdateCheckpoint = "complete"', update)

    def test_motion_trace_preserves_idle_decisions(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        functions = []
        for name in ('ModMotionTrace', 'MoveStart', 'IdleCommonFunction'):
            body = source.split('function ' + name + '(', 1)[1].split('\nfunction ', 1)[0]
            functions.append('function ' + name + '(' + body)
        harness = r"""
TRUE=1;FALSE=0;ALLBODY=0;LOWER=1;PLAYER_STATE_MOVE=1
c_IsStealth=FALSE;Event_Move={'W_Move'}
sovereignMovementTrace={enabled=true};sovereignMotion={};sovereignDiagnosticTime=3
local requests,passive,input=0,FALSE,1
function env() return FALSE end
function act() end
function GetVariable(name) if name=='MoveSpeedLevel' then return input end;return 0 end
function SetVariable() end
function GetLocomotionState() return 0 end
function ExecPassiveAction() return passive end
function ExecEventHalfBlend() requests=requests+1 end
function ExecEventHalfBlendNoReset() requests=requests+1 end
function ResetRequest() end
function SpeedUpdate() end
setmetatable(_G,{__index=function() return function() return FALSE end end})
assert(IdleCommonFunction()==TRUE and requests==1)
assert(sovereignMotion.moveStart=='requested')
passive=TRUE;sovereignMotion={}
assert(IdleCommonFunction()==TRUE and requests==1)
assert(sovereignMotion.gate:find('ExecPassiveAction',1,true))
passive=FALSE;input=0;sovereignMotion={}
assert(IdleCommonFunction()==FALSE and requests==1)
assert(sovereignMotion.moveStart=='no_input')
"""
        self.run_lua('\n'.join(functions) + harness)
