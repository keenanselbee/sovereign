Opening follow-up 1.3.3
======================

Implemented scope
-----------------

- Expand the existing catalog/status/check system: durable guarded text patches,
  explicit recipe-to-output ownership and repo comparisons to saved editors and
  the selected build. No separate source database or automatic rebuild framework.
- Nemesis aid: three-second continuous eligible entry delay; existing ten-second,
  twenty-tier ramp reaches +100% HP/FP/stamina maxima and outgoing damage. Guard
  stamina multiplier ends at 0.5. The HKS factor matches the native rows; resource
  spending, proportional adjustments, withdrawal and death protection remain.
- All twelve hallway groups use a cancelable one-second exit delay. First-group
  entry remains 1.5 seconds; victory/crystal overrides remain authoritative.
- Hadeon returns visibly to new region 18002380, sharing original region
  18002366's position with yaw increased 180 degrees. Initial facing remains.
  Parked AI stays disabled until valid living reentry. The six-second confirmed
  death retreat remains cancelable. No damage-triggered teleport or new scripted
  NPC heal was added; engine reset/full-health behavior still needs live testing.
- Approved spirit/tutorial wording, 2.5-second Soldier Ultimate lesson, and
  Deflection sparks artwork. Image sources retain separate scene, reusable blank
  gold panel and game icon 20297; no charge diamonds or concept label.

Verification
------------

The full Python suite passed 165 tests. Four focused event suites passed 16 tests,
including all twelve hallway groups, aid admission, retreat, rescue, milestones
and tutorial interruption. These simulations do not establish engine behavior.

The native regulation recipe changes exactly 280 cells across twenty aid rows,
preserving all other decoded fields, tables and binder/member metadata. Native
map readback confirms exactly one new region; removing it reproduces the original
decoded map. Evidence: `.codex-temp/opening-followup-20260925/native-candidate/`
and `accepted-native.json` in its parent.

The original 3,079-member texture pair round-tripped byte-identically. The edited
pair changes only `00_Solo/MENU_Tuto_00016.tpf.dcx`; every other payload and all
member metadata match. TPF metadata and the 148-byte DDS header are unchanged.
The 544x336 BC7 image was decoded and visually inspected. Rebuilding from the
accepted pair gives identical bytes. See the durable
[texture recipe](../../src/textures/deflection-tutorial/README.md).

[Text verification](2026-09-25-opening-dialogue-tutorial.md) records the thirteen
FMG edits. Game appearance, controller glyphs, full native aid behavior and NPC
retry state remain Pending in [TEST-MATRIX](../../TEST-MATRIX.md).

Event compilation and editor sync
--------------------------------

The first DarkScript invocation timed out without output. Recompiling the exact
inputs independently succeeded in 5.8 seconds; the canonical build then passed
with the same binary hash. Receipt:
`.codex-temp/event-builds/1790395883850029400/receipt.json`.
Decoded changes are limited to events 5750302/5750303, 5750320 through 5750331 and
5750403; event order/count and metadata are unchanged. All other shipped event
binaries remain equivalent. The reviewed shrine candidate was accepted to both
repository source and runtime binaries.

Qualified guarded editor sync completed, with saved destination hashes rechecked:

| Scope | Receipt under `.sovereign/handoffs/` |
|---|---|
| Parameters | `a5423701a7e543cbba1753dc8d86afef/receipt.json` |
| Maps | `92f84b2fd5bc4b04afd59fdc4ae05cf0/receipt.json` |
| Text | `3c355f32f9e14d17808eec640452f46d/receipt.json` |
| Events and source | `83942d856fdc448b84a4633a27fc7164/receipt.json` |
| Coordinated player/HKS | `e7b04b9a45e644a089a03fc8a2183bbe/receipt.json` |

The player qualification rebuilt 665 animation and three behavior members with
identical packed bytes and verified the behavior graph roundtrip. Open editor
buffers should reload these saved files before subsequent edits.

Deployment queued
-----------------

Both complete packages were prepared from all repository-owned runtime files,
preserving the selected external dependency. Main has 73 files, eight changed;
textures has three files, two changed. Exact changed-path inventories and source
hashes were verified before submission. No intermediate payload was staged.

One protocol-3 all-profile finalization request is pending because the Vortex
bridge snapshot is unavailable/stale. Receipt:
`.vdb/finalizations/opening-followup-1.3.3/receipt.json`.
Request ID: `e87c271d-cee3-4b56-8e69-2d4a97cbcc0c`.
Main build: `e5cf93386f3b2b90382324a9`; textures build:
`0a3e6b8554788f2cf6236ff5`. Both versions are 1.3.3.

The bridge will preserve disabled/absent package states and wait for safe active
profile deployment. Vortex was not launched to drain the queue. Live 1.3.3 bytes
are not yet verified, and the previous packaging selection remains until the
finalization completes. Resume this receipt, never submit a duplicate request.
`releaseReady` remains false; this is not Nexus publication.
