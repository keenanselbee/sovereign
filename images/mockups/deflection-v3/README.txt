Deflection mockup v3

spark-overlay.png: standalone AI-generated spark burst referenced from scene.png.
1594x986 RGBA with verified transparent background and semitransparent glow.
Place on a layer above the combat illustration, then move and scale the white-hot
center onto the impact point; the generated placement is not automatically aligned.
Adjust layer opacity to taste. No scenery, icon or panel is included. Prompt and
generation mode are recorded in spark-overlay.txt. No runtime changes.

combat-illustration-original.png: original 544x336 combat illustration, decoded
directly from installed base-game MENU_Tuto_00016.tpf.dcx. No added panel or icon.
tutorial-image-current.png: exact decoded 544x336 image from the current Sovereign
texture package's MENU_Tuto_00016.tpf.dcx, including enhanced sparks and icon panel.
Current TutorialParam row 1180 selects imageId 16. Both PNGs were extracted without
AI editing or resizing; they preserve the decoded DDS pixels. Extraction evidence
and parameter check: .codex-temp/deflection-illustration-extraction-20260926/.
Sources: base-game and packages/textures/mod/menu/hi/00_solo.tpfbhd/.tpfbdt pairs.

scene.png: clean illustration with enhanced deflection sparks.
scene-faded.png: alternative combat illustration with the enhanced spark burst
and a more muted, faded scene. Created with built-in imagegen using the original
combat illustration as the base and scene.png as the spark reference. AI edit,
not a pixel-exact transfer. Prompt recorded in scene-faded.txt. Mockup alternative;
the existing historical composite still uses scene.png.
panel-background.png: reusable blank gold-bordered panel, transparent outside.
icon.png: unchanged extracted game icon 20297.
icon-upscaled.png: faithful 1280x1280 enlargement of icon.png, using 32x
nearest-neighbor pixel replication. Every original RGBA pixel is preserved;
no AI redrawing or invented detail. The original 40x40 pixel structure remains
visible at large sizes. This separate copy is not used by the runtime recipe.
layered-mockup.svg: self-contained scene, panel and icon layers.
mockup.png: flattened preview.
compose.ps1: reproduces the PNG from the three source layers.

The built-in image generation tool created the clean scene and blank panel.
Prompts: remove all overlays and text while preserving the deflection scene; create an isolated empty charcoal panel with gold corner ornamentation and transparent surroundings.
The final assembly uses the exact extracted icon without AI redrawing.
The runtime texture build recipe is in src/textures/tutorial/.
As of 2026-09-26, its approved input is deflection.png in that source directory,
copied unchanged from the author's Desktop deflect-2.png. This folder retains
the earlier mockup variants; they are no longer the runtime recipe inputs.
