# Mechanics evidence and release decisions

Inspection baseline: 2026-09-09. These are static findings from local source,
compiled events, parameters and map exports, not gameplay test results. Do not turn
proposed behavior into Nexus claims. Local detailed exports and earlier analyses are
under `.codex-temp/sovereign-inspect/`; source event IDs below provide durable anchors.
Existing user edits to regulation and shrine map are preserved by workflow preparation.

## Nemesis and the physical red crystal

Current compiled logic enables Nemesis through Great Rune progression (flag 181,
derived from flags 170-179) and first-journey eligibility (flag 50). Breaking the red
crystal is not an activation requirement in the inspected logic. Conditional Nemesis
effects include doubled HP/attack and tripled rune rewards for eligible enemies;
these are not an unconditional global difficulty modifier.

In `map/MapStudio/m18_00_00_00.msb.dcx`, the named Nemesis crystal
`AEG258_158_2019` has entity ID 18002346, HP 1000 and defense 10000, without a
configured break item lot/behavior. An overlapping `AEG258_159_2018` has entity ID
0, HP 1 and defense 0, also without the release payload. A visible model breaking
therefore does not establish that Nemesis was released. In the inspected compiled
shrine events, references to 18002346 hide it at startup (5750300) and show it after
Hadeon's defeat (5750303); no matching destruction-to-release transition was found.

The intended design discussed with the author is an optional harder mode released
by breaking the crystal. Implementing that still needs an explicit persistent release
flag, host-only activation, crystal presentation across reloads, NG+ policy and a
decision about existing saves where Nemesis is already active. Keep this separate
from a change that merely removes testing resets.

The inspected cycle contains testing-scale waits: initial waits of six seconds and
other random waits up to 60 seconds. Combat blessing waits are around 5-6 seconds,
not the older 30-600 description. Do not promise a fixed six-second cadence. Removing
the Bind Seal may also leave eclipse event 5750115 ended until constructor reload;
test immediate reactivation as well as reloading.

## Shrine and Hadeon / Crucible Lord

Primary source: `event/src/m18_00_00_00.emevd.dcx.js`, events 5750300-5750309.

| Finding | Why it matters / proposed review |
|---|---|
| Startup event 5750300 resets 1055420914, 1055420915, 1055420916, 1055420917 and 1055420009 in its TEMP block | Testing reset defeats persistence; remove only deliberate reset writes after classifying each flag |
| A nearby commented early exit guards broader initialization | Do not uncomment the whole exit as a shortcut; it can skip ritual setup |
| 5750303 uses actor 18000850 for special-effect/boss-defeat operations while Hadeon is 18002354 | Confirm and correct actor references against the map, then test defeat reconciliation |
| Post-defeat startup can skip 5750302 / common 90005300 death reconciliation | Check actor removal and reload behavior after permanent defeat |
| Reward lot 6050 grants accessory 1043, Erdtree's Favor +3; reward flag is 1055420916 | Death flag 1055420915 precedes delayed payout; quitting during the interval can lose the reward |
| Reference 18002349 is a region, not a mapped asset/group | Barrier calls need the correct object and location, not an arbitrary nearby numeric substitution |

Existing barrier assets 18002347 and 18002379 are at different locations. Removing
resets alone does not resolve these lifecycle, reference and reward issues. Design
the reward to reconcile owed-but-unclaimed completion after load, and prevent repeat
grants after collection. Decide NG+ reset behavior before calling completion permanent.

Ritual 5750309 checks area 18002377, Hadeon HP <= 0 and absence of Bind Seal 6800.
It grants gesture 102 once through flag 1055420009, then uses effects 1626966/1626967
for progression. Lot 6800 is repeatable (lot flag 0). Its NG+ eligibility guard is
commented out. Role 2 is set without clearly clearing role 3. The final death/HP
condition needs gameplay interpretation because HP drain may be intentional.

Bind Seal 6800 equips effect 1626910: +16 stamina recovery and +70 casting DEX,
not +70 actual Dexterity. Equipping sets bound role 1 and suppresses the affected
enemies; removal/deletion switches to role 2. Verify inventory/equipment changes,
role exclusivity and eclipse resumption in the same session and after reload.

## Obliterator and special attacks

The inspected weapon row 23085000 exists, but no connected acquisition recipe/drop
was found. Goods 8115 (Meteoric Ore Slab) and 8116 (Eye of Astel) are placeholders
in the inspected path. Do not publish an acquisition guide until an obtainable path
is implemented and tested from a save without the weapon.

The weapon uses category 984. Skill 660, Harness Void Eye, costs 45 FP and applies
effect 1626770 for 60 seconds, including state 7750 and +100 magic/lightning attack.
The ultimate HKS gate checks readiness 7588 and window 7551, excludes cooldown 7587,
and requires the relevant two-handed/right-hand input branch. In the inspected
configuration the combination uses R2 with L1 when the swap setting is true (L2
when false), with button hold below two seconds. These are source conditions;
controller behavior and input timing still require an in-game test.

The general charge meter has ten steps: ordinary kill/deflect gives one, larger
deflect two. It starts at effect 277 and reaches full at 287. The Obliterator's
resident effect 287 bypasses this ordinary charging path, but its buff/readiness
conditions still matter, explaining why simply equipping it is insufficient. The
ultimate uses Astel's beam bullet 4620221 and refreshes the buff. Older descriptions
of a universal 30-second requirement do not match this inspected path.

A two-handed crouch attack uses a gravity projectile. An additional one-handed
behavior reference 300000867 resolves to an invalid reference (-1) in the inspected
data; verify the expected attack and missing connection before listing it as working.

## Evidence policy

For every published feature keep: source path plus event/row ID, condition and
effect, source/build hashes, test IDs, and the latest observed result. Use
**Implemented (static evidence)**, **Observed in game**, **Proposed**, or **Unresolved**
explicitly. A successful compiler run, matching package hash, or copied description
is not evidence that progression, acquisition or persistence works.
