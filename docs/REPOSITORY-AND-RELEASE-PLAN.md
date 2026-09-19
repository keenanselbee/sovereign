# Sovereign repository and release plan

Refreshed 2026-09-10 after the full repository backup and the author's Hewg decisions.
This is an implementation plan, not a deployment receipt.
It replaces the earlier recommendation to adapt the legacy Grailwright extension:
use the shared **Vortex Development Bridge (VDB)** now used by Grailwright.
The initial refresh changed planning documents only. Subsequent implementation is
recorded in [the workflow checkpoint](WORKFLOW-PREP-CHECKPOINT.md); read that report
for current tool availability and completed handoffs/stages. No Nexus publication occurred.
The 2026-09-11 [VDB/versioning review](VDB-RELEASE-PARITY.md) selects the local 1.0.0
target and records the remaining artifact, promotion and collection-readiness work.

## Pre-cleanup restore point

Full snapshot:
`Z:/Backup/Elden Ring/sovereign/repo-before-workflow-refresh-20260910-201725/Sovereign`.
Its parent contains `copy.log`, `verification.json`, `sha256-manifest.jsonl` and the
read-only verification script. The receipt records the exact file count and byte total.
All source files were copied, including `.git`, uncommitted/untracked work, ignored
textures, local configuration, `archive/` and `.codex-temp/`. No repository reparse
points were found. Copied payloads were independently SHA-256 checked against the
unchanged source before this documentation refresh.

This is the complete repository before the refreshed plan, not a snapshot of external
editor workspaces, Vortex, the live game or saves. Back up each affected external file
again when a later handoff is prepared. Keep this snapshot immutable. To recover,
restore to a fresh directory and compare the manifest before selecting files to bring
back; do not mirror the snapshot over newer work. The refreshed planning documents
are intentionally later than this snapshot.

## Execution stages and current checkpoint

| Stage | Status | Deliverable and completion gate |
| --- | --- | --- |
| S0 - Preserve and record | Complete | Full repository copy and SHA-256 manifest; accepted design recorded in FEATURE-CORRECTNESS-PLAN |
| S1 - Resolve file ownership | Complete | Verified a0x accepted into repo/DSAnimStudio; Hadeon's three assets accepted into repo; independent rollback copies retained |
| S2 - Catalog and diagnostics | Complete | Shared catalog covers 72 runtime files and 1,118 owned sources/metadata; source copies match; optional editor destinations and overlays explicit |
| S3 - Qualify Vortex staging | Complete | Both packages switched and rolled back through VDB; 73 live files and unrelated enabled-mod state verified |
| S4 - Replace propagation | Complete | Nine shortcuts installed; scoped launcher and resume exercised through real deployment; independent source/build/shortcut recovery records |
| S5 - Tidy repository layout | Applied and verified | 519 files moved without byte changes; 671 player sources retained; installed map shortcut completed against the new layout |
| S6 - Standardize editing tools | Implemented and qualified | Event, BND/FMG, ESD and SFX candidates qualified; all six dialogue sources round-trip exactly and source/ESD/template handoff completed |
| S7 - Implement and test mechanics | Implemented; manual tests pending | Crusade, armor and Hewg built, editor copies synchronized, VDB test build deployed and file-verified; game acceptance remains in GAMEPLAY-CORRECTNESS-UPDATE and ER-030–ER-041 |
| S8 - Qualify release | Target 1.0.0 set; qualification pending | Main/texture ZIPs, serialized publishing, promotion/retry and collection readiness implemented locally; accurate descriptions, dependency provenance, clean installation, manual acceptance and first live release qualification remain |

S1 preserved the extra `a984_032400.hkx` in the accepted repo/DSAnimStudio a0x binder.
Its scoped handoff and independent rollback copies are recorded in the checkpoint.
Do not overwrite that accepted version with a historical authoring binder.

S2-S6 implement the detailed tooling sections below. Introduce only the adapters
needed by the current stage; a universal binary-editing framework is not required.
An individual mechanic's candidate can be prepared once its own editing route and
source handoff are qualified, but keep gameplay, layout and deployment changes
separately reviewable. Runtime directories now use `mod/`, `src/` and the separate texture root; the checkpoint
contains operation identities and recovery paths. Gameplay/release stages remain separate.

## Outcome and order

Make a normal edit reproducible from an agreed source through a verified candidate,
Vortex stage, game test and exact release archive. Keep the author's editor workflow
usable, preserve old builds, and make one scoped command sufficient for routine work.

