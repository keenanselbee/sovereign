Deflect stamina cost recipe
==========================

This guarded recipe multiplies five existing deflect `guardStaminaMult` values
by 0.75. It leaves ordinary guarding, stamina recovery, timing windows and all
other fields unchanged. Reapplying to an already changed baseline is rejected.
The two-handed effect retains its existing category and application behavior;
the combined in-game cost still needs measurement.

Run from the repository root, using a new scratch output directory:

```powershell
dotnet run --project src/recipes/deflect-stamina/Inspect.csproj -p:SmithboxRoot="Z:/Modding/Elden Ring/Tools/Smithbox" -- mod/regulation.bin .codex-temp/deflect-cost-candidate "Z:\Modding\Elden Ring\Tools\Smithbox"
```

The candidate is independently reread and compared across all parameter rows,
other binder members and binder metadata. It does not accept or deploy files.
