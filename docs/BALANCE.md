Sovereign balance design
=======================

Living balance document, established 2026-09-11. Read [DESIGN.md](DESIGN.md) for
feature intent and coverage. This document owns the working balance questions,
confirmed author decisions and evaluation approach. It does not approve or apply
the numerical experiments in the earlier [BALANCE-REVIEW](BALANCE-REVIEW.md).

The intended game uses Oaths, active defense and powerful custom tools against
substantial opposition. The author describes the opening as **challenging**.
Divinity deliberately preserves buffs while the player remains undamaged.
Obliterator should earn ultimate charge like the other weapons.


Author decisions
----------------

Record intent separately from current implementation and observed results.
These decisions were supplied directly by the author in this conversation.

| Date | Topic | Confirmed intent | Consequence |
| --- | --- | --- | --- |
| 2026-09-11 | Overall difficulty | The game is balanced around using Oaths and the powerful tools available | Evaluate expected tool use rather than treating an unbuffed vanilla-style run as the sole baseline |
| 2026-09-11 | Opening | "challenging" | Preserve a challenging start; this does not select exact multipliers or an early Oath acquisition change |
| 2026-09-11 | Hadeon opening direction | Keyless dungeon access; mandatory Hadeon tuned for a new character using deflects; barrier and local travel lock until victory | Supersedes optional key-triggered commitment; retain existing barrier lifetime and investigate gate removal, travel, retries and local boss tuning |
| 2026-09-19 | Hadeon combat | Deflection should be the intended new-character solution, with stronger Nemesis help as Hadeon weakens | Investigate fall-related percentage attrition; eligibility, amounts and buffs remain proposed in [the encounter review](HADEON-ENCOUNTER-REVIEW.md) |
| 2026-09-11 | Nemesis release | Releasing Nemesis starts hardcore | Preserve the explicit crystal escalation and distinguish it from existing ordinary Nemesis pressure |
| 2026-09-11 | Eclipse timers | The six-second waits were for testing; restore the commented intended waits and retain testing alternatives as comments | Restored the seven progression-dependent random waits in event 5750115; no other eclipse timing or eligibility changes |
| 2026-09-11 | Divinity | "preserve buffs as long as the player is undamaged" (spelling normalized) | Duration preservation is intended; do not replace it with a fixed short window merely because buffs last a long time |
| 2026-09-11 | Divinity damage break | Taking damage ends preservation and existing buffs start counting down | Preserve remaining buffs; verify timer resumption rather than demanding that damage remove every buff |
| 2026-09-11 | Malenia | Deflection mastery is the expected solution; deflects should grant her no healing | Preserve the encounter's defense requirement and verify healing suppression across attack variants |
| 2026-09-11 | Maliketh / Destined Death | Master deflects or use Divinity to counter the overpowering damage | Evaluate the intended counter before proposing a general boss damage reduction; distinguish holy hits from HP burn and maximum-HP loss |
| 2026-09-11 | Obliterator | Earn ultimate charge like the others; the author recalls the resident full-charge effect as likely beam-testing setup | Remove resident effect 287 in the pending gameplay fix; preserve Harness Void Eye, its buff prerequisite and the beam's buff refresh |
| 2026-09-11 | Claw and Dragonbolt | The author heavily modified them and expects them to be mostly intentional | Preserve connected custom behavior; test suspected failures rather than restoring old chains or vanilla behavior by name |

The author reaffirmed that Obliterator's full-charge effect looks like their
beam-testing setup and agreed with removing that bypass while retaining the
buff-and-beam relationship. The exact testing history is recollected rather than
independently established. The charge fix remains pending; documenting the ruling
does not mark it implemented.


How to interpret evidence
-------------------------

The [stored parameter evidence](balance-review-evidence.json) and review describe
the inspected regulation version 11711000 and named input hashes. Those recorded
inputs were rechecked unchanged when the initial documents were created. The later
eclipse fix changes the common-event source and compiled output; its current
verification is recorded in [MECHANICS.md](MECHANICS.md). The stored review remains
a historical snapshot. Totality, Divinity and ultimate findings still use the
inspected unchanged HKS, regulation and animation baseline. Future gameplay edits
must refresh the affected evidence or explicitly identify the superseded snapshot.

| Statement | Required basis |
| --- | --- |
| Intended behavior | Author statement or an explicitly accepted design decision |
| Implemented behavior | Connected source, parameters and relevant animation/event path |
| Observed behavior | Actual game result with build, save and steps |
| Suspected imbalance | Evidence plus an explanation of why it conflicts with the intended role |
| Proposed tuning | Explicitly labeled experiment; not implemented or author-approved by default |

