Sovereign editing guide
=======================

Read the relevant format section before editing or rebuilding game files. These
procedures preserve the earlier qualification limits; numeric findings and receipt
paths are historical snapshots. Active runtime paths use `mod/`, source paths use
`src/`, and current handoff commands are in [WORKFLOW-COMMANDS](WORKFLOW-COMMANDS.md).
Do not execute archived legacy propagation scripts.


Event and Message Binder Editing
--------------------------------

These file-specific procedures incorporate the unchanged-file tests run on 2026-09-09.
They refine the earlier general qualification notes in `docs/WORKFLOW.md`. Test results
apply to the inspected inputs and tool versions, not every possible binary edit.

Baseline and acceptance:

- Compare the repo, saved editor workspace and intended deployment copies before
  choosing an editing baseline. Record source hashes and preserve rollback copies.
  Resolve content differences explicitly; a newer timestamp does not select the winner.
- For patch migration, extract current vanilla files from the installed game archives
  into scratch and record archive/build provenance. Loose files left by an earlier
  extraction are not proof of the current baseline. Label uncertain historical versions.
- Prepare and rebuild candidates in `.codex-temp`. Recheck input hashes before
  accepting them. Stop on unexpected source changes or unplanned decoded differences.
- Keep accepted source and its generated runtime output together. An editor handoff
  must use the same reviewed candidate and account for open editor buffers. Builds and
  tests do not implicitly run propagation or publish anything.
- Requalify the affected route after changing its tool/library version or format options.
  Successful compilation/repacking and archive hashes alone do not verify gameplay.

`common.emevd.dcx` and other EMEVD files:

- Edit the existing reviewed JS under `src/events`; compile with configured DarkScript3
  (`Z:\Modding\Elden Ring\Tools\DarkScript\DarkScript3.exe` on this workstation).
  Use `python tools/sovereign.py build-events` for isolated candidates. Run with
  `--require-equivalent` when checking unchanged source, not after an intentional edit.
- The tested Sovereign `common` source rebuilt byte-for-byte, with all 301 events
  matching. Prefer targeted upstream additions to that source for the current update.
  Preserve modifications to existing vanilla events as well as custom event IDs.
- Keep initialization calls in their original event and relative order. In the audited
  update, event 780 is initialized by event 0, and event 6911 by event 50; preserve the
  complete new event bodies and their guards. Check whether these additions have
  already been merged before applying them again.
- Compare decoded event order/IDs, instructions/arguments, parameter bindings, layers,
  rest behavior and file metadata. Require every difference to be explained by the
  intended edit; investigate compiler changes rather than silently ignoring them.
- Default DarkScript vanilla decompile/recompile changed instruction representations
  and parameter metadata in the tested `common` and `common_func`. This is not proof
  of broken behavior, but it is not a lossless round trip. Do not replace runtime files
  wholesale using that route without further validation.

`common_func` authoring reference:

- The inspected repo has `src/events/common_func.emevd.dcx.js` for authoring, but no
  runtime `mod/event/common_func.emevd.dcx`. Preserve this distinction: the game supplies
  its current shared event library. Compiling a source reference does not make it a
  runtime deliverable.
- Before refreshing the reference, compare it for custom changes and preserve those
  deliberately. Refresh from verified current vanilla and validate callers/arguments;
  the audited current library includes helper 900005590.
- Do not introduce an old or unqualified rebuilt common_func runtime override as a
  side effect of building or propagating other events.

`item_dlc02.msgbnd.dcx`, `menu_dlc02.msgbnd.dcx` and their FMGs:

- Use WitchyBND for the BND/DCX container and the qualified Smithbox SoulsFormats
  binary FMG reader/writer for text edits. On this workstation the library is
  `Z:\Modding\Elden Ring\Tools\Smithbox\Andre.SoulsFormats.dll`.
- Tested container commands are `WitchyBND.exe --silent --bnd --unpack <scratch-file>`
  and `WitchyBND.exe --silent --bnd --repack <scratch-folder>`. Ensure the effective
  Recursive configuration is false; omitting `--recursive` alone does not override a
  saved true setting. Check the output contains binary FMGs and no recursive FMG XML.
  Do not change global tool settings implicitly to make a test pass.
- Avoid recursive FMG/XML conversion for exact text preservation. The tested route
  collapsed whitespace-only strings and converted a literal `%null%` to actual null
  (`ArtsName_dlc01.fmg`, entry 4151 in Sovereign). Null, empty string, whitespace and
  literal `%null%` must remain distinct. Preserve Unicode and line breaks exactly.
- Merge by binder identity, internal file ID/path, and FMG entry ID. Compare historical
  vanilla, current vanilla and the agreed mod baseline; apply only deliberate mod
  differences to the current base. Require expected old values and surface overlaps.
  Never import whole old FMG tables merely to preserve a few custom entries. A DLC02
  binder also contains base and DLC01 tables; inspect every contained table.
