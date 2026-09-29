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
const destinationManifest = JSON.parse(readFileSync(new URL('../../src/recipes/hadeon-teleport/destinations.json', import.meta.url), 'utf8'));
const geometry = JSON.parse(readFileSync(new URL('../../src/recipes/hadeon-teleport/regions.json', import.meta.url), 'utf8'));
const destinations = destinationManifest.destinations;
const landingIds = destinations.map(row => row.entityId);
const clearanceIds = destinations.map(row => row.clearanceId);
const eligibilityIds = destinations.map(row => row.eligibilityId);
const landingPoints = destinations.map(row => {
  const { Position: p } = geometry.clearanceRegions.find(region => region.destinationId === row.entityId);
  return [p.X, p.Y, p.Z];
});
const landingPairs = destinationManifest.pairRegions.map(row => [landingIds.indexOf(row.low), landingIds.indexOf(row.high)]);
const pairRegionIds = destinationManifest.pairRegions.map(row => row.regionId);
const distanceSquared = (p, q) => p.reduce((sum, value, i) => sum + (value - q[i]) ** 2, 0);
const horizontalSquared = (p, q) => (p[0] - q[0]) ** 2 + (p[2] - q[2]) ** 2;

function eligibleLandings(position, bossPosition, vortex = false) {
  return landingPoints.map((point, i) => ({ id: landingIds[i], point, distance: horizontalSquared(point, position) }))
    .filter(({ point }) => distanceSquared(point, position) > 2.5 ** 2
      && (!bossPosition || distanceSquared(point, bossPosition) > 2.5 ** 2)
      && (!vortex || distanceSquared(point, position) <= 8 ** 2))
    .sort((a, b) => a.distance - b.distance || a.id - b.id);
}

