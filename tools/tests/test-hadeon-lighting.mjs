import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
const source=fs.readFileSync('src/events/m18_00_00_00.emevd.dcx.js','utf8');
// The old 1055423xxx block cannot store flags in Elden Ring. A pure simulator
// otherwise accepts it and incorrectly reports a working ignition sequence.
for(const match of source.matchAll(/105542\d{4}/g)) {
 assert(![1,3,6].includes(Math.floor(Number(match[0])/1000)%10), 'Invalid Sovereign flag allocation '+match[0]);
}
function suspend(code,name,fn){let start=0;while((start=code.indexOf(name+'(',start))>=0){const open=start+name.length;let end=open+1,depth=1;while(depth){if(code[end]==='(')depth++;if(code[end]===')')depth--;end++;}const next=fn(code.slice(open+1,end-1));code=code.slice(0,start)+next+code.slice(end);start+=next.length;}return code;}
function world(initial={}){
 const st={assets:new Set(),areas:new Set(),time:0,host:initial.host??true,flags:new Set(initial.flags??[]),hp:500,bossHp:1,inside:false,fall:false,combat:true,aiEnabled:true,effects:new Set(),warps:[],resets:0,banners:0,lights:new Set(),flames:new Set(),random:0,events:[]};let active;
 const api={ON:true,OFF:false,Enabled:true,Disabled:false,AIStateType:{Combat:1},BossBGMState:{Start:0,Stop1:1},SoundType:{SFX:0},TargetEntityType:{Character:0,Area:1},TextBannerType:{GreatEnemyFelled:0},L0:'L0',L1:'L1',L9:'L9',EventFlag:id=>st.flags.has(id),CharacterHPValue:id=>id===10000?st.hp:st.bossHp*1000,HPRatio:()=>st.bossHp,
 InArea:(_,id)=>id===18000359?st.inside:id===18002367?st.fall:st.areas.has(id),
 DisableNetworkSync(){},PlayerIsInOwnWorld:()=>st.host,CharacterHasSpEffect:(_,id)=>st.effects.has(id),CharacterAIState:()=>st.combat&&st.aiEnabled,
 DisableCharacterAI:()=>st.aiEnabled=false,EnableCharacterAI:()=>st.aiEnabled=true,
 SetSpEffect:(_,id)=>st.effects.add(id),ClearSpEffect:(_,id)=>st.effects.delete(id),
 DisplayBossHealthBar:on=>st.bossBar=on,SetBossBGM(){},SpawnOneshotSFX(){},PlaySE(){},RequestCharacterAnimationReset(){},EnableAsset:id=>st.assets.add(id),DisableAsset:id=>st.assets.delete(id),
 WarpCharacterAndCopyFloor:(...args)=>st.warps.push(args),$InitializeEvent:()=>st.resets++,CharacterDead:()=>st.bossHp<=0,
 HandleBossDefeatAndDisplayBanner:()=>st.banners++,
 AnyBatchEventFlags:(a,b)=>[...st.flags].some(x=>x>=a&&x<=b),SetEventFlagID:(id,on)=>on?st.flags.add(id):st.flags.delete(id),BatchSetEventFlags:(a,b,on)=>{for(let i=a;i<=b;i++)on?st.flags.add(i):st.flags.delete(i);},ElapsedSeconds:s=>st.time-active.waitStart>=s-1e-8,
 DeleteMapSFX:id=>st.lights.delete(id),SpawnMapSFX:id=>{assert(!st.lights.has(id),'Duplicate spawn '+id);st.lights.add(id);},DeleteAssetfollowingSFX:id=>st.flames.delete(id),CreateAssetfollowingSFX:id=>{assert(!st.flames.has(id),'Duplicate flame '+id);st.flames.add(id);},Goto:label=>{throw {goto:label};},GotoIf:(label,c)=>{if(c)throw {goto:label};},RestartEvent:()=>{throw {goto:'entry'};},RestartIf:c=>{if(c)throw {goto:'entry'};},EndEvent:()=>{throw {end:true};},EndIf:c=>{if(c)throw {end:true};}};
 const ctx=vm.createContext(api);
 function add(id,args=[]){const m=source.match(new RegExp('\\$Event\\('+id+', Restart, function\\(([^)]*)\\) \\{([\\s\\S]*?)\\n\\}\\);'));assert(m,id);let code=m[2];code=suspend(code,'WaitFor',x=>`yield {condition:()=>(${x})}`);code=suspend(code,'WaitRandomTimeSeconds',x=>`yield {random:[${x}]}`);code=suspend(code,'WaitFixedTimeSeconds',x=>`yield {seconds:${x}}`);code=suspend(code,'WaitFixedTimeFrames',x=>`yield {seconds:(${x})/30}`);
 code='case "entry":'+code.replace(/^L(\d+):/gm,(_,n)=>`case "L${n}":`);
 const fn=vm.runInContext(`(function*(${m[1]}){let label='entry';while(true){try{switch(label){${code}}return;}catch(e){if(e.goto){label=e.goto;continue;}if(e.end)return;throw e;}}})`,ctx);
 st.events.push({id,iterator:fn(...args),wait:null,waitStart:0,done:false});}
 if(!initial.halls){add(5750402);add(5750403);add(5750404);add(5750370);add(5750303);add(5750305);
 const init=source.match(/\$Event\(0,[\s\S]*?\n\}\);/)[0];for(const m of init.matchAll(/\$InitializeEvent\(\d+, (\d+)([^;]*?)\);/g)){const id=+m[1];if([5750401,5750372,5750373].includes(id)){add(id,m[2].replace(/^,\s*/,'').split(',').filter(Boolean).map(Number));}}
 }else{for(let id=5750320;id<=5750331;id++)add(id);}
 function step(e){active=e;for(let i=0;i<200;i++){if(e.done)return;if(e.wait){if(e.wait.condition&&!e.wait.condition())return;if(e.wait.until!==undefined&&st.time+1e-8<e.wait.until)return;e.wait=null;}const v=e.iterator.next();if(v.done){e.done=true;return;}e.waitStart=st.time;e.wait=v.value;if(e.wait.random){const [a,b]=e.wait.random;const ratio=((st.random++*17)%26)/25;e.wait.until=st.time+a+(b-a)*ratio;}if(e.wait.seconds!==undefined)e.wait.until=st.time+e.wait.seconds;}throw Error('Busy loop '+e.id);}
 st.advance=(seconds)=>{const target=st.time+seconds;while(st.time<target-1e-8){st.time=Math.round((st.time+0.01)*100)/100;st.events.forEach(step);}};return st;
}
let w=world();w.advance(1);assert.equal(w.lights.size,0);w.inside=true;w.advance(1);assert(w.lights.size>0&&w.lights.size<96);w.advance(29.2);assert.equal(w.lights.size,96);assert.equal(w.flames.size,88);assert(w.flags.has(1055422996));w.hp=0;w.advance(.7);assert.equal(w.lights.size,96);assert.equal(w.flames.size,88);w.advance(5);w.hp=500;w.advance(30.3);assert.equal(w.lights.size,96);
w=world();w.inside=true;w.advance(.7);w.flags.add(1055420915);w.advance(.2);assert.equal(w.lights.size,96);assert.equal(w.flames.size,88);
w=world();w.inside=true;w.advance(.7);w.flags.add(1055422945);w.flags.add(1055420918);w.advance(.2);assert.equal(w.lights.size,96);w.advance(5);assert.equal(w.lights.size,96);w.flags.delete(1055422945);w.advance(2.6);assert.equal(w.lights.size,0);assert.equal(w.flames.size,0);
w=world({flags:[1055420918]});w.inside=true;w.advance(8);assert.equal(w.lights.size,0);assert.equal(w.flames.size,0);
w=world({flags:[1055420915]});w.advance(.2);assert.equal(w.lights.size,96);assert.equal(w.flames.size,88);
w=world();w.inside=true;w.advance(1);const deathLights=new Set(w.lights),deathFlames=new Set(w.flames);w.hp=0;w.advance(.7);assert.deepEqual(w.lights,deathLights);assert.deepEqual(w.flames,deathFlames);w.advance(35);assert.deepEqual(w.lights,deathLights);assert.deepEqual(w.flames,deathFlames);w.hp=500;w.advance(.2);assert(w.lights.size<10);w.advance(30.1);assert.equal(w.lights.size,96);assert.equal(w.flames.size,88);
// Verify each HP stage selects exactly one preset per position and no 150% light.
for(const [hp,stage] of [[.7,1],[.4,2],[.2,3]]){w.bossHp=hp;w.advance(.2);assert.equal(w.lights.size,96);for(const id of w.lights){const base=id<18004200?18003900:18004200;assert.equal((id-base)%5,stage);}}
assert(!source.includes('EventFlag(105542296'));
console.log('Source execution simulation passed: staggered entry, all-on completion, death/re-entry, victory/crystal interruption, and saved-state load. Not an engine test.');