- The independent binary audit found 195 item and 72 menu repo differences to preserve,
  disjoint from 318 item and 33 menu upstream changes. These are snapshot counts, not
  permanent merge assertions. The earlier XML-only item count of 194 is superseded;
  do not use that XML plan as the sole preservation specification.
- At that audit, the saved Smithbox item text matched the repo, while its menu text
  reverted the repo's 72 differences to historical vanilla. Recheck before editing.
  The former item propagation script did not deploy the menu binder; include an
  explicit scoped menu handoff when deployment is requested.
- Unchanged binary FMG read/write plus Witchy container repacking passed on both
  binders in both Sovereign and current vanilla. The scratch writer is a diagnostic,
  not an installed production merge command; inspect/adapt it before actual edits.
- Reopen every rebuilt binder with the independent binary reader and compare all text
  entries, null/whitespace values, ordering, FMG metadata, binder IDs/names/flags and
  header metadata. Verify intended text changes and preservation of everything else.
  Then check affected text in Smithbox and in game. Icon textures require separate work.

The supported binary text patch workflow now accepts explicitly absent entries with
`beforeMissing: true` and `before: null`. An existing null entry is different from
absence and must not be replaced through that declaration. Every changed or added ID
still needs an expected-value check and an independent full-binder comparison.

Detailed temporary evidence is in
`.codex-temp/rebuild-test-1789005548631119900/REPORT.md`, `receipt.json`,
`binary-fmg-receipt.json` and `binary-comparison-counts.json`. The procedures above
remain applicable if scratch is removed; regenerate evidence before relying on an
unavailable or outdated qualification result.


Easy compatibility assets and texture ownership
-----------------------------------------------

- See `docs/EASY-COMPATIBILITY-UPDATE.md` for the qualified effects, icon and older
  menu-text merge, its exact scope, evidence and remaining game tests. Recheck hashes
  before reusing its conclusions; do not apply the same additions twice.
- The existing icon archives belong to the separate Vortex `Sovereign - Textures`
  package, not the main `Sovereign` package. Preserve this ownership unless the author
  chooses to combine them. The main package workflow does not include those archives.
- WitchyBND basic BND/BXF packing preserved the tested member payloads and metadata.
  Its TPF unpack/repack preserved all tested texture bytes and decoded metadata.
  Preserve the solo `.tpfbhd`/`.tpfbdt` pair together. Compare named textures and binary
  metadata after rebuilding; a successful repack alone is insufficient.
- The missing custom SFX recovery is applied; see `docs/SFX-RECOVERY.md`. Preserve
  the recovered files in both active authoring and `src/sfx`. Alternate designs
  are archived for possible future use and must not replace active files implicitly.
- Common effects are authored in the configured SFX workspace's
  `sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd` folder. Update the loose FXR/resource-list
  additions as well as the packed output, or the next propagation rebuild loses them.
  The qualified specialized rebuild generates sorted category IDs starting at
  0/100000/200000/300000/400000. An insertion may shift existing numeric binder IDs;
  verify expected ordering, categories, names and every preserved payload explicitly.
- The two older menu binders use the qualified direct binary FMG workflow. They have
  no saved Smithbox counterparts in the inspected workspace; do not import whole old
  tables into the already-updated DLC02 binder to synchronize them.


Shared Grace ESD dialogue
-------------------------

Hewg's dialogue uses an additional preservation route documented in
[GAMEPLAY-CORRECTNESS-UPDATE](GAMEPLAY-CORRECTNESS-UPDATE.md). Its `.preserve.json`
pins a raw original `.esd`, unedited `.baseline.txt` DSL, and allowed state groups.
`build-dialogue`/`qualify-talk` compile baseline and edited DSL through ESDTool, then
transplant only the changed reviewed groups. They preserve unowned original groups,
metadata and other binder members instead of accepting a wholesale vanilla
recompile. Do not edit the pinned originals or widen the group list to silence a
failure. Review deliberate scope changes, requalify, and retain all companions in
the coordinated repo/editor handoff. This is a build-time recipe; only the resulting
talk binder ships to the game.

- See `docs/TORRENT-DIALOGUE-UPDATE.md` and its patch receipt for the applied Torrent
  merge, qualified ESDTool route and pending game tests. Do not add the helpers twice.
- Compile ESD DSL sources with ESDTool, using explicit scratch paths and the current
  mod binder as template. Run from the ESDTool installation directory. Preserve the
  template's actual `m00_00_00_00.talkesdbnd.dcx` basename and verify output exists;
  a renamed template can cause ESDTool to skip the requested output silently.
- Preserve existing custom helpers and menu branches. Allocate unused state IDs and
  reconcile helper keyword signatures when importing decompiled upstream source.
  Require all unedited groups and other binder members to remain unchanged.
