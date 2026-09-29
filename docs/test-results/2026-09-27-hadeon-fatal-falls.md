Hadeon fatal combat falls, 1.4.5
==============================

The author clarified that jumping off the bridge and dying during Hadeon's fight
must consume the attempt. Version 1.4.4 incorrectly required the player to die
inside the valid room and outside the fall region.

Event `5750420` now accepts either a valid arena position or below-arena region
`18002367` when actual player death occurs. Both admission and the following
frame's recheck use this rule. Combat flag `1055422933`, the current map, a living
Hadeon, the once-per-death latch and rescue exclusion remain required.

A fatal combat fall advances saved losses once, queues the player-death line and
unlocks another 20% aid for the next attempt, capped at 100%. It also disqualifies
the special no-loss victory reward. Merely entering the fall region, surviving,
being rescued or being teleported back does not count. Pre-combat falls and
unrelated deaths after disengagement remain excluded. Simultaneous Hadeon defeat
retains priority over counting a loss.

Verification
------------

The progression simulator covers both native death and delayed confirmation
outside the room, overlapping fall/excluded regions, one count per fall,
survived falls, rescue, pre-combat/disengaged/off-map deaths, simultaneous victory,
and loss of bonus eligibility. The existing progression and dialogue matrix also
passes. These are source simulations, not an in-game fall test.

Pre-edit source/runtime backups and hashes are in
`.sovereign/backups/hadeon-fatal-fall-145/`. No new flags, effects, recordings,
subtitle assets or item lots are needed.

Native candidate `.codex-temp/event-builds/1790542709712054100/receipt.json`
compiled successfully. Decoded comparison shows only event `5750420` changed;
the other 87 map events, event ordering, file metadata and eight other runtime
event files are preserved. Accepted map-event SHA-256:
`01ee2f55cc070307d5e51a8a2a397ffcea11fe75eb31171d43eb3368d39a26b8`.
Acceptance guards are in the backup folder's `acceptance.json`.

The existing eight encounter tests also passed, as did preparation checks,
version validation, whitespace and changed-document link checks. Editor sync uses
`.sovereign/handoffs/5793dc7c0cc94d129e74b3ad03997904/receipt.json` for the
source and compiled event together. Deployment verification follows below.

Deployment completed as 1.4.5. Prepared receipt
`.vdb/prepared/1405576001ce42f89d2f40d15b26d749/receipt.json` contains 75 files:
only `mod/event/m18_00_00_00.emevd.dcx` differs from 1.4.4, with all other 74
files preserved. Finalization receipt
`.vdb/finalizations/788f84f04377462f9b73325740007680/receipt.json`, request
`f44ccca7-59e2-41f1-8114-ccdbba8bbda4`, build `a277661b4c10cb8fff493df4`,
records the completed enabled/deployed profile. Independent live SHA-256 checks
matched all 75 prepared files. Evidence is in the backup folder's
`live-verification.json`. In-game bridge-fall acceptance remains pending.
