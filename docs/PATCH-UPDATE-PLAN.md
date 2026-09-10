# Four-file compatibility update and staging plan

Status: applied and hash-verified across repo, Script/Smithbox authoring workspaces,
Vortex and live Game/mod after the author explicitly requested the full handoff.
23 destination paths were verified; 17 physical writes preserved six existing
Vortex/live hardlink pairs. Gameplay testing remains pending.
The subsequent effects, icons and older-menu update is recorded separately in
[EASY-COMPATIBILITY-UPDATE.md](EASY-COMPATIBILITY-UPDATE.md).
Candidate: `.codex-temp/patch-update/1789010945649542400/`.
Independent backups and handoff journal:
`archive/game-updates/2026-09-09_to-steam-25080141/01-events-and-dlc02-text/`.
Use its relocated `restore-map.json`; originals are in `before/`. Historical
candidate/diagnostic files remain in scratch, with an archive pointer at the old
backup-run location. See the [archive catalog](../archive/CATALOG.md).
Durable entry-level merge evidence: [patch-updates/steam-25080141.json](patch-updates/steam-25080141.json).
See the candidate `REPORT.md` and `receipt.json` for pre-handoff qualification.
Updated from the event/text audits and rebuild qualification on 2026-09-09.
Follow the file-specific procedures in `AGENTS.md`.

## Completed candidate checks

- Common contains exactly the two planned new events and their initialization calls;
  both added event bodies match current vanilla decoded data. Other events and metadata
  are unchanged. The source diff adds 27 lines and removes none.
- The common_func reference adds helper 900005590 (19 added lines, none removed).
  All 256 existing helpers compile unchanged. The new helper's diagnostic compilation
  has the previously observed compiler representation/parameter differences from
  vanilla; its compiled binary is excluded from the three-file runtime payload.
- Both text binders match the complete binary merge expectations: 195 item / 72 menu
  custom differences and 318 item / 33 menu upstream changes, with no conflicts.
  Nulls, literal `%null%`, empty/whitespace text, entry order and metadata are preserved.
- The author corrected the saved Smithbox menu before this build; it now matches the
  repo, Vortex and live baseline. All original recorded inputs still match their
  pre-build hashes at candidate verification. The subsequent scoped handoff is complete;
  game testing is still pending. All five authoring targets, including both Smithbox
  text binders, and the runtime/source mirrors match the accepted candidate hashes.

## Intended changes

| File | Change | Acceptance |
|---|---|---|
| common.emevd.dcx | Edit existing Sovereign JS: add events 780 and 6911 and initialize them from events 0 and 50 respectively, retaining vanilla order/guards | DarkScript build; decoded diff limited to the intended additions |
| common_func | Compare and refresh the authoring reference from verified current vanilla, retaining intentional custom source changes if found | Check source differences and callers; no new runtime override |
| item_dlc02.msgbnd.dcx | Merge current vanilla with 195 repo differences identified by the binary audit | Preserve 318 upstream entry changes and all agreed custom values |
| menu_dlc02.msgbnd.dcx | Merge current vanilla with 72 repo differences | Preserve 33 upstream entry changes and all agreed custom values |

Counts describe the audited snapshots; regenerate the binary comparison if inputs
change. The current baseline was extracted from installed game archives associated
with Steam build 25080141. Recheck installation provenance before beginning.
These are three runtime replacements plus one authoring-reference update, not four
runtime files. Shrine gameplay fixes remain separate. Icon archive candidates were
subsequently qualified and applied in the easy compatibility update linked above.

## Qualified tools and current confidence

- **common: high confidence for a targeted merge.** Existing Sovereign common source
  rebuilt byte-for-byte. Use DarkScript through the repo event builder; do not replace
  it wholesale with a decompiled/recompiled vanilla file. That vanilla round trip
  changed instruction representation and parameter metadata.
- **common_func reference: high confidence after source review.** The new helper
  900005590 belongs in the current reference. The vanilla decompile/recompile is not
  qualified as an exact runtime replacement, and the repo does not ship this override.
