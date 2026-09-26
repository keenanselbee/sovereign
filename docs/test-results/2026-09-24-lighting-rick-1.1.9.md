# Lighting and Rick correction deployment: 1.1.9

Implemented and synced the ten-second room ignition, 42 smaller groups, removal
of gaze surges, controlled brazier flames, earlier tutorial, missing Wrath
behavior link and separate reset/playback frame. The shared player cancellation
diagnostic is included; Divinity cancellation remains active.

Ten source control-flow checks pass, including death at the new Rick boundaries,
lighting death/re-entry, victory/crystal interruptions, saved-state loads and HP
preset exclusivity. Native checks preserve all unrelated map fields/parameter
rows and confirm the Wrath behavior/bullet/NPC-attack route. Other event files,
hallway events and crystal cue behavior are unchanged. Repository preparation
checks pass. No game execution was performed; pose, damage, visual placement,
performance and movement-pause resolution remain pending.

Vortex finalization completed for Default profile SkC-QjDMc. Exact build
81b73f7ed5ce447e55f135bd was selected only after its completed deployment reported
no differences. The four changed live runtime files were independently hashed
against the prepared package. No SFX file changed relative to the prior live build.

Backups and native/event/package checks: `.codex-temp/room-rick-1.1.9/`.
Finalization: `.vdb/finalizations/room-rick-1.1.9/receipt.json`.
Prepared package: `.vdb/prepared/3838fc49b3d7491883b5bb142f8d5aed/receipt.json`.

## Follow-up user test: Rick

The user reports that Wrath of Gold now plays, but the stagger pose still fails
and Rick waits after the explosion. Save type and measured damage were not supplied.
This confirms visible burst playback only; pose and combat handoff fail acceptance.

Inspection found an explicit three-second wait after the shot while phase-two AI
is disabled in event 18002860. The separate vocal event can continue during combat.
The incoming actor also receives a fresh 8700 playback request immediately before
the shot. Proposed correction: remove that playback and recovery wait, then clear
transition effects, enable AI and request a replan at the handoff.

The shared c9997 behavior graph contains W_SABreak, a SABreak state and a front
selector for animation 8700. HKS normally enters it through HasBrokenSA, but the
encounter intentionally blocks that natural path with effect 1627117. The event
currently requests the clip directly without a transition-specific state hold.
This establishes a concrete alternative, not proof of the exact runtime interrupt.
Proposed correction: use an encounter-only marker to enter W_SABreak once and
hold its update path during the two-second charge, retaining critical denial and
weapon contact. Clear the marker on swap, abort and retry. Do not inflict artificial
poise damage or repeatedly restart the clip. Confirm pose entry before starting
the visible warning timer, with a bounded failure path if entry does not occur.

No gameplay files changed or deployed during this investigation. Temporary native
behavior extraction is retained in `.codex-temp/rick-stance-state-20260924/`.
