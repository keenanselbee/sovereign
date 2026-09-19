# Feature correctness and Obliterator acquisition

Implementation status 2026-09-11: Crusade, armor conversion and Hewg acquisition are
accepted into the repo; native preservation checks passed and game tests remain
pending. See [the implementation report](GAMEPLAY-CORRECTNESS-UPDATE.md) for current
status and recovery records. The investigation and agreed design below are retained.
The subsequent [mechanics review](MECHANICS-REVIEW.md) traces the custom Claw and
Dragonbolt replacement paths and Obliterator's remaining payload question. It
recommends preserving the authored mechanics pending focused observations, rather
than restoring absent rows automatically. No gameplay changes accompanied that review.

Historical design snapshot from 2026-09-10, before gameplay implementation. Agreed
designs and remaining investigations are distinguished below; the implementation
report above supersedes its earlier status statements. Execution stages and the full pre-cleanup repository
backup are recorded in [the repository plan](REPOSITORY-AND-RELEASE-PLAN.md).

The retained `.codex-temp/feature-followup/` investigation contains parameter tables,
timeline/member inventories, historical comparisons and extracted boss events. This
review rechecked hashes of current repo/editor/vanilla and both backup regulations,
all four a0x binders, three compared timeline binders, and all nine extracted files.
They match the retained inspection inputs. These are static findings, not game tests.

## 1. Preserve the missing ultimate motion first

**Completed during workflow preparation:** the verified 576-member a0x was accepted
into repo and active DSAnimStudio with independent originals/accepted copies at
`archive/workflow-prep/20260910-224802-assets/receipt.json`. The table below describes
the pre-handoff comparison; the repo/editor now have the recorded Vortex hash.
No motion edits or recompression were performed. In-game ultimate testing remains pending.

`chr/c0000.anibnd.dcx` contains the event timelines. The separate
`chr/c0000_a0x.anibnd.dcx` supplies motion assets relevant here.

| Copy | Members | SHA-256 |
| --- | --- | --- |
| Repo and DSAnimStudio packed a0x | 575 | `5b76b09a5f8e61f1b4d12a2c6553ba44183572add059537cad2b57edd99f4861` |
| Vortex and live packed a0x | 576 | `c94e2a3dd54cab4e4bc93624e1302e0ea1abc3863b94fc232c53ee5048752131` |

The additional member is `a984_032400.hkx`, binder ID 1984032400, 50,404 bytes,
SHA-256 `4fb867da18d718af1863b340fb308cb42c7d245a41ef78f09a7756996b5fe488`.
All shared member payloads and their IDs/names/flags/compression types match. Compared
binder header metadata matches and no member was removed.

The main binder already contains a984 timeline 32400. Its `ImportsHKX=false` means
the stored import-source number is not an enabled fallback motion. Having the
timeline does not supply the missing body movement. The current installation has
both; copying the older a0x over it removes the additional motion. This is separate
from the HKS buff gate, and presence alone does not prove a successful in-game ultimate.

Proposed correction, high confidence: back up all four copies and any active loose
a0x source/project, recheck hashes, then accept the exact Vortex/live a0x bytes into
repo and DSAnimStudio. No motion editing or recompression is necessary for this
one-member difference. Reconcile loose sources before any subsequent rebuild.
The existing main-animation VBS copies c0000.anibnd, not a0x; this needs an explicit
a0x handoff. Test a clean install built from the accepted sources, not only the old
working game folder. Add a preservation assertion for this member to future builds.

## 2. Restore Crusade Insignia's passive connection

Accessory 8050 references missing SpEffect 20380500 in both current repo and Smithbox.
Vanilla regulation version 11711000 contains 20380500, with
`applyIdOnGetSoul=20380501`. The latter effect exists in Sovereign and has a 20-second
duration. Preserve its intentional `iconId=-1`; do not overwrite it with vanilla's icon.

Proposed correction, high confidence: add only the exact current-vanilla 20380500 row
through Smithbox or a separately qualified parameter writer. Compare all unrelated
rows/cells and retain editor row names. Synchronize accepted authoring and runtime
outputs through the reviewed handoff. Test equip, kill activation, expiry, repeated
kills, removal, and intended icon presentation. A whole-regulation replacement is
unnecessary and would risk custom content.

