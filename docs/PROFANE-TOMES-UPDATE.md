# Profane Tomes as an in-game guide

Author-approved implementation, 2026-09-20. Eight optional volumes explain the
mod through Magus Gyre's research. This targets fresh saves: no migration,
renumbering of previous versions, or repair of old shared flags. Normal NG+
retention remains part of the design. Gameplay acceptance is still pending.

Flag correction implemented 2026-09-20: collection, availability, hat, and stock
flags now use the valid saved `1055424xxx` block. The original `1055421xxx`
allocations were invalid despite passing earlier static tests. The generator now
rejects invalid/temporary/foreign blocks and overlapping stock allocations. See
[the flag reference](EVENT-FLAGS.md) and
[the correction implementation](ONBOARDING-FLAG-FIX-PLAN.md). Gameplay tests remain pending.

The six new guides teach existing abilities; finding or reading The Mortal
Vessel is not required for deflects to charge ultimates. The two existing Farum
Azula tomes retain their crafting and Ancient Dragon Communion progression.

## Distribution

Numbers reflect acquisition order, not the order in this table. A merchant shows
the subject title; acquisition creates the corresponding numbered inventory book.
Each subject is collected once. Extra sources stop offering it after collection.

| Subject | Source | Price or chance |
| --- | --- | --- |
| The Mortal Vessel | Kalé | 500 runes |
| The Watching Star | Isolated Merchant, Weeping Peninsula | 1,000 runes |
| Borrowed Divinity | Brother Corhyn; existing Stormveil Arteria Leaf lot `10000250` | 1,000 runes; fixed pickup |
| The Hunger of Dragons | Nomadic Merchant, southern Caelid | 1,500 runes |
| Fire Remembered | Selected Fire Monks; Nomadic Merchant, Mt. Gelmir | Separate 5% drop; 2,500 runes |
| Elderblood | Existing Farum Azula pickup reached through the Four Belfries | Unchanged lot `13000830` only |
| The Price of Power | Hermit Merchant near Leyndell; existing Mohgwyn Arteria Leaf lot `12050330` | 2,500 runes; fixed pickup |
| To Become Sovereign | Existing Farum Azula Ancient Dragon Prayerbook replacement | Unchanged lot `13000120` only |

The two leaf replacements give one book instead of their previous stack of leaves.
Map geometry and placement are unchanged. Exact corpse landmarks still require
an in-game check; the source evidence establishes the lot and dungeon.

Fire Monk NPC rows `39000000`, `39000020`, `39000032`, and `39000050` reference
the `390000000` loot group. The added row `390000007` follows its seven original
rows, giving a separate 50/1,000 book roll without changing gear/material odds.
Item Discovery does not affect that roll. This is not a claim that every Fire
Monk variant can drop it. The collection flag disables the book roll after
collection, including when the book was purchased.

Merchant rows `100521`, `100670`, `100379`, `100828`, `100799`, and `100748` are
inside the existing merchant and applicable Bell Bearing shop ranges. Each has
one copy and a separate stock counter and visibility flag. Dialogue is unchanged.

## Data and event ownership

The authored captions and allocations live in
[the manifest](../src/tomes/profane-tomes.json).
[The generator](../tools/profane_tomes.py) produces guarded parameter/text plans
and the marked controller in [common events](../src/events/common.emevd.dcx.js).

- Receipt Goods `8870` and `8871` retain the two original pickup IDs. New receipt
  Goods `8872` through `8877` cover the six added subjects.
- Goods `88000` through `88063` are the eight numbered forms of each subject.
  Their individual award lots are `880000` through `880630`, stepping by ten.
  The gaps matter: consecutive lot IDs form one combined award group.
- Event `5750140` is a single host-only controller. It grants the first unused
  discovery number, waits for the numbered book to exist, then removes its receipt.
  Already owning that subject removes only a duplicate receipt. Interrupted grants
  resume from inventory state. If multiple receipts arrive simultaneously, manifest
  order breaks the tie.
- Collection flags `1055424200` through `1055424207` suppress duplicate sources.
  Availability flags `1055424300` through `1055424307` control shops. Stock counters
  start at `1055424500` through `1055424570`, stepping by ten to avoid overlapping
  stored values. These allocations were unused in the inspected source/parameters.
