Zero-quantity whistle pouch trial 1.7.0
======================================

The author reports that the HP/FP flask defaults populate the intended pouch slots
when the flasks are awarded. That observation supports trying a starting assignment
for Torrent, but owned empty flasks and an unowned zero-count whistle differ.

All twelve CharaInitParam player rows (3000-3011) change secondaryItem_04 from -1
to Spectral Steed Whistle 130. secondaryItemNum_04 remains zero. This is intended
as the bottom pouch direction; native persistence and direction require gameplay
confirmation. The whistle already has isAutoEquip=0; that value remains unchanged.
Melina's normal item-lot 100000, flags, dialogue, other pouch slots, class stats and
all other parameter tables remain unchanged. No existing-save migration or runtime
slot enforcement is introduced.


Validation and recovery
-----------------------

The [guarded incremental recipe](../../src/recipes/starting-flask-pouch/whistle-zero-quantity.patch.json)
passed original-field/hash guards, native exact unchanged-table roundtrip,
expected-row readback, unrelated-row preservation and binder/member preservation.
Each of twelve class rows has exactly one changed value; count zero is also guarded.
Evidence: `.codex-temp/whistle-pouch-170/regulation.bin.receipt.json`.

Input SHA-256: `db7e68733d1be9eb1645ac608f8030117baec328a3cd62d03a43a81a9e321d5f`.
Output SHA-256: `64ab851b859dbe70c01e0ef3d69fed8c9f98492aed5ca715522666bd92be8870`.
Independent pre-edit backups: `.sovereign/backups/whistle-pouch-170/manifest.json`.


Game acceptance
---------------

Pending: on a new character verify there is no usable whistle before the normal
award, receive it from Melina, inspect the bottom pouch and absence of an automatic
quick-item duplicate, summon Torrent, then rest/reload. Test a manually occupied
bottom slot before acquisition: the chosen item should stay assigned. Include both
new classes. Existing characters should retain their saved assignments.

A discarded zero-count assignment means this approach is unsuccessful; native data
validation does not establish that the engine will retain it. No save reset is
performed to test this behavior automatically.


Handoff and preparation
-----------------------

Guarded Smithbox handoff
`.sovereign/handoffs/c799f53fff5d4fa388757ff9c59c1f24/receipt.json` completed for
the regulation. Repository preparation, release metadata, scoped whitespace and
relative documentation links pass. Only regulation.bin differs from deployed
1.6.9. Deployment completed; game acceptance remains pending.


Deployment
----------

Prepared main package:
`.vdb/prepared/3abe83bc8126420e9c0bd70612ab3f25/receipt.json`.
Completed finalization:
`.vdb/finalizations/0ad3faaf75d747729404135bf26ed295/receipt.json`.
Default profile reports 1.7.0 enabled, deployed and verified. All 79 live main
files independently match size and SHA-256; evidence is
`.codex-temp/whistle-pouch-170/live-verification.json`. Only regulation differs
from 1.6.9. No Ultrawide/texture package change or Nexus publication occurred.
