Hadeon temporary load reset 1.4.9
================================

The author requested a fresh Hadeon encounter on deliberate loads while deaths
continue accumulating aid, and accepted a saved death-reload bypass as a temporary
approximation. This is not a title-screen lifecycle detector.

Common preconstructor 50 performs the host-only reset inline before encounter
initialization. It consumes saved flag 1055420938 without resetting progression
after a death. Otherwise it clears defeat 1055420915, losses and first-dialogue/
entitlement flags 1055420930-1055420937, last-line history 1055420940-1055420951,
and temporary combat/dialogue/aid flags. Collected-item receipts 1055420916 and
1055420250, statue keys and the crystal choice 1055420918 remain untouched.
A previously earned, undelivered normal or no-aid reward defers the reset until
delivery; reload again after collecting it to begin a fresh test.

Common event 5750425 is Default (not restarted at grace rest). It waits for a
living player, then a zero-HP native death (or Graveyard's confirmed-death flag)
without rescue protection, rechecks
one frame later and sets the saved bypass. SaveRequest occurs two frames later,
after the map loss worker's one-frame settlement. It observes deaths outside the
arena too. A recovery without reload clears the bypass before observing another
life. Native save timing and cross-file preconstructor ordering require game tests.

The earlier per-admission first-monologue override is removed. A fresh reset gives
the first speech and no aid; death retries use repeat entrance dialogue and retain
earned aid. Existing proximity, volume, subtitle-disabled and movement diagnostic
trials are unchanged. The proposed AI-replan trial is not part of this change.

Known limits and removal
------------------------

Fast travel also resets the encounter. Quitting or crashing between death and
respawn can preserve progress once. A missed death marker would reset on respawn;
test that boundary before relying on a long progression test. Resetting saved
progress is intentional: removing the code does not restore the old saved flags.

Remove the tagged preconstructor block, constructor initialization and common
event 5750425, then rebuild/sync/deploy to remove the test. Keep the restored normal
entrance history. Recovery inputs are under
`.sovereign/backups/hadeon-load-reset-149/`; do not blindly restore old whole files
after subsequent changes.

Verification
------------

- Native allocation: 598 event files and 194 regulation members; no collision for
  saved bypass 1055420938 or event 5750425.
- Twenty encounter/reset source tests passed, including both worker scheduling
  orders, saved loss at save request, death bypass consumption, subsequent reset,
  pending rewards, clients, rescue, zero HP and recovery without reload.
- Existing progression simulation passed: capped losses, fatal falls, dialogue
  selection/priority, no-repeat history and reward delivery.
- Native candidate `.codex-temp/event-builds/1790550983830168700/receipt.json`
  changed only common events 0/50/new 5750425 and map event 5750311. Metadata
  and existing event order are preserved; the seven other runtime event files
  are byte-identical. Authoring-only common_func was not accepted.
- Guarded source/runtime acceptance: `.sovereign/backups/hadeon-load-reset-149/accepted.json`.
  Editor handoff `.sovereign/handoffs/7ac11ba27a8f43d19878914523f507bf/receipt.json`
  completed for four files. Preparation, version, whitespace and local-link checks
  passed. Source simulation does not establish engine behavior.

Game acceptance remains pending: quit/load produces a fresh fight; two consecutive
deaths retain and increase aid; rest preserves state; fast travel resets; no-loss
victory and delayed reward delivery preserve item receipts; fatal bridge death
preserves the loss; repeat entrance follows death while first entrance follows
deliberate reload. AI engagement after the first monologue remains unresolved.

Deployment
----------

Prepared package `.vdb/prepared/baec46e2c97b4282948c2994a4099095/receipt.json`
contains 75 files. Only `common.emevd.dcx` and `m18_00_00_00.emevd.dcx` differ
from 1.4.8; the other 73 files match, including the external Script Exposer DLL.
Finalization `.vdb/finalizations/105f0402a85f41ad9d88841642526662/receipt.json`
completed request `e9539719-74f7-480a-b7d9-291093af83a9`, build
`1ce613c3cf2dadba8e8aa324`, version 1.4.9. Profile `SkC-QjDMc` is enabled,
deployed and verified with no differences. Independent hashing of all 75 live
files also matched; evidence is
`.sovereign/backups/hadeon-load-reset-149/live-verification.json`.
