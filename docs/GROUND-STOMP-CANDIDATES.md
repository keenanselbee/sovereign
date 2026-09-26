Ground-stomp candidate review
============================

Historical 2026-09-24 screening. The current
[2026-09-25 investigation](JUMP-TO-EVADE-INVESTIGATION.md) and
[expanded priority list](JUMP-TO-EVADE-EXPANSION.md) supersede its
priorities and unverified move attributions. In particular, Watchdog 4260351
comes from a head projectile, and Devonia 5800663 has no established active
route; the active chain uses 5800653. Do not use this older list as an edit
allowlist. Hadeon's two-flag trial is now deployed in 1.3.2, with game acceptance
pending; the regulation hash below is the historical pre-trial baseline.

Expanded native-data review, 2026-09-24, for the approved
[ground-stomp goal](GROUND-STOMP-GOAL.md). This is a proposed review list, not an
approved bulk parameter patch. No runtime files were changed. Each proposed wave
must physically clear an ordinary, correctly timed jump and jumping attack before
its roll/guard counters are removed.

The regulation inspected has SHA-256
`41b42f86d3a692df7a30b56cef27a0500c374ee88a2cca34f3bf0c038707958d`.
Current hash matched the native exports in `.codex-temp/stomp-review/`.
IDs below are **AtkParam_Npc damage rows**, not necessarily identically numbered
bullets. Listed rows are concrete starting points; lists labelled examples are
not exhaustive attack-family coverage. In-game usage and exact move attribution
of generically named rows still require animation/AI tracing.


Selection rule
---------------

Include a short, clearly telegraphed floor shockwave whose damage volume stays
low enough for the intended jump window. Exclude the stomping foot, falling body,
weapon contact and any separate rising blast or lingering hazard. A jump should
avoid the wave without making the player immune to those other contacts.

BulletParam `hitRadius` and `hitRadiusMax` are sphere radii, not separate horizontal
range and vertical height. Values below are radii in game metres; they do not prove
world-space height. Spawn dummy positions, animation transforms, terrain placement
and the swept path matter. Direct attack rows likewise attach spheres/capsules to
dummy points. All geometry remains **unverified in motion** in this review.

The native airborne-avoidance bit is useful evidence of intended jump handling,
but not proof of physical clearance. The attack definition states that
`isDisableNoDamage` overrides `isInvalidatedByNoDamageInAir`. Therefore do not
blindly combine dodge bypass with the airborne bit and call it jump-safe.