- **Text: high confidence for the merge.** Independent binary comparison found zero
  direct upstream/custom conflicts. Direct binary FMG read/write plus WitchyBND
  container packing preserved all inspected text and metadata in all four samples.
  This qualifies the route, not an as-yet unwritten production merge tool.
- Gameplay compatibility remains untested. No numerical confidence estimate replaces
  the candidate diff and game acceptance checks.

Use WitchyBND basic binder unpack/repack with effective recursion disabled; edit
FMGs directly through the tested SoulsFormats library. Preserve null, literal
`%null%`, empty and whitespace-only text separately. The recursive XML route failed
that preservation check and its old 194-item-difference count is superseded.

## Build one independent candidate

Use `.codex-temp/patch-update/<run-id>/` under the C: repository:

```text
baseline/       independent copies and original source/destination hashes
sources/        edited JS, reference source and binary text merge specification
work/           compiler and unpack/repack working directories
payload/mod/
  event/common.emevd.dcx
  msg/engus/item_dlc02.msgbnd.dcx
  msg/engus/menu_dlc02.msgbnd.dcx
verification/   decoded before/after comparisons and checks
receipt.json    provenance, tool hashes, source hashes and exact output hashes
```

1. Snapshot repo, editor and intended destination files. Record missing files as
   missing. Inspect hardlinks and independently copy backup bytes into C: scratch.
2. Resolve the saved editor discrepancy before choosing a source: at the audit,
   Smithbox item matched the repo, but Smithbox menu reverted 72 repo customizations
   to historical vanilla. A newer timestamp did not mean newer content.
3. Apply the event additions and generate an entry-level binary text merge plan with
   expected old values. Preserve all other entries, file IDs/paths, flags and metadata.
4. Rebuild the candidates in scratch. Compare against the agreed inputs and current
   vanilla. Check every preserved customization and every upstream change, including
   the literal `%null%` at ArtsName_dlc01 entry 4151.
5. Record the final payload hashes. Recheck all input hashes. If a new save or editor
   change invalidates the baseline, revise the candidate instead of overwriting it.

The `payload/mod` directory is a verified source of the three replacement binaries,
not a new Vortex mod. No patch ZIP or separate test overlay is required. Keep the
receipt with the candidate so propagation can be checked against its exact hashes.

## Repo and editor acceptance

After candidate review, copy the accepted bytes/source from this single candidate:

| Purpose | Repository | External authoring workspace |
|---|---|---|
| Common source | event/src/common.emevd.dcx.js | Z:/Modding/Elden Ring/Script/src/common.emevd.dcx.js |
| Common compiled output | event/common.emevd.dcx and existing event/src/common.emevd.dcx mirror | Z:/Modding/Elden Ring/Script/src/common.emevd.dcx |
| Shared source reference | event/src/common_func.emevd.dcx.js | Z:/Modding/Elden Ring/Script/src/common_func.emevd.dcx.js |
| Item text | msg/engus/item_dlc02.msgbnd.dcx | Z:/Modding/Elden Ring/Smithbox/msg/engus/item_dlc02.msgbnd.dcx |
| Menu text | msg/engus/menu_dlc02.msgbnd.dcx | Z:/Modding/Elden Ring/Smithbox/msg/engus/menu_dlc02.msgbnd.dcx |

Do not create a runtime common_func override during this handoff. Recheck target
hashes, preserve rollback copies, and reload the affected editor documents before
further saves. This is a coordinated handoff, not an atomic transaction across all
files: if one step fails, stop and report/restore the affected targets before continuing.
The existing item propagator excludes menu text; include an explicit matching menu
copy to all three destinations or add that file to the text propagation workflow.

Keep the common JS and its compiled outputs in the same eventual commit; keep the
common_func reference update with that event work. Text compatibility can be a separate
commit containing both binders and its merge evidence. Review/stage only the intended
files when Git staging is requested; do not commit pre-existing regulation/map changes.
Maintain a durable merge manifest with logical entry IDs and before/after hashes when
implementing the update, so its source intent does not exist only in disposable scratch.

