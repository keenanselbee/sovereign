# Sovereign 1.0.0 deployment

2026-09-19: deployed main and textures at the author's request to the active
Elden Ring Default profile (`SkC-QjDMc`). Both packages are enabled. VDB verified
all 74 staged/live files with no differences, and both exact stages are selected
as the local packaging sources. This was a local deployment, not a Nexus upload.

| Package | Version | Build | Files |
| --- | --- | --- | --- |
| Main | 1.0.0 | `dd8fd7b6f7cb375975bfc461` | 71 |
| Textures | 1.0.0 | `36448ef900ceb267210b1709` | 3 |

Main includes the accepted Hadeon milestone/fall/thorns changes and the one-frame
opening deflect timing adjustment. Its five runtime differences from the former
selected stage are regulation, player HKS, the player animation binder, the shrine
event and the previously committed common event. Textures are byte-identical to
the former selected texture stage. Neither package adds or removes files.

The unused 1.0.1 target was consolidated into 1.0.0 before submission. Both 1.0.0
payloads are now reserved; changed payloads require a new version. `releaseReady`
remains false. ER-042 through ER-047 and other manual acceptance tests remain Pending.

## Verification and recovery

Event source/binary qualification and coordinated native player qualification
passed. The reviewed repo-to-editor handoffs updated 12 destinations, with recovery
backups. Repository preparation/version checks, whitespace checks and all seven
Hadeon source tests passed. These are not in-game acceptance results.

Protocol-3 all-profile finalization completed staging but preserved the disabled
profile state. A separate explicit `deploy-batch` activated both requested builds
on the current profile and completed one Vortex deployment. The game was closed.

Durable local receipts:

- Main: `.vdb/prepared/04931832f16440e1bfec629d7cf1a803/receipt.json`.
- Textures: `.vdb/prepared/a52653257c09419e9f1f8ef7e9384eee/receipt.json`.
- Finalization: `.vdb/finalizations/8ee9925cbeb14415bbcbf3a1d2bbf374/receipt.json`.
- Deployment: `.vdb/operations/47ed677aa8f54f13b04bdc85b2ba5246/receipt.json`;
  bridge request `149faf5b-4780-4104-a322-76bdc65238b4`.
- Regulation handoff: `.sovereign/handoffs/d5e88e2915034e9daa49372c540751e9/receipt.json`.
- Player handoff: `.sovereign/handoffs/c72b8259c6a74cb79ad72b6f03f7a2e9/receipt.json`.
- Event handoff: `.sovereign/handoffs/a320c5b3307d42e0903489f9091d4293/receipt.json`.

The previous main build `fb233a986dfb581405a38222` and texture build
`fe46cb9983080cddbe556f20` remain retained for explicit rollback. No commit,
publication or manual gameplay test was performed by this deployment.
