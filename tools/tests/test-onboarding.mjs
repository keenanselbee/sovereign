// Exercise authored control flow; native parameter checks and game acceptance are separate.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/common.emevd.dcx.js', import.meta.url), 'utf8');
const start = source.indexOf('$Event(5750009,');
const body = source.slice(source.indexOf('function() {', start) + 12, source.indexOf('\n});', start))
  .replaceAll('WaitFixedTimeSeconds(6);', 'yield 6;');
const receipts = new Map([[10116, 1055420800], [10117, 1055420800],
  [10156, 1055420801], [10157, 1055420801], [30880, 1055420802],
  [30890, 1055420803], [6900, 1055420260]]);

function world({ goods = [], flags = [], host = true } = {}) {
  const state = { goods: new Set(goods), flags: new Set(flags), awards: [], notices: 0, host };
  const end = Symbol('end');
  const context = vm.createContext({
    ON: true, OFF: false, ItemType: { Goods: 1 },
    PlayerIsInOwnWorld: () => state.host,
    PlayerHasItem: (_, id) => state.goods.has(id),
    EventFlag: id => state.flags.has(id),
    SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
    RemoveItemFromPlayer: (_, id) => state.goods.delete(id),
    AwardItemLot: id => {
      assert(receipts.has(id), `Unexpected compensation lot ${id}`);
      state.awards.push(id);
      state.flags.add(receipts.get(id));
    },
    DisplayBlinkingMessage: () => state.notices++,
    EndIf: condition => { if (condition) throw end; },
    EndEvent: () => { throw end; },
  });
  const factory = vm.runInContext(`(function* () {${body}})`, context);
  function run(onWait = () => {}) {
    const iterator = factory();
    try {
      for (let i = 0; i < 20; i++) {
        const step = iterator.next();
        if (step.done) return;
        assert.equal(step.value, 6);
        if (onWait(state) === 'reload') return;
      }
      assert.fail('Onboarding did not finish');
    } catch (error) { if (error !== end) throw error; }
  }
  return { state, run };
}

test('fresh characters finish once; simulated NG+ leaves their later spells intact', () => {
  const w = world(); w.run();
  assert(w.state.flags.has(69990));
  assert.deepEqual(w.state.awards, []);
  w.state.flags = new Set([69990]); // Persistence is an explicit game-test assumption.
  w.state.goods = new Set([6940, 6910, 6950, 6941, 2006910, 7050]);
  w.run();
  assert.equal(w.state.goods.size, 6);
  assert.deepEqual(w.state.awards, []);
});

test('clients perform no cleanup or grants', () => {
  const w = world({ goods: [8865, 7050], flags: [11109884], host: false }); w.run();
  assert.deepEqual([...w.state.goods], [8865, 7050]);
  assert.deepEqual([...w.state.flags], [11109884]);
  assert.deepEqual(w.state.awards, []);
});

test('prayerbook cleanup does not require owning either taught spell', () => {
  const w = world({ goods: [8865], flags: [11109884, 1037469315] }); w.run();
  assert(!w.state.goods.has(8865));
  assert(!w.state.flags.has(11109884)); assert(!w.state.flags.has(1037469315));
  assert(w.state.flags.has(69990));
});

test('all held vanilla spells exchange once without clearing normal boss receipts', () => {
  const flags = [9111, 510110, 9115, 510150, 1041520800, 530300, 2054390850, 530805];
  const w = world({ goods: [6940, 6910, 6950, 6941, 2006910, 7050], flags }); w.run();
  assert.deepEqual(w.state.awards, [30880, 10116, 30890, 10156]);
  assert.equal(w.state.goods.size, 0);
  for (const flag of flags) assert(w.state.flags.has(flag));
  w.run(); assert.equal(w.state.awards.length, 4);
});

test('previously rewarded bosses without spells receive heart-only catch-up', () => {
  const w = world({ flags: [9111, 510110, 9115, 510150, 1041520800, 530300, 2054390850, 530805] });
  w.run(); assert.deepEqual(w.state.awards, [30880, 10117, 30890, 10157]);
});

test('Florissax exchange and defeated Senessax produce one compensation', () => {
  const w = world({ goods: [2006910], flags: [2054390850, 530805] }); w.run();
  assert.deepEqual(w.state.awards, [30890]);
  assert(w.state.flags.has(530805));
});

test('Florissax exchange does not consume a future normal Senessax reward', () => {
  const w = world({ goods: [2006910] }); w.run();
  assert.deepEqual(w.state.awards, [30890]);
  assert(!w.state.flags.has(2054390850)); assert(!w.state.flags.has(530805));
});

test('pending normal rewards becoming delivered during a wait are not compensated again', () => {
  const w = world({ goods: [6940], flags: [9111, 9115, 1041520800, 2054390850] });
  w.run(() => { for (const flag of [510110, 510150, 530300, 530805]) w.state.flags.add(flag); });
  assert.deepEqual(w.state.awards, []);
});

test('reload during a later wait retains completed compensation receipts', () => {
  const w = world({ goods: [6950, 2006910], flags: [1041520800, 530300, 2054390850, 530805] });
  let waits = 0; w.run(() => ++waits === 2 ? 'reload' : undefined);
  assert.deepEqual(w.state.awards, [30880]); assert(!w.state.flags.has(69990));
  w.run(); assert.deepEqual(w.state.awards, [30880, 30890]);
  assert(w.state.flags.has(69990));
});

test('legitimate mod purchases and already settled compensation are preserved', () => {
  const w = world({ goods: [7050, 6941], flags: [1055420235, 1055420800, 9111, 510110] });
  w.run(); assert.deepEqual(w.state.awards, []);
  assert(w.state.goods.has(7050)); assert(w.state.goods.has(6941));
});

test('Perfect Runeseal recovery still runs once', () => {
  const w = world({ flags: [60848] }); w.run(); w.run();
  assert.deepEqual(w.state.awards, [6900]); assert(w.state.flags.has(1055420260));
});
