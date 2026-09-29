import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Execute the authored event bodies with a deterministic frame clock. This
// checks ordering and guards, not Elden Ring's event VM or in-game audio.
const source = fs.readFileSync('src/events/m18_00_00_00.emevd.dcx.js', 'utf8');
const dialogue = JSON.parse(fs.readFileSync('src/audio/hadeon/dialogue-manifest.json', 'utf8'));
const failureFlags = [1055420930, 1055420931, 1055420932, 1055420933, 1055420934,
  1055420952, 1055420953, 1055420954, 1055420955, 1055420956];
const firstIntro = 1055420935, firstHalf = 1055420936, entitlement = 1055420937;
const victory = 1055420915, combat = 1055422933, confirmedDeath = 1055425042;
const request = 1055422947, speaking = 1055422946;
const deathLatch = 1055425224, halfLatch = 1055425225, roomBlock = 1055425223;

function suspend(code, name, replacement) {
  let start = 0;
  while ((start = code.indexOf(name + '(', start)) >= 0) {
    const open = start + name.length;
    let end = open + 1, depth = 1;
    while (depth) {
      if (code[end] === '(') depth++;
      if (code[end] === ')') depth--;
      end++;
    }
    const next = replacement(code.slice(open + 1, end - 1));
    code = code.slice(0, start) + next + code.slice(end);
    start += next.length;
  }
  return code;
}

function world(initial = {}) {
  const st = {
    time: 0, flags: new Set(initial.flags ?? []), effects: new Set(), areas: new Set(),
    hp: 500, bossHp: 1000, playerDead: false, inside: true, inMap: true,
    host: true, sounds: [], lots: [], music: [], ai: false, bar: false, events: [],
    carrierReady: true,
    randomChoice: initial.randomChoice ?? 0,
  };
  let active;
  const api = {
    ON: true, OFF: false, Enabled: true, Disabled: false,
    SoundType: {Voice: 7}, BossBGMState: {Start: 0, Stop1: 1},
    TargetEntityType: {Character: 0},
    CharacterBackreadStatus: id => id === 18002390 && st.carrierReady,
    WarpCharacterAndCopyFloor: (id, kind, target, dummy, floor) => {
      assert.equal(id, 18002390); assert.equal(target, 18002354);
      assert.equal(floor, target); assert.equal(dummy, 900);
    },
    DamageType: {Unspecified: 0}, AIStateType: {Combat: 1},
    EventFlag: id => st.flags.has(id),
    AnyBatchEventFlags: (lo, hi) => [...st.flags].some(id => id >= lo && id <= hi),
    SetEventFlagID: (id, on) => on ? st.flags.add(id) : st.flags.delete(id),
    BatchSetEventFlags: (lo, hi, on) => { for (let id = lo; id <= hi; id++) on ? st.flags.add(id) : st.flags.delete(id); },
    RandomlySetEventFlagInRange: (lo, hi, on) => on
      ? st.flags.add(lo + Math.min(st.randomChoice, hi - lo))
      : st.flags.delete(lo + Math.min(st.randomChoice, hi - lo)),
    CharacterHPValue: id => id === 10000 ? st.hp : st.bossHp,
    HPRatio: () => st.bossHp / 1000,
    CharacterDead: id => id === 10000 ? st.playerDead : st.bossHp <= 0,
    CharacterHasSpEffect: (_, id) => st.effects.has(id),
    ClearSpEffect: (_, id) => st.effects.delete(id),
    SetSpEffect: (_, id) => st.effects.add(id),
    PlayerIsInOwnWorld: () => st.host,
    PlayerInMap: () => st.inMap,
    InArea: (_, id) => id === 18000359 ? st.inside : st.areas.has(id),
    HasDamageType: () => false,
    EnableCharacterAI: () => { st.ai = true; },
    DisplayBossHealthBar: on => { st.bar = on; },
    SetBossBGM: (_, mode) => st.music.push({time: st.time, mode}),
    PlaySE: (emitter, _, id) => st.sounds.push({time: st.time, id, emitter}),
    AwardItemLot: id => st.lots.push(id),
    DisableNetworkSync() {},
    ElapsedSeconds: seconds => st.time - active.waitStart >= seconds - 1e-8,
    RestartEvent: () => { throw {restart: true}; },
    RestartIf: yes => { if (yes) throw {restart: true}; },
    EndEvent: () => { throw {end: true}; },
    EndIf: yes => { if (yes) throw {end: true}; },
  };
  const context = vm.createContext(api);
  function add(id) {
    const match = source.match(new RegExp(`\\$Event\\(${id}, Restart, function\\([^)]*\\) \\{([\\s\\S]*?)\\n\\}\\);`));
    assert(match, `missing event ${id}`);
    let code = suspend(match[1], 'WaitFor', condition => `yield {condition:()=>(${condition})}`);
    code = suspend(code, 'WaitFixedTimeSeconds', seconds => `yield {seconds:${seconds}}`);
    code = suspend(code, 'WaitFixedTimeFrames', frames => `yield {seconds:(${frames})/30}`);
    const generator = vm.runInContext(`(function*(){while(true){try{${code}return;}catch(e){if(e.restart)continue;if(e.end)return;throw e;}}})`, context);
    st.events.push({id, iterator: generator(), wait: null, waitStart: 0, done: false});
  }
  for (const id of [5750420, 5750421, 5750422, 5750423, 5750424, 5750312]) add(id);
  function step(event) {
    active = event;
    for (let n = 0; n < 200; n++) {
      if (event.done) return;
      if (event.wait) {
        if (event.wait.condition && !event.wait.condition()) return;
        if (event.wait.until !== undefined && st.time + 1e-8 < event.wait.until) return;
        event.wait = null;
      }
      const next = event.iterator.next();
      if (next.done) { event.done = true; return; }
      event.waitStart = st.time;
      event.wait = next.value;
      if (event.wait.seconds !== undefined) event.wait.until = st.time + event.wait.seconds;
    }
    throw Error(`busy event ${event.id}`);
  }
  st.advance = seconds => {
    const target = st.time + seconds;
    while (st.time < target - 1e-8) {
      st.time = Math.round((st.time + 0.01) * 100) / 100;
      st.events.forEach(step);
    }
  };
  return st;
}

