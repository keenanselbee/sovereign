# Sovereign file ownership: verified findings

Investigated 2026-09-10. This resolves the six file-ownership questions in the
repository plan. No runtime, editor, Vortex or live-game files were changed.
Detailed read-only exports and diagnostic source are retained in
`.codex-temp/ownership-review-20260910/`.

## Evidence and limits

- Compared all 194 regulation binder members between repo and saved Smithbox.
  Decoded every differing parameter table and compared row IDs, order, names and cells.
- Inventoried the complete main and texture stages, excluding the main package's
  declared authoring directories, and compared stage/repo/live hashes.
- Read the actual game-root Vortex deployment manifest and checked file identity
  (hardlinks), rather than inferring ownership from equal filenames alone.
- Extracted Crucible Knight binders, older English menu binders and Roundtable
  dialogue/events directly from installed encrypted archives. Steam build is
  25080141; archive/header and extracted-file hashes are in the extraction receipt.
- Rechecked the prior Hewg extraction against the fresh binder; they are identical.
  Reused the prior a0x decoded comparison after matching its recorded input hashes.

All 70 main-package files (347,720,188 bytes) match the live installation. All three
texture-package files (1,611,664,539 bytes) match repo and live. Every one of the
repo's 66 declared runtime files is present in the main stage. These checks establish
file relationships and content, not successful gameplay or VDB deployment acceptance.

## Decisions supported by the files

| Group | Finding | Recommendation |
| --- | --- | --- |
| Regulation | Gameplay fields match completely; saved Smithbox retains additional row names | Keep Smithbox as named authoring baseline; current shipped gameplay needs no merge |
| a0x motions | Vortex/live have the one additional ultimate motion; shared contents match | Preserve and accept the Vortex/live binder into repo/editor through its own handoff |
| c2500 model/textures | Sovereign-owned custom Crucible Knight variant used by Hadeon | Import all three staged binders into repo together, retaining material dependencies |
| c8000 Torrent | Three separately owned, physically linked external mods | Keep them outside Sovereign's managed/package set |
| Older menu binders | Real custom text on the current baseline; stage/repo/live agree | Retain both, with no mandatory Smithbox counterpart |
| Large icons | Separate texture package owns all three, with exact repo/stage/live agreement | Preserve separate package and ignore rules; manage paired texture files together |

These recommendations do not authorize deleting an absent counterpart or treating
every file in the shared live mod directory as Sovereign-owned.

## Regulation: no gameplay conflict

Both files report regulation version 11711000 and contain 194 members. The 91
differing table payloads contain 112,604 row-name differences, zero differing gameplay
cells, zero added/removed rows and zero row-order changes. No nonempty repo name was
replaced by an empty editor name. The common `Stripped Row Names.json` file is already
identical in Smithbox, repo and the staged authoring directory:
`8187a032dfdaeff10485cc4f8336ab37b7938989e54c5cf1062a28a8ca497b79`.

Repo/live/stage regulation hash:
`6c3d9d39b147517e8a43e8a5f4720d04a6d0b44f72aff2cf6c9b0e12b177a88d`.
Saved Smithbox hash:
`663de145ee0be6719bd5a5a01243d666ae044c0647b274743a66662e6586de62`.

Retain names for editing. Do not strip them or replace gameplay merely to make the
status display green. The future semantic status should report gameplay equality
and naming differences separately. An accepted future parameter change should use
the named authoring baseline and preserve its matching source metadata. There is no
urgent runtime correction required for this difference.

## a0x: accept the extra motion, not the older authoring binder

The named sources and hashes in [the feature plan](FEATURE-CORRECTNESS-PLAN.md) still
match. Repo/editor have 575 members; Vortex/live have 576. The additional member is
`a984_032400.hkx`, ID 1984032400, 50,404 bytes. All 575 shared member payloads and
compared metadata match. Vortex records Sovereign as owner and its a0x is hardlinked
to live. There is no justification for replacing it with the older repo/editor copy.

The configured DSAnimStudio workspace has an active packed a0x but no active unpacked
a0x folder or matching a0x project was found. The `_Default` unpacked folder and
historical `_` binders are references, not automatically selected authoring sources.
The main animation folder's `c0000_a0x.txt` is a split-data instruction, not the missing
motion. No loose `a984_032400.hkx` was found under the searched Modding/Elden Ring root.

For the handoff, back up the affected packed copies and retain the exact current
Vortex bytes in repo/DSAnimStudio. Create a reproducible unpacked source from that
accepted binder only when needed; do not rebuild from `_Default`. Existing main-TAE
sources/projects are a separate group and need not be replaced for this correction.

## c2500: these are Hadeon's custom model assets

