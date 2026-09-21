VDB and versioned release workflow
=================================

Current completion policy, 2026-09-20: each completed batch of changed packaged
files includes a version bump, verified manual-editor sync, and queued VDB
finalization. Enabled mods deploy when active and safe; closed Vortex processes
the queue next launch. Disabled/absent packages remain so. Explicit stage-only
requests override the default. Documentation/tooling outside the package and
identical retries do not produce another mod version. The agent updates version
and changelog before using the existing launcher, which does not author them.
Main 1.0.1 is staged, enabled, and deployed with verified live bytes in the Elden
Ring Default profile; textures retain their unchanged 1.0.0 payload. The existing
protocol-3 finalization reused build `47e326a49d8cc47e85a274b8` without restaging
different contents or bumping its version. Its completed receipt is
`.vdb/finalizations/default-completion-1.0.1/receipt.json`, request
`c21404b1-9f88-43d8-a58e-f2c1c0638033`. The verified build is now the selected
packaging source. This is deployment verification, not gameplay acceptance.

Seven existing finalization tests passed after the policy update, including
closed-Vortex submission, resume without duplicate submission, disabled-profile
handling, and stage-only behavior. Closed-Vortex behavior was covered by fixtures;
this live 1.0.1 finalization completed with Vortex running. No bridge code or
installation changes were required: both client and extension advertise
`profile-finish-v3`. The snapshot envelope's `protocolVersion: 1` alone is not a
capability failure; use the full capability check.

Historical target, 2026-09-19: the author requested **1.0.0** for both main and textures.
Neither package had a regular-version stage or reservation, so the unstaged 1.0.1
workflow notes were consolidated into 1.0.0 without relabeling a retained build.
The Hadeon encounter changes and one-frame opening deflect adjustment are included;
gameplay acceptance remains pending and `releaseReady` remains false.
Both packages were subsequently [deployed and verified locally](DEPLOYMENT-1.0.0.md).

Current policy: propagation uses
the checked regular target without a development suffix. Bump `mod.json` and add
a matching changelog block before staging changed bytes under a used version.
Identical package/version retries reuse their immutable build. The old `dev-version`
command remains a compatibility alias for `target-version`, returning the regular
target. Existing development stages and recovery receipts retain their original
identities. This metadata change does not stage, deploy, publish or establish acceptance.
The client check accepts protocol 1, 2 and 3. New propagation requires
`profile-finish-v3` and queues all game profiles by default, with explicit profile
and stage-only modes. Disabled selections remain disabled; absent packages stay
absent. The bridge resumes pending profile work automatically. Refreshing the local
propagation receipt selects the verified packaging stage after completion.

The following review records the earlier 1.0.0 baseline, superseded by that policy.
Reviewed 2026-09-11 against the local Grailwright implementation. Sovereign's VDB
development workflow is operational. The initial authored release target is now
**1.0.0**, with `releaseReady: false`. This is a local target, not a published release
or a claim that pending game tests passed.


Current comparison
------------------

| Area | Grailwright | Sovereign |
|---|---|---|
| Stable package identity | Per-mod catalog, shared versioned VDB client | Implemented: existing `sovereign/main` and `sovereign/textures` identities |
| Immutable stages and receipts | Archive-backed, durable stage receipt, waits for completion | Implemented: verified prepared directory, durable stage/operation receipts, pending requests resumed |
| Activation | Ordinary builds stay local; explicit final staging/deployment | Builds stay local; low-level stage is stage-only; explicitly invoked propagation composes handoff, stage, deploy, verify and select |
| Version ownership | Fixed payload per staged version, exact archive reuse | Implemented: fixed payload per package/version, stage/request reuse, retained release ZIP |
| Package source | Verified artifact associated with its stage | Verified selected Vortex stage; exact ZIP entry and payload verification |
| Version consistency | Manifest, plugin/assembly, README, changelog and optional built DLL checks | Added manifest/history check; no plugin assembly version exists for this asset mod |
| Changelog | Complete plain-text history plus reviewed Nexus consolidation | Added root history and initial 1.0.0 consolidation |
| Published release identity | Exact-stage promotion after upload, explicit retry | Implemented: exact uploaded-build receipt, promotion and safe retry |
| Collection readiness | Rejects local/unverified builds | Implemented: fresh enabled-build check against exact promotion receipts |
| Separate texture release | Independent package identity/file group | Implemented: verified texture ZIP, separate group, non-primary upload before main |

