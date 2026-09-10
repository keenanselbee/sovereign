# Missing custom SFX recovery

Applied and hash-verified 2026-09-10T06:27:34.884088+00:00.

Restored 92 custom FXRs and their 92 resource lists from Backup 2. This includes Obliterator, Nemesis/Oath of Sin, Soulflame Heresy, Dragon Communion, Stormblessed Zweihander, Sovereign Fury, Fire Giant, Crimson consumables, deflection, Hadeon, Oath of Order, Black Sun's Zenith and the ultimate force wave. Existing visual variants were retained. This repairs missing asset coverage; it does not establish that every effect is currently triggered or renders correctly in game.

## Preservation and build checks

- The unchanged specialized WitchyBND rebuild matched the complete current binder inventory.
- All 15,227 existing member payloads, paths, flags and compression types were preserved, with original relative ordering and binder metadata.
- Exactly 184 additions produce 15,411 members. Canonical category numbering shifts 214 existing binder IDs; this is expected and checked, not a change to FXR effect IDs.
- Final packed SHA256: `e07bd8d69a499b1cafce9a4db519c4a2bf6acff043877ef2ee35f4bc2ad6628f`.
- 372 destination paths verified; 371 physical writes; 1 Vortex/live hardlink pair preserved.
- Existing loose authoring files and all 230 pre-existing repo modified files remained unchanged.

## Locations

The recovered files are installed in both `sfx/modified/sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd` and the active external SFX authoring folder. The rebuilt common-effects binder is synchronized across repo, SFX authoring output, main Sovereign Vortex package and live Game/mod. The existing SFX propagation workflow now rebuilds from the recovered loose sources.

## Archive and future visual alternatives

[Archive entry](../archive/game-updates/2026-09-09_to-steam-25080141/06-sfx-recovery/README.md).

`before/` contains independent original packed files and complete authoring/repo modified source snapshots. `recovered-additions/` preserves the imported bytes and provenance. `alternative-designs/backup-2/` contains the ten unused FXR variants and two matching resource lists, explicitly retained as potentially useful future designs. They are not runtime inputs. The accompanying comparison documents colour, size, timing, layer and sound differences.

Consult `restore-map.json` before a coordinated rollback; check subsequent edits, preserve hardlinks, and remove only specifically listed new source files if reverting this recovery. Do not run old handoff scripts or replace the full current source from an older backup without review.

## Resource findings and manual checks

The deflection resource-list entry `s42021_a.tif` is not requested by the decoded FXRs; it was retained unchanged during this add-only recovery. No Nightreign texture was imported. Thorn Ward model s84157 and its three textures are present in the freshly verified current DLC02 common-effects binder, which has no inspected live mod override. Its valid resource references were retained.

Test Harness Void Eye's cast/glow, Obliterator crouch attacks and ultimate beam first. Then test the restored effects in their relevant systems, including Hadeon, Nemesis and Thorn Ward. The previously identified invalid one-handed Obliterator projectile behavior reference remains separate from this SFX repair. No game test was performed by the agent.

Exact file paths, hashes and deployment counts are recorded in [the receipt](patch-updates/steam-25080141-sfx-recovery.json). Detailed build logs and binder inventories remain under `C:\Repositories\Sovereign\.codex-temp\obliterator-vfx\recovery-1789021424455706200`.
