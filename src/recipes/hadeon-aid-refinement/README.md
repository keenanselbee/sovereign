Hadeon aid and rescue cooldown refinement
========================================

`Program.cs` builds an isolated regulation candidate from an explicitly selected
current regulation. It requires effect 1627127 to have `effectEndurance` 30 seconds
and rows 1627161-1627170 to be unoccupied. It changes 1627127 to 40 seconds and
adds ten clones of that cooldown with durations 38, 36, ... 20 seconds. The HKS
selects a clone by saved counted losses only during admitted arena aid. Existing
effect 1627126 remains the shared 15-second floor.

```powershell
dotnet run --project src/recipes/hadeon-aid-refinement/AidCooldown.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  <input-regulation.bin> <new-output-directory> `
  'Z:/Modding/Elden Ring/Tools/Smithbox'
```

The output directory must not exist. The recipe checks parameter readback, binder
metadata, every unrelated table and original SpEffect field, and input stability.
`validation.json` records hashes and the exact duration schedule. This establishes
a candidate, not game acceptance or authorization to replace the runtime file.
