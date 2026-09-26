Hadeon room and hallway lighting
================================

Death follow-up (1.3.1, deployed)
--------------------------------

Death now preserves the current brightness and set of ignited positions; pending
positions wait for recovery instead of lighting during the death camera. Hadeon
resetting his HP cannot change the frozen brightness. Confirmed death rearms the
sequence only after the player recovers, with one frame for position workers to
observe the reset; map reload also starts a fresh attempt. Brief zero-HP rescues
resume without resetting the attempt. Victory and crystal presentation retain
precedence. Flame workers also observe their ignition flag so respawn can reset
flames even when the brightness preset remains unchanged.

Source simulation covers partial/full ignition, frozen brightness through boss
HP reset, long death, retry, rescue and crystal override. Changes are restricted
to events 5750370, 5750373, 5750401 and 5750404. Thirty-second timing and all hallway
pairs remain unchanged. Game acceptance is pending.

Current revision (1.3.0)
------------------------------------------

The accepted entry duration is now thirty seconds. All 96 positions retain their
fixed shuffled order, with starts from 0.05 through 29.5 seconds (about 0.31
seconds apart) and the existing 0-0.04-second jitter. Event 5750404 completes at
thirty seconds. HP brightness, death/retry, victory and post-eclipse dimming rules
are unchanged. No map, FXR or parameter changes are needed.

Lighting remains in EMEVD condition/timer waiters, outside the player HKS Update.
The 96 ignition, 384 preset and 88 flame workers are unchanged; at most 96
controlled illumination effects are active. Faster ignition adds no workers or
peak lights. Engine condition evaluation still costs time; no frame-time
benchmark has established its cost. The reported successful 1.2.9 entry test used
the previous sixty-second timing. Thirty-second visual acceptance is pending.
Backups and compilation evidence: `.codex-temp/room-ignition-30s/`.

Hallways now swap 125 lit originals with 125 unlit duplicates, entity IDs
18006000-18006124. Original fixtures use automatic model-SFX offset 50; unlit
copies use empty offset 61. The twelve existing region events preserve their
conditions, first-region delay, exit cancellation, victory all-on and crystal
all-off states. Only one fixture per pair is enabled. No manual effect attachment
or additional per-frame player work is used. Room fixtures retain their working
independent flame/light controllers.

Four missing model-family red rows (23872050, 23873050, 23874050, 23876050) are
added using the previously verified effects and sockets. Existing rows are
unchanged. Native roundtrips preserve all unrelated map content, parameters and
binder metadata. Event simulations cover every hallway region and persistent
states; rendering and performance require the next game test. Backups, pair
mapping and native evidence: `.codex-temp/hall-aid-1.3.0/`.

Earlier revision (1.2.8)
------------------------

Entry now ignites 96 individual positions over sixty seconds in a fixed shuffled
order, spaced about 0.63 seconds apart with the existing 0-0.04-second jitter.
There are no authored off pulses. Event 5750404 owns the timeline; 5750370 now
selects HP brightness continuously during ignition. Victory still lights the
whole room; crystal destruction retains the five-second eclipse followed by
three 0.75-second dimming steps. Confirmed death resets the sequence.

The 96 physical room fixtures remain visible throughout. The 125 existing hallway
fixtures now also remain visible: their model-SFX offset 61 selects an empty row,
while events 5750320-5750331 attach/remove their effects using the unchanged
proximity, delay, victory and crystal rules. Missing placements 18009864/18009866
are no longer referenced. Three empty AssetModelSfxParam rows are added for
AEG004_693, AEG020_994 and AEG023_874; other existing empty rows are reused.
Unrelated map fields, parameter rows and the common SFX binder are unchanged.
No meshes are swapped and no extra room lights are active simultaneously.

