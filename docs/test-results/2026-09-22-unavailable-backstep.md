# Unavailable backstep trial, version 1.0.2

The author selected ignoring an unavailable defensive action instead of restoring
the vanilla backstep. The reported symptom is an occasional stationary pause
around sprinting. No in-game reproduction or HKS runtime execution was performed
during this change; ER-056 remains Pending.

Previously both backstep branches in `GetEvasionRequest` returned BACKSTEP even
when `ModEndureBlasphemousClawBackstep` applied no effect. The custom animation is
stationary and its normal evasion update is disabled. This path can therefore
produce an empty stationary action before Endure or Claw is available. It does
not establish that the engine issued a backstep during the reported sprint pause.

The helper now returns TRUE after selecting an effect and FALSE otherwise. Both
guarded and unguarded callers require TRUE before returning BACKSTEP. The final
INVALID return handles unavailable actions without entering the replacement.

Static branch review gives these expected results:

| Available ability | FP | Effect(s) and result |
| --- | --- | --- |
| Neither | Any | No effect; ignore backstep |
| Claw only | Below 9 | No effect; ignore backstep |
| Claw only | At least 9 | 1626624; existing defensive action |
| Endure only | Below 9 | 1626602; existing fallback |
| Endure only | At least 9 | 1626601; existing Endure |
| Both | Below 9 | 1626602; existing fallback |
| Both | 9 through 14 | 1626601; existing Endure |
| Both | At least 15 | 1626601 and 1626624; existing combined action |

Saved editor/repo preflight found all 2 HKS and 676 animation/source files equal.
The reviewed runtime diff changes only the helper result, its two callers and a
final newline. No effects, costs, motion data or recovery timing were edited.
Version metadata check passed. Player qualification refreshed HKS hashes and
reused matching native source/binder qualification; this does not validate HKS
runtime compilation or gameplay. The guarded handoff changed one saved editor
file and retained its recovery copy.

Protocol-3 finalization completed for all configured game profiles. Main build
`ad1cdf395029129057b31a15` was deployed and verified on the enabled profile. Repo,
saved Script workspace and live game HKS hashes all match
`74da7c6b4d0dcfd46b23b2d60c68179b5c39721b9b2ba1d1e9d29d5ed8bae1ae`.

Local receipts:

- Qualification: `.codex-temp/player-qualifications/1790137087261159300/receipt.json`
- Editor handoff: `.sovereign/handoffs/81afbfe01d064b319b4ec309b567ef13/receipt.json`
- Propagation: `.sovereign/propagation/7faa49d67ea54dc2bd4019e29cf27edc/receipt.json`

For acceptance, use the fresh-character, guard, sprint-neutral-input and unlocked
ability/resource cases in ER-056. A remaining pause during sustained movement or
after unlocking Endure needs separate reproduction; this fix only skips unavailable
actions.
