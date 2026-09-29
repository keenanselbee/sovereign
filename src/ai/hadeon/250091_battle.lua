-- Private Hadeon clone of the native 250010 battle goal.
-- Native aicommon's goal_list has no entries for these private IDs.
GOAL_RuneKnightsSwordThroatbag250091_Battle = 250091
GOAL_RuneKnightsSwordThroatbag250091_AfterAttackAct = 250092
RegisterTableGoal(GOAL_RuneKnightsSwordThroatbag250091_Battle, "RuneKnightsSwordThroatbag250091_Battle")
REGISTER_GOAL_NO_SUB_GOAL(GOAL_RuneKnightsSwordThroatbag250091_Battle, true)

-- Snapshot this once in Act15; damage during the wind-up cannot change its tier.
local function HadeonVortexTier(hp)
    if hp <= 0.25 then
        return 4, 1.50
    elseif hp <= 0.50 then
        return 3, 1.30
    elseif hp <= 0.75 then
        return 2, 1.15
    end
    return 1, 1.00
end

Goal.Initialize = function (self, ai, goal, battleActivatedCount)
    -- Diagnostic outcomes belong to the most recent Vortex attempt.
    ai:SetEventFlag(1055425275, false)
    ai:SetEventFlag(1055425276, false)
    ai:SetEventFlag(1055425277, false)
    ai:SetEventFlag(1055425278, false)
    ai:EnableUnfavorableAttackCheck(0, 3000)
    ai:EnableUnfavorableAttackCheck(0, 3001)
    ai:EnableUnfavorableAttackCheck(0, 3002)
    ai:EnableUnfavorableAttackCheck(0, 3003)
    ai:EnableUnfavorableAttackCheck(0, 3004)
    ai:EnableUnfavorableAttackCheck(0, 3005)
    ai:EnableUnfavorableAttackCheck(0, 3006)
    ai:EnableUnfavorableAttackCheck(0, 3007)
    ai:EnableUnfavorableAttackCheck(0, 3008)
    ai:EnableUnfavorableAttackCheck(0, 3009)
    ai:EnableUnfavorableAttackCheck(0, 3010)
    ai:EnableUnfavorableAttackCheck(0, 3011)
    ai:EnableUnfavorableAttackCheck(0, 3012)
    ai:EnableUnfavorableAttackCheck(0, 3013)
    ai:EnableUnfavorableAttackCheck(0, 3014)
    ai:EnableUnfavorableAttackCheck(0, 3015)
    ai:EnableUnfavorableAttackCheck(0, 3016)
    ai:EnableUnfavorableAttackCheck(0, 3017)
    ai:EnableUnfavorableAttackCheck(0, 3018)
    ai:EnableUnfavorableAttackCheck(0, 3019)
    ai:EnableUnfavorableAttackCheck(0, 3020)
    ai:EnableUnfavorableAttackCheck(0, 3021)
    ai:EnableUnfavorableAttackCheck(0, 3024)
    ai:EnableUnfavorableAttackCheck(0, 3025)
    ai:EnableUnfavorableAttackCheck(0, 3026)
    ai:EnableUnfavorableAttackCheck(0, 3027)
    ai:EnableUnfavorableAttackCheck(0, 3028)
    ai:EnableUnfavorableAttackCheck(0, 3030)
    ai:EnableUnfavorableAttackCheck(0, 3031)
    ai:EnableUnfavorableAttackCheck(0, 3032)
    ai:EnableUnfavorableAttackCheck(0, 3033)
end