Recommended order:

1. Establish current file ownership and a complete baseline inventory.
2. Qualify Sovereign's actual layouts with the existing VDB client and extension.
3. Add a reliable source handoff and replace legacy propagation internally.
4. Move shipped overrides into `mod/` with a hash-preserving path migration.
5. Promote proven format helpers into supported, repeatable tools.
6. Complete focused gameplay acceptance and remaining correctness decisions.
7. Reconcile player-facing copy, build exact release artifacts and qualify installation.

Gameplay testing can proceed alongside tooling using a recorded current build.
Folder cleanup is not a prerequisite for testing Hadeon, the crystal or combat.
Avoid combining a mechanics edit, a path migration and a deployment change in one handoff.

## Earlier review evidence and current follow-up

The later [file ownership review](FILE-OWNERSHIP-REVIEW.md) supplies fresh full-package,
regulation, archive and deployment evidence. Its decisions supersede the unresolved
ownership questions in the initial snapshot below. No acceptance/deployment occurred.

The counts and passing checks below are the earlier 2026-09-10 review snapshot;
they were not rerun as part of this backup/documentation refresh. Recompute them
in S1 before accepting files. The shared VDB manual matrix was reread for this
refresh: Grailwright results remain recorded, and Sovereign VDB-10 remains Pending.

| Area | Current evidence | Remaining work |
| --- | --- | --- |
| Core patch updates | Event/DLC02 text, older menu text, effects/icons, Torrent dialogue, TAE and player behavior/HKS updates have applied receipts | Preserve accepted results; perform their game tests, not another wholesale merge |
| Custom effects | 92 FXRs and 92 resource lists recovered; accepted common-effects binder synchronized | Verify visual triggers, timing and attachment in game |
| Shrine references | Hadeon and barrier references corrected | Confirm current map placement, blocking and cleanup |
| Shrine persistence/Nemesis | Testing resets removed; reward reconciliation and crystal-based hardcore implemented and statically checked | Reload/interruption, actual crystal destruction, follower transitions, NG+ and co-op tests |
| Repository preparation | `check` passes; 66 runtime candidates | Allowlist membership does not prove current-vanilla compatibility or package completeness |
| Scoped agreement | 41 mapped entries: 31 Match, 10 Review | Mapping does not cover every shipped asset or all editable sources |
| Main Vortex package | 70 files, 347,720,188 bytes; four reported repo differences | Resolve ownership and intended bytes before constructing a new stage |
| Workflow tests | 26 Python tests and two browser fixture tests pass | Fixture success is not a live Nexus save or Elden Ring deployment test |
| Nexus copy | Description structure check passes; shared Nexus Automation client is already integrated | Mechanics/content review, exact release identity and real remote verification |
| Release | `version` remains null, `releaseReady` false, bundled DLL unverified | Select version, verify dependency provenance and installation, complete acceptance |
| Gameplay | All 29 authored manual tests remain Pending | Record actual observations; do not infer passes from code or hashes |

The earlier checks used `tools/sovereign.py check`, `status --scope all --json`,
`tools/nexus_workflow.py package-plan`, the documented Python and browser fixture
tests, and `nexus-check --descriptions-only`. No game build, staging, deployment,
publication or full encrypted-game archive audit was run during this review.

Current difference inventory:

- `regulation.bin`: repo/live/Vortex agree; saved Smithbox differs. Earlier row-name
  findings are now confirmed across all members: zero differing gameplay cells,
  added/removed rows or row-order changes; 112,604 row-name differences in 91 tables.
- `chr/c0000_a0x.anibnd.dcx`: follow-up comparison found the live/Vortex binder has
  one extra motion, `a984_032400.hkx`; all 575 shared payloads and compared metadata
  match repo/editor. Preserve it through a scoped handoff; see the feature plan.
- Three `c2500` character/texture binders exist in the main Vortex package but not
  the repo/editor mapping. The follow-up confirms Sovereign ownership and Hadeon's
  custom model variant; accept all three as a coordinated group.
- `action/script/c8000.hks`, `chr/c8000.anibnd.dcx` and `chr/c8000.chrbnd.dcx` are
  live-only within the Sovereign mappings. The later ownership follow-up below
  identifies exact matching payloads in three separate staged Torrent mods.