// Find real positions that select every marker, including the tightly paired ones.
// Expected selection uses direct distance arithmetic, independently of event labels.
const witnessPositions = landingPoints.map((point, index) => {
  for (const radius of [2.55, 3, 4, 6, 7.9]) {
    for (let degree = 0; degree < 360; degree++) {
      const angle = degree * Math.PI / 180;
      const position = [point[0] + Math.sin(angle) * radius, point[1], point[2] + Math.cos(angle) * radius];
      if (eligibleLandings(position)[0]?.id === landingIds[index]) return position;
    }
  }
  throw new Error(`No nearby selection witness for destination ${landingIds[index]}`);
});


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
    flags: new Set([1055422933, 1055420930]), areas: new Set([`${player}:${arena}`]),
    effects: new Map(), grants: [], warpWorks: true, regionOverrides: new Map(),
    distance: 31, elapsed: Infinity, inMap: true, damage: false, aiCombat: false,
    aiEnabled: false, aiCommand: -1, commands: [], replans: 0, resets: [],
    actions: [], warps: [], sounds: [], comparisonChecks: 0, position: [40, -75.94449, 145],
  };
  const stop = kind => { throw { control: kind }; };
  const api = {
    ON: true, OFF: false, Disabled: 0, Enabled: 1, SoundType: { SFX: 0 },
    TargetEntityType: { Character: 0, Area: 1 }, BossBGMState: { Stop1: 0, Start: 1 },
    PlayerIsInOwnWorld: () => state.host,
    DisableNetworkSync() {}, NoOp() {},
    EventFlag: id => state.flags.has(id),
    AnyBatchEventFlags: (first, last) => {
      for (let id = first; id <= last; id++) if (state.flags.has(id)) return true;
      return false;
    },
    SetEventFlagID: (id, on) => {
      return on ? state.flags.add(id) : state.flags.delete(id);
    },
    BatchSetEventFlags: (first, last, on) => {
      for (let id = first; id <= last; id++) api.SetEventFlagID(id, on);
    },
    RandomlySetEventFlagInRange: first => state.flags.add(first),
    CharacterHPValue: id => state.hp.get(id),
    ElapsedSeconds: seconds => state.elapsed >= seconds,
    RandomElapsedSeconds: (min, max) => { assert.equal(min, 15); assert.equal(max, 30); return state.elapsed >= (state.periodicDelay ?? min); },
    PlayerInMap: () => state.inMap,
    CharacterDead: id => state.hp.get(id) <= 0,
    EntityInRadiusOfEntity: (id, target, radius, mode) => {
      assert.equal(id, player); assert.equal(target, boss); assert.equal(mode, 1);
      return state.distance <= radius;
    },
    EnableCharacterAI: () => { state.aiEnabled = true; state.actions.push('enable-ai'); },
    RequestCharacterAICommand: (id, command, slot) => {
      assert.equal(id, boss); assert.equal(slot, 0);
      state.aiCommand = command; state.commands.push(command);
      state.actions.push(`command-${command}`);
    },
    RequestCharacterAIReplan: id => {
      assert.equal(id, boss); assert.equal(state.aiEnabled, true);
      state.replans++; state.actions.push('replan');
    },
    RequestCharacterAnimationReset: (id, mode) => {
      assert.equal(id, boss); assert.equal(mode, api.Disabled);
      state.resets.push([id, mode]); state.actions.push('animation-reset');
    },
    HasDamageType: (id, slot, damageType) => {
      assert.equal(id, boss); assert.equal(slot, 0);
      assert.equal(damageType, api.DamageType.Unspecified);
      return state.damage;
    },
    DamageType: { Unspecified: 0 },
    CharacterAIState: (id, aiState) => {
      assert.equal(id, boss); assert.equal(aiState, api.AIStateType.Combat);
      return state.aiCombat;
    },
    AIStateType: { Combat: 0 },
    HPRatio: id => state.hp.get(id) / 1000,
    InArea: (id, region) => {
      if (id === player && state.regionOverrides.has(region)) return state.regionOverrides.get(region);
      const eligibility = eligibilityIds.indexOf(region);
      if (id === player && eligibility !== -1) {
        return distanceSquared(landingPoints[eligibility], state.position) <= 8 ** 2;
      }
      if (id === player || id === boss) {
        const position = id === player ? state.position : (state.bossPosition ?? [0, 0, 0]);
        const clearance = clearanceIds.indexOf(region);
        if (clearance !== -1) return distanceSquared(landingPoints[clearance], position) <= 2.5 ** 2;
        const pair = pairRegionIds.indexOf(region);
        if (pair !== -1) {
          state.comparisonChecks++;
          const [a, b] = landingPairs[pair];
          return horizontalSquared(landingPoints[a], position) <= horizontalSquared(landingPoints[b], position);
        }
      }
      return state.areas.has(`${id}:${region}`);
    },
    CharacterHasSpEffect: (id, effect) => state.effects.has(`${id}:${effect}`),
    SetSpEffect: (id, effect) => {
      state.effects.set(`${id}:${effect}`, true);
      state.grants.push([id, effect]);
      if (effect === 1627100) state.hp.set(id, Math.max(0, state.hp.get(id) - 50));
      if (effect === 1627101) state.hp.set(id, Math.max(0, state.hp.get(id) - 100));
    },
    ClearSpEffect: (id, effect) => state.effects.delete(`${id}:${effect}`),
    RotateCharacter: (id, target, animation, wait) => {
      assert.equal(id, boss); assert.equal(target, player);
      assert.equal(animation, -1); assert.equal(wait, false); state.actions.push('face-player');
    },
    WarpCharacterAndCopyFloor: (id, kind, destination, dummy, floor) => {
      state.warps.push(destination); state.actions.push('warp');
      assert.equal(id, boss); assert.equal(destination, floor);
      if (state.warpWorks) state.areas.delete(`${id}:${fall}`);
    },
    EndIf: condition => { if (condition) stop('end'); },
    GotoIf: (label, condition) => {
      assert.equal(condition, false, `Unexpected ${label} branch in combat-start prelude`);
    },
    EndEvent: () => stop('end'), RestartEvent: () => stop('restart'),
    RestartIf: condition => { if (condition) stop('restart'); },
    $InitializeEvent() {},
    PlaySE: (entity, type, sound) => state.sounds.push([entity, sound]),
    SpawnOneshotSFX() {},
    DisplayBossHealthBar() {}, SetBossBGM() {},
  };
  const context = vm.createContext(api);
  function event(id, values = []) {
    const start = source.indexOf(`$Event(${id},`);
    assert.notEqual(start, -1);
    const signature = /function\(([^)]*)\) \{/.exec(source.slice(start));
    const names = signature[1].split(',').map(name => name.trim()).filter(Boolean);
    assert.equal(names.length, values.length);
    let body = source.slice(start + signature.index + signature[0].length, source.indexOf('\n});', start));
    body = names.map((name, i) => `const ${name} = ${JSON.stringify(values[i])};`).join('\n') + body;
    if (id === 5750303) {
      // The prelude owns admission and early-hit release; labels after L0 own retreat.
      body = body.slice(0, body.indexOf('\nL0:'))
        .replace(/GotoIf\((L\d),/g, "GotoIf('$1',");
    }
    if (id === 5750311) {
      const engage = body.indexOf('\nL19:');
      const cleanup = body.indexOf('\nL20:');
      assert(engage > 0 && cleanup > engage, 'entrance native long-jump targets exist');
      const head = suspend(body.slice(0, engage), 'GotoIf', args => {
        const label = args.split(',')[0].trim();
        return ['L19', 'L20'].includes(label)
          ? `if (${args.slice(args.indexOf(',') + 1)}) break ${label === 'L19' ? 'engage' : 'cleanup'}`
          : `GotoIf(${args})`;
      }).replace(/Goto\(L19\)/g, 'break engage').replace(/Goto\(L20\)/g, 'break cleanup');
      body = 'cleanup: { engage: {' + head + '}\n' + body.slice(engage + 5, cleanup)
        + '}\n' + body.slice(cleanup + 5);
    }
    if (id === 5750304) {
      // Explicit native label lets the compiler skip the expanded arena selector.
      // JavaScript's existing if/else already performs the same home-path branch.
      body = body.replace(/\nL19:/g, '');
    }
    if (id === 5750430) {
      const retry = body.indexOf('\nL19:');
      const reset = body.indexOf('\nL20:');
      const head = suspend(body.slice(0, retry), 'GotoIf', args => {
        const label = args.split(',')[0].trim();
        return ['L19', 'L20'].includes(label)
          ? `if (${args.slice(args.indexOf(',') + 1)}) break ${label === 'L19' ? 'retry' : 'reset'}`
          : `GotoIf(${args})`;
      }).replace(/Goto\(L19\)/g, 'break retry').replace(/Goto\(L20\)/g, 'break reset');
      body = 'reset: { retry: {' + head + '}\n' + body.slice(retry + 5, reset)
        + '}\n' + body.slice(reset + 5);
    }
    if (id === 5750311 || id === 5750304 || id === 5750430 || id === 5750432) {
      body = body.replace(/\/\/ BEGIN HADEON (?:NEAREST|VORTEX) SELECTOR[^]*?\/\/ END HADEON (?:NEAREST|VORTEX) SELECTOR/g,
        block => {
          const labels = [...block.matchAll(/\bL(\d+):/g)].map(match => Number(match[1]));
          const final = labels.at(-1);
          let selection = block.slice(0, block.indexOf(`L${final}:`) + `L${final}:`.length);
          selection = selection.replace(/GotoIf\(L(\d+), (.*)\);/g, 'if ($2) break choice$1;')
            .replace(new RegExp(`Goto\\(L${final}\\);`, 'g'), 'break selected;')
            .replace(/Goto\(L(\d+)\);/g, 'break choice$1;');
          for (const label of labels.slice(0, -1)) {
            const finish = selection.indexOf(`L${label}:`);
            selection = `choice${label}: {` + selection.slice(0, finish)
              + '}\n' + selection.slice(finish);
          }
          selection = selection.replace(/L\d+:/g, '');
          return 'selected: {' + selection + '}' + block.slice(block.indexOf(`L${final}:`) + `L${final}:`.length);
        });
    }
    body = suspend(body, 'WaitFor', expression => `yield (() => (${expression}))`);
    body = suspend(body, 'WaitFixedTimeSeconds', seconds => `yield (${seconds})`);
    body = suspend(body, 'WaitFixedTimeFrames', frames => `yield (${frames})`);
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
  assert.equal(e.count(1626916), 2); // 75% and 50% both refresh Thorn Ward.
  assert.equal(e.count(1626976), 1);
  assert.equal(e.count(1627101), 1);
  assert.equal(e.state.hp.get(boss), 100);
  worker.advance(); assert.equal(e.count(1627101), 1); assert.equal(e.count(1626916), 2);
});

