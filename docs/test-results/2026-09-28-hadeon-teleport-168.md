Hadeon teleport and victory timing 1.6.8
========================================

Changes and evidence
--------------------

The 15:40:36 gameplay trace recorded three periodic timer expirations, two AI
observations, no acknowledgment and no successful warp. Both observations
latched the unfinished-attack diagnostic; one request persisted for about
98 seconds. Eight Vortex attempts produced neither live nor cue markers.

The periodic battle branch now accepts an elapsed request when choosing its
next action without requiring `IsFinishAttack()`. Combat, living participants,
speech and throw checks remain. The map worker still owns arena validation,
landing clearance and the 15-30-second timer. The removed gate remains observed
in diagnostics so older and newer traces can be compared.

The Vortex graph correction addresses private clip names pointing at the native
3028 timeline. Private routes keep their native motion and intended HP-tier
speeds. Arming returns from the diagnostic 100 percent trial to 25/42/58/75
percent. Marker observers remain independent of arming, so an unsuccessful roll
does not hide whether the private timeline ran. In-game confirmation is pending.

Banner readiness moves from 10.0/11.5 to 10.5/12.0 seconds into the two death
lines. The remaining tails decrease by 0.5 seconds; full playback remains
17.24/13.12 seconds. Temporary flag 1055425255, previously reserved and already
covered by startup resets, is set immediately after the actual banner command.
The live reward worker waits five seconds from that signal. Reloads with saved
victory recover the uncollected reward immediately when alive. Collection flag
1055420916 still prevents duplication. Movement behavior and diagnostics are unchanged.

Verification
------------

- Event native comparison changes only 5750290, 5750303 and 5750312; metadata
  and all unrelated events remain equal. Candidate:
  `.codex-temp/event-builds/1790636170772399000/receipt.json`.
- Ten tutorial/reward checks pass, including five seconds from actual banner,
  reload recovery, waiting for a living player, duplicate protection and full audio.
- Progression/dialogue source simulation passes.
- Native Lua 5.0 compiled-member checks pass for periodic guards and all 800
  HP-boundary/chance selections. Existing periodic and Vortex regressions pass.
- HKLib readback preserves all 2,280 graph objects except the four private clip
  `animationName` fields. Native dispatch/name/event checks pass; native motion
  binding index 74, the animation binder and other behavior members are unchanged.
  Evidence: `.codex-temp/hadeon-vortex-marker-fix/repair-validation.json`,
  `graph-validation.json` and `behavior-candidate/validation.json`.
- Native AI binder comparison preserves registration and container/member metadata;
  only the compiled battle member changes.
- Native flag scan covers 598 event files and 194 regulation members. Only the
  two already-reviewed startup clear ranges include reserved flag 1055425255;
  no other ownership collision was found.

Recovery and deployment
-----------------------

Scoped event/AI backups: `.sovereign/backups/hadeon-teleport-168/manifest.json`.
Event editor handoff: `.sovereign/handoffs/42a4466454564c178162794ee82fa7ae/receipt.json`.
Animation backup: `.sovereign/backups/hadeon-vortex-graph-marker-20260928/`.
AI/animation editor handoff: `.sovereign/handoffs/348de77db7c442b290671c7aefa6d164/receipt.json`.
Prepared main package: `.vdb/prepared/954c315fe7174469a2d878b43afcc54b/receipt.json`.
It contains 79 files; only the m18 event, private battle AI and c2500 behavior
graph differ from 1.6.7. Textures remain at the previously deployed 1.6.7.
Finalization: `.vdb/finalizations/e8ae91c3865d4972bcdcb390ca424a1a/receipt.json`.
Deployment completed on the active Default profile. Independent SHA-256
verification matched all 79 main-package live files. Evidence:
`.codex-temp/hadeon-teleport-168/live-verification.json`.

Game acceptance remains pending: ordinary melee beyond 30 seconds, speech/grab
safeguards, pre-slam warp at each HP tier, interruption/arena exit cancellation,
both banner/death-line variants, reward timing and reload recovery.
