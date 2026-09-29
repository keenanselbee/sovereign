// Source control-flow checks. Area detection, subtitle timing and playback still need a game test.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

const mapSource = readFileSync(new URL('../../src/events/m18_00_00_00.emevd.dcx.js', import.meta.url), 'utf8');
const commonSource = readFileSync(new URL('../../src/events/common.emevd.dcx.js', import.meta.url), 'utf8');
const hksSource = readFileSync(new URL('../../mod/action/script/c0000.hks', import.meta.url), 'utf8');

function event(source, id) {
  const match = source.match(new RegExp(`\\$Event\\(${id}, Restart, function\\(\\) \\{([\\s\\S]*?)\\n\\}\\);`));
  assert(match, `Event ${id} is missing`);
  return match[1];
}

function suspend(code, name) {
  let at = 0;
  while ((at = code.indexOf(`${name}(`, at)) !== -1) {
    const begin = at + name.length + 1;
    let end = begin, depth = 1;
    while (depth) {
      if (code[end] === '(') depth++;
      if (code[end] === ')') depth--;
      end++;
    }
    const replacement = `yield (() => (${code.slice(begin, end - 1)}))`;
    code = code.slice(0, at) + replacement + code.slice(end);
    at += replacement.length;
  }
  return code;
}

function run(overrides = {}) {
  const state = {
    inMap: true, host: true, inside: false, hp: 500, seconds: 0,
    flags: new Set([18002855]), calls: [], ...overrides,
  };
  const api = {
    ON: true,
    DisableNetworkSync() {},
    PlayerIsInOwnWorld: () => state.host,
    PlayerInMap: (...map) => state.inMap && map.join(',') === '18,0,0,0',
    InArea: (_, area) => area === 18002850 && state.inside,
    CharacterHPValue: () => state.hp,
    EventFlag: flag => state.flags.has(flag),
    ElapsedSeconds: seconds => state.seconds >= seconds,
    SetEventFlagID: (flag, value) => value ? state.flags.add(flag) : state.flags.delete(flag),
    ShowTutorialPopup: id => state.calls.push(['popup', id]),
    EndIf: condition => { if (condition) throw 'end'; },
    RestartIf: condition => { if (condition) throw 'restart'; },
    EndEvent: () => { throw 'end'; },
  };
  const body = suspend(event(mapSource, 5750363), 'WaitFor');
  const iterator = vm.runInNewContext(`(function*() {${body}})()`, api);
  let wait = null, done = false;
  state.step = () => {
    if (done) return 'end';
    if (wait && !wait()) return 'wait';
    try {
      const result = iterator.next();
      wait = result.value;
      done = result.done;
      return done ? 'end' : 'wait';
    } catch (error) {
      if (error !== 'end' && error !== 'restart') throw error;
      done = true;
      return error;
    }
  };
  return state;
}

test('Soldier admission latches after crossing the box, then shows Ultimate at 2.5 seconds', () => {
  const state = run();
  assert.equal(state.step(), 'wait');
  state.inside = true;
  assert.equal(state.step(), 'wait');
  state.inside = false;
  state.seconds = 2.49;
  assert.equal(state.step(), 'wait');
  assert.equal(state.calls.length, 0);
  state.seconds = 2.5;
  assert.equal(state.step(), 'wait');
  assert.equal(state.step(), 'end');
  assert.deepEqual(state.calls, [['popup', 5750]]);
  assert(state.flags.has(1055420927));
});

test('death, map exit and admission loss restart without consuming the Ultimate lesson', () => {
  for (const interrupt of [
    state => { state.hp = 0; },
    state => { state.inMap = false; },
    state => { state.flags.delete(18002855); },
  ]) {
    const state = run({ inside: true });
    state.step(); state.step();
    interrupt(state);
    assert.equal(state.step(), 'restart');
    assert.equal(state.calls.length, 0);
    assert(!state.flags.has(1055420927));
    const retry = run({ inside: true, flags: new Set([18002855]), seconds: 2.5 });
    retry.step(); retry.step(); retry.step();
    assert.equal(retry.step(), 'end');
    assert(retry.flags.has(1055420927));
  }
});

test('defeat ends pending lesson and transformation waits for its active flag to clear', () => {
  const defeated = run({ inside: true });
  defeated.step(); defeated.step(); defeated.flags.add(18000850);
  assert.equal(defeated.step(), 'end');
  assert(!defeated.flags.has(1055420927));
  assert.equal(defeated.calls.length, 0);

  const transform = run({ inside: true, flags: new Set([18002855, 18002851]) });
  transform.step(); transform.step();
  transform.seconds = 2.5;
  assert.equal(transform.step(), 'wait');
  transform.flags.add(18002852);
  assert.equal(transform.step(), 'wait', 'phase two does not release the popup');
  assert.equal(transform.calls.length, 0);
  transform.flags.delete(18002851);
  assert.equal(transform.step(), 'end');
  assert.deepEqual(transform.calls, [['popup', 5750]]);
});

test('shown and guest states skip the lesson', () => {
  for (const overrides of [
    { flags: new Set([18002855, 1055420927]) },
    { host: false },
    { flags: new Set([18002855, 18000850]) },
  ]) {
    const state = run({ inside: true, seconds: 2.5, ...overrides });
    assert.equal(state.step(), 'end');
    assert.equal(state.calls.length, 0);
  }
});

test('death banner readiness is separate from full audio cleanup', () => {
  const boss = event(mapSource, 5750303);
  assert.match(boss, /WaitFor\(EventFlag\(1055425282\) \|\| ElapsedSeconds\(25\)\);/);
  assert(!boss.includes('WaitFor(EventFlag(1055425256) || ElapsedSeconds(25))'));

  const voice = event(mapSource, 5750312);
  for (const [selector, start, banner, tail, stop, total] of [
    [1055425214, 999800113, 10.5, 6.74, 999800213, 17.24],
    [1055425215, 999800114, 12, 1.12, 999800214, 13.12],
  ]) {
    const branch = voice.split(`else if (EventFlag(${selector})) {`)[1].split('\n    else if ')[0];
    assert(branch, `Missing death branch ${selector}`);
    const bannerWait = branch.indexOf(`WaitFor(ElapsedSeconds(${banner}));`);
    const bannerFlag = branch.indexOf('SetEventFlagID(1055425282, ON)');
    const tailWait = branch.indexOf(`WaitFor(ElapsedSeconds(${tail}));`);
    const stopSound = branch.indexOf(`SoundType.Voice, ${stop}`);
    const cleanup = branch.indexOf('SetEventFlagID(1055425256, ON)');
    assert(branch.includes(`SoundType.Voice, ${start}`));
    assert(bannerWait >= 0 && bannerWait < bannerFlag && bannerFlag < tailWait && tailWait < stopSound && stopSound < cleanup);
    assert(Math.abs(banner + tail - total) < 1e-9);
  }
});

test('kill event keeps other rewards without Ultimate charge; deflection HKS retains it', () => {
  const kill = event(commonSource, 5750018);
  assert(!kill.includes('101990'));
  for (const effect of [571, 1626353, 1626200]) assert(kill.includes(`SetSpEffect(10000, ${effect})`));
  for (const sound of [450264, 2003000, 2006000, 2010000]) assert(kill.includes(`SoundType.SFX, ${sound}`));
  assert(kill.includes('IncrementEventValue(1055422000, 6, 64)'));
  assert.match(hksSource, /-- SACRED Deflection[\s\S]*?act\(AddSpEffect, 101990\)/);
});
