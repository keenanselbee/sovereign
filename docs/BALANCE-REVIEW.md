# Sovereign balance review

Review date: 2026-09-11. **Investigation and proposed tuning only. No gameplay
changes or game-test passes are recorded by this review.**

**Author clarification after this review, 2026-09-11:** the opening should be
challenging; Divinity should preserve buffs while the player remains undamaged;
Obliterator should earn ultimate charge like the other weapons. The fixed short
Divinity-window suggestion below is superseded, and earned charge is the selected
Obliterator direction. See the living [feature design](DESIGN.md) and
[balance decisions](BALANCE.md). Other numerical experiments remain unaccepted.

**Later accepted fix:** the author confirmed the six-second eclipse waits were
testing code. The intended commented ranges are now restored in event 5750115,
with six-second alternatives retained as comments. The eclipse findings and source
hash below remain the pre-fix snapshot; see [current timings and verification](MECHANICS.md).

The later design pass also traced Totality's reactive pose: HKS near line 6472
explicitly reapplies Ward and blessings after damage while its pose/resource
conditions hold. Distinguish that deliberate connected path from a passive ward
failing to be consumed; see [Oaths and defense](BALANCE.md#oaths-defense-and-survival).

Sovereign should remain a difficult game built around Oaths, deflection, unusual
weapons and earned transformations. The strongest improvement would be a smoother
opening and more consistent limits on sustained player power. Increasing enemy
stats to compensate for the strongest available buff would make ordinary builds
less viable and the opening worse.

## Evidence and limits

This review inspected the current repository regulation, player animation binder,
player/enemy HKS, saved event sources, dialogue sources, item lots and crafting
requirements. Parameter values were compared with the installed vanilla regulation;
both have regulation version `11711000`. The selected values and input hashes are
stored in [balance-review-evidence.json](balance-review-evidence.json).

The full temporary native-reader exports are under `.codex-temp/balance-review/`.
They are investigation scratch, not runtime inputs. Existing gameplay edits were
preserved. This is the repository baseline, not proof that a running game or a
published Nexus archive contains these bytes.

Parameter IDs are the reliable references for binaries; binary files have no
meaningful source line numbers. Names can be stale: for example, the connected
Obliterator attack row is still named Lightningbone Arrow. For text, the event and
function IDs below remain useful if line numbers change.

Raw attack power, weapon correction percentages, flat defense, damage reduction,
status buildup and stance damage are different quantities. A 300% correction is
not a measured 300% increase in final HP damage. Projectile branches can share hit
lists or require different states. This report does not add mutually exclusive
branches together or treat every emitted projectile as a guaranteed hit.

## Recommended priorities

| Priority | Finding | Recommended direction | Confidence |
| --- | --- | --- | --- |
| First | Ordinary eclipse initial waits are six seconds; the explicit 600-second recovery depends on earning a kill | Give every ordinary eclipse a recovery period, including failed/avoided ones; replace testing-scale initial waits | Code confirmed; experiential target needs testing |
| First | Base and Nemesis modifiers compound HP, attack, defense, detection and stance resistance | Soften the opening's simultaneous penalties; preserve the crystal's optional hardcore escalation | Values confirmed; exact encounters need measurement |
| Verify | Totality's ward supplies 90% damage-reduction values, a 180-second expiry and damage-removal condition 1 | Keep it if it is consumed on a hit as intended; test consumption and refresh before proposing a nerf | Values confirmed; removal behavior requires a game test |
| First | Obliterator permanently supplies full ultimate charge and its ultimate refreshes its own required buff | Author subsequently confirmed earned charge like other weapons; resolve that mismatch before damage tuning | Connected path and intended charge rule confirmed; gameplay fix/test pending |
| Next | Bloodflame Supremacy combines 60% attack, three-minute regeneration and a death rescue | Shorten its peak window; retain its identity and existing exclusion of other blessings | Connected values and HKS confirmed |
| Next | Divinity combines resource recovery, action cancels and extreme effect-duration extension | Author subsequently confirmed preservation while undamaged; test preservation and damage interruption, not a fixed short duration | Intent and connected path confirmed; game behavior pending |
| Next | Custom attacks combine weapon hits, bursts, status and stance effects | Tune complete moves against consistent targets, prioritizing posture loops and stacked hits | Per-move evidence below; final damage unmeasured |
| Later | Guides describe older unlocks, costs and effects | Reconcile copy with the chosen design after acquisition tests | Several concrete mismatches confirmed |

## Opening difficulty and Nemesis

### What actually stacks

In [enemy HKS](../mod/action/script/c9997.hks), `SoulDropUp` (line 154) adds effect
7360 unless the enemy already has 297000. This happens before the ordinary
golden-eye/Nemesis roll. `ModNemesis` (line 37) separately handles eclipse conversion
and follower protection; both are called by the enemy update path.

| Field | Base effect 7360 | Nemesis 1626950-1626953 | Nominal combined contribution |
| --- | --- | --- | --- |
| Maximum HP | 1.5 | 2 | 3 times the underlying HP |
| All five attack rates | 1.5 | 2 | 3 times the underlying attack rates |
| All five defense rates | 1.5 | Unchanged | 1.5 times flat defense; not 50% damage reduction |
| Received stance damage | 0.75 | 0.5 | 0.375; about 2.67 times as much stance damage required |
| Sight search rate | 2 | 5 | Potentially very large detection increase; validate engine combination |
| Hearing search rate | 2 | 10 | Potentially very large detection increase; validate engine combination |
| Rune reward rate | Unchanged | 3 | Extra reward, with other reward modifiers still relevant |

These are contributions from two effects, not complete enemy statistics. Region,
NPC, boss, journey and other effects still apply. Nemesis also has 0.65 status
damage-rate fields and increased attack deflection power. The four tier rows share
the listed numerical multipliers; four names do not establish four distinct stat
difficulty levels.

This combination particularly punishes weak early weapons: higher HP and flat
defense prolong fights, increased detection makes isolation harder, and reduced
stance damage removes a useful way to control the encounter. Oath healing helps
attrition but does not solve a lethal first hit.

### Passive encounters are present before crystal release

Common event 730 sets flags 180-187 for zero through seven Great Runes
([initializers and worker](../src/events/common.emevd.dcx.js), lines 227 and 1153).
Flag 180 has threshold zero, so the ordinary host starting state normally uses a
240-sided roll, not the function's initial 1000-sided fallback.

| Great Runes | Roll denominator | Selector 5261, threshold 5 | Selector 5262, threshold 10 |
| --- | --- | --- | --- |
| 0 | 240 | 2.08% | 4.17% |
| 1 | 120 | 4.17% | 8.33% |
| 2 | 110 | 4.55% | 9.09% |
| 3 | 100 | 5.00% | 10.00% |
| 4 | 90 | 5.56% | 11.11% |
| 5 | 80 | 6.25% | 12.50% |
| 6 | 70 | 7.14% | 14.29% |
| 7 | 60 | 8.33% | 16.67% |

The exported NPC table contains 3,174 rows carrying 5261 and 1,086 carrying 5262.
These include variants and are **not counts of placed enemies or weighted spawn
frequencies**. Godrick Soldier variants include 5261. The fallback probabilities
before the progression flag is established are 0.5% and 1%; they should not be
advertised as the usual starting chances. Other thresholds and exclusions exist.

Follower protection overrides the roll. Eclipse forces the roll to zero for
eligible tagged enemies, and the ongoing conversion worker has its own eligibility
checks. Thus ordinary random Nemesis, ordinary timed eclipse and crystal hardcore
are three distinct sources of pressure.

### The ordinary eclipse needs a failure recovery period

Event 5750115, line 10998, waits for `(181 || !50)` and eligible role/protection
states. Every one-to-seven-rune branch then waits exactly six seconds. Later random
intervals, area checks and interruptions affect the actual cycle length: this is
not an eclipse every six seconds continuously.

The explicit 600-second recovery at the end only runs when the six-bit kill counter
1055422000 is greater than zero. Event 5750018 increments it for kills while the
unbound role and eclipse are active. Event 5750116 ends the ordinary eclipse and
awards rewards by that count. A player who cannot obtain a kill can miss the long
recovery that a successful player receives. That is the wrong direction for an
opening difficulty curve.

**Proposed first experiment:** retain random Nemesis, make ordinary eclipse starts
roughly 8-12 minutes apart early on, shorten toward 4-6 minutes later, and provide
at least a five-minute quiet period after every resolved ordinary eclipse regardless
of kills. Add a clear warning before conversion. Preserve safe-area, role and
crystal guards. These are proposed playtest values, not a request to restore old
commented waits blindly. Test reload/rest/death behavior so restarting a worker does
not accidentally erase the intended recovery.

### Keep crystal release meaningful

Crystal entity 18002346, defeated Hadeon, event 5750291 and persistent flag
1055420918 lead to common event 5750101 maintaining the Sovereign of War role and
eclipse. Follower protection takes precedence. Keep this intentional hardcore
choice and its existing journey-reset policy; see
[Nemesis persistence](NEMESIS-PERSISTENCE.md).

The Bindseal relief route is currently behind Hadeon's defeat and ritual area
18002377 (event 5750309). It is therefore not an immediate answer for a new player
struggling to begin. Keep the thematic follower commitment, but offer an earlier
way to learn and survive ordinary Nemesis encounters. Do not describe performing
Dejection anywhere as the current acquisition path.

**Proposed opening experiment:** for ordinary early enemies, try base HP 1.25,
attack 1.20, defense 1.00 and received stance damage 1.00; early random Nemesis
then adds HP 1.6, attack 1.35 and received stance damage 0.8. This produces nominal
2.0 HP and 1.62 attack contributions with a 1.25 stance-work multiplier, still a
substantial threat. Keep detection nearer the base enemy instead of multiplying
both search rates aggressively. Ramp ordinary difficulty with progression and
retain a stronger, explicit hardcore profile. Do not apply these reductions to all
bosses or late-game encounters indiscriminately.

An alternative smaller first pass is to change only ordinary eclipse recovery and
early Nemesis attack/stance modifiers, keeping base HP unchanged. Measure this
before deciding whether the broader opening profile is necessary.

## Oaths: accessible core tools, bounded exceptional protection

Accessory 1050/1220 (Radagon's/Marika's Scarseal) supplies Oath of Order;
1051/1221 supplies Golden Order; Perfect Runeseal 6900 supplies Totality.
The equip effects and the player HKS `ExecWeaponChange` route support Action + L3
activation. Event 5750011 selects the corresponding package; 5750012 handles the
roughly 60-second cooldown. Controller behavior still needs game verification.

| Package | Confirmed main benefits |
| --- | --- |
| Order | Blessing's Boon: 8 HP per second for 180 seconds; Golden Vow for 180 seconds |
| Golden Order | Erdtree blessing: 12 HP per second for 180 seconds; Golden Vow |
| Golden Vow component | 15% attack correction against enemies and 10% reduced incoming enemy damage; separate, smaller PvP values |
| Totality | Golden Order benefits plus effect 1626563: 0.1 incoming damage correction in every damage type, double healing-rate field and fall-protection chain; damage-removal condition 1 |

Scarseal/Soreseal tradeoffs have been customized. The inspected equip effects use
holy-specific outgoing bonuses and incoming penalties, rather than the familiar
vanilla penalty across every damage type. Do not recommend avoiding them based on
vanilla assumptions.

The inspected map lots still include Radagon's Scarseal at 1042330100, its Soreseal
at 1051390060, Marika's Scarseal at 12020050 and her Soreseal at 15000800. This is
not an exhaustive starting-inventory audit. Give players a clear, guaranteed early
Order route and an instruction on using it before asking them to fight Nemesis.
An inexpensive early award/vendor option for one existing Scarseal is simpler than
a second difficulty menu or a new parallel buff system.

Perfect Runeseal is awarded in Goldmask dialogue when reporting that Radagon is
Marika: [t112001100.py](../src/talk/m11_00_00_00-talkesdbnd-dcx/t112001100.py),
line 525, and the corresponding overworld dialogue. It is not demonstrated to be
an all-Great-Runes reward. Existing saves with gesture flag 60848 have a recovery
award in event 5750009.

**Do not classify Totality as permanent 90% protection from its timer alone.**
The complete row also has `deleteCriteriaDamage=1`, the same damage-removal setting
as Opaline Bubbletear effect 3507. This supports a consumable ward interpretation.
The 180 seconds can be its unused expiry rather than sustained protection during
combat. State 42 being named HP Recovery does not override that removal field.
With Golden Vow, the nominal incoming factor while both are active is
0.1 x 0.9 = 0.09 before other modifiers, potentially protecting one hit.

Keep this design unless game evidence shows the ward surviving qualifying damage
or being reapplied unintentionally. Test two successive ordinary hits, Oath reuse,
unequip, death and Divinity: duration extension should not restore a consumed ward.
A strong single-hit safety buffer on a roughly one-minute Oath cadence can fit the
intended difficulty well. If it actually behaves as sustained protection, fix its
consumption/refresh first; a 6-10-second peak or 20-25% sustained reduction would be
fallback design alternatives, not a currently justified blanket nerf.

## Divinity: current acquisition and activation

The current implementation does not match the README's older Ascension Sigil,
eight-incantation and Divine Gate/Miquella account.

### Connected acquisition route

1. Common event 3080 sets dragon-communion flag 9433 after at least four flags in
   290500-290999 are set. Event 5750034 waits for 9433 before starting both crafting
   award workers. This is a flag-count check, not an explicit check for eight named
   incantations or all ancient incantations.
2. Profane Tome [1] map lot 13000830 sets 1055420240. Event 5750035 exposes recipe
   33000 through 1055420241. Material set 330000 requests weapon 34080010 (the
   reinforced Dragon Communion Seal ID) and Ancient Dragon Heart goods 22000.
   The recipe produces goods 9160; the event consumes it and awards lot 7000,
   **Elderblood Communion Seal weapon 34100000**.
3. Profane Tome [2] map lot 13000120 sets 1055420245. Event 5750036 exposes recipe
   33005 through 1055420246. Material set 330005 requires **Staff of the Great
   Beyond 33510000 plus Elderblood Communion Seal 34100000**. Goods 9161 is exchanged
   for lot 7010, **Staff of the Sovereign 34200000**. The Great Beyond staff's
   inspected shop route is the Mother of Fingers remembrance shop row 101944.
4. **Entwining Umbilical Cord accessory 6100** comes from item lot 6100. The connected
   custom event is the GEQ's Grave transforming-slime encounter in
   [m60_43_50_00](../src/events/m60_43_50_00.emevd.dcx.js), initializer line 15 and
   events 1055420900/1055420901. It is not an award from the inspected Divinity worker.

The Farum Azula lot names identify the two tome locations as replacements for the
Pearldrake Talisman and Ancient Dragon Prayerbook lots. Actual pickup placement and
the complete material route still need acquisition tests. Enemy lot 450542001 also
contains an item-specific 1055420245 flag; its reachability and category are not
enough here to promise an alternate tome route.

### Activation and persistence

The staff uses skill 656, mapped to sword-art type 146. The airborne skill path is
in `ModJump`, player HKS around line 643. Animation `a746:40030` fires judge 3094 at
about 0.9 seconds; BehaviorParam_PC 300000094 leads to bullet 10705015, which applies
1626061 to its shooter. That cycles into the 60-second Fury effect 1626063.

Common event 5750080 (line 10576) starts the application worker after ownership of
Staff 34200000. Event 5750081 waits for Fury 1626063 and checks HP marker 239 plus
equipped Cord effect 361000. It applies 1626065, whose own conditions include Fury
state 7999 and HP-rate threshold 99. That repeatedly supplies Divinity 1626080.
In practical terms: **own the staff, equip the Cord, use its airborne Fury, and meet
the full/near-full-health conditions**.

No all-Great-Runes, Divine Gate region or Miquella-defeat check appears in this
connected activation chain. The materials already make the normal route advanced,
but that is different from a verified Miquella unlock. Do not add a Miquella gate
solely to make an old guide true; decide whether that remains the intended design.

There is also an initialization edge case: 5750080 ends immediately if neither
seal nor staff is owned when it starts. The common constructor initializes it;
the crafting awards inspected here do not restart it. Test crafting the first seal
and then the staff in one uninterrupted session versus acquiring them and reloading.
A delayed unlock requiring reload would be a workflow bug, not a balance penalty.

After seeing Divinity, 5750080 applies 4301 for the finger-snap day/night worker
5750082. This is not evidence of a separate permanent Miquella unlock flag.

### Why Divinity is so strong

- 1626080 has a 0.1-second interval with 1% HP recovery, 1 FP recovery and 5% stamina
  recovery per tick. Nominal sustained rates are 10% maximum HP, 10 FP and 50%
  maximum stamina per second, subject to refresh and engine tick behavior.
- It supplies a 0.1 incoming holy-damage correction against enemies; underlying
  Fury has separate lightning protection, 1.3 maximum-resource rates and status
  damage-rate reductions. These should not be described as universal invulnerability.
- Cord itself adds 30% to all five attack rates, independently of the Divinity state.
- Player HKS grants many instant-action/cancel routes while state 7997 is active.
- 1626083 uses state 193, Modify Effect Duration, with `extendLifeRate=100`.
  Fury 1626063, Supremacy 1626370, Totality's ward and the ordinary Oath blessings
  are marked extendable. Fury therefore supplies Divinity while Divinity can
  extend Fury: a concrete feedback-loop candidate. Oath cooldown 263, ultimate
  cooldown 289 and Harness Void Eye 1626770 are not marked extendable. The ward's
  damage-removal condition remains distinct from its timer.
- Fury also has a real cost: 1626049 reduces maximum HP/FP/stamina to 0.97 for
  600 seconds. The airborne code escalates the severe self-damage branch on
  repeated casts through 120-second counter effects: 10%, 20%, 30%, 40%, 50%,
  then guaranteed on the later branch. The damage effects carry 75% or 200% HP
  fields with their own condition; these branch odds are not unconditional observed
  death probabilities. Lack of the Cord also selects the severe branch.

**Original recommendation, superseded by the author's undamaged-preservation
decision:** keep Divinity spectacular and late-game, but first test whether
the duration modifier prolongs its own enabling Fury and Supremacy. If it can sustain
itself or other exceptional buffs for excessive periods,
exclude those specific effects from extension or bound that interaction. Do not
weaken every offensive component simultaneously.

The original, now-superseded tuning candidate was a 15-20-second Divinity
window and 2-3% HP recovery per second, preserving mobility and substantial resource
recovery. Keep its initial activation demanding. Prefer a visible instability count
or a predictable recast lock to unexplained escalating death rolls; retain the
blood-sacrifice identity. The author subsequently confirmed that preservation
while undamaged is intended. Test that preservation and its interruption rather
than imposing the proposed fixed duration; see [BALANCE.md](BALANCE.md).

## Ultimates and added attacks

### Shared charging and evaluation

Common event 5750015 advances effects 277-287 in ten steps using trigger 101990;
the stronger-deflect marker 154 advances two steps. Kills feed that trigger through
5750018. Player HKS `ModUltimateAttack`/`ModUltimateAttackConditions` checks an
attack window, readiness, cooldown, hand/input state, and additional weapon buffs
for Godslayer and Obliterator. Current ultimate timelines apply common markers
276/288/289. Effect 289 is a one-second cooldown, not a universal thirty-second
charge requirement.

A strong ultimate is appropriate when earned. Evaluate complete damage, stance
damage, range, protection, setup cost and repeat frequency together. Preserve each
weapon's role instead of giving all seven the same damage number.

| Weapon | Connected evidence | Assessment and first test |
| --- | --- | --- |
| Fallingstar Obliterator | Weapon 23085000 has resident 287. `a984:32400` fires 3869 -> behavior 300000869 -> bullet/PC attack 4620221 at 0.5s. Attack has 300% corrections, 500 magic base field and 750% stance correction. At 0.667s the ultimate reapplies buff 1626770, which lasts 60s; skill 660 initially costs 45 FP. | **Highest ultimate priority:** repeated readiness and refreshed prerequisite threaten the charge economy. Require genuine charge consumption, a per-use FP cost or a meaningful cooldown; choose one primary limiter. Test repetition before touching beam power. If posture remains excessive afterward, trial 350-450% stance correction before a broad damage nerf. |
| Stormblessed Zweihander | `a979:32400` has 60% and 225% melee corrections (300000233/234), with 75% and 600% stance correction. Four wind emissions reference 2647/2648, each with 70% attack correction and shared hit-list settings. | Focus on total stance burst. The four emissions are not four proven independent hits. If a charged ultimate repeatedly bypasses boss play through stagger, trial reducing the 600% finisher toward 350-400%; retain wind coverage and damage initially. |
| Blasphemous Blade | `a980:32400`, weapon variation 200, routes its 3020 emission to 300200020 -> 10215011 -> attack 63011: 1000 fire base field and 100 flat stance damage. It also has melee hits and state-conditioned bloodflame emissions. | **High burst-test priority:** quantify which branches actually land together. Inspect healing, stored bloodflame consumption and posture as well as HP damage. If the single main blast alone trivializes stance, trial 50-60 flat stance damage; do not sum every conditional blast or nerf all shared shackle rows. |
| Mohgwyn's Sacred Spear | `a983:32400` emits the ritual branch and applies 1626370. Supremacy gives 1.6 attack rates, 3% HP/FP/stamina per second and 180s duration. HKS `ExecDeath` consumes the buff through 1626367 and restores `9% maxHP + 160`. Its cycle deliberately removes blessings/vow/ward. | **High sustained-power priority:** this is not merely a damage ultimate. Keep exclusions and death rescue; trial a 20-30s peak or reduce the sustained bonuses. Do not model it as stacking freely with Oath buffs. Test both burst and the next three minutes of combat. |
| Godslayer's Greatsword | `a981:32400` uses the buff-gated 3900 route and ordinary 3901 contacts; variation 300 reaches attack 300800300 (220% correction, 300% stance) and 300800301 (75% plus fire base 60). Those selected attack fields match vanilla rows. Soulflame adds 300 fire for 7s; Heresy rows add 1.05 attack factors. | Keep its setup/reward structure initially. The greater concern is the accumulated buff package and percentage-HP effect overlap, not proof that the main ultimate attack row is excessive. Do not nerf an unchanged attack just because its custom name sounds strong. |
| Maliketh's Black Blade | `a982:32400` selects buff-dependent 80%/90% melee rows and bullets 2323/2324 -> 2321 -> 2322. The pulse attack rows have 45% corrections and 30% stance correction; these fields match vanilla. Custom 1626905 and 6850 have different durations and stacking categories. | Test full-animation repeated-hit count and overlapping DoT, including large bosses, before lowering direct damage. Small per-tick fields can dominate through repeat hits. Preserve the distinct buff states; no demonstrated need for a blanket nerf yet. |
| Great Stars | Weapon remains motion category 35, behavior variation 1200. `a35:32400` uses normal judge 305 -> behavior 101200305 -> attack 1200305, alongside shared ultimate markers. | Do not infer that a row named Great Stars Ultimate is the active route. Measure its actual heavy strike, bloodflame and healing against the other weapons. There is insufficient connected evidence here to prescribe a numerical nerf. |

The Obliterator beam uses a player attack row. It is not simply Astel's unscaled NPC
laser damage transferred wholesale. The inspected NPC laser 4620220 has different
values. Likewise, several Godslayer and Black Blade attack fields still match their
vanilla counterparts even when the surrounding choreography and effects differ.

### Added crouch/special attacks

Godslayer's one-handed special in `a981:30600` emits normal or Soulflame branches at
about 0.567s. The connected bullets use attack rows 62401/62406 with fire base fields
239/279 and flat stance damage 16.8/21.84. Their inspected fields match vanilla Noble
Presence. Nearby custom rows 62410/62411 contain 300/500 fire fields, but their names
alone do not prove this move uses them. Test the actual connected route first.

Black Blade's two-handed special has connected 200% correction/400% stance melee
data at 75312, plus conditional projectiles. Its one-handed branches include
135%/185% correction and up to 400% stance correction. These are posture and safe
repeat-use candidates, especially with DoT, rather than a reason to flatten the
weapon's normal attacks.

Obliterator's two-handed special emits 210471008, which has impact and interval
children. Measure a large target as well as a humanoid. Its historically unused
one-handed extra reference is already documented in [MECHANICS-REVIEW](MECHANICS-REVIEW.md)
and is not promoted to a new balance defect here.

Preserve Blasphemous Claw and Dragonbolt's intentionally revised mechanics. Their
earlier reference investigation is not evidence for reverting them. Include them
in the same practical damage/resource tests when the author tests those mechanics.

## A practical tuning and test sequence

1. **Make the opening understandable:** a guaranteed early Order route, a concise
   activation hint, a recognizable Nemesis warning, and a clear crystal-hardcore
   explanation. Keep discovery for advanced combinations.
2. **Fix pacing:** ordinary eclipse recovery after failure/avoidance, longer initial
   waits, then assess early Nemesis attack and stance pressure. Preserve hardcore.
3. **Bound exceptional uptime:** test Obliterator reuse, Supremacy and Divinity
   duration interactions; separately verify that Totality's ward is consumed.
   Change one dominant limiter at a time.
4. **Tune complete attacks:** test seven weapon ultimates and their special attacks
   at equivalent progression and upgrade levels. Adjust only connected rows.
5. **Update the guide after decisions and game evidence:** especially Divinity
   materials/gates, Totality access, Oath tradeoffs and ultimate costs.

Use early, midgame and late-game saves with recorded level, Vigor, weapon upgrade,
armor, talismans, Great Runes, Oath and journey. For each relevant build test an
ordinary soldier, a knight, a small boss and a large boss, then repeat eligible
encounters as Nemesis. Record three representative attempts rather than a single
best result. Compare ordinary builds using Order with advanced builds using the
intended full toolkit; neither an unbuffed challenge run nor maximum stacking alone
should define the entire game.

| Test | Record | Proposed acceptance aim |
| --- | --- | --- |
| Opening basic enemy hit | HP lost, armor, Oath active/inactive | Routine hits should leave room to recognize and correct a mistake at sensible early Vigor |
| Early Nemesis | Hits survived, time to kill, escape and stagger opportunities | Dangerous, readable encounter; avoid unavoidable routine one-shots and compulsory cheese |
| Eclipse with no kills | End time, next start, rest/death/reload | Failure does not remove the quiet period |
| Ultimate on each target size | Total damage, actual hit count, stance breaks, cost and time until reuse | A major earned advantage; no repeatable stagger loop that skips earning another use |
| Buff combinations | Incoming damage and resource recovery, exclusions, expiration | Exceptional protection is bounded and the declared exclusions actually work |
| Divinity | Acquisition in-session/reload, health threshold, cast counters, timer interactions | Unlock matches the chosen design; no hidden reload requirement or self-sustaining timer loop |
| Hardcore/follower transitions | Existing/new enemies, crystal release, equip/remove seal, NG+ | The explicit hardcore choice and follower protection remain consistent |

Numerical tuning ranges above are initial experiments, not universal damage caps
or pass/fail facts. Final damage and hit-count measurements remain outstanding.
Store observed gameplay results through the existing [test matrix](../TEST-MATRIX.md)
and `docs/test-results/` workflow; this static review does not mark those tests passed.
