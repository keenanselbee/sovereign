# Sovereign manual acceptance tests

All tests below remain Pending until an actual game session supplies evidence.
Record test ID, build/receipt hash, game version, save type, steps, observed result,
and tester/date in a dated note under `docs/test-results/`. Add that directory when
there is a real result. Report failure details; do not replace an old result silently.
Use an isolated backed-up test save for progression and destructive inventory tests.
Code inspection and automation results belong in WORKFLOW/verification notes, not
in the Passed column. `python tools/sovereign.py tests` lists tests not marked Passed.

| ID | Scenario | Acceptance / observation needed | Status |
|---|---|---|---|
| ER-001 | Clean install and correct launcher | Intended mod and dependency load; record game/tool versions and logs | Pending |
| ER-002 | Existing save and first journey | Record Great Rune / Nemesis eligibility before and after progression | Pending |
| ER-003 | NG+ | Confirm deliberate reset/retention policy for Nemesis, Hadeon, ritual and rewards | Pending |
| ER-004 | Red crystal before/after Hadeon | Correct model, visibility, collision and intended release prerequisite | Pending |
| ER-005 | Break crystal, rest, warp, quit/reload | Release occurs once and persists according to decided design; no unrelated destruction | Pending |
| ER-006 | Nemesis eligible/ineligible enemies | Verify actual HP, damage, rune scaling, exclusions and cycle timing | Pending |
| ER-007 | Host and co-op roles | Only intended owner writes progression/grants rewards; clients display correct state | Pending |
| ER-008 | Hadeon encounter and player death | Arena, barrier, boss identity, reset and retry behave correctly | Pending |
| ER-009 | Hadeon defeat then reload | Correct death cleanup; encounter stays completed within intended journey | Pending |
| ER-010 | Quit during defeat-to-reward delay | Owed Erdtree's Favor +3 recovers; no duplicate after collection | Pending |
| ER-011 | Shrine ritual and gesture | Correct eligibility, progression, HP drain, completion and gesture persistence | Pending |
| ER-012 | Bind Seal equip/remove/delete | Exclusive roles, correct effects and immediate/restored Nemesis/eclipse behavior | Pending |
| ER-013 | Obliterator acquisition | Document obtainable path from a save with no weapon or ingredients | Pending |
| ER-014 | Obliterator ordinary special attacks | Test one/two-handed and crouch attacks, projectile and invalid reference | Pending |
| ER-015 | Ultimate initially and after buff | Record readiness, FP, input branch/window, success, cooldown and buff expiry | Pending |
| ER-016 | General ultimate meter | Verify ten steps, kill/deflect increments and weapon-specific bypass | Pending |
| ER-017 | Black armor appearance | Correct armor/variant, parts/material/textures, both body types and live file hashes | Pending |
| ER-018 | Changed maps and animations | Check shrine navigation/placement and a0x animation discrepancy in actual deployment | Pending |
| ER-019 | Nexus instructions against clean install | Acquisition, controls, requirements, dependencies and known limits match shipped behavior | Pending |
| ER-020 | Torrent appearance menu unlock | No regalia/no previous unlock hides entry; first owned regalia shows notification and menu; notification does not repeat after reopening/reloading | Pending |
| ER-021 | Torrent appearance selection and persistence | Only owned variants plus original are offered; selection marker, confirmation and actual summoned appearance agree; rest/warp/reload retains selection; selecting current choice shows appropriate feedback | Pending |
| ER-022 | Grace dialogue regressions | Torrent exit/back restores Grace controls/map; Sovereign entries 22/23 and their guards, level-up, flask and Melina menus retain existing behavior | Pending |
| ER-023 | Torrent regalia cleanup | On an isolated test save, verify upstream inventory cleanup and selection reset interact correctly with the menu after reload; record ownership/flags before and after | Pending |
| ER-024 | Updated animation authoring reload | Open the updated c0000.anibnd.dcx after archiving the old .dsaproj; verify a269/a972/a973 and affected timeline IDs; save only the reconciled project and recheck runtime scope | Pending |
| ER-025 | New and updated vanilla animation behavior | With the compatible behavior/HKS result, exercise new skills and a00/101104, a415/45000/45100/48000, a692/a693/a696/a699/40040; verify motion, sounds, attack timing and cancellation | Pending |
| ER-026 | Sovereign animation regressions | Verify existing custom special attacks, deflection, casting and ultimate behavior after the combined update; record source/runtime hashes and any a0x discrepancies | Pending |
| ER-027 | Current player skills and heavy cancel | Exercise skills 372/373 with sufficient/insufficient FP, hold/release inputs, heavy-cancel and follow-up branches, stance re-entry and one/two-handed transitions; confirm custom deflect inputs still dispatch correctly | Pending |
| ER-028 | Equipment, fall and authoring regressions | Check ladder exit, gestures, stealth/quick item equipment restrictions and effect-4070 fall behavior; reload the updated HKS/behavior sources in editors and ensure a save/rebuild does not restore old graph/name mappings | Pending |
| ER-029 | Recovered custom SFX | Test Obliterator cast/glow/crouch/ultimate, Nemesis and Thorn Ward, Hadeon, deflection visuals and other recovered effects against the SFX recovery receipt; verify rendering, attachment, timing and sound | Pending |
