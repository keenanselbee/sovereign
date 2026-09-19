Historical workflow preparation notes
=====================================

These are chronological implementation notes and superseded gates. See
[the current checkpoint](WORKFLOW-PREP-CHECKPOINT.md) for the final layout and status.
Old receipt paths are retained as recorded; the archive now lives under
`Z:/Backup/Elden Ring/archive`.

# Workflow preparation checkpoint

The active goal covers repository/workflow stages S1-S6, not gameplay implementation
or publication. The full pre-work repository backup is recorded in the
[repository plan](REPOSITORY-AND-RELEASE-PLAN.md). No commits were made.

## Completed local work

- Accepted the verified 576-member a0x binder into repo and active DSAnimStudio,
  preserving `a984_032400.hkx`. Accepted all three Hadeon c2500 binders into the repo.
  Five destinations verified; original/accepted bytes and recovery records are in
  `archive/workflow-prep/20260910-224802-assets/receipt.json`. Live/Vortex were not
  modified by that handoff. No active a0x `.dsaproj` was found.
- Added an asset catalog: 69 main runtime files, three separate texture files,
  1,118 owned source/metadata files including verified player source folders,
  SFX packing XML and six exact runtime ESD companions.
  Torrent files remain owned by their separate mods. Optional editor copies and
  the exact regulation row-name equivalence are explicit.
- Added drift-checked repo/editor handoff plans, independent recovery backups,
  atomic file replacement, interrupted-operation restore and companion guards.
- Added the shared VDB client adapter and stage-only main/texture packages.
- Added fresh-scratch BND/FMG, ESD and SFX adapters alongside the event builder.
- Recorded final armor conversion and per-journey Hewg reward decisions in the
  [feature plan](FEATURE-CORRECTNESS-PLAN.md); those mechanics are not implemented here.

The current package comparison reads the selected VDB main stage: 70 files,
347,720,188 bytes, no differing repo runtime files. The extra main file is the
existing `mods/Scripts-Data-Exposer-FS.dll`; its release provenance gate remains open.

The current unapplied migration map is `.sovereign/layout/1789113764058678000/receipt.json`:
519 files, 1,989,940,099 bytes, each with original/target path and SHA-256. It proposes
`mod/`, `src/` and `packages/textures/mod/` roots. The two root `MapStudio` files are
explicitly unclassified and remain in place; `_` publishing/art folders are retained.
Target texture ignore rules are installed in advance. No runtime/source directories
were moved and no legacy propagator was replaced. The previous 513-file plan is
superseded. The 671 files now accepted under `src/player/` already use their final
source root and are retained there rather than moved again.

## VDB stage evidence

Both byte-identical packages staged successfully with activation unchanged:

| Package | Local version | Build ID | Files |
| --- | --- | --- | --- |
| Main | 0.0.0-workflow-test | c5705ac731948b4923ca1333 | 70 |
| Textures | 0.0.0-workflow-test | fe46cb9983080cddbe556f20 | 3 |

Durable local stage receipts:

- `.vdb/prepared/e4825c1fe280450c92b0c7b77f6be6a5/receipt.json`
- `.vdb/prepared/71f711f8ecce45078c098ad49a012012/receipt.json`

Their independent prepared copies and actual Vortex stages passed complete inventory
comparison. `.vdb/selected.json` selects these exact builds for packaging. The user
disabled all Elden Ring mods; the original Sovereign staging folders remain intact.
The attempted deployment preflight found Grailwright's Test profile active and
refused before queue submission. **Sovereign activation/live-path/rollback acceptance
is still pending.** An async request asks the author to leave Elden Ring Default
(`SkC-QjDMc`) active for this check. Do not switch profiles or treat the timeout as
approval. The initially disabled state is recorded; VDB cannot restore that state
through its retained-build rollback operation alone.

## Native qualification and source limits

