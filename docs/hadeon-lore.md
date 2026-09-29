Hadeon, Lord of the Crucible
===========================

Proposed character history, supplied by the author on 2026-09-26. This is
Sovereign's original lore proposal, not a claim about established Elden Ring
canon. Dialogue remains in development; this document does not establish
implemented dialogue or change encounter behavior.


The first lord of the Crucible Knights
-------------------------------------

**Hadeon, Lord of the Crucible**, was the ancient warlord who first gathered
the Crucible Knights beneath a single banner. In an age when strength itself
conferred lordship, none among his knights could overcome him.

Then came Hoarah Loux.

Their battle became legendary. Hoarah Loux was the first warrior ever to defeat
Hadeon, but rather than kill him, he earned his allegiance. Hadeon relinquished
command of the Crucible Knights to the victor, recognizing him as the stronger
lord.

Thus the Crucible Knights entered the service of the man who would become
**Godfrey, First Elden Lord**.


The prison vigil
----------------

The author's established premise is that Hadeon guards the imprisoned Nemesis
under the charge of grace/Godfrey. Nemesis and the Blood Star are the same being,
whose release threatens the Lands Between and whose insidious influence reaches
beyond his prison. Current dialogue drafts use male pronouns for Nemesis.

Hadeon is hostile to the player; the accepted first-encounter monologue below
delays combat until its cue or a player attack. It offers no peaceful outcome.
Narrative release and the separate crystal choice are
described in [the encounter design](DESIGN.md#hadeon-the-shrine-and-crystal-release).


Direction for dialogue
----------------------

This proposed history gives Hadeon's allegiance a personal foundation: he
freely recognized the one warrior who defeated him. His reverence for Godfrey
can grow from that earned respect, while his pride survives his loss of command.

Use this as a writing direction, not additional settled history. His opening
can express the authority of a former warlord; pressure during the fight can
expose how much keeping his oath matters to him. Avoid explaining the entire
history in combat dialogue. The earlier draft lines remain suggestions, not
final dialogue.


First entrance dialogue
-----------------------

Author-selected on 2026-09-26. The initial implementation is recorded in the
[monologue report](test-results/2026-09-26-hadeon-monologue.md); in-game calibration
remains pending.

> Begone from this place. Ancient is mine oath.
> Older still, the hunger here bound.
> His whispers draw thee hither... to my blade.

Source recording: `C:\Users\Keenan\Desktop\hadeon-entrance-first.wav`.
The updated recording is 17.062 seconds of mono 44.1 kHz floating-point PCM.
It includes reverb; preserve the full recording and its tail. Remove the earlier
test bank's +3.5 dB boost and restore its positional/distance settings. Preserve
the untouched original and apply only conversion headroom to the derived audio.

Accepted behavior:

- For calibration, replay the full monologue on every fresh encounter, including
  return after a true retreat. This explicitly supersedes the initial once-per-
  journey request for now. Mid-fight fall recovery does not replay it. Other
  proposed dialogue pools are outside this implementation. After calibration,
  an interrupted first encounter should count as consumed and a return should
  use repeat dialogue; that policy remains planned until the repeat audio exists.
- Begin the recording 0.7 seconds after Hadeon appears, with Hadeon standing idle
  and boss music silent unless attacked. Time zero is the recording start, not
  entry into the room or the start of the existing summon effects.
- At the updated recording's 13-second cue, "to my blade", start boss music
  and combat only if the player remains in the valid room. This replaces the
  earlier recordings' 16.4- and 17.1-second cues.
- If the player has left the room or dropped below it at the combat cue,
  cancel the opening and reset Hadeon immediately. A valid return replays the
  full opening during calibration.
- If the player attacks Hadeon earlier, start music and combat immediately.
  His voice and subtitles continue through that transition.
- Show ordinary boss-style subtitles. Subtitle phrase boundaries, playback
  volume, music onset latency and interruption cleanup require game testing.

Implementation direction: separate the dialogue playback from the combat-start
condition, and share one playback-start signal for cue timing. Use temporary
attempt state for playback/combat, with collision checks before assigning IDs.
No saved dialogue receipt is needed for the every-encounter test. Adapt the existing
retreat, rescue and defeat handling so a canceled attempt cannot later start
music or leave Hadeon inert. Qualify native talk scripting, TalkParam and FMG
text together; the successful audio-only PlaySE test does not prove subtitles.


Player-death dialogue
---------------------

Author-selected on 2026-09-27. Consolidate the former player-killed and return-
facing-Nemesis pools into one randomized pool. Start one line immediately when
the player dies during the encounter, regardless of Hadeon's teleport status or
facing, to leave time to hear it before respawn. Do not wait for his return to
Nemesis or play a second line on teleport.

- "One fewer voice to answer him."
- "Thou shalt need another."
- "Was this thy chosen?"
- "Whisper all thou wilt."

The [recording roster](../src/audio/hadeon/recordings/README.md) owns filenames
and both reverberant/no-reverb variants. These lines have placeholders only;
recordings and runtime playback remain pending.


Hadeon's death dialogue
----------------------

Author-selected on 2026-09-27:

> Fool… wouldst thou doom these lands? Refuse the Bindseal… disturb not the crystal!

Record as `hadeon-death.wav` and `hadeon-death-nr.wav`. The roster and both
placeholders carry this wording; recording and runtime playback remain pending.
