Hadeon Vortex marker SpEffects
=============================

`Program.cs` builds an isolated regulation candidate with two marker rows:
1627600 for a live Vortex window and 1627601 for a live slam cue. Both clone
current native SpEffectParam row 5039, changing only ID, name and
`effectEndurance` from zero to 0.1 seconds. The template has no icon, behavior,
replacement or occurrence effect. Zero endurance means an instantaneous effect
in the Elden Ring parameter definition. Native c2500 TAE event 67 windows
reference SpEffects 31 and 46, both with 0.1-second endurance. The animation
controls each marker's application window. Runtime marker visibility and cleanup
still need in-game verification. This recipe does not change animation or damage
timing.

Run from the repository with a new scratch directory:

```powershell
dotnet run --project src/recipes/hadeon-vortex-markers/HadeonVortexMarkers.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  mod/regulation.bin `
  .codex-temp/hadeon-vortex-markers/new-candidate `
  'Z:/Modding/Elden Ring/Tools/Smithbox' `
  .codex-temp/flag-allocation-review/current/event
```

The creation mode checks the current native template and absence of the two rows,
searches all 598 current mod and retained vanilla event binaries for references,
and checks 194 regulation members. It checks SpEffectParam references by
decoded integer cells; arbitrary four-byte patterns in raw parameter payloads
are not sufficient evidence of an ID reference. After native write and
readback, it verifies that the two new rows differ from 5039 only by ID, name
and duration, every original SpEffect row is identical, every other regulation
member is byte identical, and binder metadata is unchanged. The candidate and input
hashes are recorded in `validation.json`. Runtime and editor files stay
untouched until a separate reviewed acceptance.

For an existing regulation with the original zero-duration markers, pass
`--repair-duration` before the four usual arguments. This mode requires both
marker rows to match the original 5039 clone, including their names and zero
endurance. It changes only the two durations to 0.1 seconds and verifies every
other decoded row, all other regulation members and binder metadata. Use a new
output directory:

```powershell
dotnet run --project src/recipes/hadeon-vortex-markers/HadeonVortexMarkers.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  --repair-duration `
  mod/regulation.bin `
  .codex-temp/vortex-cue-164/params-candidate `
  'Z:/Modding/Elden Ring/Tools/Smithbox' `
  .codex-temp/flag-allocation-review/current/event
```
