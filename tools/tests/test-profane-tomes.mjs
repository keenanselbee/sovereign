// Execute the authored event control flow. Native builds and in-game checks are separate.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/common.emevd.dcx.js', import.meta.url), 'utf8');
const data = JSON.parse(readFileSync(new URL('../../src/tomes/profane-tomes.json', import.meta.url), 'utf8'));
const books = data.books;
const numberedLots = new Map(books.flatMap(book => book.variants.map(id => [id * 10, id])));
function suspend(body, name, wrap) {
  let start = 0;
  while ((start = body.indexOf(`${name}(`, start)) !== -1) {
    const open = start + name.length;
    let end = open + 1, depth = 1;
    while (depth) {
      if (body[end] === '(') depth++;
      if (body[end] === ')') depth--;
      end++;
    }
    const replacement = wrap(body.slice(open + 1, end - 1));
    body = body.slice(0, start) + replacement + body.slice(end);
    start += replacement.length;
  }
  return body;
}
function world() {
  const state = { host: true, goods: new Set(), armor: new Set(), weapon: new Set(),
    flags: new Set(), awards: [], deliver: true };
  const stop = control => { throw { control }; };
  const api = {
    ON: true, OFF: false, ItemType: { Goods: 'goods', Armor: 'armor', Weapon: 'weapon' },
    tomeCheck: 0,
    PlayerIsInOwnWorld: () => state.host,
    PlayerHasItem: (kind, id) => state[kind].has(id),
    PlayerHasItemIncludingBBox: (kind, id) => state[kind].has(id),
    EventFlag: id => state.flags.has(id),
    SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
    AwardItemLot: id => {
      state.awards.push(id);
      if (id === 7000 || id === 7010) state.weapon.add(id === 7000 ? 34100000 : 34200000);
      else {
        assert(numberedLots.has(id), `Unknown numbered tome lot ${id}`);
        // The engine awards consecutive lot IDs together, so a missing gap is dangerous.
        if (state.deliver) for (let lot = id; numberedLots.has(lot); lot++) state.goods.add(numberedLots.get(lot));
      }
    },
    RemoveItemFromPlayer: (kind, id) => state[kind].delete(id),
    EndIf: value => { if (value) stop('end'); },
    EndEvent: () => stop('end'), RestartEvent: () => stop('restart'),
    DisplayBlinkingMessage() {},
  };
  const context = vm.createContext(api);
  function event(id = data.eventId) {
    const start = source.indexOf(`$Event(${id},`);
    assert.notEqual(start, -1);
    let body = source.slice(source.indexOf('function() {', start) + 12, source.indexOf('\n});', start));
    body = suspend(body, 'WaitFor', expression => `yield (() => (${expression})); tomeCheck = 0`);
    body = suspend(body, 'WaitFixedTimeSeconds', seconds => `yield (${seconds}); tomeCheck = 0`);
    const factory = vm.runInContext(`(function* () {${body}})`, context);
    let iterator = factory(), pending, ended = false;
    return {
      step() {
        if (ended) return 'end';
        if (typeof pending === 'function' && !pending()) return 'waiting';
        try {
          const result = iterator.next(); pending = result.value; ended = result.done;
          return ended ? 'end' : typeof pending === 'function' ? 'waiting' : 'delay';
        } catch (error) {
          if (!error.control) throw error;
          pending = undefined; context.tomeCheck = 0;
          if (error.control === 'restart') iterator = factory(); else ended = true;
          return error.control;
        }
      },
      advance(count = 1000) { for (let i = 0; i < count; i++) this.step(); },
    };
  }
  return { state, event };
}

test('discovery order determines eight unique numbers; repeated receipts cannot add books', () => {
  const w = world(), worker = w.event();
  const order = [4, 7, 1, 5, 0, 3, 6, 2];
  for (const [number, subject] of order.entries()) {
    const book = books[subject];
    w.state.goods.add(book.receiptGoods); worker.advance();
    assert(w.state.goods.has(book.variants[number]));
    assert(!w.state.goods.has(book.receiptGoods));
    assert(w.state.flags.has(book.collectedFlag));
    assert(!w.state.flags.has(book.availableFlag));
  }
  assert.equal(w.state.awards.length, 8);
  for (const book of books) w.state.goods.add(book.receiptGoods);
  worker.advance();
  assert.equal(w.state.awards.length, 8);
  assert.equal(w.state.goods.size, 8);
});

test('NG+ restores availability and knowledge from retained books without renumbering', () => {
  const w = world(), worker = w.event();
  w.state.goods.add(books[7].variants[0]);
  w.state.goods.add(books[5].variants[1]);
  w.state.armor.add(110000); w.state.weapon.add(34200000);
  worker.advance(); w.state.flags.clear(); worker.advance();
  for (const index of [5, 7]) {
    assert(w.state.flags.has(books[index].collectedFlag));
    assert(!w.state.flags.has(books[index].availableFlag));
  }
  assert(w.state.flags.has(books[0].availableFlag));
  for (const flag of [1055420240, 1055420245, 1055420220, data.hatFlag]) assert(w.state.flags.has(flag));
  assert.equal(w.state.awards.length, 0);
});

test('a pending award keeps its receipt; reload after delivery cannot duplicate the number', () => {
  const w = world(), worker = w.event(), book = books[3];
  w.state.deliver = false; w.state.goods.add(book.receiptGoods); worker.advance();
  assert.equal(w.state.awards.length, 1);
  assert(w.state.goods.has(book.receiptGoods));
  w.state.goods.add(book.variants[0]);
  w.event().advance();
  assert(!w.state.goods.has(book.receiptGoods));
  assert.equal(w.state.awards.length, 1);
});

test('guests perform no inventory or flag writes', () => {
  const w = world(); w.state.host = false; w.state.goods.add(8872);
  assert.equal(w.event().step(), 'end');
  assert.equal(w.state.flags.size, 0); assert.equal(w.state.awards.length, 0);
  assert(w.state.goods.has(8872));
});

test('Gyre hat acquisition is independent of tome knowledge', () => {
  const w = world(); w.state.armor.add(110000); w.event().advance();
  assert(w.state.flags.has(data.hatFlag));
  assert(!w.state.flags.has(1055420245));
});

test('recipe availability requires the actual tome, and crafted equipment hides its recipe', () => {
  for (const [index, eventId, availability, craftedReceipt] of [[5, 5750035, 1055420241, 9160], [7, 5750036, 1055420246, 9161]]) {
    const w = world(); w.state.flags.add(availability - 1);
    const worker = w.event(eventId); worker.advance();
    assert(!w.state.flags.has(availability));
    w.state.goods.add(books[index].variants[0]); worker.advance();
    assert(w.state.flags.has(availability));
    w.state.goods.add(craftedReceipt); worker.advance();
    assert(!w.state.flags.has(availability));
    w.state.flags.add(availability); w.event(eventId).advance();
    assert(!w.state.flags.has(availability));
  }
});
