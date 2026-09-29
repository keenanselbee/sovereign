Hadeon teleport destinations
============================

The authored landing markers in the saved map own position, height and initial
facing. `destinations.json` explicitly registers the eighteen permitted markers
and stable helper IDs. Do not treat every spherical region as a destination:
18002390 is the death-dialogue carrier, and return/home markers have other roles.
The original eight destinations remain; 18002383-18002389 and 18002391-18002393
are the ten author additions. Every caller retains its post-warp RotateCharacter
instruction, so authored initial facing is followed by turning toward the player.

`Program.cs` regenerates only named, registered helpers from current map geometry.
The 153 comparison boxes select by horizontal distance. Eighteen 2.5 m clearance
spheres and eighteen 8 m Vortex eligibility spheres use actual three-dimensional
landing positions, including raised point 18002384. Existing IDs 18005900-18005943
are retained; new helpers use collision-checked IDs 18005101-18005245. The accepted
expansion leaves all 44 earlier helpers unchanged and adds 145.


Build and update
----------------

First reconcile the repository and saved Smithbox map. Use a new candidate folder:

```powershell
$eventInputs = Get-ChildItem mod/event/*.emevd.dcx | ForEach-Object { $_.FullName }
dotnet run --project src/recipes/hadeon-teleport/Teleport.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  mod/map/MapStudio/m18_00_00_00.msb.dcx `
  .codex-temp/hadeon-teleport/new-candidate `
  'Z:/Modding/Elden Ring/Tools/Smithbox' `
  src/recipes/hadeon-teleport/destinations.json `
  src/events/m18_00_00_00.emevd.dcx.js `
  --editor-map 'Z:/Modding/Elden Ring/Smithbox/map/MapStudio/m18_00_00_00.msb.dcx' `
  @eventInputs
```

The candidate directory contains the packed map, geometry `regions.json` and a
validation receipt. Review unchanged/rebuilt native roundtrips, ID collisions,
geometry sampling and reversal of helper changes before accepting the map and
copying its geometry snapshot to this folder. No builder writes its inputs.
Moving an authored marker requires regeneration: do not hand-move its helpers.

Generate all four event selector blocks together:

```powershell
python src/recipes/hadeon-teleport/generate-selector.py `
  src/recipes/hadeon-teleport/regions.json `
  .codex-temp/hadeon-teleport/new-events.js `
  --events src/events/m18_00_00_00.emevd.dcx.js
```

Review that candidate before replacing the event source. Compile with
`python tools/sovereign.py build-events`, inspect decoded differences, and accept
source, event binary and map through the
[guarded workflow](../../../docs/workflows/build-and-handoffs.md).
Historical eight-point recipes must not be replayed against the expanded map.


Runtime and verification
------------------------

Selection runs once on each existing entrance/fall/periodic/Vortex request.
A forward tournament evaluates at most seventeen distance comparisons for eighteen
points; it neither introduces a new worker nor continuously polls helper regions.
First/repeat entrances share a selection path in event 5750311, retaining their
12.2-second voice cue and one-second repeat delay. Early hits still engage without
a delayed warp. Fall recovery remains 5750304; periodic and Vortex remain 5750430
and 5750432. Periodic retry/reset labels are L19/L20; the common selector uses
L0-L18. Entrance skip/engage labels are L20/L19. These explicit labels avoid the
native 255-instruction conditional-skip limit. The generator rejects more than
18 points until these caller budgets are redesigned.

Vortex checks use short-lived nested conditions rather than retaining one AND
group per destination. The 8 m reach allowance, both-character clearance, cue
consumption, animation continuity, cooldown sharing and encounter guards remain.
Periodic no-landing retries retain their existing 0.25-second delay and AI action
boundary requirement. The expansion does not create a tighter polling loop.

Run `node --test tools/tests/test-hadeon.mjs`. Tests cover every destination in
all five paths, timing, early hits, cancellation, three-dimensional clearance,
horizontal ranking, authored warp before player-facing rotation and the
seventeen-comparison bound. The native recipe separately tests decoded box/sphere
geometry and preservation. Actual engine boundaries, safe floors, orientation,
Vortex continuity and frame time remain in-game acceptance checks.
