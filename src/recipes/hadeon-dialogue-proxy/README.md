Hadeon death sound carrier
==========================

The guarded builder adds one map enemy and one NpcParam row to a reviewed
regulation/map pair. Enemy 18002390 clones this map's native hidden sound carrier
18000852, starts at Hadeon's authored position and uses new NpcParam 99989900.
That row clones the native carrier row 47210070 and changes only
`SoundAddBankId` to 9998 and `enableSoundObjDist` to 100. TalkID stays zero.
The builder also updates first-entrance TalkParam row 99980001's descriptive
name to match the new recording; its message and voice IDs are unchanged.

The event must initialize the carrier as the native 18000852 pattern does:
disable the character, AI, collision and gravity; enable invincibility and
default backread. Warp the carrier to Hadeon at death before playing the death
voice from entity 18002390. Keep it loaded until the full voice completes.
The native example proves PlaySE on a disabled carrier in this map; it does not
prove that a disabled character can run talk ESD. Death subtitles still need an
in-game test.

Build into an absent scratch directory, using the reviewed current inputs:

```powershell
dotnet run --project src/recipes/hadeon-dialogue-proxy/HadeonDialogueProxy.csproj '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- <regulation.bin> <m18_00_00_00.msb.dcx> <new-scratch-directory> 'Z:/Modding/Elden Ring/Tools/Smithbox'
```

The builder verifies the input hashes again before completion, preserves
existing parameter tables, rows and binder metadata, and compares the entire
decoded map including region shapes before and after adding the carrier. It
writes only scratch candidates and a validation receipt. It cannot establish
native playback or subtitle behavior.
