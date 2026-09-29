Hadeon routing, dialogue history and room progression
====================================================

Author-approved follow-up to 1.5.9, 2026-09-28. Implemented as 1.6.0;
deployment and game acceptance are separate and recorded below.

Vortex correction
-----------------

The author reported idle pauses when Hadeon tried to use Vortex. Version 1.5.9
requested 3080-3083, outside enemy HKS normal attack dispatch 3000-3039. Those
IDs also lacked global names and callbacks, and their graph event-name additions
had no matching metadata. Archive readback had not checked these integration
requirements. Correct the private routes using native-supported 3030-3033,
preserving the original 3028 and the agreed speeds, weights, chances and cue.
Native dispatch, callback, registration and graph checks must accompany readback.

Repeat-dialogue history
-----------------------

The author heard `hadeon-entrance-unyielding.wav` on consecutive death/respawn
attempts. Source selection excludes the previous line, but the existing logs
cannot identify the failed history transition. The temporary common load reset
now preserves flags 1055420940-1055420951 regardless of its death bypass.
First-encounter receipts and loss progression retain their existing test-reset
rules. This hardens persistence; it does not establish the original repeat's cause.

The removable `BEGIN REVERSIBLE HADEON DIALOGUE TRACE` block in player HKS has
one Update call and an enable switch. It observes host-player state every 0.1s,
including zero HP, and writes only transitions, capped at 1,024 rows per script
instance. It records previous/current pool-memory bitsets, selected voice,
pending requests, active playback, death-reload marker, confirmed death and
first-entrance receipt. Flags use decimal strings assembled from small suffixes
to avoid HKS numeric precision loss. Errors disable the trace without entering
gameplay logic. No progression or dialogue flags are written by the logger.

Logs use the movement capture's session filename plus `.dialogue.log`, or
`Sovereign-hadeon.dialogue.log` if no capture exists. Bit order is ascending:
entrance 0940-0943, half-health 0944-0947, kill 0948-0951, selection 5200-5215,
requests 5216-5222, all prefixed 105542. Entrance bits correspond to unyielding,
promise, another-defeat and hunger. A sampled trace can miss brief intermediate
transitions and does not prove a voice was audible; interrupted starts count as
spoken under the existing selection policy.

Lighting contract
-----------------

With previous counted deaths d capped at ten and boss remaining HP fraction h:
`b = 0.075 * d`; illuminated positions = `floor(96 * (b + (1-b) * (1-h)))`.
The baseline is fixed for an attempt. The stable shuffled order and existing
flame/light assets remain; lit positions latch until the attempt resets.
Ordinary lit fixtures use the full normal preset. Death freezes the scene;
retry uses the new baseline. Victory lights everything; crystal presentation
and the established fade retain priority. No new light assets or HKS polling
are needed for lighting.

Verification and recovery
-------------------------

Core backups: `.sovereign/backups/hadeon-followup-160/manifest.json`.
Vortex and lighting sources have separate bounded backup manifests alongside it.

Completed checks so far:

- All 43 combined encounter, death-load and progression source checks pass with preserved pool history.
- The mocked dialogue trace checks transitions, exact string IDs, death capture,
  write/read failure containment, disable switch and row limit.
- Seven existing movement/player diagnostic checks pass.

- Native Lua checks pass for 800 HP-boundary/chance selections and actual route registration.
- Graph round-trip preserves 2,268 original objects, adds 12 route objects, and
  keeps both event arrays at 1,366 entries; HKS callbacks and global registrations
  validate. Original 3028 and the other 277 original TAE records remain intact.
- Accepted Vortex candidates have a guarded recovery receipt at
  `.sovereign/backups/hadeon-followup-160/accepted-vortex/receipt.json`.
- Final player-script editor handoff:
  `.sovereign/handoffs/5f272da652e14a5e93a6321030d00865/receipt.json` (one file).
- AI and c2500 editor handoff:
  `.sovereign/handoffs/569c283cc7c24ec59a61c552635b204b/receipt.json` (three files).

- Native event build `.codex-temp/event-builds/1790585814641912200/receipt.json`
  changes only common event 50 and m18 events 0, 5750370, 5750401, 5750404,
  5750406 and 5750407. Unrelated events and map outputs are preserved.
- Lighting source simulation passes for all eleven death tiers, HP progression,
  normal presets, rescue, death freeze/recovery, retreat, victory and crystal fade.
  Two parameterized tier banks fit native condition-group limits. HP readiness
  excludes unloaded/pre-spawn zero HP; existing victory flags light everything.
- Event candidate recovery:
  `.sovereign/backups/hadeon-followup-160/accepted-events/receipt.json`.
- Repository preparation checks and version metadata validation pass for 1.6.0.

- Event editor synchronization completed: four source/binary files via
  `.sovereign/handoffs/26a9cf27192c407f91dd1b7b9cd33675/receipt.json`.
- Additional lighting checks cover pre-spawn HP0, exact threshold crossings and
  rescued zero-HP recovery. Scoped whitespace and local Markdown links pass.
- Prepared complete main package:
  `.vdb/prepared/4ff6014ec7874875b3a97f5442e02795/receipt.json`.
  All 79 paths match 1.5.9, with exactly six changed runtime files: player HKS,
  common/m18 events, Hadeon battle AI and the two c2500 animation/behavior binders.
  No files were added or removed; external dependencies remain unchanged.
- Protocol-3 finalization submitted:
  `.vdb/finalizations/45c37398209148d591b7fc82080b5790/receipt.json`,
  request `a4bae3ea-b5b4-4b24-a3e6-0fa089253a49`, build
  `ba18e738859040ccc36656fa`. Finalization completed on profile `SkC-QjDMc` with main enabled and deployed.
  Independent SHA-256 comparison verified all 79 prepared files against both
  the immutable stage and live game paths. No added/removed paths or overrides
  were introduced. The previous 1.5.9 stage remains available for rollback.
In-game routing, speed, warp continuity, dialogue repetition and lighting
acceptance must be observed in the deployed build before marking them Passed.
