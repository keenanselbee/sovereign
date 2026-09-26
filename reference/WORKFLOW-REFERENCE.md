Historical workflow reference
=============================

Retained investigation text. Use WORKFLOW.md and WORKFLOW-COMMANDS.md for current
paths, supported commands and deployment ownership. Old counts and script behavior
are historical snapshots, not current operating instructions.

# Sovereign development workflow

See the [repository and release plan](../docs/REPOSITORY-AND-RELEASE-PLAN.md) for the current
review, Vortex Development Bridge integration, proposed layout migration and release gates.

The 2026-09-10 refresh records the verified full repository backup and stages S0-S8.
S1 ownership findings are recorded in the [file ownership review](../docs/FILE-OWNERSHIP-REVIEW.md).
The a0x/Hadeon handoffs, VDB switching/rollback and layout migration are complete; see the
[implementation checkpoint](../docs/WORKFLOW-PREP-CHECKPOINT.md) and
[current commands](../docs/WORKFLOW-COMMANDS.md) for the new catalog, handoff and format tools.
The installed shortcuts now use VDB, with main files under `mod/`, sources under `src/`,
and separate texture files under `packages/textures/mod/`. The
[feature plan](../docs/FEATURE-CORRECTNESS-PLAN.md) records the agreed Hewg handoff and
Rykard eligibility decisions separately from remaining choices and game tests.

Prepared 2026-09-09. This repository now supports inspection, isolated event builds,
Vortex-backed packaging and Nexus review/update tooling. It is not marked release-ready. See [mechanics](../docs/MECHANICS.md)
and the [manual test matrix](../TEST-MATRIX.md) before changing release claims.
The completed event/text compatibility work is recorded in
[PATCH-UPDATE-PLAN.md](../docs/PATCH-UPDATE-PLAN.md), including the verified Vortex/live hardlinks
and the author's existing three-destination propagation workflow.
The later effects, icons and older-menu handoff is recorded in
[EASY-COMPATIBILITY-UPDATE.md](../docs/EASY-COMPATIBILITY-UPDATE.md). Icons retain their separate
`Sovereign - Textures` Vortex package; they are not included by the main NEXUS packager.
The completed Grace/Torrent dialogue merge and synchronized talk authoring files
are recorded in [TORRENT-DIALOGUE-UPDATE.md](../docs/TORRENT-DIALOGUE-UPDATE.md).
The applied TAE animation merge, qualified writer route and archived DSAnimStudio
project handoff are recorded in [ANIMATION-UPDATE.md](../docs/ANIMATION-UPDATE.md).
The coordinated HKS, behavior and name-ID merge and authoring handoff are recorded
in [PLAYER-BEHAVIOR-UPDATE.md](../docs/PLAYER-BEHAVIOR-UPDATE.md). Its game checks remain pending.
The recovered custom effects and archived visual alternatives are recorded in
[SFX-RECOVERY.md](../docs/SFX-RECOVERY.md). Both active SFX source and repo modified files are synchronized.
The historical archive home is `Z:\Backup\Elden Ring\archive`. Its `README.md` and
`CATALOG.md` describe the backups and restoration records. The user manages the
relocation; verify each entry's actual location and any historical restore paths
before use. Instruction cleanup must leave archive payloads untouched.

## Commands

Run from the repository root with Python 3.11 or later. Commands resolve project
paths from the script location, so invocation from another working directory is supported.

```powershell
python tools/sovereign.py check
python tools/sovereign.py status --scope all
python tools/sovereign.py status --scope events --json
python tools/sovereign.py propagation-plan --scope maps
python tools/sovereign.py build-events --require-equivalent
python tools/sovereign.py nexus-check
python tools/sovereign.py nexus-check --descriptions-only
python tools/sovereign.py nexus-status
python tools/sovereign.py tests
python tools/sovereign.py logs --lines 60
python tools/sovereign.py package --draft --version 0.0.0-prep
python -m unittest discover -s tools/tests -v
```

