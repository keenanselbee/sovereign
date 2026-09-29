Movement recorder refinement, 1.6.5
===================================

The author reports that the repeated one-to-two-second movement stops became
rare around the 1.5.6 recorder repair. This investigation does not establish
that the movement fault is fixed or that logging caused the improvement.


What changed when recording began working
-----------------------------------------

The retained 1.5.5 and 1.5.6 HKS payloads differ in exactly two lines, both
write/flush return checks in ModMovementCaptureWrite. The pre-edit HKS backup
under .sovereign/backups/hadeon-followup-156 matches the 1.5.5 payload.
Twelve pre-fix logs abort after their header at the old flush return check,
line 20459, with a nil error reason. The error is caught; Update continues,
but per-frame recording and movement summary sampling stop. The first retained
long post-fix log, 20260927-195417, contains heartbeats and seven captures.

The old check rejected a no-value flush return. The repair accepts nil,nil while
still rejecting explicit false or an error. Pre-fix logs alone cannot distinguish
nil,nil from false,nil; working post-fix recording supports the return-mismatch
explanation. Neither change adjusts movement decisions or animation dispatch.
No observer variable feeds those decisions. The diagnostic rescue timestamp is
assigned after the rescue action and only used for logging.

The other six changed package files were Hadeon's event file, four text binders
and the Hadeon audio bank. Player animation/behavior archives, regulation, maps
and AI files did not change. Package evidence:
.vdb/prepared/0681520656ed494dac0bcf1a0ed95282 (1.5.5) and
.vdb/prepared/0cc4a05ea46c492f9906e3e87aee147e (1.5.6).

Successful capture adds native reads, string/table work and batched file writes
before the rest of each Update. A timing-sensitive observer effect is plausible,
not demonstrated. Full per-frame recording stops again after twelve captures;
continued smooth play after that point weakens continuous logging overhead as
the sole explanation. Other play conditions and an early-session timing effect
remain possible. A future controlled comparison with only the diagnostic switch
changed is the cleanest way to test causation; it was not performed here.


Recent observations and filtering
---------------------------------

Nine recent movement files contain 79 trigger windows: 40 guard/deflect, 15
jump/fall, nine throw/critical contexts, five attacks, five damage reactions,
three startup windows and two sprint turns. These are contextual classifications,
not proof that each pause is harmless. The two sprint-turn cases request
W_Dash180 after a brief processed-input zero, recovering after roughly 0.9 and
0.7 seconds. The older recorder did not capture the TurnAngle used by that branch.
The latest detailed file reaches its twelve-capture limit at 106 seconds despite
a longer encounter. The current trigger is too broad to cover long combat well.

Schema 4 records turnAngle using the same hkbGetVariable("TurnAngle") read as
ExecDashTurn, plus current throwing state, expectedPause, filtered, rawStall and
filteredFrames. Optional read failures remain isolated and visible in the log.
The legacy filename prefix stays stable; the header identifies recorder 1.6.5.

Fresh event hooks allow bounded expected-action windows: attack 2.5 seconds,
deflect 1.25, damage/jump/fall two, and throw five as a fallback if the throwing
probe is unavailable. A successful throwing-state read uses the actual active
state and stops filtering immediately when it ends. Fresh Idle, Stop or Move
callbacks end action grace, as does resumed movement. Old scalar callback names
cannot suppress a capture. Sprint stops/turns are deliberately left observable.
Continuous positive-input idle/zero-speed lasting six seconds bypasses filtering,
even if an action remains active. The ordinary 0.25-second trigger then applies.
This can still capture unusually long legitimate actions; it avoids unlimited
suppression of a stuck state.

Filtered frames remain in the ring and post-trigger windows, and heartbeat
records expose filtering. The existing limits remain: 180-frame history, three
seconds after a trigger, twelve captures, thirty minutes and eight MiB. Only
capture admission changes; gameplay movement logic and speeds are preserved.
Disable sovereignMovementCaptureEnabled and requalify/sync/deploy to turn the
recorder off. Pre-edit files are in .sovereign/backups/movement-filter-165.


Verification and delivery
-------------------------

Eight recorder mock tests pass, including fifty ordinary action windows without
spending capture allowance, stale context rejection, immediate capture after
return to locomotion, ongoing/ended criticals, prolonged-action escape, sprint-turn
capture and optional TurnAngle failure. These mocks do not establish HKS engine
performance or in-game disappearance of the movement problem.

All HKS outside the reversible movement capture block matches the pre-task
1.6.4 backup exactly. Native player qualification reused unchanged assets with
fresh HKS guards: .codex-temp/player-qualifications/1790625057340361400/receipt.json.
Repository preparation checks pass for 78 owned runtime files; release metadata,
edited-document links and scoped whitespace checks pass. No generic Lua result
is treated as native HKS performance qualification.

Guarded editor sync completed under
.sovereign/handoffs/2a16d79ad0c14ef5a7263751229ca5e3/receipt.json. The complete
79-file package differs from prepared 1.6.4 only in c0000.hks. It retains the
separately prepared Vortex marker correction; that work is not a movement fix.

Prepared receipt: .vdb/prepared/04e5d0df15f0421a96df1e1f63bc0513/receipt.json.
Protocol-3 finalization is pending while Vortex is closed:
.vdb/finalizations/f2bba1742f24429cad7b152678fb57c1/receipt.json, request
cc5558b3-69db-48af-8fbb-12fd9810df3a, build b4aa89572cf1073f33447bc8.
This is queued, not completed deployment. The earlier 1.6.4 request is retained;
resume the existing receipts after Vortex processes them rather than resubmitting.
