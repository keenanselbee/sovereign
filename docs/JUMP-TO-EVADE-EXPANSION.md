Jump to Evade: expanded priority candidates
==========================================

**Second review:** all 47 priority candidates remain on the list. The
[deeper evidence review](JUMP-TO-EVADE-SECOND-REVIEW.md) checks complete bullet
branches, full animation sequences, motion imports and effect routes, and adds
specific qualifications without removing or demoting any candidate.

Expanded on 2026-09-25 against the current Sovereign 1.3.3 parameter data.
**47 distinct damage rows now have an explicit priority test plan, up from eight.**
There are 31 newly curated rows, eight previously conditional rows selected for
closer testing, and the original eight. Thirteen new entries are DLC Troll
counterparts, not thirteen new enemy families. The priority list spans ten
families when counterparts and Devonia's variants are combined.

This is research, not a gameplay patch. Confidence concerns the identity and
isolation of a potential ground counter. **None is newly verified jump-only.**
Hadeon's post-bypass test remains the first gate. No damage, collision, timing,
movement, editor workspace or deployed file was changed for this expansion.

The [original investigation](JUMP-TO-EVADE-INVESTIGATION.md) explains the combat
rule and test protocol. The updated [evidence JSON](jump-to-evade-candidates.json)
contains exact routes, flags, damage values, attachment landmarks, nearby direct
contacts and shared users. The [screening CSV](jump-to-evade-screening.csv)
contains all 1,570 screening rows; an unreviewed row is not an approved candidate.


What increased confidence
-------------------------

The previous discovery pass emphasized downward-shot probes with children of
radius <=1.5. The expanded pass also inspects gravity-driven map-colliding probes,
short standalone impact bullets, and native model attachment points. A probe
can point horizontally with zero initial speed and still fall under gravity.
Radagon and Black Knights use this structure, which the narrow heuristic missed.

Twenty-four additional character model binders provide 5,690 new dummy records.
Seven additional animation binders resolve missing routes, including Black
Knights and Scadutree Avatar. All 116 retained animation sources still match
their recorded hashes. Fresh native exports show that every row/cell in
AtkParam_Npc, Bullet, BehaviorParam and NpcParam still matches the first pass,
even though the current regulation container has changed for other work.

For every priority row, the reviewed Bullet table links only short, non-following
damage bullets with zero initial velocity to that row, and the BehaviorParam search finds no
direct-contact reference to the same attack. Companion foot/weapon/body attacks
are identified separately. This is stronger than a name or an airborne flag;
it is still not an exhaustive proof of AI, event, SpEffect or runtime spawn use.

| Priority | Rows | Evidence and remaining condition |
| --- | ---: | --- |
| P1 | 14 | Small floor-probe damage children, maximum radius <=2 and life <=0.25s. Strongest structural ground-placement evidence; all still need post-bypass jumps. |
| P2 | 27 | Short stationary pulses attached at feet/forelimbs, maximum radius <=2.3. Native attachment identity is established; animated height at emission is not measured. |
| P3 | 6 | Floor-probe routes with radius-3 damage, or delayed floor detonations. Additional clearance or whole-sequence qualification required. |

P1 corresponds to the updated Tier A. P2/P3 are selected Tier B rows with better
origin evidence; they have not been relabelled as equally safe as P1. The other
Tier B rows remain secondary. P1/P2/P3 are test priorities, not probabilities or
an instruction to patch all 47. Retain the original A/B/C/D distinction in tools
and use the new `priorityBand` field to select this test plan.


P1: small floor-probe waves
--------------------------

All numbers in the damage-row column are AtkParam_Npc IDs. Animation offsets are
authored clip times, not measured reaction windows. A row may cover several
moves or encounters; the JSON retains every traced BehaviorParam root.

