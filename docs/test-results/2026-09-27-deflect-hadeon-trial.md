Deflect stamina and Hadeon conversation trial
=============================================

The author authorized implementation and deployment of 75% of the previous
deflect stamina cost, protection from stamina guard break on successful
deflection, and a subtitle-disabled Hadeon comparison. Version 1.4.6 also
includes the previously verified aid-cap precision and independent no-repeat
dialogue updates. Gameplay acceptance remains pending.

Deflect changes
---------------

Only `guardStaminaMult` changes in five SpEffectParam rows: 102001 goes from
0.30 to 0.225; 102011, 102013 and 102015 from 0.35 to 0.2625; 102060 from
0.66 to 0.495. Timing windows, ordinary guarding and attack parameters stay
unchanged. The two-handed effect retains its existing category/application;
these individual values do not prove a combined 25% reduction in all grips.

HKS receives guard break before its normal successful-deflect branch. The trial
reroutes only `DAMAGE_TYPE_GUARDBREAK` with depleted stamina, living HP, a positive
guard action level and one of the same four timing markers used by the existing
success branch. Parry, attacking while guarding and effects 175/176 exclude it.
The existing success branch restores stamina below 1 to 1, selects the normal
deflect reaction and grants its existing rewards once. It does not refund normal
costs, protect mere window activation or reclassify direct damage, wall recoil,
blast/fling break types or positive-stamina forced breaks.

This acts before the HKS guard-break animation dispatch, but after the engine
reports the received hit. It is not a native pre-damage hook. Live acceptance
must establish that the engine's break state clears and that native exhausted
guards report a positive guard action level. A zero level conservatively leaves
the break unchanged. Do not report unconditional protection as proven yet.

Hadeon comparison
-----------------

The custom ESD entry now quits without starting a conversation. Only
`t999801800.esd` changes in its binder; other characters retain their dialogue.
The original source/native/binder are retained in the backup below. This trial
removes all Hadeon subtitles, not his separately played voice recordings.
No audio, timing, AI, room or saved first-encounter flag changes accompany it.
The full opening remains once per journey; a save that already consumed it uses
the existing repeat entrance. No save flags are cleared to force a replay.

On an eligible first entrance, inspect attacks at 13 seconds into speech and
after the recording ends. On repeat entrance, combat remains immediate.
If movement/attacks return, the conversation route is implicated; continued
passivity requires the existing combat/voice/AI-state trace, not another assumed
conversation fix. The no-repeat pool remains active for audible lines.

Verification and recovery
-------------------------

Rollback inputs: `.sovereign/backups/deflect-hadeon-146/inputs.json`.
Accepted parameter/native talk candidates: its `accepted.json`.
The guarded [parameter recipe](../../src/recipes/deflect-stamina/README.md)
verifies all rows and preserves unrelated binder members/metadata; candidate
receipt `.codex-temp/deflect-cost-146/receipt.json` records the five changes.
Talk candidate `.codex-temp/dialogue-builds/1790546572679028200/receipt.json`
preserves other ESDs and binder metadata. The selected state group contains only
one inert state with no commands or transitions; its exact companion is accepted.

`test_deflect_stamina.py` covers all four timing markers, repeated depleted hits,
ordinary blocks, positive-stamina breaks, zero action level, dead/parry/poke and
175/176 exclusions, other damage types, non-refunded ordinary costs, and routing
before the break branch. These are source tests on an ordinary Lua runtime,
not proof of native HKS/game behavior.

Manual acceptance: compare the same hit with shield, one-handed and two-handed
guards at full/low/one stamina; sustain a correctly timed long combo; deliberately
miss a deflect and confirm break risk. Check undeflectable stomp, grabs, deaths,
co-op and a pre-existing break. Verify Hadeon on an unaided first attempt and
after a genuine death, and verify no consecutive repeat lines across reloads.

All focused source tests pass: two deflect tests, three aid tests, the progression
simulation and eight existing encounter tests. Repository preparation, local
Markdown targets, whitespace and the parameter recipe build also pass.
Native player qualification reused unchanged player assets with fresh HKS guards:
`.codex-temp/player-qualifications/1790546832616694900/receipt.json`.
Talk qualification: `.codex-temp/talk-qualifications/1790546895278475300/receipt.json`.
Guarded editor handoffs completed for regulation, HKS and the three talk companions:
`.sovereign/handoffs/944e811ca3594761bc2ad8b374b748d5/receipt.json`,
`.sovereign/handoffs/145d870d48e94dbcbe3ebc21c22e6f82/receipt.json`, and
`.sovereign/handoffs/2923f7c852fc444596bc2e5d37cb06c0/receipt.json`.

The full main-package preparation contains 75 files. Against 1.4.5, exactly
four differ: regulation, player HKS, the Graveyard event file (no-repeat pools),
and its talk binder (subtitle test). The other 71, including full voice audio
and the external Script Exposer DLL, remain byte-identical.
Prepared receipt: `.vdb/prepared/8cfd9e5e47944c19b864c806dfa0e3fa/receipt.json`.
Deployment finalization: `.vdb/finalizations/8d4ec7a69f8c4e6aa2227949be1939a0/receipt.json`.
Finalization completed for active profile `SkC-QjDMc`: 1.4.6 enabled and deployed,
with no reported differences. An independent SHA-256 check matched all 75 live
files. Build ID `14f1d65bc01374ffbc0f836a`; request
`1aaee868-42fe-4749-906b-a32afa338127`. Restart the game before manual acceptance.
