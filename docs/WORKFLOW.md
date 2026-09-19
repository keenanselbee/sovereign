Sovereign development workflow
==============================

Sovereign now uses accepted repo sources/outputs, qualified native tools and the shared
Vortex Development Bridge (VDB). Repository preparation is separate from gameplay
acceptance and Nexus publication. See the [checkpoint](WORKFLOW-PREP-CHECKPOINT.md),
[command reference](WORKFLOW-COMMANDS.md), [editing guide](EDITING-GUIDE.md), and
[remaining feature plan](FEATURE-CORRECTNESS-PLAN.md).


File ownership
--------------

- `mod/` contains the main package's 70 accepted runtime files.
- `src/` contains 1,123 owned source/metadata files. SFX and dialogue are partial
  overlays; player sources include the accepted loose animation and behavior folders.
- `packages/textures/mod/` contains the separate package's three local icon archives.
  These remain Git-ignored. Their header/data pair stays together.
- `reference/mapstudio/` retains two unshipped copies with unassigned provenance.
  They are not editing or packaging inputs.
- External Smithbox, Script, DSAnimStudio and SFX directories remain working copies.
  A saved editor file is accepted deliberately, not selected by timestamp.
- The verified stage selected in `.vdb/selected.json` supplies the release ZIP.
  Vortex owns deployment. Live game files are outputs and diagnostic evidence.

`asset-catalog.json` defines ownership and mappings. Workstation paths/tools belong in
ignored `tools/eldenring-paths.local.json`; VDB location belongs in `vdb.local.json`.
Native tools stay external. The main Vortex package also retains its existing
`mods/Scripts-Data-Exposer-FS.dll`; provenance and distribution remain release gates.


Normal edit and propagation
---------------------------

1. Read the relevant editing guide/update report and compare scoped repo/editor
   inputs. Preserve custom changes and choose a baseline by content.
2. Edit with the appropriate tool, build an isolated candidate, and inspect decoded
   differences. Build success alone does not prove intended gameplay.
3. Accept matching source/output together. Reload old editor buffers after handoffs.
4. Explicit propagation prepares an immutable package and queues VDB finalization
   across all game profiles. Enabled versions deploy when active and safe; disabled
   selections update without enabling/deploying; absent packages stay absent.
   After completion, refresh the local receipt to select the verified packaging stage.
5. Record actual gameplay results in TEST-MATRIX only after an observed game test.

```powershell
python tools/sovereign.py status --scope maps
python tools/sovereign.py status --scope events --sources
python tools/vdb_workflow.py doctor
.\tools\Propagate-Sovereign.ps1 -Scope maps
.\tools\Propagate-Sovereign.ps1 -Scope maps -Profile SkC-QjDMc
.\tools\Propagate-Sovereign.ps1 -Scope maps -StageOnly
.\tools\Propagate-Sovereign.ps1 -Receipt <pending-receipt> -Profile SkC-QjDMc
```

Omit `-Profile` to update all game profiles, including disabled selections. The
example explicit profile is this workstation's Elden Ring Default. It need not be
active to queue work. `-StageOnly` stages without changing profiles or selecting a
packaging source. The launcher defaults to editor input and the checked regular version from
`mod.json`, currently `1.0.1`; `-Source repo` selects accepted repo input explicitly.
It does not generate development labels or bump the version. Once a version is staged,
changed package bytes require a new target and matching changelog block.
See [release numbering and Grailwright parity](VDB-RELEASE-PARITY.md) for the initial
1.0.0 changelog, release checks and remaining promotion work.
The nine familiar external VBS filenames now call this launcher. They no longer purge
folders or copy directly into legacy Vortex/live paths. Logs and resume instructions
are under `.sovereign/propagation-logs/`. Never run archived old implementations.
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
Descriptions remain under `_/nexus-page/`. Keep page summary, file pitch, detailed BBCode
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
Earlier investigation prose is retained in [WORKFLOW-REFERENCE](WORKFLOW-REFERENCE.md)
and [WORKFLOW-PREP-HISTORY](WORKFLOW-PREP-HISTORY.md); those snapshots do not supersede
current commands or the editing guide.