- The older `menu.msgbnd.dcx` and `menu_dlc01.msgbnd.dcx` agree in repo/live/Vortex
  but have no saved Smithbox counterpart. Absence is not automatically an error.
- The separate `Sovereign - Textures` package is outside the main package inventory.
  Its three large icon archives are deliberately ignored by Git today.
- Current unstaged regulation/map/event changes and the added shrine navigation
  file must be preserved. Their presence is not authority to replace or clean them.

See [WORKFLOW](WORKFLOW.md), [MECHANICS](MECHANICS.md),
[NEMESIS-PERSISTENCE](NEMESIS-PERSISTENCE.md), [PLAYER-BEHAVIOR-UPDATE](PLAYER-BEHAVIOR-UPDATE.md),
[ANIMATION-UPDATE](ANIMATION-UPDATE.md), [SFX-RECOVERY](SFX-RECOVERY.md),
[NEXUS](NEXUS.md) and the [manual test matrix](../TEST-MATRIX.md).

## 1. Declare ownership and preserve the baseline

Ownership means identifying who edits a file, which accepted copy is retained, which
package ships it, and who deploys it. Those roles need not belong to the same folder.
The repo should hold accepted Sovereign sources and outputs; external editors remain
working copies. A saved editor file becomes authoritative only through explicit
acceptance, not because its timestamp is newer. The selected verified Vortex build
remains authoritative for the exact release ZIP. Live files are deployment results
and diagnostic evidence, not an automatic source for the next build.

Recommended responsibility map (target policy, not a completed migration):

| File group | Authoring responsibility | Accepted repository/package responsibility |
| --- | --- | --- |
| Regulation and row names | Smithbox for parameter edits; preserve editor-only row names | Accept reviewed gameplay fields into main; keep row-name metadata with sources, outside release payload |
| Event JS and compiled EMEVD | Script workspace or scoped AI source edit, built with DarkScript | Keep source/output together; main owns runtime events; common_func stays authoring-only |
| FMG and dialogue ESD | Qualified text/ESD routes using the current mod binder | Main owns accepted message/talk binders; preserve source/template and other members |
| Player HKS, behavior and name tables | Script/DSAnimStudio workspaces and qualified graph tooling | Main owns a coordinated group; no isolated old file may overwrite its companions |
| Main TAE and a0x motion binders | DSAnimStudio packed/loose/project state reconciled | Main owns both accepted runtime binders; preserve the extra ultimate motion |
| SFX | Existing SFX workspace and specialized Witchy recipe | Main owns packed effects; source FXRs, resources and packing metadata remain reproducible |
| Maps, parts and materials | Smithbox or the identified asset editor; direct binary inputs when no source exists | Main retains intentional overrides; record direct-binary provenance instead of inventing a rebuild recipe |
| Large icon archives | Identified texture authoring inputs; paired archives handled together | Separate Sovereign - Textures package; keep ignored payloads ignored through relocation |
| Loader DLL | External dependency with recorded source/version | Preserve current main-package mods/ layout until qualified; no speculative rebuild or relocation |
| Nexus descriptions | Existing _/nexus-page text files | Shared Nexus Automation publishes reviewed copy; packaging reads the selected Vortex build |
| Archives, scratch and journals | Historical snapshots, disposable work and operation receipts respectively | None ship; preserve archive originals and durable recovery journals through cleanup |

Ownership follow-up, 2026-09-10: rerunning scoped status still gives 41 entries,
31 Match and 10 Review. This is not a complete package or Vortex conflict audit.
The following separate staged packages exactly match the corresponding live files
by SHA-256:

| Live file | Matching staged package | SHA-256 |
| --- | --- | --- |
| action/script/c8000.hks | Fast Torrent | 3c7bdb30afba00611bb5ef045a92d637d0194aa3a7c7ecaaa6bc9f79e0633205 |
| chr/c8000.anibnd.dcx | Better Torrent Movements | c74c7e64e6918f169e2c063e281ada10718d623cf8287c69beedcfbc55230e63 |
| chr/c8000.chrbnd.dcx | Long-Horn Torrent | 7ffbe74c474c2d899c5bbbf40a259d7dcc320f541b0a32f6e21e2319324c4f3c |

The subsequent full review verified deployment-manifest ownership and physical
hardlinks for all three. Leave these files under their separate packages, outside
Sovereign's managed set. The selected profile and VDB transition still need their
own qualification; that does not reopen the observed file-ownership result.

