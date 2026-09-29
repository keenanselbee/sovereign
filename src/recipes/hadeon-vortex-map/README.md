Hadeon Vortex teleport eligibility map recipe
==============================================

Historical eight-point radius migration only. For the current eighteen-point
system, use the [unified teleport recipe](../hadeon-teleport/README.md), which
owns both clearance and Vortex spheres. Do not replay this migration against
the expanded map.

`Program.cs` builds an isolated `m18_00_00_00.msb.dcx` diagnostic candidate
that expands the eight existing eligibility spheres from 6 m to 8 m. IDs
18005936-18005943 correspond in order to destinations 18002368-18002373 and
18002381-18002382. Their centers, the 2.5 m destination-clearance spheres and
pairwise selectors 18005900-18005933 remain intact. The recipe requires the
saved Smithbox map to agree with the repository map and each existing sphere
to retain its expected name, center and 6 m starting radius.

The previous 6 m radius was provisional. The inspected c2500 animation 3028 emits bullet
2500271 from sword dummy 11 at 2.667 s. Its `hitRadiusMax` is 2.5 m, and the
static FLVER dummy offset is about 1.47 m horizontally. Adding about 2 m of
wiggle and rounding yields 6 m from the landing center. The static FLVER
position is only a reference; the posed emission source, effective enemy scale,
and engine area membership need in-game calibration. Entering this eligibility
region does not guarantee a hit. The region does not change the slam hitbox.

Run from the repository with a new scratch output directory:

```powershell
dotnet run --project src/recipes/hadeon-vortex-map/HadeonVortexMap.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  mod/map/MapStudio/m18_00_00_00.msb.dcx `
  'Z:/Modding/Elden Ring/Smithbox/map/MapStudio/m18_00_00_00.msb.dcx' `
  .codex-temp/hadeon-vortex-map/new-candidate `
  'Z:/Modding/Elden Ring/Tools/Smithbox' `
  src/events/m18_00_00_00.emevd.dcx.js
```

The recipe requires decoded agreement between the repository and saved
Smithbox map, all 36 retained teleport helpers and exact destination/clearance
centers. Existing `InArea(10000, regionId)` calls may appear in event source;
other source uses stop the build. It writes the unchanged map through the native
MSB serializer, checks each expanded radius with samples in the 2.5-8 m shell
and just beyond its outer edge, then verifies that restoring exactly the eight
previous radii reproduces the full decoded input. The
manifest records input hashes, ID mappings, roundtrip results, and the candidate
hash. Neither input is edited or accepted into runtime by this recipe.

The allocation evidence for temporary flags 1055425258-1055425261 and event
IDs 5750432-5750435 is in
`.codex-temp/hadeon-vortex-map/flag-scan/flag-scan.json`. The native scan covered
598 current mod and retained vanilla event files and 194 regulation members,
with no prior reference or range collision. Repeat this scan before accepting
code that uses the IDs if the inputs change.

For the 1.6.3 diagnostic trial, the same native scan checked temporary outcome
flags 1055425275-1055425278 against the current 598 event files and 194
regulation members with no exact-reference or range collision. Its receipt is
`.codex-temp/hadeon-vortex-map/flag-scan-163/flag-scan.json`. Existing flag
1055425274 already uses this temporary block.
