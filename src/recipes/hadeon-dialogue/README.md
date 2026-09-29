Hadeon dialogue subtitles
=========================

The current first-entrance recording changes TalkMsg 999800010 to "Long have I
kept mine oath." The three `entrance-menu*.patch.json` files guard that exact
one-entry change in the base, DLC01 and DLC02 English binders. Build each against
its matching current binder through `format_workflow.py unpack` and `build
--patch`; the native carrier and TalkParam name candidate is in the
[death sound carrier recipe](../hadeon-dialogue-proxy/README.md). The ESD update
distance is now 100 metres, paired with the map event's native
`SetCharacterTalkRange` setting. Arena-distance behavior still needs a game test.

This recipe adds native subtitle rows for the fifteen new Hadeon voice lines.
The [audio manifest](../../audio/hadeon/dialogue-manifest.json) owns their
roster order, TalkParam/TalkMsg/voice IDs and cue timings. The five accepted
first-entrance rows 99980000-99980004 and text IDs 999800000-999800040 are
retained. Their TalkParam row names formerly described an old draft; the
guarded regulation candidate corrects only those owned names to the current
text. Hadeon's map TalkID remains 999801800; this recipe does not edit the map.

Every line has a contiguous TalkParam block so one `TalkToPlayer` call can
advance its phrases. Each row points both voice fields to an embedded silent
Wwise carrier whose exact duration controls the transition. The full spoken
recording plays separately from the map event. TalkParam `isForceDisp` is 0;
the native timeout remains -1. The ESD reads exactly one selection bit in
1055425200-1055425215 while active flag 1055422946 is on. The map event must
clear active for at least an ESD update frame before preempting a line.


Guarded regulation candidate
----------------------------

Run against the reviewed current regulation, into a new scratch directory:

```powershell
dotnet run --project src/recipes/hadeon-dialogue/Dialogue.csproj '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- mod/regulation.bin .codex-temp/hadeon-dialogue/all-lines-144 'Z:/Modding/Elden Ring/Tools/Smithbox' src/audio/hadeon/dialogue-manifest.json
```

The builder rejects occupied new IDs and unexpected accepted voice/message
fields. It adds 28 TalkParam rows and checks the independently decrypted
candidate against the intended table. Other parameter members, binder metadata
and every unrelated decoded row are preserved. The candidate is a TalkParam
overlay only; accept it against the exact recorded input hash.


English text and talk ESD
-------------------------

The three `menu*.msgbnd.dcx.patch.json` files declare the same 28 new
TalkMsg entries for base, DLC01 and DLC02 English menu binders. They use
`beforeMissing: true` and `before: null`, distinguishing absence from an
existing null value. Apply each through `tools/format_workflow.py unpack`
then `build --receipt ... --patch ...` against its matching current binder.
The qualified binary-FMG route validates all decoded entries, ordering,
metadata and other binder members; do not use recursive XML repacking.

The ESD source `src/talk/m18_00_00_00-talkesdbnd-dcx/t999801800.py`
selects a line by the active roster bit, starts one native conversation, then
reports conversation end to Havok to preserve combat movement. Combat gate
1055422947 may release before the first entrance ends; the ESD keeps its
subtitle sequence alive until actual talk completion or active cancellation.
It requires the active flag to clear before rearming and uses
`SetUpdateDistance(70)`. Compile through `format_workflow.py build-dialogue`
with the current m18 binder as template, preserving the untouched native
t706021800 member and binder metadata. The compiled candidate was separately
decompiled to confirm all sixteen TalkToPlayer branches.

Death requests start at Hadeon HP zero while his actor is still loaded. Native
talk continuation after CharacterDead has not been established in-game; both
death variants' subtitles and full audio tails require a gameplay test.