Goal.Activate = function (self, ai, goal)
    if ai:IsEventFlag(1055425296) then
        -- The battle goal was reactivated after queuing a private Vortex route.
        ai:SetEventFlag(1055425297, true)
    end
    -- A completed/interrupted action must not leave a Vortex relocation armed.
    ai:SetEventFlag(1055425258, false)
    -- The event leaves this request queued. Consume it only when battle chooses
    -- another action, after the previous subgoals have finished.
    if ai:IsEventFlag(1055425253) then
        ai:SetEventFlag(1055425290, true)
        -- These flags observe battle state while a request is outstanding.
        -- The map event clears them at the next timer cycle.
        local combatActive = ai:IsEventFlag(1055422933)
        local selfAlive = ai:GetHpRate(TARGET_SELF) > 0
        local targetAlive = ai:GetHpRate(TARGET_ENE_0) > 0
        local speechHold = ai:IsEventFlag(1055422946) or ai:IsEventFlag(1055422947)
        -- IsFinishAttack is observed only: it remains false at valid battle
        -- activations in game and must not prevent this action-boundary handoff.
        local attackFinished = ai:IsFinishAttack()
        local throwing = ai:IsThrowing()
        if not combatActive then ai:SetEventFlag(1055425295, true) end
        if not selfAlive or not targetAlive then ai:SetEventFlag(1055425294, true) end
        if speechHold then ai:SetEventFlag(1055425293, true) end
        if not attackFinished then ai:SetEventFlag(1055425291, true) end
        if throwing then ai:SetEventFlag(1055425292, true) end
        if ai:IsEventFlag(1055425254) or
            (combatActive and selfAlive and targetAlive and
             not speechHold and not throwing) then
            ai:SetEventFlag(1055425254, true)
            goal:AddSubGoal(GOAL_COMMON_Wait, 0.25, TARGET_ENE_0)
            return
        end
    end

    Init_Pseudo_Global(ai, goal)
    local probabilities = {}
    local acts = {}
    local paramTbls = {}
    Common_Clear_Param(probabilities, acts, paramTbls)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:DeleteObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5039)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14647)
    ai:AddObserveSpecialEffectAttribute(TARGET_ENE_0, 51)
    local distanceEnemy = ai:GetDist(TARGET_ENE_0)
    local distanceYEnemy = ai:GetDistY(TARGET_ENE_0)
    local hpRatioSelf = ai:GetHpRate(TARGET_SELF)
    local random = ai:GetRandam_Int(1, 100)
    local distanceFriend = ai:GetDist(TARGET_FRI_0)
    local paramDoAdmire = ai:GetExcelParam(AI_EXCEL_THINK_PARAM_TYPE__thinkAttr_doAdmirer)
    local eventRequest = ai:GetEventRequest()
    local hasEffect14640 = ai:HasSpecialEffectId(TARGET_SELF, 14640)
    local hasEffect14641 = ai:HasSpecialEffectId(TARGET_SELF, 14641)
    local hasEffect14642 = ai:HasSpecialEffectId(TARGET_SELF, 14642)
    local distanceEnemy_2 = ai:GetDist(TARGET_ENE_0)
    local distanceYEnemy_2 = ai:GetDistY(TARGET_ENE_0)
    local hpRatioSelf_2 = ai:GetHpRate(TARGET_SELF)
    local random_2 = ai:GetRandam_Int(1, 100)
    local paramDoAdmire_2 = ai:GetExcelParam(AI_EXCEL_THINK_PARAM_TYPE__thinkAttr_doAdmirer)
    local eventRequest_2 = ai:GetEventRequest()
    if paramDoAdmire_2 == 1 and ai:GetTeamOrder(ORDER_TYPE_Role) == ROLE_TYPE_Kankyaku or paramDoAdmire_2 == 1 and ai:GetTeamOrder(ORDER_TYPE_Role) == ROLE_TYPE_Torimaki then
        if distanceEnemy_2 >= 15 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 80
                probabilities[23] = 0
            else
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 10 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 80
                probabilities[23] = 0
            else
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 7.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 10
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 70
                probabilities[23] = 0
            else
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 10
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 70
                probabilities[23] = 0
            else
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 4.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 10
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 20
                probabilities[7] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 70
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            else
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 80
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 3 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 20
                probabilities[4] = 0
                probabilities[6] = 20
                probabilities[7] = 0
                probabilities[20] = 0
                probabilities[21] = 20
                probabilities[22] = 40
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 2 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 20
                probabilities[2] = 0
                probabilities[3] = 20
                probabilities[4] = 0
                probabilities[6] = 20
                probabilities[7] = 0
                probabilities[20] = 0
                probabilities[21] = 20
                probabilities[22] = 20
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
            probabilities[1] = 20
            probabilities[2] = 0
            probabilities[3] = 20
            probabilities[4] = 0
            probabilities[6] = 0
            probabilities[7] = 20
            probabilities[20] = 0
            probabilities[21] = 40
            probabilities[22] = 0
            probabilities[23] = 0
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[20] = 0
            probabilities[21] = 100
            probabilities[22] = 0
            probabilities[23] = 0
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[20] = 0
            probabilities[21] = 100
            probabilities[22] = 0
            probabilities[23] = 0
        else
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[20] = 100
            probabilities[21] = 0
            probabilities[22] = 0
            probabilities[23] = 0
        end
    elseif ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
        if distanceEnemy_2 >= 15 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 0
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 10 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 0
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 7.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 50
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 10
                probabilities[5] = 10
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 100
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 4.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 40
                        probabilities[2] = 100
                        probabilities[3] = 30
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 0
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 0
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 40
                        probabilities[2] = 0
                        probabilities[3] = 30
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 0
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 0
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 40
                    probabilities[2] = 100
                    probabilities[3] = 30
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 0
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 0
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 40
                    probabilities[2] = 0
                    probabilities[3] = 30
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 0
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 0
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 70
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 0
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 3.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 25
                        probabilities[2] = 100
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 25
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 25
                        probabilities[2] = 0
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 25
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 25
                    probabilities[2] = 100
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 25
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 25
                    probabilities[2] = 0
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 25
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 70
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 1 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 15
                        probabilities[2] = 100
                        probabilities[3] = 5
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 10
                        probabilities[7] = 15
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 5
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 20
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 15
                        probabilities[2] = 0
                        probabilities[3] = 5
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 10
                        probabilities[7] = 15
                        probabilities[10] = 100
                        probabilities[11] = 0
                        probabilities[12] = 100
                        probabilities[14] = 5
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 20
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 15
                    probabilities[2] = 100
                    probabilities[3] = 5
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 10
                    probabilities[7] = 15
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 5
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 20
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 15
                    probabilities[2] = 0
                    probabilities[3] = 5
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 10
                    probabilities[7] = 15
                    probabilities[10] = 100
                    probabilities[11] = 0
                    probabilities[12] = 100
                    probabilities[14] = 5
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 20
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 40
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 40
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 20
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                probabilities[1] = 20
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 25
                probabilities[7] = 25
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 10
                probabilities[15] = 100
                probabilities[20] = 0
                probabilities[21] = 25
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[1] = 20
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 25
                probabilities[7] = 25
                probabilities[10] = 0
                probabilities[11] = 100
                probabilities[12] = 100
                probabilities[14] = 10
                probabilities[20] = 0
                probabilities[21] = 25
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
            probabilities[1] = 70
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[10] = 0
            probabilities[11] = 100
            probabilities[12] = 100
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 30
            probabilities[23] = 0
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 70
            probabilities[7] = 0
            probabilities[10] = 0
            probabilities[11] = 100
            probabilities[12] = 100
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 30
            probabilities[23] = 0
        else
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[10] = 0
            probabilities[11] = 100
            probabilities[12] = 100
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 100
            probabilities[23] = 0
        end
    elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
        if ai:GetHpRate(TARGET_SELF) < 0.6 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[13] = 100
            else
                probabilities[20] = 100
            end
        elseif distanceEnemy_2 >= 15 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 10 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 7.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 40
                probabilities[5] = 40
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 20
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                probabilities[1] = 50
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 10
                probabilities[5] = 10
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[20] = 100
                probabilities[21] = 0
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 4.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 40
                        probabilities[2] = 100
                        probabilities[3] = 30
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 0
                        probabilities[14] = 0
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 40
                        probabilities[2] = 0
                        probabilities[3] = 30
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 0
                        probabilities[14] = 0
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 40
                    probabilities[2] = 100
                    probabilities[3] = 30
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 0
                    probabilities[14] = 0
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 40
                    probabilities[2] = 0
                    probabilities[3] = 30
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 0
                    probabilities[14] = 0
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 70
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 3.5 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 25
                        probabilities[2] = 100
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 25
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 25
                        probabilities[2] = 0
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 0
                        probabilities[7] = 25
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 25
                    probabilities[2] = 100
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 25
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 25
                    probabilities[2] = 0
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 0
                    probabilities[7] = 25
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 70
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif distanceEnemy_2 >= 1 then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
                if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                    if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                        probabilities[1] = 15
                        probabilities[2] = 100
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 20
                        probabilities[7] = 15
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                        probabilities[1] = 15
                        probabilities[2] = 0
                        probabilities[3] = 10
                        probabilities[4] = 0
                        probabilities[5] = 0
                        probabilities[6] = 20
                        probabilities[7] = 15
                        probabilities[14] = 10
                        probabilities[15] = 100
                        probabilities[20] = 0
                        probabilities[21] = 0
                        probabilities[22] = 30
                        probabilities[23] = 0
                    end
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                    probabilities[1] = 15
                    probabilities[2] = 100
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 20
                    probabilities[7] = 15
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                elseif ai:HasSpecialEffectId(TARGET_SELF, 14606) == false then
                    probabilities[1] = 15
                    probabilities[2] = 0
                    probabilities[3] = 10
                    probabilities[4] = 0
                    probabilities[5] = 0
                    probabilities[6] = 20
                    probabilities[7] = 15
                    probabilities[14] = 10
                    probabilities[20] = 0
                    probabilities[21] = 0
                    probabilities[22] = 30
                    probabilities[23] = 0
                end
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
                probabilities[1] = 70
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 30
                probabilities[23] = 0
            elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 40
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 40
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 20
                probabilities[23] = 0
            else
                probabilities[1] = 0
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 0
                probabilities[7] = 0
                probabilities[14] = 0
                probabilities[20] = 0
                probabilities[21] = 0
                probabilities[22] = 100
                probabilities[23] = 0
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 100) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14607) == true then
                probabilities[1] = 20
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 25
                probabilities[7] = 20
                probabilities[14] = 10
                probabilities[15] = 100
                probabilities[20] = 0
                probabilities[21] = 25
                probabilities[22] = 0
                probabilities[23] = 0
            else
                probabilities[1] = 20
                probabilities[2] = 0
                probabilities[3] = 0
                probabilities[4] = 0
                probabilities[5] = 0
                probabilities[6] = 25
                probabilities[7] = 20
                probabilities[14] = 10
                probabilities[20] = 0
                probabilities[21] = 25
                probabilities[22] = 0
                probabilities[23] = 0
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 100) then
            probabilities[1] = 70
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 30
            probabilities[23] = 0
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 100) then
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 70
            probabilities[7] = 0
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 30
            probabilities[23] = 0
        else
            probabilities[1] = 0
            probabilities[2] = 0
            probabilities[3] = 0
            probabilities[4] = 0
            probabilities[5] = 0
            probabilities[6] = 0
            probabilities[7] = 0
            probabilities[14] = 0
            probabilities[20] = 0
            probabilities[21] = 0
            probabilities[22] = 100
            probabilities[23] = 0
        end
    end
    local vortexTier, vortexWeight = HadeonVortexTier(hpRatioSelf)
    probabilities[15] = probabilities[15] * vortexWeight
    -- 3016 is the native sustained flame-breath route. Scale only its
    -- initial selection weight; existing combo follow-ups stay native.
    probabilities[10] = probabilities[10] * 0.85
    probabilities[1] = SetCoolTime(ai, goal, 3000, 10, probabilities[1], 1)
    probabilities[2] = SetCoolTime(ai, goal, 3003, 10, probabilities[2], 1)
    probabilities[3] = SetCoolTime(ai, goal, 3004, 10, probabilities[3], 1)
    probabilities[4] = SetCoolTime(ai, goal, 3005, 10, probabilities[4], 1)
    probabilities[5] = SetCoolTime(ai, goal, 3006, 10, probabilities[5], 1)
    probabilities[6] = SetCoolTime(ai, goal, 3007, 10, probabilities[6], 1)
    probabilities[7] = SetCoolTime(ai, goal, 3008, 10, probabilities[7], 1)
    probabilities[10] = SetCoolTime(ai, goal, 3016, 20, probabilities[10], 1)
    probabilities[11] = SetCoolTime(ai, goal, 3018, 20, probabilities[11], 1)
    probabilities[12] = SetCoolTime(ai, goal, 3021, 20, probabilities[12], 1)
    probabilities[13] = SetCoolTime(ai, goal, 3022, 1, probabilities[13], 1)
    probabilities[14] = SetCoolTime(ai, goal, 3025, 15, probabilities[14], 1)
    probabilities[15] = SetCoolTime(ai, goal, 3028, 15, probabilities[15], 1)
    -- All speed variants share the native attack's cooldown, even across HP tiers.
    probabilities[15] = SetCoolTime(ai, goal, 3030, 15, probabilities[15], 1)
    probabilities[15] = SetCoolTime(ai, goal, 3031, 15, probabilities[15], 1)
    probabilities[15] = SetCoolTime(ai, goal, 3032, 15, probabilities[15], 1)
    probabilities[15] = SetCoolTime(ai, goal, 3033, 15, probabilities[15], 1)
    acts[1] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act01)
    acts[2] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act02)
    acts[3] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act03)
    acts[4] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act04)
    acts[5] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act05)
    acts[6] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act06)
    acts[7] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act07)
    acts[10] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act10)
    acts[11] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act11)
    acts[12] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act12)
    acts[13] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act13)
    acts[14] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act14)
    acts[15] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act15)
    acts[20] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act20)
    acts[21] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act21)
    acts[22] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act22)
    acts[23] = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_Act23)
    local actAfter = REGIST_FUNC(ai, goal, RuneKnightsSwordThroatbag250091_ActAfter_AdjustSpace)
    Common_Battle_Activate(ai, goal, probabilities, acts, actAfter, paramTbls)