## 3. Align Black Scaled Armor conversion with the Rykard encounter

Current common event 5750020 initializes 5750021 only when neither goods 194 nor
8151 is owned. The child requires 8151. Starting after rune acquisition therefore
misses the listener. The parent also uses sequential armor-effect waits, which do
not by themselves prove the entire set is still equipped at conversion time.

Author-confirmed decisions (2026-09-10): both phases of the Rykard encounter qualify
for the proposed death-triggered conversion, including the God-Devouring Serpent
phase. Defeating Rykard while meeting the equipment requirement also qualifies.
Characters who already defeated Rykard before qualifying have missed the opportunity;
there is no retroactive conversion based on owning his rune. These decisions supersede
the earlier proposal to keep a restored-rune listener active for later equipment.

Proposed implementation, not yet applied: track a qualifying active encounter and
capture equipment eligibility at death or victory. Preserve a pending conversion
across the death/reload transition, then perform inventory changes when safe. A
completed-defeat guard must still allow a pending conversion earned in that fight.
Preserve the other color paths and prevent competing workers consuming the same item.

Confirmed for implementation: one original Scaled piece equipped is sufficient.
Convert all carried original pieces one-for-one, preserving duplicate quantities
and the altered-body variant. Exclude storage. Coordinate other color workers so
they cannot consume the same original during the pending conversion.

Test death in each phase, victory, already-defeated saves, no qualifying equipment,
equipment changes, duplicates, altered body, death/reload recovery, repeated loads and
competing color eligibility. Static confidence is high that the current listener does
not implement this design; a replacement still requires event review and game tests.
Inventory and visuals are separate checks; an event fix does not prove textures render
correctly.

## 4. Obliterator: separate missing connections from intended requirements

Weapon 23085000 has no connected acquisition entry in the inspected lots, shops and
recipes. Goods 8115/8116 are not a completed ore quest. A scripted grant elsewhere
has not been exhaustively disproved; no acquisition guide is verified.

Behavior 300000867 has `refType=0, refId=-1`: no attack row is selected for that extra
one-handed path. Adjacent 300000868 instead selects bullet 210471008, and 300000869
selects bullet 4620221. Decide whether the one-handed addition should be melee,
projectile or intentionally absent, and verify the triggering timeline. Copying the
two-handed bullet merely to eliminate -1 is not a justified fix.

`ModUltimateAttackConditions` explicitly rejects weapon category 984 without state
7750 and dispatches alternate start/end events. Void Eye effect 1626770 supplies that
state for 60 seconds. The outer ultimate gate additionally checks readiness 7588,
window 7551, absence of cooldown 7587, input duration and the right-hand/two-handed
branch. The ultimate timeline refreshes Void Eye.

Retain the intended buff requirement for the beam and the existing general unbuffed
fallback. Follow-up inspection found standard graph selectors for a984_032610 and
a984_032615, matching TAE records importing a031/32400, and attack events. Current
and Backup 2 HKS helpers are identical. Returning false rejects the buffed dispatch;
it does not mean that no alternative attack was requested. Do not remove the guard.
The exact attack lookup, selector and back-to-back start/end dispatch still need a
game test. Test fresh equip, before/after buff, expiry, insufficient FP, controller
configuration, damage and cooldown before changing the fallback.

## 5. Missing Claw and Dragonbolt gameplay effects

These are missing **SpEffectParam gameplay rows**, not missing FXR visual files.
The earlier FXR recovery cannot fill them in.

| Timeline | Missing effects requested | Historical evidence |
| --- | --- | --- |
| a00 / 50510, Blasphemous Claw | 1626616-1626620 around 0.133 s; 1626621 around 0.267 s | Backup 1 supplies 1626616-1626619 and their intermediate row 1626600; both inspected backups lack 1626620/1626621 |
| a544 / 145010, Betrayer's Dragonbolt | 1626823 around 0.667 s | Neither inspected backup supplies that row |