| Family | Damage rows | Concrete evidence / remaining test |
| --- | --- | --- |
| Crucible Knights / Hadeon | 2500182, 2500252, 2500442, 2500592 | Original four radius-1 foot-wave children; confirm every knight variant and slopes. Only 2500182 currently has both trial flags. |
| Godfrey ordinary waves | 4720114 | Original radius-1.2 child after downward probe; six behavior roots. Large arena waves remain separate. |
| Hoarah Loux ordinary waves | 4721142 | Original radius-1.2 child after downward probe; six roots. Preserve separate hands/body/grabs. |
| Devonia foot/hammer waves | 5800302 | Original radius-1 child shared by two chains; both hammer and foot paths need tests. |
| Messmer Soldier | 5830202 | Original radius-1 left-foot wave; five timeline associations. |
| Beast Clergyman / Gurranq | 2110150 | Both damage bullets, 2110152/2110158, are stationary radius-1.5 floor children lasting 0.09/0.15s. c2110 3005 at 2.733s and 3006 at 0.767s. Airborne bit is absent; test both patterns and encounters. |
| Devonia transformed limb waves | 5800653, 5800673, 5800753 | All damage children are radius 1 / 0.2s. Model landmarks resolve horse-like digits and transformed hands; probes place the damage. In 3011 emissions span 1.300-5.600s; 3016 emits at 2.600/2.667s. Whole-combo landing windows remain a separate gate. |
| Radagon compact hammer waves | 2190161, 2190281 | Newly curated: 2190161 -> 2190162 -> 2190163 and 2190281 -> 2190282 -> 2190283. Middle bullets have zero initial speed, gravity 100 and map collision; final damage radius 2, life 0.15/0.21s. c2190 3006 at 1.633s and 3018 at 3.500s. Hammer contacts 2190160/2190280 remain separate. |

Beast Claw and Devonia's transformed waves were already known conditionally.
Their promotion is specifically about the complete damage-row reuse check and
floor-probe architecture. It does not resolve Beast Claw's missing air flag or
Devonia's repeated hits. If those gates fail, keep the affected rows unchanged.


P2: additional foot and forelimb bursts
--------------------------------------

The largest concrete addition is Troll foot impacts. Each of the following
base/DLC pairs independently connects its own behavior and timeline to a
stationary bullet expanding from radius 0.1 to 2.3, life 0.2s. Dummy 30 attaches
to `R_FootTwist`, and dummy 40 to `L_FootTwist`, in both c4600 and c5390.
The damaging foot-contact row is distinct from the burst. This allows testing
only the burst while leaving a direct kick/stomp dangerous.

The first two pairs were previously conditional; the other eleven pairs were
not in the curated list. Each row below gives one witness; multiple uses of a
shared row still need qualification.

| Base damage row | DLC damage row | Foot | Witness animation / impact time |
| --- | --- | --- | --- |
| 4600101 | 5390101 | Left | 3000 / 0.833s |
| 4600131 | 5390131 | Right | 3003 / 0.667s |
| 4600141 | 5390141 | Left | 3004 / 1.000s |
| 4600171 | 5390171 | Right | 3007 / 0.833s |
| 4600181 | 5390181 | Left | 3008 / 1.033s |
| 4600211 | 5390211 | Right | 3012 / 0.833s |
| 4600311 | 5390311 | Right | 1003012 / 1.600s |
| 4600344 | 5390344 | Right | 1003015 / 2.933s |
| 4600351 | 5390351 | Left | 1003014 / 1.033s |
| 4600448 | 5390448 | Right | 1003037 / 4.100s |
| 4600450 | 5390450 | Left | 1003037 / 5.433s |
| 4600463 | 5390463 | Left | 1003038 / 2.500s |
| 4600471 | 5390471 | Left | 1003015 / 1.067s |

Examples of distinct companion contacts are 4600140 versus burst 4600141,
4600343 versus burst 4600344, and 4600441/4600443 versus 4600448/4600450.
The paired DLC routes were checked independently. Neither a matching suffix nor
a matching model name was accepted as proof of reuse.