end

function RuneKnightsSwordThroatbag250091_Act01(ai, goal, paramTbl)
    local stopDist = 5 - ai:GetMapHitRadius(TARGET_SELF)
    local canRunDist = stopDist + 0
    local forceRunMinDist = stopDist + 10
    local runProbability = 70
    local guardProbability = 100
    local walkLife = 3
    local runLife = 3
    Approach_Act_Flex(ai, goal, stopDist, canRunDist, forceRunMinDist, runProbability, guardProbability, walkLife, runLife)
    local animationId = 3000
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act02(ai, goal, paramTbl)
    local f4_local0 = 5.5 - ai:GetMapHitRadius(TARGET_SELF)
    local f4_local1 = f4_local0 + 0
    local f4_local2 = f4_local0 + 10
    local f4_local3 = 70
    local f4_local4 = 100
    local f4_local5 = 3
    local f4_local6 = 3
    local animationId = 3003
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act03(ai, goal, paramTbl)
    local f5_local0 = 5 - ai:GetMapHitRadius(TARGET_SELF)
    local f5_local1 = f5_local0 + 0
    local f5_local2 = f5_local0 + 10
    local f5_local3 = 0
    local f5_local4 = 100
    local f5_local5 = 3
    local f5_local6 = 3
    local animationId = 3004
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act04(ai, goal, paramTbl)
    local stopDist = 10 - ai:GetMapHitRadius(TARGET_SELF)
    local canRunDist = stopDist + 0
    local forceRunMinDist = stopDist + 10
    local runProbability = 70
    local guardProbability = 100
    local walkLife = 3
    local runLife = 3
    Approach_Act_Flex(ai, goal, stopDist, canRunDist, forceRunMinDist, runProbability, guardProbability, walkLife, runLife)
    local animationId = 3005
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act05(ai, goal, paramTbl)
    local stopDist = 10 - ai:GetMapHitRadius(TARGET_SELF)
    local canRunDist = stopDist + 0
    local forceRunMinDist = stopDist + 10
    local runProbability = 70
    local guardProbability = 100
    local walkLife = 3
    local runLife = 3
    Approach_Act_Flex(ai, goal, stopDist, canRunDist, forceRunMinDist, runProbability, guardProbability, walkLife, runLife)
    local animationId = 3006
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act06(ai, goal, paramTbl)
    local f8_local0 = 3.5 - ai:GetMapHitRadius(TARGET_SELF)
    local f8_local1 = f8_local0 + 0
    local f8_local2 = f8_local0 + 10
    local f8_local3 = 0
    local f8_local4 = 100
    local f8_local5 = 3
    local f8_local6 = 3
    local animationId = 3007
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act07(ai, goal, paramTbl)
    local f9_local0 = 4.5 - ai:GetMapHitRadius(TARGET_SELF)
    local f9_local1 = f9_local0 + 0
    local f9_local2 = f9_local0 + 10
    local f9_local3 = 0
    local f9_local4 = 100
    local f9_local5 = 3
    local f9_local6 = 3
    local animationId = 3008
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act10(ai, goal, paramTbl)
    local f10_local0 = 99 - ai:GetMapHitRadius(TARGET_SELF)
    local f10_local1 = f10_local0 + 0
    local f10_local2 = f10_local0 + 10
    local f10_local3 = 0
    local f10_local4 = 100
    local f10_local5 = 3
    local f10_local6 = 3
    local animationId = 3016
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act11(ai, goal, paramTbl)
    local f11_local0 = 99 - ai:GetMapHitRadius(TARGET_SELF)
    local f11_local1 = f11_local0 + 0
    local f11_local2 = f11_local0 + 10
    local f11_local3 = 0
    local f11_local4 = 100
    local f11_local5 = 3
    local f11_local6 = 3
    local animationId = 3018
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act12(ai, goal, paramTbl)
    local stopDist = 99 - ai:GetMapHitRadius(TARGET_SELF)
    local canRunDist = stopDist + 0
    local forceRunMinDist = stopDist + 10
    local runProbability = 70
    local guardProbability = 100
    local walkLife = 3
    local runLife = 3
    Approach_Act_Flex(ai, goal, stopDist, canRunDist, forceRunMinDist, runProbability, guardProbability, walkLife, runLife)
    local animationId = 3021
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act13(ai, goal, paramTbl)
    local f13_local0 = 99 - ai:GetMapHitRadius(TARGET_SELF)
    local f13_local1 = f13_local0 + 0
    local f13_local2 = f13_local0 + 10
    local f13_local3 = 0
    local f13_local4 = 100
    local f13_local5 = 3
    local f13_local6 = 3
    local animationId = 3022
    local animationId_2 = 3023
    local f13_local9 = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 360
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    if ai:HasSpecialEffectId(TARGET_SELF, 14602) == true then
        goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 15, animationId, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
    elseif ai:HasSpecialEffectId(TARGET_SELF, 14603) == true then
        goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 15, animationId_2, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
    end
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act14(ai, goal, paramTbl)
    local f14_local0 = 4.5 - ai:GetMapHitRadius(TARGET_SELF)
    local f14_local1 = f14_local0 + 0
    local f14_local2 = f14_local0 + 10
    local f14_local3 = 0
    local f14_local4 = 100
    local f14_local5 = 3
    local f14_local6 = 3
    local animationId = 3025
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act15(ai, goal, paramTbl)
    ai:SetEventFlag(1055425296, false)
    ai:SetEventFlag(1055425297, false)
    local f15_local0 = 4.5 - ai:GetMapHitRadius(TARGET_SELF)
    local f15_local1 = f15_local0 + 0
    local f15_local2 = f15_local0 + 10
    local f15_local3 = 0
    local f15_local4 = 100
    local f15_local5 = 3
    local f15_local6 = 3
    local tier, weight = HadeonVortexTier(ai:GetHpRate(TARGET_SELF))
    local animationId = 3029 + tier
    ai:SetEventFlag(1055425275, false)
    ai:SetEventFlag(1055425276, false)
    ai:SetEventFlag(1055425277, false)
    ai:SetEventFlag(1055425278, false)
    local chances = {25, 42, 58, 75}
    ai:SetEventFlag(1055425258, ai:GetRandam_Int(1, 100) <= chances[tier])
    local successDist = 5 - ai:GetMapHitRadius(TARGET_SELF) + 999
    local turnTime = 0
    local turnFaceAngle = 0
    goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, animationId, TARGET_ENE_0, successDist, turnTime, turnFaceAngle, 0, 0)
    ai:SetEventFlag(1055425296, true)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act20(ai, goal, paramTbl)
    local distanceEnemy = ai:GetDist(TARGET_ENE_0)
    if distanceEnemy >= 10 then
        goal:AddSubGoal(GOAL_COMMON_ApproachTarget, ai:GetRandam_Int(2, 3), TARGET_ENE_0, 5, TARGET_SELF, false, 9910)
    else
        goal:AddSubGoal(GOAL_COMMON_ApproachTarget, ai:GetRandam_Int(2, 3), TARGET_ENE_0, 5, TARGET_ENE_0, true, 9910)
    end
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act21(ai, goal, paramTbl)
    local lineWidth = ai:GetMapHitRadius(TARGET_SELF)
    if ai:GetExistMeshOnLineDistEx(TARGET_SELF, AI_DIR_TYPE_B, 2, lineWidth, 0) >= 2 then
        goal:AddSubGoal(GOAL_COMMON_LeaveTarget, 2, TARGET_ENE_0, 5, TARGET_ENE_0, false, 9910)
    else
        goal:AddSubGoal(GOAL_COMMON_SidewayMove, ai:GetRandam_Float(2, 2.5), TARGET_ENE_0, ai:GetRandam_Int(0, 1), ai:GetRandam_Int(30, 45), true, true, 9910)
    end
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act22(ai, goal, paramTbl)
    goal:AddSubGoal(GOAL_COMMON_SidewayMove, ai:GetRandam_Float(1.5, 2.5), TARGET_ENE_0, ai:GetRandam_Int(0, 1), ai:GetRandam_Int(30, 45), true, true, 9910)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_Act23(ai, goal, paramTbl)
    goal:AddSubGoal(GOAL_COMMON_Turn, 2.5, TARGET_ENE_0, 90, 9910, 0)
    GetWellSpace_Odds = 0
    return GetWellSpace_Odds