Old Claw rows 1626616-1626619 condition on states 7286-7289 and invoke 1626600;
1626600 conditionally invokes 1626601 under state 7705. Current HKS independently
applies 1626601 and 1626624 in its Endure/Claw handling. A follow-up scan found no
direct type-66/67 application of 1626625 in the exported main timelines; that row's
existence is not evidence of this timeline using it. Establish intended overlap
before restoring any old conditional chain.

Correction to the retained scratch REPORT: it says 1626601 changed semantics. This
review compared every exported cell against Backup 1 and found **no cell differences**
for that row. That sentence should not be used as evidence against restoring it.
The missing intermediate row, incomplete historical coverage and interaction with
current HKS still make wholesale restoration unqualified.

Dragonbolt's player Magic 2006910 deliberately selects self-buff 1626741 instead of
vanilla's bullet, alongside custom requirements, costs and visuals. The populated
bullet chain 210691000 -> 210691001 and aura rows 1626730/1626731 do not prove that
the current player cast uses them: the inspected a544/145010 has no type-2 bullet
event. Preserve the redesign. Missing 1626823 is unresolved additional behavior,
not evidence that the whole incantation should revert to vanilla. The self-buff
row alone also does not substantiate the older description's +15 SP/s claim.

The three inspected target timelines, including the ultimate, match Backup 2, whose
regulation already lacks these effects. These are pre-existing gaps, not newly lost
rows from the recent animation merge.

Investigation/fix sequence:

1. Describe and observe the intended Claw parry/counter/backstep and Dragonbolt
   self/ally/enemy behavior, using recorded current source/runtime hashes.
2. Trace each event's timing, application target, downstream state checks and effect
   chains. Inspect further historical parameter snapshots if available.
3. Restore a proven historical chain, implement a specified new effect, or remove a
   demonstrated obsolete timeline event. Do not remap to adjacent IDs or create empty rows.
4. Change one path at a time, rebuild with the qualified TAE/parameter routes, compare
   untouched events/rows and test timing, stacking, duration and interruption.

Confidence: high that the references are unresolved; low in any guessed replacement.

## Hewg and Fallingstar acquisition: agreed design

