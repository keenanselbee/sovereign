Hadeon audio test parameter patch
================================

This isolated recipe sets only NpcParam 25000011 `SoundAddBankId` from -1 to
9998. `SoundBankId` stays -1, retaining the original c2500 model sounds. The
builder rejects an already assigned additional bank and validates every decoded
NPC field, untouched parameter table and binder metadata after writing.

```powershell
dotnet run --project src/recipes/hadeon-audio-test/AudioTest.csproj '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- <absolute-baseline-regulation> <new-absolute-candidate-directory> 'Z:/Modding/Elden Ring/Tools/Smithbox' 9998
```

Review `validation.json` before accepting the candidate. The accepted runtime
already contains the patch; rebuild from a reviewed baseline, never apply twice.
After game updates, use the current regulation and ParamDef and repeat the
collision and preservation checks. Do not replace the current game regulation
with this trial's historical input.

The source event in `src/events/m18_00_00_00.emevd.dcx.js` separately passes an
entrance-only argument into event 5750302. That event plays Voice 999800001 after
enabling Hadeon; the bounds-recovery caller passes zero. No new save flags are
allocated. See the [test report](../../../docs/test-results/2026-09-26-hadeon-audio-test.md)
for audio source ownership, validation and recovery.
