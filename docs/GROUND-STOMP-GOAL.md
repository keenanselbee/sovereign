Ground-stomp counters and Hadeon's jumping lesson
================================================

Author-approved goal, 2026-09-24; trial updated 2026-09-25. The author confirmed
the existing Crucible Knight stomp is jumpable. The first local trial changes only
`disableGuard` and `isDisableNoDamage` from 0 to 1 on NPC attack 2500182.
Damage, collision, timing and airborne avoidance remain unchanged. This affects
the shared Crucible Knight route, not only Hadeon. Game acceptance remains pending.
Version 1.3.2 is deployed and adds the approved Jump to Evade lesson described below;
no wider attack edits are included.

The author requested a thorough evidence-gathering investigation on 2026-09-25
while testing Hadeon's flag combination. That research phase is documented in
[Jump to Evade: attack investigation](JUMP-TO-EVADE-INVESTIGATION.md), with
an expanded [priority candidate review](JUMP-TO-EVADE-EXPANSION.md): 1,570
screened rows, 245 curated rows in 72 groups, 116 animation binders and native
model-origin evidence. The test shortlist now contains 47 rows: 14 small
floor-probe rows, 27 foot/forelimb pulses and six larger or delayed ground
pulses. Confidence in a ground route is distinct from verified jump clearance.
The [machine-readable evidence](jump-to-evade-candidates.json) and
[screening table](jump-to-evade-screening.csv) distinguish candidates from
exclusions and unapproved results. No expansion patch was made. Live clearance
after bypass remains the adoption gate, not an assumption based on an air flag.


Intended combat rule
--------------------

Sovereign should reward choosing the appropriate defensive response. Deflection
is one important tool; timed jumping should be the answer to readable ground-stomp
shockwaves when the player is inside their footprint. Such waves should generally
ignore dodge invulnerability and deflection but remain reliably jumpable.

Moving outside the attack's reach remains possible. Direct foot/body impacts,
grabs, airborne explosions, lingering hazards and follow-up weapon swings need
their own decisions: a name containing "stomp" does not establish that all those
contacts should be avoided by jumping. Preserve clear windup, a fair jump window
and an opportunity to punish with a jumping attack where appropriate.


Pre-trial native evidence
------------------------

Inspected accepted `mod/regulation.bin`, SHA-256
`41b42f86d3a692df7a30b56cef27a0500c374ee88a2cca34f3bf0c038707958d`.
The compact [attack inventory](ground-stomp-evidence.json) records the relevant
fields and initial named candidates. Full scratch exports and their reader remain
under `.codex-temp/stomp-review/`. This is static evidence, not a game test.

Hadeon NpcParam 25000011 uses behavior variation 25000. Behavior 225000180
references Bullet 2500180, which creates 2500181 at intervals; its hit bullet is
2500182. Each points to the correspondingly numbered NPC attack row. The first
two rows have zero physical attack; damaging attack 2500182 has 220 base physical
attack. This shared Crucible Knight route is not exclusive to Hadeon.

| Attack | Guard disabled | Dodge invulnerability bypass | Airborne avoidance |
| --- | --- | --- | --- |
| 2500180, stomp carrier | No | No | No |
| 2500181, child carrier | No | No | No |
| 2500182, damaging wave | No | No | Yes |
| 4720281, Godfrey phase-shift stomp | No | Yes | Yes, but overridden by bypass according to the definition |

All four disable conventional contact parrying. That is a separate mechanism
from Sovereign's deflection and does not establish that the attacks cannot be
deflected. No direct override of these attack IDs or these guard/invulnerability
fields was found in the accepted player/NPC HKS or event sources in this pass.
NPC effects and live attack behavior still require verification.

The installed Smithbox `Assets/PARAM/ER/Defs/AtkParam.xml` describes:

- `disableGuard`: ignores the defender's guard when enabled.
- `isDisableNoDamage`: ignores invulnerability such as stepping, but not complete
  TAE invulnerability.
- `isInvalidatedByNoDamageInAir`: airborne-only avoidance; explicitly ignored
  when `isDisableNoDamage` is enabled.

Consequently, setting both invulnerability fields does not prove that a stomp
ignores rolls but respects jumps. Hadeon's current row does not already enforce
the intended rule. Do not publish the categorical tutorial until the changed
attack's jump counter is qualified.


Implementation and review sequence
----------------------------------

1. Test the two-field trial against Hadeon's full live stomp route and effects.
   Compare standing guard, timed deflection, rolling, ordinary jump and jumping
   attack. The author confirmed jumpability before the bypass edit, not after it.
2. Use existing lower-body jump protection first; do not resize collision by
   default. If bypass defeats jumping too, stop expansion and investigate an
   attack-local solution. Do not enable
   complete airborne immunity to every attack or alter global movement to solve
   one attack family. If a reliable attack-local solution is unavailable, record
   that limitation before choosing a wider implementation.
3. Review shared users before changing the Crucible Knight row. A shared edit
   changes other knights too; a Hadeon-only trial needs an isolated connected
   behavior/bullet/attack route, not just an unused cloned attack row.
4. Add the lesson below with independently owned persistent state, after the
   premise is supported. Preserve vanilla tutorial suppression and progression.
5. Audit other ground-wave families in small batches. Start with Godfrey/Hoarah
   Loux, then clearly ground-bound waves from avatars, gargoyles and other bosses.
   Treat dragon/giant foot contacts and elemental/rising attacks separately.

The initial name scan found 68 NPC attack candidates containing "stomp",
"shockwave" or "ground slam". There are also 501 NPC attack rows with airborne
avoidance enabled. Neither set is a complete or approved edit list. Use names,
airborne flags, animation references and recursive child-bullet links together to
find unlabeled damage rows such as 2500182. Record inclusion/exclusion, all shared
users, current fields, intended edits and playtest results per attack family.

