import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync('src/events/m18_00_00_00.emevd.dcx.js', 'utf8');
const order = JSON.parse(fs.readFileSync('src/recipes/hadeon-lighting-progression/ignition-order.json', 'utf8'));
const calls = [...source.matchAll(/\$InitializeEvent\((\d+), 5750401, (10554251\d\d), ([\d., ]+)\);/g)];
const upperCalls = [...source.matchAll(/\$InitializeEvent\((\d+), 5750407, (10554251\d\d), ([\d., ]+)\);/g)];
assert.equal(calls.length, 96);
assert.equal(upperCalls.length, 96);
assert.equal(new Set(order).size, 96);
const initializers = calls.map((match) => [Number(match[1]), Number(match[2]), ...match[3].split(', ').map(Number)]);
const upperInitializers = upperCalls.map((match) => [Number(match[1]), Number(match[2]), ...match[3].split(', ').map(Number)]);
assert(initializers.every(([slot, flag, , ...thresholds]) => flag === 1055425100 + slot && thresholds.length === 6));
assert(upperInitializers.every(([slot, flag, , ...thresholds]) => flag === 1055425100 + slot && thresholds.length === 5));
for (const [slot, , baselineFlag, ...lower] of initializers) {
    const rank = order.indexOf(slot);
    const [, , upperBaselineFlag, ...upper] = upperInitializers[slot];
    assert.equal(baselineFlag, 1055425262 + Math.min(11, Math.ceil((rank + 1) / 7.2)));
    assert.equal(upperBaselineFlag, baselineFlag);
    const thresholds = [...lower, ...upper];
    for (let losses = 0; losses <= 10; losses++) {
        const expected = Math.min(1, (95 - rank) / (96 * (1 - .075 * losses)));
        assert(Math.abs(thresholds[losses] - expected) < 0.000000001);
    }
}

function suspend(code, name, replacement) {
    let start = 0;
    while ((start = code.indexOf(`${name}(`, start)) >= 0) {
        let end = start + name.length + 1;
        let depth = 1;
        while (depth) {
            if (code[end] === '(') depth++;
            if (code[end] === ')') depth--;
            end++;
        }
        const next = replacement(code.slice(start + name.length + 1, end - 1));
        code = code.slice(0, start) + next + code.slice(end);
        start += next.length;
    }
    return code;
}