Hall effects reuse 7505982/7505983/7505984 at socket 200 and the existing red
other-family 75% illumination 7506127 at socket 201 for AEG023_872. All sockets
and packed effect dependencies were verified. This does not establish visual
appearance or frame time in game. Runtime simulation covers individual ignition,
concurrent HP changes, retries, victory, crystal, hallway exit/reentry and saved
states; native map/parameter readbacks preserve unrelated data.

New temporary ignition gates are 1055425100-1055425195. Previous 42 gates are
retired; 1055422996/2997 and sustained-death 1055425042 keep their roles.
Backups and native evidence: `.codex-temp/lighting-aid-1.2.8/`.
Game acceptance remains pending in ER-109/110.


Earlier revision (1.2.5)
------------------------

The 1.2.4 flag correction moved ignition gates into valid temporary range
1055425000-1055425041. In 1.2.5 the catch-light flashes are removed: a group turns
on once at its scheduled time and stays on. Room and ignition reset checks now
use shared sustained-death flag 1055425042 instead of a single zero-HP observation.
The ten-second schedule, HP intensity stages, victory hold and post-eclipse fade
remain. See [implementation and verification](HADEON-RESET-1.2.5.md).

Earlier revision (1.1.9)
------------------------

Supersedes the historical five-second/gaze behavior below. Entry takes ten
seconds: 14 individual braziers and 28 candle groups (26 of three assets, two of
two) ignite in an authored shuffled order. Each has a separate, evenly spaced
start window with 0-0.04s runtime jitter. The order is stable across retries;
randomness no longer clusters whole banks. The 0.45s catch-light flicker remains,
and HP brightness resumes at ten seconds. Long waits abort on death.

Gaze event 5750371 and gaze/surge conditions are removed. Only 25/50/75/100%
illumination is used; unused 150% placements/FXRs remain disabled. Parameterized
workers 5750372/5750373 own each group's light presets and continuous flames.
No SFX rebuild is needed. At most 96 controlled lights remain active, as before.

The 14 AEG024_157 room braziers receive entity IDs 18004800-18004813 in the
existing B087-through-B098 light order and model-SFX offset 61. New empty
AssetModelSfxParam 24157061 suppresses automatic flame creation only for these
placements. Shared row 24157050 and all other placements are unchanged. Existing
flame-only FXR 7505984 attaches at socket 200 on ignition. Along with 74 candle
flames, 88 attachments are controlled. They persist through catch-light flicker
and HP changes, then extinguish at final off or player death. Models stay visible.

Temporary gates 1055423000-1055423041 replace 1055422970-1055422995;
1055422996/1055422997 retain completion/activity roles. Victory/crystal flags,
entry box 18000359, the five-second crystal cue and 0.75s fade steps are unchanged.
All 127 hallway candles retain their own proximity/victory/crystal logic.
Native preservation checks and source simulation pass; appearance, placement and
frame time need a game test. Backups/evidence: `.codex-temp/room-rick-1.1.9/`.


Approved follow-up, implemented and awaiting deployment/game tests: the two ceiling
Grafted Scions (18000350/18000351) are suppressed by restart event 5750400.
Their ambush and reward initializers are removed; their map records and vanilla
defeat flags are preserved. Pre-lighting backups have the same actor records,
trigger and initializers, so the reported return was not established as a lighting
regression. Different saved defeat flags remain a possible explanation.

Entry now starts a five-second ignition sequence: 14 separate braziers and 12
candle banks of six or seven assets each. Each bank waits a random 0.05-4.35
seconds, then pulses on/off/on/off/on over 0.45 seconds at the 25% preset.
Candle particle flames start with their bank and remain continuous; only the
illumination flickers. HP-based brightness resumes after the entrance sequence,
and gaze pulses wait for its completion. Leaving alone does not replay the room
intro; death/rest/reload resets the attempt. Victory and crystal destruction
bypass unfinished ignition; already-defeated loads show full lighting, while
already-broken crystals load dark. Existing crystal-cue/fade timing is retained.

