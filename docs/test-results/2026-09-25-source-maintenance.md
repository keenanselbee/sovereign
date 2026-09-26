Source-maintenance verification, 2026-09-25
==========================================

The existing catalog and reviewed handoff now track recovered source freshness.
Group editing metadata identifies the authoritative input. Changed packed inputs
can refresh declared loose members and their manifest through ordinary handoff
backups and restoration. Independent loose edits must match the selected packed
member before acceptance. Repository package preparation and new ZIP creation
reject stale recorded sources.

Verification
------------

- `python -m unittest discover -s tools/tests`: 181 tests passed. Coverage includes
  conflicting source edits, matching rebuilt payloads, changed inputs after
  planning, manifest drift, package freshness, partial publication and restoration.
- `python tools/sovereign.py check`: passed against the current repository.
- `python tools/inventory_archived_baselines.py --check`: matched the saved
  [inventory](../baselines/archived-game-files.json).
- The native `tracked-members` reader built and exported real English FMG,
  player motion, nested TPF/DDS, historical DFLT parts and direct GFX samples.
  Candidate hashes and unchanged metadata matched the recorded extraction.
  Missing tracked members and changed complete member sets failed before output.
  Local fixture: `.codex-temp/tracked-reader-check.py`.
- An isolated Python handoff fixture used the real native reader to plan, accept
  and restore a GFX source and its manifest. No live runtime/editor asset was
  changed by that test.
- `python tools/sovereign.py build-events --require-equivalent`: passed after the
  shared native reader change. All nine runtime candidates matched their accepted
  baselines; `common_func` remains authoring-only. Local receipt:
  `.codex-temp/event-builds/1790401561466122700/receipt.json`.
- Both already queued 1.3.3 prepared payloads still pass `load_prepared` validation.
  Source-only catalog metadata does not strand an existing linked finish request;
  changed runtime membership, settings or payload still fails validation. No new
  request was submitted and this check does not establish deployment completion.

Coverage limits
---------------

Only explicitly recorded members refresh. Newly customized members need reviewed
extraction and manifest inclusion. Extraction does not qualify a rebuild or prove
gameplay correctness. Existing format qualifications still apply. See
[the workflow commands](../WORKFLOW-COMMANDS.md) and [source ownership](../../src/README.md).

The archived folders labelled 1.16 and 1.17 each contain 47 of the 75 catalogued
paths. Both lack `regulation.bin` and 27 parts paths. Their precise game builds and
clean vanilla provenance remain unverified; the inventory records that uncertainty
and supports later comparisons rather than automatic merging. See
[the baseline inventory](../BASELINE-INVENTORY.md).

This maintenance work changed tooling, catalog metadata and documentation. It did
not change gameplay assets, deploy, commit or publish a release.
