Hadeon encounter correction, 1.4.3
=================================

The author reports that 1.4.2 starts the bar and music at the 13-second cue,
but Hadeon remains idle even when approached. Subtitles start late from line one
when entering a smaller radius. Arena aid shows its aura but does not sustain
the stat ramp. These are gameplay failures, despite earlier native compilation
and source simulations passing.


Changes and acceptance limits
-----------------------------

The Hadeon ESD now calls `SetUpdateDistance(70)` at initialization, matching
native Gideon's arena dialogue. Its `TalkToPlayer` final argument changes
from 0 to 1, matching Gideon, Margit and Rennala boss conversation patterns.
Immediate and combat-cue conversation-release calls remain. This is a candidate
correction for the reported idle behavior, not proof of its engine cause or fix.
The update distance covers the room; positional voice attenuation is unchanged.

Native ESD comparison shows only the new state-0 command and the final argument
of the state-3 talk command differ. All other states, member metadata, the
original t706021800 member and binder metadata are preserved. Candidate:
`.codex-temp/dialogue-builds/1790529886309237100/receipt.json`.
All owned talk source/member pairs pass native qualification:
`.codex-temp/talk-qualifications/1790530025043559800/receipt.json`.
Recovery copies are under `.sovereign/backups/hadeon-dialogue-143/`.
The three-file talk handoff completed:
`.sovereign/handoffs/9d4b584cf7bd431e997e9ed05a199cc6/receipt.json`.

Speech now uses a 0.7-second appearance delay, with the timed combat cue
13 seconds after actual speech start. A hit during that initial delay must start
combat immediately without canceling or restarting the pending speech. True
departure at the cue still resets Hadeon; calibration still replays the full
opening on each fresh encounter.

Unsupported backward event jumps were found in the aid refresh, retreat grace,
hallway debounce and HP brightness loops. Native labels only jump forward;
compiler success did not validate these loops. The event correction retains
three continuous eligible seconds before aid, its continuous permission refresh,
twenty stat steps over ten seconds, withdrawal, six-second retreat cancellation
and one-second hallway absence debounce.

The aid admission stays in 5750403; new 5750405 refreshes its granted effect.
First-hall approach stays in 5750320; new 5750410 debounces departure and hands
a full exit back to the original 1.5-second approach delay. Brief reentry keeps
the lit fixtures. Brightness clears once in map initialization, with its state
retained across 5750370 restarts. Recovered retreat restarts 5750303 without
restarting music; its admission now also observes boss and confirmed player death.
Leaving before the delayed voice begins resets an unhit opening. An earlier hit
keeps combat/speech running and uses the existing ordinary retreat rules.

Native candidate:
`.codex-temp/event-builds/1790530559835198400/receipt.json`.
The map grows from 80 to 83 events: 5750313/5750405/5750410 are new. Existing
changes are limited to 0, 5750300, 5750303, 5750311, 5750320-5750331, 5750370
and 5750403. The other 62 events, their ordering, parameter bindings, rest
behaviors and file metadata are preserved; all other runtime event files rebuild
equivalently. Event SHA-256:
`B5D5DA03C652FFDB899BF77ADEE0B961452E05147FAD570264EA0B97224A5ADD`.
Source recovery is in `.sovereign/backups/hadeon-fix-143/`; native recovery is
in `.sovereign/backups/hadeon-runtime-143/`.
The two-file event editor handoff completed:
`.sovereign/handoffs/6159364248d143f98e53b9f5e6184242/receipt.json`.
The source-label scan found no backward jumps in the 19 scoped workers.
Allocation evidence is
`.codex-temp/hadeon-diagnosis-143/allocation-scan/flag-scan.json`: the new flag
and three event IDs have no collisions in 598 pre-edit native/mod event files
or 194 regulation members.

The focused source simulator passes speech/cue/early-hit timing, invalid delay
and cue positions, confirmed death versus rescue, reentry, continuous aid,
lighting death freeze and all 125 hallway fixture pairs. Its new cases cover
death during the initial delay and distinguish AI enabled from actual Combat
state. The seven encounter boon/fall/presence tests also pass. These tests model
authored control flow, not native conversation or AI execution.

The selected death line is now recorded in both recording placeholders:

> Fool… wouldst thou doom these lands? Refuse the Bindseal… disturb not the crystal!

Only the entrance and its dry variant have real recordings. Death, player-kill,
repeat entrance and half-health playback remain pending audio and implementation.
The bank, original audio, five subtitle texts and cue carriers are unchanged.

The bounded aid log now records `voice`, `gate`, `reset`, `combat` and
`aiCombat`. The first four read existing attempt flags; the last reads temporary
flag 1055422949, which event 5750313 mirrors from native Combat AI state while
the encounter is active. No diagnostic flag controls gameplay. Probes use
Script Exposer's documented decimal-string flag IDs and retain independent
failure isolation. The header is now `schema=2`, replacing the stale version.
Three diagnostic tests pass, including one failed flag probe with the remaining
fields intact. The two existing aid resource/ramp tests also pass.

Player native qualification:
`.codex-temp/player-qualifications/1790530094110409000/receipt.json`.
This guards the complete animation/behavior group and changed HKS input; it is
not proof of HKS engine execution. Diagnostic-only recovery copies are under
`.sovereign/backups/hadeon-diagnostics-143/`.
The guarded player handoff changed only the HKS file:
`.sovereign/handoffs/64c07f4f5aee4d9199b14e4c9b2b7b84/receipt.json`.


Required game retest
--------------------

- Stay at the far side of the room: speech starts 0.7 seconds after appearance,
  subtitles advance from the start, and Hadeon moves and attacks at the final
  phrase, about 13.7 seconds after appearance.
- Hit during the first 0.7 seconds and during speech: immediate retaliation and
  music, followed by uninterrupted speech and subtitle progression.
- Leave or drop before the cue; return quickly and after reset. Confirm no stale
  music, delayed combat or overlapping speech. Test death, rescue and boss defeat.
- Stay eligible for aid: after three seconds, twenty steps reach twice the
  HP/FP/stamina maxima and damage over ten seconds; the aura remains throughout
  eligibility and withdrawal remains correct on departure/victory.
- Cross hallway boundaries for less than and more than one second; test HP
  brightness thresholds, death/retry, victory and crystal destruction.

Source tests and native preservation checks cannot establish these game results.


Package and deployment
----------------------

Preparation, regular-version consistency, document links and whitespace checks
passed. Version 1.4.3 remains `releaseReady: false` pending the game retest.
The complete 75-file main package changes only the map event, Hadeon talk binder
and player diagnostic HKS from 1.4.2. The other 72 files, including the bank,
regulation, maps and external Script Exposer DLL, are byte-identical.
Prepared receipt:
`.vdb/prepared/7fe8f89533f5454692471dd159e64150/receipt.json`.
Protocol-3 finalization:
`.vdb/finalizations/786141c62d6d4be98783d3ad1d7bf262/receipt.json`.

Finalization completed for the existing Elden Ring profile SkC-QjDMc. Request
`f12a7a95-2b69-4638-b6c6-9936cc3a1660` deployed main build
`fd8a91565ed21bfb74c36d40`; the verified stage is selected for later packaging.
Independent hashes of all three changed live Game files match the prepared
package. Gameplay remains pending; no new dialogue recordings were fabricated
or included, and no Nexus publication was performed.
