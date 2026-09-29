Hadeon dialogue audio
=====================

The current candidate divides the author's 17.270833-second first-entrance wet
WAV at exactly 13.10 seconds, after "hither" and before "to my blade." The
existing `Play_v999800001` / `Play_v999800002` pair plays and stops the first
13.10 seconds. `Play_v999800003` / `Play_v999800004` plays and stops the final
4.170833 seconds, posted at 13.10 seconds on the same event clock. The two
48 kHz PCM segments concatenate byte-for-byte to the original converted voice,
preserving cadence and recorded reverb. The dry recording falls silent by
12.60 seconds and the final phrase begins around 13.25 seconds. The five
subtitle starts remain 0, 2.75, 5.55, 9.15 and 13.10 seconds, with the final
cue ending at 14.80. The shared mixer still adds 2 dB with its original spatial
routing. This split is included in the deployed 1.7.2 runtime; in-game positional audio
acceptance remains pending.

Version 1.5.6 adds the one-second nearest-clear teleport on repeat encounters,
three-loss eligibility for the another-defeat entrance and thousand-times kill
line, and silent fatal falls below the arena. Fatal falls still advance aid;
line history changes only when a line starts. It replaces the need-another and
whisper recordings with worthier and another-falls, retaining all audio/subtitle
IDs. The author confirms the 1.5.5 private waiting AI works. See the
[follow-up verification](../../../docs/test-results/2026-09-27-hadeon-followup-156.md).

Version 1.5.5 replaces the disabled-AI speech hold with a private running-AI
waiting goal. The first entrance releases at 14.6 seconds after actual voice
start, after "blade", following the nearest-clear opening teleport. An early
hit releases immediately without the delayed teleport. Repeat entrances engage
immediately and retain the shared speech delay/range gate. Subtitles, recordings,
fall recovery, progressive aid and load-reset testing are unchanged. See the
[waiting-state implementation](../../../docs/test-results/2026-09-27-hadeon-wait-155.md).

Version 1.5.4 temporarily bypasses the monologue's AI hold. Hadeon is revealed
with AI enabled, and valid entrance admission starts combat before the voice's
0.7-second settling and 12-metre proximity gates. Speech and subtitles continue
independently. The already-started combat flag skips the delayed opening teleport.
Eight-point fall recovery and the load-reset test remain unchanged. See the
[immediate-combat test](../../../docs/test-results/2026-09-27-hadeon-immediate-154.md).

Version 1.5.3 expands the opening teleport to eight destinations, including the
unchanged author-placed points 18002381 and 18002382. Fall recovery now uses the
same generated nearest-clear selector and faces the player after arrival. Only
fall recovery retains the existing one-time 5% HP penalty. See the
[eight-point update](../../../docs/test-results/2026-09-27-hadeon-eight-153.md).

Version 1.5.2 replaces the combat-AI diagnostic trials with a teleport after
"blade" finishes, approximately 14.6 seconds from actual first-monologue playback.
Hadeon chooses the nearest of six existing arena destinations with 2.5 metres of
player clearance, faces the player, then enables combat and music. Early-hit
engagement skips the delayed teleport. The restored subtitles remain enabled.
See the [teleport implementation](../../../docs/test-results/2026-09-27-hadeon-teleport-152.md).

Version 1.4.9 replaced the every-entrance first-line override with a temporary
load-reset test. Normal first/repeat entrance selection operates within a session;
the death-reload marker preserves earned aid on the next reload. See the
[load-reset record](../../../docs/test-results/2026-09-27-hadeon-load-reset-149.md)
for the heuristic's limitations and removal procedure.

Version 1.4.8 gates every entrance voice request (first monologue and all four
repeat variants) on being within 12 metres of Hadeon, after the existing minimum
0.7-second settling delay. Radius is checked only before playback; the first-monologue combat cue remains
anchored to actual audio start (14.6 seconds in 1.5.2). Other dialogue
triggers keep their existing timing. The radius is for calibration, not a verified
subtitle boundary. Restoring the ESD does not establish that distance-dependent
subtitle playback is resolved.

