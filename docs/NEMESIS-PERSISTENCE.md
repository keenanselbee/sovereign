# Shrine persistence and optional Nemesis hardcore

Applied 2026-09-10 for local testing. **Implemented and statically checked; gameplay
acceptance is pending.** No existing-save migration was added. The author's latest
clarification takes precedence over the earlier draft that gated all Nemesis activity
on crystal destruction. That draft was discarded before deployment.

## Accepted behavior

| State | Intended behavior |
|---|---|
| Crystal intact, not following | Existing passive chance-based Nemesis and ordinary progression/periodic eclipses |
| Crystal broken, not following | Persistent Sovereign of War role and eclipse escalation this journey |
| Following Nemesis, crystal intact or broken | Existing follower protection; hardcore role/eclipse suppressed |
| Leave follower state | Restore ordinary role if intact; restore hardcore if broken |
| Hadeon defeated, then rest/warp/reload | Boss and both barriers remain cleared; an owed reward is reconciled |
| NG+ | Fresh Hadeon/crystal choice; no forced hardcore; learned gesture retained |

`c9997.hks` is unchanged. Its spawn roll checks protection 1055420000 before eclipse
1055420010. This handoff adds no crystal gate to passive enemy rolls and changes no
probabilities, enemy scaling, animation, HKS or parameters. Actual suppression on
already enhanced enemies remains an acceptance test.

The ritual stays available after Hadeon with the crystal intact. Acquiring the seal
alone does not equip it: following still uses its equipped effect 1626910. The existing
unequip path consumes the seal, so the rite remains repeatable when the item is absent.
The learned gesture marker survives ordinary reloads. An interrupted performance must
be repeated; this does not save individual cinematic steps. Ritual timing, HP drain
and the existing final death condition are unchanged.

## Event and flag ownership

- `common` 5750101: new host controller for release flag 1055420918, hardcore role
  1055420003 and eclipse 1055420010, with follower/equipped-seal precedence.
- `common` 5750100: removes automatic NG+ hardcore and startup seal consumption;
  recognizes crystal-based hardcore and rechecks follower state after the spawn wait.
- `common` 5750103: uses follower role 1055420001 for equip/remove decisions, clears
  conflicting roles and selects ordinary versus hardcore on removal. This avoids
  confusing a temporary protection pulse with actual membership.
- `common` 5750115/5750116: ordinary cycle waits while ineligible; cleanup does not
  overwrite hardcore or newly acquired follower protection. An already-started cycle
  reward can finish without changing the new role. Test timing transitions in game.
- `common` 5750120: waits for the hardcore role and is initialized once by constructor,
  so an unlock in the current session can activate its icon worker.
- Shrine 5750290: sole owner of lot 6050 payout, using its existing collection flag
  1055420916. Waits eight seconds on fresh defeat, or reconciles an owed payout after
  reload once the player is alive. Save/inventory atomicity still needs an interruption test.
- Shrine 5750291: shows crystal 18002346 after defeat; host destruction sets 1055420918;
  hides the crystal whenever that flag is set. Clients observe the host flag.
- Shrine 5750300/5750302/5750304/5750305: remove testing resets, initialize shared
  death reconciliation at startup, clean up a completed encounter and guard late work.
- Shrine 5750303: host-owned victory sequence retains corrected Hadeon and barrier
  references. Reward and crystal ownership moved to the dedicated reconciliation events.
- Shrine 5750309: persistent defeat flag gates the ritual; crystal release does not.
  Retains repeat seal awards while absent and selects the correct unbound role afterward.

No new ritual-completion lock was retained. Flag 1055420009 is the existing gesture
award marker. Flags 1055420914/0917 are no longer cleared by the old testing block;
this change does not assign them a new mechanic.