- Books cannot be sold, discarded, traded, or stored. Their Goods rows retain them
  through NG+. The controller restores collection/knowledge from retained inventory;
  discovery numbers do not restart each journey.
- Recipe events `5750035` and `5750036` require the actual subject book. Retained
  crafted equipment, including storage, hides its recipe. The original crafted
  receipt conversion and Greatbow unlock remain intact. No recipe costs change.
- Owning Elderblood restores knowledge/pickup flag `1055420240`; owning To Become
  Sovereign restores `1055420245`. Owning the Staff restores Greatbow flag
  `1055420220`, supporting NG+ knowledge retention.
- Gyre's War Hat remains in slot eight of Small Dragon lot `450542001`, with
  its existing weight and Dragon Flesh outcomes. Its acquisition flag is now
  independently `1055424400`; the controller also restores that flag from owned
  armor in NG+. There is no old-save collision repair.

The two original volumes still gate their existing progression through ownership.
Opening the inventory description is never an additional mechanical requirement.

## Qualification and remaining checks

Parameter building first qualifies unchanged serialization, then compares every
decoded row against the exact expected result and verifies binder members after
encryption. The change adds 70 Goods, 64 award lots, six shops, and one enemy lot;
only the two original Goods, two leaf lots, and hat flag are edited in place.
Other parameter rows and tables are preserved.

The item binder changes 216 entries across GoodsName, GoodsInfo, and GoodsCaption.
The existing FMG patch route supports explicit `beforeMissing` additions. Complete
expected decoded comparison passes, including untouched FMGs and binder metadata.

Native event comparison limits changes to initialization event `0`, recipe events
`5750035`/`5750036`, and the new controller `5750140`. Other runtime events remain
equivalent. The controller reuses one explicit OR condition group, clearing groups
at waits to respect the engine's finite condition-group allocation.

Source execution tests cover arbitrary discovery order, eight distinct numbers,
duplicate receipts, delayed awards, reload after delivery, NG+ restoration,
host-only writes, independent hat knowledge, and existing recipe conversions.
Manifest tests check allocation separation, the two exclusive placements, Kalé's
price, and source regeneration consistency. These checks do not establish actual
shop refresh, drop behavior, item notification layout, or NG+ behavior in game.
Use ER-048 through ER-052 in [the test matrix](../TEST-MATRIX.md).

Local candidate receipts and preserved before-images are under
`.codex-temp/profane-tomes-implementation`, `.codex-temp/profane-tomes-final`,
`.codex-temp/event-builds`, and `.codex-temp/binder-candidates`.
This implementation does not stage, deploy, commit, or publish a release.

Original implementation evidence, superseded for regulation/common events by the
[flag correction](ONBOARDING-FLAG-FIX-PLAN.md):

| Artifact | SHA-256 |
| --- | --- |
| `mod/regulation.bin` | `669e846c353eb20f76e69ceb7967caefcf9b0b59d030df161691143590034b95` |
| `mod/msg/engus/item_dlc02.msgbnd.dcx` | `89d90bc0b48ea8457fb0075556854b64a7657d83ae13a1aaf77d96c566d799b7` |
| `mod/event/common.emevd.dcx` and its source companion | `b5688c2d0af241b39fd4908b84f6e8c9fa2d4a89921a17c268b6f58d4185461e` |

The acceptance journal is `.codex-temp/profane-tomes-final/acceptance.json`.
Final event qualification is `.codex-temp/event-builds/1789939310972148600/receipt.json`;
the item-text qualification is
`.codex-temp/binder-candidates/1789938628522489900/receipt.json`.
All 130 Python tests and all six tome event tests pass, as do repository preparation
and whitespace checks. The author-approved editor sync completed on 2026-09-20:
regulation and item text in Smithbox, plus common event source/binary in Script.
All four destinations match the reviewed repository bytes. Recovery receipts are
under `.sovereign/handoffs/4ff565872c224d9296968061e2616b21`,
`91faf3cc7729478baae07e441bc04994`, and `4be872a9933a4145956b88b3f0b117e0`.
This editor sync is not a game deployment.
