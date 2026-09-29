import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

// Source control-flow checks; native load ordering and saves still need game tests.
const common = readFileSync('src/events/common.emevd.dcx.js', 'utf8');
const map = readFileSync('src/events/m18_00_00_00.emevd.dcx.js', 'utf8');
const reset = common.split('// BEGIN TEMPORARY HADEON LOAD RESET')[1]
  .split('// END TEMPORARY HADEON LOAD RESET')[0];
const marker = 1055420938;
const losses = [1055420930, 1055420931, 1055420932, 1055420933, 1055420934,
  1055420952, 1055420953, 1055420954, 1055420955, 1055420956];
const dialogueHistory = [1055420940, 1055420947, 1055420951];
const history = [1055420935, 1055420936, 1055420937, ...dialogueHistory];
const protectedFlags = [1055420916, 1055420250, 1055420918, 1055420920, 1055420924];

function world(flags = []) {
  const state = { flags: new Set(flags), host: true, hp: 500, dead: false,
    bossHp: 1000, rescue: false, time: 0, saves: [], workers: [] };
  const api = {
    ON: true, OFF: false,
    PlayerIsInOwnWorld: () => state.host,
    EventFlag: id => state.flags.has(id),
    SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
    BatchSetEventFlags: (lo, hi, on) => {
      for (let id = lo; id <= hi; id++) api.SetEventFlagID(id, on);
    },
    CharacterHPValue: id => id === 10000 ? state.hp : state.bossHp,
    CharacterDead: () => state.dead,
    CharacterHasSpEffect: (_, id) => id === 1627125 && state.rescue,
    PlayerInMap: () => true,
    InArea: (_, id) => id === 18000359,
    SaveRequest: () => state.saves.push(new Set(state.flags)),
    EndIf: yes => { if (yes) throw 'end'; },
    RestartIf: yes => { if (yes) throw 'restart'; },
    RestartEvent: () => { throw 'restart'; },
  };
  const context = vm.createContext(api);
  state.load = () => vm.runInContext(reset, context);
  state.add = (source, id) => {
    const body = source.match(new RegExp(`\\$Event\\(${id}, (?:Default|Restart), function\\(\\) \\{([\\s\\S]*?)\\n\\}\\);`))[1]
      .replace(/WaitFor\(([\s\S]*?)\);/g, 'yield {condition: () => ($1)};')
      .replace(/WaitFixedTimeFrames\((\d+)\);/g, 'yield {frames: $1};');
    const make = vm.runInContext(`(function*(){while(true){try{${body}return;}catch(e){if(e==='restart')continue;if(e==='end')return;throw e;}}})`, context);
    state.workers.push({ iterator: make(), wait: null, done: false });
  };
  state.frames = count => {
    for (let frame = 0; frame < count; frame++) {
      state.time++;
      for (const worker of state.workers) {
        for (let limit = 0; limit < 20 && !worker.done; limit++) {
          if (worker.wait?.condition && !worker.wait.condition()) break;
          if (worker.wait?.until > state.time) break;
          const next = worker.iterator.next();
          worker.done = next.done;
          worker.wait = next.value;
          if (worker.wait?.frames) worker.wait.until = state.time + worker.wait.frames;
        }
      }
    }
  };
  return state;
}

test('ordinary load clears encounter and preserves repeat dialogue, receipts and crystal', () => {
  const w = world([...losses, ...history, ...protectedFlags, 1055420915, 1055422933, 1055422947, 1055425233]);
  w.load();
  assert.deepEqual([...w.flags].sort(), [...protectedFlags, ...dialogueHistory].sort());
});

test('death reload preserves progression once, next deliberate load resets', () => {
  const w = world([marker, ...losses, ...history, ...protectedFlags, 1055420915]);
  w.load();
  assert(!w.flags.has(marker));
  assert(losses.every(id => w.flags.has(id)));
  assert(history.every(id => w.flags.has(id)));
  assert(w.flags.has(1055420915));
  w.load();
  assert.deepEqual([...w.flags].sort(), [...protectedFlags, ...dialogueHistory].sort());
});

test('pending normal and no-aid rewards defer reset without losing entitlement', () => {
  for (const flags of [[1055420915], [1055420915, 1055420916, 1055420937]]) {
    const w = world([...flags, ...losses]);
    const before = new Set(w.flags);
    w.load(); assert.deepEqual(w.flags, before);
    w.flags.add(1055420916); w.flags.add(1055420250);
    w.load(); assert(!w.flags.has(1055420915)); assert(!w.flags.has(losses[0]));
  }
});

test('client load and death cannot mutate the host reset state', () => {
  const w = world([...losses, marker]); w.host = false;
  w.load(); w.add(common, 5750425); w.frames(1); w.hp = 0; w.dead = true; w.frames(8);
  assert.deepEqual([...w.flags], [...losses, marker]); assert.equal(w.saves.length, 0);
});

test('native and confirmed deaths save after loss accounting in either worker order', () => {
  for (const [reversed, confirmed] of [[false, false], [true, false], [false, true], [true, true]]) {
    const w = world([1055422933, 1055420935]);
    const workers = [[common, 5750425], [map, 5750420]];
    if (reversed) workers.reverse();
    for (const [source, id] of workers) w.add(source, id);
    w.frames(2); w.hp = 0; w.dead = !confirmed;
    if (confirmed) w.flags.add(1055425042);
    w.frames(8);
    assert.equal(w.saves.length, 1);
    assert(w.saves[0].has(marker)); assert(w.saves[0].has(losses[0]));
    w.load(); assert(w.flags.has(losses[0])); assert(!w.flags.has(marker));
  }
});

test('zero HP, rescue and short-lived death do not mark a death reload', () => {
  for (const kind of ['zero', 'rescue', 'recovered']) {
    const w = world(); w.add(common, 5750425); w.frames(2); w.hp = 0;
    w.dead = kind !== 'zero'; w.rescue = kind === 'rescue';
    w.frames(1);
    if (kind === 'recovered') { w.hp = 500; w.dead = false; }
    w.frames(8); assert(!w.flags.has(marker)); assert.equal(w.saves.length, 0);
  }
});

test('outside-combat deaths preserve state; recovery without load clears marker', () => {
  const w = world(losses); w.add(common, 5750425); w.frames(2);
  w.hp = 0; w.dead = true; w.frames(8); assert(w.flags.has(marker));
  w.hp = 500; w.dead = false; w.frames(2); assert(!w.flags.has(marker));
  w.hp = 0; w.dead = true; w.frames(8); assert(w.flags.has(marker));
  assert.equal(w.saves.length, 2);
});

test('reset is inline in preconstructor, watcher does not restart on rest, retries use history', () => {
  const preconstructor = common.indexOf('$Event(50, Default, function() {');
  assert(common.indexOf('// BEGIN TEMPORARY HADEON LOAD RESET') > preconstructor);
  assert(common.indexOf('// END TEMPORARY HADEON LOAD RESET') < common.indexOf('$InitializeEvent(0, 700);', preconstructor));
  assert(common.includes('$Event(5750425, Default, function() {'));
  assert.equal(common.split('$InitializeEvent(0, 5750425);').length, 2);
  assert(!map.includes('SetEventFlagID(1055420935, OFF);'));
});
