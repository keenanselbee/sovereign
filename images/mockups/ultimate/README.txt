Ultimate tutorial artwork

The approved runtime artwork is now src/textures/tutorial/ultimate.png,
copied unchanged from the author's Desktop ultimate.png on 2026-09-26. The images
below retain the earlier extraction/mockup references.

combat-illustration-original.png: the requested knight-swinging-his-sword combat
scene, extracted directly from base-game MENU_Tuto_00018.tpf.dcx at 544x336.
Verified the current Sovereign texture's DDS is byte-identical to the base game.
This is the illustration shown in the Ultimate tutorial, not the shared UI frame
or charge icon. No AI editing, resizing, or color adjustment. The earlier
background.png contains this same scene under a less descriptive name.
Extraction evidence: .codex-temp/ultimate-combat-extraction-20260926/.

tutorial-panel.png: original shared tutorial panel texture, extracted at its
native 646x102 size with alpha preserved. This is MENU_FL_Dialog.png from
SB_MainMenu_02, crop x=0, y=1448, width=646, height=102. The installed base-game
02_130_tutorial_modal.gfx explicitly references MENU_FL_Dialog. The complete
tutorial window is composed by the UI; this file is its source panel texture,
without the separate illustration, text, or divider. No AI generation or upscale.
Verified every output RGBA pixel against the decoded atlas (zero differences).
Extraction evidence: .codex-temp/tutorial-panel-extraction-20260926/.
Texture source: packages/textures/mod/menu/hi/01_common.tpf.dcx.
Layout source: installed base-game menu/hi/01_common.sblytbnd.dcx.

background.png: exact decoded 544x336 illustration extracted from the current
texture package's MENU_Tuto_00018.tpf.dcx. TutorialParam 5750 uses imageId 18
(Guard Counters). This is the scene illustration, with no tutorial text overlay.

icon-20269.png: original empty Ultimate charge meter, used by SpEffect 277.
icon-20280.png: original fully charged Ultimate meter, used by SpEffect 287.
Both are exact atlas crops from the current package's SB_Status_00 texture using
the base-game status-icon layout. Intermediate meter states remain in the atlas.

icon-upscaled.png: faithful 1280x1280 enlargement of full-charge icon 20280.
Uses 32x nearest-neighbor pixel replication, preserving every original RGBA
pixel exactly. No AI redrawing or invented detail. The original 40x40 pixel
structure remains visible at large sizes. Replaced the earlier AI reconstruction
on 2026-09-26; originals and runtime artwork remain unchanged.

Extraction evidence: .codex-temp/ultimate-artwork-20260926/ at repository root.
Sources: packages/textures/mod/menu/hi/00_solo.tpfbhd and .tpfbdt;
packages/textures/mod/menu/hi/01_common.tpf.dcx; mod/regulation.bin.