// Startup is monotonic: no scheduled off pulses after a group first ignites.
w=world();w.inside=true;let previous=new Set();
for(let i=0;i<3040;i++){w.advance(.01);for(const light of previous)assert(w.lights.has(light),'Startup light flickered off: '+light);previous=new Set(w.lights);}
assert.equal(w.lights.size,96);
// Lethal rescue before confirmation preserves lighting, milestone receipts and combat.
w=world();w.inside=true;w.advance(1);w.flags.add(1055422930);w.flags.add(1055422931);
previous=new Set(w.lights);w.hp=0;w.combat=false;w.advance(.2);w.hp=500;w.effects.add(1627125);w.advance(.5);w.effects.delete(1627125);w.advance(7);
for(const light of previous)assert(w.lights.has(light));assert(w.flags.has(1055422930)&&w.flags.has(1055422931));
assert.equal(w.warps.length,0);assert.equal(w.resets,0);assert(w.bossBar);assert(w.flags.has(1055422933));
// Confirmation requires an uninterrupted interval and cannot commit during rescue protection.
w=world();w.inside=true;w.advance(1);w.hp=0;w.effects.add(1627125);w.advance(.7);assert(!w.flags.has(1055425042));
w.effects.delete(1627125);w.advance(.6);assert(w.flags.has(1055425042));w.advance(6.1);assert.equal(w.warps.length,1);
assert.equal(w.warps[0][2],18002380);assert.equal(w.aiEnabled,false);assert.equal(w.resets,0);
w.advance(1);assert.equal(w.aiEnabled,false);w.hp=500;w.advance(.2);assert.equal(w.aiEnabled,true);
assert.equal(w.resets,0);
// Recovery after confirmation still cancels the queued six-second teleport.
w=world();w.inside=true;w.advance(1);w.hp=0;w.advance(.7);assert(w.flags.has(1055425042));w.hp=500;w.advance(7);assert.equal(w.warps.length,0);
// Death resets combat milestones but freezes lights; victory still wins over queued retreat.
w=world();w.inside=true;w.advance(1);w.flags.add(1055422930);const beforeDeath=new Set(w.lights);w.hp=0;w.advance(.7);assert(!w.flags.has(1055422930));assert.deepEqual(w.lights,beforeDeath);
w.bossHp=0;w.advance(6.2);assert.equal(w.warps.length,0);assert.equal(w.banners,1);
w=world();w.inside=true;w.advance(1);w.inside=false;w.combat=false;w.advance(1);w.flags.add(1055420915);w.advance(6.2);assert.equal(w.warps.length,0);
// Keep intentional falling and out-of-arena retreat, but cancel a recovered departure.
for(const kind of ['fall','exit']){w=world();w.inside=true;w.advance(1);if(kind==='fall')w.fall=true;else{w.inside=false;w.combat=false;}w.advance(6.2);assert.equal(w.warps.length,1);assert.equal(w.aiEnabled,false);assert.equal(w.resets,0);}
w=world();w.inside=true;w.advance(1);w.inside=false;w.combat=false;w.advance(1);w.inside=true;w.advance(7);assert.equal(w.warps.length,0);
console.log('Rescue/death regression simulation passed: steady ignition, rescued zero HP, temporary aggro loss, persistent death, recovered retreat, boss victory and intentional exits.');

