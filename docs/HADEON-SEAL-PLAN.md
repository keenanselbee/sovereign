Hadeon mandatory opening encounter
==================================

Status: revised design direction under investigation, 2026-09-11. The latest
request supersedes the earlier optional key-triggered commitment proposal.
Keyless access and travel gating remain unimplemented; combat assistance has a
separate [implemented update](HADEON-COMBAT-UPDATE.md), with game tests pending.

The 2026-09-19 [combat investigation](HADEON-ENCOUNTER-REVIEW.md) traces
the former Nemesis support and arena returns. Its deflection-credit proposal was
superseded by the approved minimal threshold-boon and deflect-thorn update.


Requested direction
-------------------

- No Stonesword Keys are required to enter the dungeon section.
- Hadeon is a mandatory opening opponent, tuned for a new character using deflects.
- The exit barrier is active from the start and remains until Hadeon is defeated.
- Fast travel from the starting dungeon remains prohibited until his defeat.
- The existing crystal release remains the separate deliberate hardcore choice.

This resolves the earlier question about using key expenditure as a commitment.
No new key-triggered commitment flag or optional-entry confirmation is needed.
The exact physical coverage of the starting-dungeon seal and internal retry points
still requires map/game verification. This is a local dungeon travel restriction;
blocking existing characters' travel elsewhere is not inferred from this request.


Current findings
----------------

The saved Smithbox map and DarkScript source match their repository counterparts.
The key statue 18001570, inserted-key assets 18001571/18001572 and seal 18001573
remain in the map at normal scale. Constructor calls still initialize common
helper 90005620 and local seal worker 18002569 using completion flag 18000570.
The helper still consumes two Stonesword Keys before setting that flag. No explicit
removal or forced-open setter was found in the inspected shrine/common sources.
An already-open save or an alternate physical route is not proof of keyless access
for a fresh character; unsaved editor changes are outside this evidence.

The desired custom-barrier lifetime is already implemented: event 5750300 enables
18002347 and 18002379 with golden SFX while defeat flag 1055420915 is off, and
clears them when loading a completed encounter. Event 5750303 clears them after
victory. Retain this behavior instead of adding the superseded key condition.

Hadeon's actor is 18002354, NPC row 25000011 and ThinkParam 25009000. The current
NPC has 1000 base HP and 80 base stance durability, but those are not final values:

| Contribution | Inspected value |
| --- | --- |
| Area effect 7030 | Stormveil-tier scaling: HP x1.656, attack-power rates about x1.495 |
| Effect 4410 | HP x2 |
| Boss modifier 7380 | HP x2, stamina attack x1.666, received stance damage x0.777 |
| General HKS base modifier 7360 | Normally applied unless effect 297000 is present: HP x1.5, attack rates x1.5, received stance damage x0.75 |

The listed resident HP contributions nominally produce 6624 HP; adding the general
base contribution produces 9936. These are conditional arithmetic baselines, not
observed HP. Verify effective state/category behavior before choosing final values.
The current layering is substantial enough that 1000 base HP cannot establish
fresh-character suitability. Examine guard stamina, stance recovery, attack
recovery and starting-class equipment as well as direct HP damage.

Events 5750305/5750306 also start a player-support worker after 30 seconds. Its
random branches apply a large heal, Thorn Ward or Shriek to player 10000. These
are not Hadeon self-heals. Preserve their role pending observation, but do not
make random rescue the only way an otherwise overtuned mandatory fight is viable.

All 38 inspected map collision parts have EnableFastTravelEventFlagID=0.
PlayRegionParam rows retain original dungeon/boss metadata (including 18000800 and
18000850), not a Hadeon travel gate. Starting respawn 18002020 and Grace assets
18001950/18001951 exist; their position relative to the seal must be tested.

