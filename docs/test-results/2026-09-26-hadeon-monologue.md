Hadeon entrance monologue calibration
====================================

Version 1.4.0 was deployed with verified live files. The recording reviewed below
revealed subtitle and combat-handoff failures; 1.4.1 corrected the dialogue ESD.
The 1.4.2 follow-up below replaces the recording and adds cue-time retreat
validation. Both changes require game testing. The author confirmed the earlier 1.3.9
custom audio test was audible.


Behavior and ownership
----------------------

The author supplied the revised `hadeon-entrance-first.wav` on the Desktop and
specified "to my blade" at 17.1 seconds. The full recording lasts approximately
21.269 seconds including its existing reverb. Audio conversion preserves timing,
retains the untouched source, and removes the diagnostic +3.5 dB bank gain.
Listener-relative PositionAndOrientation and the original attenuation are restored.
See the [audio source recipe](../../src/audio/hadeon/README.md).

Every fresh encounter plays the monologue during this test, including a return
after true retreat. There is no persistent once-per-journey flag. Mid-fight
reposition/fall recovery does not replay it. The final policy can later use a
saved journey receipt; no new game is required to test this version with a
living Hadeon.

Map events 5750311 and 5750312 separate combat activation from playback:

- On appearance, Hadeon remains idle and music stays stopped. The existing
  summon effects retain their timings. Flag 1055422947 requests and gates the
  monologue; 1055422946 signals active playback/subtitles.
- At 17.1 seconds, or on an earlier hit, enable AI, show the boss bar, start
  BGM 472000 and set the existing combat-presence flag. A hit does not end speech.
- Voice runs through the tail; the playback worker ends it at 21.28 seconds.
  Defeat, confirmed player death and actual retreat cancel it sooner. Beginner
  rescue's transient zero-HP frames do not count as confirmed death.
- True retreat clears both dialogue flags and keeps Hadeon visible and inert.
  Valid reentry requests the opening again. Cleanup gets a frame before the
  next request can start. Existing fall recovery passes the no-intro argument.

The bank retains voice ID 999800001 and adds Play_v999800002 as an alias for
the existing sound-specific stop action. This allows event cleanup through
PlaySE without replacing global voice or music banks.

Native subtitles use Hadeon's map TalkID 999801800 and ESD t999801800. Five
TalkParam rows 99980000-99980004 reference TalkMsg entries
999800000/010/020/030/040. Each has a real silent voice cue 999800010-999800014
in the same bank; the audible monologue remains a separate continuous voice.
This gives the native dialogue system bounded voice durations instead of relying
on undocumented timing for voiceId=-1. Subtitle timing is 0, 2.75, 7.0, 12.0
and 17.1 seconds, clearing near 18.7 seconds while the recorded reverb continues.
The text respects the game's subtitle setting. The original Graveyard tutorial
ESD remains unchanged, and additions to each of the three English menu binders
preserve their existing text.


Verification
------------

Repo and saved editor event files matched before edits (28 inspected files).
Unchanged event compilation passed. A native scan checked 598 mod/retained
vanilla event files and 194 regulation members, including flag-range uses,
before allocating temporary flags 1055422946/1055422947 and event IDs
5750311/5750312. No collisions were found.

The source-event simulator in `tools/tests/test-hadeon-lighting.mjs` exercises
the timed cue, early hit without audio interruption, tail completion, rescue,
confirmed death, true retreat/reentry, canceled retreat, defeat and guest
exclusion. Existing lighting, aid and retreat regressions remain covered.
These are logic simulations, not engine playback evidence.

The final event build preserves all 74 unrelated events and file metadata;
existing changes are confined to 5750300/5750302/5750303/5750304 and the two new
workers. The original events retain their relative order. Six talk binders
passed unchanged-source qualification, including a byte-identical rebuild of
the new m18 binder. All 33 sound-bank objects and six embedded WEMs matched
independent readback. The original full voice and five silent cue durations
match their sources. Parameter/map readback preserves every unrelated table,
row and map part. Each menu binder differs only by five added TalkMsg entries.

Guarded editor handoffs:

- Params: `.sovereign/handoffs/15622b0fef9f431e945b28be3c2116d8/receipt.json`.
- Maps: `.sovereign/handoffs/594e6d301417407081d77ac653119796/receipt.json`.
- Text and recovered FMG snapshots: `.sovereign/handoffs/42f4aed6f2a2442089808119229b6626/receipt.json`.
- Talk: `.sovereign/handoffs/f4b64379b2e6445db52fe901c3786cd1/receipt.json`.
- Events: `.sovereign/handoffs/3b3abdebd74c4bfb95fc7e24b4f51487/receipt.json`.

The full talk handoff also synchronized one reviewed trailing blank-line
difference in Hewg's DSL; his compiled dialogue did not change.

