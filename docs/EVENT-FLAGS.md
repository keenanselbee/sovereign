Sovereign event flag reference
=============================

Reviewed 2026-09-20 against thefifthmatt's
[Elden Ring ID allocation guide](https://docs.google.com/spreadsheets/d/17sE1a1h87BhpiUwKUyJ9ZjKTeehXA4OuLwmQvTfwo_M/edit?gid=1770617590#gid=1770617590)
and Sovereign's current sources. This is an allocation reference and corrective
plan, not evidence of completed gameplay tests. The subsequent correction is now
implemented in [the implementation record](ONBOARDING-FLAG-FIX-PLAN.md); the initial
inspection tables below retain the before-change evidence.


Base ownership and valid ranges
-------------------------------

Hadeon 1.2.5 reserves temporary flag 1055425042 for sustained player-death
confirmation, written only by map event 5750402 after 0.5s of zero HP and outside
beginner rescue protection. Recovery clears it. Lighting ignition now owns
1055425100-1055425195 (1.2.8); the former 42 gates are retired. Native parameters and pre-change event sources contain no
allocation conflict. See [the reset update](HADEON-RESET-1.2.5.md).

Room lighting 1.2.8 uses temporary gates 1055425100-1055425195 for 96 individual
positions; native mod/vanilla event and parameter checks found no collision.
Former 1.2.4 gates 1055425000-1055425041 are retired; 1055422996 marks completion and 1055422997 activity. Initialization and
death clear them. Former gates 1055423000-1055423041 were invalid and are no longer
referenced. Earlier gates 1055422970-1055422995 and gaze/chance bits
1055422960-1055422967 are retired and have no event readers/writers.
1055422950-1055422953 still select 25/50/75/100% brightness. Crystal presentation
flag 1055422945 and saved victory/crystal flags retain their existing roles.
Native allocation checks cover current parameters plus mod and retained vanilla
event instructions/ranges. See [the lighting update](HADEON-LIGHTING-UPDATE.md).

Rick awakening flag 1055420926 is retired by the visible-transition follow-up.
It is no longer read or written; do not reuse it for another purpose. Every
attempt starts with Soldier of Godrick. Vanilla defeat 18000850 still persists;
temporary presentation flags 18002851/18002852 reset on each attempt and abort.
See [Rick implementation](RICK-ENCOUNTER-UPDATE.md).

Ultimate tutorial uses saved receipt 1055420927, TutorialParam 5750 and event
5750363, moved from common to the Graveyard map in 1.3.2. Jump to Evade adds saved
receipt 1055420928, TutorialParam 5751 and map event/text 5750364. Native regulation
members and 598 mod/retained-vanilla event files were checked for exact references
and flag ranges before allocation. Neither receipt controls vanilla progression.
See [the lesson order](GROUND-STOMP-GOAL.md).

Chapel reward (1.1.0): shop stock reserves 1055424580-1055424589, starting at
1055424580, for Kale's single Wizened Finger. This follows the existing spaced
stock-counter convention. Pickup collection/door flag 60210 remains on lot
10010000 after its reward changes to Goods 1291; it never controls the shop.

Opening update (1.0.9): 1055420924 owns the left imp activation; 1055420925
records the first Chapel omen. Both are saved journey flags. Vanilla 18000570 is
left untouched and no longer drives any Sovereign statue, seal or torch. The
original 45-second rescue cooldown was an event timer. In 1.2.4, non-extendable
15/30-second SpEffects replace that timer; no saved cooldown flag is used. See
[the opening update](BEGINNER-OPENING-UPDATE.md).

Nemesis omens (1.0.8): saved journey bit 1055420923 records that the outdoor reveal
started. Temporary bit 1055422944 requests the crystal-break presentation and is
consumed by common event 5750360; already-broken crystals do not re-request it.
These flags never control actual hardcore or periodic eclipse state. Existing
1055420915 overrides both imp torches after Hadeon defeat. See [the omen
record](NEMESIS-OMENS.md), including native allocation checks and pending NG+ tests.

Graveyard gates (2026-09-23): 1055420920 owns the right statue activation;
1055420921 and 1055420922 are knight/Rick key collection receipts. These are
one-bit saved journey flags. Prompt flags 1055422940-1055422943 are four separate
temporary bits, cleared before each prompt. The left statue used 18000570 until 1.0.9;
Hadeon's guide torch reads existing defeat 1055420915. See
[the gate record](GRAVEYARD-KEY-GATES.md). NG+ reset remains a game-test requirement.

Tutorial update (1.0.7): `1055420990` is reserved as the disabled vanilla-tutorial
display gate. It must remain OFF; no event enables it. All TutorialParam rows except
1180 require it. The Deflection lesson retains vanilla flags `710180` (shown/display
permission) and `69060` (tutorial note awarded). See [TUTORIAL-UPDATE](TUTORIAL-UPDATE.md).

The sheet's
[base flag registry](https://docs.google.com/spreadsheets/d/17sE1a1h87BhpiUwKUyJ9ZjKTeehXA4OuLwmQvTfwo_M/edit?gid=1464882376#gid=1464882376)
lists `1055420000` at AG47 and **Sovereign** at AG48. Keep this existing base.
Flags in this namespace may be used across maps; their prefix does not restrict
them to one event file. Registry ownership avoids coordinated allocation conflicts,
but does not prove compatibility with every other mod or future game update.

The fourth digit from the right determines the following behavior within this
base. These rules do not classify unrelated item, message, entity, or event IDs.

| Sovereign flag range | Classification in the guide |
| --- | --- |
| `1055420000`-`1055420999` | Saved across area reloads |
| `1055421000`-`1055421999` | Invalid as flags |
| `1055422000`-`1055422999` | Temporary; reset on area reload |
| `1055423000`-`1055423999` | Invalid as flags |
| `1055424000`-`1055424999` | Saved across area reloads |
| `1055425000`-`1055425999` | Temporary; reset on area reload |
| `1055426000`-`1055426999` | Invalid as flags |
| `1055427000`-`1055429999` | Saved across area reloads |

Here, reload includes death, fast travel, and save/quit. Saved does not mean
permanent across NG+. The guide separately identifies flags such as `6xxxx`
as surviving NG+ and points to
[eventparam](https://soulsmods.github.io/elden-ring-eventparam/).
That five-digit range is not the invalid `1055426xxx` block.

The guide recommends multiples of ten for shop stock flags. For new Sovereign
allocations, reserve ten bits per stock base as a conservative spacing convention.
This is not a claim that every one-copy shop actually writes ten bits: Smithbox's
Shop Event Flag glossary describes quantity one as on/off. Other multi-bit counters
own every bit they occupy; checking only the starting ID misses overlaps.

Event IDs need not be valid flags unless their state is read or written as a flag,
including through `ThisEventSlot()`. Do not renumber ordinary events merely because
their IDs are outside this base. Message `1055421000`, used by
`DisplayBlinkingMessage`, is not an invalid flag use.


Initial Sovereign findings
--------------------------

| Current allocation | Assessment |
| --- | --- |
| Nemesis roles `1055420000`-`1055420003`, eclipse `1055420010` | Valid saved flags; scripts still determine when roles are cleared or recalculated |
| Spell and tome knowledge `1055420200`-`1055420260` | Valid saved block; NG+ knowledge must be deliberately retained or restored |
| Armor recovery `1055420600`-`1055420664`, Hewg `1055420700`-`1055420702` | Valid saved block, including the armor counters' occupied bits |
| Hadeon defeat/reward/crystal `1055420915`, `1055420916`, `1055420918` | Valid saved flags; fresh-journey reset remains a gameplay acceptance check |
| Nemesis temporary state in `1055422xxx`, Hadeon milestones `1055422930`-`1055422933` | Valid temporary block, appropriate for transient encounter state; explicit retry cleanup still matters |
| Tome collection `1055421200`-`1055421207` | Invalid flag block; correction required |
| Tome shop visibility `1055421300`-`1055421307` | Invalid flag block; correction required |
| Gyre hat ownership `1055421400` | Invalid flag block; correction required |
| Tome shop stock bases `1055421500`-`1055421570`, step ten | Correct spacing, but invalid flag block; correction required |

The tome allocations are authored in [the manifest](../src/tomes/profane-tomes.json)
and consumed by [the generator](../tools/profane_tomes.py) and
[common events](../src/events/common.emevd.dcx.js). The previous checks established
unused numbers, serialization, and simulated logic, but did not validate the game's
flag address rules. Their passing results do not establish that these flags work.
Duplicate suppression, shop availability/stock, and hat ownership must not be
considered accepted until the IDs are corrected and tested in game.

Minimal proposed replacement, not yet implemented:

| Purpose | Proposed allocation |
| --- | --- |
| Collection | `1055424200`-`1055424207` |
| Shop visibility | `1055424300`-`1055424307` |
| Hat ownership | `1055424400` |
| Stock counters | Bases `1055424500`-`1055424570`, step ten; reserve through `1055424579` |

These preserve the existing layout in a valid saved block. No matching `4xxx`
references were found in the inspected `src/` and `tools/` text. The follow-up
inspection below found no candidate-range values in runtime parameters or literal
integer matches in shipped maps/dialogue. Regenerate events and patch parameter
outputs together, add a flag-validity check to the existing manifest checks and
generator entry points, and use the normal qualified editor handoff.
The mod targets fresh saves, so no compatibility aliases for the invalid IDs are
needed. Inventory-based NG+ restoration remains useful with the corrected flags.


NG+ and future allocations
--------------------------

For once-per-character vanilla-save onboarding, an arbitrary unused `1055420xxx`
or `1055424xxx` flag is insufficient evidence of NG+ persistence. No permanent
onboarding marker was established by the initial review. The subsequent installed
archive review below recommends `69990` for implementation, with actual journey
retention still an acceptance test. Do not borrow a seemingly unused `6xxxx` value solely
because it lies in a permanent range; vanilla uses that range for real progression.

The existing tome design instead restores knowledge from retained, non-discardable
books. This separates retained knowledge from journey flags without assuming that
the latter survive NG+. The shrine's intended fresh Hadeon/crystal choice is a
different lifetime requirement. Keep the two policies distinct.

For each new allocation, record purpose, owner, full bit span, and intended lifetime.
Check engine validity, local collisions, and external registry ownership separately.
Use explicit flags when completion state matters. Validate reload and NG+ behavior
in game where relevant; native compilation and source simulations cannot establish
those engine guarantees.


Follow-up inspection and minimal fix scope
------------------------------------------

On 2026-09-20, a read-only native scan covered all 194 regulation tables without
parse failures. It also searched the decompressed payloads of both shipped maps
and every member of the five shipped dialogue binders for little-endian integer
values in `1055424000`-`1055424999`. None were found. Source searches also found no
uses in that block. This does not cover all vanilla assets loaded from the game
archives or resolve arbitrary computed flag expressions.

The regulation SHA-256 was
`669e846c353eb20f76e69ceb7967caefcf9b0b59d030df161691143590034b95`.
Scratch evidence and the read-only scanner are in
`.codex-temp/flag-allocation-review/`. Recheck current inputs before implementation.

The tome correction needs only:

- Change 25 manifest addresses, including two reserved stock bases with no shops.
- Regenerate the marked common-event controller. An in-memory trial produced only
  the expected flag substitutions and left surrounding source unchanged.
- Patch 16 fields across ten existing parameter rows: six shops, two map pickups,
  the Fire Monk book drop, and the hat drop. Goods, text, locations, and prices stay
  unchanged. The original full creation plan cannot simply be rerun against the
  installed tome rows, because it correctly rejects existing clone destinations.
- Validate the base, saved-block membership, distinct flag spans, and stock spacing
  before generation. Test rejection of the old `1xxx` allocations and a temporary
  block accidentally used for saved collection state. Preserve the existing
  ownership, discovery-order, and NG+ restoration tests.
- Compile and compare the event candidate, verify the exact parameter delta, then
  check shop visibility, alternate-source suppression, reload, and NG+ in game.

No custom `575...` event body in the inspected event sources uses `ThisEventSlot`.
There is no reason from this finding to renumber those events or the `1055421xxx`
message IDs. The older spell-shop stock IDs ending `0205`, `0215`, and `0221` do not
follow the recommended spacing, but all inspected custom spell shops sell one copy.
Given the glossary's one-bit description, a destructive overlap is not established.
Do not broaden the tome fix into a speculative spell-shop renumbering.

In the initial inspection, `69990` was an onboarding-marker candidate only. It was absent from the source
search, decoded regulation values, and the literal map/dialogue scan above. The
linked eventparam index does not assign it, but that index's latest commit is
`4d20990cab8d3090bc2f1fbb6755079c10f576ee` (2024-04-13), before the DLC. Its FN,
UT, and PC columns describe ranges, usage, and logging, not NG+ reset policy.
That initial inspection did not establish current vanilla/DLC consumers. The deeper
archive review below addresses this gap. Actual NG+ retention remains untested.

Once a permanent marker is qualified, the simple onboarding shape remains a
host-only entry guard, the existing sequential exchanges, and a completion flag
written after the last branch, including when no compensation is needed. Keep the
six-second waits. Keep the separately identified Placidusax stock/guard mismatch
and Florissax/Senessax duplicate-compensation decision in the onboarding change;
neither requires redesigning the tome controller.


Installed archive review and implementation recommendation
----------------------------------------------------------

The deeper 2026-09-20 review used the existing selective archive reader against
the installed game's encrypted archives, identified by Steam build `25080141`.
It extracted 589 events, 36 dialogue binders, and 1,347 maps. The UXM dictionary
also names three absent entries: `common_macro.emevd.dcx`,
`m60_42_40_10.msb.dcx`, and `m60_47_42_10.msb.dcx`. These were reported as missing,
not silently treated as inspected. The dictionary is the enumeration boundary;
this is not an assertion about unidentified archive members or executable code.

The scan covered those assets, all 194 installed regulation tables, and the
Sovereign overrides. No flag use of `69990`, `1055420800`-`1055420803`, or the
proposed `1055424xxx` block was found. Seven raw map byte matches were false
positives: decoding their maps produced no corresponding integer values.
Literal batch/range flag instructions in all 598 vanilla and mod event files also
showed no range covering the proposed allocations. Arbitrary computed expressions
and executable hardcoded references are not proven absent by these checks.

Installed regulation SHA-256:
`766521f9508de3a3532df61c45a1c2d93340f1ff7ed8306ab20df761712ca2ab`.
The archive receipt records header fingerprints, data-file sizes/timestamps, and
individual extracted hashes. Evidence remains under
`.codex-temp/flag-allocation-review/`, especially `current/extraction-receipt.json`,
`vanilla-final-findings.json`, `repo-final-findings.json`, and
`map-candidate-check.txt`.

The allocation guide and the author's
[EMEVD tutorial](https://soulsmodding.wikidot.com/tutorial:intro-to-elden-ring-emevd)
both identify the five-digit `6xxxx` range as surviving NG+. Combined with the
installed-data collision review, this supports **implementing with `69990`** as
the once-per-character onboarding marker. It does not establish an observed NG+
test or compatibility with arbitrary other mods.

The concrete proposed changes, including compensation receipts and the existing
spell-shop mismatch, are in [the implementation plan](ONBOARDING-FLAG-FIX-PLAN.md).
The investigation itself made no runtime changes. The subsequently authorized
implementation has now applied these allocations; see the linked record.
