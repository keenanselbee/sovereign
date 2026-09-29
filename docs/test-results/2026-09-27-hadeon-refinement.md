Hadeon encounter refinement
===========================

This local implementation follows the author's 22-metre entrance range, 12.2-second
teleport cue, ten-loss aid cap and periodic teleport decisions. Native build and
source checks do not establish in-game behavior. The subsequent deployment request
prepared version 1.5.7 and queued it while Vortex was closed.
That request later failed because the game was running;
the full refinement is now included in the verified [1.5.8 deployment](2026-09-28-opening-pouch-music.md#deployment).


Behavior
--------

First entrance uses the updated wet recording, preserving the original wet/dry
sources, conversion gain, +2 dB mixer and positional routing. Its five subtitle
cues start at 0, 2.75, 5.55, 9.15 and 13.10 seconds, with the last ending at 14.8.
The full recording lasts 17.270833 seconds; the event permits 17.30. The author
explicitly selected a teleport at 12.2 seconds from actual playback, which is
earlier than the measured start of "to my blade". The 0.7-second minimum settling
delay remains. First and repeat entrances use a 22-metre start gate. Native talk
range and ESD update distance are both 100 to keep subtitles active across the room.

Normal and no-loss death voices use hidden actor 18002390, cloned from the existing
inert sound carrier 18000852. NpcParam 99989900 loads bank 9998; the actor has no
TalkID and never participates in combat. It is preloaded and moved to Hadeon's
death position. If unavailable at playback, the player emitter is a bounded fallback,
with matching stop routing. Both full voice timers remain 17.24 and 13.12 seconds.
Completion flag 1055425256 permits boss cleanup; a 25-second fallback prevents
permanent reward/banner blocking. Death subtitles still belong to Hadeon and
their native continuation after actor death requires a game test.

Each counted death unlocks 5% aid, up to 50% at ten deaths. The first five loss
flags retain their meaning; 1055420952-1055420956 store losses six through ten.
The ordinary-load test reset clears both blocks; the death-reload bypass retains
them. Three-loss dialogue gates, fatal-fall counting, silent falling-death taunts,
no-loss reward eligibility and existing dialogue history rules are preserved.
Beginner rescue defaults to 40 seconds and uses 38, 36, ... 20-second cooldowns
after one through ten deaths during admitted aid. An active cooldown stays fixed
when crossing the arena boundary. See [aid ownership](../HADEON-AID-UPDATE.md).

Event 5750430 queues a periodic relocation after a random 15-30 seconds of valid
combat. Both actors must remain in the arena; active dialogue and a player within
eight metres defer the request. Private battle goal 250091 checks the request at
its next activation, checks attack completion and throw state, then acknowledges
and waits. The event rechecks eligibility, uses the same eight-point clear landing
selector as opening/fall recovery, faces the player, clears the request and replans.
Raising a request never forces an AI replan. Cancellation releases any acknowledged
wait without teleporting. Native battle 250010 is unchanged for other actors.
Engine action-selection/recovery timing and private goal loading require game tests.

The local Nexus description uses Nightmare difficulty and describes current
crystal/eclipsing behavior separately from the planned Nemesis Unbound story stage.
The actual-hit weapon signature, receiver, final confrontation and proposed
Bindseal story behavior are documented as [deferred work](../nemesis-unbound.md).


Validation and recovery
-----------------------

Initial and accepted-output recovery copies are under
`.sovereign/backups/hadeon-refinement/`; `accepted/receipt.json` guards all thirteen
native/source replacements. Existing unrelated work is preserved. Initial acceptance
was sync-only; the later explicitly requested deployment is recorded below.

The event candidate is `.codex-temp/event-builds/1790570926257421100/receipt.json`.
Only common event 50 changes. In m18, events 5750300, 5750303, 5750311, 5750312,
5750420 and 5750422 change; 5750430 and 5750431 are added. Existing event order,
metadata and all seven other runtime event files are preserved. Authoring-only
common_func remains unshipped.

The final audio candidate is `.codex-temp/hadeon-refinement-audio/output4/`:
263 HIRC objects, 114 events and 49 media pass independent readback. Only the first
voice and four retimed silent carriers change; the first carrier remains identical.
Three native FMG candidates change only TalkMsg 999800010. The talk candidate
changes only t999801800 group 1 and retains the other native ESD.

Regulation changes are chained through the aid cooldown, private battle assignment
and dialogue carrier recipes. Their readbacks preserve unrelated tables/rows and
binder metadata. The map adds only the carrier, preserving all existing enemies
and region geometry. The private battle binder has explicit 250091/250092 goal
definitions; native decompilation roundtrip, registration, compiled branch mocks
and binder readback were checked. This is not an HKS or game-engine execution test.

Source tests cover ten-loss progression and reload reset, full voice windows,
death priority, reward recovery, 22m entrance and 12.2s cue, periodic request and
cancellation, resource migration from an old stronger tier and cooldown crossing.
The 37 encounter/load-reset tests, progression simulation, three aid tests and
one rescue test pass. Local repository checks, Nexus description structure,
edited Markdown link targets and scoped whitespace checks pass.

The final client-visibility correction moves carrier initialization outside the
host-only branch, so visitors also hide it locally. Its candidate is
`.codex-temp/event-builds/1790571369106500900/receipt.json`; only event 5750300
changes from the first accepted event candidate. Recovery is recorded in
`.sovereign/backups/hadeon-refinement/client-carrier/receipt.json`.

Reviewed editor handoffs are under `.sovereign/handoffs/`: parameters
`4dcc5578e035471ca5d474c26c1ea201`, map `2d989dbeb40d4c11847b395c9f6ceb91`,
events `52b6c3791cd1447a93b465a8a72c0022`, text `67c55226f9e342b2b20e6f58d55586ea`,
AI `80e0cd3ca931412abc6bf864b142ddbf`, talk `cd20e8151b934f25aa49643149106111`,
and player `cb61bccdcda74fb88e9a6e6cb7059384`. The event-only client correction
uses `4fc4c5548cd645bfa6f1d4becc828149`. Audio has no configured external editor
mapping and remains an accepted repo-owned bank. Talk qualification is
`1790571110521247600`; player qualification is `1790571265205380200` beneath
their corresponding `.codex-temp` qualification directories.


Deployment request
------------------

Version 1.5.7 metadata and changelog checks pass. Full main-package preparation
contains 77 files: ten changed runtime files and the new private battle binder,
with no removals and an identical external Scripts-Data-Exposer-FS.dll. Textures
are unchanged. The prepared receipt is
`.vdb/prepared/949023b3e2564fe3a40e7bc3cbb134e8/receipt.json`.

Protocol-3 all-profile request `c1c6a5b5-d565-4b28-b0f0-f89a8864156a` failed
in `.vdb/finalizations/a9d9d6e056c9427b9f8ed3306534383f/receipt.json`.
Vortex was initially closed; when it processed the request, deployment failed with
"Waiting for the game to close". No successful 1.5.7 verification is claimed.
The later 1.5.8 request contains the full refinement and completed with all 77 live
files verified, as linked above. Gameplay acceptance and publication remain pending.
