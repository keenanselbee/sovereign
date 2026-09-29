import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import test from 'node:test';

const source = fs.readFileSync('src/events/m18_00_00_00.emevd.dcx.js', 'utf8');
// Arena HP/death lighting belongs to test-hadeon-lighting-progression.mjs.
// Current speech/aid/retreat behavior belongs to test-hadeon.mjs and
// test-hadeon-progression.mjs. This harness executes only hallway events.
test('Sovereign event flags use engine-supported storage blocks', () => {
    for (const match of source.matchAll(/105542\d{4}/g)) {
        assert(![1, 3, 6].includes(Math.floor(Number(match[0]) / 1000) % 10),
            `Invalid Sovereign flag allocation ${match[0]}`);
    }
});

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

function world({ flags = [] } = {}) {
    const state = { assets: new Set(), areas: new Set(), flags: new Set(flags), time: 0, events: [] };
    let active;
    const context = vm.createContext({
        EventFlag: id => state.flags.has(id),
        InArea: (_, id) => state.areas.has(id),
        DisableAsset: id => state.assets.delete(id),
        EnableAsset: id => state.assets.add(id),
        ElapsedSeconds: seconds => state.time - active.waitStart >= seconds - 1e-8,
        $InitializeEvent: (_, id) => add(id),
        EndIf: condition => { if (condition) throw { end: true }; },
        EndEvent: () => { throw { end: true }; },
        RestartIf: condition => { if (condition) throw { restart: true }; },
        RestartEvent: () => { throw { restart: true }; },
    });
    function add(id) {
        const match = source.match(new RegExp(`\\$Event\\(${id}, Restart, function\\(\\) \\{([\\s\\S]*?)\\n\\}\\);`));
        assert(match, `Missing hallway event ${id}`);
        const code = suspend(match[1], 'WaitFor', value => `yield { condition: () => (${value}) }`);
        const fn = vm.runInContext(`(function*() { while (true) {
            try { ${code} return; }
            catch (error) { if (error.restart) continue; if (error.end) return; throw error; }
        } })`, context);
        state.events.push({ id, iterator: fn(), wait: null, waitStart: 0, done: false });
    }
    function step(event) {
        active = event;
        for (let i = 0; i < 200; i++) {
            if (event.done || (event.wait && !event.wait.condition())) return;
            const next = event.iterator.next();
            event.done = next.done;
            event.wait = next.value;
            event.waitStart = state.time;
            if (event.done) return;
        }
        throw new Error(`Busy hallway loop ${event.id}`);
    }
    for (let id = 5750320; id <= 5750331; id++) add(id);
    state.advance = seconds => {
        const target = state.time + seconds;
        while (state.time < target - 1e-8) {
            state.time = Math.round((state.time + .01) * 100) / 100;
            state.events.forEach(step);
        }
    };
    return state;
}

test('125 hallway pairs preserve delays, reentry, cancellation and saved-state visibility', () => {
let w;
// Hallway pairs preserve one physical fixture while automatic model SFX owns light.
const hallBlocks=[...source.matchAll(/\$Event\(57503(?:2\d|3[01]), Restart, function\(\) \{([\s\S]*?)\n\}\);/g)];
const pairMatches=hallBlocks.flatMap(m=>[...m[1].matchAll(/DisableAsset\((18009\d+)\);\s+EnableAsset\((18006\d+)\);/g)]);
const pairs=new Map(pairMatches.map(m=>[+m[1],+m[2]]));assert.equal(pairs.size,125);
assert.equal(new Set(pairs.values()).size,125);
for(const m of hallBlocks)assert(!m[1].includes('AssetfollowingSFX'));
function checkPairs(w){assert.equal(w.assets.size,125);for(const [lit,off] of pairs)assert.notEqual(w.assets.has(lit),w.assets.has(off),'Exactly one visible per pair');}
function litCount(w){return [...pairs.keys()].filter(id=>w.assets.has(id)).length;}
w=world();w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
const regions=[...new Set(hallBlocks.flatMap(m=>[...m[1].matchAll(/InArea\(10000, (\d+)\)/g)].map(x=>+x[1])))];
assert.equal(regions.length,12);
w.areas.add(18002355);w.advance(1.4);assert.equal(litCount(w),0);w.advance(.2);assert(litCount(w)>0);
w.areas.delete(18002355);w.advance(.5);w.areas.add(18002355);w.advance(.1);assert(litCount(w)>0);
w.areas.delete(18002355);w.advance(1.1);assert.equal(litCount(w),0);
for(const region of regions){w.areas.add(region);w.advance(1.7);checkPairs(w);assert(litCount(w)>0);w.areas.delete(region);w.advance(.5);checkPairs(w);assert(litCount(w)>0);w.areas.add(region);w.advance(.1);checkPairs(w);assert(litCount(w)>0);w.areas.delete(region);w.advance(1.1);checkPairs(w);assert.equal(litCount(w),0);}
w.areas.add(regions[1]);w.advance(.2);w.areas.clear();w.advance(.5);w.flags.add(1055420915);w.advance(1.1);checkPairs(w);assert.equal(litCount(w),125);
w.flags.add(1055420918);w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
w=world();w.advance(.1);
w.areas.add(18002355);w.advance(.2);w.areas.clear();w.advance(2);checkPairs(w);assert.equal(litCount(w),0);
w=world();w.areas.add(18002355);w.advance(.2);assert.equal(litCount(w),0);
w.advance(1.4);assert(litCount(w)>0);w.areas.clear();w.advance(.5);
w.areas.add(18002355);w.advance(.1);assert(litCount(w)>0);
w.areas.clear();w.advance(1.1);assert.equal(litCount(w),0);
w.areas.add(18002355);w.advance(1.4);assert.equal(litCount(w),0);
w.advance(.2);assert(litCount(w)>0);
w.flags.add(1055420915);w.advance(.1);checkPairs(w);assert.equal(litCount(w),125);
w.flags.add(1055420918);w.advance(.1);checkPairs(w);assert.equal(litCount(w),0);
for(const flags of [[1055420915],[1055420918],[1055420915,1055420918]]){w=world({flags});w.advance(.1);checkPairs(w);assert.equal(litCount(w),flags.includes(1055420918)?0:125);}
console.log('125 hallway pairs: every region, delayed cancellation, victory, crystal and saved-state visibility passed.');

});
