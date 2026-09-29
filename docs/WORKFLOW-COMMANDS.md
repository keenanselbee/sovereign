# Current Sovereign commands

Implemented during the 2026-09-10/11 workflow goal. Main runtime files are in
`mod/`, authoring sources in `src/`, and separate
texture payloads in `packages/textures/mod/`. The nine external propagation
entry points perform validated sync only. Build and deployment are separate
requested operations. Historical switching and rollback evidence remains in
[the checkpoint](history/2026-09-11-workflow-preparation.md).

Choose the guide for the current task:

- [Inspect and choose a baseline](workflows/inspect-and-baselines.md)
- [Build candidates and review handoffs](workflows/build-and-handoffs.md)
- [Deployment and synchronization](workflows/deployment-and-sync.md)
- [Checks and recovery](workflows/checks-and-recovery.md)

The headings below preserve links to the former sections.

## Inspect and choose a baseline

See [inspection and baseline commands](workflows/inspect-and-baselines.md#inspect-and-choose-a-baseline).

## Build isolated candidates

See [candidate build commands](workflows/build-and-handoffs.md#build-isolated-candidates).

## Review a repo/editor handoff

See [handoff commands](workflows/build-and-handoffs.md#review-a-repoeditor-handoff).

## Stage, select and deploy through VDB

See [deployment commands](workflows/deployment-and-sync.md#stage-select-and-deploy-through-vdb)
and [prepared-package finalization](workflows/deployment-and-sync.md#prepared-package-deployment-and-resume).

## Verification

See [sync and deployment verification](workflows/deployment-and-sync.md#verification).

## One-time layout migration

See [layout recovery](workflows/checks-and-recovery.md#one-time-layout-migration).

## Checks

See [tooling checks](workflows/checks-and-recovery.md#checks).

## Opening follow-up sources

See [source ownership and build instructions](workflows/checks-and-recovery.md#opening-follow-up-sources).

## Catalogued source recipes

- `src/recipes/hadeon-teleport/Program.cs` (Hadeon destination integration; see its README)
- `src/recipes/hadeon-teleport/destinations.json` (Hadeon destination integration; see its README)
- `src/recipes/hadeon-teleport/generate-selector.py` (Hadeon destination integration; see its README)
- `src/recipes/hadeon-teleport/regions.json` (Hadeon destination integration; see its README)

- `src/recipes/memory-of-grace/params.patch.json` (Memory of Grace rune retention)
- `src/recipes/memory-of-grace/text.patch.json` (matching English item text)

- `src/recipes/starting-flask-pouch/whistle-zero-quantity.patch.json` (zero-count bottom-pouch whistle trial; see its README)

- `src/recipes/starting-flask-pouch/new-classes.patch.json` (Idus/Heavy starting pouch defaults; see its README)
- `src/recipes/cave-message/Program.cs` (remove the Cave of Knowledge ground inscription; see its README)

- `src/recipes/deflect-critical/Program.cs` (seven-second charges and critical-only bonus; see its README)

`tools/sovereign.py check` reads this page to confirm that these exact
`sourceRecipes` paths are documented. Their procedures are in
[build and handoffs](workflows/build-and-handoffs.md) and
[opening follow-up sources](workflows/checks-and-recovery.md#opening-follow-up-sources).

- `src/text/opening-dialogue-tutorial/item_dlc02.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu_dlc01.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu_dlc02.msgbnd.dcx.patch.json`
- `src/recipes/hadeon-followup/Program.cs`
- `src/textures/tutorial/build.ps1`
- `src/audio/hadeon/build.py` (monologue and subtitle cue bank; see its README)
- `src/recipes/hadeon-audio-test/Program.cs` (guarded additional-bank field patch)
- `src/recipes/hadeon-dialogue/Program.cs` (guarded TalkParam/map additions)
- `src/recipes/hadeon-dialogue/menu.msgbnd.dcx.patch.json`
- `src/recipes/hadeon-dialogue/menu_dlc01.msgbnd.dcx.patch.json`
- `src/recipes/hadeon-dialogue/menu_dlc02.msgbnd.dcx.patch.json`

The [Hadeon subtitle recipe](../src/recipes/hadeon-dialogue/README.md) describes
these coordinated parameter, map, text and talk-source additions.

- `src/recipes/hadeon-ai-params/Program.cs` (Hadeon private logic selection; see its README)
- `src/ai/hadeon/build.ps1` (private native AI binder; see its README)

- `src/ai/hadeon/build-battle.ps1` (private periodic battle goal; see its README)
- `src/recipes/hadeon-periodic-ai/Program.cs` (private battle assignment)
- `src/recipes/hadeon-aid-refinement/Program.cs` (40-to-20-second rescue cooldowns)
- `src/recipes/hadeon-dialogue-proxy/Program.cs` (persistent death sound carrier)

- `src/recipes/hadeon-vortex-animation/Program.cs` (private c2500 timelines; see its README)
- `src/recipes/hadeon-vortex-animation/build-graph.py` (native attack graph routes)
- `src/recipes/hadeon-lighting-progression/generate.mjs` (96 death-tier/HP ignition calls; see its README)
- `src/recipes/hadeon-vortex-markers/Program.cs` (neutral animation markers)
- `src/recipes/hadeon-vortex-map/Program.cs` (guarded arena eligibility spheres)
