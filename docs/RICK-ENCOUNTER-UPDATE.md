# Soldier of Godrick / Rick encounter, 1.0.6

## Local follow-up: ready stance, knockback and simultaneous vocal

After the 1.2.1 test, the author requested a ready stance during the half-second
recovery, a stronger backward push, and two vocal requests at the same instant
at buildup start. This follow-up is included in the authorized 1.2.2 deployment batch.

Effect 1627120 is a neutral, encounter-only combat-idle hold. Applied with the
Wrath shot, it routes c9997 into W_IdleBattle (native animation 20) on its next
eligible state update, bypassing the normal 1040 draw transition. IdleBattle holds
until the half-second recovery ends; death still has priority. Initialization,
abort and release clear the marker. Pose timing and weapon visibility need a game
test; static graph/TAE availability cannot guarantee a frame-exact transition.

Attack 75431100 now uses reaction 7 for both default/player reaction and 0.8
knockback distance (previously reaction 2 and 0.5). Holy damage remains 315 and
all other attack fields are preserved. This uses the normal charged Wrath's
backward-knockdown class at a reduced distance setting; terrain and defense still
influence the visible displacement.

Flag 18002851 now starts with the charge glow, before pose acknowledgement.
Event 18002861 issues two adjacent PlaySE calls for 472108006 with no intervening
wait, followed by the existing charge sound. The native vocal container's
single-instance/attenuation settings can prevent stacking; two requests do not
prove audible doubling or resolve the previously reported silence. No audio-bank
change was made. Buildup acknowledgement timeout and full warning remain intact.


## 1.2.1: short recovery and native audio cues

The author reports that 1.2.0's transition works better, but neither Hoarah's vocal
nor Wrath's sound was audible. Rick now has a half-second protected recovery after
the shot before AI resumes; player death/map exit still aborts safely.

Local event 18002861 plays casting sound 525305 (category 5) at the warning and
explosion sound 525316 at the phase-two gate. These match a429 casting TAE cues;
spawning the bullet alone did not request them. Character-motion vocal 472108006
now plays through native c4721 carrier 18000852 rather than the player. The host
warps this inert, non-colliding, disabled carrier to the soldier before the cue,
after both actors pass the backread check. Existing forced loading is retained.
This corrects the emitter route and position, but audibility must be retested in
game; backread/static bank evidence is not proof of successful audio playback.


## 1.2.0: held stagger and immediate handoff

The 1.1.9 user test confirmed visible Wrath playback, but the soldier still did not
hold the stagger pose. Damage remains unmeasured. This supersedes the historical
forced-8700 and three-second recovery instructions below.

The existing charge effect 1627118 together with phase-one marker 1627117 now
requests W_SABreak through shared enemy HKS. Its activation sets neutral marker
1627119; its update suppresses ordinary cancellation during the warning while
retaining death handling. The event waits for acknowledgement, bounded at one
second, then retains a full two-second warning even if acknowledgement fails.
It clears the charge and acknowledgement on swap, abort and retry. Natural
stance breaks and critical attacks remain suppressed only for the marked actor.

Rick no longer receives an incoming kneel or three-second recovery wait. At the
burst he regains collision, gravity, vulnerability and AI with a replan request.
The separate Hoarah Loux vocal continues over combat. Wrath tuning, retry state,
rewards, lighting and player movement code are unchanged. Static and native
checks do not prove the pose or AI behavior in game; retest ER-083/084.


1.1.9 correction: BehaviorParam 75431100 now points to Bullet 75431100; its
existing NPC attack retains 315 base holy damage. Rick is team owner and producer,
with one frame after enabling him before firing. The soldier's reset and forced
8700 playback are separated by one frame. Death/map abort guards cover both new
frame boundaries. No artificial poise damage or pose-hold HKS change was added.
Tutorial 18002663 now waits one second after proximity, preserving flags, note
grant and exclusions. Native route/preservation checks and event simulations pass;
runtime pose/explosion/damage need retesting. Backups: `.codex-temp/room-rick-1.1.9/`.

