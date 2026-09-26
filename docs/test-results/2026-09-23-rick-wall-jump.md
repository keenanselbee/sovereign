# Rick transition and wall-jump trial, version 1.0.6

The author reported that the previous encounter transformed successfully without
a fade and placed Rick at his original spawn. They suspected the threshold had
been crossed during a critical. They also reported that the earlier unavailable-
backstep fix did not resolve the intermittent standing pause. The exact tested
build/save, input device and reproduction sequence were not supplied. These are
user observations, not independently reproduced game tests.

The author approved a 25% threshold, the soldier vocal auditioned as 431008102,
and spawning Rick at the outgoing soldier's position. They also approved fixing
repeated scheduling in the wall-jump helper. Version 1.0.6 implements those changes;
ER-057 through ER-060 and ER-062 remain Pending for in-game acceptance.

## Wall-jump behavior

Previously, continued airborne wall contact with jump held could issue ladder idle
again each update and replace wallJumpFrameCount before its two-update delay
expired. The pending branch now owns that delay and excludes new requests until
execution. Landing clears the pending state as before and exits the temporary
ladder pose through normal movement/idle handling when still alive and on foot.
Ordinary ladder states are not affected without a pending wall-jump request.

The targeted checks execute the current ModJump control flow translated to Python
with mocked engine calls. They cover continued held input (one idle per scheduled
jump), release while pending (scheduled jump still finishes), landing with and
without movement (cancel and recover), and mounted exclusion. The same harness
checks the enemy critical marker's set/clear branches and excludes other enemies
and Rick's second phase. Newly introduced engine-call aliases were checked against
each HKS file's own definitions. These are control-flow checks, not Havok Script
compilation, engine scheduling or in-game animation tests.

## Rick and native checks

The threshold is latched at 25%; existing immortality handles oversized damage.
The outgoing actor remains invincible while its HKS critical marker clears.
Fade/audio are local to living host or entered white-phantom participants in the
map, without requiring continued entrance-trigger occupancy. Rick is enabled and
updated before warping to phase one; phase one remains enabled until the warp has
had two frames to process. The local player emits the selected native vocal so
removing the outgoing actor does not stop it. Reveal/music wait for the native
vocal's duration and pitch variation. Stats, rewards and final defeat remain intact.

DarkScript candidate 1790186234735840700 compiled successfully. Independent native
decode found changes only in events 18002860 and 18002861, with no metadata changes.
Every other shipped event was equivalent. Candidate bytes were accepted into both
the repo runtime and saved source companion with source/baseline hash guards.
Player qualification 1790186237612330500 reused the unchanged native animation and
behavior evidence with fresh HKS guards. Version and preparation checks passed.

Scratch evidence: `.codex-temp/rick-walljump-fix-20260923/`, including before-copies,
focused diffs and `check_logic.py`. Native audio routing and previews remain under
`.codex-temp/rick-audio-candidates-20260923/`. No new sound-bank asset or parameter
row was introduced. Audibility, exact warp position, critical completion, fade
recovery, arena unlock and the original pause still require gameplay testing.

## Source acceptance and deployment

Both guarded editor handoffs completed: events
`a68557d5bdbe4973ae079aa627600b66` and player files
`19ba74e42bd44504a9c70547d8d35455`. The two HKS files and event source/binary
match their saved Script workspace copies exactly.

Prepared package `.vdb/prepared/c70e761aa4554448b5abe791d5f13be2/receipt.json`
contains exactly three changes against 1.0.5: `mod/action/script/c0000.hks`,
`mod/action/script/c9997.hks`, and `mod/event/m18_00_00_00.emevd.dcx`.
All other package files, including the existing external DLL, are unchanged.

All-profile finalization was submitted once for build `59961270474bde53b1036dd6`
with request `fe91c889-eab0-4167-9271-a62c9787ce83`. Resume its existing receipt
at `.vdb/finalizations/rick-walljump-1.0.6/receipt.json`; do not resubmit.
The request remains pending: Vortex is not running and its bridge snapshot is
stale. The three live game files still match 1.0.5, so 1.0.6 is not deployed yet.
Open Vortex to allow the queued request to run, then refresh this receipt and
verify deployment before performing the pending gameplay tests.