Backups before runtime changes are in
`.sovereign/backups/hadeon-monologue-140/`. Native event candidate and flag
evidence are under `.codex-temp/hadeon-monologue-events/`; sound validation is
under `.codex-temp/hadeon-monologue-audio/` and subtitle candidates under
`.codex-temp/hadeon-dialogue/`.

Game acceptance must check audibility and position around the arena, five native
subtitle cues, no music before the final phrase, immediate retaliation on a hit
without truncating voice, and death/retreat/reload cleanup. Exact audible music
onset may require an offset for the BGM's own lead-in; 17.1 seconds is currently
the event command time. No gameplay result is inferred from compilation.


Deployment
----------

Prepared complete main package:
`.vdb/prepared/e43282194f864e17815fddb6fc4b2243/receipt.json`.
Compared with 1.3.9, seven files changed (bank, map event, map, regulation and
three menu binders), one m18 talk binder was added, and all other 67 package
files were preserved. There are 75 files total, including the preserved
external DLL. No texture package change was needed.

Protocol-3 finalization completed:
`.vdb/finalizations/69a07976400c43c3bbf7edf408af84f3/receipt.json`.
Request `812dd945-1a8a-4ac4-b236-949ae5a0d9c3`, build
`a4a8a921fcf3600a402b9f7d`, version 1.4.0. All eight changed/added files were
independently hashed against the live Game directory after finalization and
matched the accepted repository bytes. No new profile or save was created.

Final bank SHA-256:
`D1B4177695CDBB52B1E3920D7EF6C63FECFC0C3FB3AAF4EE613EB160F6347B73`.
Updated recording SHA-256:
`22FB3A998D78A11EA98289C84BB06D51FFF4527C07D2311CAC913656468C0BAC`.
Native bank evidence is `revision3/validation.json` under the audio scratch
folder. The desktop input still matched the preserved original at acceptance.


Recording review and 1.4.1 correction
------------------------------------

The author supplied `Z:\Shadowplay\Elden Ring\Elden Ring 2026.09.26 - 21.40.54.01.mp4`.
Frame inspection shows subtitle lines one, three and five, with the second and
fourth missing. The boss bar appears at the final phrase, but Hadeon remains
stationary afterward. The installed event and talk binders still matched 1.4.0.
The bar and AI-enable commands share the same event branch, supporting a
conversation-behavior problem rather than a failed 17.1-second timer. The exact
engine cause remains a hypothesis until the corrected build is tested.

