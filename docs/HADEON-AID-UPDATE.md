# Hadeon arena aid — 1.2.6

Current 1.3.3 implementation: aid waits three continuous eligible seconds,
then ramps over ten seconds in twenty five-point steps to 2x HP/FP/stamina maxima
and outgoing damage. Guard stamina cost reaches 0.5x (twice the endurance per
stamina point; approximately four times full-bar endurance with doubled stamina).
Resource percentages, spending protection and ten-second withdrawal remain.
Hadeon returns visibly to his original position facing the barrier; hallway
lights wait one continuous second outside before switching off. See
[implementation and verification](test-results/2026-09-25-opening-followup.md).
Native/source checks are distinct from pending in-game acceptance.

Version 1.3.1, deployed with verified live bytes: a 0.2-second permission grace bridges
short native permission gaps. These previously reset the ramp timer and held the
real 1.3.0 trace at tier one. The inactive path still avoids resource reads;
actual departure withdraws after the brief grace, and zero HP clears grace.
Source tests now include repeated permission gaps before the first tier, full
ramp, actual departure and death. This does not change buff magnitudes.

Movement diagnostics now retain up to 3,000 samples at 5 Hz (about ten minutes),
with scalar callback, early-return gate, animation-request, speed-reset and
speed-calculation observations. Recording remains player-only, bounded and
batched; capture is disabled after its cap. Gameplay decisions are unchanged.
The existing 600-sample aid trace also reports remaining permission grace.
These edits do not establish a fix for the independent movement pause.

Version 1.3.0 initializes the diagnostic call counter to zero, the unscanned tier
to -1 and absent pending adjustments to false. Nil globals resolve to the HKS
fallback function; the previous nil/or checks therefore threw inside Update.
After one-time tier recovery, inactive aid reads only arena permission and returns
before HP/resource reads or timers. Existing tiers and pending adjustments still
finish withdrawal. The bounded diagnostics remain, now labeled 1.3.0.
Regression mocks include the actual global fallback, 300 inactive calls, recovered
tiers, ramp/withdrawal, resource delays and diagnostics. No game observation yet
establishes whether this fixes the earlier intermittent movement pause.

Version 1.2.9 corrects the empty diagnostic log without changing aid gameplay.
Both logs start at the beginning of Update, write and flush a startup entry
before optional probes, and record probe failures as `field=ERROR[message]`.
A failed field does not discard other values or stop sampling. Builder failures
are recorded as `diagnosticError`; file failures close and stop that trace, with
one protected Script Exposer fallback. The movement trace now uses the same
living-player/non-COM/non-ghost guard, preventing zero-HP NPC log replacement.
`checkpoint` records how far the preceding Update reached; gameplay callbacks
retain their order and are not wrapped in exception handlers.
Movement remains capped at 600 samples / roughly two minutes, aid at 600 samples /
roughly five minutes. First samples flush immediately, subsequent batches every
five samples. Logging does not require entry into Hadeon's room. Actual engine
logging remains to be tested; source tests cover startup-before-probe, failing
reads, native nil/error returns, continued sampling, I/O failure and bounds.
Room and hallway lighting are byte-identical to 1.2.8. ER-110 remains unresolved.

Version 1.2.8 adds diagnosis only for the reported missing aura/stats. No new
save is required by the permission event; the root cause is not confirmed.
`Sovereign-hadeon-aid.log` records up to 600 half-second samples from the living
non-COM, non-ghost player, before the other custom Update calls. Fields include
aid call count, permission/aura, tier/direction/timer, pending recalculation,
scripted-state exclusions and current/effective maximum HP/FP/stamina.
File/native-read failures are contained and stop the trace. NPCs and dead actors
cannot open this file. The log is replaced on a new eligible script instance.
The aid remains a ten-second ramp and withdrawal; lighting's sixty-second
schedule is independent. Trace tests pass; engine diagnosis needs a new game
session with the updated files, then entering Hadeon's room (ER-111).

