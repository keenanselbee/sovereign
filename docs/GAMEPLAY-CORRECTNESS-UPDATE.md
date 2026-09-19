Gameplay correctness update
===========================

2026-09-11. The agreed Crusade, Scaled Armor and Hewg changes are implemented in the
repository and synchronized to their editor workspaces. The local development build
is deployed through VDB, with exact live-file verification. Native builds and
preservation checks passed. Gameplay has not been observed; the manual matrix
remains Pending. This is a playtest build, not release approval.


Implemented behavior
--------------------

- Crusade Insignia 8050 now has its missing passive SpEffect 20380500, copied from
  the installed vanilla regulation 11711000. All 12,050 existing effect rows were
  preserved, including custom 20380501 and its hidden icon. Smithbox row names were
  retained. This enables the existing on-kill chain; activation and expiry need playtests.
- Black Scaled conversion runs independently of the old full-set/rune listener.
  Common event 5750021 observes the host's active Rykard fight in m16_00_00_00, with
  battle flag 16002801 covering both phases. Player death or final-phase Rykard HP
  reaching zero samples equipment immediately. One original Scaled piece qualifies;
  equipping afterward does not. An already-set defeat flag 16000800 ends eligibility.
- Qualification stores five inventory counts and a pending marker. Workers 5750025
  resume after the player is alive, exchanging originals one-for-one using existing
  lots 7600/7610/7640/7620/7630. Altered body armor retains its altered form. Workers
  stop at their recorded count or when no carried original remains, and never use
  storage-inclusive possession checks. Debit, reward and count decrement have no
  intervening wait. Counts and pending progress survive ordinary reloads; actual
  save/interruption behavior and storage exclusion still require game tests.
- The red, white and gold paths remain unchanged. Those paths apply effects rather
  than consuming the originals. Their cleanup and resulting appearance need testing
  alongside the conversion. Encounter deaths include environmental damage; the event
  does not identify the attacker that delivered the killing blow.
- Hewg offers a prerequisite hint until Godskin Duo (9114) and all three base-game
  Fallingstar Beasts (32080800, 1041500800, 1036540800) are defeated. Then the menu
  offers `Forge the Fallingstar Obliterator`. Previously heard dialogue and weapon
  possession do not determine eligibility. The DLC beast is excluded.
- Forging closes the menu, fades out for about one second, requests Hewg's native
  smithing idle 930010 for a two-second pause, then fades back over one second.
  Common event 5750026 restores picture/control on interruption and stale requests
  after reload. The native idle supplies the intended animation/audio; timing and
  audible hammer strikes have not been observed in game.
- Before memory loss, the handoff uses the original four-row TalkParam chain
  21313000-21313003. In stages 3227/3228, new standalone TalkParam 21313200 reuses only
  "Use my masterpiece to slay a god." New item lot 7700 grants weapon 23085000 and
  owns collection flag 1055420700. The dialogue checks collection again before payout.
  A new journey requires the boss victories again and permits one further reward;
  this relies on normal journey flag reset and must be verified in ER-040.
- The separate farewell remains available after Godskin Duo in its original story
  stage, independently of the withheld masterpiece. Forging marks masterpiece heard
  (11109230) but does not set farewell heard (11109231) or reset story progression.

The unbuffed ultimate fallback, buffed beam gate, player HKS/graphs/animations,
Blasphemous Claw and Betrayer's Dragonbolt were not redesigned. Their existing
unresolved behavior remains covered by the feature plan and manual tests.


Ownership and preservation
--------------------------

The new runtime is `mod/script/talk/m11_10_00_00.talkesdbnd.dcx`, with five owned
companions in `src/talk/m11_10_00_00-talkesdbnd-dcx/`. The original ESD and baseline
DSL are pinned by `t213001110.preserve.json`; they are build inputs, not alternate
deployment files. Do not edit them to bypass a preservation failure.

Only Hewg groups x39, x58 and x59 change. ESDTool compiles baseline and edited DSL;
the preservation adapter transplants those reviewed groups into the original ESD.
It rejects additional changed groups, altered original fingerprints, and unowned
changes already present in the template. All other ESD groups, metadata and binder
members remain preserved. Plain vanilla DSL recompilation changes expression
encodings and condition nesting, so it is not used wholesale for this handoff.

All three shipped English menu binders receive the same three explicit text edits:
22130012 becomes the forging title, 22139900 adds the prerequisite explanation, and
22139901 adds the hint title. Existing farewell title 22130013 stays unchanged.
Every other entry, including null/empty/whitespace distinctions, is preserved.
The item binder is unchanged. New FMG entries require explicit `beforeMissing: true`;
an existing null entry is not treated as absent.

