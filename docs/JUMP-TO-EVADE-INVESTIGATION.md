Jump to Evade: attack investigation
==================================

**Expanded follow-up:** the [current priority review](JUMP-TO-EVADE-EXPANSION.md)
now covers 47 priority test rows: 14 small floor-probe rows, 27 foot/forelimb
pulses and six larger or delayed ground pulses. The evidence JSON/CSV now contain
1,570 screened rows and 245 curated rows in 72 groups, against unchanged attack,
bullet and behavior tables freshly exported from 1.3.3. No expansion patch or
new gameplay acceptance is implied. The follow-up supersedes the first-pass
counts and rankings below, including four Guardian Golem bow-impact rows.

The [second evidence review](JUMP-TO-EVADE-SECOND-REVIEW.md) retains all 47
priority rows and adds full-route and whole-animation qualifications.

First-pass research completed 2026-09-25 against Sovereign 1.3.2. This is an investigation
and proposed test order, **not an approved bulk attack patch**. No runtime assets
were changed during this investigation. The author's test of Hadeon's existing
two-flag stomp trial remains pending.

The first pass selected **eight damage rows across five groups**, followed
by 41 conditional candidates. The linked follow-up expands that test plan. Start with the same small, floor-contact wave
architecture as Hadeon. Do not convert every stomp, every airborne-avoidance row,
or every component of a move.

The goal is a readable low wave that defeats standing guard, timed deflection
and dodge invulnerability, while a correctly timed ordinary jump or jumping
attack clears it. Moving outside its range remains a valid response. Separate
feet, weapons, falling bodies, grabs and lingering hazards retain their own rules.

See the [design goal](GROUND-STOMP-GOAL.md), [detailed native evidence](jump-to-evade-candidates.json)
and [complete screening table](jump-to-evade-screening.csv). The earlier
[candidate review](GROUND-STOMP-CANDIDATES.md) is historical; corrections below
supersede its priorities and apparent-unused-row assumptions.


First-pass evidence and coverage
--------------------------------

| Work performed | Coverage |
| --- | --- |
| Current regulation scanned | 12,856 NPC attack rows; 15,545 bullets; 13,896 behaviors |
| Candidate discovery | All 501 airborne-avoidance rows; ground/stomp/slam/wave names; small, short-lived impacts reached through downward floor probes |
| Combined screening | 681 distinct attack rows, including unsuitable, unused and non-enemy results |
| Curated review | 178 rows in 53 groups: A = 8; B = 41; C = 109; D = 20 |
| Animation data | 109 character binders; 26,646 animation records containing selected event types, including the accepted player overlay |
| Shared-user search | 25,398 enemy placements from 1,347 map files, using repository overlays where present |
| Model landmarks | 1,045 dummy points from six character models, including Sovereign's c2500 overlay |

Tier A means **strong structural evidence for testing**, not proven post-edit
jump safety. B requires an additional geometry/shared-use decision. C is a
later investigation queue. D is rejected from a simple row-wide conversion or
has no established active route. U in the screening CSV means unapproved and
not individually promoted into the curated set. No tier authorizes editing.

First-pass regulation SHA-256 (current follow-up hash is in the expansion report):
`6698b106aac7d5bcae85fbb651bedb75c14974e9d1b5a6882fc164b26e2b0538`.
Installed base regulation comparison:
`766521f9508de3a3532df61c45a1c2d93340f1ff7ed8306ab20df761712ca2ab`.
The latter is the installed base file, not a claim about every historical patch.
Fresh animation archive extraction records include BHD hashes, BDT size/time and
individual file hashes. The map inventory uses the prior archive-qualified
extraction under `.codex-temp/flag-allocation-review/current/`, with current mod
map overlays. It was not freshly extracted in this pass.

The JSON preserves exact flags, damage values, bullet geometry, witness routes,
animation/dummy associations, NPC IDs and observed map/model users. Bullet paths
are shortest witnesses, not all possible paths; the accompanying bullet graph
preserves both hit-child and interval-child links for further inspection.

Names are discovery hints. An animation association joins model, behavior
variation and judge ID; it is not proof that AI chooses that animation in every
encounter. Imported animations and runtime variation switches are not fully
resolved. Disabled placements and unused rows can appear in the map inventory.
One dictionary-listed binder, `c5501.anibnd.dcx`, was absent from the current
archives. That does not block the eight Tier A candidates.


The flag interaction is the first decision gate
----------------------------------------------

