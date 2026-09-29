Movement diagnostics and Hadeon calibration 1.4.7
=================================================

The author authorized temporary movement instrumentation and deployment, then
added repeat-first-monologue testing and investigation of VFX without stat gains.
No movement decision, multiplier, animation, stat magnitude or audio asset changes.


Capture and testing
-------------------

`sovereignMovementCaptureEnabled` in the player HKS is the movement diagnostic
switch. The observer retains 180 frames, preserving up to 32 ordered hooks per
frame (extra hooks are counted). Positive processed input with idle state or
near-zero scripted speed for 0.25 seconds triggers a history dump plus three
seconds after the trigger. Intentional attacks/blocks/interaction can also produce
a capture; these are suspects, not automatic bug diagnoses. Half a second of
recovery rearms it. Limits are 12 captures, 30 minutes and 8 MiB per script instance.
Core read or I/O failure stops this observer without aborting gameplay Update.
An active capture is marked truncated if the time limit interrupts it.

Files are in the game's working directory, normally the Game folder:
`Sovereign-movement-1.4.7-<timestamp-or-session>-<suffix>.log`, with `.summary.log`
and `.aid.log` companions. Existing names are checked and the new capture uses
append mode, preserving older files. Optional `os.date` is guarded; if unavailable,
numeric collision suffixes still work. The summary retains its ten-minute cap;
the aid companion retains its five-minute cap. Restarting/reinitializing creates
another file; there is no automatic log deletion.

Hooks record callbacks, nested blocking reasons in order, movement requests,
speed resets and scale writes. Samples add processed direction/angle, sprint,
guard, event request, custom cancel/scale states and Update completion. The
prior scalar fields retain timestamps and may be stale; the ordered hook list
contains activity since the previous snapshot. No speculative raw-input or
world-position API is introduced. These are not physical velocity measurements.

Compare ordinary forward movement and releasing sprint while retaining forward;
capture both natural recovery and changing direction. Compare keyboard/controller
and note whether camera/enemies also freeze. Per-frame diagnostic overhead still
needs native observation; memory is bounded and disk writes are batched.


Hadeon changes and evidence
--------------------------

Event 5750311 temporarily clears only saved entrance receipt 1055420935 before
normal admission consumes it again. The full opening therefore repeats, with
the existing 0.7-second delay, 13-second combat cue and early-hit behavior. The
subtitle-disabled 1.4.6 AI trial remains active. Other speech pools, loss flags,
rewards and first-attempt aid suppression are unchanged.

The fresh live aid trace recorded permission once near t=13.2, then tier one:
maxima 522/78/97 became 548/81/101. Permission stayed absent, and around t=23.8
the bonus withdrew while combat/AI-combat remained on. This demonstrates brief
real stat application, followed by permission loss. The original reason for the
missed refresh is not established by the half-second trace.

The refresh worker previously waited on the very short-lived effect it refreshed.
If that effect expired, it could wait indefinitely while the admission worker
waited for departure. Event 5750403 now owns temporary admission flag 1055425233;
5750405 waits on that flag and rechecks eligibility before refreshing. Expiry can
therefore recover without repeating admission. Exit/death/victory cleanup and
the three-second initial admission remain. Aid logging adds admission, exact loss
flags, cap, tier presence and pending expected HP maximum.

The prior native allocation scan in
`.codex-temp/hadeon-progress-144/allocation-scan/flag-scan.json` covered 1055425233
among 598 event files and 194 parameter members with no conflict. Current authored
references use it only for this admission, diagnostics and broad encounter cleanup.


Verification and reversibility
------------------------------

The diagnostic tests use the workstation's existing Lua DLL with mocked game APIs;
they do not qualify Havok Script execution. Six tests cover eligibility, preserved
session files, trigger/history/post/rearm behavior, bounded hooks/captures/bytes/time,
disabled mode and failure containment. Nine encounter source tests include actual
authored refresh logic recovering after effect expiry and clearing on exit.
Aid and deflect source regressions also remain required before staging.

Native event candidate:
`.codex-temp/event-builds/1790548433518758300/receipt.json`.
Only events 5750311, 5750403 and 5750405 differ; event order, file metadata and other
runtime event files are unchanged. Coordinated runtime/source acceptance is recorded
in `.sovereign/backups/movement-diagnostics-147/events-accepted.json`.

Pre-change HKS and map/source backups are in
`.sovereign/backups/movement-diagnostics-147/`. `movement-instrumentation.patch`
there reverses only the HKS diagnostic changes. Check it with
`git apply --reverse --check .sovereign/backups/movement-diagnostics-147/movement-instrumentation.patch`
before applying; overlapping future edits require review. A source invariant check
also verifies that removing the diagnostic block and tagged observation calls
leaves pre-change gameplay code identical.

For a simple off switch, set `sovereignMovementCaptureEnabled = false`, then
requalify, sync and deploy a new version. Aid diagnostics remain independent.
For full removal, reverse the reviewed instrumentation patch. Restore normal
first-entrance behavior by removing the marked 1055420935 OFF write in 5750311
and rebuilding/qualifying the event file. Keep the separate aid-admission fix.
Do not restore the whole event backup over that fix or later edits. Retained
1.4.6 stage remains available for a deliberate full-build rollback.

All 20 focused source tests passed: six diagnostics, three aid, two deflect and
nine encounter tests. Repository preparation, version, whitespace, report link and
rollback dry-run checks passed. Native player qualification reused unchanged
assets/tools with refreshed HKS guards:
`.codex-temp/player-qualifications/1790548661670930500/receipt.json`.
Editor handoffs completed:
`.sovereign/handoffs/a61b52bc295b4cbab6b5159a83b9b049/receipt.json` and
`.sovereign/handoffs/5773c0968ad6400a82790f126c410834/receipt.json`.

Full main package: 75 files, with only player HKS and the Graveyard event binary
changed from 1.4.6. The other 73 files, including audio, regulation and the subtitle
test binder, are byte-identical. Prepared receipt:
`.vdb/prepared/954ad2d8b8ff4e1da48bbc4f10cbf0aa/receipt.json`.
Finalization completed:
`.vdb/finalizations/53594dc961084482a7f93b05f97f65ea/receipt.json`.
Build `719d09d99f9a82c2e142ad3e`, request `ef574870-0131-4f8a-a697-f6d4c307e0ee`,
profile `SkC-QjDMc`: enabled, deployed, verified with no differences. An independent
SHA-256 read matched all 75 live files; evidence is
`.sovereign/backups/movement-diagnostics-147/live-verification.json`.

Fresh 1.4.6 live logs supporting the aid finding are preserved in
`.codex-temp/movement-review-20260927/Sovereign-hadeon-aid-146-active-session.log`.
Restart the game before testing. Gameplay acceptance, diagnostic performance and
confirmation of the movement cause remain pending.
