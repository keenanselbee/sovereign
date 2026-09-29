Deflect charges and critical damage
===================================

Version 1.6.3 changes charge rows 102007-102010 from three to seven seconds.
The existing successful-deflect path refreshes/upgrades these rows, including
refreshing the fourth tier. Guard-counter damage and other charge fields stay
unchanged.

New rows 1627611-1627614 clone native Dagger Talisman effect 320900, preserving
`throwAttackParamChange=1` and `stateInfo=367`. Their five elemental attack rates
are 1.10/1.20/1.30/1.40. Category zero permits coexistence with the talisman;
actual stacking remains a game check. No icon or VFX is added.

HKS snapshots the highest active charge in `ThrowAtk_onActivate`, clears all four
charge rows, and applies exactly one critical bonus. Player ThrowParam attacker
animations 31700/31710/31720/31730/31750/31760 identify ordinary criticals;
40090/45080/45180 special grabs are excluded. The bonus has no time expiry and
is removed by the parent `Throw_Deactivate`, defensive `ThrowDef_onActivate`,
or first player Update after script load. Failed backstab attempts consume nothing.
This covers the whole multi-hit critical without extending the original charge
timer or adding an ordinary-attack multiplier.

Build an isolated candidate with a new output folder:

```powershell
dotnet run --project src/recipes/deflect-critical/DeflectCritical.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  mod/regulation.bin .codex-temp/deflect-critical-candidate `
  'Z:/Modding/Elden Ring/Tools/Smithbox'
```

The recipe requires the three-second baseline and absent new IDs. It guards
input hashes, scans parameter references, compares all untouched rows/tables
and binder metadata, and reopens the result with the native reader. It does
not modify runtime or editor files. Accept its output with the coordinated HKS
change after native player qualification. Game tests must cover both critical
types, multi-hit damage, cancellation, death/reload, Dagger Talisman stacking
and unchanged ordinary attacks.