NG+ handling relies on the engine's ordinary journey reset of event flags, as described
in the [EMEVD tutorial](https://soulsmodding.com/doku.php?id=tutorial%3Alearning-how-to-use-emevd).
There is no custom migration/reset-on-load shortcut. Verify these exact flags and the
seal/gesture inventory behavior in ER-003 before claiming tested journey behavior.

## Validation and handoff

DarkScript3 compiled all ten authoring sources. Independent SoulsFormats decoded
comparison found seven changed existing events plus one new event in `common`, and
six changed existing events plus two new events in the shrine file. The other 296
common and 54 shrine events matched completely. All seven other runtime event files
matched completely. Existing event order and file metadata were preserved.
`common_func` remains an authoring-only reference; no runtime override was introduced.

New flag 1055420918 had no occurrence in the ten original repo event sources or in
instruction argument bytes of the nine decoded baseline runtime files. This is a
scoped collision check, not a full-game flag-allocation proof.

The exact source and runtime candidates were synchronized across repository, external
Script authoring workspace, Vortex and live mod folders. Source-side compiled copies
were included. All 22 destination hashes passed; 16 physical in-place writes preserved
six existing shared-file relationships. A subsequent two-line whitespace cleanup
updated the four common JS copies (three physical writes); recompilation retained
identical runtime binaries and decoded data. All four passive HKS copies remained unchanged.
Maps, regulation, animations and behavior graphs were outside this handoff.
Reload these two JS files in DarkScript/other open editors before saving older buffers.

| Accepted file | SHA-256 |
|---|---|
| `source:common.emevd.dcx` | `e823b783c0e6b3e17d49d82adfb98c8fb9d98bf857cf146c8b985c9ffcbfc50f` |
| `binary:common.emevd.dcx` | `dbb0bc6bbe78a9b95a81c427b123d0ac4f5c23d7b1d970e4420e0fb3f24c0cba` |
| `source:m18_00_00_00.emevd.dcx` | `e29a9c8c294bd134bd6ab2776022c6da3148f70fd375adf888b04acedc9ba593` |
| `binary:m18_00_00_00.emevd.dcx` | `f1dc05dbcc824faec373fdfb5bb2405a0f8284cfa4c328976fa20a21b6037d41` |

Backups and detailed evidence remain deliberately local in
`.codex-temp/nemesis-persistence-20260910-001512/`:

- `before/` contains all 26 original scoped source/runtime/HKS snapshots.
- `plan.json` maps every original target to its backup and pre-edit hash.
- `verification.json` records decoded preservation and accepted candidate hashes.
- `deployment.json` records each deployed target, final hash and shared-file relation.
- `*.emevd.dcx.diff` contains final source comparisons against the pre-handoff state.
- `workspace/.codex-temp/event-builds/1789025365982499300/` is the accepted final build.
  Earlier scratch candidates are superseded and must not be deployed.

For rollback, use `plan.json`/`deployment.json` and verify current files still match
accepted hashes before restoring the corresponding originals in place. Do not blindly
rerun a scratch editing or deployment script over subsequent user work.

## Test next

1. Fresh journey: defeat Hadeon; verify entrance wall 18002379 and barrier 18002347
   clear, boss identity/banner/music are correct, and crystal becomes available.
2. Quit during the death-to-reward delay; reload alive. Confirm one Erdtree's Favor +3
   payout, then rest/warp/reload again with no boss, barrier or duplicate reward.
3. With crystal intact, verify ordinary passive Nemesis still occurs. Perform the
   ritual and equip the seal; confirm protection. Remove it and confirm ordinary
   behavior resumes; repeat the ritual to replace the consumed seal.
4. Break the **entity 18002346** crystal. Verify flag 1055420918 and persistent
   escalation, then rest/warp/reload. Equip the seal to suppress it; remove the seal
   to restore hardcore. Repeat with the seal already equipped when breaking the crystal.
5. Equip during ordinary eclipse cleanup and immediately after ritual completion;
   confirm cleanup cannot clear protection. Check already enhanced enemies, icons/music,
   player death/retry and host/co-op roles.
6. Enter NG+: verify Hadeon and crystal return, hardcore is not forced, old reward and
   release flags reset as intended, and the learned gesture remains. Record equipped
   seal carryover separately.

Physical-map check remains open: the inspected primary crystal has HP 1000/defense
10000; an overlapping entity-0 model has HP 1/defense 0. If only the latter breaks,
the watched destruction condition will not fire. Inspect/select 18002346 in Smithbox
and test its damageability; no automatic map replacement was made. The author also
owns the entrance wall placement. Release timing/balance and the ritual's final death
condition remain review items, not newly validated features.
