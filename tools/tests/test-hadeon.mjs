// Source-level control-flow tests. Native EMEVD and in-game behavior need separate checks.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const source = readFileSync(new URL('../../src/events/m18_00_00_00.emevd.dcx.js', import.meta.url), 'utf8');
const boss = 18002354;
const player = 10000;
const fall = 18002367;
const arena = 18000359;

// Suspend the actual authored event body at waits; the harness supplies engine state.
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

function encounter() {
  const state = {
    host: true, hp: new Map([[boss, 1000], [player, 500]]),
    flags: new Set([1055422933]), areas: new Set([`${player}:${arena}`]),
    effects: new Map(), grants: [], warpWorks: true,
  };
  const stop = kind => { throw { control: kind }; };
  const api = {
    ON: true, OFF: false, Disabled: 0, SoundType: { SFX: 0 },
    TargetEntityType: { Character: 0, Area: 1 }, BossBGMState: { Stop1: 0 },
    PlayerIsInOwnWorld: () => state.host,
    EventFlag: id => state.flags.has(id),
    SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
    BatchSetEventFlags: (first, last, on) => {
      for (let id = first; id <= last; id++) api.SetEventFlagID(id, on);
    },
    RandomlySetEventFlagInRange: first => state.flags.add(first),
    CharacterHPValue: id => state.hp.get(id),
    HPRatio: id => state.hp.get(id) / 1000,
    InArea: (id, region) => state.areas.has(`${id}:${region}`),
    SetSpEffect: (id, effect) => {
      state.effects.set(`${id}:${effect}`, true);
      state.grants.push([id, effect]);
      if (effect === 1627100) state.hp.set(id, Math.max(0, state.hp.get(id) - 50));
      if (effect === 1627101) state.hp.set(id, Math.max(0, state.hp.get(id) - 100));
      if (effect === 1626935) state.hp.set(id, 1000);
    },
    ClearSpEffect: (id, effect) => state.effects.delete(`${id}:${effect}`),
    WarpCharacterAndCopyFloor: id => {
      if (state.warpWorks) state.areas.delete(`${id}:${fall}`);
    },
    EndIf: condition => { if (condition) stop('end'); },
    EndEvent: () => stop('end'), RestartEvent: () => stop('restart'),
    $InitializeEvent() {}, PlaySE() {}, SpawnOneshotSFX() {},
    RequestCharacterAnimationReset() {}, DisplayBossHealthBar() {}, SetBossBGM() {},
  };
  const context = vm.createContext(api);
  function event(id) {
    const start = source.indexOf(`$Event(${id},`);
    assert.notEqual(start, -1);
    let body = source.slice(source.indexOf('function() {', start) + 12, source.indexOf('\n});', start));
    body = suspend(body, 'WaitFor', expression => `yield (() => (${expression}))`);
    body = suspend(body, 'WaitFixedTimeSeconds', seconds => `yield (${seconds})`);
    const factory = vm.runInContext(`(function* () {${body}})`, context);
    let iterator = factory(), pending, ended = false;
    return {
      step() {
        if (ended) return 'end';
        if (typeof pending === 'function' && !pending()) return 'waiting';
        try {
          const result = iterator.next();
          pending = result.value;
          ended = result.done;
          return ended ? 'end' : typeof pending === 'function' ? 'waiting' : 'delay';
        } catch (error) {
          if (!error.control) throw error;
          pending = undefined;
          if (error.control === 'restart') iterator = factory();
          else ended = true;
          return error.control;
        }
      },
      advance(count = 12) { for (let i = 0; i < count; i++) this.step(); },
    };
  }
  return { state, event, count: effect => state.grants.filter(([, id]) => id === effect).length };
}

test('milestones catch skipped thresholds and cannot repeat at the same HP', () => {
  const e = encounter(); const worker = e.event(5750306);
  worker.advance(); assert.equal(e.state.grants.length, 0);
  e.state.hp.set(boss, 200); worker.advance();
  assert.equal(e.count(1626935), 1);
  assert.equal(e.count(1626916), 1);
  assert.equal(e.count(1626976), 1);
  assert.equal(e.count(1627101), 1);
  assert.equal(e.state.hp.get(boss), 100);
  worker.advance(); assert.equal(e.count(1627101), 1);
});

test('full-health heal still consumes its milestone', () => {
  const e = encounter(); e.state.hp.set(player, 1000); e.state.hp.set(boss, 750);
  const worker = e.event(5750306); worker.advance();
  e.state.hp.set(player, 100); worker.advance();
  assert.equal(e.count(1626935), 1); assert.equal(e.state.hp.get(player), 100);
});

test('leaving during shriek sound delay prevents damage and preserves eligibility', () => {
  const e = encounter(); e.state.hp.set(boss, 250);
  const worker = e.event(5750306);
  worker.step(); worker.step(); // threshold wait, then first sound delay
  e.state.areas.clear(); worker.advance();
  assert.equal(e.count(1627101), 0); assert.equal(e.state.flags.has(1055422932), false);
  e.state.areas.add(`${player}:${arena}`); worker.advance();
  assert.equal(e.count(1627101), 1);
});

test('real fall charges once after arrival and never while return is stuck', () => {
  const e = encounter(); e.state.areas.add(`${boss}:${fall}`); e.state.warpWorks = false;
  const worker = e.event(5750304); worker.advance();
  assert.equal(e.count(1627100), 0);
  e.state.areas.delete(`${boss}:${fall}`); worker.advance();
  assert.equal(e.count(1627100), 1); assert.equal(e.state.hp.get(boss), 950);
  worker.advance(); assert.equal(e.count(1627100), 1);
});

test('other recovery regions and dead players do not cause fall damage', () => {
  const e = encounter(); e.state.areas.add(`${boss}:18002349`);
  e.event(5750304).advance(); assert.equal(e.count(1627100), 0);
  const dead = encounter(); dead.state.hp.set(player, 0); dead.state.areas.add(`${boss}:${fall}`);
  dead.event(5750304).advance(); assert.equal(dead.count(1627100), 0);
});

test('presence stops on exit; death clears milestones; retreat does not', () => {
  const e = encounter(); e.state.flags.add(1055422930);
  const worker = e.event(5750305); worker.advance(1);
  assert.equal(e.state.effects.has(`${player}:1627102`), true);
  e.state.areas.clear(); worker.advance();
  assert.equal(e.state.effects.has(`${player}:1627102`), false);
  assert.equal(e.state.flags.has(1055422930), true);
  e.state.hp.set(player, 0); worker.advance();
  assert.equal(e.state.flags.has(1055422930), false);
});

test('guests and completed encounters receive no encounter grants', () => {
  for (const mode of ['guest', 'defeated']) {
    const e = encounter(); e.state.hp.set(boss, 200);
    if (mode === 'guest') e.state.host = false;
    else e.state.flags.add(1055420915);
    for (const id of [5750304, 5750305, 5750306]) e.event(id).advance();
    assert.equal(e.state.grants.length, 0);
  }
});
