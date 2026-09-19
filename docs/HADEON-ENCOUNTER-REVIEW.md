Hadeon deflection and Nemesis attrition review
=============================================

Investigated 2026-09-19. This is static investigation and proposed design, not a
runtime change or observed game result. The author wants Hadeon tuned for a new
character, with deflection as the intended way to win and stronger Nemesis help
as Hadeon loses HP. Percentage HP loss on an arena fall/return is a candidate;
its eligibility and numbers are not settled.

The [opening plan](HADEON-SEAL-PLAN.md) still owns keyless access, barriers, travel
and retries. This report develops combat. Runtime, editor workspaces and deployment
were not changed. The earlier commit proposal needs refreshing after these docs.


Current player support
----------------------

Map events 5750305/5750306 start support 30 seconds after Hadeon is enabled, followed
by a 5-10 second wait before the first ordinary roll. Subsequent grants generally
have that wait plus about one second of branch work. There is no Hadeon HP scaling,
successful-deflection condition, or explicit combat-AI/living-player condition.
Arena and living-boss conditions are checked before the wait, not immediately
before the grant.

| Roll | Current result | Important details |
| --- | --- | --- |
| 2 of 6 flags | Darklight Heal, 1626935 | Instant HP fields are -100 percent and -1000 points: effectively a full heal under ordinary recovery rules. Chains to 501300, a 90-second effect with healing-rate field 1.3. Rerolls while player HP marker 239, the top HP band, is present. |
| 3 of 6 flags | Thorn Ward, 1626915/1626916 | Three sequential stages have incoming damage multipliers 0.4, 0.5 and 0.6: nominal 60/50/40 percent reduction before other modifiers. Each has 180-second duration and a damage-removal condition. Hit consumption/retaliation timing needs a game test. |
| 1 of 6 flags | Bewitching Shriek, 1626976 | Behavior 2555 fires bullet 10490004, maximum hit radius 13.5, attack 49102. Zero direct base damage and zero stance-damage fields. Applies bleed 1490010 and bewitching 1626912; usefulness against Hadeon is unverified. |

These are selection weights, not measured award frequencies. Unusable heals and
an already-present first ward stage reroll without the normal delay. Second/third
ward stages do not block a fresh ward. Effects 1626986/1626991/1626993 are short
visual effects, not additional statistical buffs.

The ward also cycles rolling-damage states. Worker 5750308 fires retaliatory Briars
through behaviors 2552/2551/2550 when damage marker 153 coincides with a stage ending.
Those bullets still apply shooter effect 1490000, with an instantaneous 80-HP cost.
They carry bleed effect 1490010; Hadeon has resident bleed immunity 90020. Do not
assume this is a cost-free tutorial shield or a reliable bleed-based boss attack.
Actual self-cost and chain timing remain unobserved.

Shriek's bewitching row lasts 60 seconds and includes incoming damage multipliers
1.5, outgoing multipliers 0.5 and stance-attack rate 0.05. These fields do not prove
Hadeon accepts it or changes allegiance. Its name does not establish a damaging
shockwave. Qualify that interaction before relying on it as a mandatory-fight payoff.

The local blessing worker shares flags 1055422049 and 1055422050-2055 with global
follower blessing event 5750111. This matters for existing saves, NG+ and co-op.
Tune this encounter independently of global follower frequency and shared Oath rows.


Which teleport represents a fall
--------------------------------

Event 5750304 has distinct recovery branches:

- Region 18002367 is below the arena: origin approximately Y=-104.4, height 25,
  versus start/landing points near Y=-75.94. It is the strongest existing candidate
  for the fall detector; exact coverage needs a map/game check. The current return
  chooses six points 18002368-18002373, rather than start point 18002366.
- Region 18002349 is a separate large box elsewhere in the dungeon. Depending on
  player location, it returns Hadeon to 18002374 or to the start and restarts the
  entrance. This is not the same arena-fall condition.
- Event 5750303 separately returns him after disengagement/player exclusion.
  That reset is not evidence that he fell.

These branches currently apply no scripted HP penalty. Charging every teleport
would allow retreat and safety recovery to become damage sources.


Proposed combat loop
--------------------

Prefer deflection and counterattacks to earn progress, with a fall serving as a
visible Nemesis punishment. Unconditional fall damage is simpler, but can make
pure ledge baiting more effective than learning deflection. It remains an explicit
alternative; the author has not selected a fall-credit rule.

A first prototype to compare in playtests, not approved final tuning:

1. Three successful deflections arm one visible Nemesis rupture. Bank at most one;
   do not require consecutive perfection or erase it on an ordinary hit.
2. The next genuine arena fall consumes it and removes 8 percent of maximum HP
   after Hadeon returns safely. An uncharged fall still performs its safety return.
   Normal attacks and guard counters remain productive throughout.
3. Preserve damage and phase during that live attempt. Death, rest, reload or a
   full encounter reset clears temporary credit/blessings. Do not make progression
   a permanent chip-away process across deaths.
4. Use existing portal/sound language and a predictable safe return with an occupied
   destination fallback and brief recovery. Avoid immediate surprise attacks or
   replaying the full entrance every time.

Maximum-HP loss avoids a shrinking percentage-of-current-HP tail. Eight percent
would still take thirteen charged falls without other damage: this is a warning
against making falls the only damage source, not a target fight length. If flight
is unreliable or infrequent, cash out the earned rupture on a successful guard
counter instead. Do not redesign flight AI merely to service the meter without a
separate moveset review.

For a first prototype, apply the 8-percent fall pulse only above 10 percent HP and
let a normal counterattack finish him on solid ground. A lethal return is possible
but needs explicit testing of relocation, death reconciliation and exactly-once
reward payout. Do not clamp HP upward when ordinary damage races the pulse.