Temporary flags 1055422970-1055422995 gate the 26 banks; 1055422996 marks completed
ignition and 1055422997 marks the active intro. Event 5750401 runs once per bank.
Brazier workers 5750372-5750376 retain their presets; candle workers 5750410-5750469
replace 5750380-5750399, and flame workers 5750470-5750481 replace 5750377.
The 480 map-SFX preset placements and 74 flame attachments remain unchanged.
This adds sleeping event workers, not lights, meshes, textures or FXR variants.

Evidence is in `.codex-temp/room-ignition-20260924/`: before-copies, bank membership,
source execution simulation and native build comparison. Simulation covers staggered
entry, all-on completion, death/re-entry, victory and crystal interruptions, and
saved-state loads; it does not establish engine timing or visual correctness.

Version 1.1.4 implements the author's 2026-09-24 lighting decisions. Native format,
event compilation and preservation checks pass; appearance, performance and timing
in the game remain pending. This is an FXR lighting trial across all 14 braziers.


Room behavior
-------------

Use existing Env_Box211, entity 18000359 (internal Region ID 9052). Its position is
(41.055, -103.418, 150.921), yaw -26.433, with dimensions 60 x 36 x 62. The author
explicitly accepts activation from the space below the room. This is also the box
already used by Hadeon's arrival event. No new entry box is added.

Before first entry, the brazier illumination is off. Entry starts at 25%. Hadeon's
remaining HP selects 50% at 75% HP, 75% at 50% HP, and 100% at 25% HP. Defeat with
the crystal intact holds 100%, including subsequent loads. Player death clears the
attempt lighting; rest/reload reconstructs it from the current encounter state.

The current BTL diffuse intensity of 2 is the 75% reference. FXRs use red diffuse
and specular colors, radius 9, view distance 50, and no shadows, fog, particles,
textures or models. Specular intensity scales from the previous 0.5 reference.
BTL-to-FXR visual equivalence still requires an in-game comparison.

| Stage | Diffuse intensity | Specular intensity | FXR |
| --- | --- | --- | --- |
| Off | 0 | 0 | None |
| 25% | 0.666667 | 0.166667 | 7506100 |
| 50% | 1.333333 | 0.333333 | 7506101 |
| 75% | 2 | 0.5 | 7506102 |
| 100% | 2.666667 | 0.666667 | 7506103 |
| 150% | 4 | 1 | 7506104 |

While Hadeon lives and the player is in the box, one of four small groups catches
Nemesis's gaze every 3-6 seconds for one second. It rises one stage. At the 100%
baseline, a 150% surge has a one-in-four chance; otherwise it stays at 100%.
Defeat, crystal destruction and player death stop the pulses.

The crystal-break presentation lasts five seconds, including its 0.1-second sound
lead-in. The outside-door cue remains ten seconds and the Chapel cue remains three.
The room holds 100% through the crystal cue, then steps down to 75%, 50%, 25%, and
off, holding each lower stage for 0.75 seconds. Reloading after crystal destruction
starts off without replaying the eclipse or fade. Actual hardcore eclipse state
is independent and is not cleared by the lighting sequence.


Assets and ownership
--------------------

Only these BTL lights have their diffuse/specular powers zeroed; all other fields
and lights are preserved. The prefix is `エクストラダンジョン松明`:

`B087`, `B087_0001`, `B088`, `B089`, `B090`, `B091`, `B092`, `B093`,
`B093_0005`, `B094`, `B095`, `B096`, `B097`, `B098`.

The existing pillar/brazier models are untouched. At each light position, five
initially disabled map-SFX regions reference the shared presets. Entity IDs are
18003900-18003969; internal Region IDs are 11000-11069. In the order above,
each light owns five consecutive IDs. Groups contain indices 0-3, 4-7, 8-11,
and 12-13. The four brighter shrine lights and two dim interior lights are unchanged.

