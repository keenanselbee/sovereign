# Inspect and choose a baseline

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
[layout and workstation guide](../REPOSITORY-LAYOUT.md).

Status lists differences and a count by default. Add `--verbose` to list matching
files too; `--json` retains every file, path and hash. Source comparisons perform
one scan rather than a separate runtime scan followed by the source scan. Each
catalogued row reports repo versus selected build (when packaged) and repo versus
saved editor (when mapped); a missing side is named explicitly. Source rows have
repo/editor comparisons, not a build comparison. Hash agreement is not gameplay
verification, and an unsaved editor buffer is outside this comparison.

`python tools/sovereign.py check` also verifies that every declared source group
has repository files, each declared text recipe exists and points to a catalogued
output, and those recipe paths are documented here. Runtime membership is checked
separately. Historical `.codex-temp` evidence may remain in documentation; a
scratch patch is not a substitute for a declared, durable recipe.

The catalog's `editing` records identify source-authoring, direct binary/text
editing and recovered overlays. `recoveredSources.manifest` points to
`src/extracted-members.json`. `check` reports missing/edited recorded sources and
archives whose hash no longer matches their recovered snapshot. These findings
also block repository package preparation and new draft/release ZIP creation.
Preparation rechecks freshness after copying. Historical retained artifacts and
their receipts remain unchanged; these checks do not launch Vortex or rebuild.

Recovered member refresh uses the existing scoped handoff. The plan reads a
changed selected archive with the native inspector, previews changed source
destinations and includes an updated manifest. It checks both ordinary editor
guards and recorded source hashes. A loose file changed independently must match
the selected packed member exactly, otherwise planning stops even with
`--resolve-conflicts`. A missing source also stops for explicit recovery.
Accept uses the normal backups/candidate publication/restore transaction; no
separate refresh daemon or database is involved. With no editor mapping, use
`--from repo` explicitly; snapshot-only changes are still a reviewable handoff.

```powershell
python tools/sovereign.py check
python tools/sovereign.py accept-plan --scope models --from repo
# Inspect the printed receipt, including recoveredSources and all entries.
python tools/sovereign.py accept --receipt <reviewed-handoff-receipt>
```

Existing event, player and dialogue qualification requirements still apply to
their scopes. A source edit requires a verified packed output before handoff;
this native extraction check does not qualify model/texture serialization or
gameplay. Only declared recovered members refresh. New custom members require
explicit manifest inclusion, and tracked removals/complete-set membership drift
stop for review. See [source ownership and coverage](../../src/README.md).

Archived vanilla candidates stay in `Z:/Backup`; their paths, known provenance
limits and catalogued-file hashes are recorded in
[the baseline inventory](../BASELINE-INVENTORY.md). Run
`python tools/inventory_archived_baselines.py --check` to verify the recorded
inventory; refresh intentionally after changing its catalog scope. These records
support future old-vanilla / modded / new-vanilla comparisons, not automatic merges.

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
[VDB-RELEASE-PARITY](../VDB-RELEASE-PARITY.md) before preparing the 1.0.0 release.
Stage submission now reserves a fixed payload for every package/version and reuses
matching prior requests/builds. Changed contents need a new label. Final release
packaging requires a matching selected release stage and retains its exact ZIP under
`.vdb/releases/`; follow the explicit freeze sequence in that release document.
Both main and texture publishing, promotion-only retries and read-only collection
readiness are implemented in [release automation](../RELEASE-AUTOMATION.md). Joint
updates are serialized textures first, main last; no commands publish implicitly.

The SFX and dialogue source folders are partial override sets, not complete vanilla
extractions. Source status compares those owned files without proposing to import
thousands of unrelated editor files. Adding a new override requires explicitly
placing/reviewing it in the repo source set. The four former dialogue source
differences were reconciled through the qualified handoff in the checkpoint.
