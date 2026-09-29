# Mechanics evidence and release decisions

Feature evidence owners
-----------------------

Use the owning report below for current implementation and its qualifications.
Earlier repeated release summaries are retained in [history](history/feature-summary-history.md).
Deployment status belongs to its receipt; observed game acceptance belongs to
[TEST-MATRIX](../TEST-MATRIX.md), not a copied release paragraph.

| Feature | Owning implementation/evidence |
| --- | --- |
| Eighteen Hadeon teleport destinations and generated helpers | [Implementation and pending game checks](test-results/2026-09-29-hadeon-destinations-172.md) |
| Memory of Grace return without rune loss | [Implementation and pending game checks](test-results/2026-09-28-memory-of-grace-171.md) |
| Hadeon Vortex tiers, mid-slam teleport and positional entrance voice | [Implementation and checks](test-results/2026-09-28-hadeon-vortex.md) |
| Hadeon arena aid | [Aid report](HADEON-AID-UPDATE.md#current-implementation) |
| Hadeon repeat teleport, dialogue gates and movement recorder fix | [1.5.6 verification](test-results/2026-09-27-hadeon-followup-156.md) |
| Hadeon running-AI monologue and combat handoff | [1.5.5 implementation and checks](test-results/2026-09-27-hadeon-wait-155.md) |
| Hadeon dialogue, progressive aid and no-aid victory | [1.4.4 implementation and checks](test-results/2026-09-27-hadeon-progression.md) |
| Ground-wave jump counters | [All 47 rows](test-results/2026-09-26-jump-all47.md); [design goal](GROUND-STOMP-GOAL.md) |
| Hadeon retreat, hallway grace, current opening follow-up | [1.3.3 implementation and qualification](test-results/2026-09-25-opening-followup.md) |
| Rick transition and retry behavior | [Rick encounter report](RICK-ENCOUNTER-UPDATE.md) |
| Room lighting and Nemesis gaze | [Lighting report](HADEON-LIGHTING-UPDATE.md); later follow-up above |
| Key barriers and rewards | [Gate ownership](GRAVEYARD-KEY-GATES.md) |
| Beginner rescue and generic Ultimate launch | [Opening support](OPENING-SUPPORT-1.2.4.md) |
| Rescue-aware Soldier/Rick music and starting flask pouch trial | [Implementation and game checks](test-results/2026-09-28-opening-pouch-music.md) |
| Lessons, text and Deflection artwork | [Opening text/artwork evidence](test-results/2026-09-25-opening-dialogue-tutorial.md), [texture recipe](../src/textures/tutorial/README.md) |
| Favor rewards and short-fall correction | [Progression report](FAVOR-PROGRESSION-UPDATE.md) |
| Chapel shard and door changes | [Shard report](CHAPEL-SHARD-UPDATE.md), [follow-up](CHAPEL-POLISH-UPDATE.md) |


Living feature intent and balance decisions are maintained in
[DESIGN.md](DESIGN.md) and [BALANCE.md](BALANCE.md). This file records implementation
evidence; an earlier review's proposed tuning is not an accepted design change.

For the 2026-09-23 independent Stonesword Key gates, three torch pairs,
Godrick Knight and final Rick key reward, see [the implementation record](GRAVEYARD-KEY-GATES.md).
The knight now uses the 1.3.2 sword-and-shield variant; its original Partisan setup
is historical (see [the accepted decision](BALANCE.md) and ER-122).
This supersedes the earlier keyless-entry proposal. Native checks and editor sync
are distinct from gameplay acceptance and package deployment.

Inspection baseline: 2026-09-09. These are static findings from local source,
compiled events, parameters and map exports, not gameplay test results. Do not turn
proposed behavior into Nexus claims. Local detailed exports and earlier analyses are
under `.codex-temp/sovereign-inspect/`; source event IDs below provide durable anchors.
Existing user edits to regulation and shrine map are preserved by workflow preparation.
For the later fresh Claw/Dragonbolt and Obliterator investigation, see
[MECHANICS-REVIEW](MECHANICS-REVIEW.md). It preserves the author's intentional custom
mechanics and distinguishes dangling historical references from connected behavior.
For the broader 2026-09-11 investigation of opening difficulty, Oaths, Divinity and
custom attacks, see [BALANCE-REVIEW](BALANCE-REVIEW.md) and its stored parameter
evidence. Its tuning ranges are proposals, not accepted gameplay changes.

For the implemented 2026-09-19 Hadeon threshold boons, fall attrition and
encounter-only deflect thorns, see [HADEON-COMBAT-UPDATE](HADEON-COMBAT-UPDATE.md).
That update supersedes the earlier random encounter-boon behavior, preserves
global follower/Oath behavior, and remains awaiting gameplay acceptance.

For the implemented 2026-09-20 optional guidebooks, discovery numbering, NG+
retention, and independent Gyre hat flag, see
[PROFANE-TOMES-UPDATE](PROFANE-TOMES-UPDATE.md). Fresh saves are the target;
older-save migration is deliberately excluded. Game tests remain pending.

For the 2026-09-20 tome flag correction and once-per-character vanilla-save
onboarding, see [the implementation record](ONBOARDING-FLAG-FIX-PLAN.md). It records
valid tome flags, completion marker `69990`, independent dragon compensation
receipts, pending-reward exclusion, prayerbook cleanup, and the Placidusax stock
correction. Native/source checks pass; actual NG+ and reward tests remain pending.

For the 2026-09-22 Soldier of Godrick / Rick two-phase encounter, see
[RICK-ENCOUNTER-UPDATE](RICK-ENCOUNTER-UPDATE.md). The author approved reserving
Golden Eyes for phase 2 and adding Boss Modifier, a full heal, 1.5x size, a fade
and The Final Battle music. Native checks pass; gameplay acceptance remains Pending.

For tutorial history and text, see [TUTORIAL-UPDATE](TUTORIAL-UPDATE.md).
The original 2026-09-23 Deflection-only replacement is superseded by three
approved lessons: Deflection two seconds after the knight-approach region,
Ultimate Attacks 2.5 seconds after Soldier arena admission, and Jump to Evade
after three safe seconds in Hadeon's room. See the [opening sequence](GROUND-STOMP-GOAL.md)
and [timing follow-up](test-results/2026-09-25-opening-followup.md). Other vanilla
lessons remain suppressed; the old statement that all 85 other rows are gated off
describes the initial implementation only. Deflection retains image slot 16,
now with custom artwork; the [current texture recipe](../src/textures/tutorial/README.md)
owns the approved Deflection and Ultimate images. Popup timing, suppression,
pause behavior and current artwork appearance still require gameplay acceptance.

## Nemesis and the physical red crystal

Current terminology is Nightmare difficulty for the combat challenge, separate
from the planned Nemesis Unbound story stage. Weapon-restricted crystal destruction
and its final confrontation are deferred. See [the accepted direction](nemesis-unbound.md).
The implementation below still uses the existing release/eclipse/follower flags;
this terminology change does not silently replace those mechanics.

The [2026-09-23 omen update](NEMESIS-OMENS.md) adds cosmetic ten-second cues at the
first outdoor reveal and crystal break, using existing Nemesis sounds without
text. New effects 1627110/1627111 are separate from real eclipse state; both imp
torches revert to normal on Hadeon defeat. Native checks do not establish gameplay.

Updated 2026-09-10: **Implemented (static evidence), game tests pending**.
See [the persistence and hardcore handoff](NEMESIS-PERSISTENCE.md) for accepted
hashes, backups, event ownership and acceptance scenarios.

The ordinary chance-based Nemesis system remains in `action/script/c9997.hks`,
byte-for-byte unchanged by this handoff. Great Rune progression still changes its
rolls. Eligible enemies and effect exclusions matter; this is not an unconditional
global multiplier. Follower protection takes precedence over the forced eclipse
spawn roll. Existing enemies and multiplayer transitions still need game tests.

Breaking crystal entity 18002346 after Hadeon's defeat now sets persistent flag
1055420918 through host-owned event 5750291. Common event 5750101 uses that unlock
to maintain the existing Sovereign of War role (1055420003) and eclipse flag
1055420010. This makes crystal destruction an optional persistent hardcore mode.
The ordinary periodic eclipse worker pauses while hardcore is unlocked.
Following Nemesis clears the hardcore role/eclipse; leaving the follower state
restores hardcore if the crystal was broken, or the ordinary unbound role otherwise.
The previous unconditional NG+ hardcore branch and its forced seal removal are gone.

The journey reset policy is fresh Hadeon/crystal choice in NG+, with no existing-save
migration. The implementation relies on ordinary event-flag reset at the journey
transition; ER-003 must verify that policy in game. Learned gesture 102 is not removed.
Its award marker is no longer cleared on map load; its NG+ notification may repeat.

The inspected map has named crystal `AEG258_158_2019`, entity 18002346, HP 1000 and
defense 10000. Overlapping `AEG258_159_2018` has entity ID 0, HP 1 and defense 0.
The new event watches destruction of **18002346**. Breaking the overlapping model
alone does not prove that flag 1055420918 was set. Map placement, damageability and
visibility remain Smithbox/game checks; this event handoff does not edit either asset.

On 2026-09-11 the author confirmed the initial eclipse waits were testing code and
requested restoration of the commented intended ranges. Event 5750115 now waits
60-10800/9300/7800/6300/4800/3300/1800 seconds for one through seven runes;
six-second test alternatives remain commented out. Later waits up to 60 seconds,
combat blessing waits around 5-6 seconds, passive probabilities, recovery and
eligibility guards are unchanged. The worker still waits through follower
ineligibility; verify resumption without a map reload.

DarkScript build `1789188345950881000` was independently decoded and compared:
only the seven wait argument pairs in event 5750115 changed; all other events,
instruction metadata, parameter bindings and file metadata match. Runtime and
source companion use SHA-256
`711757f7815b3d806cef360ccde95738b87b6a81a261f89130b2ca305bd1405a`.
The qualified repo/editor handoff is retained under
`.sovereign/handoffs/ffe8fc9baadd44d5aa9549b78c2b88bb/receipt.json`.
No Vortex deployment or gameplay pass is implied. The older balance review's
six-second findings describe its preserved pre-fix snapshot.

## Shrine and Hadeon / Crucible Lord

Primary source: [m18_00_00_00.emevd.dcx.js](../src/events/m18_00_00_00.emevd.dcx.js),
events 5750290-5750309.

- Startup no longer clears defeat 1055420915, collection 1055420916, gesture marker
  1055420009 or the former testing flags 1055420914/1055420917.
- Event 5750300 initializes death reconciliation and, after completed defeat,
  removes Hadeon, his health bar/music and both barrier assets/SFX on reload.
  The encounter entry, bounds and delayed blessing workers have defeat guards.
- Event 5750290 owns reward lot 6050 (Erdtree's Favor +1, accessory 1041). Its
  existing lot collection flag 1055420916 prevents repeat payout. A defeated but
  uncollected state is reconciled on load, including an interrupted reward delay.
  In 1.6.8 the live payout waits five seconds after actual banner display; banner
  readiness is 10.5/12.0 seconds into the normal/no-aid death line, independent
  of full voice cleanup. See [verification](test-results/2026-09-28-hadeon-teleport-168.md).
- The earlier actor correction to Hadeon 18002354 and asset corrections to entrance
  wall 18002379 are retained. Region 18002349 remains a region for bounds checks.
  The author controls wall placement and must test collision/visual cleanup.

The [earlier reference fix](SHRINE-REFERENCE-FIX.md) documents the reference-only
stage. Its statement that testing resets were preserved is superseded by this handoff.

Ritual 5750309 now checks persistent Hadeon defeat, area 18002377, a living player
and absence of Bind Seal 6800. Crystal destruction is not required. The gesture
award marker persists across map loads, while interrupted ritual performance retries.
The ritual remains repeatable after losing the seal: lot 6800 is deliberately
repeatable, and the existing unequip path consumes that seal. There is no new
once-per-journey ritual lock. Ritual timing, HP drain and its unusual final death
condition remain unchanged and require in-game interpretation.

Bind Seal 6800 equips effect 1626910: +16 stamina recovery and +70 casting DEX,
not +70 actual Dexterity. The bind controller uses follower role 1055420001 rather
than the temporary protection pulse 1055420000 to select equip versus removal.
Equipping clears conflicting roles. Cycle and ritual cleanup preserve newly acquired
follower protection. Verify equip/remove/delete, repeat ritual, active enemies and
rest/reload in both ordinary and crystal-released play.

## Obliterator and special attacks

**Implemented (static evidence, 2026-09-11):** Hewg offers weapon 23085000 after
Godskin Duo and the three base-game Fallingstar Beasts are defeated in the current
journey. The dedicated option uses the full masterpiece speech before memory loss
and its opening line afterward, with a fade/smithing presentation and item lot 7700.
Its collection flag is intended to permit one reward per journey; NG+ reset and
actual acquisition still require game tests. Goods 8115 (Meteoric Ore Slab) and
8116 (Eye of Astel) remain unused by this route. See
[implementation and evidence](GAMEPLAY-CORRECTNESS-UPDATE.md), tests ER-035â€“ER-041.
Do not publish the acquisition guide as verified until these tests pass.

The weapon uses category 984. Skill 660, Harness Void Eye, costs 45 FP and applies
effect 1626770 for 60 seconds, including state 7750 and +100 magic/lightning attack.
The ultimate HKS gate checks readiness 7588 and window 7551, excludes cooldown 7587,
and requires the relevant two-handed/right-hand input branch. In the inspected
configuration the combination uses R2 with L1 when the swap setting is true (L2
when false), with button hold below two seconds. These are source conditions;
controller behavior and input timing still require an in-game test.

The general charge meter has ten steps: ordinary deflect gives one, larger
deflect two. Version 1.6.7 removes enemy-kill charge; the full-meter spark cue remains. It starts at effect 277 and reaches full at 287. The Obliterator's
resident effect 287 bypasses this ordinary charging path, but its buff/readiness
conditions still matter, explaining why simply equipping it is insufficient. The
ultimate uses Astel's beam bullet 4620221 and refreshes the buff. Older descriptions
of a universal 30-second requirement do not match this inspected path.

A two-handed crouch attack uses a gravity projectile. An additional one-handed
behavior reference 300000867 resolves to an invalid reference (-1) in the inspected
data; verify the expected attack and missing connection before listing it as working.

## Crusade and Black Scaled Armor

**Implemented (static evidence, 2026-09-11):** Crusade Insignia's required effect
20380500 is restored from the installed vanilla regulation; existing custom effect
20380501 is preserved. Confirm the kill-triggered passive in ER-030.

One equipped original Scaled piece qualifies at death during either active Rykard
phase or at final victory. The conversion captures quantities and replaces carried
original pieces one-for-one, including duplicates and altered body armor. Workers
require carried ownership and do not deliberately withdraw from storage. A player
whose Rykard defeat flag was already set cannot start the conversion. Quantity,
storage, respawn and interruption behavior require ER-031â€“ER-034; the source does
not distinguish Rykard damage from other deaths during the active encounter.
See [the implementation report](GAMEPLAY-CORRECTNESS-UPDATE.md) for exact IDs.

## Evidence policy

For every published feature keep: source path plus event/row ID, condition and
effect, source/build hashes, test IDs, and the latest observed result. Use
**Implemented (static evidence)**, **Observed in game**, **Proposed**, or **Unresolved**
explicitly. A successful compiler run, matching package hash, or copied description
is not evidence that progression, acquisition or persistence works.

Hadeon follow-up: [Vortex routing, dialogue history and progression lighting](test-results/2026-09-28-hadeon-followup-160.md).
