Chapel and omen correction, 1.1.1
================================

Author-approved 2026-09-24 after the 1.1.0 screenshots showed the Chapel door
still demanding a finger. The door is now configured to open without collecting
either item. The maiden's ground message is removed, the existing shard caption
uses the author's exact wording, and opening eclipses include the player VFX.
Native checks passed; in-game acceptance remains pending.


Door, message and vanilla flags
------------------------------

The active restriction was ObjActParam 219002: qualification type 1 requires
Goods 106 and failure message 4072. New row 2190020 copies its animation,
alignment, action button and timing, changing only qualification type to 0,
both old/new item IDs to 0 and failure message to -1. Only the Chapel ObjAct
10013540 selects this new row. Its opened flag 10018540 remains unchanged.
All original ObjAct rows remain byte-for-byte equivalent after decoding.

The previous investigation found event 10012504 waiting on pickup flag 60210,
but missed that it is dormant: no initializer references it in the 598 inspected
runtime and installed-game event files. No Chapel event override is introduced.
There are no new flag allocations and no changed flag writes. Vanilla pickup
60210, new-game grants, arrival flags, shop stock and later progression remain
unchanged. In particular, the door fix does not mark the shard collected.

The new m10_01_00_00 map override removes only Message region 7130 and changes
that one door ObjAct row reference. All remaining objects, regions, shapes and
references pass native preservation comparison. The source map is the qualified
installed-game extraction used for the prior flag audit, SHA-256
0805b6bf88a4ad2bd6201345c0a5586469eb53473cdd6360a5ab931d777ae5ab.


Player presentation and shard text
---------------------------------

Common events 5750360 and 5750362 now apply omen-owned effect 1627111
(7505942, 3 seconds) and new effect 1627115 (7505947, 2.5 seconds) at each cue's
start. The latter clones existing 1626990 with bonfire clearing enabled. Existing
effects 1627110/1627113 still control the 10-second/3-second eclipse. Both player
effects are cleared on the existing completion/interruption paths. Real eclipse
effects, state, rewards and controls are unchanged. The screech call sequence is
unchanged; VFX 7505942 retains its authored associated sound 523911.

Oath event 5750103 always applies its existing short 1626986 presentation when
it flashes the eclipse, including when its icon effect already exists. The
ordinary eclipse and shorter blessing/reward variants retain their behavior.

Only GoodsCaption.fmg entry 1291 changes in item_dlc02.msgbnd.dcx:

> A fleeting fragment of crimson starlight, still warm with an unsettling heat.
>
> Temporarily increases healing effectiveness.
>
> Within its faint glow stirs a hunger that never fades.

The item name, icon, effects, acquisition and Nexus description are unchanged.


Evidence and acceptance
-----------------------

Temporary backups, native candidate checks, decoded event review and deployment
receipts are retained under `.codex-temp/chapel-polish-20260924`. The event review
permits only three changed events: VFX operations and two corresponding branch
length adjustments. All flag instructions and unrelated event metadata match.
The binary text workflow verifies the complete binder against the single-entry
patch. Existing parameter rows and unrelated tables are preserved.

[ER-080 through ER-082](../TEST-MATRIX.md) cover the door without looting, later
pickup, reload, return visits, NG+, VFX cleanup/coexistence and the exact caption.
These remain Pending; byte checks do not establish gameplay behavior.
