import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '../../..');
const sourcePath = path.join(root, 'src/events/m18_00_00_00.emevd.dcx.js');
const orderPath = path.join(import.meta.dirname, 'ignition-order.json');
let source = fs.readFileSync(sourcePath, 'utf8');
const original = [...source.matchAll(/\$InitializeEvent\((\d+), 5750401, (10554251\d\d), ([\d.]+)\);/g)];

if (!fs.existsSync(orderPath)) {
    assert.equal(original.length, 96, 'Capture the original 96 ignition delays before replacing the initializers');
    const order = original.map((match) => ({ slot: Number(match[1]), flag: Number(match[2]), delay: Number(match[3]) }))
        .sort((a, b) => a.delay - b.delay);
    assert.equal(new Set(order.map(({ delay }) => delay)).size, 96);
    fs.writeFileSync(orderPath, `${JSON.stringify(order.map(({ slot }) => slot), null, 2)}\n`);
}

const order = JSON.parse(fs.readFileSync(orderPath, 'utf8'));
assert.equal(order.length, 96);
assert.equal(new Set(order).size, 96);
assert(order.every((slot) => Number.isInteger(slot) && slot >= 0 && slot < 96));
const ranks = new Map(order.map((slot, rank) => [slot, rank]));
const newline = source.includes('\r\n') ? '\r\n' : '\n';
source = source.replace(/^[ \t]*\$InitializeEvent\(\d+, 5750407, [^;]+\);(?:\r?\n)?/gm, '');

// floor(96 * (b + (1 - b) * (1 - h))), b = .075 * min(losses, 10).
// Rank r ignites when count >= r + 1, hence h <= (95 - r) / (96 * (1 - b)).
function threshold(rank, losses) {
    return Math.min(1, (95 - rank) / (96 * (1 - .075 * losses)))
        .toFixed(9).replace(/0+$/, '').replace(/\.$/, '') || '0';
}

const authored = /\$InitializeEvent\((\d+), 5750401, (10554251\d\d), ([\d., ]+)\);/g;
assert.equal([...source.matchAll(authored)].length, 96, 'Expected 96 ignition initializer calls');
source = source.replace(authored, (_, slotText, flagText) => {
    const slot = Number(slotText);
    assert.equal(Number(flagText), 1055425100 + slot);
    const rank = ranks.get(slot);
    const baselineTierFlag = 1055425262 + Math.min(11, Math.ceil((rank + 1) / 7.2));
    const lower = Array.from({ length: 6 }, (_, losses) => threshold(rank, losses));
    const upper = Array.from({ length: 5 }, (_, index) => threshold(rank, index + 6));
    return `$InitializeEvent(${slot}, 5750401, ${flagText}, ${baselineTierFlag}, ${lower.join(', ')});`
        + `${newline}    $InitializeEvent(${slot}, 5750407, ${flagText}, ${baselineTierFlag}, ${upper.join(', ')});`;
});
fs.writeFileSync(sourcePath, source);
console.log('Authored 96 ignition calls with 11 death-tier HP thresholds in the original shuffled order.');