test('first combat attempt has no Thorn Ward or 25% shriek damage', () => {
  const e = encounter(); e.state.flags.delete(1055420930); e.state.hp.set(boss, 200);
  e.event(5750306).advance();
  assert.equal(e.count(1626916), 0);
  assert.equal(e.count(1626976), 0);
  assert.equal(e.count(1627101), 0);
  assert.equal(e.state.hp.get(boss), 200);
});

test('full-health player receives Thorn Ward without a scripted heal', () => {
  const e = encounter(); e.state.hp.set(player, 1000); e.state.hp.set(boss, 750);
  const worker = e.event(5750306); worker.advance();
  e.state.hp.set(player, 100); worker.advance();
  assert.equal(e.count(1626916), 1); assert.equal(e.state.flags.has(1055422930), true);
  assert.equal(e.state.hp.get(player), 100);
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

test('presence stops on exit; only confirmed death clears milestones', () => {
  const e = encounter(); e.state.flags.add(1055422930);
  const worker = e.event(5750305); worker.advance(1);
  assert.equal(e.state.effects.has(`${player}:1627102`), true);
  e.state.areas.clear(); worker.advance();
  assert.equal(e.state.effects.has(`${player}:1627102`), false);
  assert.equal(e.state.flags.has(1055422930), true);
  e.state.hp.set(player, 0); worker.advance();
  assert.equal(e.state.flags.has(1055422930), true);
  e.state.flags.add(1055425042); worker.advance();
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

test('admitted aid refresh survives permission expiry and stops on exit', () => {
  const e = encounter();
  const admission = e.event(5750403);
  const refresh = e.event(5750405);
  admission.step(); // Wait for eligible entry.
  admission.step(); // Three continuous seconds before admission.
  assert.equal(e.state.flags.has(1055425233), false);
  admission.step(); // Warm-up has elapsed.
  assert.equal(e.state.flags.has(1055425233), true);
  assert.equal(e.count(1627130), 1);

  refresh.step(); // Wait for admission, then grant once.
  refresh.step();
  const beforeExpiry = e.count(1627130);
  e.state.effects.delete(`${player}:1627130`); // Native timed effect expires.
  refresh.step(); // Finish the short refresh interval.
  refresh.step(); // Re-enter without another three-second warm-up.
  refresh.step();
  assert.equal(e.count(1627130), beforeExpiry + 1);
  assert.equal(e.state.effects.has(`${player}:1627130`), true);

  e.state.areas.clear();
  admission.step(); // Departure revokes admission.
  assert.equal(e.state.flags.has(1055425233), false);
  refresh.advance();
  assert.equal(e.state.effects.has(`${player}:1627130`), false);
  assert.equal(e.count(1627130), beforeExpiry + 1);
});

test('first speech waits for proximity and releases once after 12.2 seconds of voice', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.elapsed = 0; e.state.distance = 31;
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  const opening = e.event(5750311); opening.step(); opening.step();
  assert.equal(e.state.aiCommand, 1900);
  assert.equal(e.state.flags.has(1055422933), false);
  assert.equal(e.state.flags.has(1055425216), false);
  opening.step(); e.state.elapsed = 0.7; opening.step();
  assert.equal(e.state.flags.has(1055425216), false, 'Speech still waits for 30m');
  e.state.distance = 30.01; opening.step();
  assert.equal(e.state.flags.has(1055425216), false);
  e.state.distance = 30; opening.step();
  assert.equal(e.state.flags.has(1055425216), true);
  e.state.flags.add(1055422946); e.state.flags.add(1055425200);
  e.state.elapsed = 0; opening.step(); e.state.elapsed = 12.19; opening.step();
  assert.equal(e.state.warps.length, 0); assert.equal(e.state.aiCommand, 1900);
  e.state.elapsed = 12.2; opening.step();
  assert.equal(e.state.warps.length, 1);
  assert.equal(e.state.aiCommand, -1);
  assert.equal(e.state.resets.length, 0);
  assert.equal(e.state.replans, 1);
  assert.equal(e.state.flags.has(1055422933), true);
  assert.equal(e.state.flags.has(1055422946), true, 'Voice remains active after handoff');
  assert(e.state.actions.indexOf('warp') < e.state.actions.indexOf('command--1'));
  assert(e.state.actions.indexOf('command--1') < e.state.actions.indexOf('replan'));
  opening.advance(); assert.equal(e.state.warps.length, 1);
});

test('hit during speech releases the waiting goal and never teleports later', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.distance = 12;
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  const opening = e.event(5750311); opening.advance(4);
  e.state.flags.add(1055422946); e.state.flags.add(1055425200);
  opening.step(); e.state.damage = true; opening.step();
  assert.equal(e.state.aiCommand, -1); assert.equal(e.state.replans, 1);
  assert.equal(e.state.flags.has(1055422933), true);
  assert.equal(e.state.flags.has(1055422946), true);
  e.state.damage = false; e.state.elapsed = 20; opening.advance();
  assert.equal(e.state.warps.length, 0); assert.equal(e.state.resets.length, 0);
});

test('first-voice cancellation releases combat without relocation through the long skip', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.distance = 12;
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  const opening = e.event(5750311); opening.advance(4);
  e.state.flags.add(1055422946); e.state.flags.add(1055425200);
  e.state.elapsed = 0; opening.step();
  e.state.flags.delete(1055422946); opening.step();
  assert.deepEqual(e.state.warps, []);
  assert.equal(e.state.aiCommand, -1); assert.equal(e.state.replans, 1);
  assert(e.state.flags.has(1055422933));
});

test('invalidated or already released first entrance skips relocation and duplicate combat handoff', () => {
  for (const reason of ['admission-revoked', 'already-released', 'player-dead', 'boss-dead', 'defeated', 'attempt-ended']) {
    const e = encounter(); e.state.flags.delete(1055422933);
    e.state.flags.add(1055422947); e.state.distance = 12;
    e.state.aiEnabled = true; e.state.aiCommand = 1900;
    const opening = e.event(5750311); opening.advance(4);
    e.state.flags.add(1055422946); e.state.flags.add(1055425200);
    e.state.elapsed = 0; opening.step();
    if (reason === 'admission-revoked') e.state.flags.delete(1055422947);
    if (reason === 'already-released') e.state.flags.add(1055422933);
    if (reason === 'player-dead') e.state.hp.set(player, 0);
    if (reason === 'boss-dead') e.state.hp.set(boss, 0);
    if (reason === 'defeated') e.state.flags.add(1055420915);
    if (reason === 'attempt-ended') e.state.flags.add(1055425042);
    e.state.elapsed = 12.2; opening.step();
    assert.deepEqual(e.state.warps, [], reason);
    assert.equal(e.state.replans, 0, reason);
    assert.equal(e.state.aiCommand, 1900, reason);
  }
});

test('repeat entrance waits one second, warps once, then releases before proximity-gated voice', () => {
  const e = encounter();
  e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.flags.add(1055420935);
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  e.state.elapsed = 0;
  const opening = e.event(5750311);
  opening.step(); opening.step();
  assert.equal(e.state.aiCommand, 1900);
  assert.equal(e.state.warps.length, 0);
  e.state.elapsed = 0.99; opening.step();
  assert.equal(e.state.aiCommand, 1900);
  e.state.elapsed = 1; opening.step();
  assert.equal(e.state.aiCommand, -1); assert.equal(e.state.replans, 1);
  assert.equal(e.state.flags.has(1055422933), true);
  assert.equal(e.state.warps.length, 1);
  assert(e.state.actions.indexOf('warp') < e.state.actions.indexOf('command--1'));
  opening.step();
  assert.equal(e.state.flags.has(1055425217), false, 'No repeat pool request outside radius');
  e.state.distance = 12;
  opening.step();
  assert.equal(e.state.flags.has(1055425217), true, 'Shared gate admits every repeat variant');
  assert.equal(e.state.resets.length, 0);
});

test('a hit in the repeat wait engages immediately without delayed relocation', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.flags.add(1055420935);
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  e.state.elapsed = 0; e.state.distance = 12;
  const opening = e.event(5750311); opening.step(); opening.step();
  e.state.damage = true; opening.step();
  assert.equal(e.state.warps.length, 0);
  assert.equal(e.state.aiCommand, -1);
  assert.equal(e.state.flags.has(1055422933), true);
  assert.equal(e.state.flags.has(1055425217), false);
  e.state.damage = false; e.state.elapsed = 0.69; opening.step();
  assert.equal(e.state.flags.has(1055425217), false, 'Early-hit speech still settles');
  e.state.elapsed = 0.7; opening.advance(3);
  assert.equal(e.state.flags.has(1055425217), true);
  e.state.elapsed = 10; opening.advance();
  assert.equal(e.state.warps.length, 0);
});

