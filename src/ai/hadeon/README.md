Hadeon private AI logic
=======================

`250090_logic.lua` adds two event-command waits to Hadeon's normal logic goal.
Command 1900 holds him still while turning toward `TARGET_ENE_0` during speech;
command 1901 holds his post-retreat orientation by turning toward `TARGET_SELF`.
Each wait lasts 0.25 seconds. Clearing slot 0 to -1 and requesting an AI replan
returns to the native `010000_logic` branches. Private battle goal 250091 clones
native 250010 and preserves its attack weights, actions and interrupts. It defines
private goal IDs 250091 and 250092 because native `aicommon` has no constants
for them. It checks
periodic warp request flag 1055425253 when selecting a new battle action. If
combat is active, both targets are alive, no speech is active or pending,
and Hadeon is not throwing, it raises acknowledgment flag
1055425254 and briefly waits. While the request remains raised, the wait
repeats; the event clears the request after the warp. The event owns timer, arena
and landing validation and must recheck them before moving Hadeon. Raising the
request must not force an AI replan. Version 1.6.8 observes `IsFinishAttack()`
for diagnostics only; real traces showed it blocking requests at battle
activation for up to 98 seconds. Engine activation timing and gameplay
scenarios still require in-game acceptance.

Version 1.6.2 removes the 8 m separation gate. The elapsed 15-30-second request
survives speech, melee proximity and an unavailable landing; a retry releases the
AI wait before trying another action boundary. Death/arena invalidation or a
successful periodic/Vortex relocation resets the cooldown. Periodic destinations
must clear both participants by 2.5 m. Opening, fall and Vortex landing rules are
unchanged.

Hadeon's private `NpcThinkParam` row is 25009900, with logic ID 250090 and battle
ID 250091. Actor 18002354 alone uses that row. The original
[parameter recipe](../../recipes/hadeon-ai-params/README.md) creates the row;
the [periodic AI recipe](../../recipes/hadeon-periodic-ai/README.md) changes only
its battle ID. The original Think row 25009000 remains intact.


Rebuild
-------