Primary definitions: [BulletParam](https://raw.githubusercontent.com/soulsmods/Paramdex/master/ER/Defs/BulletParam.xml),
[AtkParam](https://raw.githubusercontent.com/soulsmods/Paramdex/master/ER/Defs/AtkParam.xml).


First geometry trials
----------------------

These have relatively small, local damage volumes and are the most promising
starting points. Their exact height and attack identity still need inspection.
All listed damage rows currently carry airborne avoidance.

| Enemy / attack candidate | Damage row IDs | Native geometry and recommendation |
| --- | --- | --- |
| Hadeon / Crucible Knight stomp wave | 2500182 | Bullet sphere grows 0.1 to 1.0, lives 0.2s. First trial; shared knight route. |
| Other Crucible Knight local ground bursts | 2500252, 2500442, 2500592 | Same 0.1-to-1.0 radius, 0.2s. Trace animations before deciding which are actual ground-stomp variants. |
| Godfrey ordinary stomp wave | 4720114 | 0.1 to 1.2, 0.2s. Review the damaging child, not zero-damage carrier 4720112. |
| Hoarah Loux ordinary stomp wave | 4721142 | 0.1 to 1.2, 0.2s. Keep grab/body impacts separate. |
| Devonia local ground impacts | 5800302, 5800653, 5800663, 5800673, 5800753 | Linked spheres grow 0.1 to 1.0; typically 0.13-0.25s. Confirm hammer/ground-wave identity per animation. |
| Burial Watchdog ground-projectile family | 4260351 | Five linked bullet variants use radius 0.5 and 0.2s. Confirm that these are low travelling floor hits, not elevated projectiles. |
| Grave Warden Duelist local impacts | 3400350, 3400351 | Direct radius-1.0 spheres at dummy points 32/22. Position in animation determines suitability. |
| Messmer Soldier local impact | 5830202 | Bullet grows 0.1 to 1.0, 0.2s. Generic row name: identify the actual move before inclusion. |


Broader ground-wave candidates
------------------------------

These fit the proposed combat rule conceptually, but their larger collision
volumes may require redesign. A low-looking visual does not establish clearance.
Unless stated otherwise, the listed rows already enable airborne avoidance.

| Enemy / attack candidate | Damage rows to inspect | Scope and geometry concern |
| --- | --- | --- |
| Godrick double/triple ground eruptions | 4750410, 4750413, 4750550, 4750553 | Damage bullets use radii 4.5/9.0. Each ground pulse is a candidate; exclude axe contact and taller rock eruptions that cannot reasonably be jumped. |
| Godfrey phase-change and arena wave | 4720281, 4720400 | Max radii 7.5/50.0. Phase-change row has conflicting bypass/airborne bits. Full-area row already disables guard, but still allows dodge invulnerability. |
| Hoarah Loux arena wave and ground bursts | 4721600; examples 4721160, 4721220, 4721370, 4721441 | Arena wave reaches radius 50; local examples reach 3.0. Full-area row already disables guard. Separate eruptions and grab slams from their low waves. |
| Starscourge Radahn physical ground waves | 4730224, 4730226, 4730234, 4730236, 4730368, 4730373 | Linked damage spheres grow 0.1 to 3.5. Include floor waves, retain sword impacts and overhead attacks. |
| Starscourge Radahn magic ground waves | 4730352, 4730354, 4730375 | Same 3.5 maximum radius. Include only after visual/height review; do not extend the rule to all gravity magic or ground lightning. |
| Radagon stomp waves | 2190260, 2190261, 2190420 | Direct radius-3 sphere and bullets reaching 6.0/6.3. Distinguish stomp impact from spreading holy damage. |
| Radagon hammer ground waves | 2190510, 2190520, 2190530 | Radius 2.0/3.0/5.0, respectively. Candidate floor components; separate hammer collision and rising holy blasts. |
| Fire Giant stomp shockwaves | 4760062, 4760171 | Radius 0.5 to 3.5. Foot contacts 4760060/61/170 are separate and must stay distinct. |
| Ordinary Erdtree Avatar slam/stomp waves | 4810183, 4810250 | Radius 7.5/4.0. Keep falling body, hammer and Putrid Avatar rot variants separate. |
| Troll/Troll Knight ground impacts, including DLC variants | Examples 4600101, 4600103, 4600121, 4600131; 5390101, 5390103, 5390121, 5390131 | Typical local radii 2.3-2.5; other rows reach 9.5. Large family: classify individual stomp/weapon-ground bursts, not every troll attack. |
| Tree Sentinel shield-ground waves | 3251241, 3251271; DLC 6251241, 6251271 | Radius 0.1 to 5.5. Only the ground wave, not shield or horse contact. |
| Draconic Tree Sentinel slam waves | 3250141; examples 3250181, 3250291, 3250301 | Radius 0.1 to 3.5. Generic rows need move tracing; exclude fireballs and lightning strikes. |
| Dragonkin Soldier ground impacts | Examples 4650132, 4650141, 4650152, 4650162, 4650182 | Radius 1.0 to 3.5; wider family includes 5.0-radius effects. Hand/body collision, ice and lightning require separate decisions. |
| Guardian Golem ground bursts | Examples 4660501, 4660506, 4660740, 4660741; DLC 5790501, 5790506 | Radii 2.1-5.2 across the inspected family. Trace slam versus other projectile effects; keep axe/body contact separate. |
| Ancestor Spirit stomp wave | 4670210 | Radius 4.0. Ground wave is a candidate; hoof contact and floating/body attacks remain separate. |
| Fallingstar Beast foot-impact burst | 4680185; DLC 6310185 | Radius 2.0 to 3.0. Exclude gravity pull-up attacks 4680295/4680455 and body charges from automatic inclusion. |
| Grafted Scion shield-ground impact | 4690181 | Direct radius-2.0 sphere at dummy 230. Verify that its position permits jump attacks; shield contact 4690180 is separate. |
| Margit hammer-jump ground burst | 2130771 | Radius 3.5. Candidate shockwave only; jumping into the descending hammer should remain dangerous. |
| Demi-Human Queen impact bursts | Examples 4130102, 4130136, 4130182, 4130183; DLC equivalents 5730102/136/182/183 | Radius 0.1 to 2.0. Generic names require tracing to distinguish ground impacts from other effects. |
| Furnace Golem ground fire waves | 5170250, 5170255 | Linked radius-6.0 spheres. Strong teaching fit for wave timing, but clearance must survive bypass. Exclude descending feet/body and elevated flames. |
| Rellana repeated ground waves | 5300760, 5300762, 5300764 | Bullets grow from 0.5 to 50.0. Strong timing-counter candidate; cannot assume the large native spheres are physically jump-clear. Preserve the gaps between waves. |
| Putrescent Knight moving floor-wave families | 5020600, 5020610, 5020620, 5020621 | Many brief linked bullets; some reach radius 42. Classify floor wave versus broad burst first. Do not apply to all ghostflame. |
| Elden Beast ring wave | 2200420 | Linked bullet radius 1.2, lifetime 3.5s. Inspect its actual travel and ring geometry; treat the later explosion as a separate attack. |


Conditional or deferred candidates
-----------------------------------

| Enemy / component | Damage rows | Why it needs more work |
| --- | --- | --- |
| Valiant Gargoyle stomp wave | 4770252, used by bullet 4770253 | Radius 5.0; airborne avoidance is OFF. Qualify or rebuild the geometry before removing rolls. |
| Elemer shield-ground impact | 3100400 | Radius-2.5 sphere at dummy 2; airborne avoidance OFF. Inspect the shield and its follow-up separately. |
| Winged Misbegotten stomp/jump burst | 3460180, 3460201 | Direct radius-2 stomp has airborne avoidance; radius-3.5 jump burst does not. Animation and model naming need confirmation. |
| Giant Crow stomp AoEs | 4560151, 4560161, 4560181, 4560201, 4560211, 4560511 | Airborne avoidance OFF; sample 4560151 uses two radius-2.5 spheres attached to the actor. High risk of overlapping the airborne player. |
| Godskin Noble landing wave | 3570262 | Radius grows to 9.5. The falling body is a distinct contact; preserve that danger. |
| Magma Wyrm crush AoEs | 4910171, 4910331 | Direct radii 7.5/8.0 at dummy 30. Too large to assume jumping physically clears them; separate magma and body contact. |
| Dragon/drake foot shockwaves | Examples 4500201, 4500211, 4500271, 4500281; corresponding 5580/5860 DLC families | Typical radii 5-7. Feet, tails, breath and elemental aftereffects overlap; inspect per animation and variant. |
| Walking Mausoleum ground bursts | Examples 4450200, 4450230, 4450250 | Radii reach 6/11/30. Optional environmental extension, not a first combat rollout. |
| Commander Gaius ground-effect family | Examples 5000101, 5000111, 5000171, 5000501, 5000511 | Local radii 2-3.2; later effects reach 15/17 and live over 2s. Generic names require attribution; exclude charge and broad gravity effects. |
| Runebear ground impacts | 4630410, 4630411; DLC 5780410/11, 5820410/11 | Actor-bound AoEs need animation height checks. Preserve body contact rather than making all bear slams jump-only. |


Explicit exclusions from a bulk change
--------------------------------------

Do not automatically include Scarlet Aeonia, Astel's gravity slam, lava/rot pools,
lingering ice, rising lightning, Rykard's large explosions, grabs, roars, charges,
weapon swings or a descending enemy body. Their visuals, duration and height do
not communicate the same low-wave counter. An airborne flag or the word "ground"
alone is insufficient.

The initial scan covers base-game and DLC rows, including generically named and
apparently unused variants. It does not prove every listed row is reached in a
live encounter, nor exclude additional unnamed attacks. Confirm usage before
editing shared damage rows.


Geometry and acceptance requirements
-------------------------------------

1. Visualize the actual damaging hitbox in motion, including child bullets and
   maximum growth. Measure its upper edge relative to the local floor throughout
   the damage window; a tiny initial radius is not sufficient.
2. Test standard grounded rolls through the wave, ordinary jumps, one/two-handed
   jumping light/heavy attacks, and relevant equip-load variations. Include close
   range, the wave edge, slopes, stairs and changes in floor elevation.
3. If the hit volume is too tall, lower or reshape only that ground-wave route.
   Large spherical AoEs may need distributed low volumes or another qualified
   method; shrinking their radius alone also shrinks horizontal coverage. Do not
   assume an independent bullet-height field exists.
4. Preserve damage, poise damage, warning duration, number of intended hits and
   separate contacts. A damage pulse should not remain active long enough to catch
   a correctly timed jump on landing unless a clearly separated second pulse is
   intended.
5. Only after jump clearance is demonstrated, qualify guard/deflect rejection and
   roll bypass together. Keep the acceptance local to each attack family. Test
   shared NPC users and multiplayer before describing the rule as universal.

Recommended first batch: Hadeon's 2500182, Godfrey's 4720114, Hoarah Loux's 4721142,
then verified low Devonia variants. Larger rings and AoEs follow after the small
wave implementation proves the collision approach.