const count = w => failureFlags.filter(id => w.flags.has(id)).length;
const voiceStarts = w => w.sounds.filter(s => s.id >= 999800001 && s.id <= 999800114);

// Admission and first-room guard never grant a death or consume rescue outside.
let w = world(); w.advance(.1);
assert(w.flags.has(roomBlock));
assert(!w.effects.has(1627122));
w.inside = false; w.advance(.1); assert(!w.flags.has(roomBlock));
w.inside = true; w.advance(.1); assert(w.flags.has(roomBlock));
w.hp = 0; w.playerDead = true; w.advance(.1); assert.equal(count(w), 0);

// Immediate native death and the delayed confirmation fallback each count once.
for (const kind of ['native', 'confirmed']) {
  w = world({flags: [combat]}); w.advance(.1); w.hp = 0;
  if (kind === 'native') w.playerDead = true; else w.flags.add(confirmedDeath);
  w.advance(.1);
  assert.equal(count(w), 1, kind);
  assert(w.flags.has(deathLatch), kind);
  assert(voiceStarts(w).some(s => s.id >= 999800109 && s.id <= 999800112), kind);
  w.advance(.5); assert.equal(count(w), 1, kind);
  w.hp = 500; w.playerDead = false; w.flags.delete(confirmedDeath); w.advance(.1);
  assert(!w.flags.has(deathLatch), kind);
}

// Saved failures progress one at a time and stop at ten even after more deaths.
w = world({flags: [combat]}); w.advance(.1);
for (let attempt = 1; attempt <= 12; attempt++) {
  w.hp = 0; w.playerDead = true; w.advance(.1);
  assert.equal(count(w), Math.min(attempt, 10));
  w.hp = 500; w.playerDead = false; w.advance(.1);
}
assert(!w.flags.has(entitlement));

// Rescue, excluded space and uncommitted intro cannot raise a failure.
for (const kind of ['rescue', 'excluded', 'outside', 'intro']) {
  w = world({flags: kind === 'intro' ? [request] : [combat]}); w.advance(.1);
  if (kind === 'rescue') w.effects.add(1627125);
  if (kind === 'excluded') w.areas.add(18002349);
  if (kind === 'outside') w.inside = false;
  w.hp = 0; w.playerDead = true; w.advance(.1);
  assert.equal(count(w), 0, kind);
}