Specific remaining dispositions:

- a0x: accept the verified extra-motion version into the repo and matching authoring
  inputs through its own backed-up handoff; do not overwrite the working stage first.
- Regulation: retain the named Smithbox authoring baseline and matching row-name
  metadata. Current runtime gameplay is equivalent; no gameplay merge is needed.
- c2500: accept all three current Sovereign-staged binders into the repo together.
  The custom model is used by Hadeon; its 33 material references are already present.
  Treat these packed files as the available source until original editing sources exist.
- Older menu binders: retain the accepted repo/stage copies and declare that a saved
  Smithbox counterpart is not required. Missing editor copies must not trigger replacement.
- Texture archives: keep separate package ownership. Their recorded layout is
  mod/menu/hi under the game root, and all three match repo/stage/live. Qualify the
  VDB handoff before moving paths; retain the ignored binaries in local recovery.

Add one machine-readable asset catalog, rather than further expanding globs and
hard-coded paths independently in each script. Keep public package identity in
`mod.json`, asset/build relationships in the catalog, and workstation paths in the
existing ignored local configuration. VDB configuration should be checked against
those identities so duplicated IDs cannot drift silently.

Each managed asset or coordinated group records:

- Stable asset ID, runtime path, owning package and authoring source/workspace.
- Build recipe, tool/version fingerprint, relevant game baseline and comparison route.
- Required companion files and editor handoff requirements.
- Which destinations actually apply; an editor-only source has no live destination.
- Qualification evidence and manual test IDs.

Keep the catalog small: one entry per asset or coordinated group, with explicit
exceptions and companion files. Reuse its mappings in status, acceptance and staging.
Report external-owned and no-editor-required files distinctly from conflicts; do not
keep presenting them as unexplained missing copies. Match only declared managed
files, and never infer deletion from another mod's presence or absence. Hash-addressed
inspection receipts can avoid repeating expensive decodes, but recheck source hashes
before accepting or deploying a candidate.

Inventory repo, selected editor roots, the two Sovereign stages and deployed files.
Keep missing, extra, byte-different and intentionally unowned files distinct. Use
Vortex ownership/conflict information before assigning live-only files to Sovereign.
For game compatibility, compare with verified installed archives and record the Steam
build; a directory labelled `1.17` or a file timestamp is insufficient provenance.

Produce a dated accepted inventory and a disposition for each difference above.
Preserve compact receipts in version-controlled docs where useful; keep full original
payloads in `Z:/Backup/Elden Ring/archive`; the former repo `archive/` remains entirely
ignored. Current handoff/layout recovery maps and copies live in `.sovereign/`. New operation identity
and recovery journals must survive scratch cleanup. Do not put their only copy in
`.codex-temp`.

**Exit:** every intended release file has an owner and selected source; unresolved
files are explicitly excluded from automatic acceptance, never silently deleted.

## 2. Consume VDB and qualify Elden Ring layouts

Shared checkout on this workstation:
`C:/Repositories/Tools/Modding/Vortex Development Bridge`.
Use its versioned bundled client selected through `dist/latest.json`, as Grailwright
does. Do not vendor the old `grailwright-nexus-metadata` extension or copy its queue.

The current VDB manual matrix records successful Grailwright staging, deployment,
same-version build retention and rollback (VDB-04/05/09). **VDB-10, Sovereign's
main/texture layout qualification, remains Pending.** The README's broader statement
that deployment/rollback are incomplete lags those recorded Grailwright observations;
neither document establishes Elden Ring acceptance.

Deliverables:

1. Tracked `vdb.json` for project `sovereign`, game `eldenring`, packages `main` and
   `textures`; ignored `vdb.local.json` for shared-tool location, and durable ignored
   `.vdb/` receipts. Use stage-only initially. The supplied Sovereign example is a
   starting template, not a qualified configuration.
2. A thin Sovereign client adapter with protocol/version checks, bounded waits and
   explicit handling of queued, completed, failed, interrupted and expired results.
3. Discover and record the actual installed Elden Ring mod type and deployment root
   for each package. VDB prepared directories are already-installed layouts; it does
   not infer installer transformations. Do not copy Grailwright's BepInEx mod type.
4. Resolve the main package's combined `mod/` and `mods/` layout. If one qualified
   type preserves both under the correct game root, keep that layout. If they require
   different deployment types, define separate deployment units and an explicit
   release assembly; do not duplicate or relocate the loader DLL speculatively.
