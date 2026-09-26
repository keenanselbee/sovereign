Archived game-file baseline inventory
====================================

This is a read-only inventory of the two folders labelled `1.16` and `1.17` under
`Z:/Backup/Elden Ring/ER Base Files`. It covers the 75 runtime paths in
[`asset-catalog.json`](../asset-catalog.json), including the main and separate textures
packages. The [machine-readable inventory](baselines/archived-game-files.json) records
each exact relative path, package, catalog group, presence, byte size and SHA-256 hash.
It also records the catalog hash so a later catalog change cannot be mistaken for the
same scope.

| Archive label | Main present | Textures present | Missing catalog paths |
| --- | ---: | ---: | ---: |
| `1.16` | 44 of 72 | 3 of 3 | 28 |
| `1.17` | 44 of 72 | 3 of 3 | 28 |

All 47 present paths occur in both folders. SHA-256 is equal for 31 paths and differs
for 16. Equality establishes byte identity only for these copies. The inventory is
useful for choosing inputs to a future three-way comparison; it does not itself
qualify a merge, rebuild, editor handoff or game compatibility.


Missing catalog paths
---------------------

The same 28 exact paths are absent from both archive folders. In particular, neither
folder has `regulation.bin`. The 27 missing parts paths are:

```text
parts/am_m_1122.partsbnd.dcx
parts/am_m_1124.partsbnd.dcx
parts/am_m_1125.partsbnd.dcx
parts/am_m_1126.partsbnd.dcx
parts/am_m_1127.partsbnd.dcx
parts/am_m_1128.partsbnd.dcx
parts/am_m_1129.partsbnd.dcx
parts/bd_m_1122.partsbnd.dcx
parts/bd_m_1123.partsbnd.dcx
parts/bd_m_1124.partsbnd.dcx
parts/bd_m_1125.partsbnd.dcx
parts/bd_m_1126.partsbnd.dcx
parts/bd_m_1127.partsbnd.dcx
parts/bd_m_1128.partsbnd.dcx
parts/bd_m_1129.partsbnd.dcx
parts/hd_m_1122.partsbnd.dcx
parts/hd_m_1150.partsbnd.dcx
parts/lg_m_1122.partsbnd.dcx
parts/lg_m_1124.partsbnd.dcx
parts/lg_m_1125.partsbnd.dcx
parts/lg_m_1126.partsbnd.dcx
parts/lg_m_1127.partsbnd.dcx
parts/lg_m_1128.partsbnd.dcx
parts/lg_m_1129.partsbnd.dcx
parts/wp_a_0615.partsbnd.dcx
parts/wp_a_0615_l.partsbnd.dcx
parts/wp_a_0868.partsbnd.dcx
```

These are missing from these two exact archive roots, not a claim that the game or
other backups lack them. The [recovered source inventory](../src/README.md) also
distinguishes recovered members from missing archive inputs.


Collection and provenance
-------------------------

Collected 2026-09-25 with
[`tools/inventory_archived_baselines.py`](../tools/inventory_archived_baselines.py).
The script reads catalog group file paths, checks only the corresponding path beneath
each labelled folder, streams each existing regular file into SHA-256, and records its
byte count. Run `python tools/inventory_archived_baselines.py --check` to compare a
fresh inventory with the saved JSON; omit `--check` to refresh it after intentionally
changing the archive or catalog. No file in the backup was written.

The `1.16` and `1.17` names are directory labels. A bounded search of those folders
for version/build manifests, receipts, `regulation.bin` and similarly named metadata
found no independent build record. The presence of game-format files, timestamps and
the 16 changed hashes do not establish an exact Steam build or prove these copies are
clean vanilla. Before using either as an authoritative upstream baseline, tie the
folder to a trusted acquisition/build record or verify its hashes against a separately
authenticated game extraction. Preserve the archive's original bytes and use the
catalog paths and hashes in the JSON to guard any later comparison.