The [expanded candidate review](GROUND-STOMP-CANDIDATES.md) now covers base-game
and DLC families, including unlabeled damaging child rows. It prioritizes physical
jump clearance and distinguishes small local volumes from large spherical AoEs
that may need collision redesign. It is a review list, not a bulk-edit manifest.


Tutorial sequence
-----------------

The author's 2026-09-25 decision replaces the three-death lesson with an entry
lesson. No death counter is needed. The implemented order is:

- Deflection before the added Godrick Knight c4351_9000 / entity 18000258.
  The selected existing box is entity 18002658 (Region ID 89), at
  (-129.509, -4.720, 94.336), dimensions 4 x 20 x 5. Crossing it arms a two-second
  delay that survives walking out. Death/map departure cancels and rearms it.
  This trigger is implemented locally in event 18002663; map bytes are unchanged.
- Ultimate Attacks one second after admission to Soldier of Godrick's arena,
  replacing his old deflection trigger. Event 5750363 now runs in the map, using
  arena 18002850 and admission 18002855. It cancels on death, departure or phase
  transition and retains saved shown flag 1055420927.
- Jump to Evade after three uninterrupted living seconds in Hadeon's room,
  region entity 18000359, excluding fatal-fall region 18002367. Map event 5750364,
  TutorialParam 5751 and saved shown flag 1055420928 are independent of Ultimate.
  Death, departure or falling cancels the pending display; victory suppresses it.

Use map-scoped event waits rather than a new per-frame player callback. Reuse a
suitable existing jumping-attack illustration (Stance Breaking image 17, visually
checked). TutorialTitle/TutorialBody entries 5750364 in all three English menu
binders follow the existing Ultimate lesson route. Preserve existing
once-only receipts and avoid overlapping popup requests.

Author-approved text:

**Jump to Evade**

Certain enemies unleash ground attacks that cannot be dodged or blocked, such as
low shockwaves from stomps or ground slams. Jump over these attacks to avoid damage.

This wording does not mean all stomps/slams have been converted. The current
implementation changes only 2500182. Jumpability after enabling bypass remains
an explicit game-test requirement; do not report the trial as validated in play.


Acceptance
-----------

- Standing guard, timed deflection and rolls overlapping the damaging wave fail
  to avoid it; a correctly timed jump and jumping attack avoid the wave.
- Late jumps and separate foot/body/weapon contacts behave as intentionally
  specified. Test close/far range, slopes and bridge edges, both grips and shields.
- Deflection appears two seconds after crossing 18002658, including when already
  outside it; interruption before display permits retry and display is once-only.
- Test Ultimate at Soldier admission and Jump to Evade after three seconds:
  cancellation/retry, once-only display, guest exclusion, prior shown state and NG+.
- Verify every changed shared attack user. Keep damage, poise damage, timings,
  ordinary jump behavior and unrelated attack rows unchanged unless deliberately
  included in the reviewed change.

Trial backup and native evidence: `.codex-temp/stomp-trial-20260925/`.
The independent native comparison found exactly the two intended cells changed,
with all other rows and binder members preserved. Event candidate
`.codex-temp/event-builds/1790372759480329000/` changes only the initializer's
region argument and event 18002663, with unchanged file metadata. Gameplay checks
remain pending. Sync accepted editor assets; deploy only when requested.

Editor handoff receipts under `.sovereign/handoffs/`:
`5aab47cd89b14863a9fa8b7bd9a1bf19` (parameters) and
`59abd281cc44456d9945b3fd355289ee` (event/source). Smithbox was saved during the
work; its differing encrypted file had identical decoded binder member bytes
to the pre-trial baseline. That reviewed difference was resolved before sync,
but a later editor save restored that old regulation again. Final verification
found the event/source pair synchronized, while the editor parameter copy lacks
the trial. Repository regulation remains the reviewed candidate. Reload the
Smithbox project before repeating the parameter handoff; do not keep overwriting
an active stale editor buffer.
The deflection, Rick and opening-support source suites passed all 21 tests.
No release version was changed and no build was deployed.


Completed 1.3.2 follow-up
-------------------------

The subsequent authorized batch implements both boss lessons, the approved
general Jump to Evade text, and the sword key knight. Native candidates/backups
are under `.codex-temp/tutorial-order-1.3.2/`; final event qualification is
`.codex-temp/event-builds/1790373733979271200/`. The 23 relevant source tests
passed. Three full binary FMG comparisons preserve all text except the new
lesson's title/body; no texture changes were required. The 598-file native flag
scan found no collision for saved receipt 1055420928.

Final editor handoffs: `8af193a5273d465d908113f3a6389a33` (parameters),
`59986185dc07448fbe4ef4919a2c13d9` (map),
`e3c142f2abd542489db784ede6759b7e` (text), and
`6886569d23c6432b95971817fdb47f27` (events). All accepted editor copies matched
before deployment. Reload open editor projects before saving stale buffers.

Version 1.3.2 contains 73 main-package files, with exactly seven runtime files
changed from 1.3.1. Prepared receipt:
`.vdb/prepared/427dafe358914770bdd31dc0d6dd2609/receipt.json`.
Finalization `.vdb/finalizations/tutorial-knight-1.3.2/receipt.json` completed for
the Default profile with enabled deployment and no live-byte differences.
Build `39fa0eda29d7809eaaa4dcab` is selected; textures retain their prior build.
This verifies deployment, not gameplay. In-game stomp jump clearance, lesson
presentation and sword-knight behavior remain pending.
