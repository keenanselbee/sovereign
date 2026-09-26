Deflection tutorial, version 1.0.7
=================================

The author approved replacing Guard Counters with Deflection using Guarding's
artwork, retaining the proximity trigger and adding a two-second delay. All other
vanilla tutorial popups/control hints are suppressed. Existing-save migration is
explicitly out of scope. This record contains static/native checks, not gameplay
observations. ER-063 and ER-064 remain Pending.

The native TutorialParam table has 86 rows, all equal to installed vanilla before
editing. Row 1180 changes imageId 18 to 16; every other row changes only
unlockEventFlagId to reserved OFF flag 1055420990. The native patch builder and an
independent comparison against the original verified all 86 intended cell changes,
row names/order, other table bytes, and binder/member metadata. Regulation changed
from `601719c2adca3a75278f52c3bcfda925463297757ef7a37446195d2d11d95009`
to `7efd280c912755aa68e8f33c8e36d0a17cbec892bafa29ba396393acbc507067`.

Event build `1790189195999686300` compiled all sources. Native decoded comparison
found only event 18002663 changed, from 12 to 32 instructions. Other events and
file metadata are unchanged. Runtime/source companion candidate SHA-256:
`a236728172d4e3d0a5157e32b6ce7712220c127fd334937e49339cd380703ba1`.
The original host-only proximity check, tutorial/item IDs, and item award behavior
remain. The delay checks death/departure; display waits out the phase transition
and is abandoned after defeat. The shown flag is set immediately before display.

Text candidate receipts:

- `1790189159522626400`: menu.msgbnd.dcx, two changed entries.
- `1790189168412540400`: menu_dlc01.msgbnd.dcx, two changed entries.
- `1790189177768162500`: menu_dlc02.msgbnd.dcx, two changed entries.
- `1790189186547913300`: item_dlc02.msgbnd.dcx, three changed entries for note 9106.

Each text candidate passed full decoded expected-result comparison through the
existing binary FMG patch route. No XML conversion or texture rebuild was used.
Exact candidate and baseline hashes were checked before atomic repo acceptance.
The version check passed for 1.0.7. Scoped repo/editor preflight found no differences
in catalogued destinations; the two older menu binders intentionally have no
configured editor destination.

The complete 86-row map and text are in [TUTORIAL-UPDATE](../TUTORIAL-UPDATE.md).
Scratch sources, backups, expected-value plans, native checks and acceptance hashes
remain in `.codex-temp/deflection-tutorial-20260923/`. Suppression through
unlockEventFlagId is supported by native definitions but still requires actual
game verification for scripted/menu-triggered tutorials and settings behavior.

Editor sync and deployment
--------------------------

The guarded editor handoffs completed without conflict overrides:

- Params: `.sovereign/handoffs/686c13aef94f49eda9698f384a8fa4b2/receipt.json`.
- Events: `.sovereign/handoffs/5a004199935042e1a8d1eeda6a50bfaf/receipt.json`,
  with event qualification `1790189374870233600`.
- Text: `.sovereign/handoffs/e6f595b26e8949859afb580396c01bc2/receipt.json`.

The five saved editor files match their repo counterparts exactly. Preparation
checks passed with 70 runtime files. Prepared package
`.vdb/prepared/7b132df7fecd4cfa9c0bdc4873758ab4/receipt.json` matches all 70 repo
runtime files and retains the staged external DLL. It changes exactly the six
tutorial runtime files against prepared 1.0.6; compared with selected 1.0.5 it also
retains the two HKS changes from 1.0.6. No other package differences were found.

All-profile completion is pending because Vortex is closed/stale. Build
`f64eb056847d29508b258479`, request `4f83e445-9287-4a6e-80a4-3b01bc82b81c`, is
bound to `.vdb/finalizations/1f1428fc530143858a628487e093f074/receipt.json`.
The live changed files still match selected 1.0.5, not this package. Resume the
existing request after Vortex processes its queue; do not submit another copy:

```powershell
python tools/propagate_workflow.py resume --receipt .sovereign/propagation/deflection-tutorial-1.0.7/receipt.json --wait-seconds 30
```

The existing finalizer verifies the acknowledged stage/profile results and selects
the exact packaging stage on completion. No Nexus publication or game test occurred.