function world({ losses = 0, bossHp = 1, visual = false, flags = [], encounterActive = true } = {}) {
    const state = { flags: new Set(flags), hp: 500, bossHp, inside: false, effects: new Set(),
        lights: new Set(), flames: new Set(), time: 0, events: [] };
    const saved = [1055420930, 1055420931, 1055420932, 1055420933, 1055420934,
        1055420952, 1055420953, 1055420954, 1055420955, 1055420956];
    for (const flag of saved.slice(0, losses)) state.flags.add(flag);
    if (encounterActive) state.flags.add(1055422933);
    let active;
    const api = {
        ON: true, OFF: false, L1: 'L1', L9: 'L9',
        EventFlag: (id) => state.flags.has(id),
        CharacterHPValue: (id) => id === 10000 ? state.hp : state.bossHp * 1000,
        CharacterHasSpEffect: (_, id) => state.effects.has(id),
        HPRatio: () => state.bossHp,
        PlayerIsInOwnWorld: () => true,
        InArea: () => state.inside,
        AnyBatchEventFlags: (a, b) => [...state.flags].some((flag) => flag >= a && flag <= b),
        SetEventFlagID: (id, on) => on ? state.flags.add(id) : state.flags.delete(id),
        BatchSetEventFlags: (a, b, on) => { for (let id = a; id <= b; id++) on ? state.flags.add(id) : state.flags.delete(id); },
        ElapsedSeconds: (seconds) => state.time - active.waitStart >= seconds - 1e-8,
        SpawnMapSFX: (id) => { assert(!state.lights.has(id), `Duplicate light ${id}`); state.lights.add(id); },
        DeleteMapSFX: (id) => state.lights.delete(id),
        CreateAssetfollowingSFX: (id) => { assert(!state.flames.has(id), `Duplicate flame ${id}`); state.flames.add(id); },
        DeleteAssetfollowingSFX: (id) => state.flames.delete(id),
        Goto: (label) => { throw { goto: label }; },
        GotoIf: (label, condition) => { if (condition) throw { goto: label }; },
        RestartEvent: () => { throw { goto: 'entry' }; },
        RestartIf: (condition) => { if (condition) throw { goto: 'entry' }; },
        EndEvent: () => { throw { end: true }; },
        EndIf: (condition) => { if (condition) throw { end: true }; },
    };
    const context = vm.createContext(api);
    function add(id, args = []) {
        const match = source.match(new RegExp(`\\$Event\\(${id}, Restart, function\\(([^)]*)\\) \\{([\\s\\S]*?)\\n\\}\\);`));
        assert(match, `Missing event ${id}`);
        let code = match[2];
        code = suspend(code, 'WaitFor', (value) => `yield { condition: () => (${value}) }`);
        code = suspend(code, 'WaitFixedTimeSeconds', (value) => `yield { seconds: ${value} }`);
        code = suspend(code, 'WaitFixedTimeFrames', (value) => `yield { seconds: (${value}) / 30 }`);
        code = `case 'entry':${code.replace(/^L(\d+):/gm, (_, label) => `case 'L${label}':`)}`;
        const fn = vm.runInContext(`(function*(${match[1]}) { let label = 'entry'; while (true) {
            try { switch (label) { ${code} } return; }
            catch (error) { if (error.goto) { label = error.goto; continue; } if (error.end) return; throw error; }
        } })`, context);
        state.events.push({ iterator: fn(...args), wait: null, waitStart: 0, done: false, id });
    }
    add(5750402);
    add(5750406);
    add(5750370);
    add(5750404);
    for (const [, ...args] of initializers) add(5750401, args);
    for (const [, ...args] of upperInitializers) add(5750407, args);
    if (visual) {
        const init = source.match(/\$Event\(0,[\s\S]*?\n\}\);/)[0];
        for (const match of init.matchAll(/\$InitializeEvent\(\d+, (575037[23]), ([^;]+)\);/g)) {
            add(Number(match[1]), match[2].split(', ').map(Number));
        }
    }
    function step(event) {
        active = event;
        for (let iterations = 0; iterations < 100; iterations++) {
            if (event.done) return;
            if (event.wait) {
                if (event.wait.condition && !event.wait.condition()) return;
                if (event.wait.until !== undefined && state.time + 1e-8 < event.wait.until) return;
                event.wait = null;
            }
            const next = event.iterator.next();
            if (next.done) { event.done = true; return; }
            event.waitStart = state.time;
            event.wait = next.value;
            if (event.wait.seconds !== undefined) event.wait.until = state.time + event.wait.seconds;
        }
        throw Error(`Busy event ${event.id}`);
    }
    state.advance = (seconds) => {
        const target = state.time + seconds;
        while (state.time < target - 1e-8) {
            state.time = Math.round((state.time + .01) * 100) / 100;
            state.events.forEach(step);
        }
    };
    state.lit = () => [...state.flags].filter((flag) => flag >= 1055425100 && flag <= 1055425195).length;
    return state;
}

