# Movement pause review, 2026-09-27

Investigation only. No runtime changes, deployment, or independent gameplay
reproduction. The author reports repeated one-to-two-second stops while holding
forward, with immediate recovery after changing direction and returning forward.

## Evidence and scope

- The expected Game-folder movement log, preserved in
  `.codex-temp/movement-review-20260927/`, was last written at 14:33:15 and
  contains only about 2.87 seconds of idle startup. It does not cover the latest
  reported stops or establish behavior of the later 1.4.6 deployment.
- The loader log records 13 loaded DLLs, including UnlockTheFps, FromStutterFix,
  RideAnywhere and Scripts-Data-Exposer-FS. It contains no movement-state trace
  identifying a culprit. Successful DLL loading is not runtime compatibility proof.
- The stronger retained incident is in
  `.codex-temp/diagnostics-1.3.0-review/Sovereign-movement.log`, lines 510-521:

  | Time | Processed input magnitude | Scripted speed | Locomotion/lower state |
  | --- | --- | --- | --- |
  | 105.077 | 2 | 2 | 1 / 1 |
  | 105.281 | 1 | 1.496 | 1 / 1 |
  | 105.491 | approximately 1 | 0 | 0 / 0 |
  | 105.700 | 1 | 0 | 0 / 0 |
  | 105.909 | 0 | 0 | 0 / 0 |
  | 106.318 | 1 | 0.033 | 1 / 1 |

  Update completed during these samples. Gesture, forced-walk effects 4101 and
  1626974, opening effect 1627121, action request and rescue markers were absent.
  HP stayed 522. Arena aid permission first appeared later, at 112.389 seconds.
  These are HKS variables, not raw directional input or measured world velocity.
  The trace supports the reported interruption but does not establish its entire
  duration or the direction used to recover.
- The older 1.2.9 capture contains a similar mismatch, but an aid exception makes
  it weaker evidence. The complete 1.3.0 Update trace demonstrates that fixing
  that exception did not resolve the movement problem.
- Reviewed current HKS movement dispatch, speed writes, custom cancel/jump/action
  functions and diagnostic implementation; authored EMEVD/ESD control paths;
  retained native effect inspections; qualified graph and TAE comparisons; and
  earlier isolation outcomes. This does not qualify every animation in game.

## Ranked suspects

Tiers express investigation priority, not measured probabilities.

| Tier | Suspect | Evidence and limits |
| --- | --- | --- |
| A | Idle/stop-to-move dispatch blocked or repeatedly restarted | Best fit to processed input remaining positive while locomotion becomes idle. `IdleCommonFunction` and `StopCommonFunction` can return through passive action, event animation, turn, guard, stance or other action gates before `MoveStart`. `Idle_onActivate`, `ExecEventAllBody` and all-body `ExecEventHalfBlend` zero scripted speed. A fresh direction can plausibly cause a new transition. No captured branch yet proves which path ran. |
| A | Transient input/sprint transition initiating a stop, followed by delayed recovery | The clean incident follows input 2 to 1: sprint to ordinary run. `ExecStop` normally refuses to stop when processed input is positive and gesture effect is absent. A brief zero or effect pulse between 5 Hz samples could initiate a stop, but cannot alone explain why positive input then fails to recover promptly. Raw axes, direction and per-frame transitions are missing. |
| B | Custom cancellation or upper-body action state overriding locomotion | `ModAnimationControl` can request idle through states 7000/7001 and movement through 7000/7003. Separate Divinity 7997 paths and attack/stance selectors remain relevant. However, the author still experienced the pause with the shared helper bypassed in 1.1.9; it is not a demonstrated sole cause. |
| B | Competing movement-scale writers or a scale persisting across a transition | `ModMovementMultiplier` and `Move_onUpdate` both write movement scale; rolling, jumping and damage callbacks also write it. The ordinary custom scales are positive, so a simple low multiplier poorly explains scripted speed and state both becoming zero. Damage callbacks do explicitly write zero, but no corresponding hit is established. The 1.2.2 speed bypass was staged/deployed; the retained report leaves its game result pending. Custom speed was restored in 1.2.4. Do not call this isolation conclusively passed or failed. |
| C | Controller/input translation | A direction change clearing the stop makes this worth comparing against keyboard W. The clean trace weakens sustained input loss because processed magnitude remains near 1, but brief dropout, directional translation or competing input sources are untested. |
| C | Conditional merged graph/action transition | The qualified current-vanilla-based graph contains substantial custom attack, deflect and stance work. Retained named-node comparisons found no Sovereign-only or overlapping ordinary Move/Idle/Walk/Run/Stop/Turn node, weakening a direct locomotion-node edit theory. Runtime graph behavior is still unverified. |
| D | Forced walk, rescue, aid, dialogue and periodic effect workers | These have real conditional paths, but the clean pre-arena incident lacks their relevant markers. Inspected aid/icon rows have no movement/action controls; statue force-animation calls require interaction. Current Hadeon dialogue ESD is a Quit-only isolation stub. Five-Hz sampling cannot exclude a very short pulse. |
| D | Ordinary locomotion clip/root motion or landing edits | Reviewed low a00 locomotion records have the same defined event payloads and timings; differences are ordering/trailing zero padding. Reviewed ordinary fall/landing records also match, apart from the documented heavy-landing effect. Custom a0x motion contains no a000 idle/run clips. A serialization/runtime issue is possible but unsupported. |
| Conditional | Frame-time or DLL interaction | No frame-time capture exists. If camera and enemies freeze too, prioritize this branch. If only the character stops and changing direction immediately restores it, actor state/input remains the stronger explanation. Loader presence alone does not justify blaming a DLL. |