The game uses 64-bit Lua 5.0 bytecode. Build `luac50.exe` from the official
[`lua-5.0.2.tar.gz`](https://www.lua.org/ftp/lua-5.0.2.tar.gz), SHA256
`a6c85d85f912e1c321723084389d63dee7660b81b8292452b190ea7190dd73bc`.
In a Visual Studio x64 developer command prompt, from the extracted source root:

```bat
cl /nologo /Od /Zi /Iinclude /Isrc /DLUA_OPNAMES /Fe:luac50.exe src\l*.c src\lib\lauxlib.c src\luac\luac.c src\luac\print.c
```

The tested optimized `/O2` build crashed while parsing; `/Od` produced valid
bytecode. Keep the compiler and source extraction in repository scratch, not in
the shipped mod. Build the binder from the installed game's native
`010000_logic.luabnd.dcx` metadata:

```powershell
& src/ai/hadeon/build.ps1 `
  -TemplateBinder 'Z:\Steam\steamapps\common\ELDEN RING\Game\script\010000_logic.luabnd.dcx' `
  -LuaCompiler '.codex-temp\hadeon-ai-155\luac50-unpatched.exe' `
  -WitchyBND 'Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe' `
  -OutputDirectory '.codex-temp\hadeon-ai-155\build-output-new'
```

`build.ps1` compiles the source, checks its native Lua header, derives
`.luagnl` and `.luainfo` from the original binder, updates only the private
registration, and repacks the three members. It requires scratch and output
inside `.codex-temp`, rejects an existing output directory, guards inputs and
tool hashes, and writes a receipt in scratch. Choose a new output directory
for each rebuild. WitchyBND 3.0.1.0 was used for
the candidate below.


Periodic battle candidate
-------------------------

Build the private battle binder from the installed game's native
`250010_battle.luabnd.dcx` metadata:

```powershell
& src/ai/hadeon/build-battle.ps1 `
  -TemplateBinder 'Z:\Steam\steamapps\common\ELDEN RING\Game\script\250010_battle.luabnd.dcx' `
  -LuaCompiler 'C:\Repositories\Sovereign\.codex-temp\hadeon-ai-155\luac50-unpatched.exe' `
  -WitchyBND 'Z:\Modding\Elden Ring\Tools\WitchyBND\WitchyBND.exe' `
  -OutputDirectory 'C:\Repositories\Sovereign\.codex-temp\hadeon-periodic-ai\battle-output-new'
```

The builder preserves the native binder's two member IDs and metadata, changes
its private registration and global names, and records input and output hashes.
The compiled native 250010 decompilation matched the original opcode, constant
and function listing after excluding source lines and memory addresses. The
private 250091 source starts with that matched decompilation, changes its goal
names, defines both private IDs, and adds the request branch at `Goal.Activate`.
The branch uses documented
Elden Ring AI methods [`IsEventFlag`, `SetEventFlag`, `IsFinishAttack` and
`IsThrowing`](https://eladidu.github.io/readable-ds-lua/d1/d81/class_ai_func.html).

The original periodic-teleport candidate was
`.codex-temp/hadeon-periodic-ai/battle-output-registered/250091_battle.luabnd.dcx`, SHA256
`29d6ce316d6e4cb347c0ab5ea93904d747ca6a82f9c92db221d971d0c05cdd48`.
Unpacking confirmed two original member IDs and payload hashes matching the
builder receipt. The separate parameter candidate and validation are under
`.codex-temp/hadeon-periodic-ai/params-candidate/`. Neither candidate has been
tested in game. The revised registered binder and combined parameter chain are
now accepted locally; see the [integration report](../../../docs/test-results/2026-09-27-hadeon-refinement.md).


Candidate qualification
-----------------------

The reviewed candidate is
`.codex-temp/hadeon-ai-155/build-output-final/250090_logic.luabnd.dcx`, SHA256
`b4dcd22fc3978050c49a166b7901d6f9fc1b600c495af6cbfb490d96bc06d546`.
The native template binder hash
was `7173e17c6ddb89c1a468fcd200ca287044e346d56f96f14837a10b4ff46b00e1`.

- Independent SoulsFormats read confirmed exactly three members with original
  IDs 1000, 1000000 and 1000001, renamed internal paths and payloads matching
  the built candidate.
- Decoded `.luainfo` registers goal 250090 as `Hadeon250090_Logic`, with
  `logicinterrupt=True`, `battleinterrupt=False`, and interrupt function
  `Hadeon250090_Interupt`; `.luagnl` contains those two globals.
- Lua 5.0.2 recompilation of the native `010000_logic` decompilation matched
  its native listing in all logic and interrupt instructions and constants.
  Only source-line labels and process memory addresses differed.
- DSLuaDecompiler read the new compiled member and recovered both wait branches
  and the unchanged default branches. A Lua 5.0.2 mock executed the compiled
  member and checked 1900/enemy facing, 1901/self facing, -1/default setup and
  the false interrupt return.

These are static and mocked checks. In-game loading, facing, command release and
ordinary attack recovery still require a gameplay test after deployment.

HP-tier Vortex, 2026-09-28
--------------------------

Act15 snapshots HP once and selects private c2500 routes 3030-3033 at
2, 7/3, 8/3 or 3 times the original motion speed. Selection weights rise
modestly at lower HP;
all routes retain shared 15-second cooldown checks. One 25/42/58/75 percent
roll arms flag 1055425258, consumed by the animation cue event. The AI never
restarts the active animation for that warp. Native Lua 5.0 compilation and
800 boundary/roll simulations pass; game behavior remains to be tested.
See [the combined report](../../../docs/test-results/2026-09-28-hadeon-vortex.md).

The current combat retune multiplies only Act10's native sustained flame-breath
selection weight for animation 3016 by 0.85. It leaves other initial action
weights and native combo follow-ups unchanged. Diagnostic flags 1055425290-5295
latch, respectively, periodic request observed by battle activation, unfinished
attack, active throw, speech hold, zero self/target HP and missing combat flag.
They never gate the action and the map event clears them at the next periodic
timer cycle. Flag 1055425296 latches after Act15 queues a private route;
1055425297 latches when the battle goal next activates after that queue. Both
reset at the next Act15. Reactivation does not prove the attack completed or
its TAE events fired.

Version 1.6.8 restores the 25/42/58/75 percent roll after correcting the private
clip bindings. Marker observations remain independent of that roll.

Version 1.6.3 temporarily replaced that probability roll with an always-armed
attempt. Cue, invalid encounter, no landing and success remain latched in
1055425275-1055425278 until the next Act15 or AI initialization. The reversible
HKS trace samples them; eligibility spheres expand to 8 m while both 2.5 m
clearances and animation timing remain. See the
[diagnostic trial](../../../docs/test-results/2026-09-28-deflect-critical-vortex-163.md).

Version 1.6.0 replaces the failed 3080-3083 routes with native-supported slots.
See [the routing correction](../../../docs/test-results/2026-09-28-hadeon-followup-160.md)
for dispatch validation and remaining game acceptance.
