Nemesis opening omens
======================

Version 1.1.4 supersedes the crystal timing below: its cue now lasts five seconds,
then the room braziers dim to off. The exterior cue remains ten seconds. See
[the lighting update](HADEON-LIGHTING-UPDATE.md).

The [1.1.1 presentation update](CHAPEL-POLISH-UPDATE.md) adds both player VFX
components to every opening omen and ensures oath-entry always has its short VFX.

The 1.0.9 [opening update](BEGINNER-OPENING-UPDATE.md) adds the 45-second
beginner rescue, grants Hadeon Thorn Ward at both 75% and 50%, separates the left
imp flag from vanilla, softens the key knight, adds the initial Chapel omen and
suppresses the exit omen after crystal destruction. Gameplay acceptance is pending.

Author-approved 2026-09-23 for local build 1.0.8. Hadeon's defeat represents
Nemesis escaping into the Lands Between; breaking the crystal remains the
separate, optional persistent hardcore choice. Both moments use existing Nemesis
audio and visuals, without a text line, banner, camera lock or player-control lock.
Implemented with native preservation checks; gameplay acceptance remains pending.


Torch progression
------------------

Each imp statue still consumes one Stonesword Key and opens only its barrier layer.
Its torch is normal before activation and red afterward, until Hadeon is defeated.
Defeat flag 1055420915 takes priority and restores both normal torches even if a
statue is activated later. Event 5750351 restores this priority on rest/reload.
Hadeon's entrance pair retains its red-before-victory, normal-after-victory behavior.
The original normal offsets (-1 at the statues, 10 at the entrance) are preserved.
See [the object and reward IDs](GRAVEYARD-KEY-GATES.md).


First outdoor reveal
---------------------

The stock exterior map m60_42_36_00 owns lifting door AEG110_064_1000, entity
1042361540. Its ObjAct 1042363540 sets flag 1042368540. Existing common event 702
and tutorial event 18000021 already use that flag for the initial time/weather
handoff. The new map override preserves every existing map object and adds only
Other region 1042362990, named SACRED - First Limgrave Nemesis Omen.

The box is 16 metres wide, 16 deep and 8 high, oriented with the door. Its centre
is 8.5 metres along the door's positive local Z, toward the stock exterior spawn
and hint regions; its bottom is three metres below the door. Its position is
approximately (-7.498, 90.956, -78.517), yaw -27.887. Placement and timing need an
in-game walk-through, including a fast exit and approaching from outdoors.

Host-only common event 5750360 waits for Hadeon defeat, the door flag, the player's
presence in this box in the exterior map, and an unused reveal receipt. It allows
two seconds for the vista before applying the ten-second omen and setting saved
journey flag 1055420923. Leaving the small box during that delay is allowed;
death or leaving the exterior map cancels before consuming the receipt.
Return visits/rest/reloads do not replay a completed reveal. NG+ reset is intended
and remains a game-test requirement. An old save with Hadeon/door flags already
set can receive its first omen on entering the region; no migration is added.


Crystal surge and effect ownership
----------------------------------

The existing host crystal-destruction event 5750291 requests presentation through
temporary flag 1055422944 immediately before setting persistent hardcore unlock
1055420918. Already-broken crystals do not request it again on reload. The same
common worker consumes the request, checks a living host in the shrine map, and
adds a three-second opening flare to the ten-second eclipse. One worker serializes
both cues; a request received during the exterior delay takes priority.

Both cues reuse the Hadeon Nemesis shriek sequence: SoundType.SFX 530181, followed
after 0.1 seconds by the existing paired 450264 sound. No new sound assets are
introduced. The crystal flare also retains its existing VFX-associated sound.
Startup event 5750100 skips only its duplicate presentation while the dedicated
omen is pending/active; its role and hardcore flag writes are unchanged.

SpEffectParam 1627110 clones 1626999 with duration 10 seconds, hpRecoverRate restored
to 1, and bonfire recovery clearing enabled. It reuses SpEffectVfxParam/FXR 7505940.
SpEffectParam 1627111 clones 1626982 for the three-second crystal flare, removes
the duplicate eclipse VFX slot, and enables bonfire clearing. Both are ordinary
death-cleared effects with no new gameplay penalty. Their expiration uses the
existing particles' authored appearance/disappearance; exact fade shape is not
claimed from compilation alone.

The worker clears only these two new effects on completion, death, rest/reload or
departure from both relevant maps. It does not clear or toggle the real eclipse
flag, hardcore/follower roles, real eclipse effects, rewards, music or travel locks.
The ordinary periodic eclipse and persistent crystal consequences remain intact.
Coexistence with a live eclipse and visual/audio timing require in-game acceptance.


Verification and recovery
-------------------------

Before-copies and hashes are retained in .codex-temp/nemesis-omens-20260923/before
and before.json, alongside isolated native candidates and their receipts. The
exterior baseline is from the existing installed-game extraction for Steam build
25080141; its qualified map hash is recorded in native-receipt.json.

Native read/write validation preserves all existing map fields and parameter rows;
only the new region and two effects are added. All other regulation tables retain
their exact bytes. The new flag allocations were checked against regulation and
598 installed/mod event files, including literal flag ranges. Decoded event review
permits only common constructor/startup plus new worker 5750360, and shrine
constructor/torch worker/crystal request. All other events and file metadata match.

ER-070 through ER-072 in [the test matrix](../TEST-MATRIX.md) track outstanding game
tests. Editor sync and VDB receipts are separate evidence of saved/deployed bytes,
not a gameplay pass. No Nexus publication is part of this local build.

Saved editor handoffs completed: events 1c05c3f2f53d47d8b3f0f13a8fa53598,
parameters ca2114cf1f4148659b7189d9700180e8, and maps
7f43b67ee7ef4c96aaeafbed9517afa3 under .sovereign/handoffs. Reload open editor
buffers before saving. Event qualification 1790209390927184900 matches saved
sources and binaries; the first candidate build was 1790209203538484700.

Full main package 1.0.8 is prepared under
.vdb/prepared/b4c56014ecba47c8b69c321a7bc55c16/receipt.json. Its eleven differences
from the selected stage include the earlier gate work, wall-jump and Rick-critical
HKS fixes, and Deflection FMG text that the older selected stage lacked. Existing
deployment bytes for changed paths are also retained under the scratch directory's
before-deployment folder. No new HKS or text changes were authored in this update.

Staging and all-profile finalization were requested through protocol 3, request
6c7fb90f-c6ec-48a1-b59d-a582e7b0943a, expected build 1c7fd9f9dec2c3f3770c6e43.
The durable receipt is .vdb/finalizations/nemesis-omens-1.0.8/receipt.json.
At this handoff Vortex was closed, bridge status unavailable/stale, and the request
was Pending: no completed stage or live deployment is claimed. Vortex processes
the existing queue on its next launch; refresh this receipt and select the verified
stage after completion, without resubmitting. Disabled/absent profile states are
preserved by the bridge. The previously selected stage remains selected meanwhile.
