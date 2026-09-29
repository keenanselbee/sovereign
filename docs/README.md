Documentation index
===================

Read by task. Current guides own procedures and decisions; feature reports and
dated tests supply evidence. Historical status does not override current
manifests, saved editor files or deployment receipts.


Frequent tasks
--------------

| Task | Read | Action |
| --- | --- | --- |
| Locate assets/workspaces | [Layout](REPOSITORY-LAYOUT.md), [source ownership](../src/README.md) | Search `asset-catalog.json`; use `python tools/sovereign.py path-check` for configured paths |
| Compare saved files | [Workflow](WORKFLOW.md) | `python tools/sovereign.py status --scope <scope>`; add `--sources` when needed |
| Edit a game asset | Matching [editing-guide](EDITING-GUIDE.md) section | Resolve baseline conflicts, build a scratch candidate, inspect decoded changes |
| Sync verified repo edits | [Handoff commands](WORKFLOW-COMMANDS.md) | `accept-plan --scope <scope> --from repo`, review, then `accept --receipt <receipt>` through `tools/sovereign.py`; format qualification still applies |
| Propagate saved editor work | [Sync workflow](WORKFLOW.md) | `python tools/propagate_workflow.py sync --scope <scope> --from editor` |
| Build/deploy when requested | [Deployment guide](workflows/deployment-and-sync.md), [versions](VDB-RELEASE-PARITY.md) | Prepare complete packages, then `python tools/finish_workflow.py deploy --stage <prepared-receipt>` |
| Resume queued deployment | [Deployment guide](workflows/deployment-and-sync.md) | `python tools/finish_workflow.py resume --receipt <finalization-receipt>`; propagation receipts retain their original resume command |
| Change gameplay/balance | Relevant [mechanics](MECHANICS.md), [design](DESIGN.md), [balance](BALANCE.md) headings | Read the owning feature report, not every earlier update |
| Record observed gameplay | [Acceptance matrix](../TEST-MATRIX.md) | Update matching rows and add dated evidence under `test-results/` |
| Nexus copy/publication | [Nexus](NEXUS.md), [release automation](RELEASE-AUTOMATION.md) | Copy edits, remote saves, uploads and promotion retain separate authorization |
| Change automation | [Task rules](agent-workflows.md), relevant module | Run documented tooling checks and affected native qualifications |

Small artwork requests need the relevant source and format procedure. They do
not require release history, balance reviews or publication instructions.


Keep, query or archive
----------------------

- Current operating guides stay directly in `docs/`. [Agent task rules](agent-workflows.md)
  contain detailed instructions needed only for particular kinds of work.
- Design owns intended behavior; balance owns tuning decisions; mechanics owns
  implementation/evidence distinctions. Update the owner and link to it instead
  of copying release summaries across all three.
- Keep feature reports explaining native formats, exact rows/flags, shared users,
  qualifications or unresolved behavior. Read those reports when relevant.
- Keep `test-results/` as dated evidence; the acceptance matrix holds current
  status. An old failed test must not be rewritten as a later pass.
- [History](history/README.md) holds superseded plans and completed workflow
  rollouts. Tiny forwarding files preserve external and read-only historical links.
- Query research JSON/CSV instead of loading it as introductory prose. The jump
  inventory is a pre-edit snapshot; the [all-47 report](test-results/2026-09-26-jump-all47.md)
  records the applied change and its deployment receipt.
- `nexus-*.txt` is publishing input. Catalogs, manifests and immutable operational
  receipts retain their paths. Do not duplicate their values in narrative guides.

Age, size or placement in `.codex-temp` alone is not a deletion criterion. Keep
recovery/qualification records and evidence for unresolved work. Remove duplicate
narrative, reproducible scratch without remaining consumers and obsolete procedure
text only after its current rule has a clear owner.


Names and maintenance
---------------------

New narrative guides and feature folders use lowercase hyphenated names; dated
reports use `YYYY-MM-DD-topic.md`. Preserve standard root names such as README,
AGENTS and TEST-MATRIX. Existing uppercase guides can stay until a coordinated
rename is worthwhile: tools directly read WORKFLOW.md, WORKFLOW-COMMANDS.md and
MECHANICS.md, and the catalog cites other evidence paths.

Python keeps `snake_case.py`; installed PowerShell entry points retain their
verb-noun names. Game/archive member names, source companions and installed
shortcut targets are integration contracts, not cosmetic rename candidates.
Artwork variants should identify role/state and document extracted source IDs.

On document moves, update active links, rebase internal links and preserve access
from immutable historical references. Never rewrite old receipts to simulate new
paths. Docs-only cleanup needs link/whitespace validation, not a mod rebuild,
version bump or deployment.