// Aid permission needs three continuous eligible seconds before the HKS ramp begins.
w=world();w.advance(.2);assert(!w.effects.has(1627130));w.inside=true;w.advance(2.9);assert(!w.effects.has(1627130));
w.inside=false;w.advance(.2);w.inside=true;w.advance(2.9);assert(!w.effects.has(1627130));w.advance(.2);assert(w.effects.has(1627130));
w.inside=false;w.advance(.2);assert(!w.effects.has(1627130));w.inside=true;w.advance(3.2);assert(w.effects.has(1627130));
for(const effect of [100690,9621]){w.effects.add(effect);w.advance(.2);assert(!w.effects.has(1627130));w.effects.delete(effect);w.advance(3.2);assert(w.effects.has(1627130));}
w.fall=true;w.advance(.2);assert(!w.effects.has(1627130));w.fall=false;w.advance(3.2);assert(w.effects.has(1627130));
w.hp=0;w.advance(.7);assert(!w.effects.has(1627130));w.hp=500;w.advance(3.2);assert(w.effects.has(1627130));
w.flags.add(1055420915);w.advance(.2);assert(!w.effects.has(1627130));
w=world();w.inside=true;w.advance(3.2);assert(w.effects.has(1627130));w.bossHp=0;w.advance(.2);assert(!w.effects.has(1627130));
w=world({host:false});w.inside=true;w.advance(3.2);assert(!w.effects.has(1627130));
console.log('Aid permission simulation passed: continuous warm-up, departure, reentry, death, victory, falling, scripted states and guest exclusion.');