test('repeat relocation selects each of the eighteen nearest clear points', () => {
  const reached = new Set();
  for (const [index, position] of witnessPositions.entries()) {
    const e = encounter(); e.state.flags.delete(1055422933);
    e.state.flags.add(1055422947); e.state.flags.add(1055420935);
    e.state.aiEnabled = true; e.state.aiCommand = 1900;
    e.state.position = position; e.state.elapsed = 0;
    const opening = e.event(5750311); opening.step(); opening.step();
    e.state.elapsed = 1; opening.step();
    assert.deepEqual(e.state.warps, [landingIds[index]]);
    assert(e.state.comparisonChecks <= landingIds.length - 1, 'selection compares at most seventeen rivals');
    assert(e.state.actions.indexOf('warp') < e.state.actions.indexOf('face-player'));
    reached.add(e.state.warps[0]);
    assert.equal(e.state.aiCommand, -1);
    opening.advance(); assert.equal(e.state.warps.length, 1);
  }
  assert.equal(reached.size, 18);
});

test('first-monologue and periodic relocation can each reach all eighteen destinations', () => {
  for (const [index, position] of witnessPositions.entries()) {
    const first = encounter(); first.state.position = position; first.state.distance = 12;
    first.state.flags.delete(1055422933); first.state.flags.add(1055422947);
    first.state.aiEnabled = true; first.state.aiCommand = 1900;
    const opening = first.event(5750311); opening.advance();
    first.state.flags.add(1055422946); first.state.flags.add(1055425200);
    opening.advance();
    assert.deepEqual(first.state.warps, [landingIds[index]]);
    assert(first.state.comparisonChecks <= landingIds.length - 1);
    assert(first.state.actions.indexOf('warp') < first.state.actions.indexOf('face-player'));
    assert.equal(first.state.aiCommand, -1);

    const periodic = encounter(); periodic.state.position = position; periodic.state.aiEnabled = true;
    periodic.state.areas.add(`${boss}:${arena}`);
    const worker = periodic.event(5750430); worker.advance();
    periodic.state.flags.add(1055425254); worker.step();
    assert.deepEqual(periodic.state.warps, [landingIds[index]]);
    assert(periodic.state.comparisonChecks <= landingIds.length - 1);
    assert(periodic.state.actions.indexOf('warp') < periodic.state.actions.indexOf('face-player'));
  }
});

