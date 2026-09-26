Beginner opening update, 1.0.9

## Opening presentation revision, 1.2.2

Event 5750362 retains the three-second eclipse effect 1627113 and existing audio,
but no longer applies player Nemesis effects 1627111 or 1627115. Their cleanup
remains scoped to the omen. Other eclipses and rescue effects are unchanged.
At the same start, neutral one-second marker 1627121 requests the player HKS to
consume it once and enter W_Land with LAND_HEAVY (native heavy-fall animation
4220). No displacement, fall-height change, damage application or global landing
rule change is introduced. Native landing recovery is retained.

Existing Chapel first-arrival/cutscene guards and persistent journey flag
1055420925 prevent ordinary respawn/later-visit repeats. Version 1.2.3 removes the extra half-second wait after readiness; the trigger still
rechecks cutscene effects. Initialization and interruption cleanup remove the
request marker; its short duration bounds an unconsumed request. Static tests do
not establish the opening's visible impact timing; fresh-save verification is
required.

=============================

Author-approved 2026-09-24. This update targets new characters and existing vanilla
saves installing Sovereign for the first time. Migration from earlier Sovereign
versions is deliberately out of scope. Gameplay acceptance remains pending.

Behavior
--------

- Common event 5750361 fully heals the host at <=30% HP in the Chapel of
  Anticipation or Stranded Graveyard while Hadeon remains undefeated. The
  45-second event timer starts with the grant. Rest, reload and death give a fresh
  allowance; leaving the eligible maps prevents further grants. The timer does
  not need persistent state or a buff that Divinity could prolong.
- Effect 1627112 copies the existing instant heal 1626935 and removes its
  follow-on effect 501300. The shared follower heal is unchanged. Existing healing
  modifiers still apply; this is not an invulnerability or resurrection effect.
- The rescue excludes HP <=1, the native Chapel transition flag 9021, the opening
  cutscene before 10010020 completes, existing suppression effects 100690/9621,
  Rick's scripted fade, and Hadeon's below-arena fall region. It does not interrupt
  the Chapel's scripted one-HP defeat. Stranded Graveyard eligibility requires
  native arrival flag 101.
- Hadeon grants/refills the existing three-stage Thorn Ward at 75% and 50% HP,
  using separate attempt flags 1055422930 and 1055422931. The 25% shriek, fall
  attrition, deflect thorns, victory/rewards and follower abilities are unchanged.
- Left statue, key prop, barrier and torch now use 1055420924. The right still
  uses 1055420920. Vanilla 18000570 is never read or cleared by the custom gates.
  No migration copies its value. Hadeon's own defeat 1055420915 already controls
  his outer barrier independently of the vanilla exterior door. Rick's existing
  one-time catch-up key award remains available on imported vanilla saves.
- The key knight retains NPC 43519000, entity 18000258, AI and reward. Base HP
  changes 576 -> 461; toughness 35 -> 28; stance durability 65 -> 52. Its unused
  resident slot 17 receives effect 1627114, with five outgoing attack-rate
  multipliers 0.9 and SA attack multiplier 0.8. This does not change guard stamina
  damage or the shared enemy difficulty/Nemesis system. Defense calculations mean
  actual damage need not fall by exactly 10%.
- Common event 5750362 waits for the initial Chapel cutscene to finish, then
  plays effect 1627113 for three seconds with the existing Nemesis screech.
  Saved journey flag 1055420925 prevents repeats. Native arrival flag 101 excludes
  progressed saves and later Four Belfries visits. No real eclipse flags, enemy
  enhancement, travel restrictions or healing penalties are applied by the omen.
- Existing crystal omen requests remain unchanged. The outside cue now requires
  crystal-destroyed flag 1055420918 to be OFF both before and after its two-second
  delay. The player must still occupy the exterior trigger after the delay;
  backing inside leaves the cue available for a later exit.
- Both imp torches and Hadeon's entrance torch still return to their original
  normal variants after Hadeon dies. Their model SFX offsets are untouched.

Description and acquisition
---------------------------

The local Nexus full description now uses directional hints for custom rewards
and ordinary acquisition instructions for unchanged items. Its tome section
describes the eight implemented subjects and discovery-order numbering, replacing
the obsolete fixed two-volume account. Recipe requirements remain explicit where
needed. This does not publish a remote Nexus update.

The Stormblessed Zweihander's existing rarity 3 and item lot 10000320 are unchanged.
The lot inherits item rarity (-1 override), compared with the replaced shield's
rarity 1. No map changes are part of this update. Actual glow and pickup availability
on an imported save remain gameplay checks.

Verification and recovery
-------------------------

Temporary before-copies and native/event evidence are retained under
`.codex-temp/beginner-rescue-20260924`. The native candidate preserves every other
NPC row, every pre-existing effect row and all other parameter tables. The custom
knight changes only its four specified fields. Compiled event review allows only
common constructor/5750360 plus new 5750361/5750362, and the Graveyard constructor
and 5750306; other events, ordering and metadata are preserved.

See ER-073 through ER-078 in [the test matrix](../TEST-MATRIX.md). Static checks,
editor synchronization and deployment verification do not mark gameplay Passed.
