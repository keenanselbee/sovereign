Hadeon opening teleport 1.5.2
==============================

The first monologue now ends with a teleport to the nearest eligible existing
arena destination (18002368-18002373), followed by facing the player, enabling
AI, the health bar and music. The cue is 14.6 seconds from actual speech start,
approximately the end of "blade" in the current dry recording; the wet recording
continues through its reverb. The existing 0.7-second settling delay, 12-metre
entrance voice gate and restored subtitles remain. Repeat entrances retain their
normal immediate-combat behavior.

The cue requires a living host and boss, a valid arena position, an active intro
and voice, no hit, and combat not already started. An early hit starts combat
without the later teleport. Leaving the room or dying prevents cue-time teleport.
This opening teleport does not invoke fall recovery or apply its HP penalty.
The existing animation reset is part of teleport placement; the separate
combat-release reset/replan trial and combat-AI diagnostic event 5750313 are gone.
HKS combat/phase/reset log fields and their event flag readers/writers are removed.
Aid and movement diagnostics remain unchanged.

The [temporary load reset](2026-09-27-hadeon-load-reset-149.md) remains active:
ordinary loads reset encounter history, while a real death marks the next reload
to preserve attempt/aid progression. Reward receipts, crystal choices and pending
reward delivery remain protected. Fast travel also resets; this is still the
existing load heuristic rather than a title-screen-specific detector.


Implementation and verification
-------------------------------

The [map recipe](../../src/recipes/hadeon-teleport/README.md) adds fifteen pairwise
comparison boxes and six 2.5-metre clearance spheres at IDs 18005900-18005920.
It allocates no event flags. Direct event branches avoid DarkScript's condition
group limit. The selector checks each candidate against every eligible rival;
occupied landing points are excluded. A tiny consistent lower-ID tie preference
moves each bisector by at most 0.084 mm. If no candidate qualifies, normal combat
starts in place. All destinations, their floor targets and existing map content
are preserved.

Native map roundtrips and reverse-removal comparison pass. A separate rebuild
with the corrected decoded-argument ID scan reproduces the accepted map hash:
`c1023329e95fd6a6e9dba69ace3a6faf7993e1eb98bcef2ab2520923ed6641cd`.
40,401 grid positions, 7,497 triple-junction positions and exact midpoint/side
checks pass. Geometry uses the modeled box transform; actual game InArea and
floor/teleport behavior remain unverified. Manifest:
`.codex-temp/hadeon-teleport-implementation/map-verified/manifest.json`.

Event candidate `.codex-temp/event-builds/1790554259533455800/receipt.json`
changes only common event 50's obsolete diagnostic clear range and map events
5750300, 5750303 and 5750311; it removes 5750313. Comparing by event ID preserves
all other events, their order and file metadata. Seven other runtime event files
are byte-identical. All 26 encounter/load-reset source tests pass, covering
nearest clear placement, timed/early-hit paths, no teleport damage, departure,
death, repeat entrances and progression preservation. These source simulations
do not prove native AI engagement.

Coordinated HKS qualification reused unchanged native player assets with current
input guards: `.codex-temp/player-qualifications/1790554316373808700/receipt.json`.
HKS's only change removes the eight combat diagnostic fields and their orphaned
comment. No AI goal, audio bank, recording or subtitle asset changes are included.

Guarded editor handoffs completed: events
`.sovereign/handoffs/2eaf05f146ed4a139c4cc97cadb89f90/receipt.json` (four files),
HKS `.sovereign/handoffs/b6261a93b8f740418836cddd1060fa9d/receipt.json` (one file),
and map `.sovereign/handoffs/4fc6f5b98e5442af80a5662175763f47/receipt.json` (one file).
Preparation, version consistency, scoped whitespace and document links pass.

Backups are under `.sovereign/backups/hadeon-teleport/`. Revert this feature by
removing its selector and added regions, restoring the reviewed cue behavior,
then rebuilding/syncing under a new version. Do not restore whole files over
later edits. Load-reset testing can remain independently enabled.


In-game acceptance
------------------

Quit/load while alive, approach within speaking range and let the first monologue
finish without hitting Hadeon. Verify teleport after "blade", adequate clearance,
facing, continued subtitles and prompt attacks. Repeat from different positions.
Separately hit him early and verify no delayed teleport; leave the room during
the speech and verify no arrival outside it. Die once and verify the next attempt
keeps progression; quit/load while alive and verify the first encounter returns.
No claim that the previous idle-AI issue is resolved is made before these tests.

Deployment completed. Prepared receipt
`.vdb/prepared/9c29a345c3e143ebab185b27733e82ae/receipt.json` contains 75 files;
only the map, two event binaries and c0000 HKS differ from 1.5.1. Finalization
`.vdb/finalizations/4188ec2a4adc4722a31ec57d9f6d789f/receipt.json` completed
request `f77539ee-8c10-4cee-bc47-3fefc6d2c155`, build
`c90eaf69e192366e584f8e8d`. Profile `SkC-QjDMc` is enabled, deployed and verified
with no differences. Independent hashes of all 75 live files match; record
`.sovereign/backups/hadeon-teleport/live-verification.json`.
In-game acceptance remains pending.
