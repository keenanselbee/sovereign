Hadeon dialogue gain and entrance proximity 1.4.8
=================================================

The author requested a +2 dB bank gain and proximity-started speech, explicitly
including all opening variants. The shared entrance event now waits for the
player to be within 12 metres of Hadeon before queueing either the full first
monologue or the four-line repeat pool. Existing room/fall/map/death guards apply.
The 12-metre radius is an initial calibration choice, not a measured subtitle
activation boundary. Subtitles remain disabled for the existing AI isolation test.

The 0.7-second settling delay remains a minimum after entrance admission. Approaching
later does not add another delay. Once speech starts, radius no longer gates it;
moving away within the room does not stop or restart playback. First-monologue
combat still follows actual playback by 13 seconds; hits still engage combat
early. Normal repeat combat is enabled before waiting for voice proximity. The
temporary 1.4.7 first-entrance override remains, so current testing hears the full
monologue every encounter. Earned aid and other dialogue triggers are unchanged.

The actor mixer receives Volume +2 dB. Original/converted recordings, all 49 WEMs,
voice routing, attenuation, spatialization, reverb and timing are preserved. Native
readback verifies one mixer property addition; bank DATA, DIDX and BKHD are identical
to the prior bank. HIRC retains 263 objects and 114 events. Source build validation
requires the accepted gain; rebuilding from preparation retains the mixer property.
The candidate is 22,419,453 bytes, SHA-256
`124ba5b16918cede0cf20fbfb368cf0cabefc87040b3fb93cf9feccf923c6efd`.

Verification
------------

Twelve encounter source tests pass, including first/repeat admission, the settling
delay, no speech outside the radius, continuation after moving away, combat timing,
and cancellation while awaiting proximity. The repeat test removes only the marked
temporary first-entrance override in the mock to exercise the normal repeat branch.
Mocked source tests do not prove native game behavior.

Event candidate `.codex-temp/event-builds/1790549158005583800/receipt.json` changes
only event 5750311. All event order/metadata and other runtime event files are
preserved. Acceptance/rollback copies are under
`.sovereign/backups/hadeon-proximity-148/`; bank/source backups are under
`.sovereign/backups/hadeon-gain-148/`.
Audio candidate and native readback are in
`.codex-temp/hadeon-monologue-audio/revision5/gain-148/`.

The previous movement diagnostic instrumentation remains unchanged, including its
1.4.7 filename/header tag; distinguish this 1.4.8 package by deployment receipt
and session creation time. No movement gameplay code or aid logic changes here.
Keep the 1.4.7 stage for full rollback; remove the proximity wait or adjust its
single radius in event 5750311 only through a rebuilt, verified new deployment.

Repository preparation, version, whitespace and documentation-link checks passed.
The event source/runtime handoff completed at
`.sovereign/handoffs/f402722c8aaf4c4cbdd43cd8e44131a4/receipt.json`.
Audio has no configured external editor mapping; accepted runtime/source validation
is recorded in `.sovereign/backups/hadeon-gain-148/accepted.json`.

Full main package: 75 files; only the bank and Graveyard event binary differ from
1.4.7, with 73 files unchanged. Prepared receipt:
`.vdb/prepared/4c52561ca077400c981a639630206e75/receipt.json`.
Finalization completed:
`.vdb/finalizations/6998a271802f4978b073073f870f6b19/receipt.json`.
Build `4467a23c5441bb24da34be62`, request `c0c5093f-4c49-419e-aaf9-02b6644dbfb9`.
Independent SHA-256 checks matched all 75 live files; evidence is
`.sovereign/backups/hadeon-proximity-148/live-verification.json`.
In-game loudness, mix headroom and the chosen radius remain acceptance checks.
