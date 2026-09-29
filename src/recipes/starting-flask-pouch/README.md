Starting flask pouch defaults
============================

The author reports that later flask acquisition populates the intended pouch
slots. Full refill/upgrade and all-class acceptance remains pending.
The guarded patch uses the existing parameter builder:

```powershell
dotnet run --project tools/tome-params/TomeParams.csproj `
  '-p:SmithboxRoot=Z:/Modding/Elden Ring/Tools/Smithbox' -- `
  <matching-input-regulation.bin> src/recipes/starting-flask-pouch/patch.json `
  <new-candidate-regulation.bin> 'Z:/Modding/Elden Ring/Tools/Smithbox'
```

The recipe requires its recorded source hash and exact original field values.
For a later game/mod baseline, inspect the current rows and deliberately rebase
the recipe; do not reuse the old regulation as a replacement.

All twelve player classes (3000-3011) receive one empty Cerulean flask (1050) in
secondary slot 02 and one empty Crimson flask (1000) in secondary slot 03. These
target right and left respectively; verify the native directional mapping in game.
Memory of Grace, other slots, the 3/1 flask capacities and all class stats remain
unchanged. The Stranded Graveyard item-lot group 2000 still grants charged flasks
1001 x3 and 1051 x1. No charges are deliberately added to character creation.

`isAutoEquip` is cleared for HP/FP flask rows 1000-1025 and 1050-1075, including
empty and charged variants through +12. This prevents automatic pickup equipment,
including after upgrades, while retaining manual equipment permission. It is a
global item rule, not a script that removes existing quick-item assignments.

The builder verifies exact native table roundtrip, unchanged unrelated rows and
tables, binder identity and output readback. These checks cannot prove that the
engine retains empty pouch entries or transfers them to charged/upgraded variants.
Test a new character before considering the defaults accepted; existing characters
do not receive a pouch migration. No save editor or persistent equipment enforcer
is introduced.

The original `patch.json` records the ten-class implementation.
`new-classes.patch.json` extends the same four pouch fields to Idus Knight (3010)
and Heavy Knight (3011), guarded against the accepted 1.6.8 regulation. All other
class fields and parameter tables remain unchanged. Apply each recipe only to its
recorded input; these are incremental patches, not replacement regulations.


Zero-quantity whistle trial
--------------------------

`whistle-zero-quantity.patch.json` targets the accepted 1.6.9 regulation. All twelve
classes set secondaryItem_04 to Spectral Steed Whistle 130 while keeping
secondaryItemNum_04 at zero. Slot 04 is the intended bottom pouch direction.
The whistle already has isAutoEquip=0, so no goods parameter change is needed.
Normal Melina item-lot 100000, acquisition flags and dialogue remain unchanged.

This is an experiment, not a verified assignment-on-pickup feature. Test a fresh
character: no usable early whistle; receive it normally; inspect the bottom pouch
and quick items; rest/reload and try using it. Also put a different item in the
bottom slot before acquisition and verify the player's choice stays intact. If
the engine drops the zero-count assignment, this parameter-only approach fails.
Existing saves receive no assignment migration, and no runtime enforcement is added.
