# Current Sovereign commands

Implemented during the 2026-09-10/11 workflow goal. Main runtime files are in `mod/`,
authoring sources in `src/`, and separate texture payloads in `packages/textures/mod/`.
The nine external propagation entry points now perform validated sync only. Build
and deployment are separate requested operations. Historical VDB switching/rollback
evidence remains in [the checkpoint](WORKFLOW-PREP-CHECKPOINT.md).

## Inspect and choose a baseline

```powershell
python tools/sovereign.py doctor
python tools/sovereign.py path-check
python tools/sovereign.py status --scope events --sources
python tools/sovereign.py propagation-plan --scope maps
```

`asset-catalog.json` declares runtime membership, package ownership, optional editor
destinations and source overlays. Local paths/tools live in ignored
`tools/eldenring-paths.local.json`. Status reads all applicable copies; it does not
choose one. Missing live files after disabling a mod are deployment state, not proof
that the repository is outdated. The regulation row-name equivalence applies only to
the two inspected SHA-256 hashes. An unlisted runtime file fails `check`.

Status and doctor use each package's verified selected VDB stage for their Vortex
comparison. With `roots.vortexStaging`, a missing selection fails explicitly;
an invalid or modified selected stage never falls back silently. Historical configs
can import an explicitly configured, existing legacy package before selection.
`path-check` also checks expected editor files and shortcut destinations. See the
[layout and workstation guide](REPOSITORY-LAYOUT.md).

Status lists differences and a count by default. Add `--verbose` to list matching
files too; `--json` retains every file, path and hash. Source comparisons perform
one scan rather than a separate runtime scan followed by the source scan. Each
catalogued row reports repo versus selected build (when packaged) and repo versus
saved editor (when mapped); a missing side is named explicitly. Source rows have
repo/editor comparisons, not a build comparison. Hash agreement is not gameplay
verification, and an unsaved editor buffer is outside this comparison.

Propagation also checks `.sovereign/editor-sync.json`, which records the last
verified shared hash for each repo/editor pair. A one-sided edit may propagate
toward the unchanged side. A stale selected source or independent destination
edit stops before copying or staging, even if its modification date is newer.
The check runs before SFX rebuild/save as well as before handoff. Successful
handoffs refresh the baseline; failed or restored handoffs do not label differing
files as synchronized.

For an initial workspace, `python tools/sovereign.py sync-baseline --scope all`
records only files whose contents already match, copying nothing. It lists and
skips differences. Automatic propagation of differing existing files without a
baseline requires a reviewed scoped `accept-plan` / `accept` first.
For a known conflict, inspect/reconcile both copies and explicitly choose the
reviewed source with `accept-plan --scope <scope> --from <repo-or-editor>
--resolve-conflicts`. This flag is not exposed by propagation shortcuts. It retains
format qualification, backups and guards against edits after planning.

Release metadata checks are read-only:

```powershell
python tools/sovereign.py version-check
python tools/release_workflow.py target-version
```

`mod.json` owns the intended public version. `changelog.txt` must begin with the same
`Version X.Y.Z` and keep older blocks newest first. Explicit package build labels derive
from that target; retained builds keep their original versions. See
[VDB-RELEASE-PARITY](VDB-RELEASE-PARITY.md) before preparing the 1.0.0 release.
Stage submission now reserves a fixed payload for every package/version and reuses
matching prior requests/builds. Changed contents need a new label. Final release
packaging requires a matching selected release stage and retains its exact ZIP under
`.vdb/releases/`; follow the explicit freeze sequence in that release document.
Both main and texture publishing, promotion-only retries and read-only collection
readiness are implemented in [release automation](RELEASE-AUTOMATION.md). Joint
updates are serialized textures first, main last; no commands publish implicitly.

The SFX and dialogue source folders are partial override sets, not complete vanilla
extractions. Source status compares those owned files without proposing to import
thousands of unrelated editor files. Adding a new override requires explicitly
placing/reviewing it in the repo source set. The four former dialogue source
differences were reconciled through the qualified handoff in the checkpoint.

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