5. Build a verified prepared snapshot from the agreed current Vortex package, stage
   it without activation, and compare every path/hash. Authoring exclusions remain
   explicit. Qualify main and textures separately.
6. In a selected test profile, verify activation, live paths, conflicts and restoration
   to the prior state. VDB only disables its own project/package siblings: legacy
   `Sovereign` folders will not automatically be replaced. Plan the one-time legacy
   enablement transition explicitly and retain those folders for recovery.

Keep distinct same-version development outputs by VDB build ID. Do not force a public
version bump for every edit. Local stages remain unpublished; real Nexus file IDs
are attached only after exact receipt-backed publication verification.

**Exit:** VDB-10 evidence identifies mod types, stage/build IDs, profile and verified
live paths. A failed or timed-out operation is investigated, not replayed blindly.
Coordinated deployment can partially fail; retain its recovery receipt.

## 3. Replace propagation with one controlled handoff

Extend `tools/sovereign.py`; keep familiar shortcuts as thin callers. External editor
folders remain supported working copies. An explicit import/handoff accepts saved
editor changes into the repo; an AI edit updates the corresponding editor source
when accepted. Neither side wins automatically.

Separate candidate building, accepting source/output, staging and deploying. Provide
one convenience workflow that composes the authorized steps, so normal use remains
simple while each result can be inspected or retried independently.

For acceptance: validate original hashes, lock the affected scope, preserve independent
backups, update the exact managed set, verify results and write a receipt. Handle
existing hardlinks deliberately during the legacy transition. Never truncate an old
VDB stage to update a new one. Preserve source plus compiled output together.

Replace the old scripts' directory purges, swallowed copy errors, success-after-failure
sounds, cwd dependence and delete-before-rebuild behavior. Once a package transitions
to VDB, its legacy shortcut must stop writing to the old stage/live paths. VDB becomes
the deployment owner for that package; the source handoff owns repo/editor copies.

Dependencies include:

- `c0000.behbnd.dcx`, `c0000.hks`, `eventnameid.txt` and `statenameid.txt` as a
  coordinated group, with the accepted animation binder checked for compatibility.
- Loose TAE sources, packed binder and current `.dsaproj` reconciliation. The earlier
  archival approval does not authorize discarding every subsequent editor project.
- SFX FXRs/resource lists/Witchy metadata and their packed output.
- The solo texture header/data pair; FMG binder metadata; current modified ESD template.

**Exit:** one scoped change reaches repo/editor/stage/live through recorded steps,
unrelated files stay unchanged, drift stops acceptance and rollback is demonstrated.

## 4. Move runtime files into mod/

Target structure (proposed, not created by this plan):

```text
Sovereign/
  mod/                    Main package's shipped game overrides
  src/                    Editable sources and required rebuild metadata
  packages/textures/      Separate texture package definition/owned assets
  tools/                  Sovereign commands and format helpers
  docs/                   Evidence, workflows, receipts and manual results
  _/nexus-page/           Existing authoritative publishing copy
  archive/                Ignored former archive location; current archive is on Z:
  .codex-temp/            Disposable extraction/build/cache output
  .vdb/                   Ignored durable staging identity and recovery records
  .nexus-automation/      Ignored durable publishing journals
  mod.json
  vdb.json
  AGENTS.md
```

Keep external native tools and large vanilla baselines outside tracked source. Do not
commit ignored texture binaries through a path move; choose their local asset location
and extend ignore rules first. Do not move the DLL into tracked `mods/` until ownership
and redistribution are resolved.

Migration procedure:

1. Build an explicit old-path/new-path map from the accepted catalog; classify
   `event/src`, `script/talk/modified`, `sfx/modified`, root `MapStudio`, `.smithbox`
   and `_` individually. Historical copies are not automatically active source.
2. Update runtime-root handling in status/build/check/package tooling and tests.
   Update path configuration, editor/shortcut targets, ignore rules and active docs
   together. Runtime paths remain relative to the game override root.
3. Move only the classified files. Keep original historical receipts unchanged and
   add relocation maps where needed. Do not mass-rewrite historical paths.
4. Compare pre/post file hashes and package entry paths, run workflow checks, and
   prove that a normal editor save/build no longer writes a second root-level copy.

**Exit:** all moved payload bytes and release-relative paths are preserved; no active
caller uses retired paths. Folder migration does not change gameplay or deploy files.

