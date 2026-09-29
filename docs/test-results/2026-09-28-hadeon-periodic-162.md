Hadeon periodic teleports, 1.6.2
================================

The author rarely saw periodic teleports during close deflect combat. Source
review found an eight-metre separation gate in both event 5750430 and private
battle goal 250091. Closing that gap while awaiting acknowledgment discarded
the request and rerolled the entire 15-30-second cooldown.

Implemented changes
-------------------

- Remove the separation gate in both event and AI.
- Reuse request flag 1055425253 as the elapsed-cooldown latch. Speech and failed
  landing selection preserve it; no additional event flags are allocated.
- Acknowledge at natural action selection after an attack finishes, outside
  throws and active/pending speech. Raising the request does not force a replan.
- Recheck speech after acknowledgment. If speech raced the acknowledgment, or
  no point qualifies, clear acknowledgment, release the AI wait and retry with
  the existing ready request. This prevents holding combat idle during speech.
- Periodic selection excludes the existing 2.5 m clearance spheres around both
  player and boss. Select the nearest eligible of eight points to the player.
  Departure/arrival SFX only play on a successful warp.
- Retain arena, alive, host and fatal-region checks. Encounter invalidation or
  a successful periodic/Vortex warp resets the cooldown. Opening/fall selectors
  and Vortex probability/animation behavior are unchanged.

Verification
------------

- 37 actual event-source simulations pass, including cooldown boundaries,
  speech/acknowledgment race, melee, all eight landing exclusions, no eligible
  landing retry, cancellation and Vortex cooldown reset.
- 11 action-boundary cases execute the compiled Lua 5.0 member, covering melee,
  speech, unfinished attack, throwing, death, inactive combat and acknowledgment.
- Existing 800 Vortex tier/chance selections pass.
- DarkScript build and independent native EMEVD comparison identify only event
  5750430 as changed; other events/maps and metadata are preserved. Receipt:
  `.codex-temp/event-builds/1790588286749112200/receipt.json`.
- Independent SoulsFormats binder comparison preserves both member identities,
  container metadata and global-name payload. Only Lua bytecode changes. Its
  native header and input/tool hashes pass the existing guarded builder. Receipt:
  `.codex-temp/hadeon-battle-build/1833563198574f248a68883bc4e724a0/receipt.json`.
- `generate-selector.py --periodic` exactly reproduces the accepted selector.
  Nested simple branches avoid exceeding DarkScript's AND-group limit.
- Backups: `.sovereign/backups/hadeon-periodic-162/manifest.json`.

Deployment and game acceptance
------------------------------

Editor synchronization completed: events receipt
`.sovereign/handoffs/25e0a817a56547de81d297fc80e49a08/receipt.json` and AI receipt
`.sovereign/handoffs/c82b5f61a77c49b4a0fc378d1ab0fa5b/receipt.json`.

The reviewed full package contains 79 files, with only the m18 event and private
battle binder changed from 1.6.1. Prepared receipt:
`.vdb/prepared/9824780bfd344f08a33d2e2f9f3fdfc0/receipt.json`.
Protocol-3 finalization completed under
`.vdb/finalizations/53dcd794f27b4b0aaaaa86bf71586097/receipt.json`,
build `5577a603f0d4a851c7e3318a`. Version 1.6.2 is deployed; stage and installed
file hashes are verified against the complete 79-file receipt.

In-game testing
must confirm natural action-selection opportunities occur reliably during melee,
both characters remain outside landing clearance, and combat resumes immediately.
The 15-30 seconds is a cooldown followed by the next safe opportunity, not a
guaranteed wall-clock interval. Native and mocked checks do not prove game behavior.
