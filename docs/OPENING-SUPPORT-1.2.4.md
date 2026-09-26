Opening support update 1.2.4
============================

Author-approved implementation, 2026-09-24. Game acceptance remains pending.

Movement investigation
----------------------

Restore `ModMovementMultiplier` and the three directional ground-scale calls.
Custom jumping and animation control remain enabled. Disabling each separately
did not eliminate the reported slowdown, including on new characters with no Oath.
This rules out those individual bypasses as fixes, not every possible interaction.

A temporary read-only HKS trace samples five times per second, capped at 600
samples per script instance. It records elapsed time, game-reported input level,
computed speed, locomotion/lower-body state, movement-cancel permission, action and
gesture requests, force-walk 4101/1626974, gesture 100200, opening landing 1627121,
HP and last rescue time. Input level is not raw controller input.

Where HKS exposes Lua file I/O, the trace writes `Sovereign-movement.log` relative
to the game's working directory, in batches of 25 samples. File failures are caught.
Otherwise it uses installed Scripts-Data-Exposer action 10001; this creates no
console. Retail capture availability is not verified. The logger issues no movement
or animation commands. Reproduce soon after loading and compare input and speed
with state/effect markers. A falling input level still needs comparison with
physical controller/keyboard input before assigning the fault to Sovereign.

Lighting and tutorial
---------------------

The 42 ignition gates move from invalid 1055423000-1055423041 to unused, valid
temporary flags 1055425000-1055425041. The old block cannot hold these flags; the
previous source simulation wrongly accepted every integer. The test now rejects
invalid Sovereign blocks. No map, FXR, intensity, ten-second ignition, defeat or
crystal-dimming change accompanies this correction.

Common event 5750363 waits four uninterrupted seconds inside arena entity
18000359, excluding fatal-fall region 18002367. Leaving, falling, map departure or
death cancels the delay. Only the host can show it, before Hadeon's defeat.
Saved Sovereign flag 1055420927 is written immediately before the popup. Retired
Rick flag 1055420926 and vanilla tutorial flags are untouched.

New TutorialParam 5750 uses existing Guard Counters image 18, text 5750363 and
unlock flag 1055420927. All three English menu binders receive two new entries:

**Ultimate Attacks**

Successful deflections and defeated enemies build toward your weapon's Ultimate
attack. Watch the Ultimate icon fill to see when it's ready.

Once ready, tap Block and Heavy Attack simultaneously to unleash your weapon's
Ultimate. Press both together rather than holding Block first.

Ultimates unleash powerful attacks whose effects vary by weapon.

Beginner rescue
---------------

Common event 5750361 supplies short-lived permission only in the Chapel and
Stranded Graveyard, retaining opening readiness, scripted-defeat, Rick-transition
and fatal-fall-region exclusions. Hadeon defeat ends that worker. HKS consumes
the rescue at 30% HP or below (above the scripted one-HP state), or in the ordinary
damage death handler before its native death request.

The same function starts both cooldown effects before restoring HP to maximum.
The minimum is 15 seconds; outside Hadeon's arena the 30-second effect must also
expire. Crossing the boundary never resets either timer. Both are non-extendable
and deleted on death. The event supplies existing Nemesis visuals and sound after
consumption without a second heal. Oath healing and its follow-on are unchanged.

| SpEffect | Purpose | Duration |
| --- | --- | --- |
| 1627122 | Opening rescue eligibility | 0.3s, refreshed every 0.1s |
| 1627123 | Arena cooldown eligibility | 0.3s, refreshed every 0.1s |
| 1627124 | Consumed rescue presentation request | 1s, cleared by worker |
| 1627125 | Zero incoming player/enemy/object damage rates | 0.5s |
| 1627126 | Minimum shared cooldown | 15s |
| 1627127 | Outside-arena shared cooldown | 30s |

Lethal interception requires received damage and excludes fatal falls, deathblight,
stone/crystal death states, scripted-death effects, ladders and mounted states.
Engine ordering of lethal hits and simultaneous status damage needs game testing.
No save conversion or vanilla progression flags are introduced.

Generic Ultimate launch
-----------------------

SpEffect 241/243 change only `repAtkDmgLv` from 5 (long stagger) to 6 (small launch
back), using the SpEffect enum, not the different AtkParam enum. Generic Ultimates
and Obliterator's generic fallback inherit it. Custom signature paths and their
TAE/attack rows, damage and poise damage are unchanged. Targets can resist launch.

Hadeon's NpcParam 25000011 resident slot 2 replaces shared 5362 with local clone
1627128. The clone changes only `dmgLv_BlowS` from 4 to 6. Other Crucible knights
and shared 5362 are untouched. Other attacks with this reaction can also launch
Hadeon; this is not an Ultimate-specific target exception. Actual animation and
bridge knockback distance require gameplay confirmation.

Verification and recovery
-------------------------

Backups/hashes: `.codex-temp/opening-1.2.4/backup/` and `backup-manifest.json`.
Editor handoffs keep their own recovery copies. Native regulation comparison
verifies 11 intended rows only, other rows/tables intact and binder metadata
preserved. New tutorial flag allocation was checked across native parameters and
current event sources. Event comparison by ID limits changes to the two affected
constructors, rescue, lighting controller and the new tutorial. English text
rebuilds pass exact decoded comparison, including missing-versus-null checks.

Source simulations cover lighting, tutorial cancellation and rescue eligibility.
The isolated rescue function runs with mocked game calls in the existing
ModEngine Lua runtime to test cooldowns, repeated consumption and death exclusions;
this is not HKS engine qualification. Coordinated player qualification checks
assets/source guards, not live movement behavior.

Manual checks remain: ordinary lethal rescue; 15/30-second boundary cooldown;
scripted defeat/fatal fall unaffected; tutorial once after four seconds; ten-second
room ignition; victory/crystal states; generic one/two-handed Ultimates and
Obliterator fallback launch; signature paths unchanged; movement trace capture.