Custom airborne actions were separately bypassed in 1.2.1 and the author still
reported the pause. This lowers that helper as the sole cause without ruling out
native falling, landing, or interactions with other states.

## Next decisive diagnostic

1. Retain a distinct log per session with build identity. The current logger opens
   a fixed relative filename with `w`, so a later initialization can overwrite
   useful history. Its 3,000-sample movement cap is about ten minutes at 5 Hz.
2. Keep a bounded per-frame memory history and flush a short before/after window
   when positive input coincides with idle/zero speed for roughly 0.25 seconds.
   Treat attacks, hits, menus and interactions as classified intentional stops,
   not automatic bugs. Avoid per-frame synchronous disk writes.
3. Record input magnitude and direction, sprint/guard/action state, active
   Idle/Move/Stop/upper-body callbacks, event requests, `MoveStart` outcome,
   `SpeedUpdate` inputs/result, every speed reset and movement-scale writer,
   custom states 7000-7016/7500-7507/7997, and frame/update timing. Add raw input,
   active graph nodes and measured displacement only through verified available
   APIs; the present logger does not expose them.
4. Preserve both the inner blocking reason and caller with a frame identifier.
   Currently `ExecPassiveAction` can log the precise reason, then its caller
   overwrites `gate` with a generic passive-action label. Old values also persist
   after the condition clears; their timestamps must be respected.
5. Reproduce on flat ground with ordinary forward movement, then sprint release
   while still holding forward. Capture one pause allowed to recover naturally
   and one cleared by a sideways/backward input. Compare keyboard and controller;
   note whether camera/enemy motion continues. Test outside Hadeon's arena too.
6. Choose one isolation from the resulting branch: positive input with no
   `MoveStart` means inspect the earlier gate; repeated movement/idle requests
   means identify the caller; speed calculated positive then reset means identify
   the last writer; active moving state with positive speed but no displacement
   means inspect scale, motion, collision and physics. A raw input dip directs
   investigation to input translation. Do not add a blanket forced-move reset.

## Related evidence

- [Earlier movement review and isolation history](2026-09-24-movement-pause.md)
- [Clean 1.3.0 follow-up](2026-09-24-diagnostics-1.3.0.md)
- [Qualified player graph/HKS update](../PLAYER-BEHAVIOR-UPDATE.md)
- [Qualified animation update](../ANIMATION-UPDATE.md)
- [Current HKS](../../mod/action/script/c0000.hks)

Root cause remains unconfirmed. Confidence is moderate that the first diagnostic
priority should be movement-state dispatch/recovery rather than changing the
movement-speed balance or replacing ordinary run animations.
