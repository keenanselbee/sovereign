# Workflow preparation verification

Run on 2026-09-09. Machine-readable hashes and differences are recorded in
[workflow-qualification.json](workflow-qualification.json). This is a snapshot,
not a promise that external folders remain unchanged.

| Check | Observed result |
|---|---|
| Python workflow tests | 8 passed: containment, drift/extra-file detection, matching copies, archive contents/receipts, overwrite prevention, authoring exclusions, source-change rejection, event bindings/order/metadata, Nexus checks |
| Repository preparation check | Passed; 66 files matched the runtime candidate allowlist |
| DarkScript build | All 10 source files compiled in scratch |
| Shipped EMEVD comparison | All 9 shipped files matched decoded data after compilation |
| common_func comparison | No baseline; compiled but round trip remains unqualified; not a shipped runtime candidate |
| Actual draft ZIP | 66 runtime files plus draft marker; entry set, CRC, content SHA-256 and source hashes verified |
| Scoped file agreement | 41 files inspected across configured repo/editor/live/Vortex locations; 11 require review |
| Event source and output agreement | 10 JS files and 9 runtime event files matched across the four locations |
| Local Nexus check | Expected open items: empty short/file descriptions, unselected version, missing Nexus URL/group metadata |
| Loader logs | Existing logs resolve the Game/mod folder and show Scripts-Data-Exposer-FS.dll loading; no game session launched by this prep |
| Manual gameplay acceptance | 0 Passed; all 19 scenarios Pending |

The draft ZIP version `0.0.0-prep` is a test label. Its SHA-256 is
`70126e5fd2f1ba080d39f5686851151df1128d957c0067067ff44114c9dedc13`.
It is not a release package and does not include the unresolved external DLL.

Review items include the editor regulation byte difference, menu binders absent
from the inspected editor location, `c0000_a0x.anibnd.dcx` differing from live/Vortex,
and destination-only c2500/c8000 resources. Do not automatically remove those extra
files: establish why they are present and whether another mod owns them. The earlier
parameter comparison found the inspected editor regulation changes were row names
only; rerun a semantic comparison if either regulation changes again.

Detailed local evidence remains in these ignored directories:

- `.codex-temp/event-builds/1788996617773408100`: inputs, outputs, decoded before/after
  data, compiler log and receipt.
- `.codex-temp/packages/1788996668208148800`: verified draft ZIP and receipt.
- `.codex-temp/sovereign-inspect`: earlier mechanics/workflow inspection exports.

No gameplay source or runtime file was changed by the preparation commands. Existing
user changes to regulation and shrine map remain. No editor handoff, live/Vortex
propagation, external project correction or Nexus publication was performed.