- Vanilla decompile/recompile may alter expression encodings and flatten unconditional
  subconditions. Record these differences; compare imported helper source and a
  separate vanilla rebuild rather than claiming original vanilla byte equivalence.
- The accepted authoring handoff synchronized external t000001000 and t000003000
  source/ESD pairs and added a packed mod template beside that unpacked folder.
  Recheck these against runtime before later edits; restoring the former vanilla
  loose ESDs loses shipped customizations. Reload old editor buffers before saving.


TAE animation editing
---------------------

- See `docs/ANIMATION-UPDATE.md` and its receipt before editing c0000 animations.
  The reviewed 33 additions and 40 existing-record updates are already applied.
- Qualify the installed SoulsFormats TAE writer and specialized Witchy ANIBND
  rebuild on unchanged scratch inputs. Preserve event bytes, order, timing,
  mini-headers, group relationships and all unedited records. Document exact
  alignment/layout differences; decoded equality is not byte equality.
- Merge by file/animation ID and expected event values. Reordered events and
  zero extensions are not automatically conflicting gameplay edits. Preserve
  deliberate mod values and require explicit review for changes to those values.
- The working loose folder and packed DSAnimStudio output must stay synchronized.
  The former animation propagation VBS only copied the packed binder.
- A same-name `.dsaproj` can override the binder's timelines on open. The author
  chose to archive the old project for this handoff; open the updated packed binder
  to create a fresh project. Preserve and reconcile any later saved project rather
  than repeating the archive decision implicitly. Check open editor buffers.
- Coordinate final animation testing with HKS/behavior work without overwriting
  that work. Keep separate motion archives and their existing deployment differences
  outside a TAE-only handoff unless explicitly reviewed and included.


Player behavior and HKS editing
-------------------------------

- See `docs/PLAYER-BEHAVIOR-UPDATE.md` and its receipt before further player changes.
  The graph/HKS/name-ID update is applied; do not import those additions again.
- Use the qualified Elden Ring HKLib.CLI v0.1.2 for the inner behavior HKX/XML and
  WitchyBND basic BND mode for the outer binder. Requalify after tool updates.
  Compare complete decoded values and untouched binder members, not just build success.
- Match named graph nodes by class/name and preserve anonymous sharing. Generated
  object numbers are not stable identities. Remap graph events, external name IDs,
  animation IDs and pointer references in their respective namespaces.
- Custom animationInternalId values need not index animationNames: the inspected
  ERClipGeneratorTool allocates above the maximum existing clip ID. Preserve the
  custom allocation convention and avoid collisions; do not repair apparent table
  mismatches without establishing how the custom clips are bound.
- Keep c0000.behbnd.dcx, c0000.hks, eventnameid.txt and statenameid.txt coordinated.
  The accepted behavior authoring folder includes matching HKX/XML and Witchy metadata.
  Archived propagation scripts copied packed outputs and do not compile XML or synchronize
  the two name-ID files. Reload open editor buffers before saving after a handoff.
- Preserve curated/custom HKS logic while porting targeted upstream changes. Check
  embedded common_define tables too: the applied update includes skill row 373.
  A generic Lua parser is not a qualified Havok Script runtime checker; distinguish
  static checks from game compilation and manual acceptance.
- The separately completed animation update is the accepted baseline. Never deploy
  the superseded TAE candidates from the player-update scratch run over it.
- Seven existing custom clip references and the separate a0x/location-specific
  overrides remain documented in the update report. They are not newly fixed features
  and are not authority to remove assets or overwrite unrelated work.


Historical game-update archive
------------------------------

- The historical archive home is `Z:\Backup\Elden Ring\archive`, outside this
  repository. Follow its `README.md` and `CATALOG.md` when archive work is requested.
  The user manages the relocation; verify an entry's actual location before using
  it. Do not move, delete, or rewrite archive contents during instruction cleanup.
- Promote verified original snapshots, matching editor sources/projects, labelled
  comparison baselines and restoration evidence into a new dated target-build entry.
  Keep temporary tools/inspection data in `.codex-temp` and active work in place.
- Hash files before and after moving, preserve original receipts, provide relocated
  restore paths and update documentation. Never overwrite an existing archive entry
  or infer an old vanilla patch version from a directory name alone.
- Archive payloads are external backups; any remaining repo-local archive payloads
  are Git-ignored. Neither location supplies runtime/package inputs.
  Do not propagate them, automatically restore them, or run old handoff scripts.
- The completed event/text, effects/icons/text, Torrent and animation backups for
  build 25080141 belong under `Z:\Backup\Elden Ring\archive\game-updates\2026-09-09_to-steam-25080141`.
  Consult those entries' restore maps and verify paths against the current archive
  location; historical receipts may still name the former repo or scratch paths.
