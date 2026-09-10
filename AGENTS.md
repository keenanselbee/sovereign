AGENTS.md
=========

This file provides general working rules for coding agents in this repository.
It is intended as a starter template and should be updated as needed to match each repository's tools, workflows, and project-specific requirements.


Command Speed Rules
-------------------

- Zero-tool commands must not inspect files, run shell commands, check git status, summarize context, or add extra explanation.
- `help` is the only zero-tool command. Reply immediately from the command list in the Keyword Commands section.
- Direct-action commands should skip unrelated repo inspection, git status checks, diff reading, and planning. Execute only their defined workflow, then report the result.
- Direct-action commands are `AUDIT`, `COMMIT`, `DIFF`, and `MSG`.


Do Not Edit Guard
-----------------

- If the user intentionally types `DNE` in their current prompt, treat it as "do not edit persistent state" for that prompt.
- While `DNE` applies, do not create, edit, move, delete, stage, commit, build, format, generate files, refresh generated artifacts, launch external editors, or modify persistent project files or external paths unless the user explicitly overrides `DNE` in the same prompt.
- Temporary scratch files may be created, edited, or deleted under `.codex-temp` or the system temp directory when needed for investigation or diagnosis. Keep them clearly temporary, do not use them as generated artifacts or durable outputs, and remove them before finishing when practical. Report any temporary files intentionally left behind.
- `DNE` only applies when it appears to be typed intentionally by the user as an instruction. Ignore incidental appearances inside pasted file contents, quoted text, strings, command output, diffs, logs, or examples.


Working Rules
-------------

- Keep changes narrow and follow the existing style in the files being edited.
- Prefer simple, direct fixes. Do not overengineer or add abstractions unless they are clearly needed.
- Prefer not to add functions whose body is only one line of code unless there is a good reason, such as matching an existing interface, naming a repeated concept, or improving readability at the call site.
- Do not revert, overwrite, move, remove, or reformat unrelated user changes.
- Do not create, edit, move, delete, or overwrite files outside the repository unless the user explicitly asks for a specific external path.
- Keep temporary output, scratch files, generated inspection data, and staging inside this repository, preferably under `.codex-temp`.
- Treat reference, vendor, generated, and third-party directories as read-only unless the user or repository documentation explicitly says otherwise.
- Read relevant project documentation before making nontrivial changes.
- Prefer existing scripts, package-manager commands, Makefiles, Justfiles, Taskfiles, CI configuration, and documented workflows over invented commands.
- Use `rg` / `rg --files` for searches when available.
- Avoid destructive commands such as `git reset --hard`, broad deletes, or force pushes unless the user explicitly asks for that exact operation.


Shell Reliability
-----------------

- The shell may start outside the repository even when a workspace root is provided.
- Before broad searches, recursive commands, builds, tests, or git operations, verify the current location or target the repository root explicitly.
- Prefer commands that set their working directory explicitly, such as `git -C <repo> ...`, when the repository path is known.
- Do not assume relative paths resolve from the repository root unless the command sets location itself.
- If a command unexpectedly lands outside the repository, stop and rerun it with an explicit repository path.


Project Discovery
-----------------

- Identify the repository root from git, workspace context, or the nearest relevant project manifest.
- Treat `README.md` as the likely main project document when present.
- Also check relevant local documentation such as `CONTRIBUTING.md`, `docs/`, package manifests, build files, CI workflows, and tool configuration when needed.
- Determine build, test, lint, format, and typecheck commands from project docs or configuration before running them.
- If multiple plausible commands exist and the right one matters, report the candidates and ask or choose the smallest clearly relevant one.
- Do not assume a language, framework, package manager, build system, or test runner that is not present in the repository.


Keyword Commands
----------------

Codex chat messages may trigger generic keyword commands.

