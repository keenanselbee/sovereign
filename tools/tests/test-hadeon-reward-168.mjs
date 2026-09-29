import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/m18_00_00_00.emevd.dcx.js', import.meta.url), 'utf8');
const body = source.match(/\$Event\(5750290, Restart, function\(\) \{([\s\S]*?)\n\}\);/)[1]
  .replaceAll('WaitFor(', 'yield (() => ').replaceAll('WaitFixedTimeSeconds(5);', 'yield (() => now() >= startDelay() + 5);');

function run(initial = []) {
  const state = { flags: new Set(initial), time: 0, dead: false, awards: 0 };
  let delayStart;
  const api = {
    now: () => state.time,
    startDelay: () => delayStart ??= state.time,
    PlayerIsInOwnWorld: () => true,
    EventFlag: id => state.flags.has(id),
    CharacterDead: () => state.dead,
    EndIf: value => { if (value) throw 'end'; },
    EndEvent: () => { throw 'end'; },
    AwardItemLot: id => { assert.equal(id, 6050); state.awards++; state.flags.add(1055420916); },
  };
  const iterator = vm.runInNewContext(`(function*(){${body}})()`, api);
  let wait, ended = false;
  state.step = () => {
    if (ended) return;
    try {
      while (!wait || wait()) {
        const next = iterator.next();
        if (next.done) { ended = true; return; }
        wait = next.value;
      }
    } catch (error) {
      if (error !== 'end') throw error;
      ended = true;
    }
  };
  return state;
}

test('live reward waits for actual banner, then five seconds', () => {
  const state = run(); state.step();
  state.flags.add(1055420915); state.time = 30; state.step();
  assert.equal(state.awards, 0);
  state.flags.add(1055425255); state.step();
  state.time = 34.99; state.step(); assert.equal(state.awards, 0);
  state.time = 35; state.step(); assert.equal(state.awards, 1);
  state.step(); assert.equal(state.awards, 1);
});
test('reload recovers an earned reward without requiring temporary banner flag', () => {
  const state = run([1055420915]); state.step(); assert.equal(state.awards, 1);
  const collected = run([1055420915,1055420916]); collected.step(); assert.equal(collected.awards, 0);
});
test('dead player waits until alive and already-collected rewards are not duplicated', () => {
  const state = run([1055420915]); state.dead = true; state.step(); assert.equal(state.awards, 0);
  state.dead = false; state.step(); assert.equal(state.awards, 1);
  const other = run(); other.step(); other.flags.add(1055425255); other.step();
  other.flags.add(1055420916); other.time = 5; other.step(); assert.equal(other.awards, 0);
});
test('boss signals the reward immediately after banner display', () => {
  assert.match(source, /HandleBossDefeatAndDisplayBanner\(18002354, TextBannerType.GreatEnemyFelled\);\s*SetEventFlagID\(1055425255, ON\);/);
});
