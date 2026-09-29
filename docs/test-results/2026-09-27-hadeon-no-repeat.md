Hadeon repeat dialogue history
=============================

The author requested excluding the previous line from each repeat pool. Event
5750312 now keeps independent saved history for entrance (1055420940-0943),
half-health (1055420944-0947) and player-killed (1055420948-0951). Each range
uses the full 105542 prefix for all four flags. First-time and fixed defeat
lines do not consume these pools. This update shipped in 1.4.6; see the
[combined deployment record](2026-09-27-deflect-hadeon-trial.md).

With no history, all four lines are eligible. Thereafter, one uniform draw
among three slots maps to the three lines other than the previous selection.
This avoids reroll loops and bias. History updates immediately before playback;
interrupted lines count as spoken, while queued requests superseded before
selection do not. Encounter resets do not clear these saved flags.

Verification
------------

`tools/tests/test-hadeon-progression.mjs` exhaustively checks every previous
selection and random outcome for all three pools, one-hot history, independent
pools, consecutive requests, saved-history reload simulation and a superseded
request. Existing progression, duration and interruption checks also pass.
These are source simulations, not game-engine proof.

Native allocation scan: `.codex-temp/hadeon-no-repeat/allocation-scan/flag-scan.json`.
It checked 598 mod/retained vanilla event files (including flag ranges) and
194 regulation members, finding no collisions for the twelve saved flags.
Pre-edit source and native binaries are backed up under
`.sovereign/backups/hadeon-no-repeat/`.

The first compiler attempt exhausted temporary AND condition groups. Nested
single-flag branches replace compound checks without adding waits, event
workers or timing changes. In-game repetition, persistence and NG+ behavior
remain pending acceptance.

Native candidate `.codex-temp/event-builds/1790545476283941200/receipt.json`
compiled successfully. Decoded comparison changes only event 5750312, preserving
all 88 event IDs/order and file/event metadata; the other eight runtime event
files remain equivalent. Both source-side and runtime native copies were
accepted with input hashes and recovery record
`.sovereign/backups/hadeon-no-repeat/accepted.json`.
The eight existing Hadeon event tests and three aid tests also pass.
Guarded editor sync completed for the reviewed JS/native pair:
`.sovereign/handoffs/6493a23526e842439c0bfeee93a9a0f5/receipt.json`.
No live-game files changed. Local Markdown targets and whitespace checks pass.
