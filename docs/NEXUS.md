# Nexus API and Sovereign release target

Package-source update: when `.vdb/selected.json` selects a completed main build,
the existing packaging commands read that exact Vortex stage and reverify its full
inventory against the stage receipt. Drafts without a selection use the configured
legacy Sovereign package. Final releases require a completed selected stage with
the exact release version, and retain the verified ZIP and its stage identity under
`.vdb/releases/main/<version>/`. Identical retries return that ZIP; publication
rejects scratch-only archives or changes to the selected build/contents. They never
fall back from a drifted selected stage to
different bytes. See [the current workflow commands](WORKFLOW-COMMANDS.md) for
stage preparation/selection; publishing and release gates below still apply.

Versioning update 2026-09-11: `mod.json` now selects **1.0.0** as the local release
target, with full version history in root `changelog.txt`. This does not relabel the
selected development build or mark the mod release-ready. `version-check` validates
the target/history; release packaging and publishing also require that consistency.
The publisher fingerprints the history during its preflight. See
[VDB release parity](VDB-RELEASE-PARITY.md) for the remaining promotion workflow.

Historical API review, 2026-09-09, against the published [Nexus OpenAPI specification](https://api.nexusmods.com/openapi.yaml)
(OpenAPI 3.0.3, API version 3.0.0; server `https://api.nexusmods.com/v3`).
The inspected specification's SHA-256 is
`1dc1ade76e9fd73f7edf3bebab41e7bc4b1c3578e87f85d70f0ad09b7e2c7746`.
A temporary snapshot is in `.codex-temp/nexus-api-audit/openapi.yaml`. Runtime checks
use the API contract directly; they do not download or execute a specification file.
Recheck the published contract before changing the client or adding publishing.

## Configured files and publication order

Public identifiers belong in `mod.json`. Credentials belong only in the
`NEXUS_API_KEY` environment variable, never in manifests, scripts, arguments or chat.

| Identifier | Value | Meaning |
|---|---|---|
| Game domain | `eldenring` | Nexus game slug |
| Page ID | `201` | Game-scoped mod ID used in the page URL |
| Unique mod ID | `18610093293769` | v3 `/mods/{id}` identifier |
| Main group ID / API File ID | `7949853` | Persistent Sovereign main file |
| Main Short Unique File ID | `sVKWduzP0` | Author-confirmed UI identifier |
| Texture group ID / API File ID | `893965` | Persistent Sovereign - Textures file |
| Texture Short Unique File ID | `qdbCxL2mS` | Author-confirmed UI identifier |

The author confirmed these mappings with both Advanced/API dialogs. Fresh read-only
API calls confirmed main's primary version **Sovereign 0.1.0**, immutable v3 ID
`18610093344220`, game-scoped file ID `50652`; textures' non-primary version is
**Sovereign - Textures 0.1.0**, immutable v3 ID `18610093305851`, game-scoped file ID
`12283`. The API's parent group names remain misleading: main's is
`Sovereign -  Textures`, and textures' is `Sacred Tweaks`. Use the confirmed IDs,
not those historical names. Earlier notes treating 893965 as main are superseded.

`mod.json` is the authored metadata source: `nexus.groupId` identifies main, and
`nexus.textures.groupId` identifies textures on the same page. Keep this metadata
there instead of introducing a duplicate `API.txt`. The shared API transport,
credential handling and ID meanings match Grailwright despite the different filename.

When both packages are updated together, publish and verify textures first, then
publish main last. This is the author's ordering requirement so main stays above
textures in the files list. Serialize the uploads; resolve any failed or uncertain
texture upload before proceeding to main. Main remains primary; textures remain
non-primary. A textures-only update does not call for a duplicate main upload just
to reorder the page. The combined publisher now enforces this sequence and supports
texture-only publication. See [release automation](RELEASE-AUTOMATION.md) for review,
publication, exact-operation resume, promotion and collection-readiness commands.

Historical groups and archived versions remain untouched. The short UI identifiers
come from the author's screenshots; the read endpoints do not independently verify them.

## Repeatable checks

```powershell
python tools/sovereign.py nexus-check
python tools/sovereign.py nexus-status
```

`nexus-check` checks local description structure and metadata without networking.
`nexus-status` performs three authenticated GETs: resolve the Elden Ring page,
list its file groups, then list the configured group's versions. It rejects identity
mismatches and unexpected response shapes. It selects an active primary version,
or the only active version when no primary exists. Ambiguity remains Verify (exit 2).
Errors remain Verify (exit 1); no stale result is substituted. Successful observations
are printed as JSON, not saved as release receipts. The API host is fixed and
redirects are refused so credentials cannot be forwarded to a different host.

An equal version label does not prove equal archive contents. Page copy, file pitch,
changelog, visual rendering and mechanics still need separate verification. The
selected local release version was unset at that review. Short/file pitches now have local drafts;
the full description still needs the mechanics review described below.

## Description workflow (Grailwright conventions)

`mod.json` selects `_/nexus-page` as the description directory. These are the three
authoritative files; do not create competing copies at the repository root.

| File | Nexus destination | Editorial rule |
|---|---|---|
| `nexus-short-desc.txt` | Page summary | At most 350 characters; stable identity and player experience |
| `nexus-file-desc.txt` | File-row description for main group `7949853` | At most 255 characters and shorter than the summary; a distinct, persuasive pitch |
| `nexus-full-desc.txt` | Main page description | Detailed features, requirements, installation and compatibility in Nexus BBCode |

`description-bbcode.txt` is the historical reference, not a second publishing source.
`nexus-changelog.txt` holds completed release changes separately from the pitches.
Never repeat the full description in README or use the file pitch as a changelog.

Keep short and file descriptions stable across normal fixes, tuning and feature
growth. Rewrite them only when the mod's central identity or promise changes.
Keep the file pitch distinct in meaning and phrasing, not just shortened or lightly
reworded. The checker rejects exact normalized copies; editorial review catches
near-copies. Use ASCII punctuation and plain `[code]` blocks, not Markdown fences or
`[code=...]`. Preserve Sovereign's existing color/theme and page voice. Tables belong
inside plain code blocks with pipe columns and a separator row.

### Local editing and review

1. For `NEXUS`, check local files and inspect fresh remote file/page evidence. Report
   Current / Update / Verify separately for the release file, short description,
   file pitch, full description and changelog. Unknown evidence stays Verify.
2. Compare features added since the active release with the full page. Propose the
   smallest edits that describe behavior still present in the intended release;
   leave superseded implementations and routine history in the changelog.
3. A normal request to edit descriptions authorizes local copy changes. Read
   `docs/MECHANICS.md` and the affected source/test evidence first. In particular,
   crystal activation, Shrine persistence/rewards and Obliterator acquisition are
   unresolved; the current full draft must not be treated as verified merely because
   its BBCode passes. Do not invent requirements, percentages or acquisition paths.
4. Run `python tools/sovereign.py nexus-check --descriptions-only` and review the
   actual wording. This checks all three files without requiring a new release
   version. Run the ordinary `nexus-check` for release metadata checks as well.

### Saving an explicitly requested Nexus update

Updating this workflow or editing local drafts does not itself publish them. A clear
request to save the descriptions, or an affirmative reply to a concrete pending
Nexus update proposal, authorizes the specified save. Carry that authorization
forward; do not ask again for the same changes.

- For a description-only update, use the three files above and save only the requested
  changed fields. Short/full descriptions belong to the page editor. The file pitch
  belongs to the existing file's editor; verify its current immutable version within
  main group `7949853` before editing. A page-description save alone does not save the pitch.
- Before saving, refresh the relevant remote values, retain their exact prior text
  in `.codex-temp/nexus-description-backups/`, and record which local file hashes are
  being applied. Serialize Nexus writes with the repository's `operation('nexus')`
  lock for the complete review/save/verification operation. Recheck source hashes
  and target identity before applying; re-review if either changed.
- Use the available authenticated browser tooling for description saves. Reopen the
  saved editor fields and compare them with the approved local text, accounting only
  for known line-ending/editor normalization. Check the rendered page too. Record
  the target IDs, source hashes, backup path, time and outcome under
  `.codex-temp/nexus-description-results/`. Saved text and verified rendering are
  separate observations; report partial success without repeating completed writes.
- If a file version is already current, retain it while saving changed descriptions.
  Do not upload duplicate bytes or append a duplicate changelog to refresh page copy.
  A full release request also needs the verified archive/version and release gates.

This matches Grailwright's source-file roles, editorial rules and review/save behavior.
Sovereign now has standalone review/save and publishing wrappers, plus a combined
audit. The editor interaction code was adapted from Grailwright, with repository-owned
paths, a dedicated Chrome profile and the shared `operation('nexus')` lock. Do not
invoke Grailwright's script directly against this repo.

## What the API supports

- Uploading a new version: create a multipart upload with integer `size_bytes` and
  `filename`; PUT each part to its presigned URL; collect ETags; POST completion XML;
  POST `/uploads/{id}/finalise`; wait for `state: available`; then POST
  `/mod-files/{groupId}/versions` with the upload ID and reviewed file metadata
  (`7949853` for main, `893965` for textures).
- The old `/mod-file-update-groups/{group_id}/versions` endpoint is deprecated and
  eligible for removal on/after 2026-09-09. Use `/mod-files/{id}/versions`.
- POST `/mods/{id}/changelogs` appends entries, including when a version already
  exists. Reconcile after partial success; never blindly repeat an upload or changelog.
- PUT `/mod-files/{id}` updates the persistent file's name. It does not update the
  full page description. This spec exposes no main-page short/full description edit
  endpoint; those remain browser operations.
- The listed version-read schema lacks file-description and archive-hash fields.
  Do not claim that this GET verifies either surface.
- The announced MD5 requirement on/after 2026-12-01 applies to single-part uploads
  and the matching `Content-MD5` PUT header, not the documented multipart request.

Several mod/file endpoints are experimental. Publishing is an explicit operation,
separate from the default audit and dry run.
For a future release, use the existing Elden Ring packaging and propagation workflow,
an exact reviewed archive, fresh remote state, a lock and an immutable upload receipt.
Nexus publishing is separate from copying editor outputs into repo/live/Vortex.

## Audit of the other repositories

Grailwright's `tools/Publish-NexusMod.ps1` uses the documented `apikey` header,
multipart/ETag/completion/finalise/available sequence and current version-creation
endpoint. Its payload flags and `data.version.id` response lookup match the spec.
Its browser-based description editor remains appropriate. No upload was performed
as part of this audit, so this is contract review rather than end-to-end qualification.

Findings to address in Grailwright before adapting its uploader:

1. `Send-MultipartUpload` casts `size_bytes` to `[string]`; `CreateUploadRequest`
   requires an integer/int64. Send `[int64]$archiveItem.Length`. Server coercion may
   currently accept it, but the existing JSON does not conform to the schema.
2. `Get-CurrentRemoteFileVersion` falls back only to Main files when none is primary.
   A group containing only active Optional or Miscellaneous files cannot resolve its
   changelog baseline. This does not block Sovereign's current Main file.
3. The version reread probes description fields that the published schema does not
   promise. It records whether they were verified; preserve that distinction and
   retain browser verification when fields are absent.

Grailwright also assumes its own manifests, BepInEx package layout, helper scripts
and Vortex extension. Do not copy its publisher into Sovereign without adapting
those dependencies. No Grailwright files were changed in this audit.

The website repo `keenanselbee.com/worker/index.js` uses the separate v2 GraphQL API
for a daily public `user.memberId` / `uniqueModDownloads` query. The supplied v3
contract has no equivalent profile-total endpoint, so changing only its base URL
would break it. Its existing timeout, identity/count validation and stored fallback
are appropriate. A live invocation with an in-memory storage stub succeeded and its
four existing Worker tests passed; no deployed storage or website files were changed.


## Standalone commands and the NEXUS chat command

```powershell
# One-time local dependency setup (already completed on this workstation):
.\tools\Update-NexusDescription.ps1 -Setup
# One-time interactive Nexus login in Sovereign's dedicated Chrome profile:
.\tools\Update-NexusDescription.ps1 -LoginOnly
# Audit: API + Vortex package inventory + short/full browser comparison:
.\tools\Get-NexusLiveState.ps1
# Only compare short/full descriptions (default does not save):
.\tools\Update-NexusDescription.ps1
# Explicit page save or restoration after reviewing the corresponding operation:
.\tools\Update-NexusDescription.ps1 -Save
.\tools\Update-NexusDescription.ps1 -BackupPath <backup-json>
.\tools\Update-NexusDescription.ps1 -BackupPath <backup-json> -Save
# Inspect/upload an already verified, non-draft Vortex candidate:
.\tools\Publish-NexusMod.ps1 -ArchivePath <zip>
.\tools\Publish-NexusMod.ps1 -ArchivePath <zip> -Publish
```

Node.js 22+, npm, installed Chrome and Python 3.11+ are needed. Configure the ignored
`nexus-automation.local.json` with an absolute `toolRoot` pointing to the separate
`@keenan/nexus-automation` checkout, or set `NEXUS_AUTOMATION_ROOT`. Setup runs
`npm ci` there using its lockfile (Playwright 1.62.0), without installing another
browser. No Grailwright checkout is required at runtime. Both repositories can
share that package and its `.local` state; when using separate package checkouts,
set the same absolute `NEXUS_AUTOMATION_STATE_ROOT` for both consumers. Login uses a visible dedicated Chrome
window; review/save use the same regular Chrome profile and close it afterward. The
shared engine launches installed Chrome directly, with its sandbox enabled, then attaches
Playwright over a dedicated loopback DevTools port, matching Grailwright's approach.
It does not use Playwright's browser-launch defaults or `--no-sandbox`. Do not run
another browser against the same profile concurrently. API credentials are omitted
from the browser process environment. Login credentials/cookies stay in the ignored
profile directory. No personal browser cookies are copied into it.

Sovereign retains its packaging/release gates, reviewed changelog policy, Elden Ring
identity checks, audit format, and existing wrapper defaults. The shared package
owns the editor, API/storage transport, multipart upload, source rechecks, page/profile
locks, browser ownership records, and publication journal. Existing browser profiles,
description backups, and upload journals keep their locations and remain ignored.

The `NEXUS` chat command is the coordinator, as in Grailwright: run the combined
audit, review feature evidence, report Current / Update / Verify for each surface and
propose the exact outstanding changes. An affirmative reply authorizes those proposed
changes. Refresh the affected inputs, perform the needed operations and verify their
outcomes; retain an already-current version instead of duplicating it. The audit itself
never builds a ZIP, posts a changelog or saves a description. It does write local
browser observations/backups. `-SkipBrowser` is available for API/package-only audits.

File-row description and changelog reads are still browser fallback steps; the
combined audit explicitly leaves them Verify. New-version uploads submit the file
pitch and changelog. An existing file-pitch-only edit remains an agent browser step.
The standalone page editor handles short/full descriptions only. The API uploader
does not rename the historical persistent group or alter Vortex metadata/deployment.

The publisher checks release readiness, selected version, dependency verification,
local copy structure, current remote group/version, exact ZIP entries/hashes and
unchanged Vortex contents before uploading. Draft archives are refused. It expects
`nexus-changelog.txt` to begin with `TargetVersion=<selected-version>` and
`BaselineVersion=<active-version>`, then reviewed change lines. It refuses a target
version label already found in this group, including archived versions.

Publishing defaults to a read-only plan. `-Publish` uploads multipart data with an
integer byte size, finalises it, waits for availability, rechecks inputs/remote state,
creates a new Main version with the existing version as its predecessor, appends the
reviewed changelog and rereads the immutable created version ID. It requests that the
new file be primary, allows mod-manager downloads, shows requirements, updates the
page version and archives the predecessor. Review these flags before the first real
release; they are not evidence that the current release already uses them.

Every upload attempt creates `upload-journal.json` next to the package receipt.
Its last stage distinguishes upload preparation, an uncertain version POST,
confirmed version creation, an uncertain changelog POST and verified version reread.
An existing journal prevents an automatic retry. Reconcile remote outcomes first;
never delete the journal merely to make a retry run. A successful version upload
still needs the separate short/full save and file/changelog rendering checks.

The shared CLI supports explicit `resume --journal <path>` after inspection for
safe stages with known upload/version identity. It refuses uncertain version or
changelog POST outcomes and legacy journals. It never restarts a partial upload.
Preserve the exact package directory and its receipt/journal after publication;
new release archives/journals are retained under `.vdb/releases/`. Preserve legacy
scratch journals too; cleaning `.codex-temp` indiscriminately would discard them.

### Shared extraction qualification on 2026-09-10

The shared package's preservation record maps transport, editor, ownership, locking,
failure/recovery, and adapter fixture tests to the original capabilities. Sovereign's
Python packaging/audit tests and intercepted editor tests also run against it.
The extraction did not perform an authenticated editor save, live upload, changelog
POST, or Vortex deployment. The earlier live observations below are historical,
not qualification of this new implementation.

### Qualification on 2026-09-09

- Python tests cover Vortex-only files, DLL/zero-byte preservation, explicit exclusions,
  source drift, release gates, multipart integer sizes/ETags/finalisation, changelog
  baseline checks and refusal to repeat a partially successful upload.
- Intercepted local Chrome editor tests cover read without saving, fill, save, reload
  verification, restoring prior values, and refusing a save after local source drift.
  They do not send requests to Nexus or prove the current Nexus editor is unchanged.
- A complete test ZIP was built from the actual Vortex source: 70 files, 347,157,794
  uncompressed bytes, 20 authoring exclusions. Each ZIP entry was verified against
  the source snapshot. The candidate remains under `.codex-temp/vortex-packages/`.
- A live read-only audit confirmed Sovereign 0.1 in group 893965. The new browser
  profile could not access the Manage editor. Run `-LoginOnly`, then repeat the review
  to qualify the authenticated editor path before the first actual save. No Nexus
  save, upload, changelog POST or Vortex mutation was performed during qualification.

Follow-up: the initial Playwright browser launch displayed `--no-sandbox` and the
author reported a Cloudflare challenge. The launcher now starts regular installed
Chrome and attaches over CDP, as Grailwright does. Login succeeded with this route.
The editor opens directly at the validated `/edit/general` URL, avoiding the public
page's asynchronously loaded Manage menu. A live authenticated comparison then
read both description fields and saved a local backup successfully. Both local
drafts differ from the live copy; no remote text was changed. Evidence is under
`.codex-temp/nexus-description-requests/1789010319332831400/result.json`.
The real save operation remains untested; the live review and local fixture save
tests are distinct qualification results.

Verification commands:

```powershell
python -m unittest discover -s tools/tests -v
node --test tools/nexus/test-description.mjs
python tools/sovereign.py check
python tools/sovereign.py nexus-check --descriptions-only
```