Use the existing detailed [animation](ANIMATION-UPDATE.md),
[behavior](PLAYER-BEHAVIOR-UPDATE.md) and Smithbox recipes for other formats.
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

## Stage, select and deploy through VDB

Configure `vdb.local.json` from `vdb.local.example.json`, or set
`VORTEX_DEVELOPMENT_BRIDGE_ROOT`. The adapter loads the bundled client named by the
shared tool's verified `dist/latest.json`, verifies its hash and accepts client
protocol 1, 2 or 3. Explicit combined deployment requires `profile-finish-v3` and can queue while
Vortex is closed. Existing low-level stage/deploy operations still use protocol 1
and require a fresh extension snapshot.
It does not vendor the extension or alter the Vortex database directly.

```powershell
python tools/vdb_workflow.py doctor
python tools/vdb_workflow.py prepare --package main --version 0.0.0-workflow-test --from vortex
python tools/vdb_workflow.py prepare --package textures --version 0.0.0-workflow-test --from vortex
python tools/vdb_workflow.py prepare --package main --version 0.0.0-workflow-test --from repo --scope maps
python tools/vdb_workflow.py stage --receipt <prepared-receipt>
python tools/vdb_workflow.py wait --receipt <prepared-receipt> --seconds 15
python tools/vdb_workflow.py select --receipt <completed-stage-receipt>
python tools/vdb_workflow.py deploy --receipt <completed-stage-receipt> --profile <active-profile-id>
python tools/vdb_workflow.py wait-operation --receipt <operation-receipt> --seconds 15
python tools/vdb_workflow.py verify --receipt <completed-stage-receipt> --profile <active-profile-id>
python tools/vdb_workflow.py rollback --receipt <previous-stage-receipt> --profile <active-profile-id>
```

The example version is only a local qualification label. `prepare --from vortex`
preserves the configured existing package; `--from repo` deliberately substitutes
that package's catalogued repo overrides while retaining the staged external DLL.
Add `--scope` to replace only that scope and keep all other selected-stage bytes.
Adding catalogued runtime files requires an existing verified selected stage,
`--from repo`, and a scope covering every new file. Inspect `addedRuntimePaths` and
the complete package difference before staging. Extra baseline files still fail;
this does not authorize removing previously shipped files or adopting unknown files.
The copied payload is independently verified and kept under `.vdb/prepared/`.
Both packages use the default game-root mod type: main retains `mod/` and `mods/`,
textures retains `mod/menu/hi`. Main and texture identities stay separate.

Stage is always stage-only. Queue acceptance is not completion. Exit 2 means queued
or pending; inspect/wait on the existing request instead of submitting it again.
Failed/interrupted/expired receipts require review. Operation receipts preserve the
selected client, request ID and previously enabled mods. A deployment requires the
named Elden Ring profile already active; the adapter never switches profiles.

`select` changes only the local package-source pointer. Nexus packaging then reads
the verified selected main Vortex stage rather than the mutable legacy folder. It
rechecks the complete stage against its receipt and fails on drift; it never silently
substitutes current repo bytes. Stage selection does not deploy or publish. Existing
Nexus commands, explicit release version and manual/dependency gates remain in force.

Rollback activates a retained VDB build. This protocol has no disable-all operation;
returning to an initially empty profile requires disabling the test packages and
deploying through Vortex. Legacy mods with unrelated/ambiguous identity also require
an explicit transition. The installed propagation shortcuts now use the scoped launcher. Do not run their
archived legacy implementations, or edit an immutable VDB stage in place.

## Verification

For ordinary propagation, use sync only:

```powershell
.\tools\Propagate-Sovereign.ps1 -Scope maps
.\tools\Propagate-Sovereign.ps1 -Scope sfx
python tools/propagate_workflow.py sync --scope events --from editor
```

The launcher defaults to editor input. `-Source repo` reverses direction;
`-Qualification` supplies an existing native proof. It has no version, package,
profile, stage-only, wait or receipt options. Sync neither checks release metadata
nor requires a selected VDB build/client. It never prepares a package or calls Vortex.
Save the editor files first. Only catalogued runtime files and tracked companions
are accepted; maps/regulation/text use byte/conflict checks, not gameplay validation.

