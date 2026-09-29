Hadeon entrance audio trial
==========================

The author authorized a reversible local trial using the first ten seconds of
`HEYYEYAAEYAAAEYAEYAA.mp3`, the existing ME3 profile and ordinary save. No separate
profile or save is created. This is experimental test content; gameplay acceptance
and public release remain pending.


Implementation
--------------

- A dedicated `sd/cs_c9998.bnk` holds one nonlooping clip and its Play/Stop voice
  events. Audio authoring sources live in `src/audio/hadeon/`.
- The guarded [parameter recipe](../../src/recipes/hadeon-audio-test/README.md)
  changes only NpcParam 25000011 `SoundAddBankId` from -1 to 9998. Hadeon's default
  model sound bank stays unchanged.
- Event 5750300 passes entranceAudio=1 to 5750302. Immediately after Hadeon is
  enabled, the host's living player hears Voice 999800001 attached to Hadeon
  18002354. Existing entrance timing, AI startup and combat workers are preserved.
- Event 5750304 passes zero on its recovery call. Ordinary retreat/reentry and
  fall teleports do not retrigger the clip. Reloading the map creates a fresh
  entrance opportunity; no persistent flags or dialogue/subtitle records are added.


Validation
----------

The [audio recipe](../../src/audio/hadeon/README.md) uses installed
Wwise 2023.1.10.8659 for 48 kHz mono PCM media and a native-format BKHD 135 bank.
The clip contains exactly 480,000 samples. All seven sound-bank objects and the
embedded media passed native readback; a separate rebuild produced the same
960,616-byte bank with SHA-256
`E45C706E2E484D5D4BD87D229E242B6B8AC115A8F3313065F9F41BC7B83AC5DB`.
The collision scan checked 602 banks, 227,226 HIRC objects and 22,332 embedded
media IDs without conflicts. No matching external WEM filename was found.
The sound inherits ordinary one-shot behavior, with no Loop override.

The native regulation readback preserved every other NPC field, all other tables,
member order and binder metadata. The unchanged event-source qualification passed
before editing. The changed build preserves all 78 event IDs/order and file
metadata; only 5750300's entrance argument and five instructions plus one parameter
binding in 5750302 differ. All other shipped event files remain equivalent.

Evidence is retained under `.codex-temp/hadeon-audio-regulation/` and
`.codex-temp/event-builds/1790470483469945400/`, including
`audio-validation.json`. Successful native validation does not prove ME3 loading,
the additional bank's residency, voice-bus behavior or audible playback.

Manual check: fully restart through the existing ME3 setup and enter Hadeon's room
while he is undefeated. Listen for one ten-second clip at his entrance spawn.
Check voice volume, normal Crucible Knight sounds, retreat/reentry and recovery
teleports. Repeat after death/reload; confirm completed-boss saves do not spawn him
or play the cue. Record results before treating this route as accepted.


Deployment
----------

Version 1.3.7 passed repository preparation checks (73 runtime candidates).
The prepared main package contains 74 files including the existing external DLL.
Against the prepared 1.3.5 main payload, only regulation and m18 EMEVD changed;
the sole added file is `mod/sd/cs_c9998.bnk`. All other files, including the external
DLL, are unchanged. The previous 47 attack-row changes remain present.

The deployment was initially queued while Vortex was closed. The subsequent
diagnostic pass resumed the same receipt and confirmed completed deployment to
profile `SkC-QjDMc`. Live regulation, m18 EMEVD and bank hashes match 1.3.7.
The existing profile/save setup is unchanged. Preparation receipt:
`.vdb/prepared/7903775dc45c4a4a852035111182c0d4/receipt.json`.
Finalization receipt:
`.vdb/finalizations/9fe43b4fb1064a229237adb6b75668e4/receipt.json`.
Request `4f47bd09-28bb-4841-a993-0dce31b72b70`, main build
`a5c7d8b7362708315ae47080`, profile scope all (preserving enabled/disabled/absent
states). The existing 1.3.6 texture request remains separate and unchanged.

The existing receipt can refresh verification without submitting another request:

```powershell
python tools/finish_workflow.py resume --receipt .vdb/finalizations/9fe43b4fb1064a229237adb6b75668e4/receipt.json
```


First playback attempt
----------------------

The author reported no audible clip on an existing save and confirmed Hadeon
appeared with his full entrance effects. No new game is required
by the event logic: an undefeated Hadeon's initial entrance after map load passes
the audio argument; ordinary retreat and recovery callers deliberately do not.

The ME3 `transient-profile/2026-09-26_18-35-19.log` identifies ME3 0.13.0 and
Elden Ring 1.17.1.0, loading the existing `Game/mod` path without a save override.
It reports the Wwise hook at line 39, modified regulation and m18 event reads, and
twelve redirects to `sd/cs_c9998.bnk` at lines 468-471, 506-509 and 538-541.
There are no WARN or ERROR entries. This proves the bank was requested and
redirected; it does not prove Wwise parsed it successfully or that PlaySE fired.
The log has no per-event playback or Wwise decoder diagnostics.

Deployment and additional-bank discovery are verified. Audible playback remains
failed in this attempt, with the precise cause still under investigation.


Loudness diagnostic, 1.3.8
--------------------------

The author requested a maximum-volume test to rule out inaudibility. The trial
mixer now adds 3.5 dB, with distance attenuation and spatialization disabled.
The source peak is -3.985 dBFS; the expected peak before voice-bus processing is
-0.485 dBFS, avoiding deliberate sample clipping. Game Voice and Master volume
settings remain effective. No global bank or user settings are changed.