end

function RuneKnightsSwordThroatbag250091_ActAfter_AdjustSpace(ai, goal, paramTbl)
    goal:AddSubGoal(GOAL_RuneKnightsSwordThroatbag250091_AfterAttackAct, 10)
end

Goal.Update = function (self, ai, goal)
    return Update_Default_NoSubGoal(self, ai, goal)
end

Goal.Terminate = function (self, ai, goal)
end

Goal.Interrupt = function (self, ai, goal)
    local distanceEnemy = ai:GetDist(TARGET_ENE_0)
    local f23_local1 = 5 - ai:GetMapHitRadius(TARGET_SELF)
    local turnTime = 0
    local turnFaceAngle = 0
    local random = ai:GetRandam_Int(1, 100)
    local hpRatioSelf = ai:GetHpRate(TARGET_SELF)
    local paramDoAdmire = ai:GetExcelParam(AI_EXCEL_THINK_PARAM_TYPE__thinkAttr_doAdmirer)
    local distanceFriend = ai:GetDist(TARGET_FRI_0)
    local hitRadius = ai:GetMapHitRadius(TARGET_SELF)
    local prevTargetingState = ai:GetPrevTargetState()
    local f23_local10 = ai:AddObserveSpecialEffectAttribute(TARGET_ENE_0, PLAN_SP_EFFECT_FALL_FROM_HORSE)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5025)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5026)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5027)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5028)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5029)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5030)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5031)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5032)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5033)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5034)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5035)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5036)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5037)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 5038)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14610)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14611)
    ai:AddObserveSpecialEffectAttribute(TARGET_SELF, 14612)
    if ai:IsLadderAct(TARGET_SELF) then
        return false
    end
    if ai:HasSpecialEffectId(TARGET_SELF, 5110) == true or ai:HasSpecialEffectAttribute(TARGET_SELF, SP_EFFECT_TYPE_ILLNESS) == true then
        return false
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:HasSpecialEffectId(TARGET_SELF, 14647) == true then
        goal:ClearSubGoal()
        goal:AddSubGoal(GOAL_COMMON_ApproachTarget, 1.5, TARGET_ENE_0, 1, TARGET_SELF, true, -1, 0, 0, 0)
        return true
    end
    if ai:IsInterupt(INTERUPT_UseItem) and ai:HasSpecialEffectId(TARGET_SELF, 5039) == false then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
            if random <= 80 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 40 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
                return true
            elseif random <= 80 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
                return true
            else
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ApproachTarget, 3, TARGET_ENE_0, 5, TARGET_SELF, false, 9910)
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 15) then
            if random <= 80 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ApproachTarget, 3, TARGET_ENE_0, 5, TARGET_SELF, false, 9910)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_Shoot) then
        if ai:HasSpecialEffectId(TARGET_SELF, 5039) == false then
            if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 7.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14606) == true then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3003, TARGET_ENE_0, 999, 0, 0)
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 30 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
                return true
            elseif random <= 60 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
                return true
            else
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ApproachTarget, 3, TARGET_ENE_0, 5, TARGET_SELF, false, 9910)
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 15) then
            if random <= 80 then
                goal:ClearSubGoal()
                goal:AddSubGoal(GOAL_COMMON_ApproachTarget, 3, TARGET_ENE_0, 5, TARGET_SELF, false, 9910)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_SuccessGuard) and ai:HasSpecialEffectId(TARGET_SELF, 5039) == false and ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
        if random <= 80 then
            goal:ClearSubGoal()
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3003, TARGET_ENE_0, 999, 0, 0)
            return true
        else
            return true
        end
    end
    if ai:IsInterupt(INTERUPT_Damaged) and ai:HasSpecialEffectId(TARGET_SELF, 5039) == false and ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
        if random <= 30 then
            goal:ClearSubGoal()
            goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3007, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
            return true
        elseif random <= 60 then
            goal:ClearSubGoal()
            goal:AddSubGoal(GOAL_COMMON_ComboTunable_SuccessAngle180, 10, 3008, TARGET_ENE_0, 999, turnTime, turnFaceAngle, 0, 0)
            return true
        elseif random <= 80 then
            goal:ClearSubGoal()
            goal:AddSubGoal(GOAL_COMMON_SidewayMove, ai:GetRandam_Float(1.5, 2.5), TARGET_ENE_0, ai:GetRandam_Int(0, 1), ai:GetRandam_Int(30, 45), true, true, 9910)
            return true
        else
            return true
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5025) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 60 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3001, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3007, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 60 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3001, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3007, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5026) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 60 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if random <= 60 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3002, TARGET_ENE_0, 999, 0, 0)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5027) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 20 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3004, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 40 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3007, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3008, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 20 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3004, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 40 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3007, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3008, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 60 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if random <= 60 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5028) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5029) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5030) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 50 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 60 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3002, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5031) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 60 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if random <= 60 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5032) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 50 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 80 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5033) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if ai:HasSpecialEffectId(TARGET_ENE_0, 51) == true then
                    if random <= 10 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 20 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3004, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                elseif ai:HasSpecialEffectId(TARGET_ENE_0, 51) == false then
                    if random <= 50 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                        return true
                    elseif random <= 70 then
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3004, TARGET_ENE_0, 999, 0, 0)
                        return true
                    else
                        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                        return true
                    end
                end
            elseif ai:HasSpecialEffectId(TARGET_SELF, 14600) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3000, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3004, TARGET_ENE_0, 999, 0, 0)
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3002, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5034) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if random <= 60 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 40 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5035) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if random <= 60 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 40 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5036) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if random <= 60 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 40 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5037) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 4.5) then
            if random <= 60 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3025, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 40 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(5038) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
            if random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3016, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            goal:AddSubGoal(GOAL_COMMON_ApproachTarget, ai:GetRandam_Int(2, 3), TARGET_ENE_0, 5, TARGET_ENE_0, true, 9910)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 15) then
            goal:AddSubGoal(GOAL_COMMON_ApproachTarget, ai:GetRandam_Int(2, 3), TARGET_ENE_0, 5, TARGET_ENE_0, true, 9910)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) then
            goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
            return true
        end
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(14610) and ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 360, 180, 15) then
        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
        return true
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(14611) and ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 360, 180, 4.5) then
        goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3026, TARGET_ENE_0, 999, 0, 0)
        return true
    end
    if ai:IsInterupt(INTERUPT_ActivateSpecialEffect) and ai:GetSpecialEffectActivateInterruptId(14612) then
        if ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 5) then
            return true
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_F, 120, 180, 10) then
            if random <= 20 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3005, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 40 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3006, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_L, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_R, 120, 180, 5) then
            if ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
                if random <= 50 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                    return true
                elseif random <= 80 then
                    goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                    return true
                else
                    return true
                end
            end
        elseif ai:IsInsideTargetCustom(TARGET_SELF, TARGET_ENE_0, AI_DIR_TYPE_B, 120, 180, 5) and ai:HasSpecialEffectId(TARGET_SELF, 14601) == true then
            if random <= 50 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3018, TARGET_ENE_0, 999, 0, 0)
                return true
            elseif random <= 80 then
                goal:AddSubGoal(GOAL_COMMON_ComboRepeat_SuccessAngle180, 10, 3021, TARGET_ENE_0, 999, 0, 0)
                return true
            else
                return true
            end
        end
    end
    return false
end

RegisterTableGoal(GOAL_RuneKnightsSwordThroatbag250091_AfterAttackAct, "RuneKnightsSwordThroatbag250091_AfterAttackAct")
REGISTER_GOAL_NO_SUB_GOAL(GOAL_RuneKnightsSwordThroatbag250091_AfterAttackAct, true)

Goal.Activate = function (self, ai, goal)
end

Goal.Update = function (self, ai, goal)
    return Update_Default_NoSubGoal(self, ai, goal)
end

