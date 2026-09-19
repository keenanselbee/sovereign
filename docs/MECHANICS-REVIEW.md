Obliterator, Claw and Dragonbolt review
=====================================

Reviewed after the release automation work, 2026-09-11 local time. The author's
Claw/Dragonbolt changes are treated as intentional. No gameplay source, runtime
file, editor output or deployment was changed during this investigation. These
are static findings and recommendations, not observed game-test results.


Evidence and limits
-------------------

Fresh native reads used the installed Smithbox libraries and parameter definitions
to inspect current repo/editor regulation, current player timelines and both known
historical backups. Each input hash was checked before/after reading. The reader,
project file and bounded exports are retained in `.codex-temp/mechanics-review/`.
The reader initially needed Smithbox's native DLL directory added to its process
PATH; it then completed. No external tool installation or asset rebuilding occurred.

- Current repo and saved Smithbox regulation match:
  `4ac33e616abeb4cdac6242ad12b377133277fe656d1d5c3f23896be2e43241df`.
- Current player timeline binder:
  `a36f192c3a0918e7bbf70507c0b5dbd685bde842a22daf1b03749df75e2c6de0`.
- The relevant current Claw/Dragonbolt/Void Eye effect cells and special-attack
  behavior cells match Backup 2. Row names can differ; comparisons use cells.
- Animations a00/50510, a544/145010 and a984/30600, 32400, 32610, 32615 match
  Backup 2 completely. These questionable references predate the recent handoffs.
- DSAnimStudio's installed Elden Ring template identifies events 1/2 as attack/
  bullet behavior and 66/67 as effect applications. HKS and parameter links were
  inspected alongside those events, rather than treating absent effect IDs alone
  as proof that a feature is broken.


Blasphemous Claw
----------------

The current design has a coherent replacement for the old conditional effect chain.
`ModEndureBlasphemousClawBackstep` in `mod/action/script/c0000.hks` is called from the
backstep input path. It explicitly handles Endure state 7705, Claw state 7180 and
the FP branches: both at 15 FP, the available individual effect at 9 FP, and the
Endure no-FP state otherwise. It applies existing effects 1626601/1626602 (Endure
state markers) and 1626624 (Claw state 7181).

Animation a00/50510 still has valid attack and bullet paths at about 0.333 seconds,
both gated by state 7181. They resolve through behavior rows 300000690 and 300000897
to attack 300000690 and bullet 10208000 respectively. The bullet has a corresponding
player attack row, and the animation's attack event explicitly selects Parry
(`AttackType=64` in the installed TAE template).
The cosmetic row names are not reliable evidence of intended mechanics.

The six earlier effect requests 1626616-1626621 are still dangling. Backup 1's
1626616-1626619 gated states 7286-7289 and invoked 1626600, which gated 7705 and
invoked 1626601. The current HKS supplies the Endure marker directly. Also, 1626601's
cells are unchanged from Backup 1: the older scratch report's assertion that its
semantics changed was incorrect. Neither backup supplies 1626620/1626621.

Effect 1626625 exists, but its mere presence does not establish that it is used:
no direct 66/67 application appears in the reviewed Claw timeline, and no inbound
reference was found in the inspected parameter tables. This does not invalidate
the independently connected attack/bullet parry routes.

Opinion: leave the custom mechanics intact. The evidence fits an old conditional
implementation being superseded by explicit HKS logic, with leftover references.
Restoring the old chain could interfere with the chosen FP/state behavior. Test
Claw-only, Endure-only and combined backsteps at the FP boundaries and confirm the
intended parry window/targets before considering any change or cleanup.


Betrayer's Dragonbolt
---------------------

The spell has independent connected paths despite the absent 1626823 requested by
a544/145010 at about 0.667 seconds:

- Magic 2006910 directly applies existing self-buff 1626741 for 180 seconds. Its
  parameters include status buildup multipliers of 0.85, lightning damage-received
  multipliers of 1.35 and enemy lightning damage multiplier 1.25. These are raw
  modifiers, not independently measured final damage or resistance percentages.
- HKS explicitly detects 1626741 and selects the Betrayer movement, roll and jump
  multipliers, authored as 1.15 times the respective global settings.
- Behavior 300000089 invokes bullet 210691000, whose child 210691001 carries
  1626730 and 1626731. Those effect rows deliberately distinguish friendly and
  opposing targets. The ally row supplies its own buff modifiers; the enemy row
  includes increased lightning damage received. Both use 90-second durations.
- The referenced bullets have corresponding player attack rows. The self-buff,
  ally branch and enemy branch are not dependent on the missing 1626823 row.

This supports a deliberate self-enhancement plus ally/enemy interaction design,
not a missing wholesale vanilla spell import. Neither inspected backup contains
1626823, and the current connected effect cells/timeline match Backup 2.

Opinion: leave it intact. The isolated missing timeline effect looks more like a
leftover than evidence that the spell's intended core behavior is broken. Test
self/ally/enemy application, expiry and movement restoration. README's exact
stamina-per-second claim still needs measurement: the self row uses
`changeStaminaPoint=-1` with `motionInterval=0.667`, which is not sufficient evidence
for the documented +15 SP/s. Do not silently retune the spell to match prose.


Fallingstar Obliterator
----------------------

The strongest unresolved connection is the extra one-handed payload. Animation
a984/30600 has a bullet-behavior request at about 1.1 seconds, selecting behavior
300000867. That row is present but has `refType=0, refId=-1`: no payload target is
assigned. It was already this way in Backup 2. Other ordinary attack events remain
at about 0.433, 0.600, 0.767 and 1.067 seconds, so this does not establish that the
whole move is nonfunctional. It may be an intentionally disabled extra payload or
an unfinished connection. Copying the two-handed projectile would invent a design.

The two-handed special connects through 300000868 to gravity bullet 210471008.
The ultimate connects through 300000869 to beam bullet 4620221, with an existing
player attack payload. The ultimate refreshes Void Eye effect 1626770.

`ModUltimateAttackConditions` explicitly requires state 7750 for category 984 to
take the beam route. Void Eye supplies that state for 60 seconds. Without it, HKS
requests the alternate heavy-special start/end events; matching a984/32610 and
32615 records and graph animation selectors exist. Those records import a031/32400
and contain attack events. Returning false from the beam gate therefore does not
mean that HKS requested no action. Simultaneous start/end dispatch, timing and
actual fallback damage still require observation.

Opinion: preserve the buff requirement and fallback. Prioritize a focused test of
the one-handed special with/without Void Eye and the ultimate before buff, during
buff and after expiry. If the intended extra one-handed effect is missing in play,
choose its payload explicitly with the author. Do not infer a projectile, remove
the beam gate or restore historical effects solely to eliminate reference warnings.

The existing manual matrix remains Pending. No gameplay fix is recommended without
an observed failure or an explicit design decision about the unassigned extra payload.