The installed/native definitions and the upstream
[attack definition](https://raw.githubusercontent.com/soulsmods/Paramdex/master/ER/Defs/AtkParam.xml)
describe guard bypass, general invulnerability bypass and airborne avoidance as
separate fields. The airborne field explicitly loses effect when general bypass
is enabled. Conventional parry rejection is another separate field.

The [animation template](https://github.com/Meowmaritus/DSAnimStudio/blob/master/DSAnimStudioNETCore/Res/TAE.Template.ER.xml)
identifies flag 132 as lower-body jump invulnerability, 134 as a falling/jump
variant and 94 as complete invulnerability. The accepted player's `a00.tae`
contains flag 132 in animations 4000, 4010 and 4020, respectively over authored
windows 0-2.3, 0-1.0 and 0-1.2 seconds. These are timeline windows, not measured
in-game jump durations or proof that all parts are protected for those durations.

**Unresolved:** whether `isDisableNoDamage=1` bypasses the particular lower-body
protection we need in the tested player state. There is no engine-level proof in
these parameter definitions. The author confirmed the original Crucible stomp
was jumpable; that does not qualify the changed combination. Do not infer safety
merely because `isInvalidatedByNoDamageInAir` remains 1.

Sovereign's deflection flows through just-guard handling, including
`SetJustGuardSucceedEffect` in `mod/action/script/c0000.hks`. Setting
`isDisableParry` alone would not establish that a wave rejects deflection.
`disableGuard=1` is the relevant proposed first trial; verify both health damage
and absence of successful-deflection rewards. Oath/ward protection can obscure
the result, so qualify the basic mechanic without those protections first.

If Hadeon's post-edit jump succeeds reliably, expand in small groups. If jumping
also fails, stop the rollout: adding the airborne flag again cannot fix an
explicit override. Investigate attack-local collision/handling rather than
making the player globally invincible while jumping. Do not change every enemy
or global movement to compensate for a failed premise.


Why the strongest architecture is promising
-------------------------------------------

Hadeon's route is:

```text
c2500 animation 3008, at 0.800s, left-foot dummy 4
  -> Behavior 225000180
  -> Bullet 2500180: travelling carrier, interval child 2500181
  -> Bullet 2500181: -90-degree probe, speed 100, collides with map
  -> Bullet 2500182: stationary damage pulse at contact
  -> AtkParam_Npc 2500182
```

The first two attack rows have zero base damage, stamina damage and poise damage.
The final child grows from radius 0.1 to 1.0 over 0.06 seconds and lives 0.2
seconds. It deals the actual 220 base physical / 140 stamina / 20 poise attack
values before the game's damage calculation. Those values are not final player
HP loss. Dummy 4 attaches to `L_FootTwist`; dummy 3 to `R_FootTwist`.

This is substantially stronger evidence of ground placement than a row name.
It still needs an in-game check on slopes, stairs and floor edges: probes can
hit different levels of terrain, and nearby body/weapon damage is independent.

The [bullet definition](https://raw.githubusercontent.com/soulsmods/Paramdex/master/ER/Defs/BulletParam.xml)
uses sphere radii, not independent width and height. A radius-50 wave is not
proved to be a physically thin floor ring. Conversely, do not require collision
redesign just because a radius is large: first test the existing jump protection.
Geometry changes are a fallback, and shrinking a sphere also shrinks its reach.


Tier A: first expansion tests
----------------------------

All IDs in the damage column are **AtkParam_Npc IDs**. DLC bullet IDs often
start with `20` and must not be confused with their attack IDs. Animation times
below are authored clip offsets; AI windup, blending and travel add context.

| Group | Damage rows | Native route / animation evidence | Important shared scope |
| --- | --- | --- | --- |
| Hadeon / Crucible Knight | **2500182** | `2500180 -> 2500181 -> 2500182`; c2500 **3008**, 0.800s, left foot | Already the two-flag trial; shared with other knights, not Hadeon-only |
| Other Crucible foot waves | **2500252, 2500442, 2500592** | Roots 2500250 / 2500440 / 2500590; c2500 **3025** at 1.000s, **1003004** at 0.767s, **1003022** at 0.933s; last uses right foot | Same radius-1 / 0.2s floor-probe design; qualify all variants |
| Godfrey ordinary waves | **4720114** | Root 4720112, downward 4720113, damage 4720114; c4720 **3001** at 2.300s, dummy 40; radius 1.2 / 0.2s | Six roots; also 3009, 3034, 6000, 6002, 6003. Does not cover the full-screen variant |
| Hoarah Loux ordinary waves | **4721142** | Root 4721140, downward 4721141, damage 4721142; c4721 **3005** at 1.600s; radius 1.2 / 0.2s | Six roots; also 3018, 3032, 3034, 3035, 3037. Leave grabs/body and full-screen waves alone |
| Devonia foot / hammer waves | **5800302** | `205800300 -> 301 -> 302` and `205800310 -> 311 -> 312`; final attack shared; radius 1 / 0.13-0.25s | c5800 **3003/3007** from left foot, **3002/3004/3005** from hammer. A row edit changes both |
| Messmer Soldier | **5830202** | `205830200 -> 205830201 -> 205830202`; left-foot dummy 4, radius 1 / 0.2s | c5830 **3008, 3010, 1003008, 1003010, 2003010**; impact offsets 0.933-1.767s |

Except for the deployed Hadeon trial, these damage rows currently have guard
disable 0, dodge bypass 0, airborne avoidance 1. Suggested first changes, **only
after acceptance**, are guard disable and dodge bypass on the damaging rows;
preserve damage, stamina/poise, radius, timing, projectile count and effects.

Devonia's carrier rows have zero HP damage but nonzero poise fields. Do not call
every floor-probe carrier harmless in every respect, or modify carriers merely
because they precede the damage child.


Tier B: worthwhile next candidates
---------------------------------

These 41 rows have a concrete route or plausible local ground contact, but each
has an additional qualification requirement. The JSON lists every row and
animation association, including DLC counterparts.

| Candidate | Damage rows | Reason to investigate / remaining issue |
| --- | --- | --- |
| Beast Clergyman / Gurranq Beast Claw | **2110150** | Two floor chains; radius 1.5, 0.09/0.15s; c2110 **3005** at 2.733s and **3006** at 0.767s. No airborne flag; test both shared encounters and all claw directions |
| Promised Consort Radahn local wave | **5220190** | c5220 **3009** at 0.867s, dummy 3; downward probe and radius-1.2 child. No airborne flag; same damaging row also serves carriers, so isolate if those create unwanted contacts |
| Devonia transformed ground waves | **5800653, 5800673, 5800753** | Radius-1 floor impacts. **3011** emits several times from 1.3 to 5.6s; **3016** at 2.600/2.667s. Whole-combo timing and body overlap matter |
| Godskin Noble rapier impact | **3570191** | Radius 1.5 / 0.2s; several rapier impact animations. Keep blade thrust and subsequent attacks separate |
| Local Troll / DLC Troll bursts | **4600101/103/121/131**, **5390101/103/121/131** | Selected local 2.3-2.5-radius pulses. Do not extend automatically to all 49 air-flagged rows in either family |
| Demi-Human Queen / DLC copy | **4130102/136/182/183**, **5730102/136/182/183** | Small ground-impact candidates; identify staff/body companions and pulse timing |
| Avatar | **4810183, 4810250** | Butt-slam wave and stomp, separate from body and rot; radii 7.5/4, 0.1s. Particularly important to test the airborne-flag interaction |
| Godrick / shared variant | **4750410/413/550/553** | Triple: **3031** at 2.367, 3.400, 5.733s. Double: **20005** at 2.800, 4.233s. Radii 4.5/9; qualify each pulse and axe overlap |
| Fire Giant | **4760062, 4760171** | Radius 3.5 / 0.15s; timelines **3006**, **3018**. Foot/body contacts are distinct attacks |
| Misbegotten stomp | **3460180, 5950180** | Foot-associated direct radius-2 hit; moving hitbox qualification needed |
| Grave Warden Duelist | **3400350, 3400351** | Two radius-1 hits in **1003005**, at 2.400/2.467s; dummies 32/22 attach to twin hammers, not feet |
| Elemer / Bell Bearing Hunter | **3100400** | Direct radius 2.5, dummy 2; no airborne flag. Separate shield contact and follow-up |
| Grafted Scion | **4690181** | Direct radius 2, dummy 230, **3008** at 1.533s. Shield hit 4690180 remains separate |
| Pumpkin Head variants | **4340370, 4341370** | Local 2/1.6-radius pulses; thin variant's imported animation route still needs resolution |
| Golem Smith | **5260230/231/232** | 1.5/2/3.5-radius, 0.2s impacts; exclude the separate 2-second projectile family 5260221 |

Beast Claw and the Consort wave demonstrate why a scan limited to the airborne
flag misses plausible candidates. They are not elevated to A because no current
post-bypass jump evidence exists and shared/adjacent damage needs attention.


Tier C: broader expansion queue
------------------------------

There are 109 rows here, grouped and enumerated in the evidence JSON. They are
worth retaining, but should not delay proving the smaller-wave implementation.

| Family | Starting damage rows | Main concern |
| --- | --- | --- |
| Godfrey / Hoarah full-area waves | 4720281, 4720400, 4721600 | Radii 7.5/50/50. Full-screen attacks already reject guard but allow ordinary invulnerability; they use different rows from ordinary stomps |
| Radagon ground/hammer effects | 2190260/261, 2190420, 2190510/520/530 | Direct hammer contact plus ground and holy follow-ups; isolate intended component |
| Starscourge Radahn | Physical 4730224/226/234/236/368/373; magic 4730352/354/375 | Separate physical and gravity components; do not include giant explosion 4730492 |
| Dragonkin Soldier | 4650132/141/152/162/182 | Ground contacts, hand motion and ice/lightning may overlap; not approval for all 37 flagged rows |
| Guardian Golem / DLC copy | 4660740-4660757 selected entries; corresponding 5790 rows | Follow-up excludes 4660501/506 and 5790501/506 as bow-fired routes. Other selected bursts still need review; not the entire numeric range |
| Ancestor Spirit | 4670210 | Shared by several animations; distinguish ground wave from hoof and dive contacts |
| Fallingstar Beast / DLC | 4680185, 6310185 | Feet AoE separate from charge and gravity pull |
| Tree / Draconic Sentinels | 3251141/1241/1271; 6251141/1241/1271; 3250141/181/291/301 | Mounted body, shield, fire and lightning cannot be converted together |
| Margit | 2130771 | Hammer/jump body overlap; burst radius 3.5 |
| Furnace Golem | 5170250, 5170255 | Stomp and jumping ring chains; radius 6, multiple emission paths and landing flames |
| Rellana | 5300760/762/764 | **3036** contains all three routes; damage spheres expand to 50. Do not mistake initial radius 0.5 for final height |
| Putrescent Knight | 5020600/610/620/621 | Long recursive chains, short pulses but some radii reach 42; check outward/return waves and landing windows |
| Elden Beast ring push | 2200420 | Radius 1.2, but child lives 3.5s; inspect moving ring path and delayed child creation |
| Gargoyle | 4770252 | Actual bullet 4770253, radius 5, no airborne flag |
| Godskin Noble landing | 3570262 | Radius 9.5; falling body and knockaway are distinct |
| Magma Wyrm / DLC | 4910171/331; 5920171/331 | Large direct spheres, body motion, magma |
| Dragons / drakes | Selected 4500201/211/271/281 and 5580/5860 copies | Foot waves mixed with large feet, tail, breath and elemental companions |
| Walking Mausoleum | 4450200/230/250 | Optional environmental case; huge feet and uneven ground |
| Gaius | 5000101/111/171/501/511 | Local candidates only; leave charge and larger gravity effects separate |
| Runebears | 4630410/411; 5780410/411; 5820410/411 | Actor-bound volume and body contact, not stationary floor pulses |
| Starcaller | 4380172/182/192 | Strong floor-probe structure, but multiple direct emissions and variant states; spike visuals may not communicate a low wave |
| Horned Warrior | 5250220, 5250485, 5250540/541/581 | Mixed wind/elemental and rising effects; floor placement alone is insufficient |
| Great Red Bear claw | 5820300 | Small floor impacts share row with a radius-3 close pulse |
| Ancient Dragon stake wave | 4510801 | Small floor contacts share row with other lightning bullets; isolate before changing |


Corrections and exclusions
-------------------------

1. **Godfrey's existing bypass does not prove his ordinary wave bypasses rolls.**
   Sovereign changes 4720112, whose base damage/stamina/poise values are zero.
   The damaging 4720114 remains guardable and dodgeable. A separate modified
   phase-shift attack, 4720281, already has bypass, but is a much larger volume.
2. **Watchdog 4260351 is not established as a stomp.** Animation 3038/3039 fires
   from dummy 40, attached to `HeadSub`. Its damaging parent travels at 35 with
   a -3-degree angle, then creates successive child generations. Remove it from
   the early stomp list; small child radius and an airborne flag were misleading.
3. **Devonia 5800663 has no established active route.** Bullet 205800661 points
   to **205800653**, not 205800663. No hit/interval predecessor or BehaviorParam
   root was found for 205800663. Other spawning mechanisms were not exhaustively
   excluded, so this is not a claim that it can safely be deleted.
4. **Small children can share an attack with lingering hazards.** Death Rite Bird
   4980740 and DLC 6260740 serve both short floor contacts and 5-second damage
   bullets. Row-wide bypass would alter both. Bloodfiend 5080601/606 and Prelate
   3910184 also have 5-second bullets despite relatively small radii.
5. **The airborne flag is not a ground-wave whitelist.** Crucible fire breath,
   Sentinel fireballs, numerous body attacks and other effects carry it. Do not
   convert these, ordinary weapon swings, roars, grabs, charges, rising lightning,
   Scarlet Aeonia, Astel's gravity slam, rot/lava pools or lingering ice.

Comparing the four relevant flags to the installed base regulation found only
four changed rows within the 681-row screening set: 2500182 (the trial),
4720112 and 4720281 (Godfrey bypass), and 2120720 (a Sovereign Malenia bullet).
This comparison does not mean their other fields or the rest of Sovereign are
vanilla. The Malenia effect is outside this expansion proposal.


Test protocol and adoption gates
--------------------------------

For Hadeon, record the exact deployed version and whether the wave itself hits;
separate an overlapping sword/foot contact. Use normal equipment without rescue
heal, ward, Oath invulnerability or other effects masking the outcome where
practical. Record HP and successful-deflection charge/reward, not just animation.

| Check | Expected result for an accepted wave |
| --- | --- |
| Stand inside wave, no input | Damage; confirms overlap and prevents a false jump pass from being out of range |
| Shield held / weapon block | Damage; distinguish guard rejection from simply exhausting stamina |
| Correctly timed shield and weapon deflection | Damage; no successful-deflection reward |
| Light/medium roll through the wave while still in its footprint | Damage despite roll invulnerability; rolling out of reach is allowed |
| Ordinary jump, no attack | Avoids the wave reliably across a usable timing window |
| One-handed and two-handed jumping attacks | Avoid wave; airborne weapon/arm posture must not make one grip unexpectedly fail |
| Early and late jump | Predictable failure outside the window; no damage long after the wave appears to pass |
| Near foot versus several metres away | Distinguish separate physical foot/body contact; wave counter remains readable |
| Wave edge, slopes, stairs and bridge edge | No inaccessible floor-probe hits or terrain-specific loss of the counter |
| Every pulse and shared variant | No unmodified child or later pulse contradicts the taught rule |
| Relevant co-op case | Host/guest damage and timing consistent enough to teach the same counter |

Suggested evidence per clip: enemy/map, animation or move, attack and bullet ID,
version/hash, flags, distance/terrain, equipment/grip/load, input timing, HP before
and after, deflect reward, outcome and video timestamp. Mark **not tested** rather
than passing an unobserved case. A compact proposed promotion gate is five clean
ordinary-jump and five jumping-attack successes at a normal distance, plus
guard/deflect/roll failures on overlapping wave trials and edge/terrain checks.
Those repetitions are a proposed acceptance standard, not tests performed here.

Initial evidence state: original Hadeon stomp jumpable = author confirmed;
Hadeon with both new flags = pending; every expansion candidate = pending.
Do not reinterpret lack of damage from a rescue heal as a jump success.

If Hadeon passes, test the other three Crucible waves before broadening the
shared family, then ordinary Godfrey, ordinary Hoarah, Messmer Soldier and
Devonia. Qualify both Devonia foot and hammer paths. Beast Claw and the Consort
wave are especially useful next experiments because they have no airborne bit:
they help distinguish geometric clearance from flag-dependent avoidance.

The simple implementation remains parameter-only on an explicit accepted
allowlist. It adds no global update loop, wait loop, player movement change,
new bullets or light effects. Clone a route only when a shared attack row also
controls an unsuitable component and a narrow row edit cannot satisfy the rule.
Avoid making every attack jump-only; the goal is recognizable counter variety.


Reproduction and remaining limits
--------------------------------

Scratch evidence and native readers are retained under
`.codex-temp/jump-investigation-20260925/`: current parameter exports,
archive receipts, TAE event extracts, model dummy records, map users,
`analyze.py`, `publish.py` and C# readers. Native extraction used the existing
archive-qualified reader from `.codex-temp/event-baseline-audit/`; no game
archives or editor workspaces were written. The durable JSON/CSV preserve the
reviewed subset and broad screening even if scratch is later removed.

Discovery is reproducible from the retained inputs: scan names and the airborne
bit, then find bullets launched at -80 degrees or steeper that collide with the
map and produce a damaging child of radius <=1.5 and life <=0.5 seconds. Follow
`HitBulletID` and `intervalCreateBulletId` backwards to BehaviorParam, associate
judge IDs with TAE event 1/2 and map-observed models, and inspect all bullets
sharing each attack. This is a discovery heuristic, not an engine simulation.

Remaining limits: no animated Havok pose evaluation or live hitbox measurements;
no exhaustive AI/state-machine reachability proof; no exhaustive FXR/event/SpEffect
spawn-route scan; inherited-animation variants can be undercounted; no new
gameplay acceptance. The investigation supplies a prioritized, traceable test
inventory rather than claiming every low attack in the game has been identified.
