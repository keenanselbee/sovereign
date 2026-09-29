# Checks and recovery

## One-time layout migration

```powershell
python tools/layout_workflow.py plan
python tools/layout_workflow.py apply --receipt <reviewed-layout-receipt>
python tools/layout_workflow.py restore --receipt <applied-or-interrupted-layout-receipt>
```

The one-time migration is complete. Do not apply an old plan again. The commands
remain available for inspected recovery; a new clone already uses the final layout.
Review the plan's complete old/new file map. Apply verifies and independently backs
up all inputs before moving any file, rejects new source members and existing targets,
then changes the catalog after output verification. It does not edit Vortex, live
files, external editors, old receipts or unclassified files. Empty directories remain.
The receipt maps historical paths to their new locations. Earlier catalog-dependent
handoff receipts are historical evidence; do not blindly replay them after migration.
Restore reverses a complete or interrupted move only if no affected file/catalog has
later edits. Inspect failed backup preparation before retrying the same receipt.

## Checks

```powershell
python -m unittest discover -s tools/tests -v
python tools/sovereign.py check
```

Requalify affected native routes after tool/library/options changes. Build receipts
and fixture tests do not mark manual gameplay acceptance Passed.

## Opening follow-up sources

`src/recipes/hadeon-followup/Program.cs` owns the guarded native regulation/map
patch. Build instructions and baseline requirements are in
[its README](../../src/recipes/hadeon-followup/README.md).
`src/textures/tutorial/build.ps1` rebuilds the paired texture archive;
see [its README](../../src/textures/tutorial/README.md). The independent
scene, reusable panel and icon remain in `images/mockups/deflection-v3/`.
These catalog recipes identify ownership; they do not automatically rebuild,
accept, deploy or replace arbitrary newer editor saves.
