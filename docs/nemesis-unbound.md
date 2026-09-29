Nemesis Unbound
===============

Accepted direction, 2026-09-27. The story expansion and weapon restriction below
are deferred; this document does not claim that they are implemented.

Nightmare difficulty names Sovereign's combat challenge. Crystal destruction is
a story transition, not a separate difficulty mode. Hadeon's defeat grants access
to the prison; breaking the crystal releases Nemesis. Earlier appearances can be
manifestations of his imprisoned influence.


Story progression
-----------------

The intended sequence is Hadeon defeated, prison accessible, qualifying attack
breaks the crystal, Nemesis Unbound, final confrontation, then a defined resolution.
The last encounter and the world's condition after victory still need design.
Hostile enemies should visibly reflect the released influence, preserving friendly
NPCs and essential scripted encounters. Loaded enemies and later spawns both need
explicit coverage; the existing eligibility filters do not guarantee every enemy.

The Bindseal currently suppresses the lasting eclipse while equipped. Changing it
to personal protection without reversing the story stage is a proposal, not part
of the current runtime changes. Keep difficulty, prison release and final victory
as distinct concepts rather than reinterpreting one existing flag for all three.


Qualifying crystal attacks
--------------------------

The approved investigation target is an actual attack signature on Fallingstar
Obliterator, Maliketh's Black Blade and Sacred Relic Sword. A compatible crystal
receiver would recognize that signature and apply special seal damage or trigger
destruction. Ordinary hits must not break it. Account for upgraded variants,
offhand hits, projectiles, multi-hit attacks and multiplayer ownership.

An unused field or ID alone is insufficient: prove that the attack carries the
marker and that this receiver reads it. A weapon-specific on-hit effect and a
character receiver are candidates; neither is qualified yet. The current geometry
asset cannot simply receive character SpEffects. Checking equipped weapons plus
an arbitrary hit would misidentify offhand and lingering projectile attacks.
Do not repurpose a shared damage type or alter damage against ordinary enemies.

Current map entity 18002346 is asset AEG258_158_2019, with 1000 HP and 10000 defense
in AssetEnvironmentGeometryParam 258158. It is not an NPC health proxy. Overlapping
asset AEG258_159_2018 has entity ID 0 and separate 1 HP health. No elemental weakness
is configured in these asset rows. Event 5750291 watches destruction of 18002346
after Hadeon's defeat; no weapon whitelist exists in that event.

Retain the current release flag and journey behavior when the deferred gate is
implemented. Independently test that ordinary damage cannot bypass it and that
each allowed weapon can complete it without another weapon merely being equipped.

See [current mechanics](MECHANICS.md#nemesis-and-the-physical-red-crystal) and
[release persistence](NEMESIS-PERSISTENCE.md) for the existing implementation.