const expectedCount = (losses, hp) => Math.floor(96 * (1 - (1 - .075 * losses) * hp) + 1e-9);
for (let losses = 0; losses <= 10; losses++) {
    const w = world({ losses });
    w.advance(.1);
    assert.equal(w.lit(), expectedCount(losses, 1), 'Death baseline is prepared outside the room');
    w.inside = true;
    w.advance(.1);
    assert.equal(w.lit(), expectedCount(losses, 1), `Full HP, ${losses} losses`);
    assert(w.flags.has(1055425262 + losses));
    assert.equal([...w.flags].filter((flag) => flag >= 1055425262 && flag <= 1055425272).length, 1);
    for (const hp of [.843, .617, .391, .157, .001]) {
        w.bossHp = hp;
        w.advance(.1);
        assert.equal(w.lit(), expectedCount(losses, hp), `${losses} losses, HP ${hp}`);
    }
    w.bossHp = 0;
    w.flags.add(1055420915);
    w.advance(.1);
    assert.equal(w.lit(), 96, `Defeat, ${losses} losses`);

    const boundary = losses <= 5
        ? initializers[order[84]][3 + losses]
        : upperInitializers[order[84]][3 + losses - 6];
    const atBoundary = world({ losses });
    atBoundary.inside = true;
    atBoundary.bossHp = boundary + .0001;
    atBoundary.advance(.1);
    assert.equal(atBoundary.lit(), expectedCount(losses, boundary + .0001));
    atBoundary.bossHp = boundary - .0001;
    atBoundary.advance(.1);
    assert.equal(atBoundary.lit(), expectedCount(losses, boundary - .0001));
}


// Time alone must never light another fixture, either before entry or in combat.
for (const losses of [0, 3, 10]) {
    const steady = world({ losses, visual: true, encounterActive: false });
    steady.advance(.2);
    const baseline = new Set(steady.lights);
    steady.advance(35);
    assert.deepEqual(steady.lights, baseline, 'No timed ignition outside the room');
    steady.inside = true;
    steady.flags.add(1055422933);
    steady.bossHp = .8;
    steady.advance(.2);
    assert.equal(steady.lights.size, expectedCount(losses, .8));
    const combatLights = new Set(steady.lights);
    const combatFlames = new Set(steady.flames);
    steady.advance(35);
    assert.deepEqual(steady.lights, combatLights, 'Constant HP preserves the exact lit set');
    assert.deepEqual(steady.flames, combatFlames, 'Constant HP preserves the exact flame set');
}

// Baseline is ready before room entry, even while Hadeon is unloaded.
for (const losses of [0, 2, 3, 5, 10]) {
    const early = world({ losses, bossHp: 0, encounterActive: false, visual: true,
        flags: [1055425273, 1055425195] });
    early.advance(.2);
    assert.equal(early.inside, false);
    assert.equal(early.lit(), expectedCount(losses, 1));
    assert.equal(early.lights.size, early.lit());
    assert(!early.flags.has(1055425273), 'The never-baseline sentinel must be cleared');
    early.bossHp = .8; early.advance(.1);
    assert.equal(early.lit(), expectedCount(losses, 1), 'Inactive HP cannot add lighting');
    early.inside = true; early.flags.add(1055422933); early.advance(.1);
    assert.equal(early.lit(), expectedCount(losses, .8));
}
// Reproduce a latched cancellation with readiness restored before continuation.
// This scheduling counterexample made all 96 fixtures ignite in 1.6.0.
for (const losses of [0, 2, 3, 5, 6, 10]) {
    const race = world({ losses, bossHp: .8 }); race.advance(.2);
    const expected = expectedCount(losses, .8);
    assert.equal(race.lit(), expected);
    const bank = losses <= 5 ? 5750401 : 5750407;
    const blocked = race.events.filter(e => e.id === bank && e.wait?.condition && !e.wait.condition());
    race.flags.delete(1055425274);
    const awakened = blocked.filter(e => e.wait.condition());
    assert.equal(awakened.length, 96 - expected);
    race.flags.add(1055425274);
    for (const event of awakened) {
        const next = event.iterator.next(); event.wait = next.value; event.done = next.done;
    }
    assert.equal(race.lit(), expected, 'Readiness recovery cannot bypass an HP threshold');
    race.advance(.1); assert.equal(race.lit(), expected);
}
// Same-map death recovery applies the next baseline before returning to the room.
{
    const retry = world({ losses: 2, encounterActive: false, visual: true });
    retry.advance(.2); assert.equal(retry.lit(), 14);
    retry.hp = 0; retry.advance(.6); retry.flags.add(1055420932);
    retry.hp = 500; retry.advance(.2);
    assert.equal(retry.inside, false); assert.equal(retry.lit(), 21);
    assert.equal(retry.lights.size, 21);
}