**Ancestor Spirit 4670180** adds one further priority row. Radius 1.8, life
0.15s, with separate physical contacts; dummy 20/22 attaches to `R_Finger0` /
`L_Finger0` on its forelimbs. Witnesses are c4670 3002 and 1003002 at 2.333s,
3020 at 1.167/1.200s, and 3027 at 1.033s. Nearby direct contacts include
4670181, 4670291, 4670262 and 4670121. The named Front Stomp contacts
in the evidence are 4670291 and 4670262; do not conflate the whole animation with
the one selected damage pulse.

For P2, preview the actual emission poses before applying bypass. A foot
attachment identifies the limb, not its world-space height at that instant.
Reject a move if the burst is emitted in the air, if its upper extent defeats
normal jumps, or if its sequence has no fair landing/re-jump window. Test direct
foot contact at close range separately from the outward burst.


P3: larger or delayed ground pulses
----------------------------------

| Family | Damage rows | Evidence / remaining condition |
| --- | --- | --- |
| Radagon wider hammer wave | 2190201 | c2190 3010 at 1.367s; 2190201 -> 2190202 -> 2190203, gravity-100 map probe. Damage expands from radius 2 to 3, life 0.21s. Direct hammer row 2190200 stays separate. |
| Black Knight great-hammer wave | 5840131 | Fresh c5840 3004 at 2.233s, great-club dummy 11; 205840131 -> 205840132 -> 205840133. Damage radius 2 -> 3, life 0.21s, airborne bit 0. Direct attack 5840130 remains separate. |
| Black Knight alternate great-hammer wave | 5840441 | c5840 3003022 at 2.333s; 205840441 -> 205840442 -> 205840443, same gravity-probe architecture. Distinct attack and direct-contact row 5840440; do not assume a one-row change covers both variants. |
| Radagon delayed floor detonation | 2190292 | c2190 3019 at 2.200s launches the chain; final bullet 2190296 shrinks radius 1 -> 0.1, damage life 0.5s, downward gravity 10. |
| Radagon delayed ground floor | 2190372 | c2190 3028 at 3.267s launches the chain; final bullet 2190376 has radius 2, damage life 0.5s. |
| Radagon delayed hammer floor | 2190382 | c2190 3029 at 3.267s launches the chain; final bullet 2190386 has radius 2, damage life 0.21s. Additional behavior 221900401 has no matched animation and remains a reachability uncertainty. |

The delayed chains pass through map-colliding gravity probes and attack-1
visual/timer nodes. Their two-second timer is not itself a two-second damaging
hazard. This differs from the excluded Death Rite Bird rows that share actual
damage with long-lived bullets. The 2190296 damage child also has downward gravity 10; unlike the other
priority damage children, it has potential vertical motion that needs measurement. The
emitted chain can still create multiple pulses, so test the complete pattern, visual warning, normal jump and jump attack.
The initial travelling Radagon rows 2190291/2190371/2190381 are not included in
these child-only priorities.

All priority rows currently have guard disable and dodge bypass 0 except the
existing Hadeon trial 2500182. All have airborne avoidance 1 except Beast Claw
2110150 and the two Black Knight rows. Preserve existing air/parry settings in
any future minimal trial; their presence or absence does not prove the result.


Secondary additions and rejected shortcuts
------------------------------------------

These are documented beyond the 47 priorities, so useful evidence is retained
without diluting the higher-confidence test list.