// Fatal bridge falls count even after leaving the room volume. Native death and
// the confirmed-death fallback both unlock aid and remove no-loss eligibility.
for (const kind of ['native', 'confirmed']) {
  w = world({flags: [combat]}); w.advance(.1);
  w.inside = false; w.areas.add(18002367); w.areas.add(18002349);
  w.advance(1); assert.equal(count(w), 0, 'falling alive is not a loss');
  w.hp = 0;
  if (kind === 'native') w.playerDead = true; else w.flags.add(confirmedDeath);
  w.advance(.1); assert.equal(count(w), 1, kind);
  assert(!voiceStarts(w).some(s => s.id >= 999800109 && s.id <= 999800112),
    'fatal below-arena falls never start a player-killed line');
  assert(![1055425210, 1055425211, 1055425212, 1055425213]
    .some(id => w.flags.has(id)), 'fall does not select a subtitle');
  w.advance(2); assert.equal(count(w), 1, 'one count per fatal fall');
  w.hp = 500; w.playerDead = false; w.flags.delete(confirmedDeath);
  w.areas.clear(); w.inside = true; w.advance(.1);
  w.bossHp = 0; w.advance(.2);
  assert(!w.flags.has(entitlement), 'fatal fall disqualifies the no-loss reward');
  assert(voiceStarts(w).some(s => s.id === 999800113));
}

// A survived fall/recovery and a rescued zero-HP fall frame consume nothing.
w = world({flags: [combat]}); w.advance(.1);
w.inside = false; w.areas.add(18002367); w.advance(2);
w.hp = 0; w.effects.add(1627125); w.playerDead = true; w.advance(.1);
assert.equal(count(w), 0);
w.hp = 500; w.playerDead = false; w.effects.clear();
w.areas.clear(); w.inside = true; w.advance(.1);
assert.equal(count(w), 0);

// Falls before combat, after disengagement, off-map, or alongside boss victory
// remain excluded. A fatal fall must not turn simultaneous victory into a loss.
for (const kind of ['intro', 'disengaged', 'off-map', 'victory']) {
  w = world({flags: kind === 'intro' ? [request] : [combat]}); w.advance(.1);
  w.inside = false; w.areas.add(18002367);
  if (kind === 'disengaged') w.flags.delete(combat);
  if (kind === 'off-map') w.inMap = false;
  w.hp = 0; w.playerDead = true; w.advance(.01);
  if (kind === 'victory') w.bossHp = 0;
  w.advance(.1); assert.equal(count(w), 0, kind);
  if (kind === 'victory') assert(w.flags.has(entitlement));
}

// Adjacent-frame simultaneous death resolves as victory, not a failed attempt.
w = world({flags: [combat]}); w.advance(.1);
w.hp = 0; w.playerDead = true; w.advance(.01);
w.bossHp = 0; w.advance(.1);
assert.equal(count(w), 0); assert(w.flags.has(entitlement));
assert(voiceStarts(w).some(s => s.id === 999800114));
w.flags.add(victory); w.advance(.1); assert.equal(w.lots.length, 0);
w.hp = 500; w.playerDead = false; w.advance(.1);
assert.deepEqual(w.lots, [10000320]);
w.advance(.5); assert.deepEqual(w.lots, [10000320]);

// A prior genuine death chooses ordinary boss-death VO and never earns the bonus.
w = world({flags: [combat, failureFlags[0]]}); w.advance(.1);
w.bossHp = 0; w.advance(.1);
assert(!w.flags.has(entitlement));
assert(voiceStarts(w).some(s => s.id === 999800113));
w.flags.add(victory); w.advance(.1); assert.equal(w.lots.length, 0);

// A 50% crossing queues one line and persists first-line selection once played.
w = world({flags: [combat]}); w.advance(.1); w.bossHp = 490; w.advance(.1);
assert(w.flags.has(halfLatch)); assert(w.flags.has(firstHalf));
assert(voiceStarts(w).some(s => s.id === 999800104));
w.bossHp = 300; w.advance(.2);
assert.equal(voiceStarts(w).filter(s => s.id === 999800104).length, 1);

