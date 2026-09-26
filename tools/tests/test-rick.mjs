// Execute the authored event control flow with mocked engine state. Not an engine/warp test.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/m18_00_00_00.emevd.dcx.js', import.meta.url), 'utf8');
const player = 10000, soldier = 18000851, rick = 18000850, saved = 1055420926;
function body(id) {
  const start = source.indexOf(`$Event(${id},`);
  assert.notEqual(start, -1);
  return source.slice(source.indexOf('function() {', start) + 12, source.indexOf('\n});', start));
}
function suspend(code, name, wrap) {
  let start = 0;
  while ((start = code.indexOf(`${name}(`, start)) !== -1) {
    const open = start + name.length;
    let end = open + 1, depth = 1;
    while (depth) { if (code[end] === '(') depth++; if (code[end] === ')') depth--; end++; }
    const replacement = wrap(code.slice(open + 1, end - 1));
    code = code.slice(0, start) + replacement + code.slice(end);
    start += replacement.length;
  }
  return code;
}
function encounter(flags = []) {
  const state = { flags: new Set(flags), hp: new Map([[player, 500], [soldier, 1000], [rick, 1000]]),
    admitted: false, loaded: true, critical: false, calls: [], effects: new Set() };
  const api = { ON: true, OFF: false, Enabled: 1, Disabled: 0, L9: 9,
    CharacterUpdateFrequency: { AlwaysUpdate: 0 }, TargetEntityType: { Character: 0 },
    BossBGMState: { Start: 1, Stop1: 0 }, SoundType: { CharacterMotion: 1, SFX: 5 },
    PlayerIsInOwnWorld: () => true, PlayerInMap: () => true,
    EventFlag: id => state.flags.has(id), CharacterHPValue: id => state.hp.get(id),
    HPRatio: id => state.hp.get(id) / 1000, InArea: () => state.admitted,
    CharacterBackreadStatus: () => state.loaded, ElapsedSeconds: () => true,
    CharacterHasSpEffect: (id, effect) => effect === 18480 ? state.critical : state.effects.has(`${id}:${effect}`),
    SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
    SetSpEffect: (id, effect) => { state.effects.add(`${id}:${effect}`); if (effect === 110) state.hp.set(id, 1000); },
    ClearSpEffect: (id, effect) => state.effects.delete(`${id}:${effect}`),
    EndEvent: () => { throw 'end'; }, EndIf: condition => { if (condition) throw 'end'; },
    GotoIf: (_, condition) => { if (condition) throw 'cleanup'; },
  };
  api.SetNetworkconnectedEventFlagID = api.SetEventFlagID;
  for (const id of [18002860, 18002861, 18002862]) {
    for (const match of body(id).matchAll(/\b([A-Z]\w+)\(/g)) {
      const name = match[1];
      if (!(name in api)) api[name] = (...args) => state.calls.push([name, ...args]);
    }
  }
  const context = vm.createContext(api);
  state.start = (id = 18002860) => {
    const [main, cleanup = ''] = body(id).split('L9:');
    let code = suspend(main, 'WaitFor', expr => `yield (() => (${expr}))`);
    for (const wait of ['WaitFixedTimeSeconds', 'WaitFixedTimeFrames']) code = suspend(code, wait, () => 'yield true');
    const iterator = vm.runInContext(`(function*(){${code}})`, context)();
    let pending, done = false;
    return {
      step() {
        if (done || (typeof pending === 'function' && !pending())) return false;
        try { const next = iterator.next(); pending = next.value; done = next.done; }
        catch (error) {
          if (!['end', 'cleanup'].includes(error)) throw error;
          if (error === 'cleanup') vm.runInContext(cleanup, context);
          done = true;
        }
        return true;
      },
      drain() { for (let n = 0; n < 100 && this.step(); n++); },
    };
  };
  return state;
}

test('first attempt waits for admission, threshold, critical completion and loading, then bursts once', () => {
  const s = encounter(), event = s.start(); event.drain();
  assert(!s.calls.some(c => c[0] === 'EnableCharacterAI'));
  s.admitted = true; s.flags.add(18002855); event.drain();
  s.hp.set(soldier, 250); s.critical = true; event.drain();
  assert(!s.flags.has(18002851)); assert(s.effects.has(`${soldier}:1627116`));
  s.critical = false; s.loaded = false; event.drain();
  assert(!s.flags.has(18002851));
  s.loaded = true; event.drain();
  assert(!s.flags.has(saved)); assert(s.flags.has(18002852)); assert(!s.flags.has(18002851));
  const warp = s.calls.findIndex(c => c[0] === 'WarpCharacterAndCopyFloor');
  const reveal = s.calls.findIndex(c => c[0] === 'EnableCharacter' && c[1] === rick);
  const blasts = s.calls.filter(c => c[0] === 'ShootBullet');
  assert(warp >= 0 && reveal > warp); assert.equal(blasts.length, 1);
  assert.equal(blasts[0][1], rick); assert.equal(blasts[0][2], rick); assert.equal(blasts[0][4], 75431100);
  assert(!s.effects.has(`${rick}:1627117`)); assert(!s.effects.has(`${rick}:1627116`));
  assert(!s.effects.has(`${soldier}:1627118`));
});

test('old awakening flag cannot skip phase one on a new attempt', () => {
  const s = encounter([saved]); const event = s.start(); event.drain();
  assert(!s.flags.has(18002852));
  assert(s.calls.some(c => c[0] === 'EnableCharacter' && c[1] === soldier));
  assert(!s.calls.some(c => c[0] === 'EnableCharacter' && c[1] === rick));
  s.admitted = true; s.flags.add(18002855); event.drain();
  assert(s.calls.some(c => c[0] === 'EnableCharacterAI' && c[1] === soldier));
  assert(!s.calls.some(c => c[0] === 'ShootBullet'));
});

test('death during the reset boundary prevents forced kneel and burst', () => {
  const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
  const event = s.start();
  for (let n = 0; n < 30 && !s.calls.some(c => c[0] === 'RequestCharacterAnimationReset'); n++) event.step();
  assert(s.calls.some(c => c[0] === 'RequestCharacterAnimationReset'));
  assert(!s.calls.some(c => c[0] === 'ForceAnimationPlayback'));
  s.hp.set(player, 0); event.drain();
  assert(!s.calls.some(c => c[0] === 'ForceAnimationPlayback'));
  assert(!s.calls.some(c => c[0] === 'ShootBullet'));
});

test('death after Rick activates but before his shot cancels the burst', () => {
  const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
  const event = s.start();
  for (let n = 0; n < 30 && !s.calls.some(c => c[0] === 'EnableCharacter' && c[1] === rick); n++) event.step();
  assert(s.calls.some(c => c[0] === 'EnableCharacter' && c[1] === rick));
  assert(!s.calls.some(c => c[0] === 'ShootBullet'));
  s.hp.set(player, 0); event.drain();
  assert(!s.calls.some(c => c[0] === 'ShootBullet'));
  assert(!s.calls.some(c => c[0] === 'EnableCharacterAI' && c[1] === rick));
});

test('death during the warning cancels the burst and removes the glow and protection', () => {
  const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
  const event = s.start();
  for (let n = 0; n < 30 && !s.flags.has(18002851); n++) event.step();
  assert(s.flags.has(18002851)); assert(s.effects.has(`${soldier}:1627118`));
  s.hp.set(player, 0); event.drain();
  assert(!s.calls.some(c => c[0] === 'ShootBullet'));
  assert(!s.flags.has(18002851)); assert(!s.flags.has(18002852));
  assert(!s.effects.has(`${soldier}:1627118`)); assert(!s.effects.has(`${rick}:1627117`));
});

test('burst hands combat to Rick after brief recovery without a forced kneel', () => {
  const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
  const event = s.start();
  for (let n = 0; n < 30 && !s.calls.some(c => c[0] === 'ShootBullet'); n++) event.step();
  assert(!s.calls.some(c => c[0] === 'EnableCharacterAI' && c[1] === rick));
  assert(body(18002860).includes('ElapsedSeconds(0.5)'));
  event.drain();
  const shot = s.calls.findIndex(c => c[0] === 'ShootBullet');
  const ai = s.calls.findIndex(c => c[0] === 'EnableCharacterAI' && c[1] === rick);
  assert(shot >= 0 && ai > shot);
  assert(s.calls.some(c => c[0] === 'RequestCharacterAIReplan' && c[1] === rick));
  assert(!s.calls.some(c => c[0] === 'ForceAnimationPlayback'));
  assert(!s.effects.has(`${rick}:1627116`)); assert(!s.effects.has(`${rick}:1627117`));
  assert(!s.effects.has(`${soldier}:1627119`));
  assert(!s.flags.has(saved));
});


test('completed boss stays absent', () => {
  const s = encounter([18000850, saved]); s.start().drain();
  assert(!s.calls.some(c => c[0] === 'EnableCharacter'));
  assert(!s.calls.some(c => c[0] === 'EnableCharacterAI'));
});

test('retry music starts phase one even with the obsolete awakening flag', () => {
  const s = encounter([saved, 18002855]); s.admitted = true;
  const music = s.start(18002862); music.drain();
  assert(s.calls.some(c => c[0] === 'SetBossBGM' && c[1] === 931000 && c[2] === 1));
  assert(!s.calls.some(c => c[0] === 'SetBossBGM' && c[1] === 219000 && c[2] === 1));
  s.flags.add(18002851); music.drain(); s.flags.add(18002852); music.drain();
  assert(s.calls.some(c => c[0] === 'SetBossBGM' && c[1] === 219000 && c[2] === 1));
});

test('warning and vocal contain no fade or player animation freeze', () => {
  assert(!body(18002861).includes('FadeToBlack'));
  assert(!body(18002860).includes('ForceAnimationPlayback(10000'));
  assert(body(18002860).includes('ElapsedSeconds(2)'));
  assert(!source.includes('EventFlag(1055420926)'));
});

test('missing pose acknowledgement is bounded and still retains the warning', () => {
  const code = body(18002860);
  const ack = code.indexOf('CharacterHasSpEffect(18000851, 1627119) || ElapsedSeconds(1)');
  const warning = code.indexOf('ElapsedSeconds(2)');
  const shot = code.indexOf('ShootBullet(');
  assert(ack >= 0 && warning > ack && shot > warning);
  assert.equal(code.match(/ClearSpEffect\(18000851, 1627119\)/g).length, 3);
});

test('death during half-second recovery clears protection without activating Rick', () => {
  const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
  const event = s.start();
  for (let n = 0; n < 30 && !s.calls.some(c => c[0] === 'ShootBullet'); n++) event.step();
  assert(s.calls.some(c => c[0] === 'ShootBullet'));
  s.hp.set(player, 0); event.drain();
  assert(!s.calls.some(c => c[0] === 'EnableCharacterAI' && c[1] === rick));
  assert(!s.effects.has(`${rick}:1627116`)); assert(!s.flags.has(18002852));
});

test('local audio requests two simultaneous vocals and one charge/explosion cue', () => {
  const s = encounter([18002855]); const event = s.start(18002861); event.drain();
  assert(!s.calls.some(c => c[0] === 'PlaySE'));
  s.flags.add(18002851); event.drain();
  assert.deepEqual(s.calls.filter(c => c[0] === 'PlaySE'), [
    ['PlaySE', 18000852, 1, 472108006], ['PlaySE', 18000852, 1, 472108006],
    ['PlaySE', soldier, 5, 525305]]);
  s.flags.add(18002852); event.drain(); event.drain();
  assert.equal(s.calls.filter(c => c[0] === 'PlaySE' && c[3] === 525316).length, 1);
});

test('aborted warning never plays explosion audio', () => {
  const s = encounter([18002855, 18002851]); const event = s.start(18002861); event.drain();
  s.hp.set(player, 0); event.drain();
  assert(!s.calls.some(c => c[0] === 'PlaySE' && c[3] === 525316));
});

test('combat-ready hold lasts through recovery and clears on release or death', () => {
  for (const die of [false, true]) {
    const s = encounter([18002855]); s.admitted = true; s.hp.set(soldier, 250);
    const event = s.start();
    for (let n = 0; n < 30 && !s.calls.some(c => c[0] === 'ShootBullet'); n++) event.step();
    assert(s.effects.has(`${rick}:1627120`));
    if (die) s.hp.set(player, 0);
    event.drain();
    assert(!s.effects.has(`${rick}:1627120`));
    assert.equal(s.calls.some(c => c[0] === 'EnableCharacterAI' && c[1] === rick), !die);
  }
});

test('audio gate starts with the glow before pose acknowledgement', () => {
  const code = body(18002860);
  const glow = code.indexOf('SetSpEffect(18000851, 1627118)');
  const audio = code.indexOf('SetEventFlagID(18002851, ON)');
  const ack = code.indexOf('WaitFor(CharacterHasSpEffect(18000851, 1627119)');
  assert(glow >= 0 && audio > glow && ack > audio);
});