// HP brightness must change during ignition rather than waiting for its completion.
w=world();w.inside=true;w.advance(10);const initialCount=w.lights.size;
assert(initialCount>=30&&initialCount<=35);w.bossHp=.4;w.advance(.15);
assert(w.lights.size<=35);for(const id of w.lights){const base=id<18004200?18003900:18004200;assert.equal((id-base)%5,2);}
w.advance(21);assert.equal(w.lights.size,96);
const starts=[...source.matchAll(/\$InitializeEvent\(\d+, 5750401, (\d+), ([\d.]+)\);/g)];
assert.equal(starts.length,96);assert.equal(new Set(starts.map(x=>x[1])).size,96);
const delays=starts.map(x=>+x[2]).sort((a,b)=>a-b);for(let i=1;i<delays.length;i++)assert(delays[i]-delays[i-1]>.30);
assert.equal(delays[0],.05);assert.equal(delays[95],29.5);
console.log('30-second individual ignition and concurrent HP brightness passed.');

// Hallway pairs preserve one physical fixture while automatic model SFX owns light.
const hallBlocks=[...source.matchAll(/\$Event\(57503(?:2\d|3[01]), Restart, function\(\) \{([\s\S]*?)\n\}\);/g)];
const pairMatches=hallBlocks.flatMap(m=>[...m[1].matchAll(/DisableAsset\((18009\d+)\);\s+EnableAsset\((18006\d+)\);/g)]);
const pairs=new Map(pairMatches.map(m=>[+m[1],+m[2]]));assert.equal(pairs.size,125);
assert.equal(new Set(pairs.values()).size,125);
for(const m of hallBlocks)assert(!m[1].includes('AssetfollowingSFX'));
function checkPairs(w){assert.equal(w.assets.size,125);for(const [lit,off] of pairs)assert.notEqual(w.assets.has(lit),w.assets.has(off),'Exactly one visible per pair');}
function litCount(w){return [...pairs.keys()].filter(id=>w.assets.has(id)).length;}
w=world({halls:true});w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
const regions=[...new Set(hallBlocks.flatMap(m=>[...m[1].matchAll(/InArea\(10000, (\d+)\)/g)].map(x=>+x[1])))];
assert.equal(regions.length,12);
w.areas.add(18002355);w.advance(1.4);assert.equal(litCount(w),0);w.advance(.2);assert(litCount(w)>0);
w.areas.delete(18002355);w.advance(.5);w.areas.add(18002355);w.advance(.1);assert(litCount(w)>0);
w.areas.delete(18002355);w.advance(1.1);assert.equal(litCount(w),0);
for(const region of regions){w.areas.add(region);w.advance(1.7);checkPairs(w);assert(litCount(w)>0);w.areas.delete(region);w.advance(.5);checkPairs(w);assert(litCount(w)>0);w.areas.add(region);w.advance(.1);checkPairs(w);assert(litCount(w)>0);w.areas.delete(region);w.advance(1.1);checkPairs(w);assert.equal(litCount(w),0);}
w.areas.add(regions[1]);w.advance(.2);w.areas.clear();w.advance(.5);w.flags.add(1055420915);w.advance(1.1);checkPairs(w);assert.equal(litCount(w),125);
w.flags.add(1055420918);w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
w=world({halls:true});w.advance(.1);
w.areas.add(18002355);w.advance(.2);w.areas.clear();w.advance(2);checkPairs(w);assert.equal(litCount(w),0);
w.flags.add(1055420915);w.advance(.1);checkPairs(w);assert.equal(litCount(w),125);
w.flags.add(1055420918);w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
for(const flags of [[1055420915],[1055420918],[1055420915,1055420918]]){w=world({halls:true,flags});w.advance(.1);checkPairs(w);assert.equal(litCount(w),flags.includes(1055420918)?0:125);}
console.log('125 hallway pairs: every region, delayed cancellation, victory, crystal and saved-state visibility passed.');

// Freeze the precise brightness, even when Hadeon resets HP during the death camera.
w=world();w.inside=true;w.advance(12);w.bossHp=.4;w.advance(.1);
const frozenLights=new Set(w.lights),frozenFlames=new Set(w.flames);
w.hp=0;w.advance(.1);w.bossHp=1;w.advance(8);
assert.deepEqual(w.lights,frozenLights);assert.deepEqual(w.flames,frozenFlames);
w.inside=false;w.hp=500;w.advance(.2);assert.equal(w.lights.size,0);assert.equal(w.flames.size,0);
w.inside=true;w.advance(30.2);assert.equal(w.lights.size,96);
// Crystal presentation overrides a frozen death state and still ends fully off.
w.hp=0;w.advance(.7);w.flags.add(1055422945);w.flags.add(1055420918);w.advance(.2);
assert.equal(w.lights.size,96);w.flags.delete(1055422945);w.advance(2.6);
assert.equal(w.lights.size,0);assert.equal(w.flames.size,0);
console.log('Death retains exact lighting, pauses ignition, resets on recovery and preserves crystal precedence.');
