Sovereign development workflow
==============================

Sovereign now uses accepted repo sources/outputs, qualified native tools and the shared
Vortex Development Bridge (VDB). Repository preparation is separate from gameplay
acceptance and Nexus publication. See the [checkpoint](WORKFLOW-PREP-CHECKPOINT.md),
[command reference](WORKFLOW-COMMANDS.md), [editing guide](EDITING-GUIDE.md), and
[remaining feature plan](FEATURE-CORRECTNESS-PLAN.md).

The [repository layout and path guide](REPOSITORY-LAYOUT.md) records the completed
cleanup, descriptive editor shortcuts and stable `roots.vortexStaging` setting.
Run `python tools/sovereign.py path-check` to verify those paths without deploying.


File ownership
--------------

- `mod/` contains the main package's accepted runtime files.
- `src/` contains owned source/metadata files. SFX and dialogue are partial
  overlays; player sources include the accepted loose animation and behavior folders.
- `packages/textures/mod/` contains the separate package's three local icon archives.
  These remain Git-ignored. Their header/data pair stays together.
- `reference/mapstudio/` retains two unshipped copies with unassigned provenance.
  They are not editing or packaging inputs.
- External Smithbox, Script, DSAnimStudio and SFX directories remain working copies.
  A saved editor file is accepted deliberately, not selected by timestamp.
- `src/text/opening-dialogue-tutorial/` retains guarded recipes for the accepted
  English opening dialogue and Deflection text. The packed binders are already
  updated; these recipes support qualified rebuilds from earlier inputs.
- The verified stage selected in `.vdb/selected.json` supplies the release ZIP.
  Vortex owns deployment. Live game files are outputs and diagnostic evidence.

`asset-catalog.json` defines ownership and mappings. Workstation paths/tools belong in
ignored `tools/eldenring-paths.local.json`; VDB location belongs in `vdb.local.json`.
Native tools stay external. The main Vortex package also retains its existing
`mods/Scripts-Data-Exposer-FS.dll`; provenance and distribution remain release gates.


Normal edit and propagation
---------------------------

1. Read the relevant editing guide/update report and compare scoped repo/editor
   inputs. Preserve custom changes and choose a baseline by content. Automatic
   propagation checks the last verified shared hashes in `.sovereign/editor-sync.json`
   and stops on stale sources or independently changed destinations.
2. Edit with the appropriate tool, build an isolated candidate, and inspect decoded
   differences. Build success alone does not prove intended gameplay.
3. Accept matching source/output together, then sync the affected catalogued files
   back to their configured manual editor workspaces by default. The author has
   authorized these scoped syncs without another confirmation. Use the guarded,
   recoverable `accept-plan --from repo` / `accept` workflow and each format's
   qualification; resolve independent editor edits first. Reload old editor buffers
   after handoffs. Report any sync that could not complete.
4. Propagation ends after validated repository/editor sync. It records changed files,
   before/after hashes and linked recovery copies, without checking release metadata,
   preparing a package, selecting a VDB build or contacting Vortex. Save editor files
   first; unsaved buffers cannot be propagated. Unchanged files still receive the
   applicable consistency checks and a successful "Already synchronized" result.
5. Build/deploy only when separately requested. Collect all current repo-owned runtime
   files for each affected package, preserving verified external dependencies. Do not
   overlay only the last synced scope onto an older selected build. Assign the next
   unused regular version and changelog once for the batch before staging. Use the
   protocol-3 finalization queue; disabled/absent states remain preserved. If Vortex is
   closed, leave the authorized request queued rather than launching it. Resume its
   existing receipt and select the verified build after completion.
6. Record actual gameplay results in TEST-MATRIX only after an observed game test.

Propagation does not authorize build/deployment, Nexus publication or commits.
Audit and DNE requests remain read-only.

```powershell
python tools/sovereign.py status --scope maps
python tools/sovereign.py status --scope events --sources
python tools/sovereign.py status --scope text --json
python tools/vdb_workflow.py doctor
.\tools\Propagate-Sovereign.ps1 -Scope maps
python tools/propagate_workflow.py sync --scope events --from editor
python tools/propagate_workflow.py resume --receipt <existing-deployment-receipt> --profile SkC-QjDMc
```

