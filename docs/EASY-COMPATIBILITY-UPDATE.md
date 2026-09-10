# Completed effects, icons and older menu-text compatibility update

Applied and hash-verified against installed Steam build 25080141 on 2026-09-10T04:34:05.186459+00:00.
These are the confirmed easy fixes from the shipped-file audit. HKS, behavior graphs,
animations, regulation, materials, events, maps and ESD dialogue were not changed.
Gameplay verification remains pending; this does not mark Sovereign release-ready.

## Results

| Output | Accepted change | Preservation checks |
|---|---|---|
| sfx/sfxbnd_commoneffects.ffxbnd.dcx | 19 FXRs plus 19 resource lists added | All 15,189 existing member payloads/flags/names preserved; total 15,227 |
| menu/hi/00_solo.tpfbhd + .tpfbdt | 30 missing individual textures added on the current archive layout | All 3,049 existing payloads preserved; total 3,079 |
| menu/hi/01_common.tpf.dcx | Six unchanged-old sheets replaced with current sheets | Other 50 texture payloads and decoded metadata preserved |
| msg/engus/menu.msgbnd.dcx | 33 upstream entry changes merged | 66 custom differences preserved; zero conflicts |
| msg/engus/menu_dlc01.msgbnd.dcx | 33 upstream entry changes merged | 72 custom differences preserved; zero conflicts |

The six sheets are SB_FE_02, SB_Icon_08_dlc, SB_MainMenu_02, SB_Operating_1,
SB_Preset and SB_Preset_2. Each selected mod sheet matched historical vanilla before
replacement. Existing custom DDS/PDN source artwork was not overwritten.

The installed historical loose extraction has uncertain exact patch provenance.
Current inputs were extracted from the installed game archives and fingerprinted.
Counts describe these snapshots, not every version of the mod or game.

## Locations and backups

The handoff verified **57 paths**, made **51 physical writes**, and preserved six
existing Vortex/live hardlink pairs. This includes 38 newly added authoring files.

- Effects: repo, SFX workspace packed output, main Sovereign Vortex package and live
  Game/mod. The 38 loose source additions were also installed in the SFX workspace's
  existing effect/ResourceList folders. Existing loose source files are unchanged.
- Older menu text: repo, main Sovereign Vortex package and live Game/mod. These two
  binders have no saved Smithbox counterparts in the inspected workspace; the
  separately maintained DLC02 text and existing propagation scripts were untouched.
- Icons: repo, **Sovereign - Textures** Vortex package and live Game/mod. Existing
  separate-package ownership is retained. The main Sovereign package remains free of
  these three archives and does not silently bundle the texture package.

Independent rollback copies and relocated restoration map:
`archive/game-updates/2026-09-09_to-steam-25080141/02-effects-icons-and-older-text/`.
Originals are in `before/`; labelled inputs are in `comparison-baselines/`.
Accepted candidate copies and the historical journal remain in the original
scratch run. Read the archive entry's README.md and `restore-map.json` before rollback.
Restore the solo header/data pair together and
restore existing targets in place to preserve Vortex links. Only the 38 specifically
recorded new source files are removed when undoing the authoring additions; do not
delete or replace the whole authoring workspace.

Durable per-entry evidence: [steam-25080141-easy.json](patch-updates/steam-25080141-easy.json).
Detailed temporary qualification, candidates, source inventory and comparisons:
`C:/Repositories/Sovereign/.codex-temp/easy-update/1789013816480952100/`.

## Qualified editing routes

WitchyBND unchanged BND/BXF/TPF rebuilds passed comparisons before editing. The two
older menu binders also passed complete binary FMG comparisons. Text merging used
the previously qualified direct SoulsFormats FMG writer, preserving null, empty,
whitespace and literal-marker strings, table ordering and metadata.

The real loose SFX source folder rebuilt to exactly the original decoded binder.
The candidate used the same specialized FFXBND source workflow as the author's
propagator. Adding members shifts 8,490 existing numeric IDs under its established
sorted category numbering, with ranges starting at 0/100000/200000/300000/400000.
Every pre-existing payload and relative entry order was checked; IDs were not blindly
ignored. All 19 new resource lists have their named packed resource counterparts.
The changed binder's full ID mapping is retained in the scratch plans directory.

The icon pair uses current vanilla member identities/layout with existing mod payloads
overlaid by exact names. The common TPF uses the six current texture records and keeps
all other mod records. Both were reopened and compared with explicit full expectations.

The installed Smithbox reader does not recognize the mod's DFLT header variant.
For read-only inspection, the diagnostic validates its compressed/uncompressed sizes
and decompresses the zlib stream before invoking the binary reader. WitchyBND handles
the actual unpack/rebuild. This is not evidence that the old file was corrupt.

## Remaining acceptance

- Check new and existing item/class icons, loading/help imagery and existing custom UI.
- Check old/custom effects and the added effect visuals when their gameplay triggers
  are available. New weapon behavior still depends on the deferred HKS/animation work.
- Check existing custom menu text and current text in the game's supported language/
  DLC configurations. Updating these older binders does not establish which binder
  is selected in every installation.
- The Torrent appearance menu still requires the separately deferred shared ESD merge.
- Preserve the separate texture package when planning releases; the main NEXUS
  workflow currently packages only Sovereign. No ZIP was published or Nexus page saved.

No game session was run and no manual test was marked passed. All 198 other
runtime-location comparisons from the preceding audit remained unchanged, including
the intentionally deferred HKS, behavior and animation files and the existing a0x
repo/deployment discrepancy.
