Deflection tutorial texture
===========================

The approved layered artwork is in `images/mockups/deflection-v3/`. Its
`compose.ps1` combines the clean scene, blank gold panel and extracted game icon
20297 into `mockup.png`. The panel contains no text or charge diamonds.

`build.ps1` converts that PNG to the original 544x336, one-mip BC7 DDS layout and
replaces only `MENU_Tuto_00016.tpf.dcx` in a scratch copy of the texture package's
`00_solo.tpfbhd`/`.tpfbdt` pair. It accepts the two qualified pair baselines as
complete identities, including the tutorial member hash. It requires an empty
output directory, WitchyBND and DirectXTex `texconv` supplied as paths:

```powershell
.\src\textures\deflection-tutorial\build.ps1 `
  -OutputDirectory .codex-temp\deflection-tutorial-build `
  -WitchyBnd 'Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe' `
  -Texconv 'C:\Windows\System32\texconv.exe'
```

The script produces a candidate only. Before accepting its paired archives,
reopen the candidate and compare every member's name, ID, flags and payload hash
against the baseline. The sole expected difference is the payload of
`00_Solo\MENU_Tuto_00016.tpf.dcx`; inside that TPF, the texture metadata and DDS
header stay unchanged while the BC7 blocks change. Then inspect the decoded
544x336 artwork. This does not establish the in-game appearance.

On 2026-09-25, an unchanged round trip of the original 3,079-member archive was
byte-identical. The edited candidate preserved every other member's payload and
metadata, as well as all tutorial TPF metadata and DDS header bytes. Its accepted
pair hashes are `4FD01F5ED33EC29BB7C37E51E34765467C7FF84FF09DDE390F1714B627ED4D22`
for `.tpfbhd` and `CE8EF7371ED16015FB309AE23C4A1B61194220EB3ABDA80CC54863F9751149CF`
for `.tpfbdt`. Rebuilding from that accepted pair produced both files byte-for-byte.
Game appearance remains untested.
