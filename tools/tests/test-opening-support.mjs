import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';
const source=fs.readFileSync('src/events/common.emevd.dcx.js','utf8');
const mapSource=fs.readFileSync('src/events/m18_00_00_00.emevd.dcx.js','utf8');
function suspend(code,name,wrap){let i=0;while((i=code.indexOf(name+'(',i))!==-1){const begin=i+name.length+1;let end=begin,depth=1;while(depth){if(code[end]==='(')depth++;if(code[end]===')')depth--;end++;}const next=wrap(code.slice(begin,end-1));code=code.slice(0,i)+next+code.slice(end);i+=next.length;}return code;}
function run(id,options={}){
 const s={map:'18,0,0,0',flags:new Set([101]),effects:new Set(),hp:500,arena:false,soldier:false,fall:false,host:true,elapsed:0,calls:[],...options};
 const api={ON:true,SoundType:{SFX:5},TargetEntityType:{Character:0},DisableNetworkSync(){},
 PlayerIsInOwnWorld:()=>s.host,PlayerInMap:(...x)=>x.join(',')===s.map,InArea:(_,x)=>x===18000359?s.arena:x===18002367?s.fall:x===18002850?s.soldier:false,
 EventFlag:x=>s.flags.has(x),CharacterHPValue:()=>s.hp,CharacterHasSpEffect:(_,x)=>s.effects.has(x),ElapsedSeconds:x=>s.elapsed>=x,
 ClearSpEffect:(_,x)=>s.effects.delete(x),SetSpEffect:(_,x)=>s.effects.add(x),
 SpawnOneshotSFX:(...x)=>s.calls.push(['vfx',...x]),PlaySE:(...x)=>s.calls.push(['sound',...x]),
 SetEventFlagID:(x,v)=>v?s.flags.add(x):s.flags.delete(x),ShowTutorialPopup:x=>s.calls.push(['tutorial',x]),
 EndIf:x=>{if(x)throw 'end'},EndEvent:()=>{throw 'end'},RestartIf:x=>{if(x)throw 'restart'},RestartEvent:()=>{throw 'restart'}};
 let body=(id===5750363||id===5750364?mapSource:source).match(new RegExp('\\$Event\\('+id+', Restart, function\\(\\) \\{([\\s\\S]*?)\\n\\}\\);'))[1];
 body=suspend(body,'WaitFor',x=>`yield ()=>(${x})`);body=suspend(body,'WaitFixedTimeSeconds',x=>`yield ()=>true`);
 const iterator=vm.runInNewContext('(function*(){'+body+'})()',api);let wait=null,done=false;
 s.step=()=>{if(done)return 'end';if(wait&&!wait())return 'wait';try{let n=iterator.next();wait=n.value;done=n.done;return done?'end':'wait'}catch(e){if(e==='end'||e==='restart'){done=true;return e}throw e}};
 return s;
}
test('rescue permission is limited to the two opening maps and safe player states',()=>{
 for(const config of [{},{arena:true},{map:'10,1,0,0',flags:new Set([10010020])}]){
  const w=run(5750361,config);w.step();assert(w.effects.has(1627122));assert.equal(w.effects.has(1627123),!!config.arena);
 }
 for(const config of [{map:'60,42,36,0'},{fall:true},{flags:new Set([101,18002851])},{effects:new Set([100690])},{effects:new Set([9621])},{map:'10,1,0,0',flags:new Set([10010020,9021])},{flags:new Set([101,1055420915])},{host:false}]){
  const w=run(5750361,config);w.step();assert(!w.effects.has(1627122));
 }
 const w=run(5750361,{effects:new Set([1627124])});w.step();assert(!w.effects.has(1627124));assert(w.calls.some(x=>x[0]==='vfx'));assert(!w.effects.has(1627112),'event must not duplicate the HKS heal');
});
test('Ultimate waits for Soldier admission and 2.5 seconds; Hadeon entry cannot trigger it',()=>{
 const w=run(5750363,{arena:true});w.step();w.step();assert.equal(w.calls.length,0);
 w.soldier=true;w.step();assert.equal(w.calls.length,0);w.flags.add(18002855);w.step();
 w.elapsed=2.49;w.step();assert.equal(w.calls.length,0);
 w.elapsed=2.5;assert.equal(w.step(),'end');assert(w.flags.has(1055420927));assert.deepEqual(w.calls,[['tutorial',5750]]);
 for(const config of [{flags:new Set([1055420927])},{flags:new Set([18000850])},{host:false}])assert.equal(run(5750363,config).step(),'end');
});

test('interrupted Soldier lesson retries and never covers transformation or Rick phase',()=>{
 for(const change of [w=>w.soldier=false,w=>w.hp=0,w=>w.flags.add(18002851),w=>w.flags.add(18002852),w=>w.flags.delete(18002855),w=>w.map='60,42,36,0']){
  const w=run(5750363,{soldier:true,flags:new Set([18002855])});w.step();w.step();change(w);assert.equal(w.step(),'restart');assert(!w.flags.has(1055420927));assert.equal(w.calls.length,0);
 }
 for(const phase of [18002851,18002852]){
  const w=run(5750363,{soldier:true,flags:new Set([18002855,phase]),elapsed:10});w.step();w.step();assert.equal(w.calls.length,0);
 }
});

test('jumping lesson waits three safe seconds inside Hadeon arena with an independent receipt',()=>{
 const w=run(5750364,{flags:new Set([1055420927])});w.step();w.step();assert.equal(w.calls.length,0);
 w.arena=true;w.step();w.elapsed=2.9;w.step();assert.equal(w.calls.length,0);
 w.elapsed=3;assert.equal(w.step(),'end');assert(w.flags.has(1055420928));assert.deepEqual(w.calls,[['tutorial',5751]]);
 for(const config of [{flags:new Set([1055420928])},{flags:new Set([1055420915])},{host:false}])assert.equal(run(5750364,config).step(),'end');
 for(const config of [{hp:0},{fall:true},{map:'60,42,36,0'}]){
  const w=run(5750364,{arena:true,...config});w.step();w.step();assert.equal(w.calls.length,0);
 }
 assert(!source.includes('$InitializeEvent(0, 5750363)'));
 assert(!source.includes('$Event(5750363,'));
 assert(!source.includes('$Event(5750364,'));
});

test('interrupted jumping lesson does not consume its receipt; victory suppresses pending display',()=>{
 for(const change of [w=>w.arena=false,w=>w.hp=0,w=>w.fall=true,w=>w.map='60,42,36,0']){
  const w=run(5750364,{arena:true});w.step();w.step();change(w);
  assert.equal(w.step(),'restart');assert(!w.flags.has(1055420928));assert.equal(w.calls.length,0);
 }
 const w=run(5750364,{arena:true});w.step();w.step();w.flags.add(1055420915);
 assert.equal(w.step(),'end');assert(!w.flags.has(1055420928));assert.equal(w.calls.length,0);
});
