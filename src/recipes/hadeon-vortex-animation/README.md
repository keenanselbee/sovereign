Hadeon Vortex Slam animation routes
===================================

This recipe builds four private c2500 attack routes from the native Ordovis
Vortex spin slam, animation 3028. Hadeon's private AI can request 3030, 3031,
3032 or 3033 for speeds 2, 7/3, 8/3 or 3 relative to the original motion.
Other Crucible actors retain 3028.
Each route imports the original 3028 HKX motion, copies its 62 native TAE
events, and uses constant TAE event 608 to change playback speed. The c2500
behavior graph adds four Attack states, event transitions and selectors. Each
private clip names its matching TAE timeline while its internal motion index
still references native 3028.

The ground wave is native TAE animation 3028's bullet 271 / SpEffect 625092
at timeline 2.666667. Its preceding sword contact starts at 2.566667. Each
private timeline applies marker SpEffect 1627600 from timeline 0 to 5 and
marker 1627601 for a 0.1-second real-time window. The cue timeline starts
at 0.666667, 0.333333, 0 or 0 for routes 3030-3033 respectively. That is
one real second before the ground wave for the first three tiers. At 3x,
the ground wave arrives only 0.888889 real seconds after the animation starts,
so a full one-second warning cannot fit on this timeline. The marker rows
must exist in the accepted regulation and have no gameplay effect of their own.
Version 1.6.4 corrects their instantaneous duration to 0.1 seconds, following
native type-67 markers in the same attack. Timeline positions stay unchanged;
refresh and interruption behavior still require game verification. See the
[marker recipe](../hadeon-vortex-markers/README.md).
The event/AI handoff consumes the attack arm at the cue and avoids interrupting
the active animation during teleport.

Build from content-verified c2500.anibnd.dcx and c2500.behbnd.dcx inputs.
Keep all intermediate XML, HKX and archive outputs under `.codex-temp`. The
following commands assume the inspected workstation paths and a new scratch
directory. The HKLib executable writes a sibling XML or HKX file with the
same stem as its input.

```powershell
$repo = 'C:/Repositories/Sovereign'
$scratch = "$repo/.codex-temp/hadeon-vortex-animation/rebuild"
$smithbox = 'Z:/Modding/Elden Ring/Tools/Smithbox'
$hklib = 'Z:/Modding/Elden Ring/Tools/HKLibCLI.v0.1.2/net7.0/HKLib.CLI.exe'
$recipe = "$repo/src/recipes/hadeon-vortex-animation"
$before = "$repo/.sovereign/backups/hadeon-vortex-animation"
New-Item -ItemType Directory -Path $scratch -ErrorAction Stop | Out-Null
dotnet run --project "$recipe/HadeonVortexAnimation.csproj" "-p:SmithboxRoot=$smithbox" -- extract-graph "$before/c2500.behbnd.dcx" "$scratch/graph-original.hkx" $smithbox
& $hklib "$scratch/graph-original.hkx"
python "$recipe/build-graph.py" "$scratch/graph-original.xml" "$scratch/graph-candidate.xml"
& $hklib "$scratch/graph-candidate.xml"
Copy-Item -LiteralPath "$scratch/graph-candidate.hkx" -Destination "$scratch/graph-readback.hkx" -ErrorAction Stop
& $hklib "$scratch/graph-readback.hkx"
python "$recipe/verify-graph.py" "$scratch/graph-original.xml" "$scratch/graph-readback.xml" 'Z:/Steam/steamapps/common/ELDEN RING/Game/mod/action/script/c9997.hks' 'Z:/Steam/steamapps/common/ELDEN RING/Game/mod/action/eventnameid.txt' 'Z:/Steam/steamapps/common/ELDEN RING/Game/mod/action/statenameid.txt' "$scratch/graph-validation.json"
dotnet run --project "$recipe/HadeonVortexAnimation.csproj" "-p:SmithboxRoot=$smithbox" -- "$before/c2500.anibnd.dcx" "$before/c2500.behbnd.dcx" "$scratch/graph-candidate.hkx" "$scratch/candidate" $smithbox
```

The builder fails on ID collisions, source drift, unrelated binder changes or
changes to any original TAE record. Do not reuse an existing output directory.

The 3030-3033 slots already have native HKS callbacks, global event/state
names, graph eventNames and eventInfos. The graph recipe attaches four states
to those existing event slots. Native Attack3020-3028 selectors use consecutive
userData values 18546709-18546717; the new selectors use the next four unused
values, 18546718-18546721. No existing graph node uses them. This follows
the native allocation pattern; whether the field affects runtime dispatch
remains subject to the game test. The recipe does not append event names or
eventInfos. The previous 3080-3083 candidate added
names without matching eventInfos and could not dispatch through the native
HKS; do not use it. The qualified correction's graph readback preserved all
2,268 original objects after accounting for object-ID renumbering and added
exactly 12 route objects. Both native event arrays remain at 1,366 entries.
Its TAE readback preserved all 278 original animation records. SoulsFormats
added eight trailing zero alignment bytes to one copied native TAE event in
each private record; all
defined event bytes and timings remained unchanged. The four private records
otherwise add only the speed event and two marker events. The candidate and
receipt are in `.codex-temp/hadeon-vortex-animation/followup-3030-candidate/`.
The graph dispatch receipt is
`.codex-temp/hadeon-vortex-animation/followup-3030-graph-validation.json`.

The first accepted graph kept `animationName=a000_003028` in each private clip,
despite assigning its selector a private `animId`. All native c2500 attack
selectors name the same animation in their clip and selector. This mismatch
can select native 3028's TAE timeline, which contains neither custom marker,
even when the private records themselves read back correctly. The guarded
repair uses `repair-graph.py` on the accepted graph XML, converts the result
through HKLib, and verifies the readback with `repair-graph.py --verify` and
`verify-graph.py`. The former proves exactly four `animationName` changes
across all 2,280 objects; the latter checks native HKS, names, eventInfos,
transitions and original graph content. Use `HadeonVortexGraphRepair.csproj`
to bind the verified graph HKX into an isolated behavior candidate while
preserving all other binder members and the unchanged animation binder.
Inputs, native tools and output directories must be content-verified and
fresh. The 2026-09-28 candidate and receipts are under
`.codex-temp/hadeon-vortex-marker-fix/`. The graph still uses native motion
index 74 and TAE imports source 3028. Runtime marker firing remains an
in-game check.

These are native format checks, not game acceptance. In-game verification must
confirm that event 608 speeds both visible motion and TAE timing, the cue occurs
one real second before the ground wave at every tier, markers clear on
interruption, and only Hadeon can request the private routes. Do not present
an untested tier as gameplay-verified.

To retune the already accepted four private routes, run
`dotnet run --project HadeonVortexRetune.csproj "-p:SmithboxRoot=<Smithbox tools>" -- <accepted c2500.anibnd.dcx> <new scratch output directory> <Smithbox tools>`.
The guarded retune requires the prior 1, 4/3, 5/3, 2 rates and cue markers,
then reads back the native archive. It verifies all 278 other animation records,
every other binder member and metadata, and writes a validation receipt beside
the candidate. The c2500 behavior graph is unchanged by this retune. The
original five-argument builder now uses the same new rates when rebuilding
from a verified native pre-route baseline; do not feed it an accepted archive.
