Movement event-state tracing, 1.6.6
==================================

The author reports frequent movement stops again. The 1.6.5 log from
20260928-135741 contains two mid-movement event requests with a fresh
ResetEventState speed reset (lines 176 and 2777). Both have eventRequest=1
and eventAnim=-1. The second returns to movement about 2.77 seconds later.
These identify an event-animation path, not the specific requesting mechanic.
Other recent captures include ordinary guard damage, jumps and rolls; capture
counts are not counts of confirmed unexplained stops.


Changes and limits
-------------------

Recorder 1.6.6/schema 5 adds observation hooks to 278 existing Event callbacks
and two existing playback-request gates. Activation is recorded before the
speed reset. Entry/exit snapshots retain callback name, animation ID, playback
request, command ID, input, scripted speed, movement cancellation, event flag
and object-action interpolation time. Each optional read is isolated.

Event update names/timestamps distinguish a continuing event from a stale
locomotion callback. Existing deactivate callbacks are recorded explicitly.
For states without a deactivate callback, follow the last event update and
the next existing locomotion callback; no new engine callback is installed.
The native requester may still be unidentified if its IDs are unavailable.

The observer issues no gameplay writes, dispatches or cancellations. Removing
only these additions reproduces the pre-task HKS exactly. The existing
sovereignMovementCaptureEnabled switch disables these hooks and probes.
Existing file-size, capture-count, history and time limits remain unchanged.
The filename keeps its historical 1.4.7 prefix; use the header for recorder version.

This version also includes the previously requested local opening-sound fix:
event 5750362 retains sound 530181, its 0.1-second delay and one 450264 request.
The second identical 450264 request is removed. Original sound assets and all
other decoded event instructions/metadata are preserved.


Verification and recovery
-------------------------

All ten player-diagnostic checks pass, including activation snapshot retention,
disabled/inactive probe suppression, optional-read failure isolation, and coverage
of every ResetEventState caller before the reset. These are mocked Lua checks,
not native HKS execution or gameplay acceptance.

Native player qualification reused unchanged assets with fresh HKS guards:
.codex-temp/player-qualifications/1790630334261348600/receipt.json.
The sound build's independent decoded comparison proves exactly one instruction
removed from event 5750362:
.codex-temp/event-builds/1790629779228409400/local-acceptance.json.

Pre-task HKS, metadata and test backups plus the diagnostic-only patch are under
.sovereign/backups/movement-event-trace-166. The opening sound's earlier backups
are under .sovereign/backups/opening-sound-deduplicate. Restore through reviewed
source changes and the normal qualified handoff/deployment; never overwrite a
retained stage. In-game reproduction and attribution remain pending.


Delivery
--------

Guarded player/event editor handoffs completed:
.sovereign/handoffs/9c0070ffcff84f56bc3f5562849515d8/receipt.json and
.sovereign/handoffs/238787ddc74d4611b585ac176a7cc0b7/receipt.json.

Prepared package: .vdb/prepared/8d62450bbc204d1b9669b823e6520a7c/receipt.json.
Only c0000.hks and common.emevd.dcx differ from the complete 1.6.5 package.
Protocol-3 finalization completed through Vortex for the enabled profile:
.vdb/finalizations/57a90d1e129a4da6888f81013034ddbd/receipt.json, build
a17a1580f4bbb01a058b882e. All 79 installed files match the prepared hashes.
This verifies installation, not gameplay behavior.