This source builds `cs_c9998.bnk` with all sixteen author-recorded Hadeon
lines and silent subtitle carriers. The 32 original wet and dry WAVs in
`recordings/` remain untouched. Playback uses only the unsuffixed wet WAVs;
`prepare.py` converts those to 48 kHz mono PCM16 with a 1 dB gain reduction.
The bank's shared ActorMixer then adds 2 dB of voice gain; it does not change
the converted WAVs or embedded WEM media. The converted voice peaks range
from about -1.0 to -2.3 dBFS before mixer gain. Each line keeps its full
original length, including the reverb tail; the two first-entrance segments
together reproduce its full original length.

`dialogue-manifest.json` is the shared roster and timing contract. Index 0
retains the first entrance's accepted voice, stop alias, five TalkParam rows,
five TalkMsg entries and 13-second final subtitle cue. Indices 1-15 are new.
The map event owns audible `PlaySE` voice and preemption. Talk ESD
`t999801800.py` watches active flag 1055422946 and selector flags
1055425200-1055425215, then starts one native TalkParam conversation from the
selected line's first row. A new line requires at least one ESD update with
the active flag off between requests. Sound bank 9998 uses BKHD version 135.

Version 1.4.6 tracks the last started line independently for each
four-line repeat pool. Saved flags 1055420940-1055420943 record entrance history,
1055420944-1055420947 half-health, and 1055420948-1055420951 player-killed.
The next draw has three equally likely alternatives; first-time lines do not
consume repeat history, and requests discarded before playback do not change it.
Interrupted lines count once they start. See
[verification](../../../docs/test-results/2026-09-27-hadeon-no-repeat.md).

| Index | Line | Duration (s) | Full voice | Stop alias | TalkParam start | TalkMsg start | Subtitle starts (s) |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | First entrance, two segments | 13.100 + 4.171 | 999800001 + 999800003 | 999800002 + 999800004 | 99980000 | 999800000 | 0, 2.75, 5.55, 9.15, 13.10 |
| 1 | Unyielding entrance | 9.985 | 999800100 | 999800200 | 99980110 | 999801100 | 0, 2.85, 4.25 |
| 2 | Promise entrance | 4.895 | 999800101 | 999800201 | 99980120 | 999801200 | 0 |
| 3 | Another defeat entrance | 8.160 | 999800102 | 999800202 | 99980130 | 999801300 | 0, 3.70 |
| 4 | Hunger entrance | 8.542 | 999800103 | 999800203 | 99980140 | 999801400 | 0, 4.15 |
| 5 | First half-health | 10.758 | 999800104 | 999800204 | 99980150 | 999801500 | 0, 2.65, 5.35 |
| 6 | Hunger half-health | 8.090 | 999800105 | 999800205 | 99980160 | 999801600 | 0, 2.70 |
| 7 | Surrendered half-health | 5.772 | 999800106 | 999800206 | 99980170 | 999801700 | 0, 2.35 |
| 8 | Dominion half-health | 6.054 | 999800107 | 999800207 | 99980180 | 999801800 | 0 |
| 9 | Oath half-health | 6.137 | 999800108 | 999800208 | 99980190 | 999801900 | 0 |
| 10 | Thousand times player-killed | 6.447 | 999800109 | 999800209 | 99980200 | 999802000 | 0, 2.50 |
| 11 | Worthier player-killed | 5.747 | 999800110 | 999800210 | 99980210 | 999802100 | 0 |
| 12 | Chosen player-killed | 3.285 | 999800111 | 999800211 | 99980220 | 999802200 | 0 |
| 13 | Another falls player-killed | 5.552 | 999800112 | 999800212 | 99980230 | 999802300 | 0 |
| 14 | Hadeon death | 17.218 | 999800113 | 999800213 | 99980240 | 999802400 | 0, 4.20, 6.70 |
| 15 | Hadeon death, no bonus | 13.092 | 999800114 | 999800214 | 99980250 | 999802500 | 0, 4.70, 7.90 |

