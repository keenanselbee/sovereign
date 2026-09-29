Opening pouch defaults and rescue-aware music
============================================

Author-approved local implementation, 2026-09-28. Gameplay verification is pending.
Source/runtime acceptance and editor sync were followed by the author's explicit
deployment request. Version 1.5.8 is deployed and verified; gameplay remains pending.


Rescue-aware music
------------------

Map event 18002862 no longer treats a host's transient zero HP as completed death.
It requires both current zero HP and existing death-confirmation flag 1055425042.
The unchanged monitor 5750402 sets that flag only after 0.5 seconds at zero HP,
excludes rescue protection 1627125, and resets after recovery. Visiting players
use their native CharacterDead state, independent of the host's flag.

Both phase cues stay running through rescue without a stop/start replay. Phase
transitions, boss victory and map departure retain their immediate music handling.
The heal, cooldowns, damage handling and actual HP values are unchanged; there is
no 1-HP floor or new event state. This change targets music, not other encounter
controllers or unrelated bosses' death checks.


Flask pouch trial
-----------------

The [guarded recipe](../../src/recipes/starting-flask-pouch/README.md) assigns empty
Cerulean flask 1050 to secondary slot 02 and empty Crimson flask 1000 to slot 03
in all ten player classes (3000-3009). The intended mapping is FP right, HP left;
native direction and empty-item persistence require a new-character test.

Each empty flask has initial count one. Class flask capacities remain HP 3 / FP 1,
and the existing Stranded Graveyard event 18000020 still awards item-lot group
2000: charged Crimson 1001 x3 and charged Cerulean 1051 x1. The grant flag 60000,
item lots, class stats, Memory of Grace and other pouch/quick-item slots are intact.
Whether native replenishment makes these empty entries usable earlier than the
grant is also a game-test question; no earlier filled-flask grant was added.

Automatic pickup equipment (`isAutoEquip`) is disabled for all 52 empty/charged
HP and FP variants through +12 (1000-1025, 1050-1075). Manual equipment permission
is unchanged. This item rule applies globally but does not clear existing saved
assignments or force a new layout on existing characters. Test that upgrading,
emptying, refilling and reallocating flasks retain the player's chosen slots.


Validation and recovery
-----------------------

Native parameter preparation passed exact table roundtrip and saved-output
readback. Only four fields in each of ten CharaInitParam rows and `isAutoEquip`
in 52 EquipParamGoods rows change. All other rows/tables and binder identities
are preserved. Candidate and receipt are under `.codex-temp/flask-pouch-review/`.
Independent recovery inputs are under `.sovereign/backups/opening-pouch-music/`.
The accepted regulation SHA-256 is
`3d41ea643daadaf79979220b8d09525a1968ab203279b11b62b52766978629fd`.
Smithbox handoff `6b0e1f255917468d94afbb8d9bafb27a` completed with one runtime file.

The event candidate is `.codex-temp/event-builds/1790580927479166200/receipt.json`.
Native comparison changes only event 18002862, preserving file metadata and all
other events; the eight other shipped event binaries remain equivalent.
The unshipped common_func reference remains unshipped. Accepted map-event hash:
`d38fa5bcfd63b0940c3cebbd51a6cb160be14655c91776c622f8fce3324f722a`.
All 20 Soldier/Rick source simulations pass, including repeated zero-HP rescue
in each phase, real death, admission/handoff, victory/map departure during rescue
and guest death handling. These are mocked source executions, not game tests.
Script handoff `6743f32ce54f45e08c1b66a3dd309051` completed for the event binary
and JS, with native source/output qualification `1790581007168782500`.
Independent destination hashes match both completed editor handoff receipts.
Repository preparation, scoped whitespace and local Markdown link checks pass.

Before acceptance in game: create a new character, inspect both pouch directions
before and after awakening, verify three HP charges and one FP charge, and check
that the quick-item bar stays empty of automatically assigned flasks. Exhaust and
refill each flask, upgrade it, change its assignment manually, rest and reload.
Also load an existing character and check that saved equipment was not rearranged.
For music, trigger a lethal beginner rescue in each Soldier/Rick phase, then verify
that genuine death, transformation, victory and map departure still stop or change
the correct cue. Guest death behavior also remains a manual check.


Deployment
----------

Version 1.5.8 contains the complete Hadeon 1.5.7 refinement plus this batch.
Relative to the prepared 1.5.7 payload, only regulation.bin and the m18 event
binary change. The reviewed full main package contains 77 files with the external
DLL preserved and no texture-package changes. Version metadata checks passed.

Prepared receipt: `.vdb/prepared/e3f140f8ab8f4251b32186eb7ea286df/receipt.json`.
Completed protocol-3 finalization:
`.vdb/finalizations/032d39b0a551408b81193b1484bcda8f/receipt.json`, request
`85954ad0-e618-4029-9af7-628527776f18`. Active profile `SkC-QjDMc` reports enabled,
deployed and verified. All 77 live-file sizes and SHA-256 hashes independently
match, recorded in `.sovereign/backups/opening-pouch-music/live-verification.json`.
The verified selected main package is now 1.5.8. No Nexus publication occurred.

The earlier 1.5.7 request was inspected and found failed because the game was
running. It was not resubmitted. The author closed the game before the distinct
1.5.8 request, which completed successfully.