// Durations measured from the 48 kHz dialogue PCM and kept independent of the
// event timeout values. The manifest ties each index to its play/stop aliases.
const measuredSeconds = [
  17.2708333333, 9.98475, 4.894583, 8.159708, 8.542354, 10.757833,
  8.090188, 5.771646, 6.053667, 6.137042, 6.446917, 5.7468541667,
  3.285, 5.5524583333, 17.218042, 13.091792,
];
function soundAt(state, id) { return state.sounds.find(sound => sound.id === id); }
function assertVoiceEdge(state, beforeId, afterId) {
  const before = dialogue.lines.find(line => line.soundId === beforeId);
  const stop = soundAt(state, before.stopAlias);
  const after = soundAt(state, afterId);
  assert(stop && after, `missing ${beforeId} stop or ${afterId} start`);
  assert(after.time - stop.time >= .09, `${beforeId} to ${afterId} lacked the 0.1-second OFF edge`);
}
for (let index = 0; index < dialogue.lines.length; index++) {
  const line = dialogue.lines[index];
  const requestId = index === 0 ? 1055425216 : index <= 4 ? 1055425217
    : index <= 9 ? 1055425218 : index <= 13 ? 1055425220
      : index === 14 ? 1055425221 : 1055425222;
  const flags = [request, requestId];
  if (index >= 6 && index <= 9) flags.push(firstHalf);
  if (index === 3 || (index >= 10 && index <= 13)) flags.push(1055420932);
  w = world({flags, randomChoice: index <= 4 ? index - 1
    : index <= 5 ? 0 : index <= 9 ? index - 6 : index <= 13 ? index - 10 : 0});
  if (index >= 10 && index <= 13) w.hp = 0;
  w.advance(measuredSeconds[index] + .2);
  const start = soundAt(w, line.soundId), stop = soundAt(w, line.stopAlias);
  assert(start && stop, `${line.key}: missing play/stop pair`);
  const elapsed = stop.time - start.time;
  assert(elapsed >= measuredSeconds[index], `${line.key}: playback cut short at ${elapsed}`);
  assert(elapsed <= measuredSeconds[index] + .05, `${line.key}: timeout too long at ${elapsed}`);
  assert(line.cues.at(-1).end <= measuredSeconds[index], `${line.key}: final cue exceeds audio`);
  if (index >= 14) {
    assert.equal(start.emitter, 18002390, 'Death voice survives the dying boss emitter');
    assert.equal(stop.emitter, start.emitter);
    assert(w.flags.has(1055425256), 'Cleanup is released after the full tail');
  }
}

// Half health waits until the entrance finishes; a genuine kill interrupts it.
for (const [requestFlag, voiceId, stopId, duration] of [
  [1055425221, 999800113, 999800213, 17.24],
  [1055425222, 999800114, 999800214, 13.12],
]) {
  w = world({flags: [request, requestFlag]}); w.carrierReady = false;
  w.advance(duration + .3);
  assert.equal(soundAt(w, voiceId).emitter, 10000, 'Missing carrier uses player audio fallback');
  assert.equal(soundAt(w, stopId).emitter, 10000);
  assert(w.flags.has(1055425256), 'Missing carrier cannot hang death completion');
}

// Half health waits until the entrance finishes; a genuine kill interrupts it.
w = world({flags: [request, combat, 1055425216]}); w.advance(.1);
w.bossHp = 490; w.advance(.1); assert(w.flags.has(1055425218));
assert(!soundAt(w, 999800104));
w.advance(measuredSeconds[0] + .3);
assert(soundAt(w, 999800104));
assertVoiceEdge(w, 999800001, 999800104);

w = world({flags: [request, combat, 1055425216]}); w.advance(.1);
w.hp = 0; w.playerDead = true; w.advance(.3);
const killStart = w.sounds.find(sound => sound.id >= 999800109 && sound.id <= 999800112);
assert(killStart && soundAt(w, 999800002));
assertVoiceEdge(w, 999800001, killStart.id);

// Boss death outranks both queued half-health speech and an active kill line.
for (const priorVoice of ['half', 'kill']) {
  const priorRequest = priorVoice === 'half' ? 1055425218 : 1055425220;
  w = world({flags: [request, priorRequest, ...(priorVoice === 'kill' ? [1055420932] : [])]});
  if (priorVoice === 'kill') w.hp = 0;
  w.advance(.1);
  const priorId = priorVoice === 'half' ? 999800104 : 999800109;
  assert(soundAt(w, priorId), priorVoice);
  w.bossHp = 0; w.advance(.05);
  assert(soundAt(w, dialogue.lines.find(line => line.soundId === priorId).stopAlias));
  assert(!w.flags.has(speaking), `${priorVoice}: active flag did not drop before replacement`);
  assert(!soundAt(w, 999800114));
  w.advance(.25);
  assert(soundAt(w, 999800114), priorVoice);
  assertVoiceEdge(w, priorId, 999800114);
}

// The saved entitlement can deliver on reload, but the lot receipt prevents a
// duplicate and old completed saves never gain a retroactive bonus.
w = world({flags: [entitlement, victory]}); w.advance(.1);
assert.deepEqual(w.lots, [10000320]);
w = world({flags: [entitlement, victory, 1055420250]}); w.advance(.1);
assert.equal(w.lots.length, 0);
w = world({flags: [victory]}); w.advance(.2);
assert(!w.flags.has(entitlement)); assert.equal(w.lots.length, 0);