Every line has one silent Wwise PCM carrier per subtitle phrase. Its media ID
is the manifest's `carrierBase` plus cue index. The first entrance preserves
carrier IDs 999800010-999800014. Later lines use their TalkMsg block as the
carrier base; carrier and text IDs are separate namespaces. Cue start times
after the first line are estimates from recording cadence and waveform pauses.
The last cue of each line ends near the spoken end, while the full voice keeps
playing through its reverb. The first entrance's current final cue starts at
13.10 seconds; all boundaries remain calibration estimates. Native TalkParam
transition overhead and death dialogue after boss HP reaches zero need in-game
calibration.


Bank structure
--------------

The bank name/ID remain `cs_c9998` / 1155255848, selected by Hadeon's
NpcParam `SoundAddBankId` 9998. Event names use `Play_v<ID>` and
`Stop_v<ID>`. Every full voice has a separate `Play_v<stopAlias>` event wired
to that voice's stop action for EMEVD cancellation. Original first entrance
sound 999800001 and alias 999800002 retain their IDs; the final phrase uses
sound/media 999800003 and stop alias 999800004. Its sound node is 3900001100
with play/stop actions 3900003200/3900003210. Stop both aliases when the
opening line is interrupted. Post the final phrase once at 13.10 seconds from
the actual first-segment playback request, at Hadeon's current position.

All sounds are embedded, PCM, one-shot children of the original Voice mixer.
The mixer uses voice bus 3170124113, its original listener-relative
`PositionAndOrientation` routing and attenuation object 3900000004, plus
2 dB `Volume` on the shared ActorMixer. Its children precede the mixer in
HIRC, and actions precede events, matching the native ordering that was
audible before this expansion.


Build and validation
--------------------

From the repository root:

```powershell
python src/audio/hadeon/prepare.py --scratch .codex-temp/hadeon-audio-next
python src/audio/hadeon/build.py --scratch .codex-temp/hadeon-audio-next
```

`prepare.py` checks the pinned installed ffmpeg and WwiseConsole executables,
validates and hashes all wet originals, writes derived WAVs to `converted/`,
splits the converted first voice at sample 628800 without re-encoding either
segment,
creates exact silent WAVs in `subtitle-cues/`, converts all media through Wwise
PCM and updates `cs_c9998/soundbank.json`. The updated first entrance source
is hash-pinned; its conversion, WEM and changed silent carriers are regenerated.
The unchanged first silent carrier WEM remains hash-pinned. A blank Wwise project and
external-source list are created under `.codex-temp/hadeon-monologue-audio/
revision5/`. WwiseConsole reports `ConversionSettingsNotFound` while applying
the blank project's default PCM setting; the script verifies each output's
format and sample count before using it.

`build.py` packs a candidate into a new output directory below the supplied
`--scratch` directory (the historical default is
`.codex-temp/hadeon-monologue-audio/revision5/`) through pinned rewwise and independently decodes it. It checks
BKHD 135, original mixer routing and 2 dB gain, action/event mappings, child
order, 269 HIRC objects, 117 events, all 50 embedded WEM bytes and readback
graph equality. Each voice WEM must match its assigned converted WAV or segment sample count; each
carrier must be exact zero PCM at its planned length. It also verifies that the
two segment PCM payloads exactly rejoin into the converted voice. The earlier 1.4.4
candidate was 22,419,448 bytes, SHA-256
`C0C4BFB24ABEA892AD02A33CBF42F658053148B92DB88054D5CD13EB8C3A67C9`.
The 1.4.8 gain candidate under `revision5/gain-148/` is 22,419,453 bytes,
SHA-256 `124BA5B16918CEDE0CF20FBFB368CF0CABEFC87040B3FB93CF9FECCF923C6EFD`.
Only its HIRC chunk changes from the previous bank: the ActorMixer gains one
`Volume` property. The BKHD, DIDX and DATA chunks and all 49 WEMs are identical.
`prepare.py` retains the existing mixer when it rebuilds the graph, so its
2 dB setting survives a subsequent media preparation.
The earlier source/candidate guard receipt is `revision5/handoff.json`. Prior sources are
backed up in `.sovereign/backups/hadeon-dialogue-144/`; runtime recovery copies
and acceptance hashes are in `.sovereign/backups/hadeon-progress-144/accepted-inputs/`.
This validation does not establish in-game voice balance or subtitle timing.