| Route | Observed result | Evidence |
| --- | --- | --- |
| Events | All nine shipped files decoded-equivalent; common_func authoring-only, no packed baseline | `.codex-temp/event-builds/1789108142670411200/receipt.json` |
| Menu DLC02 | Unchanged basic BND/binary FMG rebuild fully decoded-equivalent | `.codex-temp/binder-candidates/1789108221172444800/receipt.json` |
| Item DLC02 | Scratch-only `%null%` to null patch changed exactly the requested text | `.codex-temp/binder-candidates/1789108277773354700/receipt.json` |
| Shared Grace dialogue | Two custom sources reproduce the current binder byte-for-byte | `.codex-temp/dialogue-builds/1789107226118550800/receipt.json` |
| Common effects | Complete specialized source plus 415 repo overrides/metadata reproduces current binder byte-for-byte; all 15,411 members compared | `.codex-temp/sfx-builds/1789107463558973500/receipt.json` |

The binary inspector includes the previously qualified read-only DFLT
envelope reader used by the SFX test. It validates compressed/decoded lengths; Witchy
still performs packing. Qualification is tied to the recorded source/tool hashes.
The new Python suite currently has 55 passing tests; local `check` passes.

An exploratory basic-unpack-to-specialized-SFX build correctly failed preservation:
generic extraction produced TPFs where specialized packing requires DDS. Its rejected
candidate remains under `.codex-temp/binder-work/1789107294273368300/`; it was not
accepted anywhere. Use the supported complete-source SFX route.

The initial dialogue comparison below is superseded by the source/header selection
fix and completed handoff described afterward. It originally found:

| Source | Current-template result |
| --- | --- |
| t112001100.py in m11_00_00_00 | Changes t112001100.esd; needs semantic review |
| t112006000.py in m60_00_00_00 | Member unchanged in the combined build |
| t601016000.py in m60_00_00_00 | Changes t601016000.esd; needs semantic review |
| t630006100.py in m61_00_00_00 | Complete binder byte-identical |

Those candidate receipts are under `.codex-temp/dialogue-builds/1789107696001432100`,
`1789107699308490100` and `1789107706672513600`. No outputs from those preliminary
runs were accepted. Generic player handoffs remain unavailable until their
source/project reconciliation is qualified.

## Dialogue source handoff completed

The decoded investigation found **zero state-group differences** in the two apparent
mismatches. Only `Unk70/Unk74/Unk78/Unk7C` differed. ESDTool chooses the last parsed
ESD as its header template, and repeated Python `-i` options replace rather than
append the source list. The original wrapper could therefore skip the first source
in a multi-source call. The corrected adapter compiles every source separately,
filters its matching ESD header, and carries the result into the next compilation.
It independently exports and compares all decoded groups/commands/conditions and
metadata, without hiding unknown fields.