Event 5750370 owns brightness flags 1055422950-1055422953. Event 5750371 owns
gaze flags 1055422960-1055422963 and chance flags 1055422964-1055422967.
All are temporary and explicitly reset on restart. Events 5750372-5750376 each
own one preset per brazier and sleep on mutually exclusive conditions. There are
70 sleeping event slots, with one selected light per position; no per-frame polling.
Common event 5750360 owns temporary crystal-presentation flag 1055422945. It raises
that flag before consuming request 1055422944 and clears it after removing the
presentation effects. The fade waits for both request and active flags to clear.

Five FXRs and five empty resource lists are added to the common-effects overlay.
They were authored with @cccode/fxr 32.1.0, then read and round-tripped independently
with Smithbox's native FXR reader. The specialized binder rebuild preserves all
15,411 old member payloads and metadata; only canonical insertion-related numeric
binder IDs shift. No external texture or model resources are required.


Hallway and verification
------------------------

The 127 candle assets in events 5750320-5750331 retain their 12 approach regions
while Hadeon lives. His defeat turns all on. Crystal destruction turns all off
immediately and keeps them off on reload. The room braziers and, from 1.1.5, room candles wait for the
eclipse before fading. The original first group's 1.5-second approach delay remains.

The subsequent approved proximity correction makes all 12 groups turn off on
leaving their own approach box while Hadeon lives, and re-arm for the next entry.
The first group's delay is cancelled by leaving, victory or crystal destruction;
it cannot briefly light after the player has already left. Victory holds all
groups on regardless of proximity, and crystal destruction takes priority over
both conditions. This event-only correction is synced locally; deployment and
in-game acceptance remain separate.

Backups are retained under `.codex-temp/hadeon-fxr-trial-20260924-000537/backup`,
with SHA-256 manifest `backup-manifest.json`. The subsequent refresh, candidates,
map differences and verification receipts are in `.codex-temp/hadeon-lighting-20260924`.
The editor map differs from the original repo map only in the ordering of c4721
and c8120 model entries; the editor's ordering is preserved.

Native checks cover unchanged MSB/BTL roundtrips, all unrelated fields, 70 unique
initially disabled map-SFX regions, temporary flag allocation, all preserved SFX
members, affected event IDs and metadata, and 20 mutually exclusive stage/gaze
combinations. See ER-088 through ER-091 in the test matrix for manual acceptance.


Room candle extension (1.1.5, corrected in 1.1.6)
-------------------------------------------------

The author approved all 82 room candle assets: 75 floor/ledge candle assets and
seven tall candlesticks. The two entrance assets already owned by the hallway
remain excluded: AEG023_873_2005 (18009987) and AEG023_875_2013 (18009986).
All 127 hallway assets and their existing event bodies are unchanged.
The exact room inventory is [hadeon-room-candles.csv](hadeon-room-candles.csv).

| Model | Room assets |
| --- | --- |
| AEG004_692 | 5 |
| AEG020_992 | 25 |
| AEG023_862 | 7 |
| AEG023_872 | 1 |
| AEG023_873 | 1 |
| AEG023_875 | 39 |
| AEG023_876 | 4 |

The candles share the existing room brightness flags, entry box and timing.
They start off, light red at 25% on entry, rise with Hadeon's HP thresholds,
hold at 100% after victory, and fade 75/50/25/off after the five-second crystal
presentation ends. Saved crystal destruction starts them off without replay.
No additional saved flags, player effects or tutorial timing changes are added.

Models, transforms, collision and physical candle counts are preserved. Each
asset receives a unique entity ID (18004100-18004181) and model-particle offset
61, backed by a new empty AssetModelSfxParam row for its model. Existing rows
are untouched, so other candles using these models retain their old behavior.
The empty row prevents an automatic light from stacking with its controlled one.