Sync records are under `.sovereign/sync/<id>/receipt.json`. They link to guarded
handoff receipts under `.sovereign/handoffs/` containing exact before/after hashes,
qualifications and independent recovery copies. Unchanged inputs still validate and
produce a successful "Already synchronized" result. Missing files, unknown divergent
pairs, stale sources, independent destination edits and input drift stop acceptance.
Logs remain under `.sovereign/propagation-logs/`. Inspect interrupted sync and child
receipts before retry/restore; use the existing handoff `restore` for reviewed recovery.
Do not pass a sync receipt to deployment `resume`.

Events verify saved sources against compiled outputs. Player shortcuts keep HKS,
names, graphs, animations and their sources coordinated, even when the shortcut name
mentions only one file. SFX sync retains the local WitchyBND build/save, backup and
full-extraction guards; that asset repack is separate from creating a Vortex build.
SFX source drift after acceptance leaves an interrupted sync with its completed
handoff still available for inspection/recovery.

Build/deploy only on a separate request. Collect all current repo-owned runtime files
for each affected package and preserve verified external dependencies. Use one new
version/changelog for the accepted batch; do not overlay only the last synced scope
onto an older selected stage. The commands below remain explicit preparation and
deployment/recovery tools, rather than the propagation-shortcut path.

To compose source acceptance and scoped stage preparation, use
`python tools/propagate_workflow.py plan --scope <scope> --from editor --version <version>`
(with `--qualification` for player/dialogue), review its receipt, then run
`python tools/propagate_workflow.py apply --receipt <receipt>`.
This creates a prepared VDB receipt; stage and deploy remain explicit. Failure after
source acceptance retains that completed handoff and its independent restore copies.
The familiar external VBS filenames now call `Propagate-Sovereign.ps1`; their original
implementations are backed up and must not be run against a VDB deployment.

Plans recheck complete scoped input membership and any player/dialogue qualification
before acceptance, including when source and destination initially matched.

Event plans and direct event handoffs automatically qualify the selected saved
DarkScript sources against the saved runtime binaries, using isolated compilation
and decoded comparison. Stale binaries stop acceptance with the affected filenames
and comparison location. Compile/save those edits in DarkScript and retry. Saved
source companions must also match runtime; `common_func` remains authoring-only.
Unchanged input/tool fingerprints reuse the previous event qualification. Qualification
is rechecked before acceptance, including when no file copy is needed.

For local preparation without an active game profile, use the existing plan/apply
commands. Version is optional and defaults to the checked regular target in `mod.json`.
Player and repo-dialogue qualification also runs automatically:

```powershell
python tools/propagate_workflow.py plan --scope events --from editor
python tools/propagate_workflow.py apply --receipt <printed-propagation-receipt>
```

Review the plan before applying. Apply accepts the chosen repo/editor direction and
prepares a package, without staging or deployment. The familiar propagation shortcuts
perform sync only. SFX local preparation still uses its documented
build/save step; it does not silently rebuild the editor extraction during planning.

For an explicitly requested scoped deployment with a verified current baseline,
the existing combined command remains available after versioning and verification.
Its scoped overlay does not collect unrelated repo changes. Use full-package
preparation for a batch of separately synced scopes. Existing requests resume here:

```powershell
python tools/propagate_workflow.py run --scope maps --from editor --profile SkC-QjDMc
python tools/propagate_workflow.py run --scope events --from repo --wait-seconds 30
python tools/propagate_workflow.py resume --receipt <propagation-receipt> --profile SkC-QjDMc
```

