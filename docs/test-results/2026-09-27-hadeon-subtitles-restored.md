Hadeon subtitle restoration
===========================

The author requested subtitles back after the subtitle-disabled AI trial failed
to resolve passive behavior. Restore `t999801800.py`, its native ESD companion,
and the map talk binder to the preserved pre-isolation implementation. Audible
voice, entrance timing, proximity gating and AI events are unchanged.

The rebuilt binder matches the preserved pre-isolation binder byte for byte:
SHA-256 `73a8d8aee71177867b60208e3ef44d5f898fd8090a905056fa88e3ba39b71e86`.
Only member `t999801800.esd`, state group 1, differs from the disabled binder;
unrelated members and metadata are preserved. Native build receipt:
`.codex-temp/dialogue-builds/1790551908514684500/receipt.json`.
Full talk qualification passed:
`.codex-temp/talk-qualifications/1790551989348874600/receipt.json`.
Recovery inputs and guarded local acceptance are recorded under
`.sovereign/backups/hadeon-subtitles-restore/`.
Editor handoff `.sovereign/handoffs/3f217f1bd92648aa9e6f35f6829cd6b5/receipt.json`
completed for the source, native companion and talk binder (three files).
`sovereign.py check` passed with 74 runtime candidates. Scoped whitespace and
local documentation-link checks passed. In-game subtitle acceptance is pending.

This restores the existing subtitle route; it does not prove that its earlier
distance/restart symptoms are resolved. The author also clarified that Hadeon
tracks the player in front while idling, then changes action when the player goes
behind him. See the updated [AI trial](2026-09-27-hadeon-ai-replan-150.md).
No additional AI change was included in this restoration step. It is now included
in the authorized [1.5.1 release trial](2026-09-27-hadeon-release-151.md); that
record owns the current deployment status.
