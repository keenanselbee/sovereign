import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';
const source = readFileSync(new URL('../../src/events/common.emevd.dcx.js', import.meta.url), 'utf8');
const start = source.indexOf('$Event(5750362,');
const body = source.slice(source.indexOf('function() {', start) + 12, source.indexOf('\n});', start));
function suspend(code, name, wrap) {
  let i = 0;
  while ((i = code.indexOf(`${name}(`, i)) !== -1) {
    const first = i + name.length + 1; let end = first, depth = 1;
    while (depth) { if (code[end] === '(') depth++; if (code[end] === ')') depth--; end++; }
    const text = wrap(code.slice(first, end - 1));
    code = code.slice(0, i) + text + code.slice(end); i += text.length;
  }
  return code;
}
function opening(flags = []) {
  const s = { flags: new Set(flags), effects: new Set(), hp: 100, inMap: true, host: true, elapsed: false, calls: [] };
  const api = { ON: true, SoundType: { SFX: 5 }, DisableNetworkSync() {},
    PlayerIsInOwnWorld: () => s.host, PlayerInMap: () => s.inMap,
    EventFlag: id => s.flags.has(id), CharacterHPValue: () => s.hp,
    CharacterHasSpEffect: (_, id) => s.effects.has(id), ElapsedSeconds: () => s.elapsed,
    ClearSpEffect: (_, id) => s.effects.delete(id),
    SetSpEffect: (_, id) => { s.effects.add(id); s.calls.push(['effect', id]); },
    SetEventFlagID: (id, on) => on ? s.flags.add(id) : s.flags.delete(id),
    PlaySE: (...args) => s.calls.push(['sound', ...args]),
    EndIf: c => { if (c) throw 'end'; }, EndEvent: () => { throw 'end'; },
    RestartIf: c => { if (c) throw 'restart'; },
  };
  let code = suspend(body, 'WaitFor', x => `yield (() => (${x}))`);
  code = suspend(code, 'WaitFixedTimeSeconds', () => 'yield true');
  const iterator = vm.runInNewContext(`(function*(){${code}})`, api)(); let pending, done = false;
  s.step = () => {
    if (done || (typeof pending === 'function' && !pending())) return false;
    try { const n = iterator.next(); pending = n.value; done = n.done; }
    catch (e) { if (!['end', 'restart'].includes(e)) throw e; done = true; }
    return true;
  };
  s.drain = () => { for (let n = 0; n < 30 && s.step(); n++); };
  return s;
}
test('first arrival waits for cutscene and starts eclipse/landing without player aura', () => {
  const s = opening(); s.drain(); assert.equal(s.calls.length, 0);
  s.flags.add(10010020); s.effects.add(9621); s.drain(); assert.equal(s.calls.length, 0);
  s.effects.delete(9621); s.drain();
  assert.deepEqual(s.calls.filter(x => x[0] === 'effect'), [['effect', 1627113], ['effect', 1627121]]);
  assert(s.flags.has(1055420925));
  s.elapsed = true; s.drain(); assert(!s.effects.has(1627113)); assert(!s.effects.has(1627121));
  assert(body.includes('ElapsedSeconds(2.9)')); // Existing 0.1 + 2.9-second presentation.
});
test('visited or progressed saves cannot replay the opening landing', () => {
  for (const flag of [101, 1055420925]) { const s = opening([flag, 10010020]); s.drain(); assert.equal(s.calls.length, 0); }
});
test('death or leaving during the opening clears presentation', () => {
  for (const leave of [false, true]) {
    const s = opening([10010020]); s.drain();
    if (leave) s.inMap = false; else s.hp = 0;
    s.drain(); assert(!s.effects.has(1627113)); assert(!s.effects.has(1627121));
  }
});
test('opening starts on the first ready step without an extra timer', () => {
  const s = opening(); s.drain();
  s.flags.add(10010020); s.step();
  assert(s.effects.has(1627113)); assert(s.effects.has(1627121));
  assert(!body.includes('WaitFixedTimeSeconds(0.5)'));
});