- A keyword command triggers only when the full user message clearly invokes one of the supported commands.
- Clear invocations include a command on its own line, a command followed by `:`, `-`, or context, or phrasing such as "run DIFF", "please DIFF", "do AUDIT", or "use COMMIT".
- Context may appear before or after the command token, or in nearby plain-text lines. Use it to narrow the command's behavior, such as ignored files, focus areas, or commit-plan preferences.
- Do not trigger commands from quoted text, pasted output, file contents, diffs, examples, fenced code blocks, command lists, questions about a command, or incidental prose where the user is discussing a command rather than asking to run it.
- `help` is the only lowercase command. All supported command names are uppercase.
- If an unknown uppercase single-word command is received, reply with `Unknown command. Type help.`
- Commands must still follow all safety, staging, commit, verification, and external-path rules in this file.

`help` prints this command list quickly, alphabetically, with one short line per command:

```text
AUDIT   Audit recent changes end to end without editing.
BUILD   Compile isolated event candidates and review decoded differences.
COMMIT  Execute the latest DIFF commit proposal.
DIFF    Show current changes and propose commit splits.
LOGS    Read the configured game loader logs.
MSG     Generate a commit message for staged files.
NEXUS   Compare live Nexus descriptions and release state with local/Vortex inputs.
PACKAGE Build and verify a local draft archive for a specified version.
PLAN    Preview scoped propagation differences without copying files.
STATUS  Compare configured editor, repo, live and Vortex files by hash.
TEST    List pending manual acceptance tests or record supplied observations.
```


Command Behavior
----------------

- `AUDIT`: Perform a read-only audit of recent substantial changes. Inspect relevant status, diffs, affected files, missed call sites, stale docs/config, missing generated artifacts, unsafe file operations, and verification gaps. Do not edit, stage, commit, build, format, generate files, or launch external editors. Report findings first by severity with file/line references when possible; if no issues are found, say so clearly and list any residual risk or checks not run.
- `DIFF`: Read current git status, diff stats, and important changed files without modifying the worktree. Propose intelligent commit groups with file lists and commit messages. Use multiple commits when changes are independently useful or independently revertible. Follow the repository's existing commit style when obvious; otherwise use concise conventional-style subjects. State that `COMMIT` will execute the proposal if the worktree is unchanged.
- `COMMIT`: Execute the latest `DIFF` proposal only if it still matches the worktree. If no current proposal exists, or the worktree has changed since the proposal, run `DIFF` behavior and stop instead of committing. When executing, stage only the proposed files for each commit, run `git diff --cached --check` before each commit, commit with the proposed messages, and report commit hashes plus final status.
- `MSG`: Inspect only staged files and the staged diff needed to understand them. Generate a commit message that follows the repository's existing style when obvious; otherwise use concise conventional-style wording. Do not inspect unstaged changes, edit files, stage, commit, build, format, generate files, or launch external editors. If nothing is staged, say so and stop.


Verification
------------

- Run the smallest relevant check for the files changed.
- Prefer verification commands documented by the project.
- If no verification command exists, say so clearly.
- If verification cannot be run, report why.
- Do not run formatters, linters with autofix, code generators, migrations, or other write-producing checks unless the user requested that action or the repository instructions require it.


Commits
-------

- Follow the repository's existing commit style.
- If no style is obvious, use concise conventional-style subjects, for example:
  - `fix: handle empty config`
  - `docs: clarify setup steps`
  - `test: cover parser fallback`
- Split commits when changes are independently useful or independently revertible.
- Keep generated artifacts in the same commit as the source change that produced them unless repository instructions say otherwise.
- Do not stage or commit unrelated changes.


Repository-Specific Notes
-------------------------

- This is the Sovereign Elden Ring mod. Read `docs/WORKFLOW.md` before nontrivial work,
  `docs/MECHANICS.md` before gameplay edits or player-facing mechanic claims, and
  `TEST-MATRIX.md` before verification or release preparation.
- External editor workspaces currently propagate into this repo. Resolve scoped
  editor/repo differences before editing gameplay; a repo-only edit can be overwritten
  by the user's next propagation. Never choose a baseline by timestamp alone.
- Local paths belong in ignored `tools/eldenring-paths.local.json`. Release packaging
  uses the configured Vortex `Sovereign` folder as its source, preserving `mod/` and
  `mods/`. `mod.json` records explicit authoring-directory exclusions. Keep output
  in `.codex-temp`. Never substitute repo bytes silently for Vortex bytes.