The existing shared bridge should remain the integration. Do not duplicate it or
rename the current package IDs: those IDs already own retained stages and rollback
history. Preserve Elden Ring's `mod/` plus `mods/` layout; Grailwright's BepInEx
package-folder layout and assembly checks do not apply here.


Observed health and changes made
-------------------------------

The live bridge reported client/extension 0.1.0, protocol 1, and the existing Elden
Ring Default profile `SkC-QjDMc`. Current selected builds are main
`fb233a986dfb581405a38222` and textures `fe46cb9983080cddbe556f20`.
Both stages and their live files were compared by hash. The prior gameplay report
retains the original deployment and rollback evidence.

An audit bug was fixed: status and inventory review previously inspected the old
configured `Sovereign` folders while packaging inspected selected VDB stages. They
now resolve the same verified selected stage per package. With no selection they
retain the legacy fallback; selected-stage drift fails explicitly. Source acceptance
still operates only on the catalogued repo/editor paths.

`mod.json` now selects 1.0.0. Root `changelog.txt` begins the new release series with
implemented changes in the current development baseline. Its older 1,081-line
history, beginning at `11.0-1.16`, is retained byte-for-byte in
[reference/changelog-before-1.0.txt](../reference/changelog-before-1.0.txt). The
historical file was recovered from the verified full backup and matched Git HEAD;
SHA-256 is `05128d596abcbe26e69f196accdc3803f40c0f14e6a45f4080a573adfeba5f8f`.
It is reference material, not a version sequence to sort after the new 1.0.0 series.
Keep the existing tracked lowercase filename so Windows and case-sensitive checkouts
resolve the same file. The Nexus API was read on 2026-09-11 and confirmed active version 0.1 in
group 893965 (immutable version 18610093305851). The local Nexus changelog therefore
uses `TargetVersion=1.0.0` and `BaselineVersion=0.1`; publishing rechecks that baseline.
That mapping was superseded by the author's main/texture API screenshots and fresh
API reads: main is group `7949853`, textures is `893965`, both active at `0.1.0`.
The local main changelog now uses `TargetVersion=1.0.0` and `BaselineVersion=0.1.0`.
The notes remain subject to game acceptance and final release review.

Both mappings now live in `mod.json` and are checked against `vdb.json`. Submitted
receipts from the old mapping remain readable only when their project hash differs
by this exact Nexus metadata correction; other configuration drift still fails.
Unsubmitted old candidates must be prepared again. Existing stages and receipts
are not rewritten, registered, deployed or promoted by the correction.

The current selected main build keeps its original `0.0.0-dev.20260911-gameplay`
label. Retained stages were not renamed or changed. Future ordinary propagation
uses `1.0.0-dev.<UTC timestamp>` until the authored target changes. No new stage,
deployment, upload, or collection mutation was performed for this workflow review.

Verification passed: 82 workflow tests, repository check, local Nexus structure and
changelog payload checks, and PowerShell parsing of the propagation launcher. All
73 catalogued runtime comparisons matched; all 74 selected-package live files
(including the DLL) matched their immutable receipts. These results establish file
and workflow consistency, not gameplay acceptance.


Version and changelog rules
---------------------------

Use `mod.json` as the one authored release-version source. Match Grailwright's
numbering: `MAJOR.MINOR.PATCH`, with one-digit minor and patch components. Thus
1.0.0, 1.0.1 through 1.0.9, then 1.1.0; 1.9.9 rolls to 2.0.0. Major may exceed nine.
New propagation uses that regular target directly. Historical development labels
remain readable; do not rename retained stages or generate new timestamped labels.

Keep root `changelog.txt` newest first:

```text
Version 1.0.1
Describe the completed change.

Version 1.0.0
Retain the previous version's change lines.
```

No Markdown bullets, blank line after a header, duplicate blocks or duplicate change
lines within a block. The checker rejects malformed numbering, out-of-order history
and a newest version that disagrees with the manifest. `check` and release Nexus
checks include this validation. Publishing also fingerprints the history so edits
during preflight invalidate the plan.

```powershell
python tools/sovereign.py version-check
python tools/release_workflow.py target-version
python tools/sovereign.py nexus-check
```

The separate `_/nexus-page/nexus-changelog.txt` is the reviewed upload payload,
not the full history. Consolidate every unpublished local version into final-state
change lines under matching target/baseline headers. Never copy intermediate version
headings into that payload. Keep short and file pitches stable unless the mod's
identity changes. Existing published 0.1 remains historical, rather than being
renamed or rewritten as 1.0.0.


