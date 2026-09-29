Hadeon periodic teleport AI parameter recipe
===========================================

This guarded candidate builder changes only `battleGoalID` in existing private
`NpcThinkParam` row 25009900 from native 250010 to private 250091. It preserves
the row's logic goal 250090 and does not change the map assignment. Use it after
other parameter candidates in the same update have been accepted as inputs.

```powershell
dotnet run --project src/recipes/hadeon-periodic-ai/HadeonPeriodicAI.csproj -p:SmithboxRoot="Z:/Modding/Elden Ring/Tools/Smithbox" -- <accepted-regulation.bin> <new-candidate-directory> <Smithbox-directory>
```

The output directory must not exist. The builder checks the expected old value,
compares all other decoded Think fields, all unrelated tables and binder metadata,
then decrypts and verifies the candidate. It writes a validation receipt and does
not change accepted runtime or editor files. Build the matching private battle
binder from [the AI source](../../ai/hadeon/README.md) before using this candidate.
