// Compatibility entrypoint; browser implementation lives in Nexus Automation.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const config = process.env.NEXUS_AUTOMATION_ROOT ? null : JSON.parse((await fs.readFile(path.join(repo, 'nexus-automation.local.json'), 'utf8')).replace(/^\uFEFF/, ''));
export const sharedToolRoot = process.env.NEXUS_AUTOMATION_ROOT || config.toolRoot;
if (!path.isAbsolute(sharedToolRoot)) throw new Error('Nexus Automation toolRoot must be absolute');
const manifest = JSON.parse(await fs.readFile(path.join(sharedToolRoot, 'package.json'), 'utf8'));
if (manifest.name !== '@keenan/nexus-automation') throw new Error('Configured checkout is not Nexus Automation');
const contract = await import(pathToFileURL(path.join(sharedToolRoot, 'src/contracts/request.mjs')));
if (contract.protocolVersion !== 1) throw new Error('Unsupported Nexus Automation protocol');
const ui = await import(pathToFileURL(path.join(sharedToolRoot, 'src/browser/editor.mjs')));
export const { normalizeText, buildEditUrl, readDescriptions, fillDescriptions, clickSave, verifySaved } = ui;
const files = await import(pathToFileURL(path.join(sharedToolRoot, 'src/state/files.mjs')));
export const { assertSourceHashes } = files;
export function getDesiredFromBackup(backup) {
  if (!backup.previous) throw new Error('Backup JSON does not contain previous descriptions');
  return { shortDescription: backup.previous.shortDescription ?? '', fullDescription: backup.previous.fullDescription ?? '' };
}
export async function runRequest(request) {
  const { runDescription } = await import(pathToFileURL(path.join(sharedToolRoot, 'src/operations/descriptions.mjs')));
  return runDescription({ schemaVersion: 1, ...request }, { stateRoot: process.env.NEXUS_AUTOMATION_STATE_ROOT || request.sharedStateRoot || path.join(sharedToolRoot, '.local') });
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const requestIndex = process.argv.indexOf('--request');
  if (requestIndex < 0 || !process.argv[requestIndex + 1]) throw new Error('Missing --request');
  files.readJson(process.argv[requestIndex + 1]).then(runRequest).then(result => console.log(JSON.stringify(result))).catch(error => { console.error(error.message); process.exitCode = 1; });
}
