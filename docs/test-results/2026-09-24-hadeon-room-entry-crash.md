# Hadeon room entry crash — 1.1.6

- Tester: author, reported 2026-09-24; first test since the lighting changes.
- Build: `0b06ea6dc4a496207c643774`, version 1.1.6.
- Finalization: `.vdb/finalizations/hadeon-candle-fix-1.1.6/receipt.json`.
- Save type: not supplied.
- Game executable version in dump: 2.7.1.0.
- Observation: game crashed on entering Hadeon's room. Later lighting stages and performance were not tested successfully.
- ER-092: Failed at room entry. ER-088 and ER-093 remain unverified.

## Diagnostic evidence

`eldenring.exe.24904.dmp`, recorded at 01:30:51 PDT, contains an access
violation (`0xc0000005`) reading address `0x18` at `eldenring.exe+0x20d35bb`.
The faulting stack belongs to `GXFFX::I::GXFfxUpdater` (identified by RTTI).
The caller obtains a null result from a bounds-checked configuration lookup,
then dereferences that result. Export-only Scaleform labels shown by the
debugger are distant nearest symbols, not evidence of a Scaleform UI fault.

The deployed candle flame FXR `7506110` contains a Basic node at
`root.0.0.0.0` with zero configurations and a state mapping selecting
configuration 0. Its generator removed the PointLight configuration while
retaining the node and its mapping. This is a concrete invalid reference
consistent with the faulting lookup. The mini dump lacks the relevant heap
data to recover the effect ID directly, so attribution remains a strongly
supported diagnosis pending a corrected in-game test.

The usual typed FXR reader masks this defect by constructing a default
configuration when reading an empty Basic node. Generic/raw inspection
preserves the actual zero count. All five brazier light presets and ten
candle light presets pass this specific raw reference check; that does not
establish their overall in-game correctness.

Extracted repo and live binder payloads for `7506110` match:
`3d002675b56f2c7dce8bd953fe264cb4f993c0b85608ff4996247240bb2a28ae`.

## Proposed repair and remaining acceptance

Remove the entire unused PointLight leaf from a fresh copy of source
`7505983`, retaining the flame sibling and its ancestors. A scratch candidate
removes exactly one leaf and has no invalid raw configuration references.
Validate this invariant on the packed output as well as loose sources.
Retest room entry, exit/re-entry, HP stages, victory, and crystal fade in game.

Diagnostics and the undeployed candidate are retained under
`.codex-temp/hadeon-crash-1.1.6/`. No runtime files, editor workspaces, release
version, or deployment were changed during this investigation.