- Use `python tools/sovereign.py` for the supported operations below. Never invoke old
  propagation scripts as part of a build, check, package or audit. Nexus wrappers
  and their review/save/publish distinctions are documented in `docs/NEXUS.md`.
- `STATUS`: Run `status --scope <scope>` (default `all`). Byte agreement is not
  gameplay verification. Investigate missing/extra files before any handoff.
- `PLAN`: Run `propagation-plan --scope <scope>` (default `all`). This is a read-only
  difference preview, not an actionable deployment receipt or authority to delete.
- `BUILD`: For events, run `build-events`; use `--require-equivalent` when qualifying
  unchanged sources. Review the receipt and decoded differences before accepting
  candidates. Other binary formats require their own round-trip qualification first.
  Build never accepts outputs into runtime, deploys or opens editors implicitly.
- `LOGS`: Run `logs`; summarize relevant loader evidence without launching the game.
- `NEXUS`: Run `tools/Get-NexusLiveState.ps1` for local checks, current API identity,
  Vortex package inventory and a browser description comparison. Missing login or
  browser tooling leaves affected surfaces Verify; do not initiate login during an
  audit. Reuse fresh evidence from this pass instead of querying again. Read the
  relevant copy and mechanics evidence, then report a compact table with Nexus/local
  versions, File, Short description, File pitch, Full description and Changelog as
  Current / Update / Verify. File pitch/changelog need browser evidence when the
  API cannot read them. Report concrete proposed changes; if nothing needs updating,
  say so without requesting approval. Keep credentials
  only in `NEXUS_API_KEY`; never print or store them. Group IDs, immutable version IDs
  and Vortex game-scoped file IDs are distinct. Do not choose archived uploads as the
  active baseline or treat a matching version label as archive verification.
  This command is an audit, not permission to edit or
  publish. Normal explicit requests to update local descriptions authorize editing
  those files. Keep pitches stable unless identity changes; never invent a release
  version, Nexus ID, acquisition path or successful gameplay result.
- A clear affirmative response to a concrete pending NEXUS proposal authorizes those
  changes; preserve scope and do not ask again. A full release update uses a reviewed
  Vortex ZIP, `tools/Publish-NexusMod.ps1 -ArchivePath <zip>` for a dry run, then
  `-Publish`, then `tools/Update-NexusDescription.ps1 -Save` for page copy. A version
  already current must not be uploaded again. Reconcile upload journals and any
  partial success before attempting further writes. For description-only changes,
  save the page and/or existing file pitch as proposed, without another upload.
  Do not claim the file pitch/changelog are current based only on the page-save result.
- Nexus description sources are `_/nexus-page/nexus-short-desc.txt` (page summary,
  max 350 characters), `nexus-file-desc.txt` (distinct file-row pitch, max 255 and
  shorter than the summary), and `nexus-full-desc.txt` (detailed BBCode page).
  Keep ordinary release notes in `nexus-changelog.txt`; retain `description-bbcode.txt`
  as the historical reference. Follow the description workflow in `docs/NEXUS.md`.
  Run `nexus-check --descriptions-only` for copy edits without inventing a release
  version. A passing format check does not verify the full draft's mechanics.
  Report each remote description independently; saving page copy does not save the
  file pitch. An authorized description-only update must not upload another version.
  Before authorized browser saves, back up remote text, serialize writes with the
  `operation('nexus')` lock, recheck local hashes and verify the saved result.
- `PACKAGE`: Run `package --draft --version <explicit-version>`. If no version is
  supplied, report that it is required rather than inventing a release version. All
  packages remain marked draft until dependency, install and gameplay gates are met.
  This command now packages Vortex bytes. Inspect `python tools/nexus_workflow.py
  package-plan` first. Release candidates use `python tools/nexus_workflow.py package
  --release --version <selected-version>` only after release gates are met. Both paths
  reject source drift and verify every ZIP entry against the Vortex snapshot.