## 5. Turn qualified editing routes into supported commands

Promote the useful scratch helpers into small reviewed adapters. They must not depend
on a particular old run directory. Start with events and text, then dialogue and SFX;
retain qualified animation/graph routes but keep semantic changes narrowly scoped.

| Content | Build/inspection route | Required preservation check |
| --- | --- | --- |
| BND/DCX/BXF/TPF | WitchyBND with explicit effective settings | Member paths, IDs, ordering, metadata and untouched payloads; paired files together |
| EMEVD | Existing DarkScript builder and independent decoded reader | Instructions, arguments, bindings, layers, event order/rest behavior; common_func stays authoring-only |
| FMG text | Qualified binary SoulsFormats writer plus Witchy container | Null, empty, whitespace, literal `%null%`, Unicode, IDs and unedited entries remain distinct |
| ESD | ESDTool, explicit current mod binder template and correct basename/cwd | Intended groups only; other ESD members preserved; verify output actually exists |
| SFX | Qualified specialized Witchy recipe | Expected sorted category-ID shifts and every preserved FXR/resource-list payload |
| TAE | Qualified SoulsFormats TAE route plus specialized ANIBND packing | Animation/event identity, timings, bytes, groups and explained alignment differences |
| HKX/HKS | Qualified HKLib graph route, Witchy container and focused source edits | Separate ID namespaces, shared references, custom clips and coordinated name tables |
| Regulation/MSB | Smithbox plus qualified readers | Field/entity/reference diff; qualify a writer per intended operation before automated mutation |

Add tools to the existing path configuration, including WitchyBND, ESDTool and HKLib;
record installed library hashes/options. Tool or format changes invalidate affected
qualification. Build unchanged inputs first where the route is not currently qualified.
Generic Lua validation is not Havok runtime acceptance; ESD DSL is not executable Python.

Current equivalents are documented in WORKFLOW-COMMANDS: catalog doctor/status,
format unpack/build with decoded inspection reports, qualified accept/restore, VDB
stage/deploy/verify/rollback, and combined propagation run/resume. Existing public
commands remain compatible. `PLAN` continues to mean a read-only
propagation preview, not this long-term planning document or deployment authorization.

Use one run manifest linking input hashes, tool fingerprints, semantic differences,
accepted outputs, stage/build identity and tests. Summaries show differences and the
next required action; full decoded files remain local. Cache by content/tool/options,
and recheck source hashes before any mutation even when using cached inspection.

**Exit:** documented recipes can run from a fresh scratch workspace without the
original chat or one-off scripts, and tests cover drift, preservation, failure and recovery.

## 6. Gameplay acceptance and remaining decisions

The [feature correctness plan](FEATURE-CORRECTNESS-PLAN.md) records Crusade Insignia's
missing passive, the encounter-based Black Scaled Armor design, Obliterator attacks,
the missing a984_032400 motion, and unresolved Claw/Dragonbolt gameplay effects.
It now records the agreed three-base-game-beast Hewg forging route, the existing
story timing, fade/smithing transition, original voiced handoff and heard-dialogue
handling. Both Rykard phases qualify; already-defeated saves receive no retroactive
armor conversion. The feature plan records the agreed inventory policy, short post-memory-loss line
and once-per-journey reward with that journey's boss requirements.

Preserve the live/Vortex-only motion before any a0x handoff. Preserve the existing
unbuffed general attack and buffed beam; the fallback has static graph/TAE evidence
and needs a game test. Missing Claw/Dragonbolt effects do not authorize removing the
author's custom mechanics or restoring whole vanilla parameter rows.

The latest [Nemesis handoff](NEMESIS-PERSISTENCE.md) is the starting implementation.
Do not reapply the removed testing resets or gate ordinary passive Nemesis on crystal
destruction. Ordinary Nemesis remains active; breaking the crystal unlocks persistent
hardcore for the journey, suppressed while following Nemesis.

Priority test sessions:

1. **Shrine and crystal:** ER-004/005/008/009/010/011/012 and ER-029. Verify that the
   damaged crystal is entity 18002346, not just the overlapping entity-0 model. Check
   current Smithbox damageability and entrance placement, both barriers, interrupted
   reward recovery, no duplicate payout, repeat ritual and follower transitions.
2. **Progression:** ER-002/003/006/007. Existing saves, NG+, ordinary versus hardcore
   timing, already enhanced enemies and host/client ownership. No existing-save
   migration was implemented; determine whether supported saves need one.
