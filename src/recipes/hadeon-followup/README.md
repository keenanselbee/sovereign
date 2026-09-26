Hadeon follow-up native patch
============================

`Program.cs` applies the approved 1.3.3 changes to an explicitly selected pre-change
regulation and map. It requires the qualified Smithbox libraries externally.
Run from the repository with an output directory that does not yet exist:

```powershell
dotnet run --project src/recipes/hadeon-followup/Patch.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  <baseline-regulation.bin> <baseline-m18_00_00_00.msb.dcx> `
  <new-candidate-directory> 'Z:/Modding/Elden Ring/Tools/Smithbox'
```

The baseline must still have twenty 2.5-point aid tiers and no region 18002380.
The script rejects already-patched inputs. It changes fourteen fields per tier
(resource maxima, ten outgoing damage multipliers and reciprocal guard cost),
then adds one return region at the original spawn position, rotated 180 degrees.
It verifies decoded readback, unchanged other tables/member metadata, and removal
of the added region reproducing the original decoded map. `validation.json`
records hashes and exact changes. Review that receipt before guarded acceptance.
This is a patch recipe, not a complete regulation rebuild or gameplay test.

The 2026-09-25 baseline and acceptance evidence are retained locally under
`.codex-temp/opening-followup-20260925/`. Future game/editor changes require a new
baseline review; never replay the patch blindly onto newer work.
