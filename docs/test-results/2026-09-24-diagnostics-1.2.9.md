Sovereign 1.2.9 diagnostic findings
==================================

Author observations
-------------------

The author reports that boss-room incremental lighting worked well, hallway
proximity lighting still did not activate, and boss-room entry gave neither
gradual stats nor the player aura. This observation does not establish victory,
crystal, retry or frame-time acceptance for the room sequence.

Log evidence
------------

Both current logs have the 1.2.9 startup marker and were last modified at 21:38:47
local on 2026-09-24. Copies are retained under
`.codex-temp/diagnostics-1.2.9-review/`.
The movement trace has 280 samples; 279 report the preceding Update checkpoint
as ModHadeonAid. The aid trace has 115 samples; every sample reports `attempt to
index a function value` at c0000.hks:20192, the pending-state diagnostic field.
At t=30.786 to 31.806, processed forward input remains above 0.9 while actual
movement speed is zero. Both logged forced-walk effects, 4101 and 1626974, are
absent throughout this trace. Other zero-speed intervals include combat/damage
and are not by themselves proof of the reported involuntary stop.

Confirmed source defect
-----------------------

The script's final `_G` metatable returns `dummy` for missing globals. Assigning
nil to a global removes its entry and therefore reads back as a function.
`sovereignAidCalls` is never initialized before `(sovereignAidCalls or 0) + 1`,
so the new diagnostic counter fails immediately. After initializing that counter,
`sovereignAidStage = nil` breaks the numeric stage check; pending=nil likewise
breaks both the aid state machine and its diagnostic field. These are independent
of entering the arena. The aid callback fails before its permission/aura path,
and subsequent Update work (rescue update, HP/button/magic helpers, frame count)
is not reached. This explains the missing aid and is a strong movement suspect,
but the older movement report predates the aid feature and remains unproven.

A scratch-only candidate explicitly initializes the counter, uses -1 as the
initial stage and false for no pending recalculation, updating matching checks.
Using the actual global fallback reproduces the original failures; the candidate
passes the existing ramp/withdrawal, resource-lag and timeout scenarios with that
fallback installed. Previous mock tests lacked this global behavior and missed
these failures. No runtime file has been edited or deployed in this review.

Hallway effects
---------------

The logs do not report hallway region/event execution. The attachment change in
1.2.8 remains the main regression boundary; its exact engine failure is not yet
established. Do not alter the working room sequence or claim an event-capacity
limit from these observations. Diagnose one hallway controller's trigger and
spawn path separately after correcting the confirmed HKS failures.