| Family / rows | Why it remains secondary or excluded |
| --- | --- |
| Tree Sentinel 3251161/1281/1451 and DLC 6251161/1281/1451 | Radius-2 / 0.2s pulses from halberd dummy 81, with separate weapon contacts. Need the animated weapon-tip height; unlike Troll foot bursts, attachment identity does not establish a ground-facing contact. |
| Guardian 3650900 | Radius-1.5 / 0.1s spear pulse shared across numerous attack animations; qualify every pose before a shared-row edit. |
| Troll 4600251/0261/0381/0571 and DLC 5390251/0261/0381/0571 | Hand/weapon origins; deliberately separated from the priority foot subset. |
| Dragonkin 4650300/0301/0810/0811 | Confirmed right/left toe origin, but radius 3.5 and nearby hand pulses in the same sequences. |
| Scadutree Avatar 5230205 | Fresh 3005/3006 timelines resolve repeated hand-launched probes; radius 3.2, thorn/hand overlap and pulse spacing remain open. |
| Consort Radahn 5220191 | Holy foot-wave child exists, but the same attack also damages through its carrier and probe. Row-wide edits cannot be described as child-only. |
| Dancing Lion 5210151/0431/0511 | Small floor-contact children share damage with head-launched, moving parents. |
| Golem Smith 5260281 | Separate short damage child, but produced by thrown hand projectiles; ground-counter readability and launch condition need review. |
| Guardian Golem 4660501/0506 and DLC 5790501/0506 | **Correction:** newly read origins are `L_Bow001`; these routes were previously grouped with local impacts. Excluded from the simple ground-wave rollout. |
| Giant Dog 4550221, Guardian 3650410, Troll 4600971 | Native origins are Jaw, Spine2 and L_mouth respectively. Small collision spheres alone were misleading. |
| Graven School 3730110 | Shared row includes a ten-second damaging bullet. |
| Melina 2180100; seekers 4480130/5380130/5800500 | Ally scope or additional holy-seeker strike components; gravity floor contact is insufficient to establish a suitable low enemy wave. |

Rellana, Furnace Golems, Putrescent Knight and other large arena waves remain
in the original later queue. This pass does not increase their jump-clearance
confidence merely because their visuals look ground-bound.


Evidence, reproduction and next test order
------------------------------------------

| Coverage | First pass | Expanded |
| --- | ---: | ---: |
| Screening rows | 681 | 1,570 |
| Curated candidate/exclusion rows | 178 | 245 |
| Curated groups | 53 | 72 |
| Tier A / B / C / D rows | 8 / 41 / 109 / 20 | 14 / 85 / 114 / 32 |
| Animation binders | 109 | 116 |
| Animation records with selected events | 26,646 | 27,233 |
| Model dummy records | 1,045 | 6,735 |

Current regulation SHA-256:
`5c21a9413b84f5fe568398153464f72e17a795a9f402985b015f611d0cebae9f`.
The JSON preserves the prior regulation hash, exact table-equivalence results,
input hashes, archive receipts, native model hashes and every priority ID.
Map-user evidence retains the first-pass 25,398-placement snapshot; this pass
makes no claim to have refreshed map placements or proved every AI route active.

Scratch readers and exports are retained under
`.codex-temp/jump-expansion-20260925/`, including `analyze.py`, `publish.py`,
current parameter exports, new model/animation extracts and archive receipts.
The new discovery predicate includes enemy-range damage rows with at least one
bullet of maximum radius <=3.5 and life <=0.5s, in addition to the original
name/air/floor-probe screening. It deliberately admits false positives for
manual review; the numbers are not counts of safe jumpable attacks.

After Hadeon's trial passes, qualify the remaining Crucible waves and the two
ordinary Godfrey/Hoarah rows. Then test Beast Claw, compact Radagon waves,
Messmer Soldier and Devonia. For broader common-enemy coverage, start P2 with
one Troll left-foot and one right-foot burst, then their DLC equivalents before
covering the remaining animations. Test P3's wider waves and delayed chains
individually. A failed family remains unchanged rather than receiving global
jump immunity or an unreviewed collision redesign.

Use the [original acceptance protocol](JUMP-TO-EVADE-INVESTIGATION.md): baseline
standing overlap, guard/deflect/roll failures, ordinary-jump and both-grip jump
attack successes, early/late timing, close/far range, slopes and all shared
variants. Record exact attack and bullet IDs so a companion foot or hammer hit
cannot be mistaken for failure of the selected ground-wave counter.

Validation completed: exact priority/group counts and JSON/CSV agreement;
all priority bullet/behavior path edges; P1 size/lifetime limits; P2 native
attachment evidence; delayed timer damage fields; and 18 local document links.
All 75 runtime/package files retained their initial hashes. Concurrent unrelated
authoring-source additions and README edits were preserved and excluded from
this research change. The verification record is retained at
`.codex-temp/jump-expansion-20260925/verification.json`. No in-game check ran.
