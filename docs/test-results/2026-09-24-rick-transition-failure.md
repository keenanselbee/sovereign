# Rick transition recording investigation

The author supplied `Z:\Shadowplay\Elden Ring\Elden Ring 2026.09.24 - 13.02.04.01.mp4`
after reporting that they handled 1.1.8 deployment. The recording itself does not
identify the loaded build hashes or save. The 29.92-second clip was inspected as
one-second frames, with additional quarter-second samples around the transition.
The golden charge is visible around 10-12 seconds; Rick replaces the soldier
without a visible Wrath explosion. The author reports an interrupted stance-break
pose and a deflect tutorial one second too late. The tutorial is not visible in
this recording.

## Confirmed firing defect

Event 18002860 passes 75431100 as ShootBullet's fourth argument. The installed ER
EMEDF defines that argument as Behavior ID, not Bullet ID. Fresh native reads of
current regulation confirm Bullet 75431100 and its attack route exist, but neither
BehaviorParam nor BehaviorParam_PC has row 75431100. Existing event shots such as
803301800 have BehaviorParam rows with refType 1 pointing to their Bullet rows.
This missing link is a concrete defect, independent of the pose issue.

The smallest correction is a dedicated BehaviorParam row pointing to Bullet
75431100, preserving the dedicated NPC attack and 75%-base-attack intent. Use the
active Rick as both team owner and producer after activation has settled, rather
than firing from the soldier that is disabled in the same event tick. This second
change avoids another lifetime ambiguity; it is not a separately proven cause.

The author's established SpEffect route is also present: Totality 1626558/1626559
use stateInfo 275 and behaviorId 2511/2512, whose BehaviorParam_PC rows point to
10641100/10641101. A dedicated one-shot effect could use that pattern, but the
existing Totality rows must not be reused directly for Rick: their PC behavior,
attack, stamina and ownership differ. An animation bullet also requires a valid
behavior route and would add TAE/binder changes. Prefer repairing the event route
first rather than combining firing implementations or emitting duplicate blasts.

## Pose investigation

The event requests an animation reset immediately before forcing 8700, without a
frame boundary. It disables AI, but has no explicit temporary pose-hold state in
the enemy script. SABreak_onUpdate still calls DamageCommonFunction and its normal
transition handlers. Protection 1627117 denies natural stance-break entry and
critical throws; it is not itself a scripted pose hold.

The shared soldier c4310 8700 timeline inspected from the installed base archive
has its initial main window through 3.967 seconds and normal AI cancel flags from
3.467 seconds; it is not merely a sub-two-second clip. c4311's local animation
binder has only its skeleton. The exact active graph/node at the interruption
was not captured, so an animation-state interruption remains the leading
hypothesis, not a proven root cause. Start by separating reset from playback by
an update boundary. If the pose still exits early, use a transition-specific
actor marker to hold the approved stance state for the warning and release it on
swap/recovery/abort. Preserve critical denial, weapon contact and ordinary enemies.
Do not blindly loop the full stumble animation or disable the shared enemy script.

## Tutorial

Event 18002663 still waits ElapsedSeconds(2) after the ten-unit proximity trigger.
Changing this to one second is the direct requested timing adjustment. Preserve
the transformation exclusion, death/map checks, once-only flag and note grant.
The clip cannot establish exact visual onset or tutorial settings behavior.

## Scope and verification

Only the separately documented player cancellation diagnostic was implemented
and synced. Rick, tutorial, params and animation binders were investigated, not
edited or deployed. Current recording failures supersede the earlier pending
pose/burst acceptance; the seven mocked event-flow tests never verified native
behavior references or Havok animation playback.

Scratch frames, backups and native inspection helper/results remain under
`.codex-temp/rick-pause-review-20260924/`. Follow-up engine tests need the two-second
kneeling warning, exactly one visible damaging burst, correct damage ownership,
no player freeze, safe abort/retry and restored ordinary enemy behavior.
