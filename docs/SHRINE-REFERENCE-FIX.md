# Shrine reference fix for encounter testing

Applied 2026-09-10. Gameplay acceptance remains Pending.

In `event/src/m18_00_00_00.emevd.dcx.js`:

- Event 5750303 now targets Hadeon (18002354) in its victory sound and boss-defeat/banner calls. Rick's own event is unchanged.
- Events 5750300 and 5750303 now target the second collision asset (18002379) for five asset enable-state/SFX operations previously aimed at region 18002349. All encounter/teleport region checks retain 18002349.
- Testing resets, reward timing, ritual and Nemesis logic are unchanged. No map was edited; the author is positioning AEG099_002_9001 in Smithbox.

The chosen collision model is labelled "Long piece of invisible collision" by Smithbox. Golden Barrier effect 7505236 was included in the earlier SFX recovery. Its rendering and alignment still need observation.

## Verification and handoff

Used the repository's `build_events` workflow against an isolated scratch workspace. All eight other shipped event outputs compared equivalent. The shrine's full decoded comparison matched an expected object with exactly seven first-argument changes across events 5750300 and 5750303. All 60 event records, their order, remaining arguments, parameter bindings, layers, rest behavior and file metadata were preserved except those edits.

Backed up and synchronized 11 source/runtime paths across repo, external Script workspace, Vortex and live game. Eight physical writes preserved three shared-file relationships. All destination hashes were verified; scoped event status reports 19 matches. No automatic propagation script, map save or game launch occurred.

- Source SHA-256: `14264275b41cd78cc7e627a605abae2b299f976a17e8e3ec3ac1f43690faf30c`
- Runtime SHA-256: `dfed241dd8ae1f59676ffc3876295a7e35ccb58fe135b69b820305fd3e57078d`
- Local backups, plan and receipt: `.codex-temp/shrine-reference-fix-20260910-000611/`
- Build receipt: `workspace/.codex-temp/event-builds/1789023978409838700/receipt.json` beneath that directory.

## Author's test

1. In Smithbox, position asset AEG099_002_9001, entity 18002379, across the desired entrance. Save and propagate the map through the normal map workflow.
2. Reload the shrine event in any open script editor before saving, so an older buffer cannot restore the previous IDs. Restart/reload the game as needed to load the updated event.
3. Before Hadeon's defeat, verify golden VFX placement and physical blocking separately, including both barriers if applicable.
4. Defeat Hadeon. Verify the victory presentation, removal of blocking collision and golden VFX, crystal visibility and delayed reward. Check that Rick's encounter still behaves normally if not already defeated.
5. Report observations against ER-008 and ER-029 with the runtime hash above. Completion after reload is not an acceptance criterion for this limited fix: the existing testing reset block deliberately remains active. Persistent defeat/reward behavior is a separate outstanding change.

## Subsequent persistence change

The 2026-09-10 [persistence and hardcore handoff](NEMESIS-PERSISTENCE.md) supersedes
this reference-only stage: testing resets have now been removed with completed-state
cleanup, interrupted reward reconciliation and crystal-triggered hardcore behavior.
The entity/reference fixes documented here are retained.
