Memory of Grace 1.7.1
====================

Memory of Grace now disables its rune-clearing flag while preserving the native
return-to-grace behavior. Only SpEffectParam 3226 clearSoul changes from 1 to 0.
EquipParamGoods 115 and all other parameter fields remain unchanged. The English
short description, effect paragraph and confirmation describe the return without
mentioning runes. The item name and surrounding lore are unchanged.

The [incremental recipes](../../src/recipes/memory-of-grace/README.md) use guarded
baseline values. Current repository and saved Smithbox inputs matched before edits.
The parameter builder passed exact unchanged-table roundtrip, expected-row readback
and preservation checks. The text builder's complete decoded result matches the
three intended replacements, preserving all other entries and binder metadata.

Parameter candidate receipt: `.codex-temp/memory-grace-171/regulation.bin.receipt.json`.
Text candidate receipt: `.codex-temp/binder-candidates/1790642211621351900/receipt.json`.
Pre-edit recovery: `.sovereign/backups/memory-grace-171/manifest.json`.
Regulation SHA-256: `5bc646a4aac046e5b6b9458513c2be22dd00cce0532ef8e513f9245b92413051`.


Game acceptance
---------------

Pending: use with held runes and verify return to the last visited grace with the
same balance. Repeat with an existing dropped-rune pile and verify it survives.
Check confirmation/cancel, animation, item reuse, supported use restrictions and
existing saves. Retreat from Hadeon must not count as a death or grant another aid
tier. No death, aid, boss or encounter event was changed by this patch.


Editor handoff
--------------

Both guarded handoffs completed: regulation through
`.sovereign/handoffs/5398149c6d2c49e3ab44179fab781c0c/receipt.json`, and item text
through `.sovereign/handoffs/acc9494f57fd418d8c72d44fea856c29/receipt.json`.
The latter also refreshed the three affected recovered FMGs and their manifest.
Scoped whitespace and relative documentation link checks pass.


Deployment
----------

Repository preparation and version checks pass. Prepared main package:
`.vdb/prepared/736d4daf01bb47298b5ae7832efcaa4d/receipt.json`.
Only regulation.bin and the English item binder differ from 1.7.0.
Completed finalization:
`.vdb/finalizations/f405cb9d9ce6493298e2d9c24f2c42f6/receipt.json`.
Default profile reports 1.7.1 enabled, deployed and verified. All 79 live files
independently match size and SHA-256; evidence:
`.codex-temp/memory-grace-171/live-verification.json`. Gameplay remains pending.