Do not assume a raw attack field is final damage. Separate weapon correction,
base attack, defense, damage reduction, status buildup, percentage-HP damage and
stance damage. Count actual hits: conditional projectiles, shared hit lists and
target size can change the result. Include setup, resource cost, risk, duration and
repeat frequency when comparing powers.

The intended strength can be exceptional. The meaningful questions are whether
the player earned it, whether its conditions work, and whether it leaves the
intended alternatives and encounters useful. Buff preservation during undamaged
Divinity is an example of intended exceptional strength, not evidence of a defect.


Difficulty across progression
-----------------------------

### Opening and ordinary encounters

**Confirmed direction: challenging.** The exact tolerance for early deaths, Oath
discovery and optional dangerous detours remains to be specified. Do not translate
that single word into approval of either the current numbers or a global reduction.

Guaranteed early Order access and reduced early stat stacking remain candidates
to evaluate against the author's chosen opening. The intended eclipse waits have
separately been restored as confirmed below. Improving explanations, telegraphs
and access to known tools can address a different problem from reducing enemy
strength.

Useful observations are the first ordinary enemy hit, a small group encounter,
the first Nemesis, the first successful deflect, the first usable Oath and the first
unavoidable progression fight. Record what the player could reasonably know and
obtain at each point, not only a fully optimized route.

