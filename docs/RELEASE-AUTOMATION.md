Release automation
==================

Both packages now support verified retained ZIPs, journaled Nexus publication,
exact-build VDB promotion and read-only collection readiness. The repository owns
package policy; transport and Vortex mutations use the existing shared tools.
The workflow was verified with intercepted local fixtures. No live upload or
promotion was performed to qualify this implementation.


Prepare and review
------------------

After acceptance, prepare/stage/wait/select each release from its verified tested
bytes using the sequence in [VDB-RELEASE-PARITY](VDB-RELEASE-PARITY.md). Use the
authored version for both packages initially. Packaging never stages or deploys.

```powershell
python tools/nexus_workflow.py package-plan --package main
python tools/nexus_workflow.py package-plan --package textures
python tools/nexus_workflow.py package --package main --release --version 1.0.0
python tools/nexus_workflow.py package --package textures --release --version 1.0.0
```

Release readiness/dependency checks still apply. Drafts use the same commands
without `--release`. Texture ZIPs contain the catalogued `mod/menu/hi/` assets,
including both header/data companions, and are installed alongside main. Main keeps
its `mod/` and `mods/` layout. Exact release ZIPs and receipts live under
`.vdb/releases/<package>/<version>/`; do not rebuild or overwrite them for publication.
Current-build manual test evidence remains a separate acceptance requirement;
automatic enforcement of that evidence is not yet implemented.


Publish and resume
------------------

```powershell
python tools/release_pipeline.py release --textures <texture-zip> --main <main-zip>
python tools/release_pipeline.py release --textures <texture-zip> --main <main-zip> --apply
python tools/release_pipeline.py release --textures <texture-zip> --main <main-zip> --apply --resume
```

Without `--apply`, the command reviews inputs and remote baselines without writes.
All packages pass preflight before any upload. A joint release uploads and verifies
textures first, then main last. Textures are non-primary and do not update the page
version; main remains primary. Nexus changelogs belong to the mod, so main posts the
reviewed block once. Textures use `nexus-textures-file-desc.txt` as their separate
file pitch. A textures-only release does not append duplicate main changelog notes.
Descriptions of the mod page are still saved separately through the existing tool.

Omit one archive for a single-package update. An unfinished batch must resume with
its original package set and exact archives; it cannot be bypassed by requesting
main alone. The existing `Publish-NexusMod.ps1` wrapper also uses this coordinator:
`-ArchivePath <main-zip> -TexturesArchivePath <texture-zip> -Publish`, with `-Resume`
for explicit recovery. A textures-only wrapper call uses `-Package textures`.

Every upload retains its shared journal beside its ZIP. Confirmed uploads are
rechecked by immutable Nexus version ID and never repeated. Resume uses the shared
publisher's original request and fingerprint. An uncertain upload, version POST or
changelog POST requires reconciliation and is not repeated automatically. Batch
progress is under `.vdb/release-batches/`; package journals remain authoritative
even if a process stops before the batch receipt records completion.


Promotion and collection readiness
----------------------------------

After verified uploads, the coordinator records `nexus-release.json` with exact
stage/build, version, SHA-256, MD5, size, group, immutable Nexus version and numeric
game-scoped file IDs, then promotes those exact builds through VDB. A missing numeric
file ID stays pending. `promotion.json` records submission before invoking VDB;
pending retries wait on the same request. Interrupted/failed/expired requests need
inspection, never blind resubmission. Existing confirmed release identities are not
overwritten. Promotion changes publication metadata, not enablement/deployment.

```powershell
python tools/release_pipeline.py promote --archive <retained-zip>
python tools/release_pipeline.py readiness
```

Promotion retry never uploads, and can address an older retained build after the
selected development build changes. It rechecks the retained payload and remote
identity. Readiness does not register, upload, promote, enable or deploy anything.
It requires a fresh active Elden Ring profile and both enabled packages to match
their retained payloads, successful promotion receipts and exact Nexus file IDs.
It reports local, pending, mismatched and promoted packages, missing packages and
unavailable observations. Exit 2 means pending promotion or not ready; exit 1 is an
error. A passing report does not establish gameplay acceptance.
