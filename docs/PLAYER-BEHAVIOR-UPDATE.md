# Player behavior and HKS compatibility update

Applied against the archive-derived installed Steam build **25080141**. This update
combines current vanilla player behavior with Sovereign's custom graph and HKS.
It is a verified file integration; in-game acceptance remains Pending.

## Files and authoring ownership

The coordinated runtime set is:

- `chr/c0000.behbnd.dcx`
- `action/script/c0000.hks`
- `action/eventnameid.txt`
- `action/statenameid.txt`

All four match across repo, main Vortex and live mod folder. The packed behavior
and HKS also match their DSAnimStudio and Script authoring copies. The previously
absent `DSAnimStudio/c0000-behbnd-dcx` folder now contains the matching three HKX
members, Witchy binder metadata and editable `Behaviors/c0000.xml`.

The handoff verified 19 paths through 15 physical writes and preserved all four
Vortex/live hardlink pairs. Reload open HKS/behavior editor buffers before saving.
The existing propagation scripts copy packed output; they do not compile behavior
XML or coordinate the two name-ID files. Maintain those mappings together with the
graph whenever events/states are added. Their authoring source is the repo's
`action/` files; no separate existing editor-owned name-ID files were found.

The author's completed [animation update](ANIMATION-UPDATE.md) was adopted without
rewriting it. Its accepted SHA-256 remains
`a36f192c3a0918e7bbf70507c0b5dbd685bde842a22daf1b03749df75e2c6de0` at all four
locations. Earlier TAE candidates in this player-update scratch run are superseded.

## Behavior merge

Current vanilla was the base. Named nodes were matched by unique class/name, not
generated `objectN` IDs. Unchanged anonymous references were matched while preserving
sharing; modified anonymous objects were transferred with rewritten pointers.

- Retained all 69 new vanilla named nodes, 32 vanilla-only existing-node changes,
  and the new heavy-cancel branch in `SwordArtsStance_SM`.
- Retained 336 custom named nodes: 276 clips, 30 selectors and 30 states; also retained
  Sovereign's 319 custom-only existing-node changes, including `Attack_SM`.
- Combined the 28 selectors edited on both sides. Both sides only added entries;
  existing order is retained, with the vanilla additions followed by Sovereign's
  appended additions. No old selector entry was replaced or removed.
- Retained the current animation table and appended the mod-only names. Nearly
  24,000 apparent vanilla clip differences were index renumbering, not separate edits.
- Removed one anonymous object made unreachable by the replaced transition pointer.
  The rebuilt graph has 36,868 objects and 31,368 named/singleton anchors.

### ID handling

Graph event slot 1465 belongs to `W_DrawStanceRightAttackHeavyCancel` in current
vanilla. Sovereign's 30 added events now occupy 1466-1495; their graph references
were updated consistently. The external name-ID namespace is separate:

- `eventnameid.txt`: vanilla heavy-cancel remains 2759; custom IDs move to 2760-2789.
- `statenameid.txt`: vanilla heavy-cancel remains 2294; custom IDs move to 2295-2324.

The graph has 1,496 event names. Sovereign's ten existing trailing zero event-metadata
records were retained, giving 1,506 metadata records; no recognized event reference
uses those trailing unnamed records. They were not silently trimmed.

Custom clip IDs are not assumed to index the animation-name table. The inspected
[ERClipGeneratorTool allocation code](https://github.com/The12thAvenger/ERClipGeneratorTool/blob/8f4ada3a10ce7ea75d0379c058193a1b1699b1c5/ERClipGeneratorTool/ViewModels/BehaviorGraphViewModel.cs)
allocates above the maximum existing clip ID without extending that table. This
explains the original mod's table mismatches. The merge preserves that convention:
226 generated custom IDs move from 14856-15081 to 14889-15114, while the separate
50-ID range 20000-20049 is preserved. No ID aliases two different animation names.

## HKS changes

The existing curated Sovereign source was edited narrowly. Thirteen functions
received current vanilla additions and one callback was added:
`DrawStanceRightAttackHeavyCancel_onUpdate`. The other 1,386 existing functions
remain text-identical. Changes include skills 372/373, FP handling for 96/99,
stance cancellation/re-entry, effect 4070's fall guard, equipment-change restrictions
and the updated throw eligibility. Existing custom input, movement, deflect,
Obliterator and ultimate logic was preserved around those additions.

The independently extracted current `common_define.hks` also changes
`SwordArtPutOppositeWeapon[373]` from `{FALSE, FALSE, TRUE}` to
`{TRUE, FALSE, TRUE}`. Sovereign embeds that table, so its row was updated too.
The other upstream shared-script change removes a debug call from a function that
Sovereign does not override; the game supplies that function. No common_define
runtime override was introduced.

## Verification and limits

- HKLib.CLI v0.1.2 preserved every parsed XML value through unchanged conversions of
  historical, current and mod graphs. The mod HKX rebuilt byte for byte; vanilla
  HKX encodings differed while their complete decoded trees matched.
- The candidate was compiled and decoded again. Independent structural comparison
  verified the exact planned union, all current/custom nodes and approved remaps.
- Unchanged WitchyBND basic BND repacking preserved all member payloads and metadata.
  The final binder contains the verified candidate HKX and the two unchanged members,
  with header fields, names, IDs, flags and compression metadata preserved.
- All graph event names resolve in the external mapping, recognized event references
  and variable bindings are in range, and per-machine state IDs are unique.
- All 33 distinct new vanilla animation names resolve in the adopted TAE binder.
- The new HKS callback matches current vanilla tokens after resolving named constants.
  Every documented edit to an existing function reverses exactly to its old source.
  This is static validation, not a Havok Script runtime compilation or game test.
- Repository preparation checks pass. Scoped status confirms c0000 HKS, behavior
  and animation agreement; unrelated location-specific overrides remain separate.

Seven existing custom clip names lack entries in the main TAE binder:
`a978_030300`, `a978_030600`, `a978_032300`, `a978_032400`, `a978_032600`,
`a981_030300`, `a981_032300`. They were already present before this merge and remain
unchanged. Their intended use/fallback needs gameplay investigation; do not describe
them as verified working attacks. The separate a0x repo/live discrepancy was also
preserved. Status additionally lists location-specific c2500/c8000 overrides; they
were not copied, removed or qualified by this update.

Run ER-014/015/016 and ER-025/026, plus the dedicated ER-027/028 checks in
[TEST-MATRIX.md](../TEST-MATRIX.md). Confirm new skills, heavy-cancel input/release
windows, insufficient FP, one/two-handed transitions, equipment restrictions and
Sovereign deflect/ultimate behavior in game. No release-readiness claim is implied.

## Evidence, backups and repeatability

The durable receipt is `docs/patch-updates/steam-25080141-player-behavior.json`.
The adjacent graph plan and HKS diff record the applied edits. Detailed inputs,
qualification, candidates and independent verifiers remain in
`.codex-temp/player-update/1789017055699019100/`; the investigation scripts are in
`.codex-temp/behavior-xml-review/`. Recheck source/tool hashes before reuse.

Original replaced files and comparison baselines are archived under
`archive/game-updates/2026-09-09_to-steam-25080141/05-player-behavior-and-hks/`.
Its SHA-256 manifest and `restore-map.json` identify the relocated originals, all
19 destinations and the five newly added authoring files. The original handoff
journal retains historical scratch paths. Do not rerun it or restore one member
of the coordinated graph/HKS/name-ID set in isolation. Check subsequent edits and
open buffers before any rollback. The separate accepted animation update is retained.
