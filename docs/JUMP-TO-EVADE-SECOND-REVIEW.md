Jump to Evade: second evidence review
====================================

Reviewed again on 2026-09-25 at the author's request. **All 47 priority candidates
and all 245 curated records are retained, with their existing tiers unchanged.**
This pass adds qualifications and checks the supporting evidence; it does not
cross off attacks, apply parameters or establish gameplay acceptance.

The [expanded shortlist](JUMP-TO-EVADE-EXPANSION.md) remains the test plan. The
[second-review evidence](jump-to-evade-second-review.json) supplements the
[candidate inventory](jump-to-evade-candidates.json), rather than replacing it.


Checks that strengthen the shortlist
------------------------------------

- Independently rebuilt attack-to-bullet associations for all 245 curated rows
  from the complete Bullet table. All agree with the published inventory.
- For all 47 priorities, traced every reverse parent and the complete forward
  graph from every registered BehaviorParam root, using both hit-child and
  interval-child links. This checks sibling branches as well as shortest paths.
  No additional HP-damaging attack row was found in those forward graphs.
- Checked all 49 damage bullets used by the 47 rows. No acceleration, auto-homing,
  inherited speed, random lifetime, explosion delay, endless-hit setting or
  attachment-following was found. Radagon 2190296 has gravity 10 in and out of
  range; its actual movement still requires observation.
- Freshly parsed all 2,272 animation records in the 11 priority character binders,
  including records with no selected attack events. The 95 explicit native
  behavior-event witnesses cover 78 complete animation/variation patterns.
  Full sequences are recorded, extending the earlier +/-0.25-second contact scan.
- Inspected 26 motion-import relationships involving priority animations. Reused
  motion is distinguished from reused attack events; twelve enhanced Godfrey /
  Hoarah animations switch to separate large-wave rows.
- Freshly exported 12,096 SpEffect rows. No behaviorId literal matches a priority
  behavior ID or judge ID. From 223 associated NPC rows and the inspected model
  timelines, followed 416 effects through explicit replacement, cycle, attack
  and spirit-death links. No behavior-spawn or judge-modifier setting was found
  in that effect closure.
- Searched 12 repository HKS/event source files for exact priority attack,
  behavior and linked bullet IDs; no literal matches. This does not resolve
  calculated IDs, engine behavior, external scripts or every possible FXR path.

These are positive structural checks, not a claim that a held jump avoids every
wave. The parameter files still match the expansion baseline, and the animation
sources matched their recorded hashes before native parsing.


Qualifications added without removing candidates
------------------------------------------------

| Candidate family | What the deeper review establishes | Specific test to keep |
| --- | --- | --- |
| Crucible / Hadeon, Godfrey, Hoarah, Messmer Soldier | Damage pulses are separate, but intermediate probe and final-child BehaviorParam entries also exist without explicit timeline matches. Some damage bullets use launch-condition value 5, labelled Unknown by the installed enum. | Keep all selected rows. Verify actual floor placement, slopes and edge cases; do not call every registered route floor-only or unused. |
| Devonia's four priority rows | Carrier/probe attack rows have zero HP damage but nonzero poise values: 20 for ordinary foot/hammer routes, 10 for transformed routes. | Record loss of air control or stagger as well as HP. A no-HP-loss result alone does not prove a clean jump counter. |
| Beast Claw | The two animated roots have numShoot 12 / 4, lifetimes 0.55 / 1.5s and interval children every 0.1s. Damage children last 0.09 / 0.15s. | Test both entire patterns, several distances and landing inside the pattern. Child lifetime is not whole-wave duration. |
| Trolls and Ancestor Spirit | Separate short pulses and foot/forelimb landmarks remain supported; imported motion variants with their own events were checked. | Preserve all 27 rows. Verify actual pose at emission, scale, overlapping body contacts and the full combo; a rest-model dummy is not a live hitbox measurement. |
| Radagon compact/wider waves | Gravity-driven probes, isolated damage children and separate hammer contacts remain supported. | Test the wave after the hammer reaches the ground, at close/far distances and during jump attacks. Ground placement alone does not prove the sphere clears the upper body. |
| Radagon delayed waves | Non-damaging timer nodes remain distinct from the final short damage pulses. 2190296 has nonzero gravity; 2190382 has an additional registered root without a matched attack event. | Keep all three rows. Test delay, landing/re-jump timing and possible vertical movement; retain the unresolved alternate root in the record. |
| Black Knight | Both great-hammer variants retain their own root, gravity probe, short damage child and separate physical weapon contact. | Test both variants; neither has the airborne-avoidance bit. Do not infer success or failure solely from that bit. |

