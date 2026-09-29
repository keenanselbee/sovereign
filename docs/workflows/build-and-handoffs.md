# Build candidates and review handoffs

## Build isolated candidates

After accepting a verified edit, syncing the affected files to the configured manual
editor workspaces is authorized by default. Follow the qualified handoff below;
preserve independent editor changes and the complete coordinated asset group.
This does not make an inspection request a sync request or authorize deployment.

```powershell
python tools/sovereign.py build-events --require-equivalent
python tools/format_workflow.py unpack --file msg/engus/menu_dlc02.msgbnd.dcx
python tools/format_workflow.py build --receipt <unpack-receipt> --require-equivalent
python tools/format_workflow.py build --receipt <unpack-receipt> --patch <text-patch.json>
python tools/format_workflow.py build-sfx --require-equivalent
python tools/format_workflow.py build-sfx --from editor --require-equivalent
python tools/format_workflow.py build-dialogue --file script/talk/m00_00_00_00.talkesdbnd.dcx --source src/talk/m00_00_00_00-talkesdbnd-dcx/t000001000.py --source src/talk/m00_00_00_00-talkesdbnd-dcx/t000003000.py --require-equivalent
```

All outputs are new `.codex-temp` candidates. `--require-equivalent` is an unchanged
source qualification, not a flag to use after an intentional edit. Events use
DarkScript and an independent EMEVD reader; `common_func` stays authoring-only.

Text uses basic Witchy BND extraction/packing and a binary FMG writer. A patch is an
array of `{ "file": "Example.fmg", "id": 123, "before": "old", "after": "new" }`.
Both values are required; JSON null, empty text, whitespace, Unicode and literal
`%null%` remain distinct. Existing IDs must match uniquely. The initial adapter
replaces existing text only; additions/deletions require an explicitly extended and
tested patch route. Do not hand-edit FMG/XML outside this patch route and then accept
a build based on partial comparison. The full decoded expected result must match.

The accepted Cave of Knowledge dialogue and Deflection wording has four durable,
guarded recipes. `asset-catalog.json` maps them to their binder outputs; these
recipes are authoring inputs and are not automatic editor handoff companions:

- `src/text/opening-dialogue-tutorial/item_dlc02.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu_dlc01.msgbnd.dcx.patch.json`
- `src/text/opening-dialogue-tutorial/menu_dlc02.msgbnd.dcx.patch.json`

Their `before` values guard the pre-edit binder text. Current accepted outputs
already contain the `after` values, so do not reapply the patches to those outputs.
For a later rebuild from qualifying earlier inputs, unpack each matching binder,
apply its own patch through `format_workflow.py build --patch`, review the complete
decoded result, then qualify and accept the source/output under the normal workflow.

Basic BND edits produce a complete decoded inventory for review. Intentional member
changes still need a preservation specification. The wrapper rejects output/member
path redirects and changed input/tool fingerprints. Do not use basic BND mode for
specialized animation, SFX, texture-pair or graph edits.

SFX builds copy the complete configured editor extraction into scratch, overlay the
repo's accepted overrides/packing metadata, then use specialized Witchy packing.
The full extraction includes DDS textures; a basic BND unpack produces TPFs and is
not an interchangeable source. Every full/overlay input is hashed. Keep that external
source available and synchronized. Unchanged qualification compares all 15,411
members and binder metadata, including the historical DFLT compression envelope.

The default SFX source is the accepted repo overlay plus the complete editor
extraction. `--from editor` builds the complete editor extraction as saved, without
overlaying older repo files. Both routes use isolated candidates and preserve the
existing packed output. `--require-equivalent` is for unchanged-source qualification.
For a reviewed editor rebuild/save, use `python tools/sfx_workflow.py build-save`.
It makes independent recovery copies and atomically replaces only the packed editor
output. Restore that output with `python tools/sfx_workflow.py restore --receipt
<sfx-editor-save-receipt>`. Later edits prevent restoration. This save alone does not
accept repo sources or deploy. New repo-owned SFX overrides still need explicit
inclusion in the source overlay; do not assume the whole editor extraction is tracked.

Dialogue uses ESDTool from its installation directory with the current mod binder's
real basename as template. It compiles each source explicitly, filtered to its matching
ESD so the compiler preserves that member's header. Repeating `-i` with individual
sources in one invocation replaces the source list; do not use that older recipe.
ESD `.py` files are DSL and must never be run as Python. The adapter checks member
identities/metadata, exports decoded state groups and rejects changes to other ESDs.
Intentional changes inside a selected ESD still need group/state semantic review.

Use the existing detailed [animation](../ANIMATION-UPDATE.md),
[behavior](../PLAYER-BEHAVIOR-UPDATE.md) and Smithbox recipes for other formats.
No generic Lua validator or successful archive rebuild establishes game correctness.

## Review a repo/editor handoff

```powershell
python tools/sovereign.py accept-plan --scope events --from repo
python tools/sovereign.py accept --receipt <reviewed-handoff-receipt>
python tools/sovereign.py restore --receipt <applied-handoff-receipt>
```

`--from editor` reverses the direction. Review the receipt and build evidence first.
These commands copy exact bytes; they do not prove that source and output implement
the same behavior. Plans cover scoped companions, detect conflicting duplicate
outputs, reject drift, and make independent backups before replacing destinations.
Atomic replacement avoids truncating a shared hardlink. No Vortex/live files are
written. Durable records/backups are under ignored `.sovereign/handoffs/`.

Player HKS/graph/animation handoffs require
`python tools/player_workflow.py --from editor` (or `--from repo`), followed by
`accept-plan --scope animations --from <same-source> --qualification <receipt>`.
The qualifier checks complete packed/loose consistency, graph XML/HKX roundtrip,
ultimate motion and absence of an unresolved saved project. HKS/name inputs are
guarded, but no generic compiler is used to claim Havok Script compatibility.
Native qualification is reused when its asset membership, packed/loose bytes,
names, configuration and tool fingerprints still match. HKS-only edits receive
fresh input guards without rebuilding unchanged binders/graphs. Changed assets or
tools require a full qualification; a saved DSAnimStudio project still requires
reconciliation. The complete player group remains coordinated.
Dialogue handoff is
available after `python tools/format_workflow.py qualify-talk` verifies every owned
source rebuild and its exact `.esd` companion against runtime. Pass that receipt to
`accept-plan --scope talk --from repo --qualification <receipt>`. Source/tool drift
invalidates qualification. Never apply a source-only group to evade these requirements.

Hewg's source additionally owns `.preserve.json`, `.original.esd` and `.baseline.txt`
companions. The format workflow compiles both baseline and edited DSL and transplants
only the manifest's reviewed changed state groups into the preserved original ESD.
Keep the original/baseline hashes fixed; unexpected differences require investigation,
not widening the allowed groups automatically. See the editing guide and gameplay report.

Interrupted operations retain their receipt/backups. Restore refuses later manual
edits and can recover a replacement completed before its final journal write.
Inspect leftover `.sovereign-accepting`/`.sovereign-restoring` files and locks before
manual cleanup; do not replay an interrupted operation blindly.
