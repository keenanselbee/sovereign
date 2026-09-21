# Opening deflect window: one extra frame

Implemented locally on 2026-09-19 at the author's request. The opening deflect
window is now 13/60 seconds (approximately 216.7 ms), previously 0.2 seconds
(12 frames at 60 FPS). This is a timing trial; in-game acceptance remains Pending.

## Scope

Changed only the end time of 38 type-66 events applying effect 102001, starting
at zero and previously ending at 0.2 seconds. The events are in the 19700-series
opening guard animations, with IDs ending in 0 or 1:

| TAE | Changed events |
| --- | ---: |
| a00 | 8 |
| a02 | 8 |
| a03 | 8 |
| a10 | 2 |
| a12 | 2 |
| a13 | 4 |
| a15 | 6 |

The 0.1- and 0.066667-second repeat-attempt windows and separate 0.133333-second
windows are unchanged. No HKS, behavior graph, regulation, stamina cost, reward,
effect parameters, motion clips or cooldown changes were made for this trial.
An extra 1/60 second allows a slightly earlier Block press; it does not retroactively
deflect damage that arrived before the input. Time is authored in seconds rather
than by counting rendered frames.

## Verification and recovery

Before editing, all seven loose files and the packed animation binder matched
their saved DSAnimStudio counterparts. No active `c0000*.dsaproj` was present.
Inputs were backed up and hash-checked again before acceptance.

Unchanged SoulsFormats serialization preserved every decoded TAE field, record,
event byte, group relationship and timing. `a00.tae` also roundtripped byte for
byte. The other six files were logically equal with serialization/layout changes;
the unchanged-roundtrip byte-size differences were -80, -240, -688, -672, -736
and -640 bytes for a02/a03/a10/a12/a13/a15 respectively. These are not gameplay
changes; no byte-identical TAE claim is made for those six files.

Each edited TAE was reopened and compared against the exact expected decoded
result, with only the planned endpoints changed. An unchanged specialized Witchy
ANIBND repack preserved every member payload and binder metadata. The edited
packed binder retained all header/member metadata and order, with seven changed
members and 658 byte-identical members. Packed edited TAEs matched the loose
candidate bytes and the expected decoded data.

The coordinated native player qualification passed after acceptance, including
source-to-binder consistency and unchanged behavior-graph roundtrip. Its receipt
is `.codex-temp/player-qualifications/1789869534315726900/receipt.json`.
These checks do not establish in-game timing or controller behavior.

Evidence, tools, exact event indices and rollback inputs are retained under
`.codex-temp/deflect-window-plus-one-20260919/`, including `timing-patch.json`,
`packed-verification.json`, `guards.json` and `acceptance.json`.

Accepted animation binder SHA-256:
`c69b0635db0fefce72a0f47482b6e2ed44e7dc62921b6009936ffaf99cc9c70b`.
Original binder SHA-256:
`a36f192c3a0918e7bbf70507c0b5dbd685bde842a22daf1b03749df75e2c6de0`.

The repository's loose sources and runtime binder were updated together. The
subsequent authorized [1.0.0 deployment](DEPLOYMENT-1.0.0.md) synchronized the
saved editor copies and verified the staged/live files. The original trial receipt
records its earlier repository-only acceptance. No Nexus description change or
in-game acceptance is implied by deployment.

Test ER-047 with deliberate early/on-time/late presses, one/two-handed weapons,
shields, rapid attack chains, repeated Block taps, and Hadeon/Malenia encounters.
Verify existing stamina costs, charge rewards, Malenia healing suppression and
Hadeon thorns remain intact. Record actual observations before marking it Passed.