`status`, `propagation-plan`, `check`, `nexus-check`, `tests`, and `logs` read files.
Builds, packages and helper binaries stay in `.codex-temp/`; accepted handoff backups
and VDB operation records stay in durable ignored `.sovereign/` and `.vdb/`.
The commands above do not deploy or launch the game. The separate VDB adapter has
explicit stage/deploy operations documented in WORKFLOW-COMMANDS. `nexus-status` contacts
the official Nexus API with read-only requests. The separate Nexus wrappers below
open a dedicated browser or publish only with their explicit save/publish options.
`0.0.0-prep` is a draft example, not the mod's selected release version.

Copy `tools/eldenring-paths.example.json` to `tools/eldenring-paths.local.json` and
adjust paths on another workstation. The local copy is ignored by Git. The example
records this workstation's authoring arrangement. An alternate config can be passed
before the command: `python tools/sovereign.py --config C:/path/paths.json status`.
Event builds also require .NET 10 SDK, the configured DarkScript3 executable and
Smithbox's local `Andre.SoulsFormats.dll` and Oodle library. These dependencies are
not redistributed by this repo. No package download or tool installation is automated.

## Source ownership and handoff

Current propagation runs **chosen source -> reviewed repo/editor handoff -> immutable
VDB stage -> Vortex deployment -> verified package selection**. Before any
gameplay edit, compare the relevant four copies and choose an agreed baseline using
content, not timestamps. A matching hash means identical bytes, not correct mechanics.
Differences can be row names alone. Unsaved editor buffers are not inspected.

1. Run scoped status. Resolve editor/repo differences and record baseline hashes.
2. Make a narrow candidate in a repository scratch run; state the intended field,
   event, flag, text or animation changes and the behavior they implement.
3. Compile with a qualified format-specific tool, reopen the result and compare
   decoded data. Verify unrelated rows, instructions, binder entries and metadata.
4. Review the exact changed behavior and required manual tests. Accept only the
   intended source and runtime outputs into the repo, retaining a rollback copy.
5. An explicitly requested editor handoff must update the matching authoring source
   and output from the same candidate, with expected-hash checks. Reload affected
   files in open editors before saving. Repository edits alone are not a handoff.
6. Explicit propagation must use the reviewed scope and destinations, preserve prior
   managed files, stop on drift, verify destination hashes, and record a receipt.
   Live testing uses the actual game-folder launcher and a backed-up test save.

`propagation-plan` is an informational preview of differences, not a deployable
transaction or approval receipt. It never chooses a winning file. The new
`accept-plan`/`accept`/`restore` commands support reviewed repo/editor handoffs;
qualified player/dialogue/SFX handoffs and the installed shortcut wrappers use the
current catalog. Do not run archived legacy scripts or modify an immutable VDB stage.

## Historical workflow observations

The following observations document the pre-VDB investigation. Counts, old script
behavior and capability tables are snapshots. Use [current commands](../docs/WORKFLOW-COMMANDS.md)
and the [editing guide](../docs/EDITING-GUIDE.md) for current operations and file paths.

### Former Elden Ring workflows

Paths below are relative to `Z:/Modding/Elden Ring`. Destination runtime paths are
relative to the repo, `Game/mod`, and `Vortex/Sovereign/mod`.

| Authoring workspace | Existing script | Runtime output / observation |
|---|---|---|
| Smithbox | propagate-regulation.bin.vbs | regulation.bin; row names to repo/Vortex only |
| Smithbox | propagate-map.vbs | map/**/*.dcx; deletes destination map trees first |
| Smithbox | propagate-item.msgbnd.dcx.vbs | English item_dlc02 binder only |
| Script | propagate-c0000.hks.vbs | action/script/c0000.hks |
| Script | propagate-c9997.hks.vbs | action/script/c9997.hks |
| Script | propagate-event.vbs | Existing compiled DCX plus source copies; does not compile JS |
| DSAnimStudio | propagate-c0000.anibnd.vbs | chr/c0000.anibnd.dcx |
| DSAnimStudio | propagate-c0000.behbnd.vbs | chr/c0000.behbnd.dcx |
| SFX | propagate-sfxbnd_commoneffects.ffxbnd.vbs | Builds with WitchyBND, then copies shared effects |