let w = world({ losses: 10, bossHp: 0, encounterActive: false });
w.inside = true;
w.advance(.1);
assert.equal(w.lit(), 72, 'Unloaded boss HP cannot light beyond the death baseline');
w.bossHp = 1;
w.flags.add(1055422947);
w.advance(.1);
assert.equal(w.lit(), 72);
w.bossHp = .617;
w.advance(.1);
assert.equal(w.lit(), expectedCount(10, .617));

w = world();
w.inside = true;
w.bossHp = .617;
w.advance(.1);
const beforeRescue = w.lit();
w.hp = 0;
w.bossHp = .391;
w.advance(.2);
assert.equal(w.lit(), beforeRescue, 'A zero-HP rescue pulse freezes the precise lit set');
w.hp = 500;
w.advance(.2);
assert.equal(w.lit(), expectedCount(0, .391), 'Rescue resumes HP-driven ignition without attempt reset');
assert(!w.flags.has(1055425042));

w = world({ visual: true });
w.inside = true;
w.advance(.1);
assert.equal(w.lit(), 0);
w.bossHp = .617;
w.advance(.1);
assert.equal(w.lit(), expectedCount(0, .617));
assert.equal(w.lights.size, w.lit());
assert([...w.lights].every((id) => (id - (id < 18004200 ? 18003900 : 18004200)) % 5 === 3));
const frozen = new Set([...w.flags].filter((flag) => flag >= 1055425100 && flag <= 1055425195));
w.hp = 0;
w.bossHp = 1;
w.advance(1);
assert(w.flags.has(1055425042));
assert.deepEqual(new Set([...w.flags].filter((flag) => flag >= 1055425100 && flag <= 1055425195)), frozen);
assert.equal(w.lights.size, frozen.size);
w.advance(5);
assert.equal(w.lit(), frozen.size);
w.inside = false;
w.hp = 500;
w.advance(.2);
assert.equal(w.lit(), 0);
assert.equal(w.lights.size, 0);
w.inside = true;
w.advance(.1);
assert.equal(w.lit(), 0);

w = world({ losses: 5 });
w.inside = true;
w.advance(.1);
assert.equal(w.lit(), 36);
w.hp = 0;
w.advance(.2);
w.hp = 500;
w.advance(.4);
assert.equal(w.lit(), 36);
assert(!w.flags.has(1055425042));
w.bossHp = .6;
w.advance(.1);
const beforeRetreat = w.lit();
w.inside = false;
w.bossHp = 1;
w.flags.add(1055420952); // A saved loss arriving mid-attempt cannot change the snapshot.
w.advance(.2);
assert.equal(w.lit(), beforeRetreat);
assert(w.flags.has(1055425267));
w.inside = true;
w.bossHp = .3;
w.advance(.1);
assert.equal(w.lit(), expectedCount(5, .3));

w = world({ visual: true });
w.inside = true;
w.bossHp = .5;
w.advance(.1);
w.flags.add(1055420915);
w.advance(.1);
assert.equal(w.lights.size, 96);
assert.equal(w.flames.size, 88);
w.flags.add(1055422945);
w.flags.add(1055420918);
w.advance(.1);
assert.equal(w.lights.size, 96);
w.advance(2);
assert.equal(w.lights.size, 96);
w.flags.delete(1055422945);
w.advance(2.5);
assert.equal(w.lights.size, 0);
assert.equal(w.flames.size, 0);
w = world({ visual: true, flags: [1055420915] });
w.advance(.1);
assert.equal(w.lights.size, 96);
w = world({ visual: true, flags: [1055420918] });
w.advance(.1);
assert.equal(w.lights.size, 0);

assert(!source.match(/\$Event\(5750404,[\s\S]*?\n\}\);/)[0].includes('ElapsedSeconds(30)'));
console.log('Hadeon lighting source simulation passed: all 11 loss tiers, HP boundaries, 100% fixtures, rescue, death freeze/reset, retreat, victory and crystal. Gameplay acceptance remains pending.');