`run` accepts the specified source scope, prepares/stages its package, deploys through
Vortex, and selects that exact build for packaging only after live-byte verification.
Omit `--profile` to update all existing Elden Ring profiles; specify it to limit scope.
Neither queuing nor source acceptance requires that profile to be active. Enabled
versions wait for safe deployment, disabled selections update without deployment,
and absent packages remain absent. `--stage-only` changes no profile or packaging
selection. Duplicate or ambiguous provider identities fail before activation. The default version
is the checked target; this does not imply publication or acceptance. Player and repo-dialogue
qualification runs automatically if no existing `--qualification` is supplied.
For SFX from the editor, `run` first builds with WitchyBND and saves the packed editor
output with a recovery receipt, then accepts the scoped sources/output. It rechecks
the complete SFX extraction before and after source acceptance. Other scopes propagate
their saved outputs; event propagation verifies that saved source and binaries agree.
If later propagation
fails, inspect its source-handoff receipt and `sfxEditorSave` separately; restoring the
packed editor output does not undo a completed repo handoff or deployment.

Do not start Vortex merely because it is closed. The protocol-3 finish request is
durable and the extension processes it on the next launch. The low-level `stage`
command's fresh-snapshot requirement is not the normal closed-Vortex completion
path. For an already prepared package containing multiple accepted scopes, reuse
that exact package with `finish_workflow.submit` / `refresh`; do not prepare partial
same-version replacements. Keep the finalization receipt before waiting and resume
it without another submission. A completed stage alone is not completed deployment.

The default wait budget is 120 seconds (`--wait-seconds 1..600`). A pending result
returns exit 2 with the existing propagation receipt. `resume` waits on that request;
it does not queue a duplicate stage/deployment. Interrupted or failed submissions
require inspection. Child receipts remain linked before deployment submission, and
source acceptance remains recoverable if later staging/deployment fails. A completed
Vortex callback with mismatching live bytes is an error and does not select the build.
The legacy combined path passed real deployment/resume checks. The new all-profile
finish path has fixture coverage; native all-profile acceptance remains pending.
The legacy-provider transition and external shortcut installation are complete.

If package preparation fails after source acceptance, rerun `apply --receipt` to
continue locally, or `resume --receipt --profile` to continue the requested deployment.
Both recheck the recorded accepted files and configuration before continuing and do
not repeat the handoff. Later edits, incomplete handoffs, or older receipts without
accepted-input guards still require inspection. Recovery does not blindly resubmit
an uncertain Vortex operation.

Regular versions keep their requested identity. Identical package/version retries
reuse the original immutable stage/request; changed bytes require a new version and
matching changelog block. Historical development receipts remain resumable and retain
their selected-build reuse behavior. No new development labels are generated.

The sync-only PowerShell launcher works from any working directory:

```powershell
.\tools\Propagate-Sovereign.ps1 -Scope maps
.\tools\Propagate-Sovereign.ps1 -Scope sfx
python tools/propagate_workflow.py resume --receipt <existing-deployment-receipt> --profile SkC-QjDMc
```

The installed VBS shortcuts call this launcher and report synchronization success
or failure. Existing queued deployments are unaffected; explicitly resume their
original receipts through Python with the original profile/stage-only mode.

The installed item shortcut uses `-Scope item-text`, an alias for Python scope
`file:msg/engus/item_dlc02.msgbnd.dcx`. It accepts only that binder and preserves
the repository's menu binders. `-Scope text` explicitly accepts the whole text
scope. Python `file:<runtime-relative-path>` selection is limited to catalog-owned
FMG binders; it cannot bypass coordinated player or other format qualifications.

All nine shortcuts are sync-only. Their current scopes and validation limits are
listed in [the sync-only update](PROPAGATION-SYNC-UPDATE.md).
The historical 2026-09-20 shortcut backups and verification hashes are retained in
`.sovereign/shortcuts/9f5e33dc2a924ea197a823224eca7917/receipt.json`.

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
[its README](../src/recipes/hadeon-followup/README.md).
`src/textures/deflection-tutorial/build.ps1` rebuilds the paired texture archive;
see [its README](../src/textures/deflection-tutorial/README.md). The independent
scene, reusable panel and icon remain in `images/mockups/deflection-v3/`.
These catalog recipes identify ownership; they do not automatically rebuild,
accept, deploy or replace arbitrary newer editor saves.
