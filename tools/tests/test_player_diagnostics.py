"""Mocked Lua diagnostic checks; not an HKS engine qualification."""
import unittest
import test_beginner_rescue_logic as rescue


@unittest.skipUnless(rescue.LUA.is_file(), 'Existing Lua runtime is unavailable')
class PlayerDiagnostics(unittest.TestCase):
    run_lua = rescue.RescueLogic.run_lua

    def diagnostics_source(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        trace = source.split('-- Temporary player-only diagnostics.', 1)[1].split('function Update()', 1)[0]
        aid_state = source[source.index('sovereignAidPermissionGrace = 0'):source.index('function ModAidResources()')]
        fallback = source[source.rindex('global = {}'):]
        return aid_state + '-- Temporary player-only diagnostics.' + trace + fallback

    def test_heartbeat_isolation_errors_and_limits(self):
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        trace = source.split('-- Temporary player-only diagnostics.', 1)[1].split('function Update()', 1)[0]
        harness = r'''
TRUE=1;FALSE=0;IsCOMPlayer='npc';IsGhost='ghost';GetHP='hp';GetSpEffectID='effect'
GetEventFlag=10003
GetFP='fp';GetStamina='stamina';GetMaxStamina='staminaMax';TraversePointerChain='pointer'
local npc,ghost,hp=1,0,500
local opened,files,errors=0,{},0
local throwRead,throwWrite,throwOpen=false,false,false
os=nil
math.mod=math.fmod -- HKS exposes math.mod; the test DLL may not.
local flags={['1055422946']=1,['1055422947']=1,['1055422948']=0,
 ['1055422933']=0,['1055422949']=1,['1055425233']=1,
 ['1055420930']=1,['1055420931']=0,['1055420932']=0,
 ['1055420933']=0,['1055420934']=0}
function env(key,id)
 if key=='npc' then return npc elseif key=='ghost' then return ghost elseif key=='hp' then return hp end
 if key=='effect' then return id==1627130 and 1 or 0 end
 if key==10003 then
  assert(type(id)=='string' and flags[id]~=nil)
  if id=='1055422948' and throwRead then error('flag read failed') end
  return flags[id]
 end
 if key=='fp' and throwRead then error('FP read failed') end
 if key=='pointer' and throwRead then return nil,'native pointer unavailable' end
 return 100
end
function GetDeltaTime() return .5 end
function GetVariable() return 1 end
function GetLocomotionState() return 1 end
function GetHalfBlendInfo() return 0,0 end
function ModHadeonAidCap() return 4 end
function ModGetEffectiveHPMax()
 -- The startup heartbeat was flushed before the first optional resource read.
 assert(files[sovereignAidTrace.path].flushed:find('schema=2',1,true))
 return 500
end
function act() errors=errors+1 end
local occupied='Sovereign-movement-1.4.7-session-1.log'
files[occupied]={text='older session',closed=true,close=function() end}
io={open=function(path,mode)
 if mode=='r' then return files[path] end
 if throwOpen then return nil,'permission denied' end
 opened=opened+1
 local file={text='',flushed='',closed=false}
 function file:write(text)
  if throwWrite then error('write failed') end
  self.text=self.text..text;return self
 end
 function file:flush() self.flushed=self.text;return self end
 function file:close() self.closed=true;return self end
 files[path]=file;return file
end}
ModPlayerDiagnostics();assert(opened==0)
npc=0;ghost=1;ModPlayerDiagnostics();assert(opened==0)
ghost=0;hp=0;ModPlayerDiagnostics();assert(opened==0)
hp=500;throwRead=true;sovereignUpdateCheckpoint='ModJump'
assert(not sovereignMovementTrace.enabled)
ModPlayerDiagnostics();assert(opened==3,'opened='..opened)
local movement=sovereignMovementCapture.path
assert(movement=='Sovereign-movement-1.4.7-session-2.log','path='..movement)
assert(files[occupied].text=='older session')
ModMotionTrace('callback','Idle_onUpdate');ModMotionTrace('gate','Idle:ExecPassiveAction')
assert(sovereignMotion.callback=='Idle_onUpdate' and sovereignMotion.callbackAt>=0)
local aidPath=sovereignAidTrace.path
assert(aidPath==movement..'.aid.log')
local aid=files[aidPath].flushed
assert(aid:find('schema=2; detail=death-aid-motion',1,true))
assert(aid:find('admitted=1 aidCap=4 loss1=1 loss2=0',1,true))
assert(aid:find('FP read failed',1,true) and aid:find('native pointer unavailable',1,true))
assert(aid:find('permissionGrace=0 direction=0 timer=0',1,true))
assert(aid:find('scripted=0 hp=500 hpMax=500',1,true))
assert(aid:find('staminaMax=100',1,true) and aid:find('checkpoint=ModJump',1,true))
assert(files[movement].flushed:find('recorder=1.6.7 schema=6',1,true))
assert(files[movement..'.summary.log'].flushed:find('input=1',1,true))
throwRead=false
for i=1,3050 do ModPlayerDiagnostics() end
assert(opened==3 and sovereignMovementTrace.samples==3000 and sovereignAidTrace.samples==600)
assert(files[movement..'.summary.log'].closed and files[aidPath].closed)
assert(files[aidPath].flushed:find('fp=100',1,true))
assert(files[aidPath].flushed:find('scripted=0 hp=500 hpMax=500',1,true))
assert(files[movement..'.summary.log'].flushed:find('callback=Idle_onUpdate',1,true))
assert(not sovereignMovementTrace.enabled)
ModMotionTrace('callback','should_not_record');assert(sovereignMotion.callback=='Idle_onUpdate')
assert(sovereignMovementCapture.count<=sovereignMovementCapture.capacity)
assert(sovereignMovementCapture.bytes<=8388608)
assert(errors==0)
'''
        aid_state = source[source.index('sovereignAidPermissionGrace = 0'):source.index('function ModAidResources()')]
        fallback = source[source.rindex('global = {}'):]
        self.run_lua(aid_state + '-- Temporary player-only diagnostics.' + trace + fallback + '\n' + harness)

    def test_ring_trigger_post_window_recovery_and_hook_order(self):
        harness = r'''
TRUE=1;FALSE=0;os=nil;math.mod=math.fmod
local files={};local opens,reads=0,0
local input,speed,state=1,1,1
function GetDeltaTime() return .1 end
function GetVariable(name)
 reads=reads+1
 if name=='MoveSpeedLevel' then return input end
 if name=='MoveSpeedLevelReal' then return speed end
 return 0
end
function GetLocomotionState() return state end
function ModMovementDiagnosticFields() return ' input='..input..' speed='..speed end
io={open=function(path,mode)
 if mode=='r' then return files[path] end
 assert(mode=='a')
 opens=opens+1
 local f={text='',flushed='',closed=false}
 function f:write(s) self.text=self.text..s end
 function f:flush() self.flushed=self.text end
 function f:close() self.closed=true;return self end
 files[path]=f;return f
end}
sovereignMovementCapture.capacity=3
ModMovementCaptureTick(true)
local path=sovereignMovementCapture.path
assert(opens==1 and path:find('session-1.log',1,true))
for i=1,5 do ModMovementCaptureTick(true) end
assert(sovereignMovementCapture.count==3 and sovereignMovementCapture.captures==0)
ModMotionTrace('gate','ExecPassiveAction:ExecTalk')
ModMotionTrace('gate','IdleCommonFunction:ExecPassiveAction')
for i=1,32 do ModMotionTrace('event','event-'..i) end
assert(sovereignMovementCapture.hookCount==32 and sovereignMovementCapture.dropped==2)
speed=0;state=0
ModMovementCaptureTick(true);ModMovementCaptureTick(true)
assert(sovereignMovementCapture.captures==0)
ModMovementCaptureTick(true)
assert(sovereignMovementCapture.captures==1 and sovereignMovementCapture.post)
local log=files[path].flushed
local inner=log:find('gate=ExecPassiveAction:ExecTalk',1,true)
local outer=log:find('gate=IdleCommonFunction:ExecPassiveAction',1,true)
assert(inner and outer and inner<outer and log:find('dropped=2',1,true))
assert(log:find('BEGIN capture=1',1,true) and log:find('frame=7',1,true))
for i=1,31 do ModMovementCaptureTick(true) end
assert(not sovereignMovementCapture.post)
assert(files[path].flushed:find('END capture=1',1,true))
assert(sovereignMovementCapture.pendingCount==0)
speed=1;state=1
for i=1,6 do ModMovementCaptureTick(true) end
assert(sovereignMovementCapture.armed)
speed=0;state=0
for i=1,3 do ModMovementCaptureTick(true) end
assert(sovereignMovementCapture.captures==2)
assert(sovereignMovementCapture.count<=3 and sovereignMovementCapture.bytes<=8388608)
assert(reads>0 and opens==1)
'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_known_actions_preserve_capture_budget_but_not_stuck_recovery(self):
        harness = r'''
TRUE=1;FALSE=0;os=nil;math.mod=math.fmod;IsThrowing='throw'
local input,speed,state,throwing=1,1,1,0
local badAngle=false
function GetDeltaTime() return .1 end
function GetVariable(name)
 if name=='MoveSpeedLevel' then return input end
 if name=='MoveSpeedLevelReal' then return speed end
 return 0
end
function hkbGetVariable(name)
 assert(name=='TurnAngle')
 if badAngle then error('angle unavailable') end
 return 135
end
function env(key) if key=='throw' then return throwing end;return 0 end
function GetLocomotionState() return state end
function ModMovementDiagnosticFields() return '' end
local files={}
io={open=function(path,mode)
 if mode=='r' then return files[path] end
 local f={text=''}
 function f:write(s) self.text=self.text..s end
 function f:flush() end
 function f:close() end
 files[path]=f;return f
end}
local function ticks(n) for i=1,n do ModMovementCaptureTick(true) end end
ticks(1)
local trace=sovereignMovementCapture
local log=files[trace.path]
for cycle=1,10 do
 for _,event in ipairs({'W_AttackBothLight1','W_DeflectMediumUp','W_DamageLv2','W_Jump_F','W_FallStart'}) do
  speed=0;state=0;ModMotionTrace('event',event);ticks(8)
  speed=1;state=1;ticks(6)
 end
end
assert(trace.captures==0 and trace.filteredFrames>=400 and not trace.failed)
-- Live captures showed these native actions, including nested movement helpers.
for _,callback in ipairs({'Jump_F_onUpdate','Jump_D_onUpdate',
 'Stealth_to_Idle_onUpdate','Stealth_to_Stealth_Idle_onUpdate',
 'GuardBreak_onUpdate','GuardDamageMiddle_onUpdate','DamageLv6_Fling_onUpdate','Land_onUpdate'}) do
 speed=0;state=0
 for i=1,8 do
  ModMotionTrace('callback',callback)
  ModMotionTrace('callback','MoveCommonFunction')
  ticks(1)
 end
 speed=1;state=1;ticks(6)
end
speed=0;state=0
for i=1,25 do ModMotionTrace('eventUpdate','Event60060_onUpdate');ticks(1) end
speed=1;state=1;ticks(6)
assert(trace.captures==0,'ordinary transitions exhausted capture budget')

assert(log.text:find('turnAngle=135',1,true))
-- Old scalar callback/event values alone cannot suppress a new stop.
sovereignMotion.callback='DamageLv2_Middle_onUpdate';sovereignMotion.event='W_AttackBothLight1'
speed=0;state=0;ticks(3)
assert(trace.captures==1)
speed=1;state=1;ticks(40)
-- A fresh locomotion callback ends attack grace immediately.
speed=0;state=0;ModMotionTrace('event','W_AttackBothLight1');ticks(2)
assert(trace.captures==1)
ModMotionTrace('callback','Idle_onUpdate');ticks(3)
assert(trace.captures==2)
speed=1;state=1;ticks(40)
-- An ongoing critical is expected, but prolonged stalls remain observable.
speed=0;state=0;throwing=1;ticks(50)
assert(trace.captures==2)
ticks(15);assert(trace.captures==3)
speed=1;state=1;throwing=0;ticks(40)
-- Throw completion ends filtering even before its fallback timeout expires.
speed=0;state=0;throwing=1;ModMotionTrace('zeroBy','Throw_Activate');ticks(2)
throwing=0;ticks(3);assert(trace.captures==4)
speed=1;state=1;ticks(40)
-- Turn requests are intentionally not filtered; optional probe errors are isolated.
badAngle=true;speed=0;state=0;ModMotionTrace('event','W_Dash180');ticks(3)
assert(trace.captures==5 and not trace.failed)
assert(log.text:find('turnAngle=ERROR[',1,true))
assert(log.text:find('expectedPause=attack filtered=true',1,true))
-- A continuously updating native event still records a prolonged stall.
speed=1;state=1;ticks(40)
speed=0;state=0
for i=1,65 do ModMotionTrace('eventUpdate','Event60060_onUpdate');ticks(1) end
assert(trace.captures==6,'fresh event callbacks hid a prolonged pause')

'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_capture_write_accepts_void_success_and_rejects_explicit_errors(self):
        harness = r'''
local trace=sovereignMovementCapture
local writeMode,flushMode='void','void'
local file={text='',flushed=''}
function file:write(text)
 if writeMode=='throw' then error('write threw') end
 if writeMode=='false' then return false,'write rejected' end
 if writeMode=='error' then return nil,'write error' end
 self.text=self.text..text
end
function file:flush()
 if flushMode=='throw' then error('flush threw') end
 if flushMode=='false' then return false,'flush rejected' end
 if flushMode=='error' then return nil,'flush error' end
 self.flushed=self.text
end
trace.file=file;trace.bytes=0
ModMovementCaptureWrite('first')
assert(trace.bytes==5 and file.flushed=='first')
writeMode='false'
local ok,reason=pcall(ModMovementCaptureWrite,'bad')
assert(not ok and reason:find('write rejected',1,true) and trace.bytes==5)
writeMode='error'
ok,reason=pcall(ModMovementCaptureWrite,'bad')
assert(not ok and reason:find('write error',1,true) and trace.bytes==5)
writeMode='throw'
ok,reason=pcall(ModMovementCaptureWrite,'bad')
assert(not ok and reason:find('write threw',1,true) and trace.bytes==5)
writeMode='void';flushMode='false'
ok,reason=pcall(ModMovementCaptureWrite,'next')
assert(not ok and reason:find('flush rejected',1,true) and trace.bytes==5)
flushMode='error'
ok,reason=pcall(ModMovementCaptureWrite,'next')
assert(not ok and reason:find('flush error',1,true) and trace.bytes==5)
flushMode='throw'
ok,reason=pcall(ModMovementCaptureWrite,'next')
assert(not ok and reason:find('flush threw',1,true) and trace.bytes==5)
trace.bytes=8388608
ok,reason=pcall(ModMovementCaptureWrite,'overflow')
assert(not ok and reason:find('byte limit',1,true) and trace.bytes==8388608)
'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_disabled_capture_does_not_probe_or_open(self):
        harness = r'''
local reads,opens=0,0
sovereignMovementCaptureEnabled=false
function GetDeltaTime() reads=reads+1;error('disabled read') end
function GetVariable() reads=reads+1;error('disabled read') end
io={open=function() opens=opens+1;error('disabled open') end}
assert(pcall(ModMovementCaptureTick,true))
assert(pcall(ModMotionTrace,'gate','blocked'))
assert(reads==0 and opens==0 and not sovereignMovementCapture.active)
assert(sovereignMovementCapture.hookCount==0)
'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_capture_errors_are_contained_and_limits_close(self):
        harness = r'''
TRUE=1;FALSE=0;os=nil;math.mod=math.fmod
local failOpen,failWrite,failRead=false,false,false
local opens,errors=0,0
local files={}
function GetDeltaTime() return .1 end
function GetVariable(name)
 if failRead and name=='MoveSpeedLevel' then error('input probe failed') end
 return 1
end
function GetLocomotionState() return 1 end
function ModMovementDiagnosticFields() return '' end
function act() errors=errors+1 end
io={open=function(path,mode)
 if mode=='r' then return files[path] end
 if failOpen then return nil,'permission denied' end
 opens=opens+1
 local f={text='',closed=false}
 function f:write(s)
  if failWrite then error('disk full') end
  self.text=self.text..s;return self
 end
 function f:flush() return self end
 function f:close() self.closed=true;return self end
 files[path]=f;return f
end}
failOpen=true
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and errors==1 and opens==0)
sovereignMovementCapture.failed=false;failOpen=false;failWrite=true
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and errors==2 and opens==1)
assert(files[sovereignMovementCapture.path].closed)
sovereignMovementCapture.failed=false;failWrite=false;failRead=true
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and errors==3)
failRead=false;sovereignMovementCapture.failed=false
sovereignMovementCapture.time=1800
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and not sovereignMovementCapture.active)
assert(files[sovereignMovementCapture.path].closed)
assert(sovereignMovementCapture.bytes<=8388608)
sovereignMovementCapture.failed=false;sovereignMovementCapture.time=0
sovereignMovementCapture.bytes=8388607;sovereignMovementCapture.file=false
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and errors==4)
assert(sovereignMovementCapture.bytes<=8388608)
sovereignMovementCapture.failed=false;sovereignMovementCapture.bytes=0
sovereignMovementCapture.captures=12;sovereignMovementCapture.file=false
assert(pcall(ModMovementCaptureTick,true))
assert(sovereignMovementCapture.failed and sovereignMovementCapture.captures==12)
assert(files[sovereignMovementCapture.path].closed)
'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_event_activation_snapshot_exit_and_probe_isolation(self):
        harness = r'''
GetEventID='event';CheckForEventAnimPlaybackRequest='request'
GetCommandIDFromEvent='command';IsMoveCancelPossible='cancel'
GetEventEzStateFlag='ez';GetObjActRemainingInterpolateTime='blend'
local reads,anim,speed=0,60000,1
local fail=false
function env(key)
 reads=reads+1
 if key=='event' then return anim end
 if key=='request' then return 1 end
 if key=='command' then return -1 end
 if key=='blend' and fail then error('optional blend probe failed') end
 return 0
end
function GetVariable(key) if key=='MoveSpeedLevelReal' then return speed end;return 1 end
function act() error('observer attempted gameplay action') end
function SetVariable() error('observer attempted variable write') end
sovereignMovementCapture.active=true;sovereignMovementTrace.enabled=true
sovereignMovementCaptureEnabled=false
ModMovementEventTrace('eventEnter','Event60000_onActivate')
assert(reads==0 and sovereignMotion.eventEnter==nil)
sovereignMovementCaptureEnabled=true;sovereignMovementCapture.active=false
ModMovementEventTrace('eventEnter','Event60000_onActivate')
assert(reads==0)
sovereignMovementCapture.active=true;sovereignDiagnosticTime=10
ModMovementEventTrace('eventEnter','Event60000_onActivate')
assert(sovereignMotion.eventEnter=='Event60000_onActivate')
assert(sovereignMotion.eventEnterAt==10)
assert(sovereignMotion.eventEnterContext:find('anim=60000 request=1 command=-1 input=1 speed=1',1,true))
local entry=sovereignMotion.eventEnterContext
anim=-1;speed=0;fail=true;sovereignDiagnosticTime=12
assert(pcall(ModMovementEventTrace,'eventExit','Event60000_onDeactivate'))
assert(sovereignMotion.eventExit=='Event60000_onDeactivate' and sovereignMotion.eventExitAt==12)
assert(sovereignMotion.eventExitContext:find('optional blend probe failed',1,true))
assert(sovereignMotion.eventEnterContext==entry,'exit overwrote entry snapshot')
ModMotionTrace('eventUpdate','Event60001_onUpdate')
assert(sovereignMotion.eventUpdateAt==12)
assert(sovereignMovementCapture.hooks[1]=='eventEnter=Event60000_onActivate')
assert(sovereignMovementCapture.hooks[3]=='eventExit=Event60000_onDeactivate')
-- Later engine values cannot replace the original entry snapshot.
assert(sovereignMotion.eventEnterContext:find('anim=60000',1,true))
'''
        self.run_lua(self.diagnostics_source() + '\n' + harness)

    def test_every_event_reset_caller_identified_before_reset(self):
        import re
        source = (rescue.ROOT / 'mod/action/script/c0000.hks').read_text(encoding='utf-8')
        callers = 0
        for name, body in re.findall(r'^function (\w+)\([^\n]*\)\n(.*?)(?=^function |\Z)', source, re.M | re.S):
            if '    ResetEventState()' not in body:
                continue
            callers += 1
            hook = f'ModMovementEventTrace("eventEnter", "{name}")'
            self.assertIn(hook, body)
            self.assertLess(body.index(hook), body.index('ResetEventState()'))
        self.assertGreater(callers, 50)

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
sovereignMovementCaptureEnabled=true
sovereignMovementCapture={active=true,hooks={},hookCount=0,dropped=0}
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
