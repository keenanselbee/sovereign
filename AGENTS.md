AGENTS.md
=========

These instructions apply to Sovereign, the Elden Ring mod.

Read `C:\Repositories\System\AGENTS.md` for shared working rules and its
`docs/style-guide.md` before edits. If unavailable, report that and use available
project guidance. Project-specific rules take precedence.


Task routing
------------

Use [the documentation index](docs/README.md) when the relevant guide is unknown.
Before nontrivial work, read applicable sections of [WORKFLOW](docs/WORKFLOW.md).
Search headings in long guides and read the relevant sections. Follow reports
when they supply needed evidence or format procedures; do not load every report,
research JSON/CSV or historical plan by default.

| Task | Required guidance |
| --- | --- |
| Gameplay edits or mechanic claims | Relevant [MECHANICS](docs/MECHANICS.md), [DESIGN](docs/DESIGN.md), [BALANCE](docs/BALANCE.md) sections and feature report |
| Runtime/format edits or editor sync | [Asset rules](docs/agent-workflows.md#asset-editing-and-editor-sync), matching [EDITING-GUIDE](docs/EDITING-GUIDE.md) section and linked format procedure |
| Build, deployment, packaging or versioning | [Deployment rules](docs/agent-workflows.md#builds-deployment-and-versions), relevant [commands](docs/WORKFLOW-COMMANDS.md), shared software-versioning policy |
| Nexus audit, copy or publication | [Nexus rules](docs/agent-workflows.md#nexus-and-publication), relevant [NEXUS](docs/NEXUS.md) and [release automation](docs/RELEASE-AUTOMATION.md) sections; mechanics evidence for claims |
| Verification or release preparation | Relevant [TEST-MATRIX](TEST-MATRIX.md) rows; [tooling verification](docs/agent-workflows.md#workflow-tooling-verification) when changing tools |
| STATUS, PLAN, BUILD, LOGS or TEST | [Command meanings](docs/agent-workflows.md#local-command-meanings) |
| Layout, source ownership or workstation paths | [REPOSITORY-LAYOUT](docs/REPOSITORY-LAYOUT.md), [source ownership](src/README.md), `asset-catalog.json` |

Linked rules are mandatory for their scope. History is evidence, not current
operating policy, and does not authorize actions.


Always applicable
-----------------

- Runtime lives in `mod/`, sources in `src/`, separate textures in
  `packages/textures/mod/`, artwork in `images/`. Do not recreate the old `_` tree
  or root game folders. `asset-catalog.json` owns source/runtime mappings.
- Keep author intent, implementation, historical claims and gameplay results
  distinct. Divinity preserving buffs while undamaged is intentional; Obliterator
  should earn ultimate charge. Record author clarifications in the owning guide.
- Resolve scoped repo/editor differences by content before runtime edits. Preserve
  unrelated changes and open-editor work; never choose a baseline by timestamp.
  Verified runtime edits include standing-authorized, guarded sync to configured
  Smithbox, Script, DSAnimStudio and SFX workspaces. Follow asset rules for
  qualification, coordinated files and recovery. Report blocked sync.
- Propagation is sync-only. Builds/deployment, Nexus publication, commits and
  external installation require their applicable authorization. Requested
  deployment collects complete affected repo-owned packages, preserves verified
  external dependencies and uses protocol-3 finalization. If Vortex is closed,
  queue without launching it. Preserve disabled/absent package states; distinguish
  queued from completed deployment.
- `mod.json` owns the target version. Changed staged payloads require a new unused
  regular version and changelog; docs-only changes do not. Keep `releaseReady`
  false until acceptance. Never overwrite immutable stages or reuse their versions
  for changed contents.
- Preserve `.sovereign/`, `.vdb/`, `.nexus-automation/`, editor-sync baselines,
  recovery records, selected-stage pointers, version reservations and release/
  upload journals. Inspect and resume existing requests; never blindly resubmit.
  Preserve scratch evidence still needed by unresolved work or qualifications.
- Use supported commands and scoped checks. Never run archived propagation
  scripts, ESD DSL as Python or generic Lua checks as proof of HKS compatibility.
  Keep native dependencies external; verify rebuilt formats before acceptance.
- Docs-only edits require link and whitespace checks. Keep runtime names,
  installed entry points and tool-consumed paths stable. New narrative guides and
  history use lowercase hyphenated names; standard root files retain their names.
  Do not edit `reference/` during cleanup.
