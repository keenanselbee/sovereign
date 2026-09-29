Hadeon immediate-combat isolation 1.5.4
======================================

The author reports that the 1.5.3 opening teleport succeeds but Hadeon remains
idle. The requested test bypasses the AI hold instead of adding another reset.
Event 5750302 reveals Hadeon and enables AI without first disabling it for speech.
Event 5750311 enables AI, starts the health bar/music and marks combat started on
valid entrance admission for both first and repeat lines. That happens before
speech's existing 0.7-second settling delay and 12-metre proximity gate.

The first-line receipt, audible voice, subtitle ESD and cancellation rules are
unchanged. After voice starts, the existing combat flag immediately satisfies
the handoff wait and prevents the delayed teleport/reset branch. Its authored
eight-point selector is retained for restoration but bypassed during this test.
The normal fall-recovery event, map, AI goal/parameters, effects, audio bank and
player code are unchanged. No new diagnostic logging or flags are added.

The existing departure controller can still disable AI while waiting for a valid
return. Valid re-entry enables it before speech. The ordinary load-reset test,
real-death reload bypass, aid progression and reward protections remain unchanged.


Verification and recovery
-------------------------

28 encounter/load-reset tests pass. They cover immediate first-entry combat
before delay/range, retained voice request/playback, hits and cancellation without
an opening teleport, exit/death behavior, eight-point fall selection with one
penalty after arrival, quantized-distance ties and load/death progression.
These source tests do not establish that normal AI actions execute in game.

Pre-edit source, binaries, tests and release metadata are backed up under
`.sovereign/backups/hadeon-immediate-154/`. To remove the test, restore the reviewed
spawn AI hold and first/repeat admission split from that source, preserving later
edits, then rebuild/sync/deploy under a new version. The retained timed teleport
branch becomes active again when first admission no longer marks combat started.

Native candidate `.codex-temp/event-builds/1790556200906645700/receipt.json`
changes only events 5750302 and 5750311. All other events, their order and file
metadata are preserved; the other eight runtime event files are byte-identical.
The compiled map event SHA-256 is
`831197184d8255fd5d41843ea11a9f800f5f84531412a83ed727a1a27ee721ea`.
Guarded editor handoff:
`.sovereign/handoffs/c3f15020af5f4b23b32eb8977855b0a2/receipt.json`.
Preparation, regular-version consistency, scoped whitespace and document links pass.
Deployment completed. Prepared receipt
`.vdb/prepared/203e5b72d8c6435e9e08dc878c015226/receipt.json` contains 75 files;
only the Hadeon map event differs from 1.5.3. Finalization
`.vdb/finalizations/285c035956dd4dea985c6c150fb5bdf6/receipt.json` completed
request `d95e1d69-e1db-4abb-9385-06fa8c26decd`, build
`f89d184c493cd78ca1c3d3ec`. Profile `SkC-QjDMc` is enabled, deployed and verified
with no differences. Independent hashes of all 75 live files match; record
`.sovereign/backups/hadeon-immediate-154/live-verification.json`.
The author subsequently reported that Hadeon attacks normally in this immediate-combat test. This implicates the old speech hold/release sequence; it does not independently identify the failing engine state.


In-game test
------------

Quit/load while alive to reset the encounter. Approach Hadeon without hitting him.
Observe whether he approaches and attacks before and during the first speech;
voice/subtitles should still play, and no timed opening teleport should occur.
If normal attacks work, the old hold/release sequence is implicated. If he remains
idle even with AI enabled from appearance, investigate the active battle action,
approach/guard subgoal and live phase effects before choosing another repair.

The follow-up uses a dedicated running-AI wait; see [the 1.5.5 implementation](2026-09-27-hadeon-wait-155.md).