Vortex's manifest assigns all three binders to Sovereign, and each stage file is
hardlinked to the corresponding live file. They differ from newly extracted vanilla:

- `c2500.chrbnd.dcx`: five members; only the FLVER payload differs. Its model has
  54 materials, 40 meshes and 179,506 vertices versus vanilla's 27 materials,
  27 meshes and 118,309 vertices. Both contain 704 nodes. Header metadata matches.
- `c2500_h.texbnd.dcx` and `c2500_l.texbnd.dcx`: each retains all 46 original
  textures unchanged and adds 46 `c2600`-named textures; none are removed.
- All 33 distinct material references resolve exactly once in the repo's accepted
  `allmaterial.matbinbnd.dcx`. The added variant includes `#31#` materials.
- The current shrine map's Hadeon actor, entity 18002354 (`c2500_9004`), uses model
  c2500 and NpcParam 25000011, named Crucible Lord Hadeon in Smithbox. Its display
  mask enables 31, alongside 10/11/12, connecting the custom variant to this encounter.

This is sufficient evidence to retain/import the three files as a coordinated
Sovereign group. Treat the accepted packed binaries as the available source until
an original model-editing project is located. No active custom loose model/texture
source was found in the searched editor roots; do not substitute vanilla or Nightreign
reference files. The audit does not establish the identity of the original asset
author or replace a visual check of Hadeon and ordinary Crucible Knights.

## Torrent, text and icons

The deployment manifest, SHA-256 and physical hardlinks agree on all three Torrent
files: Fast Torrent owns `action/script/c8000.hks`; Better Torrent Movements owns
`chr/c8000.anibnd.dcx`; Long-Horn Torrent owns `chr/c8000.chrbnd.dcx` under Game/mod.
Their separate packages explain the earlier live-only warnings conclusively.

The older English menu binders contain 66 and 72 entry differences respectively
from the freshly extracted baseline, including Sovereign banners, custom dialogue
options and Dragon Communion text. They are not disposable vanilla leftovers.
Keep their accepted bytes and current text-editing route; an absent saved Smithbox
copy is not a missing game file. Existing whitespace differences are preserved data,
not a reason to run a broad text normalization.

All three icon archives are owned by Sovereign - Textures in the default deployment
manifest and are hardlinked to Game/mod/menu/hi. Their repo copies match exactly.
Keep `00_solo.tpfbhd` and `00_solo.tpfbdt` together and retain `01_common.tpf.dcx`.
The separate package remains useful; do not move these ignored binaries into Git
accidentally during the layout migration.

## Deployment workflow implications

Sovereign main and textures use the recorded default game-root deployment, preserving
their prepared `mod/` paths and main's `mods/Scripts-Data-Exposer-FS.dll`. The separate
Elden Mod Loader deployment manifest is not the manifest owning these Sovereign files.
Use that observed layout for VDB qualification; do not copy Grailwright's BepInEx type.

65 main files are stage/live hardlinks; five map/navigation files are independent
copies with identical bytes. All three texture files are hardlinked. Updating only
one location cannot be assumed to update every counterpart. The replacement handoff
must verify destinations and existing file identity, then let Vortex own deployment.

The loader DLL is a main-package external dependency, with matching stage/live bytes
and recorded ownership. Its provenance/redistribution gate remains open. Preserve
its current location and pinned hash; do not invent a source build or silently bundle
other mods from the shared live directory. Actual VDB stage/activate/rollback testing
is still pending and is separate from this layout inspection.

## Hewg: the four-boss gate needs a dedicated integration

The agreed requirement is Godskin Duo plus the three base-game Fallingstar Beasts,
with the full masterpiece speech. Local Godskin Duo event 13002850 sets 9114.
The beast flags are recorded in the feature plan. No ore items are required.

Two real dependencies make a simple condition replacement insufficient:

1. Hewg helper x58 unlocks the farewell when 11109230 (masterpiece heard) is set and
   11109231 is not. Holding the masterpiece behind the beasts also holds the farewell
   unless we deliberately preserve its accessibility independently. Do not fake weapon
   collection or consume the farewell to work around this.
2. Main menu x39 only calls x58 during stage 3226. Common event 3239 switches him to
   3227 on flag 9116 (Maliketh), and later 3228 is possible. Reusing the old branch alone
   introduces a story-stage cutoff in addition to the requested four boss flags.

The implementation must separate boss eligibility, weapon collection, speech-heard
state and ordinary story progression. Preserve the farewell independently as agreed.
The author settled the post-memory-loss behavior: use only "Use my masterpiece to
slay a god." for the late handoff; use the full masterpiece speech beforehand.
Award once per journey, requiring that journey's Godskin Duo and three base-game
beast victories again. Neither handoff is implemented yet.
No files need to be deployed to finish this ownership decision or begin repo tooling.
