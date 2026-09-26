Graveyard key gates and guide torches
====================================

Author-approved 2026-09-23. Implemented locally; gameplay acceptance is pending.
The subsequent [Nemesis omen update](NEMESIS-OMENS.md) restores both imp torches
to normal after Hadeon's defeat, overriding activation state, and includes this
previously sync-only gate work in local build 1.0.8.
This replaces the earlier keyless-entry proposal in [the Hadeon opening
plan](HADEON-SEAL-PLAN.md). Package build/deployment is separate from editor sync.


Behavior and ownership
----------------------

As of 1.1.7, the two statues each consume one Stonesword Key, expose their inserted-key
prop, and exchange their normal torch for the red copy. The single shared barrier
opens only after both statues are activated. Either order is allowed. Activation is
saved for the journey and must not charge the player again after rest or reload.
As of 1.0.9, the left statue uses Sovereign flag 1055420924; vanilla 18000570
is neither read nor cleared. Existing vanilla saves start with both custom locks
closed. There is no migration from previous Sovereign versions. Hadeon's existing
defeat flag alone controls his outer barrier, regardless of the vanilla door state.

All objects belong to m18_00_00_00. The author's exact placement is retained.

| Object | Left entity / part | Right entity / part |
| --- | --- | --- |
| Statue | 18001570 / AEG027_078_9000 | 18001574 / AEG027_078_9001 |
| Inserted key | 18001571 / AEG027_216_9000 | 18001572 / AEG027_217_9000 |
| Shared barrier | 18001573 / AEG099_271_9000 | Same barrier; second asset removed by author in 1.1.7 |
| Normal torch | 18001576 / AEG004_693_2121 | 18001577 / AEG004_693_2002 |
| Red torch | 18001578 / AEG004_693_2122 | 18001579 / AEG004_693_2123 |

Hadeon's entrance torch uses the reverse progression: red 18001582
(AEG004_693_2125) before defeat, normal 18001581 (AEG004_693_2074) afterward.
Existing Hadeon defeat flag 1055420915 owns this state. All red copies use model
particle offset 50, resolving to AssetModelSfxParam 4693050 / FXR 7505982.
The author explicitly confirmed normal offsets -1 for the lock torches and 10
for the Hadeon entrance torch; preserve these distinct settings.
The accidental AEG004_693_2124 duplicate was removed by the author before the edit.

Local event 5750350 adapts the native one-key interaction and restores the key
prop on completed loads. The original lower key uses socket 200 / animation
60810; the right upper key uses socket 201 / animation 60811. Confirm both
animations and physical alignment in game. Each prompt has its own temporary
flags. Shared common_func stays unchanged and authoring-only.
One call to seal worker 18002569 checks both saved activation flags and retains
native sound/SFX cleanup. Neither a single key nor Hadeon's defeat alone opens
this imp seal. There is no new flag or vanilla flag dependency. The author's
saved map removes AEG099_271_9001 and moves the remaining barrier to
(-117.98892, 14.633367, 17.897795); other decoded map fields are unchanged.
Event 5750351 restores and switches each of the three torch pairs locally; the
later omen update adds Hadeon's defeat as a priority reset for the two imp pairs.


Key rewards
-----------

Version 1.3.2 converts this actor to sword and shield: custom NPC 43519000 retains
its HP/poise/outgoing-damage tuning and key lot, while receiving sword donor
43510010's variant fields (resident effects 0/22, display masks 0/2, network warp
distance and mounted-target behavior). Map ThinkParam changes from 43511000 to
43510000. Other map fields and NPC rows are preserved. The original setup follows.

A regular Godrick Knight, c4351_9000 / entity 18000258, is added at the saved
c4300_9002 dummy's position (-116.364, -1.620973, 121.975), yaw 36.570995.
The dummy remains an inactive DummyEnemy; inspection found no active enemy within
eight metres to disable. Its dungeon draw settings and collision h001900 are
retained by the new actor. No overworld patrol or collision is imported.

NpcParam 43519000 clones the current Limgrave Partisan/greatshield knight row
43511010, with ThinkParam 43511000. Only its loot references change: enemy lot
becomes -1 and map lot becomes 18000910. Equipment, scaling and ordinary Sovereign difficulty behavior remain inherited.
The 1.0.9 local tuning sets base HP 576 -> 461, toughness 35 -> 28, and stance
durability 65 -> 52. Resident effect 1627114 multiplies all five outgoing attack
rates by 0.9 and outgoing SA damage by 0.8. Guard stamina damage is unchanged;
attack-rate reductions are not a promise of exactly 10% less post-defense damage.
The donor placement was verified in the installed-game extraction's
m60_42_37_00. Existing map model c4351 is reused.

Map lots 18000910 (knight) and 18000920 (Rick) each clone the native one-key lot
18000010: Goods 8000, quantity 1, weight 1000, no other outcomes and no luck
scaling. Each has its own saved collection flag. The knight uses native death
loot; Rick's host-only event 5750352 waits for final defeat 18000850 and awards
the second lot. The lot receipt prevents repeats, including recovery after an
interrupted victory/reload. An already-defeated Rick without the new receipt also
qualifies. No reward is added to phase one; existing Rick rewards are unchanged.

| Flag | Owner / purpose | Intended lifetime |
| --- | --- | --- |
| 1055420924 | Sovereign left statue activation (1.0.9) | Saved for journey |
| 1055420920 | Right statue activation | Saved for journey |
| 1055420921 | Knight key lot collection | Saved for journey |
| 1055420922 | Rick key lot collection | Saved for journey |
| 1055422940-1055422943 | Separate statue yes/no prompt pairs | Temporary, reset on reload and before each prompt |

No new flag uses event-slot completion. New saved and temporary allocations use
the valid blocks in [the flag reference](EVENT-FLAGS.md). Check NG+ reset and
host/guest behavior in game. Hadeon's encounter barriers, crystal, combat, rewards
and the separately proposed fast-travel restriction are unchanged by this work.


Verification
------------

Scratch candidates, guarded before-copies and the native preservation receipt
are under .codex-temp/graveyard-locks-20260923. Native map roundtrip passes;
the sole decoded map addition is the regular knight. Every existing map field
and parameter row is retained, with only the new NPC and two lots added.
All other regulation tables preserve their original bytes and binder metadata.
Event build 1790207644430129700 passes independent decoded comparison: every
existing event except the constructor is unchanged, existing relative event order
and file metadata are preserved, and only 5750350-5750352 are added. All other
runtime event candidates are equivalent. Saved source/binary qualification
1790207915013376400 passes. Compilation is not gameplay verification.

Guarded editor handoff receipts under .sovereign/handoffs are
24b6961ff71a4ae299d0e07e7d392923 (map),
97bcd66bdf064cd8a068e348cb05da3a (params), and
d73b683e394843f587c067dcd2e93386 (events). They retain independent recovery copies.
Normal completion syncs these files to Smithbox and DarkScript; reload open editor
buffers before saving. No VDB package, live deployment or release-version change
is part of this sync-only implementation.

Acceptance is tracked by ER-065 through ER-069 in [the test matrix](../TEST-MATRIX.md).
Test zero/one/two keys, both statue orders, cancelled prompts, used-statue reuse,
rest/reload after one activation, both collision layers, all three torch pairs,
knight navigation and loot, interrupted/uncollected rewards, final Rick victory,
simultaneous death, co-op and NG+. Verify that disabled torch assets remove their
automatic flame/light without lingering effects.