Version 1.2.7 makes two small corrections for the fresh-character test:
HP-percentage markers use effective maximum HP and refresh when only the maximum
changes; existing Oath healing still uses its base-HP value. A maximum-only marker
refresh does not add a Frenzied Flame curse roll. Each aid step checks the expected
maximum for HP, FP and stamina, allowing two points for native rounding. An
unexpected FP/stamina maximum skips that resource's adjustment for the step and
clears its fractional carry; the existing HP wait/timeout remains. No equipment
tracking, migration, extra flags or changed effects are added.

Approved on 2026-09-24. Entering Hadeon's arena builds Nemesis's aid in twenty
2.5-percentage-point steps over ten seconds. Full strength grants 1.5x maximum
HP, FP and stamina and 1.5x outgoing physical, magic, fire, lightning and holy
damage. Current resources scale proportionally, preserving damage and spending.
This is not a recurring full heal. The Darklight Shard's sustained player visual
accompanies the blessing without its healing-effectiveness mechanic.

Guard endurance uses reciprocal blocking cost: at full strength,
`guardStaminaMult = 1 / 1.5`. This is 50% more blocking endurance per stamina
point, not +50 Guard Boost. Together with 1.5x maximum stamina, theoretical
full-bar blocking endurance is 2.25x before other mechanics. Attack poise damage,
passive poise, status buildup and signature moves are not separately modified.

Aid holds while the living player remains in the arena before Hadeon's death.
Boss death or arena departure starts a ten-second withdrawal, including a
partially built blessing. Reentry resumes from the remaining tier. Resource
percentages scale down; living HP cannot be reduced below one by this adjustment.
Damage can still kill, and the code never revives zero-HP players. Actual player
death clears the native effects. The beginner rescue now fills the effective
maximum HP; Oath healing behavior is unchanged.

## Ownership and implementation

- Map event `5750403` supplies short-lived host-only permission `1627130` while
  inside `18000359`, outside fatal-fall region `18002367`, with Hadeon alive and
  without saved victory `1055420915`, confirmed death `1055425042` or scripted
  states `100690` / `9621`. Permission expires within 0.3 seconds on map departure.
- SpEffect `1627131` carries existing VFX row `7505352`, also used by shard
  effect `501300`. It has no shard state 50 or healing bonus. The visual stays
  applied through tier changes and is removed after withdrawal.
- Effects `1627141`–`1627160` are mutually exclusive stat tiers, derived from
  neutral row 153. Only the new tier remains after each swap. All new effects
  clear on actual death. No vanilla flags or existing parameter rows change.
- HKS `ModHadeonAid` waits for native maximum recalculation before adjusting
  current resources. It retains intervening damage/FP/stamina spending and
  fractional rounding. A mismatching maximum times out without stale writes.
  `bCurrHPIndependeMaxHP` avoids an additional native current-HP adjustment.
- Effective maximum HP reads `ChrDataModule` offset `0x13C`; current FP/stamina
  writes use `0x148` / `0x154`. The existing base-HP helper is retained for other
  systems. Offset evidence: [fromsoftware-rs data layout](https://github.com/vswarte/fromsoftware-rs/blob/main/crates/eldenring/src/cs/chr_ins/module/data.rs).
  Calls use the installed [Script Exposer API](https://github.com/ElaDiDu/Scripts-Data-Exposer-FS/blob/main/NewHksInfo.lua).

## Verification and remaining game checks

Native regulation roundtrip preserves every previous row, other table payload
and binder/member metadata. All 22 new IDs were checked against native rows and
references. Compiled map changes are limited to one constructor call and the new
permission event. Lua mocks cover ramp/withdrawal, partial bars, intervening
spending, reentry, one-HP withdrawal, actual death, delayed maxima and timeout.
Event simulations cover host/arena permission and the existing lighting/rescue
regressions. These checks do not establish HKS engine ordering or visuals.

Game acceptance is pending: ER-105/106/107 in [the test matrix](../TEST-MATRIX.md).
Specifically verify native resource clamping, equipment/max-resource changes,
rescue during ramp/withdrawal, simultaneous player/boss death, reload/warp,
co-op exclusion and VFX ending cleanly. No game was launched by this change.

Pre-edit files and hash manifest are retained under
`.codex-temp/hadeon-aid-1.2.6/`. Qualified editor sync and VDB completion are
recorded in that directory's completion receipt once finalization finishes.