Event 5750377 owns the 74 actual particle-flame effects as a single group:
start when room lighting becomes active, remove when it becomes off. The
existing red candle FXR 7505983 is copied to 7506110 with its point-light
configuration removed; flame geometry, texture and emitter settings remain
intact. It is attached at these models' dummy 200.

Correction in 1.1.6: the other eight models do not need an added particle flame.
The seven tall candlesticks and curved AEG023_872 retain their models and their
controlled map lights. The earlier calls to 834042 and 830022 were removed.
Neither was available in the common or m18 binder. Inspecting 830022 and the
available 834040/834041/834044 family showed supplemental point lights and no
rendered flame-particle configurations; importing them would add uncontrolled
lighting. No substitute flame geometry or new resource dependency is introduced.
The exact map inventory is unchanged; its Flame FXR column now says None for
these eight models.

Ten small pure-light FXRs (7506120-7506129) supply the five stages for two
existing light families. The 75% reference is intensity 8/radius 4 for 74 candles
and intensity 3.2/radius 4.5 for the eight other assets. From 1.1.6, each preset
copies every original PointLight field from 7505983 or 800370 respectively.
Only colour (red), diffuse/specular intensity (stage/75), zero fade-out for
instant preset replacement and the existing 50m visibility bound are changed.
The original startup intensity ramp is replaced by the selected steady stage
so a 0.75-second fade step can reach its intended value. Exposure adaptation,
volumetric settings, all unknown light fields and original flicker are preserved.
Flicker intervals are 0.1875-0.375s for 74 candles and 0.25-0.5s for the other
eight. Shadows remain disabled. At most one controlled light is selected per
asset. Five assets whose old offset 50 had no exact model-SFX row receive the
explicit controlled red candle effect at their verified socket.

Five initially disabled map-SFX regions per candle are alternatives, not five
simultaneously active lights. Entity IDs 18004200-18004609 and internal region
IDs 11100-11509 are collision-checked. Static light positions use native FLVER
socket coordinates transformed by each asset's placement; the eight models
whose old light was at the asset origin retain that origin.

Events 5750380-5750399 control four spatial strips of 21, 21, 21 and 19 candles,
with five mutually exclusive workers per strip. Together with the flame owner,
this adds 21 sleeping controllers, no per-candle polling loop and no model
switching. Only the affected strip switches light presets during a gaze pulse;
flames are not recreated. The existing room/brazier/gaze/hallway controllers
are preserved byte-for-byte in the decoded event comparison.

Backups and qualification receipts are retained in
`.codex-temp/hadeon-candles-20260924`. Checks cover native map/parameter/FXR
readbacks, unchanged unrelated map fields and parameter rows, all 15,421 old
SFX binder members, exactly 22 new effect/resource members, exclusive preset
conditions and event ownership. The prior unmodified SFX build reproduced the
original packed bytes. Native checks do not measure in-game frame time or
establish visual equivalence; see ER-092 through ER-094.


Corrective qualification (1.1.6)
-------------------------------

Backups and receipts are retained in `.codex-temp/hadeon-candle-fix-1.1.6`.
The only intended packaged differences from 1.1.5 are the common-effects binder
and the Graveyard event binary. The map, regulation, BTL, 74-candle flame FXR,
braziers, hallway, gaze/HP controllers and crystal/eclipse timing are unchanged.

Ten candidate light FXRs are independently read and round-tripped with the
native reader. A semantic readback comparison checks every PointLight field
against its actual source, allowing only the six explicitly owned fields.
The retained flame effect contains no PointLight or SFXReference. Binder review
requires identical member names/order/metadata, no additions or removals, and
exactly ten changed effect payloads. Event review requires only 16 removed
instructions in 5750377: eight creates and their eight matching deletes, with
all other event bodies and metadata identical. Deployment hashes are checked
separately from gameplay. ER-092 through ER-094 remain the in-game acceptance
cases; the two exceptional model families should show controlled red illumination
without extra particle flames or unscaled coloured lights.
