# Mechanics evidence and release decisions

Living feature intent and balance decisions are maintained in
[DESIGN.md](DESIGN.md) and [BALANCE.md](BALANCE.md). This file records implementation
evidence; an earlier review's proposed tuning is not an accepted design change.

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

## Nemesis and the physical red crystal

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
- Event 5750290 owns reward lot 6050 (Erdtree's Favor +3, accessory 1043). Its
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
