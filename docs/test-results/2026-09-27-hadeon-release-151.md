Hadeon combat release trial 1.5.1
================================

The author reports that Hadeon tracks the player while remaining idle after the
monologue. Moving behind him triggers a different action, and hitting him can
trigger attacks. The installed goal 250010 has nonzero frontal attack weights;
those observations do not establish which action is selected or executed.

Event 5750311 now requests one animation reset immediately before its existing
AI enable/replan at the first monologue's timed cue. The living-player/boss,
valid-room, intro-gate and not-already-in-combat guards remain. The reset also
requires ongoing voice and no current hit: early-hit engagement, voice
cancellation and repeat entrances retain their existing actions. Voice and
subtitle playback flags are not cleared by the reset. The cue remains 13 seconds
from actual voice start, after the existing 0.7-second minimum appearance delay
and 12-metre entrance voice gate. This is an unconfirmed repair candidate, not a
demonstrated engine diagnosis.

The [subtitle restoration](2026-09-27-hadeon-subtitles-restored.md) is included.
Phase effects 14600/14601 are observed, not applied or replaced. Temporary flags
1055425250/1055425251 mirror them every 0.1 seconds in event 5750313. Flag
1055425252 records the reset request; it does not confirm animation execution.
The existing bounded aid log adds `bossPhase14600`, `bossPhase14601` and
`bossAnimReset`. Native combat remains a separate field. Probe state clears after
departure/defeat; each entrance clears the reset marker. The movement capture's
older filename/build label remains unchanged; the new fields identify this trial.

Verification and recovery
-------------------------

Allocation scan `.codex-temp/hadeon-release-151/allocation-scan/flag-scan.json`
checked 598 event files and 194 regulation members without collisions. Native
candidate `.codex-temp/event-builds/1790553027511658600/receipt.json` changes only
events 5750311 and 5750313, preserving metadata and the other eight runtime event
files. Map SHA-256:
`c0f89772ff1fd4e94bd0351f6da42986597357d0c114cacc59a6c1bab068063e`.
The coordinated player qualification reuses unchanged native binders with new
HKS guards: `.codex-temp/player-qualifications/1790552990825862500/receipt.json`.
This validates asset consistency, not HKS execution in game.

All 29 encounter/load-reset source tests pass, including reset order/once,
early-hit and cancellation bypass, already-started combat, repeat entrance,
room/death guards and independent phase probes/cleanup. HKS changes are only the
three diagnostic field reads; they add no gameplay action or state mutation.
Preparation, version consistency, scoped whitespace and local-link checks pass.
Guarded editor handoffs completed: events
`.sovereign/handoffs/151c5474d22e47aca222d69eb1c04441/receipt.json` (two files),
HKS `.sovereign/handoffs/6effe08d259349eab3a55ac359dd403c/receipt.json` (one file).
The earlier three-file subtitle handoff remains valid and is included unchanged.

Recovery copies and accepted map receipt are under
`.sovereign/backups/hadeon-release-151/`. To remove this trial, remove the guarded
reset/marker in 5750311, restore 5750313's prior native-combat-only observer and
remove the three HKS log fields, then rebuild/sync/deploy under a new version.
Do not restore whole backups over later edits. Subtitles and the earlier load
reset can remain independently.

For acceptance, quit/load while alive to exercise the existing fresh-encounter
test. Stay in the room and do not hit Hadeon through the cue. Verify he approaches
and attacks, the voice continues, and subtitles appear. On a separate entrance,
hit him early and verify his reaction/action is not reset at the later cue. If
he remains idle, retain the session aid log and inspect phase/reset/native-combat
fields. Subtitle distance behavior and native AI engagement remain unverified.

Deployment status
-----------------

Deployment completed. Prepared receipt
`.vdb/prepared/c99d337733a44369a88e1fa808e5ea32/receipt.json` contains 75 files;
only the Hadeon map event, c0000 diagnostic script and restored talk binder differ
from 1.5.0. Finalization
`.vdb/finalizations/793cd5e5468b4fce8bd0ad680239120a/receipt.json` completed
request `dc33b7f2-16f2-45fd-ae36-f3285a263ae1`, build
`fd1f0c8ed0c2a82f32f65d5d`. Profile `SkC-QjDMc` is enabled, deployed and
verified with no differences. Independent hashes of all 75 live files match;
receipt `.sovereign/backups/hadeon-release-151/live-verification.json`.
In-game engagement and subtitle acceptance remain pending.
