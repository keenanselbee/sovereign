Sovereign source files
======================

The existing folders contain editable sources and modified-file overlays.
`asset-catalog.json` owns qualified source/editor mappings. A loose extraction
does not automatically become a complete or qualified rebuild input.

Recovered members, 2026-09-25
----------------------------

[extracted-members.json](extracted-members.json) records 388 recovered files from
42 accepted runtime archives/direct files. Each entry retains the runtime hash,
original archive member name, ID, flags, compression and extracted-file hash.
Binder headers and whether the extraction contains every member are recorded.
Nested DDS entries identify their containing TPF and texture metadata.

| Location | Recovered content |
|---|---|
| `player/c0000_a0x-anibnd-dcx/` | 16 added motion HKX files |
| `models/c2500-chrbnd-dcx/` | Hadeon's modified FLVER |
| `textures/c2500_h-texbnd-dcx/`, `textures/c2500_l-texbnd-dcx/` | Two TPF members and 92 added high/low DDS entries |
| `materials/allmaterial-matbinbnd-dcx-wmatbinbnd/Chr/matxml/` | 14 additional c8000 material members already shipped in Sovereign's binder |
| `models/*-partsbnd-dcx/` | 84 members from 30 equipment archives, plus 119 nested DDS files |
| `text/*-msgbnd-dcx/` | 57 differing binary FMG members across four English binders |
| `menu/` | Three modified GFX binaries; original authoring projects remain unavailable |

The material entries preserve shipped content; extraction does not establish
original authorship. Twenty-six equipment archives have no counterpart in the
archived `Z:/Backup/Elden Ring/ER Base Files/1.17` tree. Their full member sets are
retained and marked `baselineAvailable: false`; that absence does not prove every
member is a custom modification. FMG members retain complete binary contents,
including unchanged entries; these are not semantic text-delta recipes.

The 174 raw members, 211 DDS files and three GFX files were checked against their
packed bytes and read back after copying. All 1,474 pre-existing source files
and the 42 runtime inputs were unchanged during acceptance. The local receipt is
`.codex-temp/source-extraction-20260925/accepted.json`.

Rebuilding and future edits
--------------------------

Use the manifest to locate the original runtime archive and selected members.
For partial overlays, retain the other members from a reviewed baseline. Preserve
packing metadata and qualify a scratch rebuild before accepting a runtime change.
GFX copies remain compiled graphics; extracting them cannot restore an original
FLA/project. Existing binary FMG editing safeguards still apply.

The catalog's `editing` records identify editable inputs and accepted packed
authority for each group. These recovered snapshots now participate in the
existing reviewed `accept-plan` / `accept` handoff. A changed selected archive is
read into guarded candidates; the plan includes affected loose members and the
manifest. Backups and restoration cover those changes with the normal handoff.
Independently edited loose files are accepted only when they already match the
selected packed member. Otherwise acceptance stops without overwriting them.

`check`, repository package preparation and new ZIP creation check recorded
source freshness. These checks cover the manifest's explicitly listed members;
they do not discover every newly customized vanilla member. Add newly owned
members to the manifest explicitly after reviewed extraction. Removed tracked
members and changed complete member sets stop for review. Untracked members and
textures are reported by the native reader, not imported automatically.

For groups without an editor mapping, use the existing handoff with `--from repo`
after a qualified packed edit; it can update just the recorded snapshots. No
editor mapping or automatic rebuild is inferred. HKS, name lists, maps and
regulation remain directly editable in their established locations. See
[the workflow commands](../docs/WORKFLOW-COMMANDS.md) and
[archived baseline inventory](../docs/BASELINE-INVENTORY.md).
