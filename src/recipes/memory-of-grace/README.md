Memory of Grace
===============

The 1.7.1 change disables only `SpEffectParam` 3226 `clearSoul`. Goods 115 keeps
its native effect reference, use animation, confirmation, restrictions and reusable
behavior. The effect's `stateInfo` and `heroPointDamage` remain unchanged.

`params.patch.json` guards the complete 1.7.0 regulation hash and original field.
Build an isolated candidate with `tools/tome-params/TomeParams.csproj`, passing
the input regulation, this patch, a new output path and the Smithbox tool root.
The builder verifies native roundtrip and preservation of unrelated data.

`text.patch.json` changes only GoodsInfo 115, GoodsCaption 115 and GoodsDialog
10011954 in the English item binder. Apply through `tools/format_workflow.py`
unpack/build, using the [qualified workflow](../../../docs/workflows/build-and-handoffs.md).
The accepted output already contains these changes; do not replay the original
patch against it. Rebase expected values deliberately for later game updates.

The name and surrounding lore stay intact. Player-facing effect text reads
"Return to the last site of grace visited." The confirmation uses a question mark.
Native validation is complete; rune retention and encounter retreat need gameplay
acceptance. See the [evidence](../../../docs/test-results/2026-09-28-memory-of-grace-171.md).
