Deflection and Ultimate tutorial textures
========================================

The current artwork is `deflection.png` and `ultimate.png` beside this recipe.
The author updated both PNGs on 2026-09-28 after the 2026-09-26 acceptance.
Both are 544x336 with a combat scene and corner icon. Earlier layered artwork remains in
`images/mockups/deflection-v3/` as mockup history, not the runtime build input.

`build.ps1` converts that PNG to the original 544x336, one-mip BC7 DDS layout and
replaces `MENU_Tuto_00016.tpf.dcx` (Deflection) and `MENU_Tuto_00018.tpf.dcx`
(Ultimate) in a scratch copy of the texture package's `00_solo.tpfbhd`/`.tpfbdt`
pair. It accepts the recorded qualified pair baselines as complete identities,
including the Deflection member hash. It requires an empty
output directory, WitchyBND and DirectXTex `texconv` supplied as paths:

```powershell
.\src\textures\tutorial\build.ps1 `
  -OutputDirectory .codex-temp\deflection-tutorial-build `
  -WitchyBnd 'Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe' `
  -Texconv 'C:\Windows\System32\texconv.exe'
```

The script produces a candidate only. Before accepting its paired archives,
reopen the candidate and compare every member's name, ID, flags and payload hash
against the baseline. Only the two named tutorial payloads may change; inside
their TPFs, the texture metadata and DDS headers stay unchanged while the BC7
blocks change. An unchanged rebuild may have no differences. Inspect the decoded
544x336 artwork. This does not establish the in-game appearance.

On 2026-09-25, an unchanged round trip of the original 3,079-member archive was
byte-identical. The edited candidate preserved every other member's payload and
metadata, as well as all tutorial TPF metadata and DDS header bytes. Its accepted
pair hashes are `4FD01F5ED33EC29BB7C37E51E34765467C7FF84FF09DDE390F1714B627ED4D22`
for `.tpfbhd` and `CE8EF7371ED16015FB309AE23C4A1B61194220EB3ABDA80CC54863F9751149CF`
for `.tpfbdt`. Rebuilding from that accepted pair produced both files byte-for-byte.
Game appearance remains untested.

The 2026-09-26 two-image candidate preserved archive/member metadata, all 3,077
other members, and both TPF metadata records and DDS headers. Readback BC7 blocks
matched the encoded source outputs. Mean absolute RGB channel error against the
source pixels was 0.461 for Deflection and 0.270 for Ultimate (0-255 scale).
PNG color-profile previews can differ from the raw DDS preview; the recipe keeps
the source pixel values and the game's existing BC7_UNORM interpretation.
Evidence: `.codex-temp/tutorial-artwork-verify-20260926/verification.json`.
The new pair hashes are `E4707D8DDA184947736961ACEEF4E339A298F6141792118E43A742E0D583A862`
(header) and `F864DFE0D10D134D1566132FC7DFB76FA11469C5C07BDF41AA4FC3183F2939CD`
(data). Rebuilding from this accepted pair reproduced both files byte-for-byte.
This is the version 1.3.6 texture update; gameplay appearance still needs
an in-game check after deployment.

The 2026-09-28 PNG inputs have SHA-256 hashes
`F7DFA4267D4AF2542634275103CCC75404E5EBDD4907DB97C41C639E4DCB5B5A`
(Deflection) and
`919D190C4256BEBC4D1D06CB65562857E61492355075D997E752AF5B90EFCB5C`
(Ultimate). The rebuilt pair has hashes
`835888BD7BE39FD84BF04770B9631B0A0F5B22EC2AADA48812633069CEAC791C`
(header) and
`0B140C323FA65FC079EB6B88006F444ECF7B35480BB959DB114E30990E4D1AFE`
(data). The independent comparison found exactly two changed members among 3,079:
`MENU_Tuto_00016` and `MENU_Tuto_00018`. All other member payloads, member IDs,
names, flags and archive metadata matched the baseline. Both TPF metadata records
and DDS headers were preserved; encoded BC7 blocks matched the source output.
Evidence is in `.codex-temp/tutorial-texture-verify-20260928/verification.json`.
Gameplay appearance remains untested.
