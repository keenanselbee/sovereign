Model authoring files
====================

The original weapon-model extraction was moved unchanged from the former root
`parts` folder. The 2026-09-25 recovery adds Hadeon's FLVER and member overlays for
30 equipment archives, with nested DDS images where applicable. Exact paths,
member metadata, baseline limits and hashes are recorded in
[the extraction manifest](../extracted-members.json).

These are recovered binary editing inputs, not automatically qualified rebuild
sources. Some folders are partial overlays; preserve unlisted baseline members.
Compare with the corresponding `mod/` binder and qualify serialization before
accepting a rebuilt output. See [source coverage](../README.md).
