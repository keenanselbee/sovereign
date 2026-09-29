Earlier feature-summary prefaces
================================

Archived during documentation consolidation on 2026-09-26. These are former
prefaces from three living guides, preserved as history rather than instructions
or current status. Several older values and retry/lighting descriptions were
superseded. Use [the feature evidence owners](../MECHANICS.md#feature-evidence-owners)
and their current qualification records. No game behavior changed in this cleanup.


Design preface
--------------

Current 1.3.3 implementation: aid waits three continuous eligible seconds,
then ramps over ten seconds in twenty five-point steps to 2x HP/FP/stamina maxima
and outgoing damage. Guard stamina cost reaches 0.5x (twice the endurance per
stamina point; approximately four times full-bar endurance with doubled stamina).
Resource percentages, spending protection and ten-second withdrawal remain.
Hadeon returns visibly to his original position facing the barrier; hallway
lights wait one continuous second outside before switching off. See
[implementation and verification](../test-results/2026-09-25-opening-followup.md).
Native/source checks are distinct from pending in-game acceptance.

Approved 1.2.6: [Nemesis's aid](../HADEON-AID-UPDATE.md) visibly builds over ten
seconds on Hadeon arena entry, reaches +50% resource maxima/damage/guard
endurance, holds during the encounter and withdraws over ten seconds after
victory or departure. Withdrawal must not kill a living player; it is not a
repeated resource refill. The sustained shard aura is cosmetic. Actual player
death clears the aid; Oath healing remains outside this change.

The [1.2.5 Hadeon correction](../HADEON-RESET-1.2.5.md) confirms sustained zero HP
before encounter/lighting/milestone resets, cancels recovered retreat requests,
and removes the light ignition flashes. Native/source checks pass; game retest
is still required.

The author-approved [1.2.4 opening support update](../OPENING-SUPPORT-1.2.4.md)
restores movement scaling with bounded diagnostics, corrects room ignition flags,
adds the Ultimate lesson and an ordinary lethal-hit beginner rescue. Generic
Ultimates, including Obliterator's generic fallback, gain launch back; custom
signature paths remain unchanged. Game acceptance is pending.

The [Rick visible transition](../RICK-ENCOUNTER-UPDATE.md) is now implemented locally
and synced to editors, awaiting deployment/game testing: stance-break bait at 25%
HP, two-second golden warning, one charged burst at 75% base attack power,
Hoarah vocal and a visible actor swap. Every attempt starts with the soldier;
only final victory persists. No percentage-HP damage or black fade is used.

Approved room follow-up: remove the two ceiling Grafted Scions; illuminate the
boss room through a short randomized ignition sequence, then retain HP-based
brightness and Nemesis gaze pulses. Hallway candles switch off outside their own
boxes while Hadeon lives, remain on after victory, and switch off after crystal
destruction. See [the implementation record](../HADEON-LIGHTING-UPDATE.md).

Version 1.1.6 corrects the [Hadeon lighting update](../HADEON-LIGHTING-UPDATE.md):
82 room candles use grouped red-light presets preserving their source settings.
The 74 particle flames stay continuous; eight other assets use illumination only.
Models and hallway controls remain unchanged; visual/performance playtests are pending.

The 1.1.4 [Hadeon lighting update](../HADEON-LIGHTING-UPDATE.md) adds staged brazier
illumination, brief gaze surges, victory/crystal hallway states and a five-second
crystal cue followed by room dimming. In-game visual and performance checks are pending.

The 1.1.0 [Chapel reward update](../CHAPEL-SHARD-UPDATE.md) replaces the maiden's
Wizened Finger with one existing Darklight Shard and moves the finger to Kale for
100 runes. The [1.1.1 Chapel fix](../CHAPEL-POLISH-UPDATE.md) removes the remaining
finger restriction and ground message, revises shard text, and completes omen VFX.

The 1.0.9 [opening update](../BEGINNER-OPENING-UPDATE.md) adds the 45-second
beginner rescue, grants Hadeon Thorn Ward at both 75% and 50%, separates the left
imp flag from vanilla, softens the key knight, adds the initial Chapel omen and
suppresses the exit omen after crystal destruction. Gameplay acceptance is pending.



Balance preface
---------------

Current 1.3.3 implementation: aid waits three continuous eligible seconds,
then ramps over ten seconds in twenty five-point steps to 2x HP/FP/stamina maxima
and outgoing damage. Guard stamina cost reaches 0.5x (twice the endurance per
stamina point; approximately four times full-bar endurance with doubled stamina).
Resource percentages, spending protection and ten-second withdrawal remain.
Hadeon returns visibly to his original position facing the barrier; hallway
lights wait one continuous second outside before switching off. See
[implementation and verification](../test-results/2026-09-25-opening-followup.md).
Native/source checks are distinct from pending in-game acceptance.

Approved 1.2.6: [Hadeon aid](../HADEON-AID-UPDATE.md) uses twenty 2.5-point steps
over ten seconds, reaching 1.5x maximum/current-resource scaling and damage.
Current bars retain their percentage and intervening resource spending.
Guard cost is reciprocal (2/3 at full aid), giving 1.5x endurance per stamina
point and approximately 2.25x full-bar endurance with the stamina increase.
Ten-second withdrawal preserves at least 1 HP, including a partial blessing.
This changes the opening player's support, not Hadeon's NPC stats. Runtime
resource behavior and fight difficulty still require game testing.

Approved 1.2.4: beginner rescue retains the 30% threshold and full heal, with a
shared 30-second cooldown reduced to 15 seconds inside Hadeon's arena and a brief
post-heal damage shield. Try lethal-hit interception without changing Oath healing.
Generic Ultimates gain small launch back; Hadeon's local resistance permits that
reaction, including from other attacks. Damage/poise damage remain unchanged.
See [implementation and pending game checks](../OPENING-SUPPORT-1.2.4.md).



Mechanics preface
-----------------

Current 1.3.3 implementation: aid waits three continuous eligible seconds,
then ramps over ten seconds in twenty five-point steps to 2x HP/FP/stamina maxima
and outgoing damage. Guard stamina cost reaches 0.5x (twice the endurance per
stamina point; approximately four times full-bar endurance with doubled stamina).
Resource percentages, spending protection and ten-second withdrawal remain.
Hadeon returns visibly to his original position facing the barrier; hallway
lights wait one continuous second outside before switching off. See
[implementation and verification](../test-results/2026-09-25-opening-followup.md).
Native/source checks are distinct from pending in-game acceptance.

The [ground-stomp investigation](../GROUND-STOMP-GOAL.md) records the approved
jump-counter goal and implemented Hadeon entry lesson. On 2026-09-26 the author
confirmed the Hadeon two-field trial works: guard, deflect and roll rejection
alongside normal-jump and jump-attack clearance. Version 1.3.4 extends the same
two flags to thirteen more priority rows, making fourteen total. The author's
subsequent explicit instruction expands this to all 47 reviewed rows in 1.3.5. Damage,
collision, timing and airborne-avoidance flags remain unchanged. Each newly
converted family still needs its own gameplay test; see the
[full-batch report](../test-results/2026-09-26-jump-all47.md).

Version 1.2.6 adds [Hadeon's arena aid](../HADEON-AID-UPDATE.md): ten-second ramp
to +50% resource maxima/damage and reciprocal guard stamina cost, proportional
current resources, visual-only shard aura and a safe ten-second withdrawal on
victory/departure. Beginner rescue uses effective maximum HP. Native/source
checks pass; resource ordering and presentation still require game acceptance.

The [Rick visible transition](../RICK-ENCOUNTER-UPDATE.md) is now implemented locally
and synced to editors, awaiting deployment/game testing: stance-break bait at 25%
HP, two-second golden warning, one charged burst at 75% base attack power,
Hoarah vocal and a visible actor swap. Every attempt starts with the soldier;
only final victory persists. No percentage-HP damage or black fade is used.

The approved [room follow-up](../HADEON-LIGHTING-UPDATE.md) is implemented locally:
ceiling Scions are suppressed, room illumination ignites in 26 staggered banks,
and hallway proximity controls re-arm on exit. Event compilation and source
simulation pass; deployment and game acceptance remain pending. Rick's visible transition is implemented as described above.

Version 1.1.7 requires both statue activations for one shared imp barrier
([gate ownership](../GRAVEYARD-KEY-GATES.md)). It also removes the invalid unused
light node from candle flame FXR 7506110, preserving all other decoded source
fields. The [1.1.6 room-entry crash](../test-results/2026-09-24-hadeon-room-entry-crash.md)
requires a corrected in-game retest; static checks are not gameplay acceptance.

Version 1.1.6 corrects the [Hadeon lighting update](../HADEON-LIGHTING-UPDATE.md):
82 room candles use grouped red-light presets preserving their source settings.
The 74 particle flames stay continuous; eight other assets use illumination only.
Models and hallway controls remain unchanged; visual/performance playtests are pending.

The 1.1.4 [Hadeon lighting update](../HADEON-LIGHTING-UPDATE.md) adds staged brazier
illumination, brief gaze surges, victory/crystal hallway states and a five-second
crystal cue followed by room dimming. In-game visual and performance checks are pending.

Version 1.1.3 restores a later Favor upgrade: Hadeon grants +1, the Shunning-Grounds
duplicate becomes one Darklight Arc, and Ashen Leyndell retains +2. The custom +3
is removed without old Sovereign-save conversion. See [the progression update](../FAVOR-PROGRESSION-UPDATE.md)
for exact rows, unchanged collection flags and the included short-fall correction.

The 1.1.2 [Rick follow-up](../RICK-ENCOUNTER-UPDATE.md) adds saved phase-two retries,
an explicit ground-level warp target, Hoarah Loux's transition vocal with a hidden
sound carrier, hittable transition protection, and normal Nemesis visuals on the
beginner rescue heal. Native/source checks do not establish gameplay acceptance.

The 1.1.0 [Chapel reward update](../CHAPEL-SHARD-UPDATE.md) replaces the maiden's
Wizened Finger with one existing Darklight Shard and moves the finger to Kale for
100 runes. The [1.1.1 Chapel fix](../CHAPEL-POLISH-UPDATE.md) removes the remaining
finger restriction and ground message, revises shard text, and completes omen VFX.

The 1.0.9 [opening update](../BEGINNER-OPENING-UPDATE.md) adds the 45-second
beginner rescue, grants Hadeon Thorn Ward at both 75% and 50%, separates the left
imp flag from vanilla, softens the key knight, adds the initial Chapel omen and
suppresses the exit omen after crystal destruction. Gameplay acceptance is pending.