All 49 selected damage bullets set `isUseSharedHitList=1`. Their hit-record
lifetimes differ: Beast Claw 3s, many ordinary foot bursts 1s, Godfrey/Hoarah
0.4s, some Radagon pulses 0.3/0.5s, and several entries 0. The installed definition
labels values <=0 as indefinite hit-record lifetime. This is hit-history data,
not bullet lifetime or proof that separate roots share one cooldown. Count
actual hits through overlapping fronts and repeated emissions in the game.


Alternate routes and animation reuse
------------------------------------

Fifteen registered bullet-entry behaviors across eight priority rows lack an
explicit type-1, type-2 or type-5 witness in the native timelines reviewed here:

| Damage row | Unmatched registered behavior IDs |
| --- | --- |
| 2500182 | 225000181, 225000182 |
| 2500252 | 225000251, 225000252 |
| 2500442 | 225000441, 225000442 |
| 2500592 | 225000591, 225000592 |
| 4720114 | 247200113, 247200114 |
| 4721142 | 247210141, 247210142 |
| 5830202 | 258300201, 258300202 |
| 2190382 | 221900401 |

The first seven rows have registered entries directly into their probe or damage
child, in addition to the witnessed travelling-wave root. The eighth has a longer
alternate chain. These are retained as unresolved entry points. No matching
SpEffect literal or repository source literal was found; absence of those matches
does not establish that the engine never uses an entry.

A concrete animation-reuse check illustrates why full sequences matter:

| Model / animation | Native bullet judge | Referenced wave |
| --- | ---: | --- |
| c4720 / 3001 | 112 | Ordinary chain ending in attack 4720114 |
| c4720 / 1003001, importing 3001 motion | 400 | Separate large-wave attack 4720400 |
| c4721 / 3005 | 140 | Ordinary chain ending in attack 4721142 |
| c4721 / 1003005, importing 3005 motion | 600 | Separate large-wave attack 4721600 |

Five further imports in each Godfrey/Hoarah family follow the same distinction.
The existing large-wave candidates remain in the wider queue; they have not been
removed or silently folded into ordinary-wave acceptance. Radagon 20002 imports
3018 motion but has no explicit type-2 bullet event in its own timeline; motion
reuse alone does not establish another use of 2190281.


Interpretation and preservation
------------------------------

Keep the original 14 / 27 / 6 test-priority split. This review found reasons to
make tests more specific, not evidence requiring a smaller candidate list.
The first live gate remains Hadeon's guard/deflect/roll rejection alongside
ordinary-jump and both-grip jump-attack clearance. Later families require their
own checks even if Hadeon passes.

The native player template calls flag 132 lower-body jump invulnerability.
That supports testing lower-body protection; it does not prove that jumping
literally removes a collider or that general invulnerability bypass preserves
it. No global airborne immunity, movement change or speculative collision
resize follows from this review.

Evidence is retained under `.codex-temp/jump-rereview-20260925/`: the fresh native
reader, complete animation events, fresh SpEffect export and `review.py`. The
public JSON keeps the reviewed graphs, full attack-event patterns, motion-import
records, motion/hit-history controls, source hashes and explicit limitations.
The numeric source search and effect closure are bounded static checks, not
whole-engine reachability proofs. No gameplay test or deployment ran.
