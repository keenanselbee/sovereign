Sovereign feature design
=======================

Living design document, established 2026-09-11. Sovereign's author designed its
custom mechanics and is the authority on their intent. This document records that
intent alongside implementation evidence; it does not make every current value or
earlier recommendation an approved design decision.

Use [BALANCE.md](BALANCE.md) for numerical baselines, tuning questions and evaluation.
Use [MECHANICS.md](MECHANICS.md) and its linked investigations for implementation
proof. The [older player guide](../README.md) contains valuable design history but
also outdated names, unlocks and values.


Design foundation
-----------------

**Confirmed by the author:** Sovereign is balanced around using Oaths and the
powerful tools available to the player. Its difficulty is deliberate. The opening
can nevertheless be excessively difficult, particularly with Nemesis enemies.
Releasing Nemesis through the crystal starts the deliberate hardcore mode.

The design task is to preserve this demanding game and its extraordinary rewards
while making the intended tools, commitments and counters understandable. Strong
effects are not automatically defects. Balance changes must account for how the
author expects a feature to be acquired, activated and maintained.

The author describes the intended opening as **challenging**. The timing of the
first Oath and exact recovery/difficulty targets remain open. An earlier Oath award
and lower starting multipliers are proposals, not accepted changes. Restoring the
intended eclipse waits is separately confirmed below. There is no accepted new
difficulty-menu design.

Reading the feature sections:

- **Confirmed intent** means the author explicitly established the behavior.
- **Implementation evidence** means a connected code/data path was inspected. It
  does not mean that an actual game test passed.
- **Legacy description** means an earlier guide describes the feature; its current
  details or continued intent need confirmation.
- **Open** identifies a design choice or verification gap without filling it with
  an invented answer.

Descriptions of a feature's likely role are working interpretations unless marked
as confirmed intent. A source mismatch can require a code fix, a documentation fix
or clarification; it does not automatically authorize redesign.

**Working completeness assessment:** assuming the connected mechanics function as
intended, Sovereign is broadly feature-complete as a gameplay overhaul. The review
has not identified a missing major combat system that requires expansion. The
larger remaining design questions concern teaching essential tools, acquisition
and power progression, and clear consequences for optional commitments. This is
an architectural/design assessment, not a claim of full content verification or
release readiness. The proposed Hadeon entry seal refines an existing encounter.


Combat and controls
-------------------

### Deflection and active defense

**Implementation evidence:** player HKS has custom deflection animations selected
by attack direction, guard damage and weapon/hand configuration. Deflection also
feeds the ultimate charge system. The stronger-deflect marker advances two charge
steps; the ordinary path advances one. These connect defense to the opportunity to
use a powerful attack.

The older guide presents precise blocking as a core mechanic available without a
special tear. The author confirms that deflection mastery is the expected answer
to Malenia, denying her healing, and one intended answer to Maliketh. Current HKS
and attack parameters support these roles; see Exceptional bosses below. Attack
variants and timing still need game tests. This does not make every boss attack
subject to the same rules.

Sources: [player HKS](../mod/action/script/c0000.hks), `ModDeflectAnimation`,
`ModDisableMaleniaDeflectLifesteal`; [common events](../src/events/common.emevd.dcx.js),
5750015 and 5750043. Balance dimensions are timing, stamina, stagger, recovery,
weapon differences and contribution to ultimate charge, not HP damage alone.

### Special attacks and ultimates

**Confirmed intent:** Obliterator should earn its ultimate like the other weapons.
The author recalls its permanent full-charge effect as likely beam-testing setup
and reaffirmed removing that bypass. Preserve Harness Void Eye, its buff
prerequisite and the beam's buff refresh in that fix. The charging change is still
pending; the intended rule is settled.

**Implementation evidence:** common event 5750015 advances meter effects 277-287
through ten steps using trigger 101990. Kills feed that trigger through 5750018.
The player functions `ModUltimateAttack` and `ModUltimateAttackConditions` select
the input/animation path and weapon-specific buff prerequisites. Weapon 23085000
currently supplies resident effect 287, bypassing ordinary charging. Removing that
bypass is a future gameplay task, not completed by this documentation.

The older universal thirty-second cooldown description is not the current meter
design. Separate the charge meter, one-second effect 289, animation commitment,
weapon prerequisites and any skill cost. A whole move can contain melee contacts,
conditional projectiles and effects; its displayed name does not identify all of
its damage sources.

