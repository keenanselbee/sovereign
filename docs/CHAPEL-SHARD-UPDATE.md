Chapel maiden reward, 1.1.0
==========================

The door-preservation claim below was disproved by the author's 1.1.0 game test.
The [1.1.1 correction](CHAPEL-POLISH-UPDATE.md) documents the active item
requirement and the dormant event gate.

Author-approved 2026-09-24. Replace the maiden's Wizened Finger pickup with one
existing Darklight Shard and move the finger to Kale for 100 runes. The author
explicitly declined an acquisition hint in the full description. No new item,
caption, icon, effect, eclipse cue, dialogue or map placement is introduced.

Implementation
--------------

- ItemLotParam_map 10010000 changes only lotItemId01 from Goods 106 to Goods 1291.
  Quantity one, guaranteed weight, Goods category, rarity behavior and collection
  flag 60210 are preserved. The shard keeps its existing effect and text.
- The native Chapel event 10012504 checks 60210 to enable door 10011540, rather
  than checking finger inventory, but this event is not initialized. The active
  ObjActParam 219002 independently requires Goods 106; preserving 60210 alone
  did not unlock the door. Already-collected vanilla pickups stay collected;
  no retroactive shard or reset of the native collection flag is added.
- ShopLineupParam 100522 copies Kale's ordinary single-stock Goods row 100501.
  It sells Goods 106 for 100 runes, quantity one, with no release prerequisite or
  name override. Its independent stock counter begins at 1055424580, reserving
  the ten-bit range through 1055424589. Existing finger ownership retains the
  item's native maximum-one restriction.
- The saved dialogue's regular shop command covers rows 100500 through 100524;
  no shop-range or dialogue edit is required. The existing tome at 100521 remains.
- Full description, all message binders, events, maps, Goods and effects are
  unchanged. All 1.0.9 opening changes remain in the full package.

Verification and recovery
-------------------------

Before-copies and native roundtrip/preservation evidence are retained under
`.codex-temp/chapel-shard-20260924`. The native candidate verifies the pickup's
single changed field, the new shop row, unchanged other rows/tables and binder
metadata. The stock range is checked against parameters, runtime maps/dialogue,
and both runtime and qualified installed-game events, including range operations.

ER-079 in [the test matrix](../TEST-MATRIX.md) remains pending. Static verification
and editor/deployment checks do not establish in-game pickup or shop behavior.