New mod-owned state uses 1055420600 (armor pending), 1055420610-1055420659 (five
10-bit counts), 1055420660-1055420664 (worker completion), 1055420700 (weapon claim),
and 1055420701/1055420702 (presentation request/completion). These are separate from
Hadeon/crystal and ordinary Hewg progression flags. No existing authored reference
or inspected parameter field collided with these allocations.

The catalog now owns 70 main runtime files, three texture files and 1,123 sources.
VDB permits a catalogued new runtime only when it starts from a verified selected
stage and the chosen repo scope includes every addition. Unrelated staged bytes
remain the package baseline. The new main package has 71 files including its DLL.


Evidence and recovery
---------------------

- Crusade acceptance and both prior regulations:
  `.sovereign/gameplay/crusade-20260911/receipt.json`.
- Original common source/runtime before this gameplay stage:
  `.sovereign/gameplay/armor-20260911/common.before.js` and `common.before.dcx`.
- Fourteen repo candidate/metadata acceptances, independent prior copies and hashes:
  `.sovereign/gameplay/accepted-20260911/receipt.json`.
- Current common build:
  `.codex-temp/event-builds/1789166654677363000/receipt.json`.
  Only existing events 0/5750020/5750021 changed; 5750025/5750026 were added. Other
  event bodies, ordering among existing events and file metadata are preserved.
- Hewg dialogue, parameter and text build evidence:
  `.codex-temp/gameplay-20260911/hewg-source/final/receipt.json`,
  `hewg-regulation/receipt.json`, and `hewg-text-builds.json` under the same work folder.
- Fresh Rykard event/map and Hewg binder/model extraction receipts are under that
  work folder. They identify the installed archive headers and extracted-file hashes.
- The complete pre-work backup remains listed in WORKFLOW-PREP-CHECKPOINT.

Never restore these originals over later work without comparing current hashes.
The earlier S1-S6 layout receipt predates the new catalog and intentionally refuses
automatic restoration after these edits. Use its relocation map for inspected recovery.

Required manual checks are ER-030 through ER-041, plus the existing animation,
ultimate, appearance, co-op and clean-install scenarios. Static checks do not mark
any game scenario Passed. No Nexus publication or release version is assigned here.


Completed handoff and test build
-------------------------------

The four reviewed repo-to-editor handoffs completed with independent backups:

- Params and row names: `.sovereign/handoffs/cf9acdb99fb94d0ba1ad901416752311/receipt.json`.
- Common event source/output: `.sovereign/handoffs/fefbfb74a6f243a5a01f344810942f5a/receipt.json`.
- DLC02 menu only: `.sovereign/handoffs/35771bf3df50431f8b4eb7c177bec287/receipt.json`.
- Dialogue and companions: `.sovereign/handoffs/d3917480375748f7a13e590ad8a7a90f/receipt.json`.

The dialogue qualification at
`.codex-temp/talk-qualifications/1789166806092572300/receipt.json` passed all seven
DSL sources across five binders, including an unchanged byte-identical rebuild of
the accepted Hewg binder. Native negative tests also rejected an unauthorized group
change and an altered original fingerprint without creating outputs; see
`.codex-temp/gameplay-20260911/preservation-negative/receipt.json`.
The workflow suite passed 77 tests, the repository check passed, and `git diff --check`
reported no whitespace errors. No game test was marked Passed.

Local main build `fb233a986dfb581405a38222`, version
`0.0.0-dev.20260911-gameplay`, is retained at
`.vdb/prepared/f214f86a7645452d822c8c8757014e6c/receipt.json`.
Deployment to the existing Elden Ring Default profile completed at
`.vdb/operations/385ca3fb7506411a91300ef032695b9f/receipt.json`.
Compared with the prior selected main build, only regulation, common and three menu
binders changed; the Hewg talk binder was added. Nothing was removed. Existing item
text, player animations/HKS, Claw/Dragonbolt paths, Hadeon assets and the external
DLL retain their prior package bytes. Textures remain on their existing build.

The durable folder `.sovereign/gameplay/accepted-20260911/` contains
`package-comparison.json`, `handoff-plans.json`, `editor-verification.json`,
`selected-before.json` and `deployment-verification.json`. The last two verification
records check all 1,123 mapped source files, 28 editor runtime counterparts, and
74 live package files (73 runtime assets plus the DLL). Unrelated enabled Vortex
mods were preserved. Empty historical directories contain no retired runtime files.

For a reviewed runtime rollback, the prior main stage remains at
`.vdb/prepared/6e2bfe4bc74c4b919e6e680dd6660d87/receipt.json`; use the documented
VDB rollback command with profile `SkC-QjDMc`. Re-select that verified stage if it
should also become the package source. Runtime rollback does not roll back repo or
editor authoring files; inspect the independent handoff backups before restoring
those. Do not rerun propagation immediately after a runtime-only rollback unless
reapplying the new authoring version is intended.
