Workflow preparation checkpoint
===============================

Updated 2026-09-11 after VDB switching/rollback, installed-shortcut qualification and
layout migration. This covers S1-S6 preparation, not gameplay changes or publication.
No commits were made. Earlier implementation history is in
[WORKFLOW-PREP-HISTORY](WORKFLOW-PREP-HISTORY.md).


Implemented state
-----------------

- The accepted a0x binder preserves `a984_032400.hkx`; all three Hadeon c2500 assets
  are retained under `mod/chr/`.
- The catalog owns 69 main runtime files, three texture files and 1,118 source/metadata
  files. The main Vortex package has 70 files including the existing external DLL.
- Event, BND/binary FMG, ESD, specialized SFX and coordinated player qualifications
  have documented tools and drift-checked source/output handoffs.
- VDB main/textures staging, activation, verification and rollback passed against
  the real Elden Ring Default profile. Unrelated enabled mods stayed unchanged.
- Nine external VBS entry points now call `tools/Propagate-Sovereign.ps1`. They retain
  their familiar names but do not purge directories or copy into live/legacy stages.
- 519 accepted runtime/source files (1,989,940,099 bytes) moved into `mod/`, `src/` and
  `packages/textures/mod/` without byte changes. The 671 existing `src/player/` files
  stayed in place. Texture archives remain ignored.
- Two root MapStudio copies moved separately into `reference/mapstudio/`: one is an
  exact runtime duplicate, the other differs. Both retain unassigned provenance and
  are excluded from authoring/package inputs. Their original bytes are backed up.
- Armor conversion and Hewg/per-journey reward choices remain recorded in
  [FEATURE-CORRECTNESS-PLAN](FEATURE-CORRECTNESS-PLAN.md), without implementation here.


Verification evidence
---------------------

| Check | Evidence |
| --- | --- |
| Main and texture switch/rollback, 73 live files, unrelated enabled state | `.sovereign/vdb-qualification/switch-20260911-2110/receipt.json` |
| Launcher run/resume before migration | `.sovereign/propagation/0df6fb839d6c48bc89196019d2a9051d/receipt.json` |
| Installed map VBS after migration, real source/stage/deploy/verify route | `.sovereign/propagation/40301ece7419411f910a488923f61213/receipt.json` |
| Current-layout event build, nine runtime outputs equivalent; common_func not shipped | `.codex-temp/event-builds/1789162219417070600/receipt.json` |
| Native editor-SFX rebuild, byte and full decoded equality | `.codex-temp/sfx-builds/1789158320349879600/receipt.json` |
| Current selected-stage draft ZIP | `.codex-temp/vortex-packages/1789162230924566100/receipt.json` |
| Complete post-layout input/output/recovery verification | `.sovereign/layout/8187a2c0743f410ab523d5f04a657cce/post-verification.json` |

The installed map shortcut selected main build `6a286533c8067213276f5a42`, local label
`0.0.0-dev.20260911212451204`. Textures remain on `fe46cb9983080cddbe556f20`. All payload
bytes match the accepted baseline; these labels are local development identities.
The original and second byte-identical test versions remain retained for rollback.

The real launcher test caught and fixed multiple Python PATH matches and stale-heartbeat
handling while waiting for an existing request. The same deployment request was resumed
successfully. Launcher transcripts now capture native output and the resume receipt.
Current checks are `python -m unittest discover -s tools/tests -q` and
`python tools/sovereign.py check`: 74 tests pass and all 69 main runtime candidates
pass preparation checks. Manual game acceptance remains unverified.
The final shortcut amendment limits item propagation to `item_dlc02.msgbnd.dcx`;
fixtures verify that menu changes are excluded from acceptance and staging. No item
binder was propagated during that amendment. Its targeted verification is recorded
beside the post-layout report in `shortcut-amendment-verification.json`.


Recovery locations
------------------

- Full pre-work repository backup:
  `Z:/Backup/Elden Ring/sovereign/repo-before-workflow-refresh-20260910-201725/Sovereign`.
  Its parent verification records 126,291 files, 41,188,252,348 bytes, SHA-256 verified,
  with no exclusions. It includes the dirty worktree and ignored files.
- a0x/Hadeon original and accepted bytes:
  `Z:/Backup/Elden Ring/archive/workflow-prep/20260910-224802-assets/receipt.json`.
  The receipt still contains its historical repo-local archive paths; resolve payload
  basenames inside this verified relocated directory and runtime destinations through
  the layout map.
- Qualified player source handoff:
  `.sovereign/handoffs/01ffd4d8dfc94d37a40b2c58176a94ea/receipt.json`.
- Qualified dialogue source/output handoff:
  `.sovereign/handoffs/edb294a84a734f8e9d0f684867d2e690/receipt.json`.
- SFX packed-editor save backup:
  `.sovereign/sfx-builds/b01c2fe439534ecc9a6e41fb442ba29e/receipt.json`.
  Before/after bytes were identical, so that qualification did not replace the editor file.
- Nine original shortcut implementations and installed candidates:
  `.sovereign/shortcuts/90b634c707ee45908bfb080a7a711ad5/receipt.json`.
  Preserve the listed backups; do not run them against a VDB deployment. Before manual
  restoration, require each target to match its recorded installed hash. Restoring an
  old shortcut would also restore obsolete paths and is not a normal rollback.
- Item-only shortcut amendment, superseding that shortcut's original installed hash:
  `.sovereign/shortcuts/e138fac926e3421bbd6952a97275a1c5/receipt.json`.
  This retains both versions and leaves the original installation receipt intact.
- Layout map and independent backups for every moved file:
  `.sovereign/layout/8187a2c0743f410ab523d5f04a657cce/receipt.json` and `backup/`.
  `layout_workflow.py restore` refuses later edits. Do not apply the completed plan again.
- Unshipped map-reference relocation:
  `.sovereign/layout/8187a2c0743f410ab523d5f04a657cce/reference-copies/receipt.json`.

Historical handoff receipts retain old catalog/path fingerprints. Do not blindly replay
them after migration. Use the relocation map and preserved copies for inspected recovery.
Some empty former directories remain where Windows refused removal; they contain no
migrated payload and are not runtime inputs. The check command detects recreated retired
runtime files.


Next scope
----------

Use the [current command reference](WORKFLOW-COMMANDS.md) for editing and propagation.
The former legacy Sovereign packages stay disabled; the VDB versions own deployment.
Gameplay work and release qualification remain in S7/S8. No gameplay test was marked
Passed, no public release version was assigned, and no Nexus upload or save occurred.
