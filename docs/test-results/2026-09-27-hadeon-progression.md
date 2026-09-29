# Hadeon dialogue and progressive aid, 1.4.4

The author approved implementation and deployment of the complete recordings,
progressive encounter aid and special no-aid victory. Native/source verification
and deployment are separate from gameplay acceptance, which remains pending.

Version 1.4.5 corrects the fatal-fall exclusion described below: fatal bridge
falls during active combat now count. See the [correction](2026-09-27-hadeon-fatal-falls.md).

## Behavior

- The first tracked attempt has no arena stat or guard-stamina aid, beginner
  rescue in the boss room, 75%/50% Thorn Wards, or 25% wail/damage pulse.
  Rescue elsewhere and ordinary combat/deflection mechanics remain available.
- Each genuine combat death unlocks another 20% maximum HP/FP/stamina and damage,
  up to 100% after five losses. Existing parameter tiers also reduce guard stamina
  cost, reaching 0.5x at full aid. Three continuous eligible seconds precede the
  existing five-point steps every 0.5 seconds. Withdrawal still takes ten seconds
  and protects current resource percentages, damage and spending.
- First entrance is once per journey. Speech begins 0.7 seconds after admission;
  combat/music begin 13 seconds into the recording or immediately on an early hit.
  Hits do not stop the recording. Repeat entrances engage immediately and select
  one of four short lines after the same speaking delay.
- First half-health speech is once per journey, followed by a four-line random
  pool on later attempts. Half-health speech queues behind entrance speech and
  never pauses combat. Death speech preempts ordinary lines.
- Four player-death lines start on actual death, independent of the later return
  teleport. Rescue, retreat, entrance and fall recovery do not count as losses.
  A frame of fatal-hit resolution gives simultaneous Hadeon defeat precedence.
- Hadeon's defeat selects the normal warning or the no-loss remembrance line.
  The full recording tail is retained. Native corpse-bound subtitle behavior
  still needs an in-game check.
- A no-loss victory also grants Stormblessed Zweihander through existing item lot
  `10000320` (weapon `4045000`). The lot sets receipt `1055420250`; the event never
  pre-sets it. Persistent entitlement permits later delivery after an interrupted
  payout and the existing receipt prevents a duplicate Stormveil pickup.

Existing saves begin at the first tracked attempt; past losses are not inferred.
Already defeated Hadeon saves do not receive the new bonus retroactively. Journey
flags intentionally persist through reloads; their NG+ reset needs game acceptance.

## Ownership

| State | Owner |
| --- | --- |
| Saved failures 1–5 | `1055420930`–`1055420934` |
| First entrance / first half-health consumed | `1055420935` / `1055420936` |
| No-aid victory entitlement | `1055420937` |
| Current voice selectors | `1055425200`–`1055425215` |
| Pending voice requests | `1055425216`–`1055425222` |
| Room rescue guard / death latch / half-health latch | `1055425223`–`1055425225` |
| Victory capture / first entrance in progress | `1055425226` / `1055425227` |
| Voice / intro combat gate | Existing `1055422946` / `1055422947` |

Map events `5750311`/`5750312` own entrance timing and serialized playback.
`5750420`–`5750424` own loss counting, half-health requests, victory capture,
bonus delivery and the local rescue guard. Common `5750361` also clears that guard
after map departure. HKS reads the saved failure cap and direct rescue guard.
The [recording roster](../../src/audio/hadeon/recordings/README.md) owns current
wording and filenames; source recordings are preserved.

## Verification and deployment

Native flag-allocation scan checked 598 retained event files and 194 regulation
members with no collisions for the new saved/temp flags and event IDs. Evidence:
`.codex-temp/hadeon-progress-144/allocation-scan/flag-scan.json`.
Pre-edit event/HKS recovery copies are in `.sovereign/backups/hadeon-progress-144/`.

Event candidate `.codex-temp/event-builds/1790541442938319800/receipt.json`
compiled successfully. Independent decoded comparison preserved all file metadata
and unrelated events: only common `5750361` changed; m18 changed seven existing
events and added the five progression workers (83 to 88 events). All seven other
runtime event files remained byte-identical. Authoring-only `common_func` was not
accepted into runtime.

The audio handoff `.codex-temp/hadeon-monologue-audio/revision5/handoff.json`
pins all 32 original recordings and candidate inputs. Independent bank readback
matched 263 HIRC objects, 114 events and all 49 embedded WEMs. The regulation
candidate added 28 TalkParam rows and corrected five owned row names, preserving
all unrelated rows/tables and binder metadata. Three English text binders matched
their complete expected decoded FMG results. The talk binder changed only
`t999801800` group 1; its 16 selector branches were independently decompiled.

Local acceptance and recovery receipt:
`.sovereign/backups/hadeon-progress-144/accepted-inputs/receipt.json`.
Player qualification `1790541058287911800` reused unchanged native player assets
with fresh HKS guards; talk qualification `1790541634142938700` rebuilt owned
sources against their native companions.

Scoped checks passed:

- `test-hadeon-progression.mjs`: all sixteen selectors and full durations, priority
  and inactive-edge sequencing, half-health queue, loss exclusions/caps,
  simultaneous victory, saved entitlement recovery and duplicate reward guards.
- `test-hadeon.mjs`: eight encounter boon, fall, presence and first-attempt cases.
- `test-hadeon-lighting.mjs`: arena lighting, all 125 hallway pairs, aid permission,
  first/repeat opening, cue timing, early hits, rescue, retreat and death regressions.
- HKS aid (two), rescue (one), diagnostics (three) tests; preparation checks,
  version metadata, whitespace and local documentation link targets.

These simulations do not execute Elden Ring's event VM or prove game playback.
The configured editor handoffs are recorded under `.sovereign/handoffs/`:
player `fd455b6b089443ac9db39af23f38b13a`, events
`af949584b259493684067c5f72d5f997`, parameters
`e33eab20146c470c876ddd212291f5de`, talk
`81b8d46eb1cf47fd8eef29fd5ac302ff`, and text
`954565cef802437cac40ab9be2b86eb0`.

Version 1.4.4 deployment completed. Prepared receipt
`.vdb/prepared/f5fcddc1d8334c06a6dfd1c620a10b0d/receipt.json` contains all 75
main-package files: the nine intended runtime changes and 66 preserved files,
including the external DLL. No paths were added or removed.

Protocol-3 finalization
`.vdb/finalizations/ba569ffdf32a479596ae02edadb0e618/receipt.json`, request
`23957ad6-292c-4139-9a63-0fa44be2d580`, build `fe8b0372f5462d9dd4e9274b`,
completed on profile `SkC-QjDMc`: enabled, deployed and verified with no
differences. An independent SHA-256 comparison of all 75 prepared files against
the game installation also found no differences; evidence is
`.codex-temp/hadeon-progress-144/live-verification.json`.
All 32 original WAV hashes still match. No gameplay pass, commit or publication
is implied; `releaseReady` remains false.

## Required gameplay acceptance

Test first/repeat entrance and half-health lines, every random variant, early hits
during the 0.7-second gap and speech, room-wide subtitle timing, corpse speech and
full tails. Confirm first-attempt restrictions, each of the five aid caps including
shield stamina cost, one count per combat death, rescue/fall/retreat exclusions,
simultaneous victory, reload persistence and NG+ reset. Verify no-loss item delivery,
recovery after interrupted payout and suppression of a duplicate world pickup.
Recheck actual AI engagement; a boss bar and music alone are insufficient evidence.
