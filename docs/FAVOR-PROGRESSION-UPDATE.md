Erdtree's Favor progression, version 1.1.3
========================================

Hadeon now grants Erdtree's Favor +1 through existing item lot 6050. The lot keeps
collection flag 1055420916 and the existing interrupted-reward reconciliation.
Shunning-Grounds lot 35000700 now grants one Darklight Arc (Goods 197), retaining
collection flag 35007700. Already-collected vanilla treasure grants nothing extra.

The custom +3 accessory 1043, its dedicated effect 310423 and its three accessory
text entries are removed. No conversion for older Sovereign saves is provided, as
requested. Existing vanilla talismans are unaffected. Base/+1/+2 parameters and
the Ashen Leyndell +2 lot 11050100 remain unchanged. The historical +3 reward in
earlier reports is superseded by this change; no map or event edit is needed.

The same deployment includes the approved short-fall correction in c0000.hks:
Blasphemy/Supremacy force a protected medium landing only above 20 metres, matching
their existing lethal-fall check. Vanilla state 266 retains its original behavior.

Validation checks exact decoded parameter changes and preserves every other row,
table and text entry. The text container also passed a byte-exact Witchy roundtrip.
The short-fall condition passed 96 static height/buff combinations and qualified
player asset handoff. These checks do not establish in-game behavior; ER-086 and
ER-087 in TEST-MATRIX remain pending.

Temporary candidates, backups and native evidence are under
`.codex-temp/favor-1.1.3/`. Editor handoffs and VDB finalization retain independent
recovery receipts. Nexus publication is separate from this local deployment.