- `TEST`: List unpassed tests with `tests`. When the user supplies actual observations,
  record build/save context and evidence under `docs/test-results/` and update only
  the matching result. Code inspection alone must not mark a manual test Passed.
- Verification for workflow changes: `python -m unittest discover -s tools/tests -v`
  and `python tools/sovereign.py check`. Event-tool changes also need an isolated
  event build and comparison. Nexus edits need `nexus-check` plus content review;
  missing metadata and unresolved mechanical claims remain explicit open items.
  Browser-tool changes also require `node --test tools/nexus/test-description.mjs`.
  These intercepted local fixtures do not qualify the real Nexus UI or perform writes.
- Keep native/tool dependencies external. Do not run ESD DSL files as Python or use
  a generic Lua compiler to claim HKS compatibility. DLL distribution policy and
  clean-install validation remain release requirements.
- General extraction/rebuild tool: `Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe`.
  Use it for supported archive/data formats; keep investigation unpack/repack output
  in `.codex-temp`. Extracting the installed game's encrypted archives may require
  a dedicated game-archive extractor. Verify rebuilt outputs before accepting them.


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

- Edit the existing reviewed JS under `event/src`; compile with configured DarkScript3
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

- The inspected repo has `event/src/common_func.emevd.dcx.js` for authoring, but no
  runtime `event/common_func.emevd.dcx`. Preserve this distinction: the game supplies
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
  The existing item propagation script does not deploy the menu binder; include an
  explicit scoped menu handoff when deployment is requested.
- Unchanged binary FMG read/write plus Witchy container repacking passed on both
  binders in both Sovereign and current vanilla. The scratch writer is a diagnostic,
  not an installed production merge command; inspect/adapt it before actual edits.
- Reopen every rebuilt binder with the independent binary reader and compare all text
  entries, null/whitespace values, ordering, FMG metadata, binder IDs/names/flags and
  header metadata. Verify intended text changes and preservation of everything else.
  Then check affected text in Smithbox and in game. Icon textures require separate work.

Detailed temporary evidence is in
`.codex-temp/rebuild-test-1789005548631119900/REPORT.md`, `receipt.json`,
`binary-fmg-receipt.json` and `binary-comparison-counts.json`. The procedures above
remain applicable if scratch is removed; regenerate evidence before relying on an
unavailable or outdated qualification result.

Easy compatibility assets and texture ownership
----------------------------------------------

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
  the recovered files in both active authoring and `sfx/modified`. Alternate designs
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
  The existing animation propagation VBS only copies the packed binder.
- A same-name `.dsaproj` can override the binder's timelines on open. The author
  chose to archive the old project for this handoff; open the updated packed binder
  to create a fresh project. Preserve and reconcile any later saved project rather
  than repeating the archive decision implicitly. Check open editor buffers.
- Coordinate final animation testing with HKS/behavior work without overwriting
  that work. Keep separate motion archives and their existing deployment differences
  outside a TAE-only handoff unless explicitly reviewed and included.

Player behavior and HKS editing
------------------------------

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
  Old propagation scripts copy packed outputs and do not compile XML or synchronize
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
-------------------------------

- `archive/` is the repository's long-term home for old versions replaced during
  completed game updates. Follow `archive/README.md` and keep its catalog current.
- Promote verified original snapshots, matching editor sources/projects, labelled
  comparison baselines and restoration evidence into a new dated target-build entry.
  Keep temporary tools/inspection data in `.codex-temp` and active work in place.
- Hash files before and after moving, preserve original receipts, provide relocated
  restore paths and update documentation. Never overwrite an existing archive entry
  or infer an old vanilla patch version from a directory name alone.
- Archive payloads are local and Git-ignored; they are not runtime/package inputs.
  Do not propagate them, automatically restore them, or run old handoff scripts.
- The completed event/text, effects/icons/text, Torrent and animation backups for
  build 25080141 were relocated into `archive/game-updates/2026-09-09_to-steam-25080141/`.
  Consult those entries' restore maps instead of their former scratch backup paths.