Nemesis escalation
------------------

Use Hadeon HP bands for phase and successful deflection for repeated rewards.
Guarantee the useful mechanical help; randomness can select whispers and visual
presentation. A wounded player should not depend on drawing the right lottery ticket.

| Hadeon HP | Proposed earned assistance |
| --- | --- |
| Above 75 percent | Small stamina recovery and a clear acknowledgement of successful timing. |
| 75-50 percent | One encounter ward charge and a modest heal when wounded. |
| 50-25 percent | Stronger ward/heal and a short bonus to the next guard counter's stance damage. |
| Below 25 percent | Strongest protection and a conspicuous empowered counterattack to close the fight. |

Give a one-time clear phase-transition cue. Repeated aid needs a bounded cooldown
and fresh deflection progress, preventing idle heal farming. Refresh one bounded
reward rather than stacking unlimited wards/counter multipliers. Do not interrupt
input or obscure an incoming attack. Healing, stamina, durations and counter
multipliers remain tuning decisions.

Use encounter-local parameter copies and existing Nemesis visuals. Remove the
Briars self-cost and rolling/contact damage from the tutorial ward route. Any
offensive burst should follow an earned counterattack, rather than deliberately
taking damage. Preserve shared Sin/Bindseal effects. Assistance does not grant
allegiance, award a Bindseal, break the crystal or enable hardcore.


Clean implementation boundary
-----------------------------

- Use one host-owned encounter controller and one owner of recovery teleports.
  Coordinate 5750303/5750304 so falling, disengagement and death cannot start
  competing relocations. Replace this encounter's old random blessing worker.
- Arm fall detection only after Hadeon is alive on the arena floor. Latch entry
  into the fall region and rearm only after a verified return outside it. A
  cooldown alone cannot prevent repeated damage inside an oversized region.
- Recheck player/boss life, encounter state and defeat after delayed sequences.
  Pause support during teleports and clear only encounter-owned state on exit.
- A new instantaneous SpEffect applied to Hadeon can provide percent damage.
  The installed SpEffect definition documents effectEndurance=0 as one pulse
  and positive changeHpRate as subtraction from maximum HP. Use changeHpPoint=0,
  without a chained/repeating effect. This avoids changing maximum HP or reading
  raw HP addresses. Engine application and modifier interactions still need tests.
- Do not count 101990 as a pure deflect signal: common event 5750018 also emits it
  on kills. Effect 102001 marks a deflection window, not a successful hit.
  Existing 0.1-second marker 102019 is emitted by SetJustGuardSucceedEffect and is
  a narrower candidate for a map-event-only prototype. Qualify missed/merged
  pulses, consecutive hits and ordinary blocks. Never clear this shared marker.
  If unreliable, add a dedicated encounter-gated success pulse in that function
  and requalify the complete player group.
- Arena/combat checks alone do not prove attacker identity. Verify attribution
  with incidental enemies, hazards and co-op; guests must not write host progress.
- Reserve local flags/parameter IDs after checking current allocations. Derive
  phase from Hadeon's HP. Preserve defeat 1055420915, reward 1055420916, crystal
  1055420918 and the agreed journey reset policy. No new permanent progression
  system is necessary.


Starting-character tuning and acceptance
---------------------------------------

Current NPC 25000011 retains 1000 base HP, area 7030 (HP x1.656), 4410 (HP x2)
and boss 7380 (HP x2). Conditional general effect 7360 adds HP x1.5: nominal
9936 HP with it, 6624 without. These are arithmetic baselines, not observed HP.

Base stance durability is 80. Received stance rates 0.777 and 0.75 would require
about 137 raw stance damage before recovery/other behavior. Listed area/boss/base
stamina-attack multipliers multiply to about 2.63. Successful-deflect stamina
reduction and the custom two-handed branch need separate measurement. Healing
cannot fix a guard-stamina loop that starting equipment cannot sustain.

Tune the unique NPC/encounter effects, preserving other Crucible Knights and shared
modifiers. First trial removing redundant HP inflation and using an early-area
baseline. Seek recoverable mistakes, sustainable successful-deflect stamina and
consistent counter openings without Oaths, upgrades, consumable stock or one
required starting class. Final HP/damage values are playtest outputs.

Acceptance covers starting classes and one/two-handed guards; failed blocks versus
deflects; rapid multi-hits; passive waiting/ledge baiting; fall versus retreat
regions; occupied landing points; repeated region contact; simultaneous deaths;
phase boundaries; post-death/out-of-arena grants; retries; existing follower buffs;
co-op ownership; NG+; and unchanged reward/crystal progression. Compare normal
fights with no-attack ledge strategies and record deflects, falls, mistakes and
time to victory. No manual test was marked Passed.


Evidence
--------

The regulation, shrine map and saved event source matched their configured editor
counterparts. Regulation SHA-256:
4ac33e616abeb4cdac6242ad12b377133277fe656d1d5c3f23896be2e43241df.
Map SHA-256:
80c52f903a95cf788456d2a4bdc8c15130cb09593a17b278b20ee4f24f14e85e.

Sources: [shrine events](../src/events/m18_00_00_00.emevd.dcx.js),
[player HKS](../mod/action/script/c0000.hks),
[common events](../src/events/common.emevd.dcx.js), and the named current regulation
rows. The read-only native reader and selected-row/map export remain under
.codex-temp/hadeon-attrition-review/. Smithbox's installed SpEffect definition
supplies percent-damage field semantics. The reader checks input hashes before
and after inspection; it writes no runtime or editor assets.