Source evidence: [Compiler.MakeESD](https://github.com/thefifthmatt/ESDLang/blob/9fa7fa90849a662b36839f077e321a02f9e992f4/Script/Compiler.cs),
[CommandRunner](https://github.com/thefifthmatt/ESDLang/blob/9fa7fa90849a662b36839f077e321a02f9e992f4/Script/CommandRunner.cs),
and [ESDOptions input handling](https://github.com/thefifthmatt/ESDLang/blob/9fa7fa90849a662b36839f077e321a02f9e992f4/Script/ESDOptions.cs).
The source checkout is retained only as scratch reference under
`.codex-temp/dialogue-state-review/1789108530515282400/upstream`.

All six owned scripts now compile explicitly and reproduce their four current
binders byte-for-byte, with full decoded equality. Current qualification:
`.codex-temp/talk-qualifications/1789112046019407300/receipt.json`.
Six exact runtime ESD members were added beside the repo DSL sources; adoption record:
`.sovereign/source-adoptions/talk-20260911/receipt.json`.

A native two-source regression fixture changed one argument in each script and
verified both resulting ESD state changes, with every other member/metadata preserved:
`.codex-temp/dialogue-multisource-fixture/1789113080497946200/verification.json`.
Those synthetic edits exist only in scratch and were not accepted into the mod.

Completed handoff: `.sovereign/handoffs/edb294a84a734f8e9d0f684867d2e690/receipt.json`.
Sixteen paths were guarded; eleven required writes: four external source/ESD pairs
and three missing external packed templates. The existing m00 template and its two
source/ESD pairs already matched. Independent before/after copies are retained with
the receipt. No runtime, Vortex or live file changed. Reload these dialogue files
before saving from an editor buffer opened before the handoff.

`qualify-talk` plus `accept-plan --scope talk --from repo --qualification <receipt>`
now supports this handoff reproducibly. It refuses source, tool, catalog or companion
drift; generic unqualified dialogue acceptance remains blocked. Restoration uses the
durable backups even if the temporary qualification outputs have been cleaned up.

## Next gated steps

The earlier closed-Vortex blocker is cleared. Elden Ring Default (`SkC-QjDMc`) is
active and the bridge is fresh. Both original VDB packages are enabled and their 73
files passed real live verification. The legacy `Sovereign` and `Sovereign - Textures`
entries are also enabled; the author has been asked to disable those two entries
before the version-switch/restoration test. Preserve unrelated enabled mods.

1. Finish the Elden Ring VDB deployment and restoration checks with a stable active
   profile. Record observed live paths and unrelated enabled-mod state.
2. Finish qualified source/output handoffs and replace the legacy propagation
   shortcuts. They must not keep writing directly into Game/mod or old stages.
3. Apply the reviewed root-to-mod/src migration only after the new handoff callers
   work. Keep texture binaries ignored under their separate package root, preserve
   old receipts and move only hash-checked classified files.
4. Re-run the documented checks, then begin separately reviewed gameplay changes
   and actual manual acceptance. Do not mark the S1-S6 goal complete yet.

## Player sources and scoped propagation

Player qualification `.codex-temp/player-qualifications/1789113415601532700/receipt.json`
verified the complete loose animation folder against the accepted 665-member binder.
The behavior XML describes the selected HKX exactly; HKLib v0.1.2 reproduced its
decoded XML tree and HKX bytes. Basic BND repacking then preserved all three behavior
members and binder metadata. The separate a0x binder retains the ultimate motion.
No active c0000 `.dsaproj` was present. HKS/name files were fingerprinted as coordinated
inputs; this is not a Havok Script runtime compilation or a gameplay test.

The 671 source files were accepted into `src/player/` using the regular drift-checked
handoff, with 676 guarded paths and no runtime replacement. All 671 destinations were
verified. Receipt and independent accepted copies:
`.sovereign/handoffs/01ffd4d8dfc94d37a40b2c58176a94ea/receipt.json`.
All 1,118 catalogued repo/editor source files now agree by hash.

`python tools/player_workflow.py --from editor` (or `--from repo`) creates a fresh
qualification receipt. Pass it to the coordinated `animations` or `hks` handoff.
The handoff rejects new saved projects, input/tool drift and isolated player scopes;
it does not remove or overwrite a DSAnimStudio project implicitly.

`vdb_workflow.py prepare --from repo --scope <scope>` now starts from the selected
verified Vortex package and replaces only the scoped accepted repo runtime files.
Other scopes and the external dependency keep their selected-stage bytes.
`propagate_workflow.py plan/apply` composes reviewed source acceptance with this
scoped prepared candidate. A stage preparation failure retains the completed source
handoff and rollback receipt; it does not hide partial success or deploy anything.
The familiar external shortcuts are intentionally not replaced until the Vortex
deployment/restoration test establishes the complete route.

## Current Vortex and migration qualification

The 2026-09-11 follow-up verified the selected main build's 70 files and texture
build's three files against the deployed game bytes through the live extension.
Both operations completed with `deployed: verified`, no differences, and the selected
build enabled. Operation receipts:
`.vdb/operations/f64336fd69314831801495fa3712969f/receipt.json` and
`.vdb/operations/611d4d680df2410d9aa972e205bf12cc/receipt.json`.
This proves current bytes, not which duplicate provider wins a later deployment.

Two byte-identical versions labelled `0.0.0-workflow-switch` were staged without
activation and independently checked against the original package inventories:

- Main `9ba77a7af69c985671f18275`:
  `.vdb/prepared/48d2f59293c7456b8bafcc36df247ea9/receipt.json`.
- Textures `e3204ad3a1922f056a925b33`:
  `.vdb/prepared/f3e5dc8acb014fdfb7a698318b9171b5/receipt.json`.

The selected package pointers still name the original test builds. No deploy or
rollback was submitted in this follow-up. The intended test is to activate these
identical candidates, verify live bytes and sibling state, then rollback to the
original VDB builds while preserving unrelated enabled mods. The current profile
is no longer empty; do not use the earlier all-disabled snapshot as its restore target.
Evidence and enabled-mod snapshot:
`.sovereign/vdb-qualification/45813e6d85744343b8d1f2fa8e25cfca/receipt.json`.

`tools/layout_workflow.py` replaces the scratch-only migration planner with documented
plan/apply/restore commands. Its current plan is
`.sovereign/layout/8187a2c0743f410ab523d5f04a657cce/receipt.json`:
519 files, 1,989,940,099 bytes. It has not been applied. The tool backs up every listed
file independently, checks source membership and hashes, moves only classified files,
switches the catalog after verification, and records old/new paths without rewriting
historical receipts. Restoration refuses later edits and handles interrupted moves.
It leaves unclassified files and empty directories in place for separate review.
Deployment/restoration and replacement callers remain prerequisites to the actual move.

Propagation now rechecks full scoped path membership and qualification even when no
source copy was originally needed. A new source file or changed qualification tool
invalidates the plan. All 62 workflow tests and `sovereign.py check` pass; the new
tests cover these drift cases and layout preservation, interruption and restoration.
No game acceptance row was marked Passed.

The next continuation added `propagate_workflow.py run/resume`, composing the existing
source handoff, stage, deployment, verification and selection commands. It records
child deployment identity before submission, resumes pending requests, rejects wrong
live bytes, and binds the receipt to its explicit profile. Player/repo-dialogue
qualification is automatic when no receipt is supplied. The stage's scoped payload
must still match the reviewed source acceptance; later source drift cannot slip into
the candidate silently. VDB deploy/rollback now rejects the known legacy duplicate
providers before queueing; read-only verify remains available.

This combined path has not deployed to the real game yet. The external SFX shortcut's
build step is not wired into it; other saved-output scopes are implemented. External
shortcut replacement and the actual layout move remain pending. The live bridge
still reported both legacy entries enabled at 2026-09-11T20:16:35Z.
All 66 Python workflow tests and the 69-file preparation check pass after these changes.

## SFX propagation and launcher follow-up

The SFX build step is now integrated into `propagate_workflow.py run --scope sfx
--from editor`. The builder uses the complete current editor extraction without
overlaying older repo files. `sfx_workflow.py` validates all source membership/bytes,
candidate and tool hashes before saving the packed editor output with independent
before/after copies. Atomic replacement preserves any hardlink peers. Its restore
command uses the durable copy and refuses later packed-file edits. The propagation
receipt links this save separately from the subsequent repo handoff and deployment.
New source edits after the build invalidate propagation instead of accepting stale
packed output alongside newer source files.

Native unchanged-source qualification passed with byte-for-byte and full decoded
equality across all 15,411 members. Receipt:
`.codex-temp/sfx-builds/1789158320349879600/receipt.json`.
The following editor-save qualification retained independent recovery copies:
`.sovereign/sfx-builds/b01c2fe439534ecc9a6e41fb442ba29e/receipt.json`.
Its before/after hash is the same `e07bd8d69a499b1cafce9a4db519c4a2bf6acff043877ef2ee35f4bc2ad6628f`,
so no packed editor file was replaced. No runtime or deployed file changed.

`tools/Propagate-Sovereign.ps1` is the repository launcher for run/resume. It resolves
the repo from its own location, requires an explicit profile, passes child exit codes
through and gives routine runs a unique local development label. PowerShell syntax
validation passed. The external VBS files are still unchanged. Real version switching,
rollback, launcher end-to-end qualification, shortcut installation and the layout move
remain pending; fixtures and native rebuilds do not substitute for those checks.

The bridge again reported both legacy Sovereign entries enabled at
2026-09-11T20:25:10Z. This is the same pending transition across three goal turns:
disable only those legacy entries, retain the original VDB builds and unrelated mods,
then resume. All pending stage/verification jobs from earlier steps are completed;
there is no deployment job to poll or restart.
All 69 Python workflow tests and the 69-file preparation check pass after this follow-up.