Sources: [shrine events](../src/events/m18_00_00_00.emevd.dcx.js),
[common helper reference](../src/events/common_func.emevd.dcx.js),
[enemy HKS](../mod/action/script/c9997.hks), and
[existing persistence design](NEMESIS-PERSISTENCE.md).
Native scratch evidence and reader: `.codex-temp/hadeon-seal-review/`.
Map SHA-256: `80C52F903A95CF788456D2A4BDC8C15130CB09593A17B278B20EE4F24F14E85E`.
Regulation SHA-256: `4AC33E616ABEB4CDAC6242AD12B377133277FE656D1D5C3F23896BE2E43241DF`.
Outer barrier 18002379 is approximately (-120.417, 12.965, 9.826), near the
key/Grace area; older placement snapshots are superseded.


Recommended implementation
--------------------------

1. **Remove the local key gate.** Replace this map's key-helper/seal initialization
   with deterministic removal of seal 18001573 and the obsolete statue/key props,
   or remove those parts in Smithbox and remove their event callers together.
   Preserve the ordinary shared helper for other dungeons. Disabling only the
   visible statue would leave the blocking seal unresolved. Explicit removal is
   preferable to silently consuming keys or repeatedly simulating key use.
2. **Retain defeat-controlled barriers.** Keep the current startup/victory rule.
   Verify the outer barrier blocks the exit, the inner barrier protects the
   crystal, and neither blocks the route to Hadeon or the usable retry area.
3. **Use Hadeon's defeat flag for native travel gating.** Qualify
   EnableFastTravelEventFlagID and point the relevant dungeon floors at 1055420915.
   This can avoid a new mirrored completion flag. Verify Grace and original
   PlayRegion restrictions too; do not fake another boss's defeat. Return-item
   restrictions are a separate check and may require scoped PlayRegion settings.
4. **Make the opening retry loop reliable.** Prefer existing internal Grace/respawn
   facilities if they work. Add a scoped respawn correction only if needed. Test
   death, Stakes, return items, rest, reload and simultaneous victory/death.
   Preserve refill access and stop any forced respawn behavior after victory.
5. **Tune Hadeon locally for starting equipment.** First measure effective HP,
   damage, guard stamina and successful-deflect/stance behavior. Trial removal of
   the extra 4410 HP doubling and replacement of Stormveil scaling with an early
   baseline; reassess the remaining boss modifier locally. Do not weaken shared
   7380/7360 or every Crucible Knight. Keep advanced tools/Oaths unnecessary for
   this first encounter, and teach the actual deflect input before requiring it.
6. **Review the whole mandatory route and early rewards.** Check any remaining
   poison, chariots, encounters and traversal requirements on the route, not just
   Hadeon. His current reward is Erdtree's Favor +3 (1043), whose inspected fields
   are HP x1.045, stamina x1.115 and equip load x1.095. Victory also exposes the
   Bindseal rite and crystal choice. Confirm those early rewards are desired;
   do not silently move or weaken them.

A suggested first-playtest target is a readable, forgiving introduction to
successful deflection and counterattack, with recoverable ordinary mistakes and
consistent stance opportunities. Exact HP/damage numbers remain experiments,
not approved tuning. Keep the challenge interesting without requiring an Oath,
an upgraded weapon, consumable stock or a completed build to leave the starting area.


Acceptance and remaining decisions
----------------------------------

Verify fresh characters with varied starting equipment, no keys, no Oath, no
weapon upgrades, key-gate cancellation remnants, all reachable exits/floors,
Grace/Stake/death recovery, rest/refills, return items, reload, Hadeon victory and
simultaneous death, existing progressed saves, NG+ and host/client ownership.
NG+ and existing saves need explicit treatment; a local gate must not become an
unrelated global travel prohibition.

Compare only intended event/map/parameter changes through the qualified workflow.
Record real game observations in [TEST-MATRIX.md](../TEST-MATRIX.md). Most encounter
assets and defeat persistence already exist. Keyless entry and local travel gating
are bounded changes; fresh-character combat and route tuning are the main work.
