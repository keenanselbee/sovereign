# Animation compatibility update

Applied 2026-09-09 against the current archive-derived Steam build 25080141.
Sovereign's `chr/c0000.anibnd.dcx` now includes the reviewed upstream TAE updates.
Behavior graphs and HKS were not edited. In-game acceptance remains Pending.

## Scope and preservation

- Added `a269.tae` (15 records), `a972.tae` (12) and `a973.tae` (6): 33 records.
- Updated 32 existing records that still matched the historical vanilla baseline.
- Merged eight overlapping records at event level: a00/101104; a415/45000,
  45100 and 48000; and a692/a693/a696/a699, each animation 40040.
- Preserved all 15,265 other existing animation records and all 14 mod-only TAE
  files. Six pre-existing empty vanilla TAE omissions remain unchanged; restoring
  those was not part of this update.
- The binder contains 665 members: three added, seven modified and 655 with
  byte-identical payloads. Existing IDs, paths, flags, compression metadata and
  relative ordering are preserved, as are the binder header fields.

The eight overlaps contained event ordering differences and, in four records,
trailing zero extensions. No custom timing or defined parameter value changes
were found against the old baseline. The merge preserves Sovereign event order
and parameter bytes while applying 16 upstream event timing edits and inserting
one sound event. The unchanged parameterless Blend event at index 0 of a00/101104
acquires eight alignment zero bytes when that animation is rebuilt; this is the
only decoded payload exception to the explicit expected result.

The a00 event-66 parameter block retains Sovereign's 16 bytes, including effect ID
19997. Current vanilla uses eight bytes, with the omitted trailing bytes all zero
and outside the installed template's eight-byte definition. This serialization
difference was deliberately retained rather than treated as a gameplay change.

## Qualification and checks

An unchanged specialized WitchyBND ANIBND rebuild preserved all 662 original
member payloads and their metadata. Six of the seven existing TAE files rebuilt
byte for byte through the installed Smithbox SoulsFormats library. The seventh,
`a00.tae`, preserved all decoded metadata and animation/event data but became
544 bytes smaller. Inspection localized the size change to 34 empty-animation-name
blocks, each reduced by 16 bytes, with corresponding offset relocation. The
writer's empty-name handling explains this layout normalization; it is not a
claim of byte-identical a00 serialization.

Every candidate TAE was compared with an explicit expected result, including
record order, mini-headers, names, event groups, timing and parameter bytes.
The packed candidate was reopened independently and checked against the same plan.
All 33 new records reference 25 distinct motion clips present in the installed
current game archives (`c0000_a9x` and `c0000_dlc02`). No mod override of those
motion binders was present at verification. This proves reference availability,
not correct gameplay execution.

## Authoring handoff and rollback

The accepted candidate updated the ten affected loose TAE paths in the working
DSAnimStudio folder and the packed binder in DSAnimStudio, repo, main Vortex and
live game: 14 verified paths, 13 physical writes. The existing Vortex/live hardlink
was retained. All 656 other authoring files, including Witchy metadata, remained
unchanged. The propagation VBS only copies the packed file; it does not rebuild
the loose folder.

The author selected archiving the old `c0000.anibnd.dcx.dsaproj`. That saved project
contains timeline data and takes priority over the binder when DSAnimStudio opens
it. Its full contents were backed up and hash-verified before removing only the
active old project file. **Open the updated packed binder in DSAnimStudio** to
import it into a fresh project; the GUI was not launched during this handoff.
The old project's editor-only labels/layout remain recoverable from the backup.
Restoring the old project as the active sidecar without reconciling its timelines
can restore the old animation data on the next save.

Original inputs, independent packed-file backups, the full old working folder and
the old saved project now live under
`archive/game-updates/2026-09-09_to-steam-25080141/04-animations/`.
Its `restore-map.json` maps destinations to relocated backups. Packed originals
are in `before/`, and the full input folders are in `comparison-baselines/`.
The old project is `before/editor-project/c0000.anibnd.dcx.dsaproj`.
The accepted candidate, verification output and historical journal remain in
`.codex-temp/animation-update/1789016705947586400/`, with an archive pointer.
Retain the local archive until acceptance and include it in workstation backups.
Do not rerun the applied one-shot handoff. A rollback must restore matching loose
TAEs, packed files and project together, and remove only the three newly added
TAEs listed in the receipt after checking for subsequent edits.

## Repeatable editing route

1. Snapshot current vanilla, historical vanilla and the accepted mod sources.
   Compare editor/repo/Vortex/live contents; a packing-only hash difference does
   not select a different baseline. Stop on unexplained concurrent edits.
2. Qualify unchanged TAE serialization and specialized Witchy ANIBND repacking
   for the installed tool versions. Use scratch copies throughout. Keep binary
   TAE data; do not substitute an unqualified recursive XML round trip.
3. Build an explicit merge plan keyed by TAE file and animation ID. Preserve mod
   differences where upstream is unchanged. Reconcile overlapping events by
   identity and expected old values, not only list positions or whole-file copies.
4. Use the qualified SoulsFormats reader/writer for changed TAEs and copy wholly
   new vanilla TAE files unchanged. Repack the scratch `*-wanibnd` folder with
   `WitchyBND.exe --silent --repack <scratch-folder>` using its ANIBND metadata.
   Keep the current global Recursive=false setting; do not change tool settings
   implicitly. Verify outputs and require every difference to match the plan.
5. Account for DSAnimStudio's saved project and open buffers before authoring
   handoff. Back up and synchronize the same accepted loose/packed candidate;
   preserve deployment hardlinks and check hashes. Never invoke broad propagation
   as part of a qualification build.

Durable tool/output hashes, affected IDs, exact event edits and clip references
are in [the receipt](patch-updates/steam-25080141-animations.json). The local
scratch helper is diagnostic tooling, not a general-purpose animation editor.
Requalify after changing the tool/library/template version.

## Remaining acceptance

Run ER-024 through ER-026 in [TEST-MATRIX.md](../TEST-MATRIX.md), coordinated with
the separate behavior/HKS update. Check the new skills, eight affected moves,
casting/cancel windows, sounds and existing Sovereign special attacks. The separate
`c0000_a0x` repo/live clip discrepancy was preserved, not resolved by this TAE
update. No Nexus release or package upload was performed.
