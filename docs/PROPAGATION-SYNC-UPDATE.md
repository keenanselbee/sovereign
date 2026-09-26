Sync-only propagation
=====================

The nine active shortcuts under `Z:\Modding\Elden Ring` now call the shared
`tools/Propagate-Sovereign.ps1` sync-only launcher. Their filenames and scope mappings
are preserved. Build and deployment are separate requested work; propagation does
not read/check release metadata, choose a VDB baseline, prepare a package or call Vortex.

| Workspace / shortcut | Accepted scope |
|---|---|
| Smithbox / `propagate-regulation.bin.vbs` | Regulation and tracked row-name JSON |
| Smithbox / `propagate-map.vbs` | Five catalogued map files |
| Smithbox / `propagate-item.msgbnd.dcx.vbs` | Only `item_dlc02.msgbnd.dcx` |
| Script / `propagate-event.vbs` | Saved event sources and matching compiled outputs |
| Script / `propagate-c0000.hks.vbs` | Coordinated player group |
| Script / `propagate-c9997.hks.vbs` | Coordinated player group |
| DSAnimStudio / `propagate-c0000.anibnd.vbs` | Coordinated player group |
| DSAnimStudio / `propagate-c0000.behbnd.vbs` | Coordinated player group |
| SFX / `propagate-sfxbnd_commoneffects.ffxbnd.vbs` | Common-effects archive and tracked source overlay |

Player qualification covers HKS/names, animation and behavior assets and their
tracked sources together. It rejects unresolved saved DSAnimStudio projects and
does not claim generic Lua compilation proves Havok Script compatibility. Events
retain native saved source/output checks. Valid cached qualifications remain reusable.
Maps, regulation and text use saved-file ownership, conflict and hash checks, not
gameplay validation. Save open editor buffers before syncing.

SFX retains its local WitchyBND repack/save with a backup and full-source guards.
This keeps the packed archive consistent with saved effects; it is not a Vortex build.
New source overrides still require explicit ownership in the repository overlay.

Each sync links a guarded handoff receipt, exact before/after hashes, qualification
evidence and independent backups. Unchanged inputs still validate and record a
successful receipt. Conflicts, missing inputs and drift stop acceptance. An
interrupted operation retains child receipts for inspection/restore; a successful
handoff followed by an SFX guard failure is not reported as a completed sync.

Sync receipts live under `.sovereign/sync/`, handoffs/backups under
`.sovereign/handoffs/`, and launcher logs under `.sovereign/propagation-logs/`.
The shortcuts display synchronization success/failure and remind the user that
building/deployment remain separate. The two archived `.disabled` direct-copy
scripts remain disabled and unchanged.

Existing deployment recovery
----------------------------

The PowerShell launcher no longer accepts deployment/version options. Existing
queued requests and immutable builds are unchanged. Use the explicit Python
`propagate_workflow.py resume --receipt <existing-deployment-receipt>` with the
original profile/stage-only mode to recover them; never submit a duplicate request.
Sync receipts cannot be used as deployment receipts. The explicit Python
`plan/apply/run` build/deployment tools retain their existing semantics.

When a later build is requested, collect all current repo-owned runtime files for
each affected package and preserve verified external dependencies. Assign the next
unused regular version/changelog once per batch. Do not combine only the latest
synced scope with an older selected build, which could omit other accepted edits.

Verification
------------

Regression checks cover sync with unavailable release/VDB metadata, no package
creation, unchanged files, missing inputs, independent changes, unknown divergence,
input drift, interrupted-copy recovery, player/event qualification and SFX source
guards. An isolated PowerShell runner verifies argument dispatch, item-text scope,
paths with spaces, failure exit codes and rejection of old deployment options.
Existing deployment/resume tests remain in the full workflow suite.

Verification on 2026-09-23: all 154 workflow tests passed, including the isolated
PowerShell launcher checks. `python tools/sovereign.py check` passed with 70 runtime
candidate files. The item-text alias now uses a separate variable, fixing the old
PowerShell ValidateSet rejection before Python dispatch.

All nine installed shortcuts were backed up and their replacement hashes verified.
The installation receipt is
`.sovereign/shortcuts/0bc71551efa640a88ca18c6680f5611a/receipt.json`.
No real editor assets were propagated, no mod version was changed, and no package
was prepared/deployed as part of this tooling update. Fixture checks do not establish
native/gameplay acceptance of future editor changes.

Audit follow-up, 2026-09-23: native-tool timeouts and malformed XML now record an
`interrupted` sync receipt with the error and exit through the normal CLI error path.
Regression coverage exercises both failures through the CLI and checks that no
handoff or VDB output is created. All 155 workflow tests and the 70-file repository
check passed. The release-parity document now states the sync-only policy and marks
the earlier automatic version/deployment policy as historical.
