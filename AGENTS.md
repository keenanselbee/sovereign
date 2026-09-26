AGENTS.md
=========

These instructions apply to Sovereign.

- For this checkout under `C:\Repositories`, read `C:\Repositories\System\AGENTS.md` for shared working rules and project routing. The rules below are project-specific additions and overrides.
- If the shared file is unavailable in another environment, report that and use the available local instructions and project documentation.


Repository-Specific Notes
-------------------------

- See `docs/REPOSITORY-LAYOUT.md` for the cleaned layout: Nexus text directly in
  `docs/`, promotional media directly in `images/`, runtime in `mod/`. Do not recreate
  the former `_` tree or root game folders. Moved partial asset overlays are not
  qualified rebuild sources. Run `python tools/sovereign.py path-check` for the
  configured editor/tool paths, selected VDB stages and descriptive folder shortcuts.
- This is the Sovereign Elden Ring mod. Read `docs/WORKFLOW.md` before nontrivial work,
  `docs/MECHANICS.md` before gameplay edits or player-facing mechanic claims, and
  `TEST-MATRIX.md` before verification or release preparation.
- Read `docs/DESIGN.md` and `docs/BALANCE.md` for gameplay design and balance work.
  Keep confirmed author intent, current implementation, older guide claims and
  unaccepted tuning proposals distinct. Divinity preserving buffs while undamaged
  is intentional; Obliterator should use earned ultimate charge. Record author
  clarifications in the living documents rather than treating old reviews as policy.
- Current catalog/handoff/VDB/format commands and their limits are in
  `docs/WORKFLOW-COMMANDS.md`; completed preparation and remaining acceptance
  work are in `docs/WORKFLOW-PREP-CHECKPOINT.md`. Runtime files live in `mod/`,
  sources in `src/`, and separate texture payloads in `packages/textures/mod/`.
- Use `asset-catalog.json` for file/source ownership; do not duplicate mappings in
  workstation settings. SFX/dialogue source folders are partial overlays. Player
  handoffs require `player_workflow.py --from <source>` qualification and the whole
  coordinated group, including `src/player/` sources. Dialogue needs
  `qualify-talk` and its unchanged input/tool/companion receipt before `accept-plan`.
  Never choose a source-only group to bypass coordinated handoff requirements.
- VDB `stage` never activates. Wait for its completed receipt before selecting a build.
  Completing authorized runtime changes includes qualified manual-editor sync.
  Propagation is sync-only: validate saved files, reject conflicts, accept the scoped
  sources/outputs and record a receipt. Do not bump versions, prepare packages or call
  Vortex as part of propagation. Build and deployment are separate requested work.
  For an explicitly requested deployment, use the existing protocol-3 finish queue,
  not low-level stage-only by default. Finalization defaults to all game profiles;
  `--profile` narrows scope and `--stage-only` changes no profile or packaging selection.
  Enabled versions deploy when active and safe; disabled selections update without
  enabling/deploying; absent packages stay absent. The bridge continues queued work
  independently of the launcher. Resume refreshes local receipts and selects the
  verified packaging stage after finalization completes. Legacy receipts keep their
  original recovery path and explicit deployment scope.
  Selected main VDB stages now supply Nexus package bytes, verified against the full
  stage receipt. Never overwrite those retained stages or invoke legacy propagation
  during a VDB deployment. Main and texture switching/rollback are qualified.