Remaining implementation stages
--------------------------------

1. **Release artifact binding is implemented locally.** Release receipts contain the
   exact VDB package/build/stage identity and intended release version. Packaging
   requires a matching completed selected stage and rejects version/stage/payload
   drift. The verified ZIP and receipt are retained under `.vdb/releases/main/<version>/`;
   identical retries reuse those bytes. Publication accepts only that retained ZIP.
   The actual 1.0.0 freeze remains pending acceptance; metadata checks do not relabel
   test stages or mark them published. See the commands below.
2. **Promotion and safe retry are implemented locally.** Confirmed uploads create
   durable exact-build release receipts; VDB promotion is submitted once and pending
   retries wait on that request. Upload resumes use the shared original journal and
   refuse uncertain POST outcomes. Missing game-scoped file IDs stay pending.
3. **Texture release support is implemented locally.** Both catalogued texture
   companions remain together in a verified retained ZIP. The coordinator publishes
   textures non-primary before main, validates both before the first upload and
   prevents a failed texture step from being bypassed by a main-only retry.
4. **Collection readiness is implemented locally.** A read-only check compares both
   enabled packages against exact retained files, promotion receipts and Nexus IDs.
   Local, pending, mismatched, missing and unavailable states are not ready. Separate
   follow-up work remains: enforce current-build manual test evidence automatically,
   and improve independent file-pitch/changelog observation in the combined audit.
5. **Qualify and release 1.0.0.** Run pending game scenarios, verify DLL provenance
   and redistribution, test clean installation with textures, and review the full
   description against observed mechanics. Inspect both final ZIPs. Publishing and
   promotion follow an explicit release instruction; record resulting remote IDs
   and collection readiness. The first real upload/promotion still needs end-to-end
   verification, even after intercepted contract tests pass.

See [release automation](RELEASE-AUTOMATION.md) for commands and recovery. The 104
workflow tests passed; the new release path still needs its first explicitly authorized
live upload/promotion. Keep gameplay changes separate from this workflow work. Current HKS, behavior,
animation and special-effect questions remain governed by the feature plan and
manual matrix; VDB byte agreement does not settle those questions.


Freezing an accepted main release
--------------------------------

Normal builds remain isolated and explicit test propagation retains unique development
labels. Stage submission reserves each package/version under `.vdb/staged-versions/`
before contacting VDB. Identical retries reuse the original request/build; changed
contents require a new label. Older stage receipts are checked too. Missing or altered
retained payloads and uncertain submissions require inspection, never a fresh submission
under the same label. Keep reservations and prepared receipts across scratch cleanup.

After game acceptance, freeze the verified selected bytes under the authored release
version. For the current 1.0.0 target, the explicit sequence is:

```powershell
python tools/vdb_workflow.py prepare --package main --version 1.0.0 --from vortex
python tools/vdb_workflow.py stage --receipt <prepared-receipt>
python tools/vdb_workflow.py wait --receipt <prepared-receipt>
python tools/vdb_workflow.py select --receipt <completed-receipt>
python tools/nexus_workflow.py package --release --version 1.0.0
```

Do not use the legacy-folder fallback for a release freeze: a verified selected tested
stage must already exist. Wait for completion before selection. These low-level stage
and select commands do not activate the build; any desired deployment remains explicit.
Release readiness/dependency checks still apply. Packaging returns the durable retained
ZIP, and the publisher checks the selected identity and exact ZIP again before upload.
Draft candidates stay in `.codex-temp`; old scratch-only release ZIPs must go through the
new release packaging route before publishing. Interrupted retention fails closed: inspect
the partial directory and its candidate receipt before recovery, never overwrite it.
Upload journals now stay beside the retained release ZIP; preserve older scratch journals
as well. Promotion is implemented; current-build manual-test enforcement remains follow-up work.


Reference implementation
------------------------

Grailwright's relevant files are `tools/Stage-VortexMod.ps1`,
`tools/VortexDevelopmentBridge.ps1`, `tools/Promote-VortexRelease.ps1`,
`tools/Test-VortexCollectionReadiness.ps1`, `tools/Test-ModVersionConsistency.ps1`,
`tools/Export-VortexPackage.ps1`, and its root `AGENTS.md`. Review their current
contracts when implementing the remaining stages. The local Grailwright review
found a policy/checker discrepancy: its version regex permits multi-digit minor
and patch components although its instructions forbid them. Sovereign's new checker
enforces the documented convention directly.
