Hadeon destination expansion 1.7.2
=================================

All eighteen authored landing points now participate in first and repeat
entrances, fall recovery, periodic combat teleports and Vortex relocation.
Positions, heights and initial rotations are preserved exactly. Existing
RotateCharacter calls still turn Hadeon toward the player after placement.
Selection ranks horizontal distance, while clearance and Vortex eligibility
use three-dimensional spheres at each landing's actual height.

The [destination registry and generator](../../src/recipes/hadeon-teleport/README.md)
own 153 comparison boxes, eighteen 2.5 m clearance spheres and eighteen 8 m
Vortex spheres. All 44 existing helpers are unchanged; 145 new helpers use
18005101-18005245 after map/source and all nine runtime-event collision checks.
The author confirmed that all ten additions and their orientations are intentional.
Entity 18002390 remains reserved for the death-dialogue audio carrier.

The two entrance selectors now converge after their existing timing gates.
This avoids duplicating native label sets. Long branches use explicit labels
within L0-L20, and Vortex evaluates short-lived nested eligibility checks instead
of retaining eighteen condition groups. No new events, saved flags, timers or
per-frame coordinate calculations are introduced. Each request evaluates at most
seventeen pair comparisons. Periodic no-landing retry cadence remains unchanged.


Verification
------------

The native map builder passed unchanged and edited roundtrips, reversal of all
helper edits, exact authored-marker preservation and repeat-build idempotence.
It performed 544,012 selection checks across four heights; maximum measured
horizontal nearest-distance error was 0.246 mm, below the 1 mm tolerance.
Candidate receipt: `.codex-temp/hadeon-teleport-18/accepted-candidate/manifest.json`.
Map SHA-256: `ae2719347aed50c831a69e7c3a941a2f04eb5ceaea8260754c4591f168b91d0a`.

Native event compilation passed. Only events 5750304, 5750311, 5750430 and
5750432 changed; metadata and all other runtime events remain equivalent.
Candidate: `.codex-temp/event-builds/1790668006622705700/receipt.json`.
Event SHA-256: `1de4b247af5b5d5729a18e21502c7501fbd865fd20269a49add568b3cc90ecf2`.
The eight unrelated shipped event files remain equivalent. Authoring-only
common_func remains unshipped.

Scoped backups: `.sovereign/backups/hadeon-destinations-172/manifest.json`.

All 49 encounter, progression and reward checks passed. The selector tests reach
each of the eighteen destinations through all five entry paths, check placement
before player-facing rotation, and enforce the seventeen-comparison bound.
Regenerating the event source produces identical bytes.

Accepted native map and event files were synced through guarded handoffs to
Smithbox and Script. Receipts:
`.sovereign/handoffs/8fe4120eba394572bde9ff1b493f1352/receipt.json` and
`.sovereign/handoffs/40f5b3078d6a4bfea386c1db30cf8f96/receipt.json`.

Repository preparation, version consistency, scoped whitespace and relative-link
checks passed. The complete 79-file main package differs from 1.7.1 only in the
Stranded Graveyard map and event binary. Preparation receipt:
`.vdb/prepared/a7e1c3691a7e49b8a19cf820e09feaeb/receipt.json`.

Protocol-3 deployment completed for enabled profile `SkC-QjDMc`, with build
`47d67d8c09b7a0fe07c1f6b9`. All 79 stage and live files independently matched their
prepared hashes. Finalization receipt:
`.vdb/finalizations/13c959e7607b4d37a1c9c479998d5359/receipt.json`.
Hash evidence: `.codex-temp/hadeon-teleport-18/deployment-hashes.json`.


Game acceptance
---------------

Pending: both sides of paired markers, raised landing floor/collision, initial
orientation followed by player-facing rotation, first and repeat entrance timing,
fall recovery and penalty, periodic action-boundary teleport, Vortex motion
continuity, wall/crystal clearance, arena exit/death cancellation and frame time.
Source/native verification does not establish in-game navigation or performance.
