Sovereign tutorial replacement, 1.0.7
=====================================

Local follow-up, 2026-09-25: the Ultimate Attacks lesson now waits 2.5 seconds
instead of 1 second after Soldier of Godrick arena admission. Cancellation,
transformation protection and the once-shown receipt are unchanged. The Deflection
panel and its inventory note now explain up to four guard-counter charges and
include the Guard Counter input. The spirit at the Cave of Knowledge entrance
uses the approved Sovereign wording below. These edits are separate from the
already deployed 1.3.2 baseline; deployment and game acceptance remain pending.
Version 1.3.3 packages the approved sparks artwork with game icon 20297 and a
blank reusable gold panel. The scene, panel and icon remain separate source
layers; the image contains no charge diamonds, text or concept-preview label.
See [verification and remaining checks](test-results/2026-09-25-opening-dialogue-tutorial.md).

Version 1.3.2 implements the complete opening lesson order: Deflection two seconds
after crossing 18002658; Ultimate Attacks one second after Soldier of Godrick
arena admission; Jump to Evade three seconds inside Hadeon's room. Both boss
lessons run in the map event file, with no tutorial worker waiting in common.
They retain separate once-shown receipts and cancel pending display on invalid
player/encounter states. The jumping lesson uses existing Stance Breaking artwork
17 and approved general wording without Heavy Attack instructions. See
[the implementation and exact text](GROUND-STOMP-GOAL.md). Native/source checks
are distinct from pending gameplay acceptance.

2026-09-25 local update: Deflection now triggers two seconds after crossing
existing region entity 18002658 before the added Godrick Knight (18000258).
Walking out of the region does not cancel the delay; death/map departure does,
with a fresh entry permitting retry. Event 18002663 retains shown flag 710180,
note receipt 69060 and item 9106. Soldier of Godrick proximity and transformation
guards no longer own this lesson. No map edit is required. Compiled verification
and source simulation are separate from pending game acceptance and deployment.
This initial deflection handoff preceded the completed 1.3.2 sequence above. See
[the current plan](GROUND-STOMP-GOAL.md). The original implementation below is
historical context.

The author approved suppressing every vanilla tutorial popup and reusing the arena
Guard Counters slot for Deflection with Guarding artwork. Keep the existing
proximity trigger, add a two-second delay, and retain its shown/item flags. Existing
save migration is explicitly out of scope. No game test has been performed.

Implementation
--------------

- TutorialParam 1180 retains menuType 100, triggerType 0, repeatType 1, textId
  302400 and unlock flag 710180. Its imageId changes from 18 to 16, copied from
  Guarding row 1070. No texture asset changes.
- The other 85 rows, including unnamed rows 0-2, require flag 1055420990. This
  reserved flag stays OFF; no event enables it. All their other fields are preserved.
  In particular, original tutorial flags can still be set and old notes awarded by
  vanilla events without granting these panels display permission.
- Event 18002663 retains the host-only 10-metre check around phase-one entity
  18000851 and waits two seconds before showing the lesson. It abandons display on
  death/departure/defeat, waits out transformation flag 18002851, and sets 710180
  immediately before ShowTutorialPopup. A retry after an interrupted delay can
  show the lesson; a displayed lesson retains vanilla once-shown behavior.
- TutorialTitle/TutorialBody entry 302400 is updated in all three shipped English
  menu binders. GoodsName/GoodsInfo/GoodsCaption entry 9106 in item_dlc02 becomes
  About Deflection with matching instructions. Existing note award flag 69060,
  quantity and multiplayer restrictions are preserved.
- This suppresses TutorialParam panels and control hints. Item acquisition notices,
  ordinary dialogs, and existing tutorial-note awards are separate and unchanged.

Text
----

Title: Deflection

Tap Guard just before an attack connects to deflect it. Guard with a shield or a
weapon held in both hands.

Deflect in quick succession to build up to four charges and greatly increase
guard-counter damage. Successful deflections also charge your weapon's ultimate.

`<?keyicon@24?>` just before impact: Deflect

`<?keyicon@23?>` after blocking: Guard Counter


Cave of Knowledge spirit
------------------------

Map entity 18000701 (`c3660_9000`, TalkID 706021800) retains its existing
conversation and opening ellipsis. Replace these TalkMsg entries in all three
shipped English menu binders:

| Message ID | Wording |
| --- | --- |
| 706020010 | Brave Tarnished. Descend, and remember. |
| 706020020 | Raise your guard at the moment their steel strikes. |
| 706020030 | Your warrior's blood has not forgotten. |

TalkParam rows 70602000 through 70602003 form the adjacent dialogue sequence.
The saved annotated ESD source associates all four with the single call starting
at 70602000. The earlier scratch investigation incorrectly inferred that this
call displayed only the ellipsis; separate calls would risk repeating dialogue.
This text-only edit therefore adds no ESD override and changes no voice IDs,
animations, map placement or dialogue conditions.


Native row map
--------------

The current regulation contains 86 rows and matches installed vanilla TutorialParam
before this change. This table is from native inspection, not just the row-name
catalogue. Each suppressed row changes only unlockEventFlagId to 1055420990.

| ID | Original lesson | Result | Original gate | Image |
| --- | --- | --- | --- | --- |
| 0 | Unnamed placeholder | Suppressed | 0 | 0 |
| 1 | Unnamed placeholder | Suppressed | 0 | 0 |
| 2 | Unnamed placeholder | Suppressed | 0 | 0 |
| 1000 | Keybind: Camera Controls | Suppressed | 710000 | 0 |
| 1010 | Keybind: Using Items | Suppressed | 710010 | 0 |
| 1020 | Sites of Grace | Suppressed | 710020 | 3 |
| 1030 | Keybind: | Suppressed | 710030 | 0 |
| 1040 | Keybind: | Suppressed | 710040 | 0 |
| 1050 | Keybind: | Suppressed | 710050 | 0 |
| 1060 | Sorceries and Incantations | Suppressed | 710060 | 7 |
| 1070 | Guarding | Suppressed | 710070 | 16 |
| 1080 | Keybind: | Suppressed | 710080 | 0 |
| 1090 | Keybind: Dashing | Suppressed | 710090 | 0 |
| 1100 | Wielding Armaments | Suppressed | 710100 | 133 |
| 1110 | Keybind: Lock-on Target Change | Suppressed | 710110 | 0 |
| 1120 | Keybind: Guarding | Suppressed | 710120 | 0 |
| 1130 | Bows | Suppressed | 710130 | 14 |
| 1140 | Crouching | Suppressed | 710140 | 15 |
| 1150 | Keybind: Backstab | Suppressed | 710150 | 0 |
| 1160 | Stance Breaking | Suppressed | 710160 | 17 |
| 1170 | Keybind: HUD Display | Suppressed | 710170 | 0 |
| 1180 | Guard Counters | Deflection; Guarding artwork | 710180 | 18 -> 16 |
| 1190 | Stakes of Marika | Suppressed | 710190 | 105 |
| 1200 | Skills | Suppressed | 710200 | 19 |
| 1210 | Dodging | Suppressed | 710210 | 131 |
| 1500 | The Map | Suppressed | 710500 | 100 |
| 1510 | Guidance of Grace | Suppressed | 710510 | 102 |
| 1520 | Horseback Riding | Suppressed | 710520 | 103 |
| 1530 | Death | Suppressed | 710530 | 104 |
| 1550 | Summoning Spirits | Suppressed | 710550 | 106 |
| 1560 | Materials | Suppressed | 710560 | 107 |
| 1570 | Item Crafting | Suppressed | 710570 | 108 |
| 1580 | Containers | Suppressed | 710580 | 109 |
| 1590 | Flask of Wonderous Physick | Suppressed | 710590 | 110 |
| 1600 | Adding Skills | Suppressed | 710600 | 121 |
| 1610 | Birdseye Telescopes | Suppressed | 710610 | 112 |
| 1620 | Spiritspring Jumping | Suppressed | 710620 | 113 |
| 1630 | Vanquishing Enemy Groups | Suppressed | 710630 | 123 |
| 1640 | Teardrop Scarabs | Suppressed | 710640 | 115 |
| 1650 | Summoning Other Players | Suppressed | 710650 | 116 |
| 1660 | Cooperative Multiplayer | Suppressed | 710660 | 117 |
| 1670 | Competitive Multiplayer | Suppressed | 710670 | 118 |
| 1680 | Invasion Multiplayer | Suppressed | 710680 | 119 |
| 1690 | Summoning Pools | Suppressed | 710690 | 120 |
| 1700 | Hunter Multiplayer | Suppressed | 710700 | 124 |
| 1710 | Monument Icon | Suppressed | 710710 | 126 |
| 1720 | Requesting Aid from a Hunter | Suppressed | 710720 | 125 |
| 1730 | Fast Travel to Sites of Grace | Suppressed | 710730 | 127 |
| 1740 | Strengthening Armaments | Suppressed | 710740 | 128 |
| 1750 | Adding Affinities | Suppressed | 710600 | 122 |
| 1760 | Multiplayer | Suppressed | 710760 | 200 |
| 1770 | Pouches | Suppressed | 710770 | 130 |
| 1780 | Roundtable Hold | Suppressed | 710780 | 129 |
| 1800 | Keybind: Mounted Double Jump | Suppressed | 710800 | 0 |
| 1810 | Great Runes | Suppressed | 710810 | 132 |
| 1820 | The Cave of Knowledge | Suppressed | 710820 | 134 |
| 1850 | Duels | Suppressed | 710850 | 135 |
| 1860 | United Combat and Combat Ordeals | Suppressed | 710860 | 136 |
| 1870 | Combat with Spirit Ashes | Suppressed | 710870 | 137 |
| 1880 | Marika's Effigy at Roundtable | Suppressed | 710880 | 138 |
| 1900 | Scadutree Blessing | Suppressed | 710900 | 140 |
| 1910 | Revered Spirit Ash Belssing | Suppressed | 710910 | 141 |
| 1920 | New Inventory Features | Suppressed | 710920 | 142 |
| 2000 | Equipment Menu | Suppressed | 720000 | 0 |
| 2010 | Item Crafting Menu | Suppressed | 720010 | 0 |
| 2020 | Inventory Menu | Suppressed | 720020 | 0 |
| 2030 | Status Menu | Suppressed | 720030 | 0 |
| 2040 | Message Menu | Suppressed | 720040 | 0 |
| 2050 | Multiplayer Menu | Suppressed | 720050 | 0 |
| 2060 | Level Up Menu | Suppressed | 720060 | 0 |
| 2090 | Allocating Flask Uses | Suppressed | 720090 | 0 |
| 2100 | Memorize Spells Menu | Suppressed | 720100 | 0 |
| 2110 | Sorting the Chest | Suppressed | 720110 | 0 |
| 2120 | Shop Menu | Suppressed | 720120 | 0 |
| 2140 | Ashes of War Menu | Suppressed | 720140 | 0 |
| 2150 | Spirit Tuning Menu | Suppressed | 720150 | 0 |
| 2160 | Remembrance Duplication Menu | Suppressed | 720160 | 0 |
| 2170 | Great Rune Menu | Suppressed | 720170 | 0 |
| 2180 | Mixing Physicks | Suppressed | 720180 | 0 |
| 2190 | Rebirth Menu | Suppressed | 720190 | 0 |
| 2200 | Remnant Crafting Menu | Suppressed | 720200 | 0 |
| 2210 | Map Menu | Suppressed | 720210 | 0 |
| 2220 | Smithing Menu | Suppressed | 720220 | 0 |
| 2230 | Colosseum Menu | Suppressed | 720230 | 0 |
| 2300 | Scadutree Blessing Menu | Suppressed | 720300 | 0 |
| 2310 | Revered Spirit Ash Blessing Menu | Suppressed | 720310 | 0 |

Verification
------------

Scratch evidence is retained at `.codex-temp/deflection-tutorial-20260923/`.
Native regulation comparison verifies 86 exact cell changes, unchanged row order,
all other table bytes and binder metadata. Text candidates use exact old-value
patches and full decoded binder comparison. Event compilation is independently
decoded before acceptance. Build and deployment receipts are recorded in
[the verification record](test-results/2026-09-23-deflection-tutorial.md).

ER-063 and ER-064 remain Pending. In-game checks must confirm the display gate
blocks both scripted and menu-triggered lessons, fresh-save once-only timing,
input icons, art/layout, rereading the note, solo pause behavior, tutorial settings,
multiplayer and death/transition recovery. Native definitions document the gate;
static validation does not establish actual engine suppression or menu behavior.
