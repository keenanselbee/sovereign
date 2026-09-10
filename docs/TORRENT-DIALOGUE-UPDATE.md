# Torrent appearance dialogue update

Applied 2026-09-09 against the archive-derived Steam build 25080141 baseline.
The shared Grace dialogue now includes the upstream Torrent appearance menu while
preserving Sovereign's custom dialogue. In-game acceptance remains Pending.

## Change and verification

The source is `script/talk/modified/m00_00_00_00-talkesdbnd-dcx/t000001000.py`;
its runtime output is `script/talk/m00_00_00_00.talkesdbnd.dcx`.

- Added upstream functions x85-x90, groups 2147483557-2147483562. Adapted their
  x4 keyword arguments to the existing Sovereign helper signature.
- In x31, state 17 now calls the unlock/menu helper through new state 56 before
  continuing to existing state 51. State 8 adds selection 75; new states 57/58
  handle map/selection cleanup, run x87 and return to the existing menu loop.
- Existing entries 22/23, custom level-up logic and all other existing states are
  unchanged. All 91 other existing groups and all six other binder members are
  unchanged; those six member payloads are byte-identical.
- Binder header fields, member order/IDs/names/flags/compression metadata and
  existing ESD metadata were preserved. Witchy extraction verified every payload.
- The original repo source qualified with byte-identical member round trips.
  The six new helper sources match current vanilla except the required keyword
  adaptation. Their decoded output matches a separate current-vanilla ESDTool
  rebuild. ESDTool changes vanilla numeric/boolean expression encodings and
  simplifies unconditional subconditions: these new helper bytes are not claimed
  to match the original vanilla compiler's representation.

The appearance entry initially unlocks with owned goods 2009600, 2009610 or
2009620 and flag 69560. Original appearance is always offered in the submenu;
alternate choices require their regalia. Selection clears flags 6700-6703 and
sets the chosen flag. The earlier common-event and text/icon updates provide
supporting changes. Static inspection does not verify actual Torrent rendering.

## Authoring and deployment

The external Script/talk workspace had historical vanilla loose ESDs for both
t000001000 and t000003000. Its sources also omitted shipped custom helpers.
The repo sources reproduce shipped behavior and were selected deliberately.

The handoff updated nine paths: repo source and runtime, main Vortex and live
runtime, external packed binder, and both external custom scripts' source/ESD
pairs. Updating external t000003000 restores the already-shipped customization;
its runtime payload was not changed by this patch. The other five external loose
ESDs already matched. A packed mod binder was added beside the external unpacked
folder as an explicit future compilation template.

All nine destinations passed hash verification, with eight physical writes and
the existing Vortex/live hardlink retained. Nineteen other monitored talk files
remained unchanged. No broad propagation, Nexus publication, game launch, HKS,
behavior-graph or animation changes were performed. Reload affected source files
before saving from an editor buffer opened before this handoff.

## Rebuild procedure

Use ESDTool from its installation directory, with explicit scratch input/output
paths. ESD `.py` files are its DSL; do not execute them as Python.

```powershell
.\esdtool.exe -er -noannotate `
  -i '<scratch-template>\m00_00_00_00.talkesdbnd.dcx' `
  -i '<scratch-source>\t000001000.py' `
  -writebndfile '<scratch-output>\m00_00_00_00.talkesdbnd.dcx'
```

The template must be the accepted mod binder. Preserve its real filename: ESDTool
can silently skip output when the template basename differs from the requested
binder name. Require the expected output to exist and independently inspect it.
Requalify after tool changes; unchanged source must preserve all member payloads.
Inspect intentional group/state changes after edits. Use WitchyBND to extract the
accepted binary ESDs for authoring handoff; do not rebuild from stale loose ESDs.

## Evidence and remaining tests

Durable hashes and checks: [receipt](patch-updates/steam-25080141-torrent.json)
and [source diff](patch-updates/steam-25080141-torrent.source.diff).
Independent original backups now live in
`archive/game-updates/2026-09-09_to-steam-25080141/03-torrent-dialogue/before/`.
Use the archive entry's `restore-map.json` for the relocated restoration paths.
Candidates, decoded comparisons and the historical one-shot handoff receipt remain
in `.codex-temp/torrent-dialogue/1789015528282739600/`, with an archive pointer.
The archived files are local and Git-ignored. Do not rerun the applied handoff.

Run ER-020 through ER-023 in [TEST-MATRIX.md](../TEST-MATRIX.md): first unlock,
owned choices, actual appearance and persistence, already-selected feedback,
menu exit/map recovery, existing Sovereign menus and regalia cleanup. Record
actual observations before marking any test Passed or claiming release readiness.
