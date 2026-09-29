-- Run with the qualified Lua 5.0 interpreter; accepts compiled member as arg[1].
function RegisterTableGoal(id, name)
    Goal = {}
    if id == 250091 then BattleGoal = Goal end
end
function REGISTER_GOAL_NO_SUB_GOAL() end
TARGET_SELF = 0
TARGET_ENE_0 = 1
GOAL_COMMON_Wait = 99
dofile(arg[1] or 'src/ai/hadeon/250091_battle.lua')
-- Stop at the first native-combat call; only the actual request branch is mocked.
function Init_Pseudo_Global() error('normal-combat') end
local cases = {
    {'melee-ready', true}, {'far-ready', true}, {'attack', true},
    {'throw', false}, {'speech', false}, {'opening', false},
    {'player-dead', false}, {'boss-dead', false}, {'inactive', false},
    {'no-request', false}, {'acknowledged', true}
}
for _, case in ipairs(cases) do
    local name = case[1]
    local flags = {[1055425253] = name ~= 'no-request', [1055422933] = name ~= 'inactive'}
    flags[1055422946] = name == 'speech'
    flags[1055422947] = name == 'opening'
    flags[1055425254] = name == 'acknowledged'
    local ai = {}
    function ai:IsEventFlag(id) return flags[id] end
    function ai:SetEventFlag(id, value) flags[id] = value end
    function ai:GetHpRate(target)
        if (target == TARGET_SELF and name == 'boss-dead') or
            (target == TARGET_ENE_0 and name == 'player-dead') then return 0 end
        return 1
    end
    function ai:GetDist() return name == 'far-ready' and 20 or 1 end
    function ai:IsFinishAttack() return name ~= 'attack' end
    function ai:IsThrowing() return name == 'throw' end
    local waited = false
    local goal = {}
    function goal:AddSubGoal(kind, duration, target)
        assert(kind == GOAL_COMMON_Wait and duration == 0.25 and target == TARGET_ENE_0)
        waited = true
    end
    local ok, message = pcall(BattleGoal.Activate, BattleGoal, ai, goal)
    if case[2] then
        assert(ok and waited and flags[1055425254], name)
    else
        assert(not ok and string.find(message, 'normal%-combat') and not waited, name)
        assert(not flags[1055425254], name)
    end
end
print('Passed 11 periodic AI action-boundary cases.')