### Quick actions and input configuration

**Implementation evidence:** the current HKS sets `swapL1L2Inputs=TRUE` and
`leftHandChangeDisabledLanternEnabled=TRUE`. Consequently older literal controller
combinations are not a reliable universal reference. Document the action first and
verify its mapping with the selected configuration.

| Action | Current or historical role | Evidence boundary |
| --- | --- | --- |
| Oath activation | Apply the equipped Oath package | Action + L3 branch in `ExecWeaponChange`; requires readiness and matching equipment state |
| Weapon ultimate | Spend earned readiness on the weapon's special action | `ModUltimateAttack`; current L1/L2 swap changes the combination |
| Crouch attack | Access distinct one/two-handed weapon moves | HKS plus the selected weapon timeline; older guide uses L3 + R1 |
| Endure / Claw | Stationary defensive action replacing the ordinary backstep path | Connected FP/state branches described below |
| Quick shackles | Bring acquired utility/blood abilities into the normal input set | Legacy combinations need current input verification |
| Quick gestures | Access Totality and Rapture without navigating the gesture menu | Distinguish these actions from the equipped Oath package |
| Lantern | Toggle an acquired lantern through the replacement hand-change input | HKS configuration and lantern branches |
| Quick buff | Consolidate eligible buffs through Numen's Runes/Rune Arcs | Legacy feature; current item-to-effect eligibility needs its own complete trace |

Before changing a shortcut, evaluate one/two-handed use, alternate input settings,
movement, insufficient resources and conflicts with ordinary actions. Accessibility
here includes discoverable controls, not just lower damage.

### Endure and Blasphemous Claw

**Confirmed intent:** preserve the author's heavily modified Claw mechanics unless
evidence establishes something clearly broken. The author will test the mechanics.

**Implementation evidence:** `ModEndureBlasphemousClawBackstep` handles Endure and
Claw states, with a combined branch at 15 FP, individual branches at 9 FP and an
Endure fallback. Effects 1626601/1626602 and 1626624 lead to the current defensive
state. Animation `a00:50510` has connected attack/parry and bullet paths at about
0.333 seconds. Historical dangling effects are not the entire implementation.

The intended parry targets, low-FP behavior and timing should be documented from
the author's tests. Do not restore an obsolete effect chain simply because it
exists in a backup. See [MECHANICS-REVIEW](MECHANICS-REVIEW.md).


Oaths and allegiance
--------------------

### Order and Golden Order

**Confirmed intent:** Oaths belong to the expected toolkit for Sovereign's difficulty.
The exact time at which the player should obtain the first Oath remains open.

**Implementation evidence:** Radagon's/Marika's Scarseals select Order;
their Soreseals select Golden Order. Common event 5750011 applies the corresponding
package and 5750012 manages the approximately one-minute cooldown.

