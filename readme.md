Sovereign
=========

An Elden Ring overhaul built around deflection, weapon ultimates, Oaths, Dragon
Communion and Nemesis, the Blood Star.

The [Nexus page](https://www.nexusmods.com/eldenring/mods/201) provides player-facing
information and downloads. Local page copy is in [docs/nexus-full-desc.txt](docs/nexus-full-desc.txt).

Development
-----------

- [Repository layout and workstation paths](docs/REPOSITORY-LAYOUT.md)
- [Editing and completion workflow](docs/WORKFLOW.md)
- [Supported commands](docs/WORKFLOW-COMMANDS.md)
- [Mechanics evidence](docs/MECHANICS.md), [design](docs/DESIGN.md) and [balance](docs/BALANCE.md)
- [Manual acceptance tests](TEST-MATRIX.md)
- [Nexus and release workflow](docs/NEXUS.md)

Runtime files live in `mod/`; editable sources in `src/`. The separate texture
payload is under `packages/textures/mod/`. Documentation and Nexus text live in
`docs/`; promotional images and artwork live in `images/`.

Configure ignored workstation paths in `tools/eldenring-paths.local.json` using the
example beside it. Run `python tools/workspace_paths.py check` to inspect configured
paths and shortcuts. Follow the editing guide before rebuilding binary assets.

Automated checks establish source and file consistency. Gameplay acceptance is
recorded separately in the test matrix; `releaseReady` remains false. Historical
player-guide claims are preserved in [reference/readme-legacy.md](reference/readme-legacy.md).