test('raised landing uses horizontal nearest selection but three-dimensional clearance', () => {
  const index = landingIds.indexOf(18002384);
  const raised = landingPoints[index];
  assert(raised[1] > landingPoints[0][1] + 0.6, 'the authored raised point is retained');
  for (const height of [2.4, 2.6]) {
    const e = encounter(); e.state.position = [raised[0], raised[1] + height, raised[2]];
    e.state.areas.add(`${boss}:${fall}`); e.event(5750304).advance();
    assert.equal(e.state.warps[0] === landingIds[index], height > 2.5,
      'clearance uses vertical separation, while the point directly below remains nearest');
  }
  let witness;
  for (const other of landingPoints) {
    if (other === raised) continue;
    for (const fraction of [0.499, 0.4999, 0.5001, 0.501]) {
      const position = [raised[0] + (other[0] - raised[0]) * fraction, other[1],
        raised[2] + (other[2] - raised[2]) * fraction];
      const horizontal = eligibleLandings(position);
      const spatial = [...horizontal].sort((a, b) => distanceSquared(a.point, position) - distanceSquared(b.point, position));
      if (horizontal[0]?.id !== spatial[0]?.id) witness = { position, expected: horizontal[0].id };
    }
  }
  assert(witness, 'raised-marker boundary must distinguish horizontal from spatial nearest');
  const e = encounter(); e.state.position = witness.position;
  e.state.areas.add(`${boss}:${fall}`); e.event(5750304).advance();
  assert.deepEqual(e.state.warps, [witness.expected]);
});

test('repeat wait cancels on departure or death without warping or engaging', () => {
  for (const exit of ['room', 'fall', 'map', 'death', 'boss-death']) {
    const e = encounter(); e.state.flags.delete(1055422933);
    e.state.flags.add(1055422947); e.state.flags.add(1055420935);
    e.state.aiEnabled = true; e.state.aiCommand = 1900; e.state.elapsed = 0;
    const opening = e.event(5750311); opening.step(); opening.step();
    if (exit === 'room') e.state.areas.clear();
    if (exit === 'fall') e.state.areas.add(`${player}:${fall}`);
    if (exit === 'map') e.state.inMap = false;
    if (exit === 'death') e.state.hp.set(player, 0);
    if (exit === 'boss-death') e.state.hp.set(boss, 0);
    e.state.elapsed = 1; opening.step();
    assert.equal(e.state.warps.length, 0, exit);
    assert.equal(e.state.replans, 0, exit);
    assert.equal(e.state.flags.has(1055422933), false, exit);
  }
});

test('leaving or dying before the cue cannot release or teleport from dialogue', () => {
  for (const exit of ['room', 'fall', 'map', 'death', 'boss-death']) {
    const e = encounter(); e.state.flags.delete(1055422933);
    e.state.flags.add(1055422947); e.state.distance = 12;
    e.state.aiEnabled = true; e.state.aiCommand = 1900;
    const opening = e.event(5750311);
    opening.step(); opening.step(); opening.step(); opening.step();
    assert(e.state.flags.has(1055425216));
    e.state.flags.add(1055422946); e.state.flags.add(1055425200);
    e.state.elapsed = 0; opening.step();
    if (exit === 'room') e.state.areas.clear();
    if (exit === 'fall') e.state.areas.add(`${player}:${fall}`);
    if (exit === 'map') e.state.inMap = false;
    if (exit === 'death') e.state.hp.set(player, 0);
    if (exit === 'boss-death') e.state.hp.set(boss, 0);
    e.state.elapsed = 12.2; opening.step();
    assert.equal(e.state.aiCommand, 1900, exit);
    assert.equal(e.state.replans, 0, exit);
    assert.equal(e.state.resets.length, 0, exit);
    assert.equal(e.state.warps.length, 0, exit);
  }
});





test('leaving the room or dying while waiting for proximity never queues entrance speech', () => {
  for (const exit of ['room', 'fall', 'map', 'death']) {
    const e = encounter(); e.state.flags.delete(1055422933);
    e.state.flags.add(1055422947); e.state.aiEnabled = true; e.state.aiCommand = 1900;
    const opening = e.event(5750311);
    opening.step(); opening.step(); opening.step();
    if (exit === 'room') e.state.areas.clear();
    if (exit === 'fall') e.state.areas.add(`${player}:${fall}`);
    if (exit === 'map') e.state.inMap = false;
    if (exit === 'death') e.state.hp.set(player, 0);
    opening.step();
    assert.equal(e.state.flags.has(1055425216), false, exit);
    assert.equal(e.state.flags.has(1055425217), false, exit);
    if (exit !== 'death') assert.equal(e.state.flags.has(1055422948), true, exit);
  }
});

test('AI Combat state alone cannot bypass the first-speech wait', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.aiCombat = true;
  e.state.aiEnabled = true; e.state.aiCommand = 1900;
  const combat = e.event(5750303); combat.step(); combat.step();
  assert.equal(e.state.flags.has(1055422933), false);
  assert.equal(e.state.aiCommand, 1900);
  e.event(5750311).advance(3);
  assert.equal(e.state.flags.has(1055422933), false);
  assert.equal(e.state.aiCommand, 1900);
});

test('early prevoice hit releases the hold while speech remains queued', () => {
  const e = encounter(); e.state.flags.delete(1055422933);
  e.state.flags.add(1055422947); e.state.aiEnabled = true; e.state.aiCommand = 1900;
  e.state.aiCombat = true; e.state.distance = 12;
  const combat = e.event(5750303); combat.step();
  assert.equal(e.state.aiCommand, 1900);
  e.state.damage = true; combat.step();
  assert.equal(e.state.aiCommand, -1);
  assert.equal(e.state.replans, 1);
  assert.equal(e.state.flags.has(1055422933), true);
  const opening = e.event(5750311); opening.advance(4);
  assert.equal(e.state.flags.has(1055425216), true);
  e.state.flags.add(1055422946); e.state.flags.add(1055425200);
  opening.step(); opening.step();
  assert.equal(e.state.warps.length, 0);
  assert.equal(e.state.flags.has(1055422946), true);
  assert.equal(e.state.replans, 1, 'The cue does not release a second time');
});

