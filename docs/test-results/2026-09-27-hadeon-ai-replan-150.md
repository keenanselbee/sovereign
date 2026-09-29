Hadeon AI replan trial 1.5.0
===========================

The author reported that Hadeon remained idle after the monologue, even at close
range, but attacked after being hit. The 1.4.8 aid trace recorded intro gate OFF,
combat flag ON and native AI Combat ON at 52.212 seconds, with voice finishing at
56.265 seconds. Those states establish that the handoff fired, not that the AI
selected an attack. A stalled decision or target acquisition remains a hypothesis.

The only gameplay change is one `RequestCharacterAIReplan(18002354)` immediately
after `EnableCharacterAI` in event 5750311's first-monologue handoff. It runs once
when the thirteen-second cue or an early hit releases that branch. Existing
living-player/boss, room, fall and combat-state guards still apply. The request
does not stop voice playback. Repeat entrance and controller paths are unchanged;
no animation reset, forced attack or network update change is included.

The 1.4.9 load-reset test remains active: quit/load while alive to get a fresh
first monologue, then allow it to finish without striking Hadeon. Confirm that he
approaches and attacks after the cue. If he remains idle, record whether a hit
still wakes him. Automated checks cannot establish the outcome of native AI
replanning.

The author's follow-up reports that Hadeon still did not engage after the
monologue. The player was in front of him, and Hadeon turned to track the player
while remaining in his idle pose. Moving behind him triggered a different action.
The replan trial therefore has not satisfied engagement acceptance. This weakens
simple facing/detection explanations and makes action selection worth inspecting;
it does not identify a particular goal or prove that the different action was an
attack. No trace of the live goal or action is available.

Verification and recovery
-------------------------

Source tests cover one replan after enabling AI, no repeated requests, ongoing
voice, unchanged repeat entrance and no replan after death or invalid-room cues.
All 21 encounter/load-reset tests passed, as did the existing progression
simulation. Preparation, version, whitespace and local-link checks passed.

Native candidate `.codex-temp/event-builds/1790551340605664600/receipt.json`
changed only event 5750311; metadata/event order and the other eight runtime event
files are unchanged. Source comparison against the recovery copy proves that the
only source addition is the replan instruction and its comment. The compiled map
SHA-256 is `4efc79a0860a20fdca0c60af69d35a538f2714992af731cfc27fb49f018da656`.
Guarded local acceptance is recorded in
`.sovereign/backups/hadeon-ai-replan-150/accepted.json`. Editor handoff
`.sovereign/handoffs/3c953ffcaa6b4018b8080b467a13bf7c/receipt.json` completed for
the matching map source and binary.

Recovery inputs are in `.sovereign/backups/hadeon-ai-replan-150/`. Remove the one
replan instruction and its comment, then rebuild/sync/deploy to revert this trial
without removing the earlier reset test. Do not restore whole old files over
later work.

Deployment completed
--------------------

Prepared `.vdb/prepared/5ab252052c854f518018dc711d8797bc/receipt.json` contains
75 files; only the Hadeon map event differs from 1.4.9. Finalization
`.vdb/finalizations/659ad14b2a0c42dc86dca7bbc690859d/receipt.json` completed
request `fd1e2ce6-e12a-4f0b-b993-8896130a6555`, build
`347a6d90072c9c6e8d13ab4f`, version 1.5.0. Profile `SkC-QjDMc` is enabled,
deployed and verified with no differences. Independent hashes of all 75 live files
matched; receipt `.sovereign/backups/hadeon-ai-replan-150/live-verification.json`.
This confirms installation, not successful AI engagement in game.