Several wrappers depend on the current directory, swallow copy errors or play their
success sound after errors. Regulation propagation deletes destination row-name files
first. SFX deletes the old local packed output before compiling. Multi-target copies
have no rollback or hash checks. Archived `_ /5` scripts (directory `_`, then `5`)
contain old destinations and are not active workflow definitions.

No active wrapper was found for `c0000_a0x.anibnd.dcx`, ESD talk, other languages or
message binders, parts, materials, menus or the script-exposer DLL. Status covers the
configured scopes, including event JS, but not every runtime pattern, source file or
Smithbox row-name file.
It includes managed editor-only and destination-only files; their absence from the
repo is a review item, never permission to delete them.

The inspected Smithbox project points at the installed game. DSAnimStudio's
`_DSAS_PROJECT.json` still points at missing `C:/Steam/...` paths. Confirm which active
project is opened before correcting external settings. ESDTool's configuration has
the vanilla game as its base and an empty mod directory: future compilation must use
the existing modified binder as its template or other dialogue changes can be lost.
ESD `.py` files are an ESD DSL, not ordinary Python scripts to execute.

The inspected launcher is `Z:/Steam/steamapps/common/ELDEN RING/Game/launchmod_eldenring.bat`,
whose configuration loads `mod`. A separate tools-folder launcher also exists; do not
assume it is the one being tested. `logs` only tails logs under the configured Game
directory. Logging does not prove a specific mechanic works.

## What can be edited confidently

| Format | Current supported work | Acceptance requirement |
|---|---|---|
| Nexus/docs | Evidence-based text and formatting | Local checks, fact review, Nexus visual review |
| HKS | Focused source changes after baseline agreement | Focused diff plus game tests; generic Lua is not a qualified HKS checker |
| EMEVD | Isolated DarkScript compilation and decoded comparison | Review instructions, bindings, layers, rest behavior and metadata; game test |
| FMG/regulation | Inspection and explicit change planning | Writer round-trip qualification and version-aware semantic diff before acceptance |
| MSB | Entity/reference inspection and change planning | Writer qualification, ID/type preservation, Smithbox placement and game checks |
| ESD/TAE | Inspection and change planning | Template/binder-preserving build qualification and affected interaction tests |
| FXR/FLVER/TPF/Havok | Inspection and packaging | Tool-specific qualification plus visual/game checks before automated edits |

The event builder copies sources and local common_func inputs into an isolated run,
compiles all ten source files, and requires the complete expected output set. It
compares candidates with shipped binaries, or the source-side baseline for files not
shipped at the event root. Compression encoding is excluded; event order, duplicate
IDs, instructions, argument bytes, bindings, layers and other serialized public event
data are retained. `--require-equivalent` fails on any decoded difference or a missing
runtime baseline and still
leaves the receipt and before/after JSON for review. Compile success alone does not
qualify a no-change round trip or an in-game result. Once a deliberate source edit is
made, run without that option and review every reported difference.

`common_func.emevd.dcx` is currently excluded from the runtime event root by the old
propagator. The builder reports it as a non-runtime candidate. It does not add that
file to the shipped set. It currently has no compiled baseline in the repository:
compilation is checked, but its round trip remains unqualified and does not block
qualification of the shipped files. Sources that compile correctly can still be stale relative
to their binaries, so an initial mismatch requires investigation, not automatic copying.

