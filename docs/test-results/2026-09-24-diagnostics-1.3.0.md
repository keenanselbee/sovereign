Sovereign 1.3.0 gameplay follow-up
================================

Author report
-------------

Hallway and room lighting now work visually. Room lights extinguish on player
death, whereas the author wants the existing brightness retained through death.
The crimson aura appears on arena entry but resource bars do not visibly build
over ten seconds. Several movement stops still occur. This is partial visual
acceptance, not verification of every victory/crystal/reload scenario.

Captured evidence
-----------------

Copies of both logs are retained in `.codex-temp/diagnostics-1.3.0-review/`.
The logs identify 1.3.0. Movement contains 600 samples through t=123.289;
aid contains 280 through t=141.178. All samples after their startup report Update
checkpoint complete; no diagnostic errors are present.

Movement: t=105.491 and 105.700 retain approximately full forward input with
MoveSpeedLevelReal=0 and locomotion/lower states zero. HP is 522, rescue is unused,
and both forced-walk effects, gesture effect and Chapel opening effect are absent.
The preceding samples show sprint speed two, then input one/speed 1.496. Input
later becomes zero, then movement resumes. This occurs before arena permission
first appears at t=112.389. The aid Update exception is therefore fixed but does
not explain this captured stop. These are processed HKS variables, not raw
controller readings or a complete active-animation trace. Capture stops at the
600-sample limit, so later reported pauses are not covered.

Aid: the first step changes maximum HP/FP/stamina from 522/78/97 to 535/79/99.
Tier stays at one through the last sample. Permission drops to zero at t=113.403
while the aura and tier remain active; direction changes to -1 and timer resets.
Subsequent samples repeatedly show short timer values despite continuing arena
permission. The permission effect lasts 0.3s and is requested every 0.1s; native
reapplication/expiry timing is a leading explanation for brief gaps, not proven
by half-second sampling. Parameter isExtendSpEffectLife is eligibility for other
lifespan-extension effects, not a documented reapplication refresh switch.

A scratch reproduction using the actual aid source and global fallback, an
initial 0.6s permission and subsequent 0.30s-on/0.05s-off permission pulses stays
at tier one. A scratch-only 0.2s permission grace reaches tier twenty, with mock
maxima 750/150/150 from 500/100/100. This establishes the timer-reset failure mode,
not the exact native cause of each permission gap. Runtime files were not edited.

Death lighting: event 5750370 clears all brightness flags on confirmed player
death, while 5750404 resets the ignition flags; per-position workers then remove
the lights/flames. This is explicit behavior, not a rendering failure.

Recommended follow-up
---------------------

Preserve current room brightness and the set of ignited positions during death,
stop additional ignition, and reset on respawn/map reload. Keep crystal/victory
precedence and temporary lethal-rescue handling distinct from real death.

Debounce short permission gaps for 0.2s while retaining a cheap inactive return.
Actual departure should still trigger ten-second safe withdrawal after that
short grace. Test uninterrupted entry, brief gaps, real departure, death and
resource recalculation ordering.

Keep movement diagnostics focused on the state transition: active Idle/Move
callbacks, which branch prevents MoveStart, calls resetting real speed and the
speed-calculation inputs/output. Expand the bounded capture beyond its current
two-minute window. Do not repeat the already unsuccessful broad speed/jump/
animation-cancellation toggles or claim this pause's root cause is proven.