- Release/version conventions and remaining Grailwright parity work are in
  `docs/VDB-RELEASE-PARITY.md`. `mod.json` owns the release target; `changelog.txt`
  keeps newest-first `Version X.Y.Z` blocks and plain change lines. Match Grailwright's
  single-digit minor/patch numbering and rollover. Run `version-check` after changes.
  Each batch of changed packaged files selected for a build gets the next unused regular
  version and an accurate changelog before staging. Bump once for the cohesive batch, not for
  every edit or retry. Documentation/tooling-only changes outside the package do not
  create a mod version. Stage only affected packages, combining their changed scopes
  before reserving a version; never stage different intermediate payloads at one version.
  Explicit package preparation uses the checked regular version from `mod.json`.
  Sync-only propagation does not require release metadata or a selected VDB build.
  Do not generate new development labels. Bump the target and changelog
  before staging changed bytes under a previously used version. Propagation never
  bumps the target or implies deployment/publication. Keep `releaseReady` false until acceptance.
  Every staged package/version owns one fixed payload. Identical retries reuse the
  original build/request; changed contents require a new version. Preserve version
  reservations under `.vdb/staged-versions/`, including interrupted requests.
  Historical development receipts remain resumable. Explicit combined deployment and
  explicit release freezes retain their requested version. Preparation
  may resume after source acceptance only with matching recorded accepted-input guards.
  Status/doctor compare verified selected VDB stages beneath `roots.vortexStaging`.
  This configuration requires a selection and never falls back to a missing legacy
  package folder. Never hide stage drift.
- External editor workspaces currently propagate into this repo. Resolve scoped
  editor/repo differences before editing gameplay; a repo-only edit can be overwritten
  by the user's next propagation. Never choose a baseline by timestamp alone.
- The author gives standing authorization to sync completed, verified Sovereign edits
  to the configured manual workspaces: Smithbox, Script, DSAnimStudio and SFX under
  `Z:\Modding\Elden Ring`. This is the default completion step for affected catalogued
  assets, without another permission request. Use the existing qualified
  `accept-plan --from repo` / `accept` handoff with guards and recovery copies; keep
  coordinated sources/binaries together. Resolve independent editor changes first,
  preserve unrelated files and account for open editor buffers. Report a blocked
  sync rather than claiming completion. This author instruction overrides the shared
  external-write restriction for those configured workspaces only. Audits and DNE
  requests remain read-only unless separately authorized. Runtime edits and propagation
  alone do not request a build/deployment. When build/deployment is requested, collect
  all current repo-owned runtime files for each affected package; do not overlay just
  the last synced scope onto an older stage. Preserve verified external dependencies.
  Queue authorized finalization if Vortex is closed; do not launch it merely to drain the queue.
  Preserve disabled/absent package states and wait for safe active-profile deployment.
  Report completed versus queued work with its existing receipt, and resume that
  request rather than resubmitting. Explicit stage-only/local-only requests override
  this default. Publication, commits, and external tool installation remain separate.
- Preserve `.sovereign/editor-sync.json`, the last verified common hashes for
  repo/editor pairs. Automatic propagation rejects stale sources, independently
  changed destinations and unknown divergent pairs. After inspecting and reconciling
  a conflict, use a scoped `accept-plan --resolve-conflicts` with the reviewed source;
  never add that override to automatic propagation or choose by modification date.
  `sync-baseline` records existing equality only and cannot resolve a divergence.
- Local paths belong in ignored `tools/eldenring-paths.local.json`. Release packaging
  uses the verified selected VDB stage as its source, preserving `mod/` and
  `mods/`. `mod.json` records explicit authoring-directory exclusions. Keep output
  in `.codex-temp` for drafts/candidates. Retain final release ZIPs and their receipts
  under `.vdb/releases/`; never overwrite them or clear them during scratch cleanup.
  Never substitute repo bytes silently for Vortex bytes.
- Use `python tools/sovereign.py` for the supported operations below. Never invoke archived legacy
  propagation scripts. The installed VBS entry points now call the scoped launcher;
  use them only for explicitly requested propagation, never implicitly during audits. Nexus wrappers
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
- Nexus file identities live in `mod.json`: main group `7949853` (short ID
  `sVKWduzP0`), textures group `893965` (short ID `qdbCxL2mS`), both on unique mod
  `18610093293769`. Preserve these IDs despite misleading historical group names.
  Keep one authored metadata source; do not duplicate it in an `API.txt`.
- When a release updates both packages, publish and verify textures first, then
  publish main last so main appears above textures on Nexus. Serialize those uploads;
  do not run them in parallel. If textures fail or have an uncertain outcome, reconcile
  them before continuing to main. A textures-only release does not authorize a dummy
  main upload/version bump just to reorder the page. Preserve main as the primary file.
