import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { buildEditUrl, readDescriptions, fillDescriptions, clickSave, verifySaved, assertSourceHashes, sharedToolRoot } from './update-nexus-description.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(sharedToolRoot, 'node_modules/playwright'));

test('source drift stops a save', async () => {
  const run = await fs.mkdtemp(path.join(root, '.codex-temp/description-test-'));
  try {
    const source = path.join(run, 'copy.txt');
    await fs.writeFile(source, 'approved');
    const request = { sourceHashes: { [source]: createHash('sha256').update('approved').digest('hex') } };
    await assertSourceHashes(request);
    await fs.writeFile(source, 'changed');
    await assert.rejects(assertSourceHashes(request), /source changed/);
  } finally { await fs.rm(run, { recursive: true }); }
});

test('local editor fixture: read, edit, save, reload verification and restore', async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const context = await browser.newContext();
    let stored = { short: 'Old summary', full: '[b]Old page[/b]' };
    let saves = 0;
    await context.exposeBinding('fixtureSave', (_source, short, full) => {
      stored = { short, full }; saves++;
    });
    await context.route('**/*', async route => {
      // Every request is intercepted: this test never contacts Nexus.
      const html = `<label>Short description<textarea id="short"></textarea></label>
        <label>Full description<textarea id="full"></textarea></label>
        <button onclick="fixtureSave(document.querySelector('#short').value,document.querySelector('#full').value)">Save</button>`;
      await route.fulfill({ contentType: 'text/html', body: html });
    });
    const page = await context.newPage();
    await page.addInitScript(() => { window.addEventListener('DOMContentLoaded', () => {
      document.querySelector('#short').value = sessionStorage.getItem('short') || 'Old summary';
      document.querySelector('#full').value = sessionStorage.getItem('full') || '[b]Old page[/b]';
      document.querySelector('button').addEventListener('click', () => {
        sessionStorage.setItem('short', document.querySelector('#short').value);
        sessionStorage.setItem('full', document.querySelector('#full').value);
      });
    }); });
    const target = 'https://www.nexusmods.com/games/eldenring/mods/201';
    assert.equal(buildEditUrl(target), target + '/edit/general');
    await page.goto(buildEditUrl(target));
    const previous = await readDescriptions(page, 5000);
    assert.equal(saves, 0);
    await fillDescriptions(page, 'New summary', '[b]New page[/b]', 5000);
    await clickSave(page, 5000);
    await verifySaved(page, target, 'New summary', '[b]New page[/b]', 5000);
    assert.equal(saves, 1);
    assert.equal(stored.full, '[b]New page[/b]');
    await fillDescriptions(page, previous.shortDescription, previous.fullDescription, 5000);
    await clickSave(page, 5000);
    await verifySaved(page, target, previous.shortDescription, previous.fullDescription, 5000);
    assert.equal(saves, 2);
    assert.deepEqual(stored, { short: 'Old summary', full: '[b]Old page[/b]' });
  } finally { await browser.close(); }
});
