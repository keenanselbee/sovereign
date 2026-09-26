Sovereign 1.2.8 hallway and diagnostic regression
================================================

Author observations, 2026-09-24
------------------------------

After testing 1.2.8, the author reports no hallway proximity lights and another
brief movement stop a few seconds after leaving a room. They clarified that
they did not enter Hadeon's boss room. Hadeon is alive and the crystal intact.
Fixture visibility is uncertain; the earlier visible-but-unlit answer was qualified.
This is not a new test of blessing activation or the 60-second boss-room sequence.

Read-only findings
------------------

The live HKS, map, map event, regulation, common SFX binder and Script Exposer DLL
match the immutable 1.2.8 package. The loader log was updated at 20:48:28 local,
after deployment. The aid log was created at 20:48:43 but is empty. The movement
log is still from 19:55:40 and contains only zero-HP samples; it cannot explain
this incident. Copies are retained in `.codex-temp/lighting-aid-regression-1.2.8/`.

The aid logger is not arena-gated. It opens its file, then evaluates the full
resource snapshot before its first write. A caught error disables the logger
without recording the error. Thus an empty file does not prove that the aid
function was never reached, or identify which read/write failed.

Hallway regions and progression gates were preserved. The changed path is empty
model-SFX rows plus CreateAssetfollowingSFX instead of automatic model effects
and EnableAsset. All 125 placements, selected dummy sockets and packed effects
were verified in the prior native pass. Rendering/attachment is not established
by those checks. No instruction argument-order error was found in the installed
EMEDF definition. Saved crystal-off behavior does not match the reported state.

The map constructor now initializes 673 events versus 355 before 1.2.8. The room
alone uses 568 per-position workers. The hallway initializer follows them. This
is an additional test target, not proof of an engine event limit; no such limit
was established. Consolidating to one controller per room position could retain
individual ignition while reducing this overhead substantially.

Next bounded diagnosis
----------------------

Write/flush a basic diagnostic heartbeat before resource probes; retain the
actual caught error and isolate optional reads. Put player-only movement capture
before custom callbacks and record the last callback reached, so an earlier
failure cannot prevent all useful logging. Avoid changing speed/jump again.
For hallway lights, first distinguish trigger/event execution from effect
attachment on one existing group, before extending a replacement to all 125.
A vanilla automatic-effect control or paired unlit fixture is the fallback if
explicit attachment fails. Keep the 60-second design while reducing room workers.

No runtime files changed or new version deployed during this investigation.