test('retreat parks running AI on its self target and defeat clears its command', () => {
  const combat = source.slice(source.indexOf('$Event(5750303,'), source.indexOf('$Event(5750304,'));
  assert(!combat.includes('DisableCharacterAI(18002354)'));
  assert(combat.includes('RequestCharacterAICommand(18002354, 1901, 0);'));
  assert(combat.includes('RequestCharacterAICommand(18002354, -1, 0);'));
});

test('combat diagnosis is removed while the new handoff replans', () => {
  assert(!source.includes('$Event(5750313,'));
  assert(!source.includes('$InitializeEvent(0, 5750313)'));
  const body = source.slice(source.indexOf('$Event(5750311,'), source.indexOf('$Event(5750312,'));
  assert(body.includes('RequestCharacterAIReplan'));
  const hks = readFileSync(new URL('../../mod/action/script/c0000.hks', import.meta.url), 'utf8');
  for (const key of ['aiCombat', 'bossPhase14600', 'bossPhase14601', 'bossAnimReset']) {
    assert(!hks.includes('ModDiagnosticField("' + key + '"'));
  }
});


test('fall recovery chooses all eighteen nearest clear destinations and charges once', () => {
  const reached = new Set();
  for (const [index, position] of witnessPositions.entries()) {
    const e = encounter(); e.state.position = position;
    e.state.areas.add(`${boss}:${fall}`);
    const worker = e.event(5750304); worker.advance();
    assert.deepEqual(e.state.warps, [landingIds[index]]);
    assert(e.state.comparisonChecks <= landingIds.length - 1, 'selection compares at most seventeen rivals');
    reached.add(landingIds[index]);
    assert.equal(e.count(1627100), 1); assert.equal(e.state.hp.get(boss), 950);
    assert(e.state.actions.includes('face-player'));
    worker.advance(); assert.equal(e.count(1627100), 1); assert.equal(e.state.warps.length, 1);
  }
  assert.equal(reached.size, 18);
});

test('opening and fall share one generated selection block per event', () => {
  const blocks = [...source.matchAll(/\/\/ BEGIN HADEON NEAREST SELECTOR[^]*?\/\/ END HADEON NEAREST SELECTOR/g)]
    .map(m => m[0].split('\n').map(line => line.trim())
      .filter(line => line && !line.startsWith('//')).join('\n'));
  assert.equal(blocks.length, 3, 'fall, shared first/repeat entrance, periodic');
  assert.equal(blocks[0], blocks[1]);
  assert.equal([...source.matchAll(/\/\/ BEGIN HADEON VORTEX SELECTOR/g)].length, 1);
  for (const block of blocks) {
    assert.equal([...block.matchAll(/WarpCharacterAndCopyFloor/g)].length, 18);
    assert(!/WaitFor|WaitFixedTime|RestartEvent/.test(block), 'selection only runs at a relocation request');
  }
});

test('fall recovery outside the arena uses the home point without a damage pulse', () => {
  const e = encounter(); e.state.areas.delete(`${player}:${arena}`);
  e.state.areas.add(`${boss}:${fall}`); e.event(5750304).advance();
  assert.deepEqual(e.state.warps, [18002366]); assert.equal(e.count(1627100), 0);
});


test('quantized three-way comparison cycle still selects a clear fall destination', () => {
  const e = encounter(); e.state.position = [30.207703, -75.94449, 132.22641];
  for (const region of clearanceIds.slice(8)) e.state.regionOverrides.set(region, true);
  e.state.regionOverrides.set(18005906, false);
  e.state.regionOverrides.set(18005924, true);
  e.state.regionOverrides.set(18005928, false);
  e.state.areas.add(`${boss}:${fall}`); e.event(5750304).advance();
  assert.equal(e.state.warps.length, 1);
  assert([18002369, 18002371, 18002382].includes(e.state.warps[0]));
  assert.equal(e.count(1627100), 1);
});

test('spawn sets the first-speech hold before enabling Hadeon', () => {
  const start = source.indexOf('$Event(5750302,');
  const body = source.slice(start, source.indexOf('\n});', start));
  assert(!body.includes('DisableCharacterAI(18002354)'));
  const hold = body.indexOf('RequestCharacterAICommand(18002354, 1900, 0);');
  const reveal = body.indexOf('EnableCharacter(18002354);');
  const enable = body.indexOf('EnableCharacterAI(18002354);');
  const admission = body.indexOf('SetEventFlagID(1055422947, ON)');
  assert(hold >= 0 && hold < reveal && enable > reveal && admission > enable);
});


test('periodic teleport waits for cooldown and natural AI acknowledgement', () => {
  for (const delay of [15, 30]) {
    const e = encounter(); e.state.aiEnabled = true;
    e.state.areas.add(`${boss}:${arena}`); e.state.elapsed = 0; e.state.periodicDelay = delay;
    const worker = e.event(5750430); worker.advance();
    e.state.elapsed = delay - .01; worker.advance();
    assert(!e.state.flags.has(1055425253));
    e.state.elapsed = delay; worker.advance();
    assert(e.state.flags.has(1055425253)); assert.equal(e.state.warps.length, 0);
    assert.equal(e.state.replans, 0, 'request never interrupts current AI');
    e.state.flags.add(1055425254); worker.step();
    assert.equal(e.state.warps.length, 1); assert.equal(e.state.replans, 1);
    assert(!e.state.flags.has(1055425253)); assert(!e.state.flags.has(1055425254));
  }
});