The PowerShell launcher defaults to editor input; `-Source repo` reverses the sync.
Its only other option is `-Qualification`. It has no profile, version, package, wait,
stage-only or resume options. Existing deployment receipts use the explicit Python
`resume` command above, with their original profile/stage-only mode. Do not replay
the shortcut to recover a pending deployment.
Once a version is staged, changed package bytes require a new target and changelog
at the next requested build, not at each source sync.
See [release numbering and Grailwright parity](VDB-RELEASE-PARITY.md) for the initial
1.0.0 changelog, release checks and remaining promotion work.
The nine familiar external VBS filenames call this sync-only launcher. They do not
purge folders or copy into Vortex/live paths. Logs are under `.sovereign/propagation-logs/`;
sync receipts are under `.sovereign/sync/`, with linked handoff backups. Interrupted
syncs require inspecting those receipts before retry/restore. Never run archived old implementations.
The item shortcut uses `-Scope item-text`, accepting only `item_dlc02.msgbnd.dcx`.
Use `-Scope text` explicitly when all catalogued message binders are intended.

Player propagation qualifies the coordinated HKS/name/graph/animation group and refuses
an unresolved saved DSAnimStudio project. Dialogue currently uses accepted repo source
and matching ESD companions. SFX editor propagation rebuilds the complete editor source
with WitchyBND, saves its packed output with a backup, then accepts source/output.
Other scopes propagate saved outputs; event source must be compiled before propagation.
Event plans now verify saved source/binary consistency automatically and reject stale
outputs. Unchanged event checks and native player qualifications are reused with exact
input/tool guards; HKS-only edits do not rebuild unchanged player binders.
New SFX overrides must be explicitly added to the repo overlay. See the command reference
for qualifications, partial failures, saved-project limitations and recovery.

A pending request continues inside Vortex without the launcher. Resume with its
original profile/mode to refresh local receipts and packaging selection; never
blindly resubmit. An interrupted mutation requires
inspection. Copying a new source over an old packed file is not a qualified handoff.
Preparation failures after completed source acceptance can continue from their receipt
when accepted hashes still match. Historical development receipts retain their reuse
behavior. Regular versions retain their exact requested identity. Local plan/apply
commands need no active Vortex profile and use the checked target when omitted.
Each package/version is reserved before stage submission. Reusing its label with changed
contents fails; identical contents reuse the original stage/request. Historical receipts
also participate in the check. Main and textures have separate version reservations.


Verification and recovery
-------------------------

```powershell
python -m unittest discover -s tools/tests -q
python tools/sovereign.py check
python tools/sovereign.py build-events --require-equivalent
```

Run affected format qualifications when changing tools/options. `check` also rejects
runtime copies recreated at retired root paths. It does not establish game compatibility.
Event builds keep `common_func` authoring-only; they never add an unqualified runtime override.

The pre-work full backup, accepted asset copies, source handoffs, VDB version switching,
shortcut backups, layout map and validation receipts are listed in the checkpoint.
`.sovereign/` and `.vdb/` contain durable recovery records; `.codex-temp/` contains
regenerable build/inspection output. Preserve publishing journals during scratch cleanup.
Historical archives live at `Z:/Backup/Elden Ring/archive`; verify relocated paths before
restoring. Old receipts retain their original paths. Do not replay them after migration
without accounting for the recorded relocation map and later edits.


Nexus and remaining release work
-------------------------------

Use the existing shared Nexus Automation workflow in [NEXUS](NEXUS.md). `NEXUS` is an
audit; publishing and remote saves require the applicable explicit instruction.
Descriptions remain under `docs/`. Keep page summary, file pitch, detailed BBCode
and changelog distinct; verify mechanics before updating public claims.

Draft packaging uses the selected immutable main Vortex stage, preserving `mod/` and
`mods/`, and verifies every archive entry. It never substitutes repo bytes silently or
publishes automatically. Main and texture packages retain separate identities.
Final main release packaging requires a completed selected stage labelled with the
release version. It retains the exact verified ZIP and stage binding under
`.vdb/releases/main/<version>/`; retries return that ZIP. Publication rejects a changed
selection, payload or archive. See [the release workflow](VDB-RELEASE-PARITY.md).

The subsequent [gameplay update](GAMEPLAY-CORRECTNESS-UPDATE.md) implements the armor
and Hewg/per-journey decisions. Manual game tests, dependency provenance, clean installation, release metadata
and accurate descriptions remain in stages S7/S8 of the [release plan](REPOSITORY-AND-RELEASE-PLAN.md).
Earlier investigation prose is retained in [WORKFLOW-REFERENCE](../reference/WORKFLOW-REFERENCE.md)
and [WORKFLOW-PREP-HISTORY](../reference/WORKFLOW-PREP-HISTORY.md); those snapshots do not supersede
current commands or the editing guide.