// Each saved pool independently excludes its previous line. Enumerating every
// random result proves equal representation without a probabilistic test.
const repeatPools = [
  {requestId: 1055425217, memory: 1055420940, sound: 999800100},
  {requestId: 1055425218, memory: 1055420944, sound: 999800105},
  {requestId: 1055425220, memory: 1055420948, sound: 999800109},
];
for (const pool of repeatPools) {
  for (let previous = -1; previous < 4; previous++) {
    const actual = [];
    for (let choice = 0; choice < (previous < 0 ? 4 : 3); choice++) {
      const otherMemory = repeatPools.filter(p => p !== pool).map(p => p.memory + 2);
      const flags = [request, firstHalf, 1055420932, pool.requestId, ...otherMemory];
      if (previous >= 0) flags.push(pool.memory + previous);
      // A new world with saved flags also models selection after a reload.
      w = world({flags, randomChoice: choice}); w.advance(.05);
      const started = voiceStarts(w);
      assert.equal(started.length, 1);
      const selected = started[0].id - pool.sound;
      assert(selected >= 0 && selected < 4);
      assert.notEqual(selected, previous);
      actual.push(selected);
      assert.deepEqual([...w.flags].filter(f => f >= pool.memory && f <= pool.memory + 3),
        [pool.memory + selected]);
      assert(otherMemory.every(f => w.flags.has(f)), 'other pools retain their history');
    }
    assert.deepEqual(actual.sort(), [0, 1, 2, 3].filter(n => n !== previous));
  }
  // Consecutive requests in the same worker also advance remembered history.
  w = world({flags: [request, firstHalf, 1055420932, pool.requestId], randomChoice: 0});
  w.advance(12); const first = voiceStarts(w)[0].id;
  w.flags.add(pool.requestId); w.advance(.1);
  assert.notEqual(voiceStarts(w).at(-1).id, first);
}

// Before the third saved loss, each reduced pool remains uniform over its
// eligible lines and remembers only the last line that actually started.
for (const pool of [
  {requestId: 1055425217, memory: 1055420940, sound: 999800100, eligible: [0, 1, 3]},
  {requestId: 1055425220, memory: 1055420948, sound: 999800109, eligible: [1, 2, 3]},
]) {
  for (const previous of [-1, ...pool.eligible]) {
    const expected = pool.eligible.filter(line => line !== previous);
    const actual = [];
    for (let choice = 0; choice < expected.length; choice++) {
      const flags = [request, pool.requestId];
      if (previous >= 0) flags.push(pool.memory + previous);
      w = world({flags, randomChoice: choice});
      if (pool.requestId === 1055425220) w.hp = 0;
      w.advance(.05);
      const started = voiceStarts(w);
      assert.equal(started.length, 1);
      const selected = started[0].id - pool.sound;
      actual.push(selected);
      assert.deepEqual([...w.flags].filter(f => f >= pool.memory && f <= pool.memory + 3),
        [pool.memory + selected]);
    }
    assert.deepEqual(actual.sort(), expected, `reduced pool ${pool.requestId}, previous ${previous}`);
  }
}

// The third fatality increments the saved count before requesting its taunt.
w = world({flags: [combat, 1055420930, 1055420931, 1055420949], randomChoice: 0});
w.advance(.1); w.hp = 0; w.playerDead = true; w.advance(.1);
assert(w.flags.has(1055420932));
assert(soundAt(w, 999800109), 'thousand-times line may start on the third death');

// Even an already pending kill request is discarded before subtitle selection
// when the confirmed death is in the below-arena fall region.
w = world({flags: [request, 1055425220, 1055420949]});
w.hp = 0; w.playerDead = true; w.inside = false; w.areas.add(18002367);
w.advance(.05);
assert(!voiceStarts(w).some(s => s.id >= 999800109 && s.id <= 999800112));
assert(w.flags.has(1055420949));
assert(!w.flags.has(1055425220));

// A higher-priority request discarded before playback must not consume history.
w = world({flags: [request, 1055425217, 1055425222, 1055420941]}); w.advance(.05);
assert(w.flags.has(1055420941));
assert.equal(voiceStarts(w)[0].id, 999800114);

console.log('Hadeon progression source simulation passed: deaths, ten caps, exclusions, reward recovery, dialogue timing/priority and independent no-repeat pools. Not an engine test.');