**2026-09-24 runtime correction:** The author's recording shows interrupted pose
playback and no visible burst. Investigation found a missing BehaviorParam link
in the ShootBullet route. The implementation below describes intended behavior,
not a passed game test. See [failure evidence and proposed repairs](test-results/2026-09-24-rick-transition-failure.md).

## Visible transformation, 2026-09-24 (implemented locally, game test pending)

The approved transition is implemented and synchronized to the saved editor
workspaces. It is not deployed. The earlier 1.1.2 persistent phase-two retry
behavior below is historical and superseded: every attempt starts with Soldier
of Godrick, regardless of the old awakening flag 1055420926. Final defeat flag
18000850 and rewards are unchanged. No new event flags were allocated.

At 25% HP, event 18002860 protects the soldier while retaining weapon contact,
waits for any existing critical interaction to finish, then transfers the loaded
but disabled Rick to the soldier's ground-level dummy 900. The soldier plays the
author-approved stance-break animation 8700 with casting glow 525310 attached to
verified chest dummy 220. The existing 4.97-second Hoarah vocal starts locally.
There is no fade or player control freeze.

After two seconds, Rick is enabled and forced into 8700 under one charged Wrath
burst. Rick owns that bullet so hiding phase one cannot remove its owner. The
soldier and his casting glow are hidden/cleared, Rick's bar/music begin, and a
three-second protected recovery completes the five-second presentation. Animation
reset and stance-break effect cleanup then return Rick to normal combat. Matching
pose timing, hidden-actor warp and the reset-to-combat blend require game review;
this does not claim a visually seamless handoff from code inspection alone.

SpEffect 1627117 is permanently assigned only to phase-one NPC 43113907 through
its previously empty spEffectID14. It sets received stance damage to zero and
throwCondition to Forbidden. Actor-marked HKS additionally denies throw defense
on each update and through SetThrowFlag, and prevents the normal stance-break
state from being entered by accumulated stance damage. Rick receives this marker
only during the swap/recovery and loses it before combat. Ordinary soldiers and
Rick's normal combat remain unaffected. Existing transition protection 1627116
continues to block HP/status/stagger damage while preserving hit detection.

SpEffect 1627118 and SpEffectVfxParam 1627118 own the casting glow's lifetime.
The shadowless native glow uses one torso attachment rather than repeated spawn
calls. Charge and burst FXR names were verified in the current packed common SFX
binder; no FXR, map or animation binder was edited.

