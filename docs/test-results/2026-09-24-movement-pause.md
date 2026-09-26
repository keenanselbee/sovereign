# Intermittent player movement pause

The author reports that holding the left stick forward can produce a run-to-walk
transition followed by about one second of idle, after which movement resumes.
The first report associated this with descending stairs. Later observations
established that flat ground also reproduces it and that it can happen both
roughly six seconds after loading and later during play. Neither a slope nor
loading is a required trigger. No independent reproduction or runtime state
capture has been performed. The exact save, active buffs, equipment, location
and input configuration are not yet recorded.

This follows the author's report that the earlier movement fixes did not resolve
the symptom. It does not establish a failure of their narrower backstep,
wall-jump or protected-fall conditions.

## Inspection

- Repo, saved Script workspace and live `c0000.hks` match SHA-256
  `53f4e79f7c1bab693f33657b37bd3fcbbf08c629f25fd5d65f0c0fa02936da64`.
  The previous protected-fall height correction is present on disk. This cannot
  establish which file an already-running game loaded.
- The inspected `MoveStart`, `IdleCommonFunction`, `LandCommonFunction` and
  `LandLow_onUpdate` control flow matches the archive-derived vanilla reference,
  allowing for named engine-call aliases and formatting. Movement recovery checks
  current `MoveSpeedLevel`; it does not require releasing and pressing the stick.
- The a00 fall/landing records 4050, 4100, 4200, 4210, 4220, 4290, 202040,
  202100, 202110, 202120 and 202130 have matching animation headers and event
  type/timing/meaningful payload bytes against the retained current vanilla
  export. The inspected mod a00 export hash matches the current loose source.
  Heavy landing 202140 additionally applies effect 3510. These comparisons do
  not qualify every weapon category, clip, or live animation state.
- Fresh native inspection of current regulation confirms that plunging markers
  900/910 change attack multipliers, not movement. The inspected rescue visuals
  1626986/1626991/1626993 and omen visual 1627115 do not contain movement-control
  state information or an effect chain causing an idle action.
- `ModAnimationControl` can force idle with states 7000/7001 or request movement
  with states 7000/7003. Repeated entry would reset actual movement speed through
  the normal event helpers, so this remains worth observing at runtime. No
  inspected ordinary small-fall timeline supplies those custom cancel effects;
  there is no evidence yet that this path runs during the reported pause.
- Startup and periodic common events were inspected. No unconditional
  six-second startup movement lock was identified. Conditional six-second
  inventory exchanges and Oath icon updates are not proof of the cause.

## Next discrimination

Repeat on flat ground with keyboard W and with the controller, without sprint,
jump or an attack. Check whether camera/enemy motion continues during the pause.
If keyboard movement is unaffected, investigate the controller/input path. If
both inputs fail while the rest of the game continues, capture `MoveSpeedLevel`,
`MoveSpeedLevelReal`, `MoveSpeedIndex`, active locomotion/fall/landing nodes and
custom cancel states at the interruption before choosing a gameplay patch.
If the whole game stalls, investigate frame-time or streaming behavior instead.

Root cause remains unconfirmed. The initial investigation did not change runtime
files. A read-only native parameter export and its helper remain in
`.codex-temp/movement-pause-20260924/` for follow-up.

## Author-requested cancellation isolation

The later request temporarily bypasses only the `ModAnimationControl()` call in
`Update`. The helper remains intact for restoration. Divinity's separate
state-7997 cancellation, jump, landing and movement multipliers are unchanged.
This isolates the shared helper; it does not disable every cancellation route.

Both saved copies matched before editing. Backups and their hashes are in
`.codex-temp/rick-pause-review-20260924/backup-manifest.json`. An exact byte
comparison confirms the commented call and explanatory comment are the only HKS
change. Native player assets reused their qualification with fresh HKS guards;
no Lua compiler or gameplay result is implied.

The qualified handoff `8f5101bbb56040df95d8c13bc102e050` synced the Script
workspace. Both copies now hash to
`fb5e128c9dcb076c23d5e0a3d305ba52cc2132eae044c26b1cea5277c0150859`.
No deployment was requested or submitted. Test after explicitly deploying this
diagnostic and restarting the game; the existing running build is unaffected.


The later authorized 1.1.9 deployment includes this diagnostic. Live bytes were
verified; the movement retest remains pending. See [deployment evidence](2026-09-24-lighting-rick-1.1.9.md).


## 1.2.1 diagnostic: custom airborne actions

The author reports that the pause persists with shared animation control disabled,
including a one-to-two-second movement lock after a boss fog entrance. Live and
repo c0000 files matched the disabled diagnostic during investigation. This weakens
that helper as the cause; it does not rule out Divinity's separate cancellation.

Restore ModAnimationControl and bypass only the Update call to ModJump. Normal
jumping/landing and protected lethal-fall handling stay intact. Custom wall/double
jump, jump casting, air dash and the plunge-damage update inside ModJump are
inactive for this diagnostic. The handler remains intact for restoration. Restart
the game before testing fog entry, ordinary ground movement and small drops.
No cause or gameplay resolution is established by this isolation build.


## Local follow-up: custom speed isolation

The author reports continued slowdown to a stop a few seconds after spawn despite
the 1.2.1 custom-jump bypass. Current repo/live player hashes matched during review.
Restore ModJump and retain ModAnimationControl. Bypass the Update call to
ModMovementMultiplier and the three custom SetMovementScaleMult calls in
Move_onUpdate. Buff selection of roll/jump multipliers remains intact, as do
native movement acceleration, jump and landing functions. This isolates the two
custom action/ground speed overrides; it is not a bypass of every native or
custom movement-related instruction. No continuous forced multiplier reset is
added. Root cause remains unknown. These edits are included in the authorized 1.2.2 deployment batch; game retest remains pending.