CLI reference: [DarkScript3 RoundTripTool source](https://github.com/AinTunez/DarkScript3/blob/master/DarkScript3/RoundTripTool.cs).
Installed tool hashes are recorded in each event receipt; requalify after tool updates.
The local reader is not a general-purpose binary writer.

## Nexus conventions adopted from Grailwright

Keep `docs/nexus-full-desc.txt` as the editable full description and retain
`description-bbcode.txt` as the previous reference. The full draft still contains older
mechanical claims; formatting conversion is not feature verification. Keep short and
file descriptions distinct, with the file pitch shorter and at most 255 characters;
the short description is at most 350 characters. Keep these identity pitches stable
across routine releases. The short/file pitches are populated local drafts; the full
page still requires feature verification. Use `nexus-check --descriptions-only` for
copy editing without requiring a selected release version.
Use ASCII text, plain `[code]` blocks and established BBCode styling. Keep Sovereign's
existing visual identity instead of copying another game's theme. Changelog entries
must describe completed changes, not plans.

`NEXUS` is a review: report **Current / Update / Verify** for description, metadata,
release files and feature claims. `nexus-check` only checks local files, metadata and
basic tag balance; it cannot validate rendering, links or remote state. The page and
file-group IDs in `mod.json` are configured and verified; the release version remains
unset. `nexus-status` checks remote identity and active file versions. See
[NEXUS.md](../docs/NEXUS.md) for the API contract, observed file history and audit findings.

If the released file is already current, publish an explicitly requested description
update without duplicating the upload. A future upload must use the exact reviewed
archive hash, remote-state comparison, operation lock, prior-state backup and receipt.
Grailwright's publisher assumes its own metadata, helpers and package shape; copying a
single publishing script or its BepInEx build behavior is not an Elden Ring workflow.
Standalone description review/save, API publishing and a combined audit now live in
this repo. See [NEXUS.md](../docs/NEXUS.md) for commands, setup and qualification limits.

## Draft packaging and release gates

The package source is the exact main VDB stage selected in `.vdb/selected.json`,
when present; otherwise it is the configured legacy Vortex `Sovereign` directory.
Selected stages are verified against their full receipts before packaging. A drifted
selection fails rather than falling back. Preserve `mod/` and `mods/` paths in the ZIP.
To refresh a selected build, prepare/stage/select a new one; never overwrite retained
VDB stages. Packaging does not run propagation or substitute repo content.
`asset-catalog.json` defines repo assets; `runtimePatterns` also detects uncatalogued
runtime files and supports the legacy helper, but does not define release contents.

`mod.json` excludes propagated `src` and `.smithbox` directories. The packager reports
all exclusions and repo differences, preserves zero-byte files, rejects directory/file
links and unexpected top-level/private files, hashes the source, verifies all ZIP
entries and hashes, and rechecks the source inventory after packaging. Failed runs
must not be accepted; only successful candidates receive `receipt.json`.

The tested Vortex snapshot contains 90 files: 70 package files and 20 excluded authoring
files. Three `c2500` character files exist only in Vortex, and `c0000_a0x.anibnd.dcx`
differs from the repo. These are review observations, not permission to change either
copy. The ignored menu/hi archives are absent from this snapshot and are not added.

`mods/Scripts-Data-Exposer-FS.dll` is included because it is in the Vortex package.
Its version/source/distribution policy still needs verification. A draft filename
and external receipt identify test archives; no extra draft-marker file is inserted
into the game payload. The legacy repo-only `make_package` helper is retained for
its tests, but the `package` CLI now calls the Vortex packager.

```powershell
python tools/nexus_workflow.py package-plan
python tools/sovereign.py package --draft --version 0.0.0-workflow-test
# Once the selected version and release/dependency gates are verified:
python tools/nexus_workflow.py package --release --version <selected-version>
```

Release requires agreed source/output baselines, qualified binary changes, passing
affected tests with save/reload and multiplayer rules, completed Nexus metadata and
verified player claims, dependency/install verification, and an exact reviewed archive.
See `TEST-MATRIX.md`. Never mark a manual test Passed from code inspection alone.

The longer investigation and decoded exports remain local in
`.codex-temp/sovereign-inspect/`; the durable conclusions are in these docs. Scratch
files are not release inputs and may be regenerated or removed after review.
