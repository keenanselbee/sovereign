Hadeon rescue and steady ignition correction — 1.2.5
===================================================

Author report: Hadeon appears to retreat when a beginner rescue briefly takes the
player through zero HP, and lights flash while starting. Inspection confirmed a
raw zero-HP/lost-aggro reset trigger with an unchecked six-second teleport delay,
plus explicit on/off/on/off/on ignition pulses. This supports the reported cause;
no frame-by-frame game trace established engine timing.

Implementation
--------------

- Map event 5750402 owns valid temporary flag 1055425042. Zero HP must persist
  for 0.5s, and rescue protection 1627125 must be absent, before it sets the flag.
  Recovery cancels confirmation and clears the flag. It is host-owned and resets
  on map reload; vanilla death/progression flags are unchanged.
- Hadeon controller 5750303 monitors this confirmed state rather than raw zero HP.
  Brief loss of combat inside arena 18000359 does not queue a retreat. The separate
  player fall-region condition and out-of-arena loss-of-combat condition remain.
- The six-second retreat delay is interruptible. Recovery/return cancels it;
  Hadeon's death takes the victory path instead. The reset conditions and boss HP
  are checked again before the warp. Combat UI/state is not cleared for a canceled
  request. Existing Hadeon fall/reposition event 5750304 is unchanged.
- Presence worker 5750305 clears milestone receipts only on confirmed death.
  Positive-HP checks still prevent granting effects while the player is dying.
- Lighting controller 5750370 and ignition worker 5750401 use the same confirmed
  death flag. A transient zero-HP rescue does not darken/restart the room.
- Each ignition group now switches on once at its existing shuffled delay, with
  the existing 0–0.04s timing jitter. Removed deliberate 0.45s catch-light flashes.
  No changes to map/FXR assets, HP intensities, victory hold or crystal/eclipsing fade.

Verification
------------

The new flag is absent from all 194 native parameter tables and pre-change event
sources. Native compilation succeeds. Decoded comparison changes only constructor
0, events 5750303/5750305/5750370/5750401 and adds 5750402; every other event and
binder header is preserved.

`tools/tests/test-hadeon-lighting.mjs` executes source-event simulations for:

- Monotonic ignition over ten seconds, HP presets, victory and crystal states.
- A rescued zero-HP interval and transient loss of combat: no teleport, no lost
  milestone receipts and no extinguished lights.
- Confirmation inhibited during rescue protection, sustained death clearing the
  room/milestones and allowing the delayed teleport.
- Recovery after confirmation canceling a queued warp; Hadeon dying during the
  wait taking the victory path without teleporting.
- Preserved fall/out-of-arena retreat and cancellation after returning.

This is a bounded death confirmation, not a change to the engine's death state.
Live rescue/event scheduling, normal death retries and visual smoothness still
need an in-game retest. Backups and native-build evidence are under
`.codex-temp/hadeon-1.2.5/`; editor handoffs retain their own recovery copies.
