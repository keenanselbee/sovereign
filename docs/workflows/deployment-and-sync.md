# Deployment and synchronization

## Prepared-package deployment and resume

After the accepted source handoff, prepare complete affected packages with the
checked regular version and matching changelog. Include all current repo-owned
runtime files for each affected package and preserve verified external dependencies.
Review every prepared receipt before finalization. A prepared receipt is not a
completed stage or deployment.

```powershell
python tools/finish_workflow.py deploy --stage <prepared-receipt>
python tools/finish_workflow.py resume --receipt <finalization-receipt>
```

Repeat `--stage` for each affected package. The default wait is 15 seconds;
`--wait-seconds` accepts 0 through 45. Exit 2 means pending, 0 means verified
completion and 1 reports an operational error. These commands do not prepare
packages, accept editor files, change versions or publish to Nexus.
`deploy` prints and saves the finalization receipt before submitting the protocol-3
request. It defaults to all existing Elden Ring profiles; `--profile` narrows the
request and `--stage-only` leaves profile and packaging selections unchanged.
If a prepared stage already names a finalization receipt, inspect and resume that
request instead of submitting it again. A pending receipt is queued work, not
completed deployment; Vortex can process the request after its next launch.

`resume` uses the receipt's recorded profile and mode, without a new submission or
a profile override. After completion it verifies the stage bytes and selects all
completed, non-stage-only packages for Nexus packaging. Keep the existing receipt
for recovery and distinguish queued work from verified completion. Do not start
Vortex merely to drain a queue.

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
python tools/sovereign.py version-check
python tools/release_workflow.py target-version
python tools/vdb_workflow.py prepare --package main --version <checked-regular-version> --from repo
python tools/vdb_workflow.py prepare --package textures --version <checked-regular-version> --from repo
python tools/vdb_workflow.py stage --receipt <prepared-receipt>
python tools/vdb_workflow.py wait --receipt <prepared-receipt> --seconds 15
python tools/vdb_workflow.py select --receipt <completed-stage-receipt>
python tools/vdb_workflow.py deploy --receipt <completed-stage-receipt> --profile <active-profile-id>
python tools/vdb_workflow.py wait-operation --receipt <operation-receipt> --seconds 15
python tools/vdb_workflow.py verify --receipt <completed-stage-receipt> --profile <active-profile-id>
python tools/vdb_workflow.py rollback --receipt <previous-stage-receipt> --profile <active-profile-id>
```

Run only the preparation commands for affected packages. Replace
`<checked-regular-version>` with the checked target after assigning the next unused
regular version and matching changelog for changed payloads. Do not create new
development labels; identical retries retain their original version.
`prepare --from vortex` preserves the configured existing package;
`--from repo` deliberately substitutes
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
that exact package with `python tools/finish_workflow.py deploy --stage <prepared-receipt>`;
resume through `resume --receipt <finalization-receipt>`. Do not prepare partial
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
listed in [the sync-only update](../history/propagation-sync-transition.md).
The historical 2026-09-20 shortcut backups and verification hashes are retained in
`.sovereign/shortcuts/9f5e33dc2a924ea197a823224eca7917/receipt.json`.