Bullet/AtkParam_Npc 75431100 provide a single 0.3-second charged burst, nominal
radius 3-to-5, FXR 525316 and the original one-hit record behavior. Base holy
attack is 315 (75% of the inspected PC charged attack's 420), with PC seal
correction/final-rate lookup removed for the dedicated NPC attack. This is not
percentage-HP damage or a health cap: NPC effects, scaling and player defenses
still determine actual HP loss. Stamina attack is 40, stance attack 10, and
reaction is a medium stagger with 0.5 knockback distance. No child projectile,
status effect, invulnerability piercing or unblockable flag was added. Actual
roll, block, deflect, ward and multiplayer behavior require engine tests.

The sound carrier remains loaded while the encounter is undefeated, independent
of retired awakening state. Death during charge cancels the shot; death during
the burst/recovery clears temporary flags, glow and protection without enabling
Rick's AI. Rest/reload returns phase one. Host owns the one damaging bullet and
actor swap; the local worker only plays the vocal.

Backups of repository/editor inputs and native verification are retained under
`.codex-temp/rick-visible-20260924/`. Five parameter rows were added and one NPC
slot changed; all unrelated rows/tables were preserved. Compiled changes are
confined to events 18002860-18002863; all other events and metadata are unchanged.
Seven authored-control-flow tests pass, including interrupted warning, lethal
burst, obsolete-flag retry, completed boss, loading/critical waits and music.
Native player qualification was reused with fresh HKS guards; this is not a
Havok runtime or gameplay pass.

Handoffs: params 1a99383a59754f9486b5af3b337385b5, HKS
5936a833108a4f90bf11284ca02d7bf3, events 7ec2209557744cb69994dc1c94ed2be4.
Engine acceptance remains pending for critical/backstab denial, ordinary enemies,
pose and glow, walls/ground placement, damage/scaling, multiplayer, death/retry,
and once-only final victory/reward behavior.

## Retry and presentation follow-up, 1.1.2

The author reported that Rick still appeared at his original spawn and that
weapons passed through the outgoing soldier during the transformation. The author
also requested that reaching Rick permanently skip phase one on later attempts in
the same journey, and selected the previously auditioned Hoarah Loux vocal.

Event 18002860 now uses saved Sovereign flag 1055420926 for awakening. It is set
when phase two is ready to reveal, not merely on crossing the HP threshold. Rest,
death and reload preserve it; a new journey should reset it. Existing attempt
flags 18002851/18002852 still control the fade and music. Retry initialization
enables full-health Rick at his map placement, keeps phase one hidden, publishes
phase-two readiness before arena admission, then enables combat on entry. Final
defeat 18000850 and the key reward remain unchanged.

The first transformation waits for both Rick and the sound carrier to be loaded.
The warp now targets c4311 dummy 900, inspected at approximately (0, 0.0006, 0)
with no attached bone, and copies the soldier's floor. Rick's gravity/collision
stay disabled through the transfer; the source remains present for the half-second
settling interval. This is a native-pattern correction, not a verified engine fix.

SpEffect 1627116 clones native protection 1540, with indefinite duration until
explicit cleanup, no shared category, all stagger substitutions set to No Stagger,
zero poise/stance damage and status immunities. Existing zero physical/elemental
and status damage multipliers are retained. Visible actors no longer receive
event invincibility during the transition. The effect is removed on activation,
abort and initialization. Actual hit sounds/particles and damage-over-time cases
remain gameplay acceptance checks.

Vocal 472108006 is the selected 4.97-second Hoarah Loux preview. Hidden native
c4721_9000 / entity 18000852 is added 30 metres below Rick solely to load its
character sound bank. It has no talk or entity groups; local event 18002863 disables
its AI, rendering, collision and gravity, and makes it invincible. Backread is
forced until awakening or final victory, then released. Existing map entries and
NPC rows are preserved. The local player remains the vocal emitter. Fade/warp/hold
give about 6.2 seconds before reveal to accommodate the clip and native pitch.

Beginner rescue event 5750361 also adds effects 1626986, 1626991 and 1626993 before
its existing healing burst. Its heal, eligibility and cooldown are unchanged;
Hadeon's 75%, 50% and 25% milestone visuals already used this set.

Five source-control-flow tests in `tools/tests/test-rick.mjs` cover first admission,
critical/load waits, retry behavior, pre-reveal death cleanup, completed victory,
and retry music readiness. Native candidates preserve all previous map entries and
parameter rows. Event comparison allows only common 5750361 and Graveyard events
0/18002860/18002861/18002862 plus new 18002863. Gameplay remains Pending.
Backups and inspection receipts are in `.codex-temp/rick-retry-20260924/`.

The complete 73-file 1.1.2 package differs from 1.1.1 only in regulation, the two
event binaries and the Graveyard map. Editor handoffs completed for parameters,
map and event source/binary pairs. All-profile finalization request
`9dd44193-69f3-4226-9326-ea03dece2e0f`, build `5d9cdc99265c55a4e988351a`, completed
with the active profile enabled/deployed and no live-byte differences. The build
is selected for packaging; it is not published or marked gameplay-verified.
Receipt: `.vdb/finalizations/rick-retry-1.1.2/receipt.json`.

The author approved this encounter on 2026-09-22 after finding the previous Rick
fairly easy. Implementation and native checks are complete; gameplay acceptance
is Pending. The previous Rick remains the comparison baseline, not vanilla stats.

## Agreed behavior

- Phase 1 is Soldier of Godrick at normal size, with the previous non-golden
  Sovereign boosts retained. Golden Eyes is reserved for the transformation.
- At or below 25% HP, finish any active critical, pause the encounter and fade to black. A large hit cannot
  kill phase 1 and skip the transformation.
- Play soldier vocal 431008102 once during the fade, then reveal Rick at the
  outgoing soldier's location. Allow about five seconds before the reveal/music
  for the approximately four-second recording and its native pitch variation.
- Phase 2 is Rick, Soldier of God, at full health and 1.5 times model scale. Reuse
  Golden Eyes 5250 and Boss Modifier 7380. Play The Final Battle, cue 219000.
- Final defeat uses Legend Felled and sets 18000850, releasing both arena barriers
  and preserving the original reward and defeated-load identity.

Relative to phase 1, the two phase-2 effects contribute 4x maximum HP and 1.5x
attack rate. Relative to the previous Rick, phase 2 has 2x maximum HP and the same
attack rates, with more stance/status resistance. These are parameter comparisons,
not measured final HP damage. The unchanged tutorial effect 8041 still applies.

## Ownership and implementation

The map has no runtime scale instruction in the inspected event API. Two actors
share the original model, AI, equipment, location and route. The host swaps them
at the outgoing actor's position under the fade; no moveset edit is required.

| Resource | Purpose |
| --- | --- |
| Entity 18000851, map part c4311_9004 | New normal-size first phase |
| NpcParam 43113907 | Clone of pre-change 43113906; slot 30 changes 5250 to 5255 to suppress random Golden Eyes |
| NpcName 904311001 | New `Soldier of Godrick` name in the English item binder |
| Entity 18000850, map part c4311_9003 | Existing final boss; map scale changes from 1 to 1.5 |
| NpcParam 43113906 | Original Rick; slot 29 adds 7380; slot 14 adds the existing tutorial marker 8041 at spawn |
| NpcName 904311000 | Existing `Rick, Soldier of God`, unchanged |
| Event 18002860 | Host initialization, threshold, actor swap and transition abort cleanup |
| Temporary flag 18002851 | Transition in progress; explicitly reset on initialization |
| Temporary flag 18002852 | Phase 2 entered; explicitly reset on initialization; replaces its unused stock music-phase role |
| Event 18002861 | Local fade/freeze and recovery on completion, death, departure or abort |
| Event 18002862 | Local ownership and cleanup of cues 931000 and 219000 |
| Event 18002850 / flag 18000850 | Existing final actor death, banner and restored persistent defeat flag |

New actor, NPC, name and event IDs were absent from their respective inspected
tables/map/source. Flags 18002851/18002852 use the map's temporary 18002xxx range;
their owner is event 18002860 and their lifetime is one attempt. No new saved
progression flag is introduced. The existing fog helpers still consume 18000850.

The guard-counter tutorial follows the first-phase actor. Both actors retain
tutorial effect 8041. First-phase immortality prevents lethal threshold skips;
invincibility and an animation reset stop outgoing combat during the transition.
The final actor starts with native scaling effects, then receives existing full
recovery effect 110 before its new health bar is revealed. Phase 1 is hidden alive,
so it does not grant an early defeat or duplicate reward. Both actors are removed
when the saved defeat flag is already set.

Enemy HKS `ModNemesis` returns early only for the combination 8041 + 7380. This
preserves Rick's Golden Eyes during an eclipse, which otherwise removes effect
5250. The base-difficulty application in `SoulDropUp` remains unchanged. No shared
SpEffect rows are edited. The original Rick row now includes 8041 at spawn so the
exception does not depend on event/HKS update ordering.

## Verification and recovery

### Transition follow-up, 1.0.6

The author reported no fade despite a successful phase-two transformation, with
Rick appearing at his original spawn. The previous fade required continued
occupancy of the small entrance region 18002850. It now checks map presence,
living state and host/entered-white-phantom participation instead. The host's
threshold is latched at 25%, so a critical does not require an additional hit.

The enemy HKS mirrors IsThrowing/HasThrowRequest to existing neutral effect 18480
only on the tutorial soldier (8041 present, Boss Modifier 7380 absent). Native
inspection found no gameplay modifiers, linked effects or VFX in that row. No
shared parameter is edited. The event waits three frames for the marker to settle,
then waits for it to clear before resetting the outgoing actor or freezing players.
This uses the same neutral marker as Malenia while supplying it through Rick's
own HKS state; Rick's critical timelines did not already apply it.

Rick is enabled under black with AI/collision disabled and invincibility retained.
After two update frames he is warped to the still-enabled outgoing actor; two
more frames precede hiding that actor. The full heal precedes the reveal. The
local vocal uses the player as its emitter so disabling phase one cannot truncate
it. The existing native event selects among four vocal variants; raw durations
are 3.97-4.05 seconds, with native pitch processing retained. Fade-in and phase-two
music follow a roughly 5.3-second transition, with combat resuming after fade-in.

Death/departure/abort picture recovery, final defeat flag 18000850, rewards,
phase-two stats and music choice remain in place. In-game acceptance is Pending;
see ER-057 through ER-060 and the 2026-09-23 test record.

### Reward follow-up, 1.0.4

The author approved increasing both `GameAreaParam` row 18000850 reward fields,
`bonusSoul_single` and `bonusSoul_multi`, from 400 to 2000. Golden Eyes 5250 retains
its existing `haveSoulRate = 3`, giving an expected 6000-rune payout before other
bonuses or journey scaling; the actual in-game payout still needs verification.
The event still awards victory only for the final actor. No NPC rune drop, shared
effect, event or phase-1 reward is added by this follow-up.

Native decode/rebuild/reopen verified exactly those two changed fields, every
other GameAreaParam row, binder metadata and every other table's original bytes.
Candidate and before-copy: `.codex-temp/rick-reward-increase-20260922/`.
Version 1.0.4 was synced to Smithbox and deployed through the normal all-profile
VDB finalization. Repo, editor and live regulation hashes match. Propagation
receipt: `.sovereign/propagation/4d68d527e3064741b024c8953f41eadd/receipt.json`.
ER-059 remains Pending until the payout is observed in game.

### Encounter verification, 1.0.3

- Saved editor preflight: events, params, maps, text and HKS matched repo inputs.
- Native parameter roundtrip preserved every other NPC row and every other table's
  bytes. Only the original Rick's two fields and the new first-phase clone changed.
- Unchanged map roundtrip matched decoded data. Complete candidate comparison
  matches only the added first-phase actor and the original actor's scale.
- Binary FMG patch added one previously absent name. Full expected decoded binder
  comparison passed, preserving existing entries, member metadata and null values.
- DarkScript build `1790138171499040500` compiled successfully. Independent decode
  found changes only in events 0, 18002850, 18002860 and 18000870, plus new events
  18002861/18002862. Existing event order and file metadata are preserved; every
  other shipped event file is equivalent. `common_func` remains authoring-only.
- Player qualification `1790138250475063300` refreshes HKS hashes and reuses exact
  unchanged animation/behavior qualification. It does not prove HKS execution.
- The package differs from selected 1.0.2 in exactly regulation, the graveyard map,
  its event binary, the English item binder and c9997.hks.

Native reader/writer, before-copies, full map comparisons and candidate acceptance
records are retained in `.codex-temp/rick-phase2-20260922/`. Text candidate:
`.codex-temp/binder-candidates/1790138102055568800/receipt.json`.
Guarded editor handoffs retain independent backups under `.sovereign/handoffs/`.

Editor handoffs completed for events (`2d28e9b7719d444b99b6c29314e26a22`), params
(`7ba23b6ef562454688c98a933da83231`), maps (`06c13fed98e5422a95fffb11ab5f0ecd`),
item text (`fb06bea13bb848088cbacfad7d1061cb`) and coordinated player assets
(`199196ba6e9145328dfab692105f8908`). Only six saved editor files differed; all
unchanged coordinated player companions were guarded.

Protocol-3 all-profile finalization completed and verified deployment of main
1.0.3, build `26960b87290f7c57800f923c`, on the enabled profile. It is selected for
packaging. Stage receipt: `.vdb/prepared/8957adf559424fca9f35cbb9f2224655/receipt.json`.
Finalization receipt: `.vdb/finalizations/rick-1.0.3/receipt.json`, request
`4ee59482-8a90-4684-9afa-9c471f1b9270`. No Nexus publication or gameplay pass is implied.

ER-057 through ER-060 cover acceptance. Test actual growth, weapon reach, collision,
lock-on, cue audibility, recovery timing, eclipse behavior and host/guest state in
game. Compilation and serialization checks do not establish those outcomes.