3. **Combat:** ER-013 through ER-018, ER-024 through ER-029. Verify special attacks,
   ultimate readiness/inputs/FP/cooldown, custom deflection, new skills, saved editor
   reload, recovered effects and black armor variants.
4. **Torrent:** ER-020 through ER-023. Unlock, owned variants, selection persistence,
   cleanup and unchanged custom Grace branches.
5. **Release installation:** ER-001/019 using the exact candidate package(s), selected
   dependency versions and intended launcher, not an accumulated development folder.

Specific unresolved work requiring findings or author decisions:

- Confirm production eclipse/blessing timing: inspected waits still include testing-scale
  intervals. Do not promise the older description's timing or rebalance without a decision.
- Interpret the ritual's final death condition and interruption experience in game.
- Implement the agreed Hewg acquisition for row 23085000 after qualifying its ESD,
  reward and fade sequence. Reinspect the selected current regulation and allocate
  collision-free lot/claim IDs. Late claim uses only the masterpiece handoff line;
  the reward is once per journey with that journey's four boss victories required again.
- Investigate one-handed behavior reference 300000867, previously resolving to -1,
  and seven custom clip names documented in PLAYER-BEHAVIOR-UPDATE. Do not remove or
  fabricate replacements before determining which paths use them.
- Resolve a0x and staged/live-only asset ownership, then test that selected result.
- Determine supported co-op and existing-save behavior from observed results.

The agent can prepare decoded comparisons, narrow builds, dependency tracing and test
instructions with high confidence on qualified routes. The author supplies placement,
visual feel, balance decisions and actual play observations. Build success cannot
close those gates. Record a package/build fingerprint with every result; later relevant
changes invalidate affected tests, not necessarily the entire matrix.

## 7. Nexus and release completion

Continue using shared Nexus Automation; do not introduce a second publishing backend
just because VDB also contains publishing code. Sovereign owns release policy/copy,
Nexus Automation owns the existing remote workflow, and VDB owns stage identity and
receipt-backed metadata promotion.

Keep the author's existing rule: **the verified selected Vortex stage supplies the
upload payload**. Extend packaging to resolve a completed build ID rather than always
reading the mutable legacy `Vortex/Sovereign` path. Verify its current contents against
the receipt and compare the resulting ZIP entry-for-entry. A prepared build snapshot
and the final ZIP must have the same intended payload; no circular dependency on a
pre-existing release ZIP is required to stage from a directory.

Keep main and textures separately identified. Determine each release file/group and
required-versus-optional installation relationship before publishing textures; do not
reuse the main group ID for a different package automatically. Verify the bundled DLL's
source/version/redistribution and test the final install without unrelated development mods.

Review full description, README and changelog against current mechanics and results.
Keep short/file pitches stable unless the mod's identity changes. Explain ordinary
Nemesis, optional crystal hardcore, follower protection, Crucible Lord/shrine progression,
Obliterator acquisition and ultimate requirements only to the level supported by evidence.
Remove unsupported promises; do not equate BBCode validity with accuracy.

Release gate: selected version, recorded game build, resolved package differences,
dependency approval, required manual tests passed or an explicit reduced release scope,
verified installation and exact stage/ZIP receipts. Preserve immutable upload IDs and
journals, reconcile partial publication before retrying, and promote only the exact
published build. Keep publication separate from local build/stage operations.

## Documentation and implementation boundaries

Shorten AGENTS into durable operating rules and a format/task routing index. Move
historical qualification counts and detailed recipes into focused docs without losing
their warnings or evidence. Link this plan from WORKFLOW. Keep old verification reports
labelled as snapshots: the original eight-test/19-scenario report is not current status.
Correct stale archive guidance to reflect that the entire archive is ignored.

Implement as independently reviewable changes: catalog/diagnostics; VDB consumer and
layout qualification; controlled handoff; runtime-root migration; format adapters;
individual gameplay fixes; release copy. Do not sweep existing unrelated edits into
these changes. No commits or external mutations are authorized merely by this plan.

The first implementation batch delivered the ownership catalog, concise complete
status, and a stage-only VDB adapter. Byte-identical Sovereign stages qualified before
activation, legacy shortcut replacement and runtime directory migration. S1-S6 are
complete; see the checkpoint for actual receipts and the remaining S7/S8 work.
