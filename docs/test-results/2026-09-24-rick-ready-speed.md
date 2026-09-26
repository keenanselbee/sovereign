# Rick ready stance and speed isolation: local follow-up

Author requested two simultaneous Hoarah vocal requests at buildup start, a
combat-ready pose during recovery, stronger backward Wrath knockback, restoration
of custom jumping and isolation of custom movement-speed overrides.

Implemented the duplicate adjacent PlaySE calls and moved the audio gate before
pose acknowledgement. Added neutral marker 1627120 to enter native W_IdleBattle
on the next eligible state update and hold through the existing half-second
recovery. It clears on initialization, normal release and abort. Reaction fields
on attack 75431100 change 2 to 7 and knockback distance 0.5 to 0.8; damage and all
other fields remain unchanged. Custom jump handling is restored; the action-speed
helper and three custom ground-speed writes are bypassed. Roll/jump buff selection
and native locomotion remain intact.

Sixteen mocked control-flow checks pass, including simultaneous audio ordering,
buildup start ordering and ready-marker release/death cleanup. Native regulation
roundtrip verifies the marker plus exactly three attack-field changes, preserving
other rows/tables. Event compilation changes only 18002860 and 18002861. HKS
comparison confines changes to Move_onUpdate/Update in c0000 and
ExecPassiveTransition/IdleBattle_onUpdate in c9997. Native combat idle 20 and the
W_IdleBattle/IdleBattle_CMSG graph entries exist. This does not establish exact
frame timing, sword visibility, push distance, audible stacking or movement
resolution in game. The vocal container may reject/limit concurrent instances.

Backups and validation: `.codex-temp/rick-ready-speed-20260924/`.
Event candidate: `.codex-temp/event-builds/1790286574971720500/`.
Player qualification: `.codex-temp/player-qualifications/1790286601158335700/receipt.json`.
Handoffs: animations 82e3268162fd4f6e9730af624d9df3d5, params
23b7887ccb514795a00bbf05e6462334, events 0bea7983b936482bbdcba8b637c5a442.
No package/version preparation, Vortex deployment or live-file writes requested
or performed in this follow-up. The deployed build remains 1.2.1.