test('periodic pending request cancels on death or room exit', () => {
  for (const reason of ['death', 'boss-death', 'exit', 'boss-exit']) {
    const e = encounter(); e.state.aiEnabled = true; e.state.areas.add(`${boss}:${arena}`);
    const worker = e.event(5750430); worker.advance();
    assert(e.state.flags.has(1055425253));
    if (reason === 'death') e.state.hp.set(player, 0);
    if (reason === 'boss-death') e.state.hp.set(boss, 0);
    if (reason === 'exit') e.state.areas.delete(`${player}:${arena}`);
    if (reason === 'boss-exit') e.state.areas.delete(`${boss}:${arena}`);
    worker.step();
    assert.equal(e.state.warps.length, 0, reason); assert(!e.state.flags.has(1055425253), reason);
    assert.equal(e.state.replans, 0, reason);
  }
});

test('periodic request survives melee proximity and speech without another cooldown', () => {
  for (const speech of [1055422946, 1055422947]) {
    const e = encounter(); e.state.aiEnabled = true; e.state.areas.add(`${boss}:${arena}`); e.state.distance = 1;
    const worker = e.event(5750430); worker.advance();
    assert(e.state.flags.has(1055425253));
    e.state.flags.add(speech); e.state.elapsed = 0; worker.advance();
    assert(e.state.flags.has(1055425253)); assert.equal(e.state.warps.length, 0);
    // Simulate speech starting in the same frame as acknowledgment.
    e.state.flags.add(1055425254); worker.advance();
    assert(e.state.flags.has(1055425253)); assert(!e.state.flags.has(1055425254));
    assert.equal(e.state.warps.length, 0);
    e.state.flags.delete(speech); e.state.flags.add(1055425254); worker.step();
    assert.equal(e.state.warps.length, 1);
    assert(!e.state.flags.has(1055425253));
  }
});

test('periodic landing excludes points within 2.5 m of either participant', () => {
  for (const point of landingPoints) {
    const e = encounter(); e.state.aiEnabled = true; e.state.areas.add(`${boss}:${arena}`);
    e.state.position = [point[0], point[1], point[2] + 3]; e.state.bossPosition = point;
    const worker = e.event(5750430); worker.advance();
    e.state.flags.add(1055425254); worker.step();
    const eligible = eligibleLandings(e.state.position, point);
    assert.deepEqual(e.state.warps, [eligible[0].id]);
  }
});

test('unavailable landings retain the ready request and release AI for retry', () => {
  const e = encounter(); e.state.aiEnabled = true; e.state.areas.add(`${boss}:${arena}`);
  for (const region of clearanceIds) e.state.regionOverrides.set(region, true);
  const worker = e.event(5750430); worker.advance();
  e.state.flags.add(1055425254); e.state.elapsed = 0; worker.advance();
  assert.equal(e.state.warps.length, 0); assert.equal(e.state.replans, 1);
  assert(e.state.flags.has(1055425253)); assert(!e.state.flags.has(1055425254));
  e.state.regionOverrides.clear(); e.state.flags.add(1055425254); worker.step();
  assert.equal(e.state.warps.length, 1); assert(!e.state.flags.has(1055425253));
});


test('hidden death carrier initializes for clients as well as the host', () => {
  const start = source.indexOf('$Event(5750300,');
  const body = source.slice(start, source.indexOf('\n});', start));
  assert(body.indexOf('$InitializeEvent(0, 5750431)') < body.indexOf('if (PlayerIsInOwnWorld())'));
});

test('Vortex relocation restarts the periodic timer before a second warp', () => {
  const e = encounter(); e.state.aiEnabled = true;
  e.state.areas.add(`${boss}:${arena}`); e.state.elapsed = 0; e.state.periodicDelay = 15;
  const worker = e.event(5750430); worker.advance();
  e.state.elapsed = 10; e.state.flags.add(1055425259);
  worker.step();
  assert.equal(e.state.warps.length, 0);
  worker.step();
  assert(!e.state.flags.has(1055425259));
  assert(!e.state.flags.has(1055425253));
  e.state.elapsed = 0; worker.advance();
  e.state.elapsed = 14.99; worker.advance();
  assert(!e.state.flags.has(1055425253));
  e.state.elapsed = 15; worker.advance();
  assert(e.state.flags.has(1055425253));
});

test('first voice reposts the final phrase without restarting its subtitle timeline', () => {
  const e = encounter(); e.state.flags.add(1055425216); e.state.elapsed = 0;
  const worker = e.event(5750312); worker.advance();
  const phrase = e.event(5750433); phrase.advance();
  assert.deepEqual(e.state.sounds, [[boss, 999800001]]);
  e.state.elapsed = 13.09; phrase.step();
  assert.equal(e.state.sounds.length, 1);
  e.state.elapsed = 13.1; phrase.step();
  assert.deepEqual(e.state.sounds.at(-1), [boss, 999800003]);
  assert(e.state.flags.has(1055422946));
  assert(e.state.flags.has(1055425200));
  e.state.elapsed = 17.29; worker.step();
  assert(e.state.flags.has(1055422946));
  e.state.elapsed = 17.30; worker.step();
  assert(!e.state.flags.has(1055422946));
  assert.deepEqual(e.state.sounds.slice(-2), [[boss, 999800002], [boss, 999800004]]);
});

test('cancelled first voice cannot later post its final phrase', () => {
  for (const reason of ['retreat', 'player-death', 'boss-death', 'preemption', 'voice-off']) {
    const e = encounter(); e.state.flags.add(1055425216); e.state.elapsed = 0;
    const worker = e.event(5750312); worker.advance();
    const phrase = e.event(5750433); phrase.advance();
    if (reason === 'retreat') e.state.flags.add(1055422948);
    if (reason === 'player-death') e.state.hp.set(player, 0);
    if (reason === 'boss-death') e.state.hp.set(boss, 0);
    if (reason === 'preemption') e.state.flags.add(1055425221);
    if (reason === 'voice-off') e.state.flags.delete(1055422946);
    phrase.step(); worker.step();
    assert(!e.state.sounds.some(([, id]) => id === 999800003), reason);
    assert.deepEqual(e.state.sounds.slice(-2), [[boss, 999800002], [boss, 999800004]], reason);
  }
});