Native readback confirms exactly those mixer changes. BKHD, DIDX and DATA chunks
are byte-identical to 1.3.7; the entrance event, emitter, timing, regulation and
WEM encoding remain unchanged. This tests audibility, not the separate possible
spawn-frame emitter or codec issues. Audible playback remains pending.

The 960,620-byte bank SHA-256 is
`3A3359A847E4B9AC638AA9586BFDF1289F43342DE0C107FC50E31224770F17CA`.
Validation: `.codex-temp/hadeon-audio-build/volume-138/validation.json`.
Pre-change files: `.sovereign/backups/hadeon-audio-volume-138/`.

Deployment completed and the live bank hash matches. The prepared 74-file main
package differs from 1.3.7 only at `mod/sd/cs_c9998.bnk`. Preparation receipt:
`.vdb/prepared/048001bb66154047bb6d4516c4220d37/receipt.json`; finalization receipt:
`.vdb/finalizations/dff678ae7ccd4d8982ac71de512f3cc5/receipt.json`.
Request `94ede8ba-c1ff-45c4-bf13-c8dd48dbaebb`, build
`bc0a37040b8343ff3f6fd73e`. Repository preparation, native readback, package
preservation and live-byte verification passed. User playback confirmation is
still required after a full game restart and a fresh Hadeon entrance sequence.


Tutorial review and ordering correction, 1.3.9
----------------------------------------------

The author heard no clip in 1.3.8 either. The ME3 log
`transient-profile/2026-09-26_19-02-27.log` again shows twelve bank redirects and
no WARN/ERROR entries; the live bank matched the louder diagnostic.

The review found a concrete HIRC ordering defect. Our ActorMixer preceded its
Sound child. All 242 comparable native c2500 links and 3,762 native vcmain links
place children before parents. [Themyys' soundbank tutorial](https://docs.google.com/document/d/1lNov-a0DwnMY2yZywH3hFYzuoDfndofguvZmAnLDo-U/edit)
explicitly requires the Sound/container block above its ActorMixer. [Yonder's
solver and validator](https://github.com/ndahn/yonder/blob/main/yonder/types/soundbank.py)
sort children before parents and report a node defined after its parent as an
error. A rewwise roundtrip preserves invalid ordering, so our earlier validation
missed this requirement.

Version 1.3.9 orders attenuation, Sound, ActorMixer, actions, then events. All
seven raw object payloads are unchanged, as are BKHD/DIDX/DATA, the WEM, gain,
regulation and entrance event. The builder now checks dependency order, and a
negative check confirmed that it rejects the previous source. Bank SHA-256:
`DC93111693746D2667FF1BC789AE523CACD6B3C514286662520BFA817C9EFEB0`.
Evidence: `.codex-temp/hadeon-audio-build/order-139/validation.json`.
Backups: `.sovereign/backups/hadeon-audio-order-139/`.

Version 1.3.9 deployed and verified on the existing `SkC-QjDMc` profile; live
bank bytes match the candidate. The 74-file package differs from 1.3.8 only in
that bank. Prepared receipt:
`.vdb/prepared/c14994973620489d9a066c7dd9602f41/receipt.json`; finalization receipt:
`.vdb/finalizations/ced07f77669642f8b4448ab334d7f51b/receipt.json`.
Request `db8cb693-0ecb-4ed9-a869-aa26b4415dae`, build
`362c14508d171ac2384869e3`. No new profile or save was created.

This is a confirmed tutorial/validator violation and a plausible cause of the
silence; runtime causality remains unverified until the corrected bank is tested.
No RandomSequenceContainer is inherently required: native vcmain includes 258
direct Play-action-to-Sound links. The dedicated character-bank loader and PlaySE
route follow [Yonder's guidance](https://raw.githubusercontent.com/ndahn/yonder/main/docs/guides/adding_sounds.md).

PCM remains a separate qualification gap. [Yonder's conversion helper](https://github.com/ndahn/yonder/blob/main/yonder/wem.py)
defaults to Vorbis and its metadata reader expects format 0xFFFF; our WEM uses
PCM 0xFFFE. This does not prove PCM is unsupported. Keep it unchanged for the
ordering-only test; if that still fails, use a separately qualified native-like
Vorbis trial and instrument the event rather than continuing volume changes.


Author playback confirmation, 1.3.9
----------------------------------

On 2026-09-26, asked specifically whether the last sound-bank fix (1.3.9)
produced audible sound in game, the author answered: "Yes, I heard it."
This confirms audible playback through the corrected bank and its existing PCM
media. The earlier silent 1.3.7 and 1.3.8 results remain historical failures.
It does not establish subtitle support, final voice mixing, exact onset latency,
or every retreat/death/reload scenario.

The next requested scope is the [first entrance monologue](../hadeon-lore.md#first-entrance-dialogue),
using the supplied voice recording and a 16.4-second combat/music cue. That
behavior is not implemented by the 1.3.9 test.


Recovery
--------

Pre-test repository files and the selected-build record are preserved with hashes
under `.sovereign/backups/hadeon-audio-test-20260926/`. Guarded editor handoffs retain
their own destination backups: params `8faa4bd02def4f919f240eb7f34bc451` and events
`96171d7f1fcc40eeb3e1ec685f500bf4` under `.sovereign/handoffs/`.

Rollback must restore the matching parameter/event pair and remove the trial bank
from the replacement payload, preserving later work. Use the retained pre-test
main build through VDB when available; never overwrite a reserved stage or reuse
a version for changed contents. The ordinary save is not part of file rollback.