- Follow `docs/RELEASE-AUTOMATION.md` for both-package publication and safe retries.
  The coordinator preflights both archives, publishes textures first and main last,
  and then promotes exact uploaded builds. `--apply` requires release authorization;
  implementing or testing the tooling does not authorize a live release.
  Preserve `.vdb/release-batches/` and each retained ZIP's upload/promotion journals.
  Use `release_pipeline.py promote --archive <zip>` for promotion-only retry; pending
  requests are waited on, never resubmitted. Use its read-only `readiness` command
  before collection updates; unavailable or local builds are not ready.
- Nexus description sources are `docs/nexus-short-desc.txt` (page summary,
  max 350 characters), `nexus-file-desc.txt` (distinct file-row pitch, max 255 and
  shorter than the summary), and `nexus-full-desc.txt` (detailed BBCode page).
  Keep ordinary release notes in `docs/nexus-changelog.txt`; the historical reference
  is `reference/nexus-description-legacy.txt`. Follow `docs/NEXUS.md`.
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
  Release packaging requires a completed selected stage with the exact release label;
  freeze it from the verified tested stage bytes, then explicitly stage/wait/select.
  Packaging never stages or deploys. Publication requires the retained ZIP and matching
  stage identity; identical packaging retries return the existing ZIP unchanged.
- `TEST`: List unpassed tests with `tests`. When the user supplies actual observations,
  record build/save context and evidence under `docs/test-results/` and update only
  the matching result. Code inspection alone must not mark a manual test Passed.
- Event plans/handoffs automatically verify saved source/binary consistency before
  acceptance. Stale outputs must be compiled/saved first; `common_func` stays
  authoring-only. Unchanged event qualifications and native player checks can be
  reused with exact asset/tool guards. HKS-only changes refresh input guards without
  rebuilding unchanged binders. This does not establish HKS or gameplay correctness.
- Verification for workflow changes: `python -m unittest discover -s tools/tests -v`
  and `python tools/sovereign.py check`. Event-tool changes also need an isolated
  event build and comparison. Nexus edits need `nexus-check` plus content review;
  missing metadata and unresolved mechanical claims remain explicit open items.
  Browser-tool changes also require `node --test tools/nexus/test-description.mjs`.
  The implementation is shared through `@keenan/nexus-automation`, configured by
  `NEXUS_AUTOMATION_ROOT` or ignored `nexus-automation.local.json`; shared changes
  also require its `npm test`. Keep Sovereign's packaging/release policy here and
  use the same shared state directory as other consumers. Preserve upload journals
  beside their package receipts when cleaning scratch output.
  These intercepted local fixtures do not qualify the real Nexus UI or perform writes.
- Keep native/tool dependencies external. Do not run ESD DSL files as Python or use
  a generic Lua compiler to claim HKS compatibility. DLL distribution policy and
  clean-install validation remain release requirements.
- General extraction/rebuild tool: `Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe`.
  Use it for supported archive/data formats; keep investigation unpack/repack output
  in `.codex-temp`. Extracting the installed game's encrypted archives may require
  a dedicated game-archive extractor. Verify rebuilt outputs before accepting them.


Editing And Archive Routing
---------------------------

- Read `docs/EDITING-GUIDE.md` before format-specific edits or archive work. It retains
  the full event, binary FMG, texture, ESD, TAE, HKS/graph and archive safeguards formerly
  embedded here. Read the matching detailed update report linked by that guide.
- Use `tools/Propagate-Sovereign.ps1` or `propagate_workflow.py sync` for explicit
  scoped sync-only propagation. Sync records/backups link through `.sovereign/sync/`.
  Qualification and editor-source consistency are required even when packed files
  appear unchanged. Existing deployment receipts remain recoverable through the
  explicit Python `resume --receipt` command with their original profile/mode;
  never resubmit them. `plan/apply/run` remain explicit build/deployment tools.
- The nine external VBS filenames are preserved and call the sync-only launcher.
  They no longer purge trees or copy into immutable stages/live files themselves.
- Never restore old layout paths or replay historical handoff receipts blindly. The
  layout receipt maps old paths to current ones; see the checkpoint for recovery records.
