Hadeon threshold boons and deflect thorns
=======================================

2026-09-19. The author approved this minimal combat change after the initial
[encounter investigation](HADEON-ENCOUNTER-REVIEW.md). Implemented in repository
sources and built runtime assets; gameplay acceptance remains Pending. The later
authorized [1.0.0 deployment](DEPLOYMENT-1.0.0.md) synchronized the affected editor
copies and verified both installed packages.


Encounter behavior
------------------

| Trigger | Result |
| --- | --- |
| First reaches 75% HP | Existing full heal, including its existing follow-on recovery effect, even if the player is already full |
| First reaches 50% HP | Existing three-stage Thorn Ward and its normal damage retaliation |
| First reaches 25% HP | Existing shriek sounds/AoE plus a direct pulse removing 10% of Hadeon's maximum HP |
| Genuine below-arena fall followed by a return | One pulse removing 5% of Hadeon's maximum HP after arrival |

Threshold comparisons use `<=`, so an attack or fall that skips a threshold still
qualifies. Each boon occurs once per attempt. Death and map/rest initialization
clear the milestone flags. Ordinary fall returns and retreat/re-entry preserve
milestones while the existing encounter retains damage; retreat cannot farm boons.
No random encounter boon rolls or initial 30-second boon delay remain. Existing
flavor sounds may still vary. Shared follower/Oath boon events are unchanged.

The shriek's direct damage is independent of projectile contact, bleed immunity
and bewitching eligibility. Its existing AoE behavior remains. A fall from 28% to
23% can trigger shriek and leave about 13%. A pulse may finish Hadeon through the
existing boss-death and reward events; no separate reward path was added.

Only below-arena region 18002367 counts as a damaging fall. Recovery from region
18002349 and disengagement resets retain their existing behavior without a pulse.
Existing return destinations remain. The fall worker waits for departure from the
fall region before applying damage, then keeps its existing one-second delay.
Damage requires a living player in the arena and a living, undefeated Hadeon.
Boons and delayed shriek damage additionally require the active combat flag; a
shriek interrupted before its grant remains eligible on a valid return.


Empowered thorns
----------------

During the host's active Hadeon encounter, successful deflects fire the smallest
existing thorn burst while any of the three Thorn Ward stages is active. The
burst does not consume a ward charge. Taking damage retains the existing ward
charge loss and retaliation behavior, including that original route's parameters.

The new deflect route has a 0.5-second cooldown and no shooter HP cost or bleed
effect. It reuses attack 49000: 200 base magic damage before engine scaling and
defenses, with the existing short-range visual and radius growing to 2.5. This is
not a guaranteed 200 damage per deflect. Projectile collision determines which
nearby enemies are hit; the code does not identify a distant original attacker.

A host-only map worker refreshes a neutral presence effect every 0.05 seconds
while both combatants are alive, the player is in the arena, neither is in the
fall region, and combat is active. Presence lasts 0.15 seconds as an unload
failsafe and is explicitly removed on invalid state. Death clears the cooldown.
The successful-deflect callback checks presence, player life, a ward stage and
the cooldown before adding the dedicated burst. Ordinary blocks do not call this
new branch. Ordinary Thorn Ward elsewhere is unchanged. Guest empowerment was
not added; co-op ownership and effect replication require a game test.


Implementation and preservation
-------------------------------

| Allocation | Purpose |
| --- | --- |
| Flags 1055422930-1055422932 | Heal, ward and shriek consumed this attempt |
| Flag 1055422933 | Active Hadeon combat, owned by existing boss lifecycle event |
| SpEffects 1627100 / 1627101 | Instantaneous 5% / 10% maximum-HP subtraction |
| SpEffect 1627102 | Short-lived encounter presence |
| SpEffect 1627103 | 0.5-second deflect burst cooldown |
| SpEffect 1627104 | Dedicated deflect burst trigger |
| BehaviorParam_PC 2560 | Routes the new trigger to its bullet |
| Bullet 10490010 | Copy of 10490000 without shooter effect 1490000 or bleed effect 1490010 |

The two damage pulses and neutral markers copy neutral effect 153. Pulse
`effectEndurance` is zero, `changeHpRate` is positive 5 or 10, and `changeHpPoint`
is zero; they do not change maximum HP or chain another effect. The burst copies
1626924 through behavior 2550 to the smallest existing attack. All seven new row
IDs were absent before the edit; no original row was modified.

The shrine changes are confined to events 5750300, 5750302, 5750303, 5750304,
5750305 and 5750306. The existing boss lifecycle now also recognizes player death
when leaving combat. The Thorn Ward retaliation worker, reward/crystal events,
common events, map geometry, NPC stats and player animation/behavior binders remain
unchanged. The player HKS adds one guarded branch in `SetJustGuardSucceedEffect`.
Mandatory entry, keyless access and travel restrictions remain separate work in
[the opening plan](HADEON-SEAL-PLAN.md).


Verification and recovery
-------------------------

Pre-edit repo regulation, HKS and shrine event source/runtime matched their saved
editor counterparts. Independent backups, the parameter writer, native
preservation receipt and acceptance manifest are retained under
`.codex-temp/hadeon-thresholds-20260919/`. The regulation was reopened and every
existing row in all three touched tables compared, including names and cell
values; other table payloads and binder member metadata were preserved.

Native event builds compare decoded event bodies, order and file metadata. Player
qualification reuses unchanged graph/binder proof with fresh HKS input hashes;
it does not compile HKS or establish in-game compatibility. See the acceptance
manifest for exact build/qualification receipt paths and final hashes.

`node --test tools/tests/test-hadeon.mjs` passed seven source-level control-flow
checks by running the actual authored event bodies with mocked engine state and
suspended waits. These cover skipped/one-time milestones, a full-health heal,
interrupted shriek recovery, fall re-arming, non-fall recovery, presence/attempt
cleanup and host ownership. They do not simulate native effect timing, HKS
execution, collision, damage scaling or EMEVD scheduling in the game.

Manual acceptance is recorded as Pending in ER-042 through ER-046 of
[TEST-MATRIX](../TEST-MATRIX.md), alongside the existing Hadeon and reward tests.
Verify native percentage-damage application, deflect burst damage/range/cooldown,
guard chip interactions, interruption cleanup and victory in game. No test was
marked Passed from source inspection or native rebuilding.
