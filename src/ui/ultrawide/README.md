Ultrawide current-game compatibility
===================================

Local compatibility rebuild of the installed 21.5x9 Ultrawide UI Fixes 2.0.2
package, not an upstream release. Only the class selector and world-map GFX
change. The other 48 files retain their original bytes.

`build-compatibility-patch.py` requires FFDec 26.3, the pinned current native
GFX files stored with `.swf` extensions, the original Ultrawide `mod` root, an
existing scratch directory and a new output directory. Run `--help` for arguments.
It transfers reviewed placement matrices onto current game definitions and
checks full decoded roundtrip before writing an isolated package. Input hashes
prevent silently applying it to a different game/mod baseline.

The manual-install ZIP is retained in
`.vdb/releases/ultrawide-21.5x9-current-ui-local-compatibility/`. Install it as
a replacement for the old Ultrawide package, retaining its game-root `mod/menu`
structure. Keep Sovereign after it and winning caption/startup-logo conflicts.
Do not put these two GFX overrides in the Sovereign runtime package.

Current portrait definitions and map sprite 171's 348 frames are retained.
Source/output, ZIP inventory and payload hashes have been checked; visual
acceptance in game remains pending.
