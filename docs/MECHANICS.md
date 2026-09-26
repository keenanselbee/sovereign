# Mechanics evidence and release decisions

Current 1.3.3 implementation: aid waits three continuous eligible seconds,
then ramps over ten seconds in twenty five-point steps to 2x HP/FP/stamina maxima
and outgoing damage. Guard stamina cost reaches 0.5x (twice the endurance per
stamina point; approximately four times full-bar endurance with doubled stamina).
Resource percentages, spending protection and ten-second withdrawal remain.
Hadeon returns visibly to his original position facing the barrier; hallway
lights wait one continuous second outside before switching off. See
[implementation and verification](test-results/2026-09-25-opening-followup.md).
Native/source checks are distinct from pending in-game acceptance.

The [ground-stomp investigation](GROUND-STOMP-GOAL.md) records the approved
jump-counter goal and implemented Hadeon entry lesson. The 2026-09-25 local trial
sets guard disable and dodge-invulnerability bypass on shared NPC attack 2500182;
damage and collision stay unchanged. The author confirmed the original stomp is
jumpable, but the parameter definition warns that bypass overrides airborne
avoidance. Jumpability and deflection rejection after the edit remain untested.

Version 1.2.6 adds [Hadeon's arena aid](HADEON-AID-UPDATE.md): ten-second ramp
to +50% resource maxima/damage and reciprocal guard stamina cost, proportional
current resources, visual-only shard aura and a safe ten-second withdrawal on
victory/departure. Beginner rescue uses effective maximum HP. Native/source
checks pass; resource ordering and presentation still require game acceptance.

The [Rick visible transition](RICK-ENCOUNTER-UPDATE.md) is now implemented locally
and synced to editors, awaiting deployment/game testing: stance-break bait at 25%
HP, two-second golden warning, one charged burst at 75% base attack power,
Hoarah vocal and a visible actor swap. Every attempt starts with the soldier;
only final victory persists. No percentage-HP damage or black fade is used.

The approved [room follow-up](HADEON-LIGHTING-UPDATE.md) is implemented locally:
ceiling Scions are suppressed, room illumination ignites in 26 staggered banks,
and hallway proximity controls re-arm on exit. Event compilation and source
simulation pass; deployment and game acceptance remain pending. Rick's visible transition is implemented as described above.

Version 1.1.7 requires both statue activations for one shared imp barrier
([gate ownership](GRAVEYARD-KEY-GATES.md)). It also removes the invalid unused
light node from candle flame FXR 7506110, preserving all other decoded source
fields. The [1.1.6 room-entry crash](test-results/2026-09-24-hadeon-room-entry-crash.md)
requires a corrected in-game retest; static checks are not gameplay acceptance.

Version 1.1.6 corrects the [Hadeon lighting update](HADEON-LIGHTING-UPDATE.md):
82 room candles use grouped red-light presets preserving their source settings.
The 74 particle flames stay continuous; eight other assets use illumination only.
Models and hallway controls remain unchanged; visual/performance playtests are pending.

The 1.1.4 [Hadeon lighting update](HADEON-LIGHTING-UPDATE.md) adds staged brazier
illumination, brief gaze surges, victory/crystal hallway states and a five-second
crystal cue followed by room dimming. In-game visual and performance checks are pending.

Version 1.1.3 restores a later Favor upgrade: Hadeon grants +1, the Shunning-Grounds
duplicate becomes one Darklight Arc, and Ashen Leyndell retains +2. The custom +3
is removed without old Sovereign-save conversion. See [the progression update](FAVOR-PROGRESSION-UPDATE.md)
for exact rows, unchanged collection flags and the included short-fall correction.

The 1.1.2 [Rick follow-up](RICK-ENCOUNTER-UPDATE.md) adds saved phase-two retries,
an explicit ground-level warp target, Hoarah Loux's transition vocal with a hidden
sound carrier, hittable transition protection, and normal Nemesis visuals on the
beginner rescue heal. Native/source checks do not establish gameplay acceptance.

The 1.1.0 [Chapel reward update](CHAPEL-SHARD-UPDATE.md) replaces the maiden's
Wizened Finger with one existing Darklight Shard and moves the finger to Kale for
100 runes. The [1.1.1 Chapel fix](CHAPEL-POLISH-UPDATE.md) removes the remaining
finger restriction and ground message, revises shard text, and completes omen VFX.

The 1.0.9 [opening update](BEGINNER-OPENING-UPDATE.md) adds the 45-second
beginner rescue, grants Hadeon Thorn Ward at both 75% and 50%, separates the left
imp flag from vanilla, softens the key knight, adds the initial Chapel omen and
suppresses the exit omen after crystal destruction. Gameplay acceptance is pending.

Living feature intent and balance decisions are maintained in
[DESIGN.md](DESIGN.md) and [BALANCE.md](BALANCE.md). This file records implementation
evidence; an earlier review's proposed tuning is not an accepted design change.

For the 2026-09-23 independent Stonesword Key gates, three torch pairs, Partisan
Godrick Knight and final Rick key reward, see [the implementation record](GRAVEYARD-KEY-GATES.md).
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

For the 2026-09-23 tutorial replacement, see [TUTORIAL-UPDATE](TUTORIAL-UPDATE.md).
Tutorial 1180 teaches deflection with Guarding image 16; the other 85 native rows
are gated off. Popup timing, global suppression and pause behavior await game tests.

## Nemesis and the physical red crystal

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

Primary source: `event/src/m18_00_00_00.emevd.dcx.js`, events 5750290-5750309.

- Startup no longer clears defeat 1055420915, collection 1055420916, gesture marker
  1055420009 or the former testing flags 1055420914/1055420917.
- Event 5750300 initializes death reconciliation and, after completed defeat,
  removes Hadeon, his health bar/music and both barrier assets/SFX on reload.
  The encounter entry, bounds and delayed blessing workers have defeat guards.
- Event 5750290 owns reward lot 6050 (Erdtree's Favor +1, accessory 1041). Its
  existing lot collection flag 1055420916 prevents repeat payout. A defeated but
  uncollected state is reconciled on load, including an interrupted reward delay.
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
[implementation and evidence](GAMEPLAY-CORRECTNESS-UPDATE.md), tests ER-035–ER-041.
Do not publish the acquisition guide as verified until these tests pass.

The weapon uses category 984. Skill 660, Harness Void Eye, costs 45 FP and applies
effect 1626770 for 60 seconds, including state 7750 and +100 magic/lightning attack.
The ultimate HKS gate checks readiness 7588 and window 7551, excludes cooldown 7587,
and requires the relevant two-handed/right-hand input branch. In the inspected
configuration the combination uses R2 with L1 when the swap setting is true (L2
when false), with button hold below two seconds. These are source conditions;
controller behavior and input timing still require an in-game test.

The general charge meter has ten steps: ordinary kill/deflect gives one, larger
deflect two. It starts at effect 277 and reaches full at 287. The Obliterator's
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
storage, respawn and interruption behavior require ER-031–ER-034; the source does
not distinguish Rykard damage from other deaths during the active encounter.
See [the implementation report](GAMEPLAY-CORRECTNESS-UPDATE.md) for exact IDs.

## Evidence policy

For every published feature keep: source path plus event/row ID, condition and
effect, source/build hashes, test IDs, and the latest observed result. Use
**Implemented (static evidence)**, **Observed in game**, **Proposed**, or **Unresolved**
explicitly. A successful compiler run, matching package hash, or copied description
is not evidence that progression, acquisition or persistence works.
