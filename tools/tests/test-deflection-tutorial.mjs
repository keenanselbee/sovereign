// Source control-flow checks; popup timing and engine area detection still need a game test.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/m18_00_00_00.emevd.dcx.js', import.meta.url), 'utf8');
const match = source.match(/\$Event\(18002663, Restart, function\(([^)]*)\) \{([\s\S]*?)\n\}\);/);
let body = match[2];
let index = 0;
while ((index = body.indexOf('WaitFor(', index)) !== -1) {
  let end = index + 8, depth = 1;
  while (depth) { if (body[end] === '(') depth++; if (body[end] === ')') depth--; end++; }
  const replacement = `yield (() => (${body.slice(index + 8, end - 1)}))`;
  body = body.slice(0, index) + replacement + body.slice(end);
  index += replacement.length;
}

function run(overrides = {}) {
  const state = { inside: false, inMap: true, hp: 500, host: true, seconds: 0,
    flags: new Set(), calls: [], multiplayer: false, ...overrides };
  const api = {
    ON: true, ItemType: { Goods: 3 }, MultiplayerState: { Multiplayer: 1 },
    DisableNetworkSync() {}, PlayerIsInOwnWorld: () => state.host,
    PlayerInMap: () => state.inMap, CharacterHPValue: () => state.hp,
    InArea: (_, id) => id === 18002658 && state.inside,
    EventFlag: id => state.flags.has(id), ElapsedSeconds: seconds => state.seconds >= seconds,
    SetEventFlagID: id => state.flags.add(id), HasMultiplayerState: () => state.multiplayer,
    ShowTutorialPopup: id => state.calls.push(['popup', id]),
    DirectlyGivePlayerItem: (_, id) => state.calls.push(['item', id]),
    EndIf: condition => { if (condition) throw 'end'; },
    RestartIf: condition => { if (condition) throw 'restart'; },
  };
  const iterator = vm.runInNewContext(`(function*(${match[1]}) {${body}})(1180, 710180, 9106, 69060, 18002658)`, api);
  let wait = null, done = false;
  state.step = () => {
    if (done) return 'end';
    if (wait && !wait()) return 'wait';
    try { const result = iterator.next(); wait = result.value; done = result.done; return done ? 'end' : 'wait'; }
    catch (error) { if (!['end', 'restart'].includes(error)) throw error; done = true; return error; }
  };
  return state;
}

test('walking through the knight approach box shows deflection after two seconds, even after exiting', () => {
  const state = run();
  state.step(); state.step(); assert.equal(state.calls.length, 0);
  state.inside = true; state.step(); state.inside = false;
  state.seconds = 1.9; state.step(); assert.equal(state.calls.length, 0);
  state.seconds = 2; assert.equal(state.step(), 'end');
  assert.deepEqual(state.calls, [['popup', 1180], ['item', 9106]]);
  assert(state.flags.has(710180)); assert(state.flags.has(69060));
});

test('death or map departure cancels without consuming the lesson and allows a fresh attempt', () => {
  for (const interrupt of [state => state.hp = 0, state => state.inMap = false]) {
    const state = run({ inside: true }); state.step(); state.step(); interrupt(state);
    assert.equal(state.step(), 'restart'); assert.equal(state.calls.length, 0);
    assert.equal(state.flags.size, 0);
    const retry = run({ flags: state.flags, inside: true }); retry.step(); retry.step(); retry.seconds = 2;
    assert.equal(retry.step(), 'end'); assert(retry.flags.has(710180));
  }
});

test('guests and previously taught players do not receive the popup again', () => {
  for (const options of [{ host: false }, { flags: new Set([710180]) }]) {
    const state = run({ inside: true, seconds: 2, ...options });
    assert.equal(state.step(), 'end'); assert.equal(state.calls.length, 0);
  }
  const state = run({ inside: true, flags: new Set([69060, 18000850]), seconds: 2 });
  state.step(); state.step(); state.step();
  assert.deepEqual(state.calls, [['popup', 1180]], 'Rick defeat does not suppress the earlier knight lesson; its note is not duplicated');
});
