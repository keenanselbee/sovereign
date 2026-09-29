-- Execute with the qualified Lua 5.0 interpreter, from the repository root.
-- Tests actual Act15 selection; this does not emulate Havok or in-game damage.
function RegisterTableGoal(id, name)
    Goal = {}
    if id == 250091 then BattleGoal = Goal end
end
function REGISTER_GOAL_NO_SUB_GOAL() end
TARGET_SELF = 0
TARGET_ENE_0 = 1
GOAL_COMMON_ComboTunable_SuccessAngle180 = 10
GOAL_COMMON_Wait = 11
dofile(arg and arg[1] or "src/ai/hadeon/250091_battle.lua")

local enabled = {}
local initAi = {}
local initializedFlags = {}
function initAi:SetEventFlag(flag, value)
    assert(flag >= 1055425275 and flag <= 1055425278 and value == false)
    initializedFlags[flag] = true
end
function initAi:EnableUnfavorableAttackCheck(mode, animation)
    assert(mode == 0)
    enabled[animation] = true
end
BattleGoal.Initialize(BattleGoal, initAi, {}, 0)
for flag = 1055425275, 1055425278 do
    assert(initializedFlags[flag], "Diagnostic results must clear on AI initialization")
end
for animation = 3030, 3033 do
    assert(enabled[animation], "Private route must be registered with the AI")
end
for animation = 3080, 3083 do
    assert(not enabled[animation], "Superseded route must not remain registered")
end

local cases = {
    {1.0, 3030}, {0.75001, 3030},
    {0.75, 3031}, {0.50001, 3031},
    {0.50, 3032}, {0.25001, 3032},
    {0.25, 3033}, {0.01, 3033}
}
local checks = 0
for _, case in ipairs(cases) do
    for roll = 1, 100 do
        local ai = {hp = case[1], roll = roll, reads = 0, flags = {}}
        function ai:GetHpRate(target)
            assert(target == TARGET_SELF)
            self.reads = self.reads + 1
            return self.hp
        end
        function ai:GetMapHitRadius() return 1 end
        function ai:GetRandam_Int(first, last)
            assert(first == 1 and last == 100)
            return self.roll
        end
        function ai:SetEventFlag(flag, value)
            self.flags[flag] = value
        end
        local goal = {}
        function goal:AddSubGoal(kind, duration, animation, target)
            assert(kind == GOAL_COMMON_ComboTunable_SuccessAngle180)
            assert(duration == 10 and target == TARGET_ENE_0)
            self.animation = animation
        end
        RuneKnightsSwordThroatbag250091_Act15(ai, goal, {})
        assert(goal.animation == case[2])
        assert(ai.reads == 1)
        ai.hp = 0.01
        assert(goal.animation == case[2], "HP changes must not alter an already queued attack")
        local chances = {25, 42, 58, 75}
        assert(ai.flags[1055425258] == (roll <= chances[case[2] - 3029]), "HP-tier chance must decide arming")
        assert(ai.flags[1055425296] == true and ai.flags[1055425297] == false,
            "Queuing the route must latch only the route-queued diagnostic")
        for flag = 1055425275, 1055425278 do
            assert(ai.flags[flag] == false, "Prior diagnostic result must clear at Act15")
        end
        checks = checks + 1
    end
end

local diagnostics = { [1055425253] = true, [1055425254] = true, [1055422933] = true }
local diagnosticAi = {}
function diagnosticAi:IsEventFlag(flag) return diagnostics[flag] == true end
function diagnosticAi:SetEventFlag(flag, value) diagnostics[flag] = value end
function diagnosticAi:GetHpRate(target) return 1 end
function diagnosticAi:IsFinishAttack() return false end
function diagnosticAi:IsThrowing() return true end
local diagnosticGoal = {}
function diagnosticGoal:AddSubGoal(kind) assert(kind == GOAL_COMMON_Wait) end
BattleGoal.Activate(BattleGoal, diagnosticAi, diagnosticGoal)
assert(diagnostics[1055425290] and diagnostics[1055425291] and diagnostics[1055425292])
assert(not diagnostics[1055425293] and not diagnostics[1055425294] and not diagnostics[1055425295])
assert(diagnostics[1055425296] == nil and diagnostics[1055425297] == nil)
diagnostics[1055425296] = true
BattleGoal.Activate(BattleGoal, diagnosticAi, diagnosticGoal)
assert(diagnostics[1055425297] == true, "Next activation must record route reactivation")
print("Passed " .. checks .. " native Lua Act15 selections and request diagnostics.")
