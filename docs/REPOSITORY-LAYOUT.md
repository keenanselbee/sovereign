Repository layout and workstation paths
======================================

The 2026-09-20 cleanup separates runtime files, authoring material, documentation
and promotional media. It does not change game payloads or relocate external editors.

| Location | Purpose |
| --- | --- |
| `mod/` | Accepted main runtime payload |
| `packages/textures/mod/` | Separate texture payload, locally retained and Git-ignored |
| `src/` | Catalogued editable sources plus explicitly unqualified asset overlays |
| `docs/` | Current guides, development notes and `nexus-*.txt` publishing copy |
| `images/` | Flat collection of screenshots, GIFs, icons and promotional artwork |
| `extras/loading-screens/` | Separate default/ultrawide options; not main package inputs |
| `reference/` | Historical descriptions, reports, message exports and unassigned maps |
| `tools/` | Build, validation, sync and release helpers |

`asset-catalog.json` owns active runtime/source mappings. The moved `src/materials`,
`src/textures` and `src/models` retain authoring files and packing metadata, but are
not automatically qualified rebuild inputs. Their README files state that limit.
Older message XML exports remain under `reference/message-exports`; accepted message
binders are still in `mod/msg/engus` and the configured Smithbox workspace.

The [2026-09-25 recovered source inventory](../src/README.md) adds missing packed
members and nested texture images to those existing folders. Its manifest retains
archive/member identities and explicitly marks missing archived baselines. These
snapshots supplement the qualified catalog. Recorded members now refresh within
the existing reviewed handoff; their extraction does not qualify a rebuild or
create new editor mappings.

Nexus helpers read `mod.json`'s `descriptionDirectory`, now `docs`, and select explicit
filenames. Promotional icons use `icon-` prefixes, including alternate-set names;
ReShade artwork uses `reshade-` prefixes to avoid collisions. No media was discarded.


External paths and shortcuts
----------------------------

`tools/eldenring-paths.local.json` retains the existing Smithbox, Script, DSAnimStudio,
SFX, live-game and native-tool paths. `roots.vortexStaging` points to the stable Vortex
staging directory. Verified selected receipts choose each package's build beneath it.
The current configuration no longer refers to missing legacy package folders. A
missing selection stops packaging with an actionable error; sync-only propagation
does not require a VDB selection. Explicit old
configurations retain the initial-import route only when their source folder exists.

The nine propagation VBS launchers continue to call `tools/Propagate-Sovereign.ps1`.
They validate and sync saved files only; build/deployment is a separate request.
Folder shortcuts have descriptive names and point to `mod/`, the live game, or the
selected stage. Selected-stage shortcuts run `tools/workspace_paths.py open-stage`,
which verifies the current receipt before opening Explorer. They do not deploy.

Run `python tools/workspace_paths.py check` for a read-only check of configured paths,
catalogued repo/editor files, selected stages, editor settings and folder shortcuts.
It detects incorrect destinations even when an obsolete directory still exists.
`python tools/workspace_paths.py shortcuts` prints the intended shortcut definitions.

DSAnimStudio's current `_DSAS_WORKSPACE.json` stays in place. The older project JSON
uses the same valid game paths after correction; no camera or other settings change.
Two archived direct-copy propagation scripts are preserved with `.disabled` suffixes.
Do not restore those scripts as active launchers.


Recovery and validation
------------------------

The local `.sovereign/cleanup-1789964016726404200/receipt.json` records every moved
file's original path, destination and SHA-256, plus all 73 main/texture runtime hashes.
That directory retains pre-edit documents/configuration and external shortcut backups.
Historical build, handoff and release receipts keep their original evidence; never
rewrite their hashes or paths to simulate a new qualification.

Refresh affected qualifications after code/configuration edits. Keep native outputs in
scratch; verify runtime hashes and selected VDB stages before finishing. This cleanup
does not call propagation, stage a version, deploy or publish. Version 1.0.1 remains
the main target because packaged bytes are unchanged; textures remain 1.0.0.

Completion verification: 493 planned file moves were checked. All 73 runtime files
retain their original bytes and membership. All 144 Python tests passed, as did
preparation, version, Nexus structure, 185 relative documentation links and whitespace
checks. Path diagnostics passed for 1,196 catalogued locations, 17 folder shortcuts,
nine propagation launchers and both selected VDB stages. Player, event, dialogue and
SFX native qualifications were refreshed; the recovery directory contains their
receipts in `qualifications.json` and the final inventory in `validation.json`.

The artwork `nexus-main.pdn` was edited concurrently at both its new and old paths.
The current `images/nexus-main.pdn` was left untouched; the different old-path copy
is preserved as `images/nexus-main-old-path.pdn`. Both were backed up independently.
Use the new `images/` location for future edits. No gameplay acceptance result is
implied by these filesystem and native-format checks.
