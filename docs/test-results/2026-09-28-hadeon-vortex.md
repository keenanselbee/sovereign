Hadeon Vortex and positional entrance voice
===========================================

Author-approved implementation, 2026-09-28. The user identified Ordovis's
Vortex as the desired spinning sword slam. Native candidates and automated
checks are not evidence of in-game acceptance. Deployment status is recorded
below after finalization.


Observed failure and follow-up
------------------------------

The author reported that Hadeon pauses in idle when attempting Vortex in 1.5.9.
Inspection found unsupported attack IDs 3080-3083 outside native HKS dispatch,
missing callback/name registration and incomplete graph event metadata. The
archive checks below did not establish callable attacks. The correction is
tracked in [the 1.6.0 follow-up](2026-09-28-hadeon-followup-160.md).


Behavior
--------

All entrance dialogue now admits the player at 30 m. The native subtitle
update and talk ranges remain 100 m after admission. The original first
recording is preserved; the build cuts its converted PCM at 13.100 s. Voice
999800001 plays the opening segment, and 999800003 posts the remaining
4.170833 s from Hadeon's current position. The original 12.2 s teleport and
subtitle timeline remain. Stop aliases 999800002/999800004 cancel both pieces.
The final recording contains its original lead-in, with speech around 13.25 s.

Private battle goal 250091 selects a Vortex tier once, when Act15 begins:

| HP at selection | Speed | Relative selection weight | Teleport chance | Private route |
| --- | --- | --- | --- | --- |
| Above 75% | 1 | 1 | 25% | 3080 |
| Above 50%, through 75% | 4/3 | 1.15 | 42% | 3081 |
| Above 25%, through 50% | 5/3 | 1.30 | 58% | 3082 |
| At most 25% | 2 | 1.50 | 75% | 3083 |

The native eligibility rules and 15-second cooldown policy remain; the four
routes share cooldown checks. A tier remains fixed during the attack. The
entire animation, including recovery, uses that rate for this initial trial.
Damage and the bullet's own 0.4-second lifetime are unchanged.

The animation owns neutral SpEffects 1627600 (live) and 1627601 (cue). The cue
starts one real second before the AoE launch at original timeline 2.666667 s.
Event 5750432 consumes the attack's single chance roll, checks both living
characters remain inside the encounter, and chooses the nearest eligible
destination. It requires the player inside a 6 m destination sphere, outside
its 2.5 m clearance sphere, and Hadeon outside that same clearance sphere.
It issues no animation reset, forced animation, AI command or AI replan.
No eligible point means the attack continues in place with no later retry.

Six metres is a provisional center-based envelope: bullet radius 2.5 m,
about 1.47 m static sword dummy offset, and about 2 m allowance. Actual posed
reach and character scale still need calibration; eligibility is not a hit
guarantee. The eight destination points and existing nearest-point helpers
are preserved. New eligibility regions are 18005936-18005943.

A successful Vortex relocation sets 1055425259, restarting the existing
15-30-second periodic relocation timer. Attack-local arm flag 1055425258
clears on consumption, the next battle activation and map initialization.
The marker window also prevents an interrupted animation from relocating.
First-encounter/reset/progression behavior is otherwise unchanged.


Recovery and verification
--------------------------

Core source/runtime backups and hashes are under
`.sovereign/backups/hadeon-vortex-20260928/`; audio, map, marker and animation
subtasks retain their own input backups and native validation receipts.

- Native event build: `.codex-temp/event-builds/1790583160807862400/`.
  Only events 5750300, 5750311, 5750312, 5750430, 5750432 and 5750433 differ;
  unrelated definitions, existing ordering and file metadata are preserved.
- `node --test tools/tests/test-hadeon.mjs`: 34 checks passed, including new
  range, phrase cancellation, eligible-marker selection and timer restart cases.
- Qualified Lua 5.0 interpreter running `tools/tests/test-hadeon-vortex.lua`:
  800 Act15 selections passed, including exact quartile/probability boundaries.
- Audio rebuild/readback is reproducible. Segment PCM rejoins exactly into the
  converted original; all 48 other existing media payloads are unchanged.
- Map readback preserves all original decoded content and verifies eight new
  spheres with 128 shell samples. Marker readback preserves all old parameter
  rows, other 193 parameter members and binder metadata.
- Native allocation scanned 598 event files and 194 parameter members without
  collisions for the new flags, event IDs and marker references.

Remaining game checks: callable speed variants, motion/TAE synchronization,
one-second warning at each tier, continued animation across the warp, actual
AoE origin/facing, interruption cleanup, audio direction after the opening
teleport, 30 m audibility, and fairness of double-speed recovery. These have
not been marked Passed.

Animation qualification preserved all 278 original TAE records and all
unmodified binder members. HKLib graph readback preserved 2,268 original
objects after object-ID remapping and validated 12 new route objects. No
player graph, global name table or HKS change was needed. Candidate proof:
`.codex-temp/hadeon-vortex-animation/candidate-v5/validation.json`.
Runtime acceptance retained eight guarded outputs and recovery copies in
`.sovereign/backups/hadeon-vortex-20260928/accepted/receipt.json`.

Integration and deployment
--------------------------

Repository and version checks pass for 1.5.9, with 78 catalogued runtime
files. The complete prepared main package contains 79 files including its
retained external dependency. Relative to 1.5.8, exactly five existing
runtime files change and the two c2500 animation/behavior binders are added;
no files are removed and the texture package is unchanged.

Nine load-reset/progression checks and three aid logic checks also pass.
Local links in the twelve touched guides resolve; `git diff --check` passes.

Guarded editor handoffs completed:

- AI and c2500 archives: `.sovereign/handoffs/6a6e753a5d494eeeb32ae586e7f96704/receipt.json`.
- Events and JavaScript: `.sovereign/handoffs/45935298e7c44aa38c1903f56329cc68/receipt.json`.
- Parameters: `.sovereign/handoffs/b472b6c898214c38a3bea9ce1569ca95/receipt.json`.
- Map: `.sovereign/handoffs/9b41b782087d4e9892abc4708679e23b/receipt.json`.

Prepared package: `.vdb/prepared/4f3f850a357f490b896a6d302c19a45f/receipt.json`.
Finalization submitted once through the safe deployment queue:
`.vdb/finalizations/b6d3559847e64e25a27c2053e49003b7/receipt.json`.
Finalization completed at 2026-09-28 08:27:27 UTC after the safe-deployment
gate cleared. Build `dd922c5c9e7f14468e28c86f` is enabled and deployed to
profile `SkC-QjDMc`; VDB verified the staged and live package with no differing
files, and the verified stage is selected for packaging. All 79 package files
are covered. In-game acceptance stays pending; `releaseReady` remains false.
