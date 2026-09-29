-- Hadeon's private logic goal. Normal battle actions run in private 250091_battle.
function Hadeon250090_Logic(ai)
    COMMON_Initialize(ai)
    local eventRequest = ai:GetEventRequest()

    -- Event slot 0 holds 1900 during speech, or 1901 while parked after retreat.
    -- Short goals let a cleared command and replan resume normal selection.
    if eventRequest == 1900 then
        ai:AddTopGoal(GOAL_COMMON_Wait, 0.25, TARGET_ENE_0)
        return
    elseif eventRequest == 1901 then
        ai:AddTopGoal(GOAL_COMMON_Wait, 0.25, TARGET_SELF)
        return
    end

    if COMMON_EasySetup_Initial(ai) == false then
        local eventRequest = ai:GetEventRequest()
        if eventRequest == 100 then
            ai:AddTopGoal(GOAL_COMMON_ApproachTarget, 5, POINT_INITIAL, 0.5, TARGET_SELF, true, -1)
        elseif eventRequest == 110 then
            ai:AddTopGoal(GOAL_COMMON_ApproachTarget, 5, POINT_INITIAL, 0.5, TARGET_SELF, false, -1)
        elseif eventRequest == 80 and ai:IsNpcPlayer() == true then
            local animationRequest = ai:GetEventRequest(1)
            ai:AddTopGoal(GOAL_COMMON_Wait, 0.5, TARGET_NONE)
            ai:AddTopGoal(GOAL_COMMON_WaitWithAnime, 10, 1000 + animationRequest, TARGET_NONE)
        elseif RideRequest(ai, 10, 6) then
            ai:AddTopGoal(GOAL_COMMON_Mount, 4, 1.2)
        else
            COMMON_EasySetup3(ai)
        end
    end
end

function Hadeon250090_Interupt(ai, goal)
    return false
end
