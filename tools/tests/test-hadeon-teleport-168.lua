-- Execute with the native Lua 5.0 runtime and the compiled private battle member.
GOAL_COMMON_Wait = 1
TARGET_SELF = 0
TARGET_ENE_0 = 1
GOAL_COMMON_ComboTunable_SuccessAngle180 = 2
function RegisterTableGoal(id, name)
    Goal = {}
    if id == 250091 then BattleGoal = Goal end
end
function REGISTER_GOAL_NO_SUB_GOAL(id, value) end
function Init_Pseudo_Global(ai, goal) error("native branch") end
dofile(arg[1])

local function run(options)
    local flags = { [1055425253] = not options.noRequest,
        [1055425254] = options.ack, [1055422933] = not options.noCombat,
        [1055422946] = options.speech, [1055422947] = options.pending }
    local waits = 0
    local ai = {
        IsEventFlag = function(self, id) return flags[id] end,
        GetHpRate = function(self, target)
            if options.dead == target then return 0 end
            return 1
        end,
        IsFinishAttack = function(self) return options.finished or false end,
        IsThrowing = function(self) return options.throwing end,
        SetEventFlag = function(self, id, value) flags[id] = value end,
    }
    local goal = { AddSubGoal = function(self, id, duration, target)
        assert(id == GOAL_COMMON_Wait and duration == 0.25 and target == TARGET_ENE_0)
        waits = waits + 1
    end }
    local ok, err = pcall(BattleGoal.Activate, BattleGoal, ai, goal)
    if not ok then assert(string.find(err, "native branch")) end
    return flags, waits
end

local flags, waits = run({})
assert(flags[1055425254] and flags[1055425291] and waits == 1)
flags, waits = run({ finished = true })
assert(flags[1055425254] and not flags[1055425291] and waits == 1)
flags, waits = run({ ack = true })
assert(flags[1055425254] and waits == 1)
for _, options in ipairs({ {noRequest=true}, {noCombat=true}, {speech=true},
    {pending=true}, {throwing=true}, {dead=0}, {dead=1} }) do
    flags, waits = run(options)
    assert(not flags[1055425254] and waits == 0)
end

local count = 0
for _, sample in ipairs({{1,3030,25},{0.751,3030,25},{0.75,3031,42},
    {0.501,3031,42},{0.5,3032,58},{0.251,3032,58},{0.25,3033,75},{0.01,3033,75}}) do
    local armed = 0
    for roll = 1,100 do
        local flags = {}
        local ai = {
            SetEventFlag = function(self,id,value) flags[id] = value end,
            GetHpRate = function(self,target) return sample[1] end,
            GetMapHitRadius = function(self,target) return 1 end,
            GetRandam_Int = function(self,low,high) assert(low==1 and high==100); return roll end,
        }
        local goal = { AddSubGoal = function(self,id,duration,animation)
            assert(id == GOAL_COMMON_ComboTunable_SuccessAngle180 and animation == sample[2])
        end }
        RuneKnightsSwordThroatbag250091_Act15(ai,goal,{})
        if flags[1055425258] then armed = armed + 1 end
        assert(flags[1055425296])
        count = count + 1
    end
    assert(armed == sample[3])
end
print("10 periodic handoff cases and " .. count .. " HP-tier/chance cases passed")
