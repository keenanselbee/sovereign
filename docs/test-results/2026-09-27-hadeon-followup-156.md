Hadeon encounter follow-up 1.5.6
================================

The author confirmed the private waiting AI works in 1.5.5. This follow-up keeps
that AI, the first monologue handoff, existing map geometry, aid progression and
temporary title-load reset. New behavior still requires game acceptance.

Changes
-------

Repeat entrances hold with command 1900 and relocate after one second to the
nearest of eight clear destinations, then face the player and release normal
combat. Early damage releases immediately without a delayed warp. The voice
retains its proximity gate and minimum settling delay; the normal one-second
repeat wait already supplies settling. Death or arena departure cancels the
handoff. The first monologue retains its 14.6-second cue from actual playback.

The another-defeat entrance and thousand-times kill line require the third saved
combat loss. The loss worker increments before requesting dialogue so the third
death itself can select thousand-times. Each pool filters eligibility before
excluding its last started line. The other independent histories are unchanged.

Player death below the arena in region 18002367 does not request a kill voice or
subtitle. The dispatcher also discards an already queued kill request there,
without advancing dialogue history. The fatal fall still counts toward aid and
line eligibility. This is the existing geographic fall proxy, not a verified
engine-reported damage cause; unusual non-fall deaths in that region are also
silent. Test bridge falls in game before treating this classification as complete.

The worthier and another-falls wet recordings replace need-another and whisper
at indices 11 and 13. Voice/stop/TalkParam/TalkMsg IDs remain stable. Their full
lengths are 5.746854 and 5.552458 seconds, with event windows of 5.77 and 5.58.
Dry waveform tails place the initial subtitle ends at 2.6 and 4.0 seconds;
these remain calibration estimates. Original wet and dry WAVs are preserved.
The existing -1 dB conversion and +2 dB shared mixer gain remain.

Deflection tutorial and inventory-note text now explain that holding a weapon
in both hands reduces stamina consumed by deflection.

All twelve inspected movement logs aborted after their header at the flush
return check, with no error detail. A successful no-value return is the suspected
API mismatch; the logs alone cannot distinguish it from false,nil. Write/flush
checks now accept nil,nil;
explicit false, an error return and thrown errors still stop the capture safely.
The existing capture limits and disable switch remain. The change addresses the
suspected recorder mismatch and preserves explicit false failures; a fresh game
log must verify it. It does not establish the cause of movement pauses.

Validation and recovery
-----------------------

Pre-edit runtime/source backups and acceptance hashes are under
`.sovereign/backups/hadeon-followup-156/`. Keep these and the guarded handoff and
VDB receipts. Diagnostic removal remains the existing
`sovereignMovementCaptureEnabled = false` switch followed by qualified player
sync and a newly versioned deployment.

34 encounter/load-reset tests, the progression simulation and seven movement
recorder tests pass. Simulations cover repeat destinations, timing, both early-hit
worker orders, cancellation, eligible no-repeat pools, third-death selection and
silent fatal-fall progression. These are source/mocked checks, not engine tests.

Native audio build and separate readback passed under
`.codex-temp/hadeon-followup-156/audio/output-final/validation.json`: BKHD 135,
263 HIRC objects, 114 events and 49 embedded media. Exactly two spoken voices,
two silent carriers and their four graph media sizes change; the other 45 media
and all routing/event identities are preserved. The bank is 22,965,469 bytes,
SHA-256 `3ebda2cd8d90bc805383f107e8b86795e65bc7c7b4630fcbecf86d63943e8306`.

Native coordinated-player qualification is
`.codex-temp/player-qualifications/1790560178638925300/receipt.json`.
Editor synchronization for the HKS fix completed through
`.sovereign/handoffs/8da11acecacf4dd3b589264b6dd2503d/receipt.json`.
This guards HKS inputs; it is not a native Havok Script execution test.

Native event candidate `.codex-temp/event-builds/1790560661954211800/receipt.json`
changes only 5750302, 5750311, 5750312 and 5750420, preserving event order,
file metadata and all eight other runtime event files. The source hash was
rechecked before acceptance; one intermediate build was correctly rejected for
source drift and was not accepted. Event sync completed through
`.sovereign/handoffs/1976b078fe3d47c2bee1b0382a158c44/receipt.json`.

The inventory-note candidate passes a complete binary FMG comparison and synced
through `.sovereign/handoffs/7c3d09700af64ef4a96731b4454e95b4/receipt.json`.

The replacement subtitle text is "Find thee a worthier servant." and
"Another falls. Thy prison stands." It was recovered with local transcription
of the dry recordings; check exact wording and timing in game. No recordings
were sent to an external transcription service. The temporary transcription
environment, downloaded model and evidence remain under the ignored
`.codex-temp/hadeon-followup-156/` directory.

Three menu candidates (`1790560972599088400`, `1790560978380892600`,
`1790560984546111400` beneath `.codex-temp/binder-candidates/`) pass complete
binary FMG preservation comparisons. Each changes only tutorial 302400 and
TalkMsg 999802100/999802300. The item candidate changes only GoodsCaption 9106.
The unchanged TalkParam IDs and single-cue layout require no regulation/ESD edit.

Text synchronization completed through
`.sovereign/handoffs/4f31317c50914876b45774dfcb8b0128/receipt.json`, including
recovered binary FMG source snapshots. All four scoped handoffs are complete.
Repository checks, version checks, edited Markdown links and whitespace pass.

Deployment completed for 1.5.6 through prepared receipt
`.vdb/prepared/0cc4a05ea46c492f9906e3e87aee147e/receipt.json` and finalization
`.vdb/finalizations/d9670190e8964030847776df53ce813a/receipt.json`.
Build `a0e88383b5497abbe8d00b2c` is enabled and verified deployed in profile
`SkC-QjDMc`. Exactly seven runtime files changed from 1.5.5; the 76-file package
has no added/removed paths. Independent SHA-256 checks of all 76 installed files
match, recorded in `.sovereign/backups/hadeon-followup-156/live-verification.json`.
Gameplay acceptance of this follow-up remains pending.
