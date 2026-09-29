Hadeon aid flag precision
========================

The author reports missing stat increases and continued failure to engage after
the first monologue. These are separate investigations. The retained aid log
contains only about two seconds outside combat, with permission and combat flags
off; it does not establish the encounter's AI state or recorded loss count.

The progressive aid cap introduced in 1.4.4 used
`tostring(1055420929 + death)` for the five saved event flags. HKS uses
single-precision numbers; these expressions round to `1055420928`, so converting
them to text cannot restore the intended IDs `1055420930` through `1055420934`.
The [Script Exposer API documentation](https://github.com/ElaDiDu/Scripts-Data-Exposer-FS/blob/main/NewHksInfo.lua)
explicitly warns about rounding above 16,777,216 and recommends string IDs.

The local correction passes five exact string literals directly to GetEventFlag.
Caps, effect magnitudes, warm-up and withdrawal are unchanged. The first attempt
still deliberately receives no aid. This correction shipped in 1.4.6; see the
[combined deployment record](2026-09-27-deflect-hadeon-trial.md).

Verification
------------

`test_saved_flag_ids_survive_hks_float_precision` models single-precision numeric
conversion and rejects any malformed flag address. It failed on the old code and
passes after the correction for zero through five saved losses. All three aid
tests pass, including resource preservation and withdrawal. Ordinary wider-number
Lua tests previously missed this engine-specific defect.

Player qualification `.codex-temp/player-qualifications/1790545018797993600/receipt.json`
reuses unchanged native player assets with new HKS guards. Pre-edit HKS and its
hash are in `.sovereign/backups/hadeon-aid-flag-precision/`.
The guarded editor handoff completed for `c0000.hks` only:
`.sovereign/handoffs/11d09c8a481442648659d88af9ef96a3/receipt.json`.
No live-game files changed.
In-game aid confirmation and the separate AI-engagement diagnosis remain pending.

The author confirmed that missing aid occurred after dying and returning, not
on the intentionally unaided first attempt.

Separate combat investigation
----------------------------

Event 5750311 enables Hadeon's AI in the same valid-room branch that starts the
health bar and music. The only other AI disables found are spawning and reset.
Native Gideon event 11052860 waits for conversation completion, then sets Enemy
team, enables AI and uses AlwaysUpdate; it does not require ReplanAI, AICommand
or an animation reset. Hadeon's existing NpcParam already uses Enemy team.
Decoded Gideon evidence is retained under
`.codex-temp/hadeon-diagnosis-146/gideon-output/`.

Dialogue retaining behavior control through the final four seconds is an
unproven hypothesis. Remaining passive after the whole recording ends would
weaken it. An encounter trace needs combat flag 1055422933, voice 1055422946
and engine Combat-state diagnostic 1055422949 around the cue and after 18 seconds.
The retained two-second log cannot resolve this. No speculative AI fix is applied.

For proximity-started speech, the proposal is a distance condition around
Hadeon combined with the existing room/fall guards. Once started, speech must
remain latched independently of distance; combat timing must follow actual
audio start. No activation radius or proximity implementation is accepted yet.
