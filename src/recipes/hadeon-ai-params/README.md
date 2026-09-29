Hadeon AI parameter recipe
==========================

Clones `NpcThinkParam` row 25009000 into unused private row 25009900, changing
only the clone's name and `logicId` from 10000 to 250090. The native battle goal
remains 250010. Changes only Hadeon actor 18002354's map Think assignment to
25009900. The original Think row and every other map field remain unchanged. Build this with the matching private
logic binder from [the AI source](../../ai/hadeon/README.md) before deployment.

```powershell
dotnet run --project src/recipes/hadeon-ai-params/HadeonAIParams.csproj -p:SmithboxRoot="Z:/Modding/Elden Ring/Tools/Smithbox" -- <accepted-regulation.bin> <new-candidate-directory> <Smithbox-directory> 250090 <accepted-m18_00_00_00.msb.dcx>
```

The candidate builder guards the original logic and battle IDs, compares every
decoded original Think row and field, checks unrelated tables byte-for-byte,
and preserves binder/member metadata. Full decoded map comparison verifies only
the one actor assignment changes, including preservation of region shapes. It writes a validation receipt and never changes runtime
or editor files. Game behavior requires a separate encounter test.
