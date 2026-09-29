Tutorial and Hadeon follow-up 1.6.7
==================================

Implemented changes
-------------------

- Ultimate charge is now deflection-only. Kill event 5750018 preserves all other
  rewards. The shared full-charge spark cue remains unchanged.
- The Ultimate lesson latches Soldier arena admission, waits 2.5 seconds even
  after leaving the small start box, and waits through transformation. Death,
  departure, lost admission and victory still suppress the pending popup; the
  saved shown flag remains respected. The new text explains the readiness sparks.
- Deflection text explicitly says guard counters and critical hits consume all
  charges; the existing duration, stack count and two-handed guidance remain.
- Both author-edited PNGs under `src/textures/tutorial/` are rebuilt into the
  separate texture package. Original images and Desktop exports are unchanged.
- Hadeon subtitle cue starts move to 2.70 seconds for the hunger response,
  6.70 seconds for the final normal-death cue, and 4.70/7.90 seconds for the
  no-bonus death transitions. Voice media are unchanged.
- Death-banner readiness uses 1055425282 at 10.0/11.5 seconds of playback.
  Cleanup still waits for 17.24/13.12 seconds through 1055425256, preserving
  the hidden voice carrier while the reverb finishes.
- Hadeon Vortex uses 200/233/267/300 percent original speed by descending HP
  quartile. Flame-breath selection weight is multiplied by 0.85.
- Periodic teleport observations distinguish timer, expiry, request, acknowledgment,
  invalid encounter, speech deferral, unavailable landing and completed warp.
  AI observations distinguish unfinished attack, throwing, speech, invalid HP and
  absent combat state. Vortex queue and subsequent battle activation are logged;
  the latter is not proof that an attack completed successfully.
- Movement filtering recognizes fresh native jump, crouch, guard-reaction,
  damage, landing and event-animation callbacks. Continuous pauses still become
  eligible after six seconds; a stale callback alone cannot suppress a new stop.
  Movement decisions are unchanged. Existing diagnostic enable switches remain.

Verification and recovery
-------------------------

Event candidate `.codex-temp/event-builds/1790633716950540400/` preserves all
unrelated events and file metadata. Only common 5750018 and map events 5750363,
5750300, 5750303, 5750312 and 5750430 differ. No runtime common_func was added.
The new flags were scanned against 598 event files and 194 regulation members,
including ranges, with no prior allocation collision.

The audio comparison changes seven silent subtitle media and their size fields;
all audible voice media remain byte-identical. Native bank readback passed.
The complete texture comparison covers 3,079 members, changing only
MENU_Tuto_00016 and MENU_Tuto_00018. Archive/member/TPF metadata and DDS headers
remain unchanged. All three English menu binders change only the two tutorial
entries. Their guarded decoded comparisons passed.

Source simulations cover encounter behavior, tutorial interruption/entry,
independent banner/audio timing, kill rewards, movement filtering and diagnostic
isolation. They do not establish native AI/animation behavior or in-game appearance.
An older rescue test was updated to reflect the already-implemented first-attempt
aid exclusion; this batch makes no rescue-mechanic change.

The AI build uses native Lua 5.0.2; 800 tier selections and request diagnostic
checks passed. The animation readback changes only private TAE 3030-3033 speed
and cue fields. The behavior binder is unchanged and matches the qualified
AI/HKS/graph route, but this does not establish that the engine fires its TAE
markers. Its validation is retained under `.codex-temp/hadeon-attack-batch/`.
The 60 encounter/Rick simulations, 11 tutorial/opening checks, 10 movement checks
and dialogue-trace check passed. Optional game tests remain pending.

Completed editor handoffs:
- Events: `.sovereign/handoffs/e98b74468bf04f0da55289b67786a292/receipt.json`.
- Player HKS: `.sovereign/handoffs/87039baff00d4238b27782a6030acb46/receipt.json`.
- AI/animation: `.sovereign/handoffs/108c885f25f54f89bbdc3cb99c5b7c1a/receipt.json`.
- Text: `.sovereign/handoffs/50d0049b24424a9ab367363aaa8339e9/receipt.json`.

Main recovery files: `.sovereign/backups/tutorial-combat-167/`.
Audio recovery: `.sovereign/backups/hadeon-subtitle-timing-2026-09-28/`.
Text/texture recovery and native comparisons are retained under
`.codex-temp/tutorial-wording-20260928/`,
`.codex-temp/tutorial-texture-backup-20260928/` and
`.codex-temp/tutorial-texture-verify-20260928/`.

Deployment and game acceptance
------------------------------

Main and textures 1.6.7 deployed successfully to the active Default profile
`SkC-QjDMc`. Independently verified all 79 main files and all three texture files
against the prepared package hashes (82 total). Release readiness remains false.
Finalization: `.vdb/finalizations/f26fa0f30e534f169411683900242683/receipt.json`.
Main stage: `0be5f6228d36be313ca2b3e9`; textures: `439e0443e1680b37dda46fc5`.

Verify tutorial visibility on a save without its shown flag, text fit and both
images; deflect versus enemy-kill charging; both death subtitle sequences and
banner timing without audio truncation; all Vortex HP tiers and breath frequency.
At 300 percent speed the impact occurs less than one second after animation start,
so a full one-second pre-slam cue is impossible. Check the shortened cue in game.
The teleport and movement issues remain diagnostic investigations, not confirmed
gameplay fixes. Review the new logs after reproducing them.
