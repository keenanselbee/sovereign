Deflect criticals and Vortex diagnostic trial, 1.6.3
==================================================

The author approved seven-second deflect charges, charge-consuming critical
damage, tutorial wording, and a reversible trial to diagnose missing Vortex
teleports. Deployment and game acceptance are recorded separately below.

Deflect changes
---------------

SpEffect rows 102007-102010 change only their duration from three to seven
seconds. Successful deflects already refresh/upgrade them. The existing PvE
guard-counter damage rates remain 1.20/1.40/1.60/1.80.

Critical-only effects 1627611-1627614 clone Dagger Talisman row 320900 with its
native throw restriction, state and targeting flags. Their damage rates are
1.10/1.20/1.30/1.40. On confirmed critical attacker entry, HKS snapshots the
highest charge and removes all four charge effects. The snapshot lasts through
the whole throw animation, including multiple damage hits; parent throw exit,
defensive throw entry and first Update after load clear it. The six player
critical animation IDs are 31700/31710/31720/31730/31750/31760. Separate skill
grabs 40090/45080/45180 and failed backstab attempts do not consume charges.
See the [guarded recipe](../../src/recipes/deflect-critical/README.md).

Four tutorial copies now explain seven-second refresh, guard-counter/critical
damage, and critical consumption, retaining grip stamina, ultimate and controls.
Only the selected GoodsCaption/TutorialBody entries change.

Vortex trial
------------

- Each Vortex now arms a teleport attempt at all HP tiers. This is temporary
  diagnostic behavior, replacing the prior 25/42/58/75 percent roll.
- Eight destination eligibility spheres expand from 6 m to 8 m. Their positions,
  pairwise nearest selectors and both 2.5 m participant clearances are preserved.
- The animation cue remains a 0.1-second marker beginning one real second before
  impact. No animation assets, attack speeds or slam damage radii change.
- Flags 1055425275-5278 retain cue, invalid encounter, no eligible destination,
  and successful warp outcomes until the next Vortex or AI initialization.
  The existing reversible HKS trace records these plus armed 5258 and cooldown
  reset 5259. Schema 3 remains change-only, bounded and failure-contained.
- Existing periodic teleport improvements and load resets stay intact.

The diagnostic flags do not control gameplay. Disable the existing
`sovereignDialogueTraceEnabled` switch to stop logging. To conclude the trial,
restore the reviewed HP chance table and original sphere radii through a new
version, remove the trace fields/diagnostic setters, and retain the verified
underlying fix. Relevant source/runtime backups are under
`.sovereign/backups/vortex-trial-163`, `deflect-critical-163`,
`deflect-tutorial-163`, and `combined-163`.

Verification
------------

- Native regulation readback validates all rows and binder metadata: four
  durations plus four critical rows, every unrelated row/table preserved.
  `.codex-temp/deflect-critical-163/candidate/validation.json`.
- Critical HKS mocks exercise all six critical IDs and four tiers, no charges,
  highest-tier selection, complete-animation retention, exit/defense/load
  cleanup, dead-entry rejection and grab exclusion. Deflect stamina, aid and diagnostic tests pass.
- 48 encounter/progression/load source tests pass. Compiled Lua passes 800
  Vortex tier/always-armed cases and 11 periodic AI handoff cases.
- Native event comparison changes only event 5750432; other events/maps and
  metadata match. `.codex-temp/event-builds/1790589680421899900/receipt.json`.
- Native map comparison changes only eight radii; 128 geometry boundary samples
  pass. `.codex-temp/hadeon-vortex-map/trial-163-candidate/manifest.json`.
- Temporary diagnostic flags are free across 598 event files and 194 regulation
  members, including range checks. `.codex-temp/hadeon-vortex-map/flag-scan-163/flag-scan.json`.
- Independent AI binder inspection preserves metadata, both member identities
  and global-name payload. Only the reviewed bytecode changes.
- Four text candidates pass full decoded comparison. Candidate list:
  `.codex-temp/deflect-tutorial-163/candidates.json`.
- Native player asset qualification passes with current HKS guards; no
  generic Lua test is treated as HKS engine validation.
  `.codex-temp/player-qualifications/1790590018362192500/receipt.json`.

Deployment and game checks
-------------------------

Runtime candidates and all six editor handoffs are complete. Their receipts are
under `.sovereign/handoffs/`: params `d7117fa358b54622aca26a7e7bb2622d`, map
`b416662698494e2e9f4975863233c6f1`, text `29e28f108b884a3881e010fce5734ca3`,
AI `34cffceed4f34a948c7ae2d055390377`, events
`fe3505d6d67f408b8850b09948a0e900`, player
`0031fcc4a8b943e89c948950400c5b9d`.

The full 79-file package has exactly nine changed runtime files compared with
1.6.2. Prepared receipt `.vdb/prepared/624010db39a84685aef25f5fe6b1985b/receipt.json`;
deployment finalization `.vdb/finalizations/7a89684138ed42739e3206fda6f8b978/receipt.json`
completed for build `5228ca5dbd1bef1cbed00b50`. Version 1.6.3 is deployed, with
all 79 staged and installed file hashes verified against the prepared receipt.

In game, confirm critical animation reporting, multi-hit bonus,
Dagger Talisman stacking, no ordinary-hit/grab bonus, tutorial fit, and natural
Vortex cue detection. Inspect the latest `.dialogue.log` for `vortexArmed`,
`vortexCue`, `vortexInvalidArena`, `vortexNoLanding` and `vortexSuccess`.
Guaranteed attempts still require a valid cue, arena and safe destination;
these checks do not establish gameplay success.
