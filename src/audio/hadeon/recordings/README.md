Hadeon recording roster
=======================

All sixteen lines have an author-supplied reverberant WAV and dry `-nr.wav`
counterpart. These are original recordings; conversion headroom and sample-rate
changes belong under `../converted/`. The wet versions are used for playback.

Version 1.4.4 plays the first entrance and first 50% HP line once per journey,
then uses randomized shorter pools. Player death selects one of four lines
immediately, regardless of Hadeon's teleport status or facing. This single pool
replaces the separate player-killed and return-facing-Nemesis pools. Hadeon's
own defeat uses the remembrance line before any qualifying combat loss, or the
warning otherwise. See [audio and subtitle implementation](../README.md) and
[encounter verification](../../../../docs/test-results/2026-09-27-hadeon-progression.md).

Version 1.4.6 remembers the last started line separately for repeat
entrance, repeat half-health and player-killed dialogue. The next selection from
that pool excludes that line and gives each of the other three an equal chance.
Saved history survives encounter resets and reloads. First-time lines and fixed
defeat lines remain separate. See
[verification](../../../../docs/test-results/2026-09-27-hadeon-no-repeat.md).

Version 1.5.6 replaces the need-another and whisper slots with worthier and
another-falls below. Subtitle wording was recovered by local transcription of
the supplied dry recordings and should be checked during playback calibration.
The another-defeat entrance and thousand-times kill line require three qualifying
combat losses. The third death can select thousand-times. Eligible pools still
exclude their last started line. Fatal below-arena falls count as losses but
play no kill voice or subtitle and do not advance dialogue history.

| Trigger | Reverberant filename | No-reverb filename | Dialogue |
| --- | --- | --- | --- |
| First entrance | `hadeon-entrance-first.wav` | `hadeon-entrance-first-nr.wav` | Begone from this place. Long have I kept mine oath. Older still, the hunger here bound. His whispers draw thee hither... to my blade. |
| Repeat entrance | `hadeon-entrance-unyielding.wav` | `hadeon-entrance-unyielding-nr.wav` | Thou shalt find me as before. Unyielding. Forsake these fruitless ambitions. |
| Repeat entrance | `hadeon-entrance-promise.wav` | `hadeon-entrance-promise-nr.wav` | Doth his promise grow sweeter with each defeat? |
| Repeat entrance | `hadeon-entrance-another-defeat.wav` | `hadeon-entrance-another-defeat-nr.wav` | Each defeat hath taught thee naught. Let this be thy last. |
| Repeat entrance | `hadeon-entrance-hunger.wav` | `hadeon-entrance-hunger-nr.wav` | Again thou comest, bearing another’s hunger. Then meet thy familiar end. |
| First 50% HP | `hadeon-half-health-first.wav` | `hadeon-half-health-first-nr.wav` | Ngh... Even bound... thy reach grows long, Nemesis. Have these lands not bled enough for thee? |
| Repeat 50% HP | `hadeon-half-health-hunger.wav` | `hadeon-half-health-hunger-nr.wav` | Ngh... His chains hold. Yet still his hunger grows. |
| Repeat 50% HP | `hadeon-half-health-surrendered.wav` | `hadeon-half-health-surrendered-nr.wav` | Ngh... That strength... what hast thou surrendered? |
| Repeat 50% HP | `hadeon-half-health-dominion.wav` | `hadeon-half-health-dominion-nr.wav` | Ngh... I shall give him no dominion here. |
| Repeat 50% HP | `hadeon-half-health-oath.wav` | `hadeon-half-health-oath-nr.wav` | An oath such as mine yieldeth not. |
| Player killed | `hadeon-player-killed-thousand-times.wav` | `hadeon-player-killed-thousand-times-nr.wav` | Rise a thousand times. I shall not yield. |
| Player killed | `hadeon-player-killed-worthier.wav` | `hadeon-player-killed-worthier-nr.wav` | Find thee a worthier servant. |
| Player killed | `hadeon-player-killed-chosen.wav` | `hadeon-player-killed-chosen-nr.wav` | Was this thy chosen? |
| Player killed | `hadeon-player-killed-another-falls.wav` | `hadeon-player-killed-another-falls-nr.wav` | Another falls. Thy prison stands. |
| Hadeon defeated | `hadeon-death.wav` | `hadeon-death-nr.wav` | Fool… wouldst thou doom these lands? Refuse the Bindseal… disturb not the crystal... |
| Hadeon defeated no bonus| `hadeon-death-nobonus.wav` | `hadeon-death-nobonus-nr.wav` | Thy strength… awakens an old remembrance. Another stood where thou standest. Him… I called lord. |
