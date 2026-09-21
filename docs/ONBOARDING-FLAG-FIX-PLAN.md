Flag and vanilla-save onboarding correction plan
================================================

Implemented 2026-09-20 following the [flag investigation](EVENT-FLAGS.md).
Native candidates and source behavior tests pass; gameplay acceptance remains
pending. The sections below record the approved change scope. Support existing vanilla characters and fresh characters;
do not add compatibility handling for earlier unreleased Sovereign builds.


Tome correction
----------------

Move the manifest's invalid `1055421xxx` addresses to the matching `1055424xxx`
addresses: collection `4200`-`4207`, visibility `4300`-`4307`, hat `4400`, and stock
bases `4500`-`4570` in steps of ten, all prefixed by `105542`.

Regenerate only the marked common-event controller and patch the 16 affected
parameter fields in ten existing rows. Do not rerun the initial create-all-rows
plan against existing rows. Preserve books, captions, prices, distribution, order
assignment, and inventory-based NG+ restoration. Add small validity/overlap checks
to the existing generator and manifest tests; no new allocation framework is needed.


One-time onboarding
--------------------

Use `69990` for onboarding completion. The installed-data review found no use;
the documented `6xxxx` lifetime supplies the NG+ rationale. This is sufficiently
supported to implement, with actual NG+ retention verified during acceptance.

Event `5750009` should exit for non-host players and completed characters. Keep
the existing sequential exchanges and six-second waits. Set `69990` only after
all onboarding branches finish, even if the character needed no compensation.
Fresh characters therefore complete onboarding too, and do not have legitimately
learned spells stripped when journey-scoped shop flags reset in NG+.

Move removal of vanilla Ancient Dragon Prayerbook `8865` and clearing of its
Corhyn/Miriel teaching flags out of the two spell-ownership branches. This handles
a carried or previously delivered prayerbook even if neither spell was bought.
Retain the deliberate Spear/Strike removals and the existing spell-exchange
amounts. Preserve Perfect Runeseal recovery; the normal modded Goldmask dialogue
already awards lot `6900`, so it need not depend on ongoing onboarding execution.

Change Placidusax shop row `102359` stock flag from `290171` to `1055420235`, matching
the existing cleanup guard. Leave other one-copy spell-shop IDs unchanged: their
unusual spacing is not evidence of an actual multi-bit collision.


Dragon compensation without duplicate awards
---------------------------------------------

Use one dedicated receipt per dragon's onboarding compensation. These are valid
saved journey flags in Sovereign's registered block; `69990` prevents the whole
process from recurring in later journeys. They also prevent repeated compensation
if a reload occurs after one exchange but during a later six-second wait.

| Compensation | Receipt | Existing exchange | Catch-up without that spell |
| --- | --- | --- | --- |
| Fortissax | `1055420800` | Remembrance plus one Ancient Dragon Heart | One heart |
| Placidusax | `1055420801` | Remembrance plus three Ancient Dragon Hearts | Three hearts |
| Lansseax | `1055420802` | One heart | One heart |
| Florissax/Senessax | `1055420803` | One heart for removed Florissax spell | One heart for previously rewarded Senessax |

Within each receipt guard, handle an eligible held vanilla spell first; otherwise
consider the missed boss reward. Require both boss defeat and the normal reward's
collected flag for catch-up. If its normal reward is still pending, leave that
delivery to the existing boss-reward event. Do not infer a missing reward simply
from the player's current heart count, because hearts may have been spent.

Relevant current-journey conditions are Fortissax `9111` / `510110`, Placidusax
`9115` / `510150`, Lansseax `1041520800` / `530300`, and Senessax
`2054390850` / `530805` (defeat / reward collected).

Minimal parameter changes for the receipts:

- Give refund rows `10116` and `10117` receipt `1055420800`, and rows `10156` and
  `10157` receipt `1055420801`. Stop clearing normal reward flags `510110` and
  `510150` in onboarding. Award the existing two-row refund group for an exchanged
  spell; its heart-only trailing row can supply catch-up. Verify that direct
  trailing-row award in the native/game acceptance checks.
- Add one-heart map lots `30880` and `30890`, cloned from `30870`, with receipts
  `1055420802` and `1055420803`. Both row IDs are absent from the inspected current
  mod and vanilla parameters. Recheck neighboring lot IDs before acceptance so
  these remain separate award groups.
- Use each receipt consistently in its event guard and compensation lot. Let item
  awards record receipts for owed compensation; do not mark an owed grant complete
  before awarding it or clear its receipt on reload.
  Normal boss reward lots and their flags remain unchanged.

At entry, before any six-second wait, the event settles receipts for bosses with
nothing owed: an existing mod purchase, or no held spell and no previously
collected boss reward. This includes pending normal rewards and live bosses.
Otherwise a pending normal reward could arrive during an earlier exchange and
incorrectly qualify for catch-up later. Owed exchanges still record completion
through their item lots. This adds no new flags beyond the four planned receipts.

If Florissax's spell is removed and Senessax is already defeated, the shared
onboarding receipt permits one compensation heart, not two. If Senessax is alive,
the spell exchange still grants its one heart and the later normal boss kill
retains its normal reward. The compensation receipt does not consume that reward.

This uses ordinary item-lot receipts and existing sequential branches. It does
not add a migration version, queue, rollback system, or continual repair worker.


Verification and completion
----------------------------

Recheck exact repo/editor inputs before editing and preserve unrelated changes.
Build candidates, compare decoded parameter/event changes against this scope,
and run existing tome/onboarding checks with new cases for invalid IDs, already
compensated dragons, and both Florissax/Senessax conditions together. Sync accepted
source/binary pairs through the normal qualified editor handoff. This plan does
not authorize deployment, publication, or a commit.

Required game acceptance covers a fresh character, an existing vanilla character,
each compensation route, a reload during a later onboarding wait, previously
collected versus pending boss rewards, direct heart-only refund-row awards, and
an NG+ transition. Confirm `69990` survives, owned spells/books remain, tome
duplicate sources stay suppressed, and normal bosses/Hadeon/crystal reset as
intended. Record observed results; static inspection is not a Passed game test.


Implementation evidence
------------------------

The candidate changes exactly common events `5750009` and `5750140`, with no
other event or metadata differences. Parameter verification covers 23 field edits
across 17 rows, including the two new compensation lots, and preserves every
unrelated row and binder member. Unchanged affected tables roundtrip byte-exactly.

| Accepted artifact | SHA-256 |
| --- | --- |
| `mod/regulation.bin` | `abc570209e60f5d30746cdb227fc8b0bcdea97115a84071a260fa053acf9292b` |
| Runtime/source companion `common.emevd.dcx` | `21aaded7ae36673cc5efc2bdbda875290e1f786ff0925c9be5a3ccad50570d9f` |

Event build: `.codex-temp/event-builds/1789942885999444200/receipt.json`.
Parameter plan, native receipt, guarded acceptance, original files, and check logs:
`.codex-temp/onboarding-flag-fix/`. These scratch records are retained for review
and recovery. No staging, deployment, publication, or commit is part of this change.


Completion checks: 140 Python tests, 17 authored-event behavior tests, and repository
preparation checks pass. The latter include source simulations, not game tests.
The guarded editor sync completed and all three destinations match: Smithbox
regulation and Script common event source/binary. Neither Smithbox nor DarkScript3
was running at the pre-handoff process check. Recovery receipts are
`.sovereign/handoffs/6acf03247e9b4a748e3a94365c410dd2/receipt.json` and
`.sovereign/handoffs/9545662b400d4362aa5d2c0372db16b1/receipt.json`.
Actual acceptance remains Pending in ER-048 through ER-055.