test('Vortex marker diagnostics observe independently and never request a teleport', () => {
  const e = encounter();
  const live = e.event(5750434, [1627600, 1055425280]);
  const cue = e.event(5750434, [1627601, 1055425281]);
  live.advance(); cue.advance();
  assert(!e.state.flags.has(1055425280)); assert(!e.state.flags.has(1055425281));
  e.state.effects.set(`${boss}:1627601`, true);
  cue.advance(); live.advance();
  assert(e.state.flags.has(1055425281)); assert(!e.state.flags.has(1055425280));
  e.state.effects.delete(`${boss}:1627601`);
  e.state.effects.set(`${boss}:1627600`, true);
  live.advance(); cue.advance();
  assert(e.state.flags.has(1055425280)); assert(e.state.flags.has(1055425281));
  e.state.effects.delete(`${boss}:1627600`);
  live.advance(); cue.advance();
  assert(e.state.flags.has(1055425280)); assert(e.state.flags.has(1055425281));
  assert(!e.state.flags.has(1055425258));
  assert.deepEqual(e.state.warps, []);
});

test('Vortex cue chooses the nearest eligible clear marker once without resetting combat', () => {
  for (const [index, position] of witnessPositions.entries()) {
    const e = encounter(); e.state.areas.add(`${boss}:${arena}`);
    e.state.position = position;
    e.state.flags.add(1055425258);
    e.state.effects.set(`${boss}:1627600`, true);
    const worker = e.event(5750432); worker.advance();
    assert(e.state.flags.has(1055425279), 'relocation worker reached its cue wait');
    assert.equal(e.state.warps.length, 0, 'must wait for the animation cue');
    e.state.effects.set(`${boss}:1627601`, true);
    const eligible = eligibleLandings(e.state.position, undefined, true);
    assert.equal(eligible[0]?.id, landingIds[index]);
    worker.advance();
    assert.deepEqual(e.state.warps, eligible.length ? [eligible[0].id] : []);
    assert(e.state.comparisonChecks <= landingIds.length - 1);
    assert(!e.state.flags.has(1055425258));
    assert(e.state.flags.has(1055425275), 'cue was observed');
    assert.equal(e.state.flags.has(1055425259), !!eligible.length);
    assert.equal(e.state.flags.has(1055425278), !!eligible.length, 'successful warp is sticky');
    assert.equal(e.state.flags.has(1055425277), !eligible.length, 'no eligible point is diagnosed');
    assert(!e.state.flags.has(1055425276));
    assert.equal(e.state.replans, 0); assert.equal(e.state.resets.length, 0);
    assert.equal(e.state.commands.length, 0);
    assert(e.state.actions.indexOf('warp') < e.state.actions.indexOf('face-player'));
    worker.advance(); assert(e.state.warps.length <= 1);
  }
});

test('Vortex rejects out-of-range, unsafe and cancelled attempts', () => {
  for (const reason of ['far', 'all-blocked', 'player-dead', 'boss-dead', 'player-exit', 'boss-exit', 'fall', 'no-live', 'no-roll']) {
    const e = encounter(); e.state.areas.add(`${boss}:${arena}`);
    e.state.position = [landingPoints[0][0] + 3, landingPoints[0][1], landingPoints[0][2]];
    e.state.flags.add(1055425258);
    e.state.effects.set(`${boss}:1627600`, true); e.state.effects.set(`${boss}:1627601`, true);
    if (reason === 'far') e.state.position = [0, -75.94449, 100];
    if (reason === 'all-blocked') for (const id of clearanceIds) e.state.regionOverrides.set(id, true);
    if (reason === 'player-dead') e.state.hp.set(player, 0);
    if (reason === 'boss-dead') e.state.hp.set(boss, 0);
    if (reason === 'player-exit') e.state.areas.delete(`${player}:${arena}`);
    if (reason === 'boss-exit') e.state.areas.delete(`${boss}:${arena}`);
    if (reason === 'fall') e.state.areas.add(`${player}:${fall}`);
    if (reason === 'no-live') e.state.effects.delete(`${boss}:1627600`);
    if (reason === 'no-roll') e.state.flags.delete(1055425258);
    e.event(5750432).advance();
    assert.equal(e.state.warps.length, 0, reason);
    assert(!e.state.flags.has(1055425259), reason);
    assert.equal(e.state.flags.has(1055425275), !['no-live', 'no-roll'].includes(reason), reason);
    assert.equal(e.state.flags.has(1055425276), ['player-dead', 'boss-dead', 'player-exit', 'boss-exit', 'fall'].includes(reason), reason);
    assert.equal(e.state.flags.has(1055425277), ['far', 'all-blocked'].includes(reason), reason);
    assert(!e.state.flags.has(1055425278), reason);
  }
});

test('Vortex diagnostic range admits the six-to-eight-metre shell but keeps 2.5-metre clearance', () => {
  for (const distance of [2.4, 6.5, 7.9, 8.1]) {
    const e = encounter(); e.state.areas.add(`${boss}:${arena}`);
    e.state.position = [landingPoints[7][0], landingPoints[7][1], landingPoints[7][2] - distance];
    e.state.flags.add(1055425258);
    e.state.effects.set(`${boss}:1627600`, true); e.state.effects.set(`${boss}:1627601`, true);
    e.event(5750432).advance();
    assert.equal(e.state.warps.length > 0, distance >= 2.5 && distance <= 8, `${distance} m`);
  }
});

test('Vortex does not land inside Hadeon\'s own 2.5-metre clearance', () => {
  const e = encounter(); e.state.areas.add(`${boss}:${arena}`);
  e.state.position = [landingPoints[7][0], landingPoints[7][1], landingPoints[7][2] - 3];
  e.state.bossPosition = landingPoints[7];
  e.state.flags.add(1055425258);
  e.state.effects.set(`${boss}:1627600`, true); e.state.effects.set(`${boss}:1627601`, true);
  e.event(5750432).advance();
  assert.deepEqual(e.state.warps, []);
  assert(e.state.flags.has(1055425277));
});