Hewg's duty from Marika is to forge a weapon capable of killing a god. He stays as
Roundtable Hold burns. His god-slaying/masterpiece dialogue becomes available after
Godskin Duo; after Maliketh he forgets the Tarnished and Roderika but still offers
smithing. Vanilla does not award a bespoke Fallingstar Obliterator from this story.
See [Hewg's quest and dialogue](https://eldenring.wiki.gg/wiki/Hewg).
Integrating the custom weapon is a Sovereign extension of that story.

Agreed direction: defeat the three base-game Fallingstar Beasts and adapt Hewg's
existing **About the god-slaying weapon** conversation into **Forge the Fallingstar
Obliterator** when eligible. The author's clarification requires Godskin Duo plus
all three base-game beasts and the full masterpiece speech at the voiced handoff.
Reserve that main speech for forging instead of playing it before the beast requirement
is met. Preserve the beasts' normal rewards, including the Beast Jaw.
Use their existing defeat flags rather than introducing the earlier ore subsystem;
already-completed beast kills count. The DLC beast is not required.

| Encounter | Extracted event map | Defeat flag |
| --- | --- | --- |
| Sellia Crystal Tunnel | m32_08_00_00 | 32080800 |
| Altus Plateau | m60_41_50_00 | 1041500800 |
| Full-Grown Fallingstar Beast, Mt. Gelmir | m60_36_54_00 | 1036540800 |
| DLC Hinterland encounter | m61_52_48_00 | 2052480800 |

These are progression flags, not NPC parameter IDs. Sellia's death event sets its
flag; the other extracted constructors pass their flags to death helper 90005860.
The extraction receipt records source archive/header and file hashes; its extracted
file hashes were rechecked here. This is the recorded installed baseline, not a new
full-game extraction in this review. Revalidate before implementation if the game changes.

Agreed conversation and presentation:

1. Before eligibility, preserve unrelated ordinary dialogue and its heard-state rules;
   withhold the main masterpiece speech until Godskin Duo and all three beasts are dead.
2. Once eligible and unclaimed, offer the forging option in place of the masterpiece
   topic. Hearing the original topic earlier must not prevent this option appearing.
3. Close the menu, fade to black, pause briefly with smithing sounds, then fade back
   to Hewg. Start with roughly one-second fades; exact sound/timing is a test choice.
4. Before memory loss, play the full existing masterpiece conversation with matching
   original subtitles and award the weapon. After memory loss, play only "Use my
   masterpiece to slay a god." and award it through the surviving smithing menu.
   This latest agreement replaces both the full late speech and silent late claim
   proposals. The old heard flag is not proof of weapon collection.
5. Mark the masterpiece conversation heard and hide forging after a successful claim.
   Preserve the separate later farewell, Roderika branches and memory-loss progression.

Verified integration anchors from the retained current-game extraction:

- Binder `m11_10_00_00.talkesdbnd.dcx`, Hewg ESD `t213001110`, main menu helper x39.
- Masterpiece helper x58 uses story flag 9114 in stage 3226; menu 13 uses text 22130012.
  Handler x59 plays TalkParam 21313000 and sets heard flag 11109230.
- TalkParam 21313000 maps to message/voice 213130000, the existing masterpiece line.
  Its conversation continues with his purpose, Marika and looking after Roderika.
- Separate farewell menu 14 plays TalkParam 21313100 and sets 11109231. Do not consume
  that flag merely because forging completed. The exported nine-clip audio preview
  combines both conversations for listening; it is not one mandatory handoff speech.
- EMEVD `FadeToBlack` (2004[77]) controls opacity, duration and player freezing. Repo
  event 12032859 provides a fade/reset example. Coordinate dialogue and event states;
  restore picture and control on completion and interruption. Do not copy its warp.

The first four lines and separate farewell were exported as WAVs to the Desktop
folder `Hewg - God-slaying weapon`. Routing and extraction evidence is retained under
`.codex-temp/hewg-audio-20260910/`; no custom voice recording is required for this design.

Implementation requirements:

- The [ownership follow-up](FILE-OWNERSHIP-REVIEW.md) confirmed that x58's farewell
  depends on 11109230 and x39 calls x58 only in stage 3226. Preserve farewell access
  independently when withholding the main speech. The post-Maliketh policy cannot
  be solved by adding boss conditions to the old topic alone.
- A named hint/menu explains the three prerequisites. Check existing flags on load
  and interaction, not only future death transitions.
- Recheck the inspected Hewg ESD against the selected current binder, qualify a no-change
  rebuild, and preserve current smithing and Roderika dialogue branches. Do not assume
  the previously qualified Grace ESD source can be applied unchanged to Hewg.
- Grant 23085000 via a dedicated verified item lot and unused per-journey claim flag.
  The author confirmed one reward per journey, requiring that journey's four boss
  victories again. Do not use weapon possession alone,
  because storage, sale, discard or trade can make that ambiguous. Reconcile interrupted
  payout using the established item-lot collection mechanism and test it.
- Keep reward ownership separate from 11109230/11109231. Use the complete masterpiece
  TalkParam chain before memory loss and qualify a single-line playback afterward.
  Preserve the separate farewell rather than combining both speeches. Do not reset
  Hewg's story flags to enable the late reward.
- Test all kill orders, pre-completed saves, before/after Godskin Duo and Maliketh,
  quit/reload around payout, inventory/storage cases and the chosen NG+ policy.
- Test original-topic heard/unheard, the full handoff, withheld early speech, untouched farewell,
  repeated menu selection, fade interruption and guaranteed restoration of control.

Tools: DarkScript for any global eligibility/reward event, ESDTool for Hewg, qualified
FMG editing for menu text, Smithbox/qualified parameter writing for the item lot, and
WitchyBND for containers. No new ore assets or fabricated quest/boss IDs are necessary.

## Recommended implementation order

Preserve the extra motion; restore Crusade's vanilla row; repair the armor listener;
decide and implement acquisition at Hewg; resolve the one-handed payload and document
the buffed ultimate; investigate Claw/Dragonbolt before replacing their effects.
Each gameplay change gets its own before/after evidence and focused game test.
Update the manual matrix with these specific scenarios when implementing them;
do not mark any current pending row Passed based on this investigation.