Radagon's Scarseal is the plausible first Order on a southern exploration route:
the Weeping Evergaol boss reward. Radagon's Soreseal instead supplies the stronger
Golden Order and is a Fort Faroth pickup, allowing an informed dangerous detour.
The corresponding item lots 1042330100 and 1051390060 match the inspected vanilla
lots in every field. This establishes unchanged rewards, not measured acquisition
time or unchanged encounter difficulty. See [opening access](BALANCE.md#opening-and-ordinary-encounters).

Order combines Blessing's Boon with Golden Vow. Golden Order upgrades the healing
to Blessing of the Erdtree. The observed main buffs last 180 seconds, so the cooldown
is an activation limit rather than an intended demand for downtime every minute.
The seals' current tradeoffs are customized, including holy-specific modifiers;
do not substitute their vanilla all-damage penalties.

Acquisition, the first activation hint, equipment requirements, ally application,
stacking exclusions, unequip behavior and persistence should all be part of the
player-facing explanation. The exact ally coverage remains a game-test question.

### Totality and Sacred Ward

**Implementation evidence:** Perfect Runeseal 6900 enables Totality. Goldmask's
dialogue awards it alongside the gesture when told that Radagon is Marika; existing
saves have a recovery award. This is distinct from claiming an all-runes unlock.

Sacred Ward 1626563 has 90% incoming damage-reduction fields, a 180-second expiry,
increased healing and `deleteCriteriaDamage=1`, matching the Bubbletear's removal
setting. Its untouched duration does not establish continuous protection.

There is also a **separate reactive Totality state**. In the damage handler near
line 6472, effect 1626551 causes the HKS to check current stamina. With stamina
remaining it reapplies the pose effect, Wrath, blessings and Sacred Ward; at zero
stamina it applies 1626575. Common event 5750060 contains the associated ward/retaliation
worker. Reapplication during this pose must not automatically be called an exploit.

**Legacy description:** Totality is a defensive gesture that reacts to attacks with
Wrath and Ward, consumes resources and can be interrupted by sufficiently strong
attacks. The old guide emphasizes FP; the inspected HKS explicitly checks stamina.
Animation `a00:80960` applies the Oath trigger at about 1.60 seconds and initial
Wrath 1626558 at 1.77 seconds. Its behavior 2511 has a 57-stamina cost; reactive
Wrath behavior 2512 has zero listed stamina cost. These fields do not establish
the full pose's resource drain. The old 40-FP explanation is not verified by this
trace. Complete costs and interruption still need a game test. Test the passive
bubble and reactive pose separately, including [Divinity interactions](BALANCE.md#oaths-defense-and-survival).

### Sin, Bindseal and the Nemesis follower

**Implementation evidence:** Aberrant Bindseal 6800 supplies the Sin Oath state and
follower role. The equipment has stamina-recovery and casting-speed benefits.
Follower protection takes precedence over forced Nemesis conversion and hardcore
role selection. Removing the seal restores the appropriate ordinary or released
hardcore state; current removal consumes the seal and the ritual can replace it.

The acquisition rite requires Hadeon's defeat, the shrine ritual area, a living
player and absence of the seal. Crystal destruction is not required. The old
description of Dejection anywhere granting a Malefic Woundseal is not the current
route. Oath of Sin has its own blessing and combat interactions; its complete
numeric package remains to be catalogued before treating it as equivalent to Order.


Enemy difficulty and Nemesis progression
---------------------------------------

### Ordinary difficulty, random encounters and eclipses

**Confirmed intent:** the opening should be challenging, even before the optional
release of Nemesis. Exact early access and difficulty targets are under discussion.

**Implementation evidence:** enemy `SoulDropUp` applies the base modifier and rolls
for Nemesis using progression-dependent odds and NPC selectors. Ordinary passive
Nemesis can appear before crystal release. Common event 730 sets the Great Rune
count flags used by those odds. Timed eclipse event 5750115 is another escalation:
eligible nearby enemies can be converted during an onslaught.

These should be described as distinct layers: base difficulty, random enhanced
enemies, timed onslaughts and persistent crystal hardcore. The older enemy tier
names do not by themselves prove the full numerical scaling of every enemy.
NPC selectors, region scaling, detection and stance resistance matter too.

The author confirmed that the six-second initial eclipse waits were for testing.
The intended progression-dependent waits are restored, with testing alternatives
retained as comments; see [current timings](BALANCE.md#eclipse-pacing-and-hardcore).
Success-dependent recovery is unchanged and still needs evaluation.
State clearly what alerts the player, how an onslaught ends, how rewards are earned
and what recovery follows failure as well as success.

### Hadeon, the shrine and crystal release

**Author-confirmed location and latest design direction:** Nemesis is sealed in
the Stranded Graveyard starting dungeon. Replace the earlier optional key-triggered
proposal with keyless access and a mandatory Hadeon encounter tuned for a new
character using deflects. The exit barrier and local fast-travel prohibition last
until Hadeon's defeat. Barrier lifetime already matches; keyless access, travel
gating and new-character tuning are under investigation, not implemented by the
design review. See [the revised implementation plan](HADEON-SEAL-PLAN.md).
Preserve crystal destruction as the separate hardcore decision after Hadeon.

**Further direction, 2026-09-19:** make deflection the intended new-character
solution and increase Nemesis assistance as Hadeon weakens. Percentage HP loss on
an arena fall/return is under consideration. The [combat investigation](HADEON-ENCOUNTER-REVIEW.md)
records existing blessings, distinct recovery paths and a proposed attrition loop;
its numerical prototype is not an accepted runtime change.

**Confirmed intent:** releasing Nemesis starts hardcore. The existing accepted
implementation uses destruction of crystal entity 18002346 after Hadeon as the
persistent choice. Following Nemesis suppresses that state; leaving the follower
state restores it when the crystal has been broken.

Hadeon is the shrine encounter that gates the rite and crystal access. His defeat
and reward are separate persistent states. The owed reward should survive an
interrupted payout, while an already collected reward should not duplicate.
Erdtree's Favor +3 is the inspected reward, not the Bindseal itself.

The accepted journey policy is a fresh Hadeon/crystal choice in NG+, with no forced
automatic hardcore transition. Runtime tests for flag reset, active enemies,
follower transitions, host/client ownership and crystal targeting remain pending.
See [NEMESIS-PERSISTENCE](NEMESIS-PERSISTENCE.md).

### Exceptional bosses

**Confirmed intent, 2026-09-11:** Malenia is defeated through mastery of deflecting
her attacks, which should award her no healing. Maliketh and Destined Death are
intended to demand deflection mastery or Divinity's protection against the extreme
damage. Preserve those encounter identities when evaluating accessibility.

**Implementation evidence:** `ModDisableMaleniaDeflectLifesteal` replaces the healing
effect in 72 listed NPC attack rows with -1 while deflect marker 102001 is present,
then restores the effects. All inspected Malenia rows carrying one of those six
healing effects are covered. In the 2120 attack family, 71 of 81 rows set
`isDisableNoDamage=1`, supporting the author's recollection of attacks bypassing
dodge invulnerability. Do not translate this into an assertion about every attack
variant or the impossibility of moving outside an attack's reach.

All 26 attack rows named Maliketh in the inspected 2110 family also set that bypass
flag; Beast Clergyman rows are distinct. Maliketh's NPC effect 1926098 supplies
`atkEnemyDmgCorrectRate_Dark=5`; Divinity 1626080 supplies incoming enemy holy
correction 0.1. Elden Ring uses these Dark fields for holy damage. This supports
Divinity as a substantial counter to the holy component, not complete immunity.
Destined Death also applies HP burn 29515 and, on relevant attacks, maximum-HP
reduction 29521. Their behavior must be checked separately from direct holy damage.

These are static findings stored in [parameter evidence](balance-review-evidence.json).
Live deflect timing, both Malenia phases, Maliketh's individual hit types, Divinity
interruption and the older full-HP phase-two claim still require game observations.
The author's intended answers do not establish that every other possible build
has been proven incapable of winning.


Great Runes and permanent progression
------------------------------------

**Implementation evidence:** event 5750010 checks owned Great Rune goods and
supplies passive effects. Great Rune progress also changes Nemesis pressure and
Dragonrot thresholds. Acquiring a rune can therefore increase both capability and
risk; evaluate the two sides together.

| Rune | Inspected passive connection | Detail still requiring a complete trace/test |
| --- | --- | --- |
| Godrick | Goods 191 -> 550; +1 to all eight attributes | Active/passive stacking and persistence |
| Rennala | Goods 10080 -> 555; +5 Mind | Acquisition and rebirth interaction |
| Radahn | Goods 192 -> 561; 1.2 equip-load rate | Interaction with equip-load talismans and active effects |
| Morgott | Goods 193 -> 565; +5 Faith | Active holy, rune-loss and resistance package |
| Rykard | Goods 194 -> 570; kill event 5750018 applies 571 | Resource-stack size, lifetime and maximum effective stack |
| Mohg | Goods 195 -> 575/576 and follow-on 577 | Bloodloss trigger, affected attacks and duration |
| Malenia | Goods 196 -> 580/581 | Attack stamina, consecutive-hit and recovery interactions |

The older guide says restoration at a Divine Tower unlocks passives. The current
worker checks particular item IDs, so verify which restored/unrestored items those
are before changing that instruction. Values for the active rune packages in the
README remain historical until their connected rows are checked.


Dragon Communion, afflictions and transformation
-----------------------------------------------

### Communion and crafting

**Implementation evidence:** event 5750030 applies progression effects according
to communion flag 9433 and owned spell goods. It is not simply a counted callback
for each heart consumed. Event 3080 sets 9433 from the communion purchase-flag
count. The later recipe workers are 5750035/5750036.

The connected catalyst route is Dragon Communion Seal plus Ancient Dragon Heart,
through Profane Tome [1], to Elderblood Communion Seal; then Elderblood Communion
Seal plus Staff of the Great Beyond, through Profane Tome [2], to Staff of the
Sovereign. Recipe and item IDs are detailed in [the acquisition review](BALANCE-REVIEW.md#connected-acquisition-route).
The older automatic Formless/Elderblood/Ascension Sigil upgrade account is not the
current demonstrated implementation.

**Legacy description:** consuming dragon and ancient dragon hearts grants Arcane
and increases communion power, while acquiring curses. Precise per-heart bonuses,
limited spell uses and reset rules need a complete progression audit. Avoid using
the old eight-incantation catalyst rule to conflate the separate advanced-curse
threshold with crafting requirements.

### Dragonrot, Frenzied Flame and Bayle's blood

**Implementation evidence:** event 5750031 initializes greater-curse markers from
eight communion flags or specific advanced incantations. Event 5750032 combines
communion state, rune count, HP markers and suppression states to apply Dragonrot.
Frenzied Flame flag 9431 and Needle effect 1626700 affect suppression. Event 5750033
handles the separate Bayle curse.

The HKS `ModFrenziedFlameCurse` rolls when the HP-state update runs, using different
denominators for different curse stages. This matters when considering rapid
healing ticks and repeated HP changes. The older guide's "small chance on any HP
change" is a useful design description, not a measured per-second hazard rate.

Fatesever Needle event 5750041 remembers prior Frenzied Flame state and toggles
suppression/restoration when the effect is equipped or removed. It should not be
described as permanently curing every underlying acquisition flag. Death, reload,
unequip and ending-related flags need explicit testing.

**Working role:** these systems make acquired power costly and interact with
low-health blood builds. Confirm how often the author intends forced intervention
and whether suppression is a build choice or an expected eventual upgrade. Exact
thresholds, tick damage, warnings and treatment should be documented together.

### Sovereign Fury

**Implementation evidence:** the catalysts supply different Fury skill routes.
The inspected Fury effects increase maximum resources, change movement and defense,
and support lightning interactions. Player movement/roll/jump multipliers include
1.2 for Sovereign, above the three Dragonbolt levels.

Effect 1626049 supplies a 0.97 maximum HP/FP/stamina rate for 600 seconds as the
casting cost. The maximum effective stacking of that cost needs an explicit test.
The airborne route also tracks repeated casts through 120-second effects and can
select progressively more severe self-damage branches. Raw branch odds do not
establish unconditional observed death probabilities.

### Divinity

**Confirmed intent, 2026-09-11:** the author wants Divinity to **preserve buffs for
as long as the player remains undamaged**. Extended enabling Fury and accumulated
buffs are therefore not, on their own, unintended exploits. A fixed short duration
would change the intended reward and is not the selected design.

The author further clarifies that taking damage ends preservation: existing buffs
remain with their remaining duration and start counting down. Damage should not
be described as stripping all those buffs. This basic rule is settled; only its
implementation and special damage cases remain to verify.

The feature rewards reaching and maintaining an exceptional state. Its loss
condition is part of its balance. Whether "undamaged" means any HP loss, an enemy
hit, self-inflicted costs, blocked hits or a broken bubble remains to be clarified.
Do not silently choose those edge cases.

**Implementation evidence:** Staff of the Sovereign, its airborne Fury, equipped
Entwining Umbilical Cord and health conditions form the connected activation route.
Common events 5750080/5750081 and `a746:40030` link into Divinity 1626080.
Effect 1626083 supplies duration modification with `extendLifeRate=100`.
Fury and several other buffs are extendable; the ordinary Oath and ultimate
cooldown effects are not.

The player HKS supplies instant-action/cancel routes, and the effect supplies rapid
resource recovery and holy protection. These are the current implementation's
contributions, not a fully accepted numerical target. Test actual timer preservation
and damage interruption rather than requiring the timer to expire during perfect
play. The HP marker 239 represents the top HP band; the parameter applier also has
threshold 99. Marker presence alone is not proof of exactly full health.

Event 5750081 continually reapplies the health-conditioned applier while Fury,
Cord and the HP marker are present. The inspected Divinity chain has no explicit
damage-removal setting or separate hit latch. Rapid healing may therefore renew
the state after a hit; a small hit may not cross its HP threshold. Verify the
intended timer resumption in game before calling this an interruption defect.

The old Divine Gate/all-Great-Runes/Miquella unlock story is still an **open intent
question**: it is not present in the connected activation checks. The normal staff
materials nevertheless require advanced progression. Separate the desired unlock
from the confirmed undamaged-maintenance rule.

The Cord is acquired through the custom GEQ's Grave transforming encounter and
item lot 6100. Its current effect also increases all five attack rates; the old
Godslayer-only description is incomplete. Its interaction with armor identity and
other Soulflame tools requires separate verification.


Blood power and signature weapons
---------------------------------

### Rapture, Blasphemy and Supremacy

**Legacy description:** Rapture and Mohg's Shackle use the player's blood to unlock
an alternative power package, replacing holy blessings. The low-health cost,
explosion and death rescue are deliberate parts of that identity in the guide.

**Implementation evidence:** Blasphemy/Supremacy effects 1626360/1626370 combine
attack bonuses, resource recovery and a chain that removes blessings, Vow and Ward.
`ExecDeath` has separate rescue branches and applies 1626367 to consume the buff.
Supremacy is also applied by the Sacred Spear's ultimate. Record duration,
exclusions, trigger, rescue and post-rescue state as one feature, rather than adding
its attack bonus to a hypothetical stack with every Oath.

The desired strength and duration are open. Divinity's confirmed preservation
design changes how sustained-buff tests should be interpreted; long duration during
undamaged play is not sufficient evidence to weaken Supremacy.

### Weapon identities and acquisition

The roles below synthesize the old authored descriptions and connected paths.
Exact numerical targets remain in [BALANCE.md](BALANCE.md) and the linked review.

| Weapon | Feature identity and resource relationship | Current evidence / remaining boundary |
| --- | --- | --- |
| Stormblessed Zweihander | Mobile wind weapon with different crouch moves, a weapon blessing and a broad ultimate | Category 979; connected wind/melee ultimate. The old grave acquisition and exact blessing cost/duration need end-to-end verification |
| Blasphemous Blade | Blood expenditure and stored Ravenous Bloodflame produce different lunges, somersaults and explosions | Category 980, variation 200; connected main ultimate burst and conditional effects. Validate stack use, HP-dependent branches, healing and seventh-stack prerequisite |
| Godslayer's Greatsword | Low base strength compensated by Black Flame, short Soulflame windows and Heresy | Category 981; buff-gated ultimate and distinct shockwave branches. Validate refresh, critical reward and which Heresy effects coexist |
| Maliketh's Black Blade | Sustained Destined Death with a stronger awakened opening and multiple delivery methods | Category 982, variation 408; buff-dependent attacks and repeated projectiles. DoT stacking, awakening and phase expectations need tests |
| Mohgwyn's Sacred Spear | Blood ritual and Supremacy transform an ultimate into a broader combat state | Category 983; connected ritual and self-buff. Account for exclusions and consumed death rescue |
| Fallingstar Obliterator | Earned late-game gravity weapon with a required Void Eye buff and charged beam ultimate | Category 984; **author confirms earned charge**. Current resident full charge is a mismatch. Other ordinary/special paths remain for the author's tests |
| Great Stars | Heavy blood-themed strike, special smash and healing interactions | Motion category 35, variation 1200. Verify the actual ultimate contacts and effects rather than assuming a similarly named parameter row is selected |

Obliterator's Harness Void Eye costs 45 FP and supplies a 60-second weapon buff
with +100 magic and +100 lightning attack-power fields. The beam requires that
buff and shared full charge, resets the meter during its animation and refreshes
Void Eye without requiring an enemy hit. Without the buff, the ultimate input
selects the buff action instead of the beam. Its use of shared charge/reset and
cooldown markers is consistent with the ultimate system; the resident full-charge
effect is the mismatch. See [the complete sequence](BALANCE.md#shared-charge-rule-and-obliterator).

Obliterator's accepted forging route requires Godskin Duo and all three base-game
Fallingstar Beasts in the current journey. Hewg supplies the hint, smithing
presentation and reward. The later memory-loss stages retain an abbreviated
handoff; the original farewell remains independent. One reward per journey and
interrupted delivery require game tests. Do not substitute unused ingredient IDs
or a DLC beast for this accepted route. See
[GAMEPLAY-CORRECTNESS-UPDATE](GAMEPLAY-CORRECTNESS-UPDATE.md).


Spells, equipment and consumables
---------------------------------

### Dragonbolt and offensive magic

**Confirmed intent:** the author's Dragonbolt modifications should be preserved
unless clearly broken. Do not rebuild the old vanilla spell to match its name.

**Implementation evidence:** Betrayer's Dragonbolt has an independent self-buff,
movement changes and separate friendly/opposing-target effects. Magic 2006910,
behavior 300000089 and bullets 210691000/210691001 connect those paths. The self
effect lasts 180 seconds; the inspected target effects have 90-second durations.
The missing historical effect is not the only route to the gameplay. See
[MECHANICS-REVIEW](MECHANICS-REVIEW.md).

The HKS defines Dragonbolt, Vyke and Betrayer movement/roll/jump multipliers of
1.05, 1.10 and 1.15 relative to the global settings. Exact stamina recovery must be
measured rather than copied from the old guide.

| Magic family | Legacy feature description | Current documentation boundary |
| --- | --- | --- |
| Fireball incantations | Larger charged explosions and longer range | Trace each projectile and charge variant before assigning shared multipliers |
| Fire Giant incantations | High initial power spent down by casting and restored over time | Common event 5750055 has potency stages; exact bonuses, recovery and exceptions need full parameter tracing |
| Flame of the Fell God | Larger area/range at greater cost | Legacy values require current confirmation |
| Dragon Communion | Powerful casts with stamina/limited-use economics | Confirm spell-specific use limits and rest reset; do not generalize to every dragon-themed spell |
| Ancient Dragon Communion | Hunting, hearts and altar unlock advanced spells | Current crafting progression is distinct from the older automatic upgrades |
| Elderblood Greatbow | Anti-dragon and anti-healing spell | Event 5750036 sets availability flag 1055420220; old three-spell rule needs reconciliation |
| Blessings and fortifications | Longer useful preparation windows | Separate inspected Oath components from other unreviewed spell durations |

### Armor, shields and talismans

**Implementation evidence:** Black Scaled conversion qualifies when at least one
original piece is equipped at death during either Rykard phase or at his final
defeat. It replaces carried originals one-for-one, preserving altered body armor
and quantities. Red, white and gold paths apply effects rather than using that
same inventory conversion. Existing fully defeated saves do not begin a new
conversion through this event.

The older Dragonlord's Plate description associates armor pieces with low-health
Fury, offensive families and crouch utility, and describes the Cord as an appearance
alternative. Preserve those descriptions as design history until the complete
current piece/effect conditions are documented. Cosmetic form and gameplay bonuses
must be tested separately.

Crusade Insignia's missing on-kill connection was restored while preserving the
custom follow-on effect. This is an implementation repair, not approval to change
its balance. Its activation, refresh and expiry remain game tests.

| Equipment | Feature to document | Boundary |
| --- | --- | --- |
| Scarseals/Soreseals | Oath access, holy tradeoff and resource/casting benefit | Custom effects inspected; exact current values supersede vanilla assumptions |
| Perfect Runeseal | Totality access and equipment state | Current Goldmask award inspected |
| Aberrant Bindseal | Follower allegiance and Sin Oath | Current shrine route and role precedence inspected |
| Entwining Umbilical Cord | Soulflame/Divinity eligibility and offensive power | Current acquisition/effect inspected; older narrow bonus wording is incomplete |
| Eclipse Crest Greatshield | Black Sun's Zenith, timed parry/protection, fallback cost | Legacy description; current shield path and resource/failure limits need inspection |
| Moon of Nokstella | Spell capacity and altered backstep interaction | Legacy description; verify both equipment and HKS behavior |
| Arsenal charms | Equipment-load progression | Legacy percentages require current parameter confirmation |
| Fall-protection equipment | Survival under specific fall and status conditions | HKS `IsLandDead`; test the individual effect and mounted state |

### Items and recovery economy

The following features are represented in the older guide. Their recipes, costs,
merchant stock and exact current limits are **legacy descriptions**, not newly
verified release claims:

| Item | Described purpose | Balance relationship |
| --- | --- | --- |
| Rune Arc | Full resource restoration plus Great Rune activation | Availability changes how routinely active-rune power is expected |
| Numen's Rune | Apply eligible Quick Buffs | Convenience must retain the selected package's requirements/exclusions |
| Margit's Shackle | Darkness, buildup relief and temporary curse suppression | Escape/curse management, not just the vanilla boss restraint |
| Mohg's Shackle | Self-blood cost, surrounding blast and blood-buff access | Low-health risk, burst, buildup removal and recovery |
| Opaline Bubblesoap | Consumable bubble and accumulation relief | Survival buffer and supply economy; separate damage consumption from expiry |
| Starlight Shards | FP restoration | Stock/crafting can govern sustained powerful spell use |
| Dragon/Dragonscale Flesh | Temporary maximum-resource stacks with reduced healing | Current-resource gain, long-lived cost and rest limits must be evaluated together |
| Wondrous Physick | Three-charge preparation resource in the guide | Confirm actual charges and refill/reset behavior |
| Leaden Hardtear / Ironjar | Heavy-body protection with movement and elemental tradeoffs | Also interacts with falling, plunging and mounted behavior |
| Stonebarb Cracked Tear | Stance-focused combat window | Evaluate together with enhanced ultimate stance damage |


Exploration, Grace and presentation
----------------------------------

**Implementation evidence:** `ModJump`, `ModPlungingAttackDamage` and `IsLandDead`
contain airborne movement, height-dependent attack effects and conditional fall
survival. There are separate ordinary/heavy plunge effect families and explicit
mounted cases. The older guide's damage ranges and double-jump explanation are
not a substitute for testing each player/Torrent state.

**Legacy description:** Grace preserves defeated enemies and some long-lasting
effects, Melina provides contextual leveling/dialogue, and lava is especially
dangerous. Exact refill, respawn, curse, buff and journey-reset behavior needs
verification. These rules strongly affect attrition and cannot be treated as
cosmetic quality-of-life changes during balance work.

The Torrent appearance menu was integrated from the newer game baseline while
preserving Sovereign's Grace entries. Owned regalia gate alternatives and selection
uses appearance flags. This is compatibility work rather than a new Sovereign
combat reward. Verify appearance, persistence and Grace regressions through the
existing [Torrent update tests](TORRENT-DIALOGUE-UPDATE.md).

Icons, staged VFX, sounds and dialogue communicate charges, curses, allegiance and
temporary power. Their clarity belongs in the design: a player should be able to
distinguish a spent ward, suppressed curse, unavailable ultimate and active
hardcore state. Exact warning/discovery policy remains an author decision.


Open author questions and maintenance
-------------------------------------

The first answers are recorded in [BALANCE.md](BALANCE.md#author-decisions).
Ask focused questions when working on the affected feature; this list is not a
requirement to settle the entire mod before ordinary documentation can improve.

| Topic | Unresolved intent |
| --- | --- |
| Opening | A challenging start is confirmed; when should the first Oath be obtained and explained? |
| Divinity interruption | Which enemy, environmental, self-inflicted and absorbed/blocked damage counts as breaking the undamaged state? |
| Divinity unlock | Keep the current catalyst/Cord route, or retain any of the older Divine Gate/rune/Miquella gates? |
| Totality | What is the intended resource budget, retaliation cadence and interruption rule while holding the reactive pose? |
| Nemesis | Evaluate restored intended eclipse timing, failure recovery and first-rune difficulty jump |
| Hadeon mandatory opening | Keyless access and defeat-gated exit/travel; starting-class tuning, internal retries, mandatory route and early rewards; see HADEON-SEAL-PLAN.md |
| Signature weapons | Each weapon's intended best matchup, weakness and acceptable peak relative to its acquisition |
| Afflictions | Expected management frequency, visible warnings and the role of permanent suppression equipment |
| Rest economy | Which enemies, spell uses, stacks, curses and buffs should reset at rest, reload, death and NG+? |

When the author clarifies a feature, update its intent here and the corresponding
balance entry. Preserve evidence of what the code currently does if it differs.
Keep the earlier review as history, with explicit supersession notes where needed.
Record actual game observations through [TEST-MATRIX.md](../TEST-MATRIX.md), not
by relabeling source inspection as a passed test. Local documentation changes do
not imply that Nexus copy or a deployed package has changed.