The original ESD issued five timed TalkToPlayer calls and cleared progress
between them. Native dialogue plays consecutive TalkParam rows from one call;
the retained t801291205 source demonstrates this for rows 80120000-80120002.
The native nonblocking pattern in
[Melina's helper x79](../../src/talk/m00_00_00_00-talkesdbnd-dcx/t000003000.py)
also reports conversation end to Havok immediately after TalkToPlayer while
waiting for actual voice completion separately.

The corrected [Hadeon ESD](../../src/talk/m18_00_00_00-talkesdbnd-dcx/t999801800.py)
uses one call for rows 99980000-99980004. The existing silent voice durations
now drive native subtitle advancement. It releases conversation behavior after
the start and again when combat gate 1055422947 clears, without clearing the
subtitle sequence. Actual talk completion or playback cancellation controls
cleanup, and playback flag 1055422946 must clear before rearming. Only a still
active, canceled conversation receives ForceEndTalk. The map event continues
to own the full audible recording, 17.1-second cue and early-hit retaliation.

Only the m18 talk binder changes at runtime. The candidate's independent native
comparison preserves binder metadata, the original t706021800 member and all
Hadeon ESD metadata; only state group 1 changes. Readback shows one TalkToPlayer
command, the start/combat/cleanup release commands, and conditional cancellation.
All six owned talk binders pass unchanged rebuild qualification with matching
loose ESD companions. The existing Hadeon event simulation also passes; it does
not model native conversation behavior or prove this gameplay fix.

- Candidate: `.codex-temp/dialogue-builds/1790484605935980900/receipt.json`.
- Qualification: `.codex-temp/talk-qualifications/1790484756034006500/receipt.json`.
- Completed editor handoff (three files):
  `.sovereign/handoffs/533d60c6342d4c5bb47ba30b1c56d359/receipt.json`.
- Recovery: `.sovereign/backups/hadeon-dialogue-141/`.
- Corrected binder SHA-256:
  `5E3A7ED96DCD36FAE9E09593A4D268D5869D817FF6AE45201B60C45BD711AF31`.

Retest an uninterrupted entrance and an early hit during line one. Confirm all
five subtitles, continued movement/attacks during later lines, music at the
combat cue, and cancellation/reentry. Native transition overhead may require
further subtitle timing calibration; 1.4.1 is not marked game-accepted.

The complete 1.4.1 main package contains 75 files. Comparison with 1.4.0 shows
only the m18 talk binder changed; the other 74 files are byte-identical,
including the external DLL and sound bank. Preparation receipt:
`.vdb/prepared/11cd4fcb09754d0e91fb9dd88f424e3a/receipt.json`.
Finalization request `f8898e88-d487-4e39-9f52-9b0b90540f31`, build
`b57b9cec0c11b0a524d3400d`, is tracked by
`.vdb/finalizations/34917079f3d64e4bb4df06a4c3d4e36c/receipt.json`.
Finalization completed on the existing profile SkC-QjDMc, with the main package
enabled and deployment verified with no differences. The live Game m18 talk
binder independently matches the corrected SHA-256 above. Repository checks,
version consistency and scoped document link/whitespace checks also passed.


Revised opening and cue-time reset, 1.4.2
----------------------------------------

The author replaced the Desktop recording and specified the final phrase at
13 seconds. Subtitles now read:

> Begone from this place. Ancient is mine oath.
> Older still, the hunger here bound.
> His whispers draw thee hither... to my blade.

The period after the first sentence is explicitly requested. The three English
menu binders change only the first four existing Hadeon TalkMsg entries; the
final phrase is unchanged. Full native decoded comparison preserves all other
text and binder metadata. Guarded text handoff:
`.sovereign/handoffs/1615ef3ecfba4630a5a2ddc30aa43350/receipt.json`.

The untouched original recording has SHA-256
`4E92A5942D2FD53267DA8A4CC23AF082126B688F3AF0347ADA2DB4F23F26E424`.
It contains 752,445 mono float samples at 44.1 kHz, about 17.062 seconds including
reverb. Conversion retains the prior -1 dB headroom and positioned voice routing.
Intended subtitle starts are 0, 2.75, 5.4, 9.03 and 13 seconds; intermediate
boundaries are estimates from recording pauses and require calibration. The
five silent carriers last 2.75, 2.65, 3.63, 3.97 and 2 seconds. The native
single-conversation ESD from 1.4.1 is unchanged.

The revised bank keeps its IDs, BKHD 135, 33 HIRC objects and 13 events. Only
embedded media sizes differ in its source graph; an independent readback checks
the complete graph and all six embedded WEMs. Bank SHA-256:
`C72DC8A3B10F1C73A04645922FCAE2D310EEF0A435DA3374985B9A16B49BBC38`.
Evidence is `.codex-temp/hadeon-monologue-audio/revision4/validation.json`.

At 13 seconds or an earlier hit, the event checks that the player is in the
Graveyard map, inside the room and outside its excluded/below-arena regions.
An invalid position requests the existing retreat controller to reset Hadeon
immediately, cancel speech/subtitles and keep AI/music off. Temporary reset
flag 1055422948 lets that controller consume the request even if its original
startup condition never opened. Allocation was checked against 598 native/mod
event files, including ranges, and 194 regulation members without collisions.
Normal combat retreat retains its six-second grace period. Confirmed death and
boss defeat still take precedence, while brief rescued zero-HP frames do not
count as a departure. Playback cleanup is scheduled at 17.08 seconds.

Testing still replays the full opening on a valid return. The author's later
repeat-dialogue policy is recorded in [the lore guide](../hadeon-lore.md), not
enabled without the repeat recordings. Retest leaving or dropping just before
13 seconds, returning before the cue, rapid reentry, normal early-hit combat,
all five subtitles and the complete voice tail.

Source simulations pass the 13-second cue, valid early hit, transient rescued
zero HP, every excluded region, late exit/fall, off-map state, delayed retreat
controller initialization, cancellation and reentry. Native event comparison
changes only 5750300/5750303/5750311/5750312, preserving the other 76 events,
their order and metadata. All other runtime event builds are equivalent.
Candidate: `.codex-temp/event-builds/1790489330375905000/receipt.json`.
Flag evidence: `.codex-temp/hadeon-reset-142/flag-scan.json`.
Editor handoff: `.sovereign/handoffs/472051431d564c54915a73d8729b70b7/receipt.json`.
The reset runs immediately; a 0.1-second cleanup interval precedes eligibility
for another opening. A valid early hit has already begun combat, so a later
departure uses normal combat retreat rather than a second check at 13 seconds.

Recovery copies are under `.sovereign/backups/hadeon-audio-142/`,
`hadeon-reset-142/`, `hadeon-text-142/` and `hadeon-runtime-142/` in the same
backups directory. Repository preparation checks and version consistency pass;
these and the native/source checks do not establish gameplay acceptance.

Prepared main package:
`.vdb/prepared/b436aa5a69594def8ce782092ac2e9ce/receipt.json`.
Compared with 1.4.1, only the map event, three English menu binders and sound
bank change; the other 70 package files are preserved, with no additions or
removals. Finalization request `805c43ad-f86c-45c7-9a0d-ed10616e097a`, build
`9d82149969cdebdfc6126663`, is recorded in
`.vdb/finalizations/797de55fcba7444c81293dd2e3b5af2e/receipt.json`.
Finalization completed on existing profile SkC-QjDMc with deployment verified
and no differences. Independent hashes of all five changed live Game files
match the accepted 1.4.2 package. The in-game reset/subtitle retest remains pending.