**Current acquisition evidence:** accessory 1050 (Radagon's Scarseal) supplies
Order; 1051 (Radagon's Soreseal) supplies Golden Order. Their map lots 1042330100
and 1051390060, plus Marika's Scarseal lot 12020050, match vanilla in every field.
Radagon's Scarseal is the [Weeping Evergaol](https://eldenring.wiki.gg/wiki/Weeping_Evergaol)
boss reward, making southern exploration a plausible first-Oath route. The Soreseal
is a [Fort Faroth pickup](https://game8.co/games/Elden-Ring/archives/369955), so an
informed player can attempt the stronger Oath early through a dangerous detour.
Neither is established as an automatic opening reward. A blind player may miss
both; no reliable hours-to-acquisition estimate has been measured in Sovereign.
Evaluate discoverability before deciding whether either reward should move.

The revised [mandatory Hadeon opening](HADEON-SEAL-PLAN.md) supersedes the optional
key-triggered seal proposal. Hadeon must be balanced for a new character's deflects
and starting equipment before an Oath is assumed. The current 1000 base HP has
substantial additional scaling: Stormveil-tier 7030 and two HP-doubling effects,
with the general HKS base modifier also normally applied. Measure effective stats
and trial Hadeon-local reductions rather than changing shared enemy modifiers.
Keyless access and defeat-gated travel remain proposed implementation work; the
barrier lifetime already matches. Review route hazards, internal retries, existing
player-support blessings and early access to the reward/Bindseal/crystal together.

### Nemesis numerical baseline

| Contribution | Base effect 7360 | Nemesis effects 1626950-1626953 | Combined contribution if both apply |
| --- | --- | --- | --- |
| HP | 1.5 | 2 | 3 |
| Attack rates | 1.5 | 2 | 3 |
| Flat defense rates | 1.5 | 1 | 1.5; not equivalent to 50% damage reduction |
| Received stance damage | 0.75 | 0.5 | 0.375; approximately 2.67 times the stance work |
| Sight / hearing | 2 / 2 | 5 / 10 | Large detection contributions; actual combination needs observation |

These are not complete NPC stats. Region, boss, journey and other effects matter.
The common NPC selectors have approximately 2.08%/4.17% passive odds at zero runes,
4.17%/8.33% at one rune, and 8.33%/16.67% at seven. Counts of parameter variants do
not establish the distribution of placed enemies. Follower protection, eclipse
conversion and exclusions can override ordinary rolls.

The first-rune step changes more than a small damage number: it increases common
passive odds and admits the ordinary eclipse path in the relevant first-journey
state. Test this transition as a progression milestone. Do not attribute all such
pressure to the crystal that the player has not yet released.

### Eclipse pacing and hardcore

**Author-confirmed and restored:** the six-second initial waits were testing code.
Event 5750115 now uses the intended random waits below, retaining each six-second
alternative as a testing-only comment.

| Great Rune count | Initial random wait |
| --- | --- |
| 1 | 1-180 minutes |
| 2 | 1-155 minutes |
| 3 | 1-130 minutes |
| 4 | 1-105 minutes |
| 5 | 1-80 minutes |
| 6 | 1-55 minutes |
| 7 | 1-30 minutes |

These are initial wait ranges, not guaranteed total intervals between eclipses.
Eligibility, later waits and the kill-dependent 600-second recovery are unchanged.
Ordinary first-journey eligibility still begins at the first-rune condition.
Observe zero-kill and successful eclipses, including the next start, death, rest,
reload and followers. Unconditional recovery remains an unaccepted proposal.
See [implementation verification](MECHANICS.md) for the compiled change. The older
balance-review evidence retains its pre-fix common-event source hash intentionally.

Hardcore should be evaluated with a save that has deliberately broken the crystal.
Preserve the stronger commitment, follower precedence and accepted fresh-choice
NG+ policy. A successful ordinary-mode test does not establish hardcore balance.


Oaths, defense and survival
--------------------------

| Feature | Inspected baseline | Balance question |
| --- | --- | --- |
| Order | 8 HP/s blessing and Golden Vow for 180s | When should it become available, and is its use communicated before it is expected? |
| Golden Order | 12 HP/s blessing and Golden Vow for 180s | Is the upgrade meaningful at its acquisition point without replacing every other package? |
| Golden Vow | 15% outgoing enemy damage correction, 10% incoming enemy reduction; separate PvP values | Test actual coexistence and application, including allies |
| Ordinary Oath cooldown | Effect 263 is 59.9s; not extendable | Distinguish activation frequency from buff duration |
| Sacred Ward | 0.1 incoming correction, 180s expiry, double healing-rate field, damage-removal condition 1 | Verify consumption outside the reactive Totality pose |
| Reactive Totality | HKS with 1626551 checks stamina and can reapply Wrath, blessings and Ward after damage | Establish intended resources and interruption; repeated wards in this state are not automatically accidental |
| Sin / follower | Separate blessing/combat effects and Nemesis protection | Trace the entire package before comparing it numerically with Order |
| Claw / Endure | Distinct 15-FP combined and 9-FP individual branches, plus fallback | Verify acquisition states, resource boundaries and actual parry targets |

Totality requires two tests. First, a ward obtained outside the reactive pose
should be checked against successive hits. Second, the active pose must be tested
with ample, low and exhausted resources. The older guide describes reactive
near-invulnerability; the current HKS reapplication supports that design history.
Neither the three-minute timer nor repeated wards during the pose establishes a
bug by itself. Clarify the intended FP/stamina burden before prescribing a nerf.

Also test Totality with Divinity. Determine whether a protected hit breaks the
undamaged condition and whether resource recovery changes the pose's intended
cost. The author has not yet defined absorbed/blocked-hit semantics for Divinity.


Divinity and the meaning of undamaged
------------------------------------

**Accepted balance model:** preserve buffs while the player remains undamaged.
Maintaining that state is the challenge; an arbitrary fixed short duration is not
the selected limiter. The earlier 15-20-second duration proposal is superseded.
When damage breaks preservation, retained buffs resume their remaining timers;
they are not all removed. The author has now confirmed that basic transition.

The current route supplies duration modifier 1626083, with `extendLifeRate=100`.
Fury 1626063 is marked extendable and supplies the state used to apply Divinity.
This connection can support the intended preservation. It should be tested for
correct interruption, not automatically removed as a feedback-loop exploit.

Other inspected contributions include nominal recovery of 10% max HP/s, 10 FP/s
and 50% max stamina/s while the 0.1-second ticks run; holy protection; and many
instant-action/cancel routes. Fury and Cord add their own effects. These are raw
connected values, not tested final recovery rates or approved numerical targets.
The old guide's flat FP/stamina rates differ from the inspected fields.

| Situation | Required observation / unresolved intent |
| --- | --- |
| Stay undamaged with a short buff active | The buff is preserved according to the confirmed design; measure whether it freezes or merely decays very slowly |
| Take ordinary enemy HP damage | Verify that preservation ends and existing buffs resume counting down; check whether health-based renewal and rapid recovery mask that transition |
| Heal back to full after a hit | Clarify whether Divinity may resume within the same Fury activation or requires a fresh cast |
| Block or absorb a hit with Ward | Ask whether contact without HP loss counts as damage for this feature |
| Take chip, poison, rot, fall or environmental damage | Define which damage sources interrupt it, then test each |
| Pay a self-HP or maximum-resource cost | Define whether voluntary sacrifice interrupts Divinity or is a supported combination |
| Enter/leave Totality or blood power | Confirm intended exclusions and interruption under protection and regeneration |
| Rest, reload, die or change equipment | Confirm whether the state ends, resumes or requires reactivation; distinguish persistence from unlock |

The exact unlock remains a separate question. The inspected catalyst/Cord route
does not contain the old Divine Gate/Miquella/all-runes gates. Do not invent those
gates to offset strong maintenance behavior. Likewise, test the known acquisition
initialization edge case without turning a reload requirement into a design cost.


Exceptional boss counters
------------------------

The author confirms deflection mastery as Malenia's expected answer, denying her
healing. The HKS explicitly toggles six healing effects across 72 attack rows;
all inspected Malenia rows carrying those healing effects are covered. The 2120
attack family has 71 of 81 rows with `isDisableNoDamage=1`, supporting dodge
invulnerability bypass. Test actual windows and both phases before changing this
deliberate encounter identity. Moving outside a hitbox remains distinct from
relying on dodge invulnerability.

For Maliketh, the intended alternatives are mastered deflection or Divinity's
mitigation. All 26 inspected attack rows named Maliketh have the bypass flag.
NPC effect 1926098 multiplies outgoing holy damage by 5; Divinity's incoming enemy
holy correction is 0.1. Those two contributions multiply to 0.5 if both apply;
this is not a final-damage prediction because other scaling and physical damage
remain. It is concrete support for Divinity's intended protective role.

Destined Death's burn 29515 applies 0.2% HP loss per 0.1-second tick for three
seconds; 29521 supplies a 0.8 maximum-HP multiplier for 20 seconds. The former
matches vanilla in all inspected fields; the latter differs only in icon ID.
Do not assume holy negation cancels either effect. Observe direct hits, burn,
maximum-HP loss, regeneration and buff-timer resumption separately. These findings
use the [recorded static evidence](balance-review-evidence.json), not completed
boss tests or proof that no other strategy can win.


Ultimates and weapon balance
---------------------------

### Shared charge rule and Obliterator

**Confirmed:** Obliterator earns ultimate charge like the others. The current
resident 287 bypass is a known implementation mismatch. A future fix should use
the existing charge mechanism and verify its consumption/recovery before adding a
second cost system. A new recurring FP fee or fixed long cooldown is not currently
the selected solution.

Harness Void Eye (Ash of War 660) costs 45 FP and its `a660:40000` animation applies
1626770 at about 1.27 seconds. That 60-second weapon buff supplies +100 magic and
+100 lightning attack-power fields and state 7750. The HKS requires this state
for Obliterator's ultimate, alongside shared full-charge state 7588 and cooldown
checks. Without the buff it selects the weapon's buff action instead of the beam.

The beam fires through behavior 300000869 and bullet/PC attack 4620221. Inspected
fields are 300% weapon corrections, 500 magic base attack and 750% stance correction.
The ultimate refreshes Void Eye 1626770; the initial skill costs 45 FP and that buff
lasts 60 seconds. The agreed charge fix preserves that refresh and the Ash of War
prerequisite. Any later damage or refresh adjustment is a separate balance decision
after normal earned charging is working.

Ultimate timeline `a984:32400` applies shared reset 276 at about 0.17 seconds,
fires the beam at 0.50 seconds and reapplies Void Eye at 0.67 seconds, without a
hit-confirmation requirement. It also uses
the shared in-progress marker 288 and one-second cooldown 289. Reset 276 returns
the meter to starting effect 277. This is consistent shared-system plumbing;
resident full-charge 287 on the weapon defeats the intended earned frequency.
Godslayer also has a weapon-buff prerequisite in `ModUltimateAttackConditions`,
so requiring Void Eye is not itself inconsistent with the other ultimates.

After charge is earned and spent correctly, compare the complete beam against
other earned ultimates. A damaging late-game reward may be appropriate. Do not
judge its intended burst using the frequency of the testing bypass.

### Per-weapon questions

| Weapon | First measurement | Preserve while evaluating |
| --- | --- | --- |
| Obliterator | Meter before/after use, reuse after a miss, buff refresh, total beam damage and stagger | Earned gravity/beam identity and existing ordinary moves |
| Stormblessed | Melee plus wind hit count, final stance burst and repositioning | Mobility, wind coverage and distinct one/two-handed specials |
| Blasphemous Blade | Ravenous stacks spent, HP-dependent branch, explosion plus melee, healing and stance | Blood expenditure and earned stacked burst |
| Godslayer | Black Flame/Soulflame availability, Heresy coexistence, critical and kill rewards | Build-up into a short powerful Soulflame state |
| Black Blade | Actual pulse count, percentage-HP overlap, awakened versus sustained state | Destined Death's intended late-game role |
| Sacred Spear | Ritual burst and the following Supremacy combat period, rescue consumption | Alternative blood package and its holy-buff exclusions |
| Great Stars | Actual connected ultimate strike/effects and healing, both target sizes | Heavy, blood-themed impact rather than a name-based assumed payload |

The [earlier attack review](BALANCE-REVIEW.md#ultimates-and-added-attacks) contains
the detailed selected rows. Numerical nerfs there remain trial candidates. Several
connected Godslayer and Black Blade attack fields match vanilla even though their
choreography and surrounding effects differ. Nearby rows with custom names are
not automatically the attacks being executed.

For each attack measure total HP damage, target-size sensitivity, stance damage,
status application, recovery/commitment, healing and repeat frequency. Compare
ordinary specials separately from earned ultimates. A reliable crouch attack and
an earned finisher have different purposes.


Buffs, afflictions and economy
-----------------------------

Blasphemy/Supremacy combine offensive power, resource recovery and a consumed death
rescue. Supremacy's current 1.6 attack rates, 3% resource recovery per second and
180-second duration are substantial, but its exclusion of holy blessings is part
of the package. Divinity preserving it during undamaged play is not automatically
a duration defect under the confirmed design. Assess the rescue, hit interruption
and practical upkeep together before selecting a shorter duration.

Afflictions and items must be measured with those recovery tools. An HP-change
trigger can behave differently under many small regeneration ticks than under
occasional flask use. Low-health blood attacks can cross Dragonrot/Bayle thresholds.
Maximum-resource stacks can change how thresholds are computed and presented.

| System | Balance data to establish |
| --- | --- |
| Dragonrot | Actual thresholds by rune/curse stage, ticks, suppression, warnings and interaction with healing |
| Frenzied Flame | Trigger opportunities per HP-change pattern, stage burden, treatment and restoration on Needle removal |
| Bayle curse | Eligibility, warning, lethal trigger and supported prevention |
| Fury casting | Maximum-resource cost stacking, repeated-cast counters and severe self-damage conditions |
| Great Runes | Exact active/passive coexistence and the increased opposition unlocked at each milestone |
| Giant's Flame potency | Initial burst, depletion, recharge, affected spells and reset behavior |
| Consumables | Recipe/merchant access, supply rate, resource restoration and per-rest limits |
| Grace | Which enemies and effects persist, what refills, and whether reloading offers a different economy |
| Armor and shields | Conditional bonuses, transformation eligibility, protection resources and mobility tradeoffs |

These features are included in [DESIGN.md](DESIGN.md) even where exact current
numbers still need inspection. Their older guide values must not become tested
balance targets merely by being copied into a new document.


Evaluation and change records
-----------------------------

Use the existing [manual test matrix](../TEST-MATRIX.md). Do not create a parallel
set of claimed passes. Store real observations under `docs/test-results/` with the
build/receipt, game version, journey, save progression, level/attributes, equipment,
upgrade level, active effects and input configuration.

Test representative opening, middle and late-game builds with the tools expected
at that point. Include a simple build using Order and a deliberate advanced
combination. Compare ordinary and Nemesis encounters, humanoids and large targets,
and ordinary versus released hardcore states. Record several representative
attempts rather than only the best result.

Use a small change record when tuning is actually proposed:

```text
Feature and intended role:
Observed problem, build and save:
Connected source / parameter / animation IDs:
Current behavior and relevant interactions:
Proposed change and reason:
Author decision: open / accepted / declined
Implementation: unchanged / changed, with build reference
Observed result and remaining questions:
```

Document an accepted design change when it happens; do not manufacture approval
from this template. Routine fixes within an already authorized scope still follow
the existing workflow. Parameter/HKS/event changes require the appropriate source
handoff and gameplay checks; documentation alone needs link and whitespace checks.

The basic Divinity damage-break rule and the two exceptional boss counters are
established. The author's intended eclipse waits have now been restored and
compiled; game timing remains untested. Next work is targeted observation of the
counters and Totality's resource burden, and a gameplay task to correct
Obliterator's confirmed charge mismatch. Acquisition and per-weapon measurements
remain open. The eclipse change has not been deployed or published.