## Propagate using the existing workflow

The author prefers the existing simple flow:

```text
Build and verify in C: scratch
    -> update the agreed Script/Smithbox authoring files
    -> run propagation to repo + Vortex staging + live Game/mod
    -> verify hashes and test in game
```

The event and item scripts use `FileSystemObject.CopyFile(..., True)` to overwrite
all three destinations with the same source content. They do not invoke Vortex or
update its database. Updating both its staged and deployed paths keeps their content
aligned, which is consistent with the author's working experience. Do not promise
that Vortex can never report an external change or a deployment conflict.

The read-only hardlink check found all three affected runtime files shared between:

- `Z:/Modding/Elden Ring/Vortex/Sovereign/mod`
- `Z:/Steam/steamapps/common/ELDEN RING/Game/mod`

This does not require a separate patch mod. It means propagation is a live update,
not an isolated staging step: in-place writes through a hardlink can affect both
paths immediately. Do candidate editing and verification on independent scratch
copies first. No link surgery, extra Vortex mod or new deployment framework is needed.

1. Finish the candidate and record its hashes before changing authoring/deployed files.
2. Close the game, avoid concurrent Vortex deployment/editor saves, and independently
   back up affected authoring, repo and runtime bytes into C: scratch. Backups must be
   copied bytes, not hardlinks. Record the original hashes for rollback.
3. Hand off the verified JS, common output and both message binders to their authoring
   locations. Preserve the repo's menu customizations rather than copying the older
   Smithbox menu over them. Reload affected editor documents before further saves.
4. Use the existing event propagation workflow after compilation. It does not compile
   JS: it copies existing DCX files and all non-.bak source files. It excludes
   common_func.emevd.dcx from runtime roots, which is the intended behavior. It copies
   more than common alone, so check the remaining source files agree with their
   destination baselines before running the whole script.
5. Use the existing item propagation for item_dlc02, and include menu_dlc02 through an
   explicit three-destination copy or a small update to the text propagator. Anchor
   execution to the Smithbox directory because the current item source is relative.
   Do not run unrelated map, regulation, animation or SFX propagation for this update.
6. Verify the three runtime files in repo, Vortex and Game/mod against the candidate
   hashes. Check the common JS/reference and source-side compiled mirror as well.
   The current item script reports copy errors but continues and still chimes; the
   sound alone is not success. On failure, stop and reconcile partial copies.
7. Test using the normal game-folder launcher. A separate Vortex deploy is not an
   additional required step merely to copy bytes already written by these scripts.
   If Vortex subsequently reports external changes, inspect the affected files and
   preserve the intended candidate using the receipt instead of a blanket response.

Rollback: with the game closed, restore matching backup copies to the authoring,
repo, Vortex and live paths, then verify their original hashes. Restore source and
compiled output together. File rollback does not undo save progression; use a separate
backed-up test save for regalia cleanup or progression changes.

The minimal script improvements worth making when implementation is requested are
adding menu_dlc02 to text propagation, anchoring relative source paths, and making
copy failure produce failure rather than a success chime. Keep the familiar shortcuts
and destinations. This planning update does not edit external scripts or run propagation.

Vortex background reference:
[External changes and deployment links](https://github.com/Nexus-Mods/Vortex/blob/master/docs/mod-management/EXTERNAL-CHANGES.md).

## Game acceptance

- New and existing saves: startup, rest/warp and quit/reload.
- Regalia initialization/selection/cleanup under the intended DLC conditions; preserve
  vanilla guards and record inventory/flag effects.
- New item names/descriptions, class labels/help and Torrent appearance menu text.
- Existing Sovereign names, descriptions and custom menu entries remain correct.
- Recheck the three live hashes and relevant loader logs for the tested run.

Record actual results with the candidate receipt/build and test-save context. Missing
icons are a separate asset issue; this update alone is not a complete Tarnished-content
or shrine-correctness release.
