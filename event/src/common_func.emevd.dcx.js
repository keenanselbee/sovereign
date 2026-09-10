// ==EMEVD==
// @docs    er-common.emedf.json
// @compress    DCX_KRAK
// @game    Sekiro
// @string    ""
// @linked    []
// @version    3.5
// ==/EMEVD==

// 【共通】特殊待機_領域判定 -- [Common] Special standby_Area judgment
$Event(90005200, Restart, function(chrEntityId, animationId, animationId2, areaEntityId, timeSeconds, value, value2, value3, value4) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    areaChrSp &= InArea(10000, areaEntityId)
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_距離判定 -- [Common] Special standby_Distance judgment
$Event(90005201, Restart, function(chrEntityId, animationId, animationId2, targetDistance, timeSeconds, value, value2, value3, value4) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    areaChrSp &= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1)
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_領域＋距離判定 -- [Common] Special standby_area + distance judgment
$Event(90005210, Restart, function(chrEntityId, animationId, animationId2, areaEntityId, targetDistance, timeSeconds, value, value2, value3, value4) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    areaChrSp &= (InArea(10000, areaEntityId) && EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1))
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_領域／距離判定 -- [Common] Special standby_area/distance judgment
$Event(90005211, Restart, function(chrEntityId, animationId, animationId2, areaEntityId, targetDistance, timeSeconds, value, value2, value3, value4) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    if (0 != areaEntityId) {
        area |= InArea(10000, areaEntityId);
    }
    area |= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    areaChrSp &= area
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_領域／距離判定Ver2 -- [Common] Special standby_area/distance judgment Ver2
$Event(90005213, Restart, function(chrEntityId, animationId, animationId2, areaEntityId, targetDistance, timeSeconds, value, value2, value3, value4, chrEntityId2, timeSeconds2) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    if (0 != areaEntityId) {
        area |= InArea(10000, areaEntityId);
    }
    cond = SpecialStandbyEndedFlag(chrEntityId2);
    area |= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1) || cond;
    areaChrSp &= area
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        if (!cond.Passed) {
            WaitFixedTimeSeconds(timeSeconds);
        } else {
            WaitFixedTimeSeconds(timeSeconds2);
        }
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_戦闘状態判定 -- [Common] Special standby_Combat status determination
$Event(90005220, Restart, function(chrEntityId, animationId, animationId2, timeSeconds, value, value2, value3) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp &= CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
    if (value2 != 0) {
        chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
    }
    if (value3 != 0) {
        chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    chrSp &= chr && cond;
    WaitFor(
        chrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】特殊待機_ダメージ判定 -- [Common] Special standby_Damage judgment
$Event(90005221, Restart, function(chrEntityId, animationId, animationId2, timeSeconds, value) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || (CharacterHasSpEffect(chrEntityId, 481)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90110)
                && !CharacterHasSpEffect(chrEntityId, 90160))
            || (CharacterHasSpEffect(chrEntityId, 482)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90120)
                && !CharacterHasSpEffect(chrEntityId, 90160)
                && !CharacterHasSpEffect(chrEntityId, 90162))
            || (CharacterHasSpEffect(chrEntityId, 483)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90140)
                && !CharacterHasSpEffect(chrEntityId, 90160)
                && !CharacterHasSpEffect(chrEntityId, 90161))
            || (CharacterHasSpEffect(chrEntityId, 484)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90130)
                && !CharacterHasSpEffect(chrEntityId, 90161)
                && !CharacterHasSpEffect(chrEntityId, 90162))
            || (CharacterHasSpEffect(chrEntityId, 487)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90150)
                && !CharacterHasSpEffect(chrEntityId, 90160)));
    WaitFixedTimeSeconds(0.1);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        SetNetworkconnectedThisEventSlot(ON);
        SetSpecialStandbyEndedFlag(chrEntityId, ON);
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】思考ロジック有効化_領域判定 -- [Common] Enabling thinking logic_Area determination
$Event(90005250, Restart, function(chrEntityId, areaEntityId, timeSeconds, animationId) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp = InArea(10000, areaEntityId) && chrSp;
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || areaChrSp
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    SetNetworkconnectedThisEventSlot(ON);
    if (areaChrSp.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        if (Signed(animationId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

// 【共通】思考ロジック有効化_距離判定 -- [Common] Enabling thought logic_Distance judgment
$Event(90005251, Restart, function(chrEntityId, targetDistance, timeSeconds, animationId) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp = EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1) && chrSp;
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || areaChrSp
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    SetNetworkconnectedThisEventSlot(ON);
    if (areaChrSp.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        if (Signed(animationId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

// 【共通】思考ロジック有効化_領域＋距離判定 -- [Common] Enabling thinking logic_Area + Distance Judgment
$Event(90005260, Restart, function(chrEntityId, areaEntityId, targetDistance, timeSeconds, animationId) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    area = InArea(10000, areaEntityId) && EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp = area && chrSp;
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || areaChrSp
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    SetNetworkconnectedThisEventSlot(ON);
    if (areaChrSp.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        if (Signed(animationId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

// 【共通】思考ロジック有効化_領域／距離判定 -- [Common] Enabling thinking logic_area/distance judgment
$Event(90005261, Restart, function(chrEntityId, areaEntityId, targetDistance, timeSeconds, animationId) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    area = InArea(10000, areaEntityId) || EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    areaChrSp = area && chrSp;
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || areaChrSp
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    SetNetworkconnectedThisEventSlot(ON);
    if (areaChrSp.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        if (Signed(animationId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

$Event(90005263, Restart, function(chrEntityId, areaEntityId, targetDistance, timeSeconds, animationId, areaEntityId2) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    area |= InArea(10000, areaEntityId);
    if (areaEntityId2 != 0) {
        area |= InArea(10000, areaEntityId2);
    }
    area |= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    areaChrSp = area && chrSp;
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || areaChrSp
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    SetNetworkconnectedThisEventSlot(ON);
    if (areaChrSp.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        area |= InArea(10000, areaEntityId);
        if (area) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

// 【共通】思考ロジック有効化_ダメージ判定 -- [Common] Activate thought logic_Damage judgment
$Event(90005271, Restart, function(chrEntityId, timeSeconds, animationId) {
    EndIf(ThisEventSlot());
    DisableCharacterAI(chrEntityId);
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || (CharacterHasSpEffect(chrEntityId, 481)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90110)
                && !CharacterHasSpEffect(chrEntityId, 90160))
            || (CharacterHasSpEffect(chrEntityId, 482)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90120)
                && !CharacterHasSpEffect(chrEntityId, 90160)
                && !CharacterHasSpEffect(chrEntityId, 90162))
            || (CharacterHasSpEffect(chrEntityId, 483)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90140)
                && !CharacterHasSpEffect(chrEntityId, 90160)
                && !CharacterHasSpEffect(chrEntityId, 90161))
            || (CharacterHasSpEffect(chrEntityId, 484)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90130)
                && !CharacterHasSpEffect(chrEntityId, 90161)
                && !CharacterHasSpEffect(chrEntityId, 90162))
            || (CharacterHasSpEffect(chrEntityId, 487)
                && !CharacterHasSpEffect(chrEntityId, 90100)
                && !CharacterHasSpEffect(chrEntityId, 90150)
                && !CharacterHasSpEffect(chrEntityId, 90160)));
    SetNetworkconnectedThisEventSlot(ON);
    if (and1.Passed) {
        WaitFixedTimeSeconds(timeSeconds);
        if (Signed(animationId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
        }
    }
L1:
    EnableCharacterAI(chrEntityId);
});

// 【共通】強敵リスポン処理 -- [Common] Strong enemy respawn processing
$Event(90005300, Restart, function(eventFlagId, chrEntityId, itemLotId, timeSeconds, value) {
    if (EventFlag(eventFlagId)) {
        if (Signed(value) != 0) {
            DisableCharacter(chrEntityId);
            ForceCharacterTreasure(chrEntityId);
            EndEvent();
        }
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndEvent();
    }
L0:
    WaitFor(CharacterRatioDead(chrEntityId));
    WaitFixedTimeSeconds(timeSeconds);
    SetEventFlagID(eventFlagId, ON);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(Signed(value) == 1);
    EndIf(Signed(itemLotId) == 0);
    AwardItemsIncludingClients(itemLotId);
    EndEvent();
});

$Event(90005301, Restart, function(eventFlagId, chrEntityId, itemLotId, timeSeconds, value) {
    if (EventFlag(eventFlagId)) {
        if (SignedAlt(value) != 0) {
            DisableCharacter(chrEntityId);
            ForceCharacterTreasure(chrEntityId);
            EndEvent();
        }
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndEvent();
    }
L0:
    WaitFor(CharacterRatioDead(chrEntityId));
    WaitFixedTimeSeconds(timeSeconds);
    SetEventFlagID(eventFlagId, ON);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(SignedAlt(value) == 1);
    EndIf(SignedAlt(itemLotId) == 0);
    AwardItemsIncludingClients(itemLotId);
    EndEvent();
});

// 【共通】制圧リスポン処理 -- [Common] Suppression response processing
$Event(90005360, Restart, function(eventFlagId, chrEntityId, itemLotId) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        EndEvent();
    }
L0:
    WaitFor(EventFlag(eventFlagId));
    DisplayBanner(TextBannerType.Unknown14);
    EndIf(!PlayerIsInOwnWorld());
    AwardItemsIncludingClients(itemLotId);
});

// 【共通】変身スライム_撃破 -- [Common] Transformation slime_defeat
$Event(90005390, Restart, function(eventFlagId, eventFlagId2, entityId, chrEntityId, value, itemLotId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId2) && CharacterDead(chrEntityId));
    WaitFixedTimeSeconds(1);
    if (Signed(value) != 0) {
        SpawnOneshotSFX(TargetEntityType.Character, entityId, 960, 601111);
    } else {
L2:
        SpawnOneshotSFX(TargetEntityType.Character, entityId, 960, 601110);
    }
L3:
    WaitFixedTimeSeconds(3);
    DisableCharacter(chrEntityId);
    EndIf(!PlayerIsInOwnWorld());
    if (Signed(itemLotId) != 0) {
        AwardItemsIncludingClients(itemLotId);
    }
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
});

// 【共通】変身スライム_変身 -- [Common] Transformation slime_Transformation
$Event(90005391, Restart, function(eventFlagId, eventFlagId2, chrEntityId, chrEntityId2, value) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        DisableCharacter(chrEntityId2);
        DisableCharacterCollision(chrEntityId2);
        EndEvent();
    }
L0:
    if (EventFlag(eventFlagId2)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        EndEvent();
    }
L1:
    DisableCharacter(chrEntityId2);
    DisableCharacterCollision(chrEntityId2);
    DisableCharacterGravity(chrEntityId2);
    DisableCharacterAI(chrEntityId2);
    EnableCharacterFadeOnEnable(chrEntityId2);
    WaitFor(CharacterDead(chrEntityId));
    EnableCharacterDefaultBackread(chrEntityId);
    EnableCharacterDefaultBackread(chrEntityId2);
    WaitFixedTimeSeconds(0.5);
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, 900, chrEntityId);
    WaitFixedTimeSeconds(0.5);
    if (Signed(value) != 0) {
        SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 900, 601101);
    } else {
L2:
        SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 900, 601100);
    }
L3:
    EnableCharacter(chrEntityId2);
    EnableCharacterGravity(chrEntityId2);
    EnableCharacterCollision(chrEntityId2);
    EnableCharacterAI(chrEntityId2);
    DisableCharacter(chrEntityId);
    DisableCharacterDefaultBackread(chrEntityId);
    DisableCharacterDefaultBackread(chrEntityId2);
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    }
});

// 【共通】ネムリコレクト_ネムリ待機 -- [Common] Nemuri collect_Nemuri standby
$Event(90005400, Restart, function(chrEntityId, spEffectId, timeSeconds, timeSeconds2, value) {
    EndIf(ThisEventSlot());
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    if (Signed(spEffectId) != 0) {
        SetSpEffect(chrEntityId, spEffectId);
    } else {
        SetSpEffect(chrEntityId, 4421);
    }
    ForceAnimationPlayback(chrEntityId, 14100, true, false, false);
    WaitFor(
        HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasSpEffect(chrEntityId, 5112));
    WaitFixedTimeFrames(1);
    if (CharacterHasSpEffect(chrEntityId, 5111)) {
        SetNetworkconnectedThisEventSlot(ON);
        if (!CharacterHasSpEffect(chrEntityId, 5112)) {
            WaitFixedTimeSeconds(timeSeconds2);
        } else {
            WaitFixedTimeSeconds(timeSeconds);
        }
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, 14102, true, false, false);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】ネムリコレクト_ネムリ取得 -- [Common] Nemuri collect_Nemuri acquisition
$Event(90005401, Restart, function(eventFlagId, chrEntityId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    SetSpEffect(chrEntityId, 4430);
    WaitFor(PlayerIsInOwnWorld() && CharacterHasSpEffect(chrEntityId, 4431));
    SetEventFlagID(eventFlagId, ON);
});

// 【共通】バディ召喚_撃破対象リスト設定 -- [Common] Buddy summon_defeat target list setting
$Event(90005410, Restart, function(eventFlagId, chrEntityId, chrEntityId2) {
    if (!EventFlag(eventFlagId)) {
        WaitFor(
            (PlayerIsInOwnWorld() && CharacterHasSpEffect(chrEntityId, 9500))
                || EventFlag(eventFlagId));
        if (PlayerIsInOwnWorld()) {
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
    }
L0:
    Unknown200471(0, 0, chrEntityId2);
    WaitFor((PlayerIsInOwnWorld() && CharacterHasSpEffect(20000, 202)) || !EventFlag(eventFlagId));
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    }
    RestartEvent();
});

// 【共通】バディ召喚_石碑SFX対応 -- [Common] Buddy summon_stone monument SFX compatible
$Event(90005411, Restart, function(assetEntityId, chrEntityId, value) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    if (value == 0) {
        WaitFixedTimeFrames(1);
    }
    CreateAssetfollowingSFX(assetEntityId, 200, 620);
    WaitFor(CharacterHasSpEffect(chrEntityId, 9502));
    DeleteAssetfollowingSFX(assetEntityId, true);
    WaitFor(CharacterHasSpEffect(chrEntityId, 9503));
    RestartEvent();
});

// 【共通】馬車_初期設定 -- [Common] Horse carriage_Initial settings
$Event(90005420, Restart, function(chrEntityId, assetEntityId, assetEntityId2, chrEntityId2, chrEntityId3, chrEntityId4, timeSeconds) {
    DisableCharacterCollision(chrEntityId);
    AttachCaravanToController(assetEntityId, chrEntityId);
    AttachAssetToAsset(assetEntityId2, assetEntityId, 151);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    SetNetworkUpdateRate(chrEntityId2, true, CharacterUpdateFrequency.AtLeastEvery5Frames);
    SetNetworkUpdateRate(chrEntityId3, true, CharacterUpdateFrequency.AlwaysUpdate);
    SetNetworkUpdateRate(chrEntityId4, true, CharacterUpdateFrequency.AlwaysUpdate);
    ConnectCharacterToCaravan(chrEntityId3, assetEntityId);
    ConnectCharacterToCaravan(chrEntityId4, assetEntityId);
    EndEvent();
    WaitFixedTimeSeconds(timeSeconds);
});

// 【共通】馬車_宝扉制御 -- [Common] Carriage_Treasure door control
$Event(90005421, Restart, function(eventFlagId, assetEntityId, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId2));
    DisableObjAct(assetEntityId, -1);
    WaitFor(CharacterHasSpEffect(eventFlagId, 11500) && !EventFlag(eventFlagId));
    EnableObjAct(assetEntityId, -1);
    WaitFor(!CharacterHasSpEffect(eventFlagId, 11500));
    RestartEvent();
});

// 【共通】馬車_宝入手 -- [Common] Carriage_Treasure acquisition
$Event(90005422, Restart, function(eventFlagId, assetEntityId, objactEventFlag) {
    if (EventFlag(eventFlagId)) {
        EnableAssetTreasure(assetEntityId);
        EndEvent();
    }
L0:
    DisableAssetTreasure(assetEntityId);
    WaitFor(
        (PlayerIsInOwnWorld() && ObjActEventFlag(objactEventFlag)) || AssetDestroyed(assetEntityId));
    WaitFixedTimeSeconds(3.2);
    EnableAssetTreasure(assetEntityId);
});

// 【共通】馬車_牽引解除_XX -- [Common] Horse carriage_traction release_XX
$Event(90005423, Restart, function(chrEntityId) {
    WaitFor(CharacterHasSpEffect(chrEntityId, 5551));
    ConnectCharacterToCaravan(chrEntityId, 0);
    ChangeCharactersCloth(chrEntityId, 20, 2);
});

// 【共通】馬車_破壊挙動 -- [Common] Horse carriage_destruction behavior
$Event(90005424, Restart, function(assetEntityId, chrEntityId, chrEntityId2, chrEntityId3, assetEntityId2) {
    WaitFor(AssetDestroyed(assetEntityId));
    ChangeCharactersCloth(chrEntityId, 20, 2);
    ChangeCharactersCloth(chrEntityId2, 20, 2);
    SetSpEffect(chrEntityId, 5551);
    SetSpEffect(chrEntityId2, 5551);
    ForceCharacterDeath(chrEntityId3, true);
    DisableAsset(assetEntityId2);
    DisableObjAct(assetEntityId2, -1);
    EnableAssetTreasure(assetEntityId);
});

$Event(90005430, Restart, function(chrEntityId) {
    EnableCharacterDefaultBackread(chrEntityId);
    SetCharacterEnableDistance(chrEntityId, 2000);
    DisableCharacterDisableOnHitUnload(chrEntityId);
    EnableDistancebasedNetworkUpdateAuthority(chrEntityId);
    DisableLockOnPoint(chrEntityId, 223);
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
    CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
    SetNetworkconnectedThisEventSlot(ON);
    EndEvent();
});

$Event(90005431, Restart, function(chrEntityId) {
    EnableCharacterDefaultBackread(chrEntityId);
    SetCharacterEnableDistance(chrEntityId, 2000);
    DisableCharacterDisableOnHitUnload(chrEntityId);
    EnableDistancebasedNetworkUpdateAuthority(chrEntityId);
    DisableLockOnPoint(chrEntityId, 221);
    DisableLockOnPoint(chrEntityId, 222);
    if (!ThisEventSlot()) {
        CreateNPCPart(chrEntityId, 30, NPCPartType.Part1, 99999, 1, 1, false, false);
    }
    SetNPCPartSEAndSFX(chrEntityId, 30, -1, 120, -1, 120, 112);
    SetNetworkconnectedThisEventSlot(ON);
    EndEvent();
});

$Event(90005432, Restart, function(chrEntityId, eventFlagId) {
    if (!EventFlag(eventFlagId)) {
        DisableCharacterGravity(chrEntityId);
        SetSpEffect(chrEntityId, 5005);
        RequestCharacterAIReplan(chrEntityId);
        WaitFixedTimeRealFrames(1);
        if (!CharacterHasSpEffect(chrEntityId, 19627)) {
            ForceAnimationPlayback(chrEntityId, 30010, true, false, false);
        }
        WaitFor(EntityInRadiusOfEntity(chrEntityId, 10000, 200, 1) || EventFlag(eventFlagId));
        if (!CharacterHasSpEffect(chrEntityId, 19627)) {
            ForceAnimationPlayback(chrEntityId, 20010, true, false, false);
        }
    }
L0:
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    EnableCharacterGravity(chrEntityId);
    SetSpEffect(chrEntityId, 5006);
    RequestCharacterAIReplan(chrEntityId);
L1:
    WaitFor(
        (!EntityInRadiusOfEntity(chrEntityId, 10000, 220, 1)
            && !EntityInRadiusOfEntity(chrEntityId, 10001, 220, 1)
            && !EntityInRadiusOfEntity(chrEntityId, 10002, 220, 1)
            && !EntityInRadiusOfEntity(chrEntityId, 10003, 220, 1)
            && !EntityInRadiusOfEntity(chrEntityId, 10004, 220, 1)
            && !EntityInRadiusOfEntity(chrEntityId, 10005, 220, 1))
            || !EventFlag(eventFlagId));
    SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    RestartEvent();
});

$Event(90005433, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3) {
    WaitFixedTimeRealFrames(1);
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && (NPCPartHP(chrEntityId, 30) <= 0 || CharacterHasSpEffect(chrEntityId, 20011126)));
    if (!CharacterHasSpEffect(chrEntityId, 20011126)) {
        if (NPCPartHP(chrEntityId, 30) <= 0) {
            if (!EventFlag(eventFlagId3)) {
                if (!EventFlag(eventFlagId2)) {
                    if (!EventFlag(eventFlagId)) {
L0:
                        SetNetworkconnectedEventFlagID(eventFlagId, ON);
                        ForceAnimationPlayback(chrEntityId, 20003, false, true, false);
                        CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
                        WaitFixedTimeSeconds(1);
                        RestartEvent();
                    }
L1:
                    SetNetworkconnectedEventFlagID(eventFlagId2, ON);
                    ForceAnimationPlayback(chrEntityId, 20003, false, true, false);
                    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
                    WaitFixedTimeSeconds(1);
                    RestartEvent();
                }
L2:
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
                WaitFixedTimeSeconds(0.1);
                RestartEvent();
            }
L3:
            ForceAnimationPlayback(chrEntityId, 20000, false, true, false);
            CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
            SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            WaitFixedTimeSeconds(1);
            RestartEvent();
        }
    }
L4:
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 9999, 1, 1, false, false);
    WaitFor(!CharacterHasSpEffect(chrEntityId, 20011126));
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 560, 1, 1, false, false);
    RestartEvent();
});

$Event(90005434, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3) {
    WaitFixedTimeRealFrames(1);
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && (NPCPartHP(chrEntityId, 31) <= 0 || CharacterHasSpEffect(chrEntityId, 20011126)));
    if (!CharacterHasSpEffect(chrEntityId, 20011126)) {
        if (NPCPartHP(chrEntityId, 31) <= 0) {
            if (!EventFlag(eventFlagId3)) {
                if (!EventFlag(eventFlagId2)) {
                    if (!EventFlag(eventFlagId)) {
L0:
                        SetNetworkconnectedEventFlagID(eventFlagId, ON);
                        ForceAnimationPlayback(chrEntityId, 20005, false, true, false);
                        CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
                        WaitFixedTimeSeconds(1);
                        RestartEvent();
                    }
L1:
                    SetNetworkconnectedEventFlagID(eventFlagId2, ON);
                    ForceAnimationPlayback(chrEntityId, 20005, false, true, false);
                    CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
                    WaitFixedTimeSeconds(1);
                    RestartEvent();
                }
L2:
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
                WaitFixedTimeSeconds(0.1);
                RestartEvent();
            }
L3:
            ForceAnimationPlayback(chrEntityId, 20001, false, true, false);
            CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
            SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            WaitFixedTimeSeconds(1);
            RestartEvent();
        }
    }
L4:
    CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 9999, 1, 1, false, false);
    WaitFor(!CharacterHasSpEffect(chrEntityId, 20011126));
    CreateNPCPart(chrEntityId, 31, NPCPartType.Part4, 560, 1, 1, false, false);
    RestartEvent();
});

$Event(90005435, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4) {
    WaitFor(CharacterBackreadStatus(chrEntityId) && CharacterHasSpEffect(chrEntityId, 20011113));
    if (!EventFlag(eventFlagId4)) {
        if (!EventFlag(eventFlagId3)) {
            if (!EventFlag(eventFlagId2)) {
                if (!EventFlag(eventFlagId)) {
L0:
                    SetNetworkconnectedEventFlagID(eventFlagId, ON);
                    WaitFixedTimeRealFrames(1);
                    RestartEvent();
                }
L1:
                SetNetworkconnectedEventFlagID(eventFlagId2, ON);
                ForceAnimationPlayback(chrEntityId, 20006, false, false, false);
                WaitFixedTimeRealFrames(1);
                RestartEvent();
            }
L2:
            SetNetworkconnectedEventFlagID(eventFlagId3, ON);
            WaitFixedTimeRealFrames(1);
            RestartEvent();
        }
L3:
        SetNetworkconnectedEventFlagID(eventFlagId4, ON);
        ForceAnimationPlayback(chrEntityId, 20006, false, false, false);
        WaitFixedTimeRealFrames(1);
        RestartEvent();
    }
L4:
    ForceAnimationPlayback(chrEntityId, 20009, false, true, false);
    SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
    WaitFixedTimeRealFrames(1);
    RestartEvent();
});

$Event(90005436, Restart, function(entityId, areaEntityId, areaEntityId2) {
    DisableNetworkSync();
    WaitFor(InArea(10000, areaEntityId) && InArea(entityId, areaEntityId2));
    SetSpEffect(10000, 20011132);
    WaitFor(!InArea(10000, areaEntityId) || !InArea(entityId, areaEntityId2));
    ClearSpEffect(10000, 20011132);
    RestartEvent();
});

$Event(90005437, Restart, function(chrEntityId, eventFlagId, eventFlagId2) {
    WaitFor(CharacterBackreadStatus(chrEntityId) && CharacterHasSpEffect(chrEntityId, 20011135));
    if (!EventFlag(eventFlagId2)) {
        if (!EventFlag(eventFlagId)) {
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
            ForceAnimationPlayback(chrEntityId, 20006, false, false, false);
            WaitFixedTimeRealFrames(1);
            RestartEvent();
        }
L2:
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
        ForceAnimationPlayback(chrEntityId, 20006, false, false, false);
        WaitFixedTimeRealFrames(1);
        RestartEvent();
    }
L3:
    ForceAnimationPlayback(chrEntityId, 20009, false, true, false);
    SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
    WaitFixedTimeRealFrames(1);
    RestartEvent();
});

// 【共通】黒き刃の末裔_ステルス -- [Common] Descendants of the Black Blade_Stealth
$Event(90005440, Default, function(eventFlagId, chrEntityId) {
    SetSpEffect(chrEntityId, 14500);
    DisableCharacterHPBarDisplay(chrEntityId);
    DisableLockOnPoint(eventFlagId, 220);
    WaitFor(
        PlayerIsInOwnWorld()
            && CharacterHasSpEffect(10000, 3245)
            && EntityInRadiusOfEntity(chrEntityId, 10000, 6, 1));
    SetEventFlagID(eventFlagId, ON);
L0:
    SetSpEffect(chrEntityId, 14501);
    SetSpEffect(chrEntityId, 14502);
    EnableCharacterHPBarDisplay(chrEntityId);
    EnableLockOnPoint(chrEntityId, 220);
    WaitFor(
        (!CharacterHasSpEffect(10000, 3245) || !EntityInRadiusOfEntity(chrEntityId, 10000, 6, 1))
            && !CharacterHasSpEffect(chrEntityId, 14503)
            && PlayerIsInOwnWorld());
    RestartEvent();
    RequestCharacterAICommand(0, 0, 0);
    EzstateInstructionRequest(0, 0, 0);
});

$Event(90005445, Restart, function(chrEntityId, animationId, animationId2, areaEntityId, timeSeconds, value, value2, value3, value4, assetEntityId) {
    if (AssetDestroyed(assetEntityId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
    if (SpecialStandbyEndedFlag(chrEntityId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    EnableAssetInvunerability(assetEntityId);
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    areaChrSp &= InArea(10000, areaEntityId)
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        DisableAssetInvunerability(assetEntityId);
        RequestAssetDestruction(assetEntityId, 1);
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    DisableAssetInvunerability(assetEntityId);
    RequestAssetDestruction(assetEntityId, 1);
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

$Event(90005446, Restart, function(chrEntityId, animationId, animationId2, targetDistance, timeSeconds, value, value2, value3, value4, assetEntityId) {
    if (AssetDestroyed(assetEntityId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
    if (SpecialStandbyEndedFlag(chrEntityId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    EnableAssetInvunerability(assetEntityId);
    ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    chrSp = (CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
        || CharacterType(10000, TargetType.Alive)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.WhitePhantom);
    areaChrSp &= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1)
        && CharacterBackreadStatus(chrEntityId)
        && (CharacterHasSpEffect(chrEntityId, 5080) || CharacterHasSpEffect(chrEntityId, 5450));
    if (!(value2 == 0 && value3 == 0 && value4 == 0)) {
        if (value2 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.Combat);
        }
        if (value3 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.ActiveAlert);
        }
        if (value4 != 0) {
            chr |= CharacterAIState(chrEntityId, AIStateType.PassiveAlert);
        }
        areaChrSp &= chr;
    }
L9:
    sp = CharacterHasSpEffect(chrEntityId, 481)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90110)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    sp2 = CharacterHasSpEffect(chrEntityId, 482)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90120)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp3 = CharacterHasSpEffect(chrEntityId, 483)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90140)
        && !CharacterHasSpEffect(chrEntityId, 90160)
        && !CharacterHasSpEffect(chrEntityId, 90161);
    sp4 = CharacterHasSpEffect(chrEntityId, 484)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90130)
        && !CharacterHasSpEffect(chrEntityId, 90161)
        && !CharacterHasSpEffect(chrEntityId, 90162);
    sp5 = CharacterHasSpEffect(chrEntityId, 487)
        && !CharacterHasSpEffect(chrEntityId, 90100)
        && !CharacterHasSpEffect(chrEntityId, 90150)
        && !CharacterHasSpEffect(chrEntityId, 90160);
    areaChrSp &= chrSp;
    WaitFor(
        areaChrSp
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified)
            || CharacterHasStateInfo(chrEntityId, 436)
            || CharacterHasStateInfo(chrEntityId, 2)
            || CharacterHasStateInfo(chrEntityId, 5)
            || CharacterHasStateInfo(chrEntityId, 6)
            || CharacterHasStateInfo(chrEntityId, 260)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        DisableAssetInvunerability(assetEntityId);
        RequestAssetDestruction(assetEntityId, 1);
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EndEvent();
    }
L0:
    DisableAssetInvunerability(assetEntityId);
    RequestAssetDestruction(assetEntityId, 1);
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

// 【共通】歩く霊廟_初期設定 -- [Common] Walking Mausoleum_Initial Settings
$Event(90005450, Restart, function(chrEntityId, assetEntityId, assetEntityId2, assetEntityId3) {
    EnableCharacterDefaultBackread(chrEntityId);
    EnableCharacterImmortality(chrEntityId);
    SetCharacterEnableDistance(chrEntityId, 2000);
    DisableCharacterDisableOnHitUnload(chrEntityId);
    EnableDistancebasedNetworkUpdateAuthority(chrEntityId);
    DisableCharacterHPBarDisplay(chrEntityId);
    AttachAssetToCharacter(chrEntityId, 100, assetEntityId);
    AttachAssetToCharacter(chrEntityId, 80, assetEntityId2);
    AttachAssetToCharacter(chrEntityId, 165, assetEntityId3);
});

// 【共通】歩く霊廟_胡坐判定 -- [Common] Walking Mausoleum_Sitting with Crossed Legs Judgment
$Event(90005451, Restart, function(chrEntityId, assetEntityId) {
    if (!ThisEventSlot()) {
        WaitFor(AssetRatioDestroyed(DestructionState.Destroyed, assetEntityId) >= 0.45);
    }
L0:
    SetSpEffect(chrEntityId, 12450);
});

// 【共通】歩く霊廟_胡坐完了判定 -- [Common] Walking Mausoleum_Sitting with Crossed Crossed Completion Judgment
$Event(90005452, Restart, function(chrEntityId, eventFlagId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterHasSpEffect(chrEntityId, 12455));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
});

// 【共通】歩く霊廟_破壊素材対応 -- [Common] Walking Mausoleum_Destructible material compatible
$Event(90005453, Restart, function(assetEntityId, assetEntityId2, dummypolyId, timeSeconds) {
    EndIf(AssetDestroyed(assetEntityId2));
    AttachAssetToCharacter(assetEntityId, dummypolyId, assetEntityId2);
    if (CharacterType(10000, TargetType.WhitePhantom)
        || CharacterType(10000, TargetType.GrayPhantom)
        || CharacterType(10000, TargetType.BluePhantom)
        || CharacterType(10000, TargetType.BlackPhantom)
        || CharacterType(10000, TargetType.Invader)
        || CharacterType(10000, TargetType.Invader2)
        || CharacterType(10000, TargetType.Invader3)) {
        EnableAssetInvunerability(assetEntityId2);
    }
L10:
    WaitFor(AssetDestroyed(assetEntityId) || CharacterHasSpEffect(assetEntityId, 12460));
    EndIf(AssetDestroyed(assetEntityId2));
    EnableAssetInvunerability(assetEntityId2);
    WaitFixedTimeSeconds(timeSeconds);
    RequestAssetDestruction(assetEntityId2, 0);
});

// 【共通】歩く霊廟_遠方待機 -- [Common] Walking Mausoleum_Long distance standby
$Event(90005454, Restart, function(chrEntityId, eventFlagId, eventFlagId2) {
    if (EventFlag(eventFlagId2)) {
        ForceAnimationPlayback(chrEntityId, 30001, true, false, false);
    }
    if (!EventFlag(eventFlagId)) {
        SetSpEffect(chrEntityId, 5005);
        RequestCharacterAIReplan(chrEntityId);
        DisableCharacterGravity(chrEntityId);
        WaitFixedTimeFrames(1);
        if (EventFlag(eventFlagId2)) {
            ForceAnimationPlayback(chrEntityId, 30001, true, false, false);
        } else {
            ForceAnimationPlayback(chrEntityId, 0, true, false, false);
        }
        WaitFor(
            EventFlag(eventFlagId)
                || (PlayerIsInOwnWorld() && EntityInRadiusOfEntity(chrEntityId, 10000, 200, 1)));
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
L0:
    SetSpEffect(chrEntityId, 5006);
    RequestCharacterAIReplan(chrEntityId);
    EnableCharacterGravity(chrEntityId);
    WaitFor(
        (PlayerIsInOwnWorld() && !EntityInRadiusOfEntity(chrEntityId, 10000, 220, 1))
            || !EventFlag(eventFlagId));
    SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    RestartEvent();
});

// 【共通】歩く霊廟_歩行時開閉禁止 -- [Common] Walking mausoleum_Do not open or close while walking
$Event(90005456, Restart, function(chrEntityId, assetEntityId, assetEntityId2, eventFlagId) {
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    DisableObjAct(assetEntityId, -1);
    DisableObjAct(assetEntityId2, -1);
    WaitFor(CharacterHasSpEffect(chrEntityId, 12455));
    EnableObjAct(assetEntityId, -1);
    EnableObjAct(assetEntityId2, -1);
});

// 【共通】歩く霊廟_天井蓋対応 -- [Common] Walking mausoleum_Ceiling cover compatible
$Event(90005457, Restart, function(chrEntityId, assetEntityId, assetEntityId2, assetEntityId3) {
    if (CharacterHasSpEffect(chrEntityId, 12455)) {
        DisableAsset(assetEntityId);
        DisableObjAct(assetEntityId2, -1);
        ReproduceAssetAnimation(assetEntityId2, 1);
        EndEvent();
    }
L0:
    AttachAssetToCharacter(chrEntityId, 100, assetEntityId);
    ReproduceAssetAnimation(assetEntityId2, 1);
    DisableObjAct(assetEntityId2, -1);
    DisableObjAct(assetEntityId3, -1);
    WaitFor(CharacterHasSpEffect(chrEntityId, 12455));
    DisableAsset(assetEntityId);
    EnableObjAct(assetEntityId3, -1);
});

// 【共通】歩く霊廟_土台安定対応 -- [Common] Walking mausoleum_Foundation stability support
$Event(90005458, Restart, function(chrEntityId, assetEntityId) {
    if (!ThisEventSlot()) {
        AttachAssetToCharacter(chrEntityId, 166, assetEntityId);
        DisableAsset(assetEntityId);
        WaitFor(CharacterHasSpEffect(chrEntityId, 12465));
    }
L0:
    EnableAsset(assetEntityId);
    SetNetworkconnectedThisEventSlot(ON);
    EndEvent();
});

// 【共通】歩く霊廟_ボスソウル複製 -- [Common] Walking Mausoleum_Boss Soul Duplication
$Event(90005459, Restart, function(chrEntityId, eventFlagId, chrEntityId2) {
    DisableCharacter(chrEntityId2);
    DisableCharacterCollision(chrEntityId2);
    DisableCharacterGravity(chrEntityId2);
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(PlayerIsInOwnWorld() && EventFlag(eventFlagId));
    EnableCharacter(chrEntityId2);
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, 270, chrEntityId);
});

// 【共通】陸ダコ_初期設定 -- [Common] Land octopus_Initial settings
$Event(90005460, Restart, function(chrEntityId) {
    WaitFor(CharacterBackreadStatus(chrEntityId));
    CreateNPCPart(chrEntityId, 60, NPCPartType.Part6, 999999999, 1, 1, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 60, 124, 124, -1, -1, -1);
});

// 【共通】陸ダコ_左触手破壊 -- [Common] Land Octopus_Left Tentacle Destruction
$Event(90005461, Restart, function(chrEntityId) {
    WaitFor(CharacterBackreadStatus(chrEntityId) && !CharacterHasSpEffect(chrEntityId, 11753));
    CreateNPCPart(chrEntityId, 10, NPCPartType.Part1, 11, 1, 1, false, false);
    CreateNPCPart(chrEntityId, 20, NPCPartType.Part2, 11, 1, 1, false, false);
    cond = cond2;
    WaitFor(
        NPCPartHP(chrEntityId, 10) <= 0
            || NPCPartHP(chrEntityId, 20) <= 0
            || (NPCPartHP(chrEntityId, 10) <= 10 && NPCPartHP(chrEntityId, 20) <= 1)
            || (NPCPartHP(chrEntityId, 10) <= 9 && NPCPartHP(chrEntityId, 20) <= 2)
            || (NPCPartHP(chrEntityId, 10) <= 8 && NPCPartHP(chrEntityId, 20) <= 3)
            || (NPCPartHP(chrEntityId, 10) <= 7 && NPCPartHP(chrEntityId, 20) <= 4)
            || (NPCPartHP(chrEntityId, 10) <= 6 && NPCPartHP(chrEntityId, 20) <= 5)
            || (NPCPartHP(chrEntityId, 10) <= 5 && NPCPartHP(chrEntityId, 20) <= 6)
            || (NPCPartHP(chrEntityId, 10) <= 4 && NPCPartHP(chrEntityId, 20) <= 7)
            || (NPCPartHP(chrEntityId, 10) <= 3 && NPCPartHP(chrEntityId, 20) <= 8)
            || (NPCPartHP(chrEntityId, 10) <= 2 && NPCPartHP(chrEntityId, 20) <= 9)
            || (NPCPartHP(chrEntityId, 10) <= 1 && NPCPartHP(chrEntityId, 20) <= 10)
            || CharacterHasSpEffect(chrEntityId, 11753));
    SetNPCPartHP(chrEntityId, 10, 0, false);
    SetNPCPartHP(chrEntityId, 20, 0, false);
    if (!CharacterHasSpEffect(chrEntityId, 11753)) {
        ForceAnimationPlayback(chrEntityId, 20001, false, false, false);
    }
    WaitFixedTimeSeconds(2);
    RestartEvent();
});

// 【共通】陸ダコ_右触手破壊 -- [Common] Land octopus_Right tentacle destroyed
$Event(90005462, Restart, function(chrEntityId) {
    WaitFor(CharacterBackreadStatus(chrEntityId) && !CharacterHasSpEffect(chrEntityId, 11752));
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 11, 1, 1, false, false);
    CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 11, 1, 1, false, false);
    WaitFor(
        NPCPartHP(chrEntityId, 30) <= 0
            || NPCPartHP(chrEntityId, 50) <= 0
            || (NPCPartHP(chrEntityId, 30) <= 10 && NPCPartHP(chrEntityId, 50) <= 1)
            || (NPCPartHP(chrEntityId, 30) <= 9 && NPCPartHP(chrEntityId, 50) <= 2)
            || (NPCPartHP(chrEntityId, 30) <= 8 && NPCPartHP(chrEntityId, 50) <= 3)
            || (NPCPartHP(chrEntityId, 30) <= 7 && NPCPartHP(chrEntityId, 50) <= 4)
            || (NPCPartHP(chrEntityId, 30) <= 6 && NPCPartHP(chrEntityId, 50) <= 5)
            || (NPCPartHP(chrEntityId, 30) <= 5 && NPCPartHP(chrEntityId, 50) <= 6)
            || (NPCPartHP(chrEntityId, 30) <= 4 && NPCPartHP(chrEntityId, 50) <= 7)
            || (NPCPartHP(chrEntityId, 30) <= 3 && NPCPartHP(chrEntityId, 50) <= 8)
            || (NPCPartHP(chrEntityId, 30) <= 2 && NPCPartHP(chrEntityId, 50) <= 9)
            || (NPCPartHP(chrEntityId, 30) <= 1 && NPCPartHP(chrEntityId, 50) <= 10));
    SetNPCPartHP(chrEntityId, 30, 0, false);
    SetNPCPartHP(chrEntityId, 50, 0, false);
    ForceAnimationPlayback(chrEntityId, 20000, false, false, false);
    WaitFixedTimeSeconds(2);
    RestartEvent();
});

// 【共通】陸ダコ_出産停止 -- [Common] Land octopus_Stop giving birth
$Event(90005463, Restart, function(eventFlagId, chrEntityId) {
    if (!ThisEventSlot()) {
        WaitFor(
            EventValue(eventFlagId, 3) >= 5
                || (HasDamageType(chrEntityId, 0, DamageType.Unspecified)
                    && !CharacterHasSpEffect(eventFlagId, 11757)));
    }
L0:
    SetSpEffect(chrEntityId, 11757);
});

// 【共通】陸ダコ_出産 -- [Common] Land octopus_birth
$Event(90005464, Restart, function(eventFlagId, chrEntityId, chrEntityId2, thresholdValue) {
    EndIf(EventValue(eventFlagId, 3) > thresholdValue);
    DisableCharacter(chrEntityId2);
    DisableCharacterCollision(chrEntityId2);
    DisableCharacterAI(chrEntityId2);
    WaitFor(
        CharacterHasSpEffect(chrEntityId, 11771)
            && EventValue(eventFlagId, 3) == thresholdValue
            && !CharacterDead(chrEntityId));
    WaitFixedTimeFrames(1);
    IncrementEventValue(eventFlagId, 3, 5);
    EnableCharacter(chrEntityId2);
    ForceAnimationPlayback(chrEntityId2, 20000, false, false, false);
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, 70, chrEntityId);
    WaitFixedTimeSeconds(3);
    EnableCharacterCollision(chrEntityId2);
    EnableCharacterAI(chrEntityId2);
});

// 【共通】高路ガーディアン_部位破壊 -- [Common] Takaji Guardian_Part Destruction
$Event(90005470, Restart, function(chrEntityId) {
    WaitFor(CharacterBackreadStatus(chrEntityId));
    if (!ThisEventSlot()) {
        if (CharacterHasSpEffect(chrEntityId, 12160)) {
            CreateNPCPart(chrEntityId, 20, NPCPartType.Part2, 80, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 20, 120, 120, -1, -1, -1);
        }
        if (CharacterHasSpEffect(chrEntityId, 12161)) {
            CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 80, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 30, 120, 120, -1, -1, -1);
        }
        if (CharacterHasSpEffect(chrEntityId, 12162)) {
            CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 40, 120, 120, -1, -1, -1);
        }
        if (CharacterHasSpEffect(chrEntityId, 12163)) {
            CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 50, 120, 120, -1, -1, -1);
        }
    }
L1:
    if (CharacterHasSpEffect(chrEntityId, 12160)) {
        hpSp = NPCPartHP(chrEntityId, 20) <= 0
            && CharacterHasSpEffect(chrEntityId, 12156)
            && CharacterHasSpEffect(chrEntityId, 12168)
            && !CharacterHasSpEffect(chrEntityId, 12170)
            && !CharacterHasSpEffect(chrEntityId, 12171);
    }
    if (CharacterHasSpEffect(chrEntityId, 12161)) {
        hpSp2 = NPCPartHP(chrEntityId, 30) <= 0
            && CharacterHasSpEffect(chrEntityId, 12156)
            && CharacterHasSpEffect(chrEntityId, 12169)
            && !CharacterHasSpEffect(chrEntityId, 12170)
            && !CharacterHasSpEffect(chrEntityId, 12171);
    }
    if (CharacterHasSpEffect(chrEntityId, 12162)) {
        hpSp3 = NPCPartHP(chrEntityId, 40) <= 0
            && !CharacterHasSpEffect(chrEntityId, 12170)
            && !CharacterHasSpEffect(chrEntityId, 12171);
    }
    if (CharacterHasSpEffect(chrEntityId, 12163)) {
        hpSp4 = NPCPartHP(chrEntityId, 50) <= 0
            && !CharacterHasSpEffect(chrEntityId, 12170)
            && !CharacterHasSpEffect(chrEntityId, 12171);
    }
    WaitFor(hpSp || hpSp2 || hpSp3 || hpSp4);
    GotoIf(L5, hpSp4.Passed);
    GotoIf(L4, hpSp3.Passed);
    GotoIf(L3, hpSp2.Passed);
    GotoIf(L2, hpSp.Passed);
    Goto(L9);
L2:
    ForceAnimationPlayback(chrEntityId, 20011, false, true, false);
    CreateNPCPart(chrEntityId, 20, NPCPartType.Part2, 80, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 20, 120, 120, -1, -1, -1);
    Goto(L9);
L3:
    ForceAnimationPlayback(chrEntityId, 20008, false, true, false);
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 80, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 20, 120, 120, -1, -1, -1);
    Goto(L9);
L4:
    if (!CharacterHasSpEffect(chrEntityId, 12156)) {
        ForceAnimationPlayback(chrEntityId, 20006, false, true, false);
    } else {
        ForceAnimationPlayback(chrEntityId, 20010, false, true, false);
    }
    CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 75, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 40, 120, 120, -1, -1, -1);
    Goto(L9);
L5:
    if (!CharacterHasSpEffect(chrEntityId, 12156)) {
        ForceAnimationPlayback(chrEntityId, 20007, false, true, false);
    } else {
        ForceAnimationPlayback(chrEntityId, 2009, false, true, false);
    }
    CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 75, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 50, 120, 120, -1, -1, -1);
    Goto(L9);
    if (CharacterHasSpEffect(chrEntityId, 12160)) {
        SetNPCPartHP(chrEntityId, 20, 9999999, false);
    }
    if (CharacterHasSpEffect(chrEntityId, 12161)) {
        SetNPCPartHP(chrEntityId, 30, 9999999, false);
    }
    if (CharacterHasSpEffect(chrEntityId, 12162)) {
        SetNPCPartHP(chrEntityId, 40, 9999999, false);
    }
    if (CharacterHasSpEffect(chrEntityId, 12163)) {
        SetNPCPartHP(chrEntityId, 50, 9999999, false);
    }
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】高路ガーディアン_左腕部位破壊 -- [Common] Takaji Guardian_Left arm part destroyed
$Event(90005471, Restart, function(chrEntityId) {
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && CharacterHasSpEffect(chrEntityId, 12160)
            && !CharacterHasSpEffect(chrEntityId, 12170));
    if (ThisEventSlot()) {
        SetNPCPartHP(chrEntityId, 20, 9999999, false);
    } else {
        CreateNPCPart(chrEntityId, 20, NPCPartType.Part2, 80, 1, 3, false, false);
        SetNPCPartSEAndSFX(chrEntityId, 20, 120, 120, -1, -1, -1);
    }
L0:
    WaitFor(
        (NPCPartHP(chrEntityId, 20) <= 0
            && CharacterHasSpEffect(chrEntityId, 12156)
            && CharacterHasSpEffect(chrEntityId, 12168)
            && !CharacterHasSpEffect(chrEntityId, 12171))
            || CharacterHasSpEffect(chrEntityId, 12170));
    if (!CharacterHasSpEffect(chrEntityId, 12170)) {
        ForceAnimationPlayback(chrEntityId, 20011, false, true, false);
    }
    CreateNPCPart(chrEntityId, 20, NPCPartType.Part2, 80, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 20, 120, 120, -1, -1, -1);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】高路ガーディアン_右腕部位破壊 -- [Common] Takaji Guardian_Right arm part destroyed
$Event(90005472, Restart, function(chrEntityId) {
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && CharacterHasSpEffect(chrEntityId, 12161)
            && !CharacterHasSpEffect(chrEntityId, 12170));
    if (ThisEventSlot()) {
        SetNPCPartHP(chrEntityId, 30, 9999999, false);
    } else {
        CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 80, 1, 3, false, false);
        SetNPCPartSEAndSFX(chrEntityId, 30, 120, 120, -1, -1, -1);
    }
L0:
    WaitFor(
        (NPCPartHP(chrEntityId, 30) <= 0
            && CharacterHasSpEffect(chrEntityId, 12156)
            && CharacterHasSpEffect(chrEntityId, 12169)
            && !CharacterHasSpEffect(chrEntityId, 12171))
            || CharacterHasSpEffect(chrEntityId, 12170));
    if (!CharacterHasSpEffect(chrEntityId, 12170)) {
        ForceAnimationPlayback(chrEntityId, 20008, false, true, false);
    }
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 80, 1, 3, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 30, 120, 120, -1, -1, -1);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】高路ガーディアン_左脚部位破壊 -- [Common] Takaji Guardian_Left leg part destroyed
$Event(90004473, Restart, function(chrEntityId) {
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && CharacterHasSpEffect(chrEntityId, 12162)
            && !CharacterHasSpEffect(chrEntityId, 12170));
    if (ThisEventSlot()) {
        SetNPCPartHP(chrEntityId, 40, 9999999, false);
    } else {
        CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 75, 1, 3, false, false);
        SetNPCPartSEAndSFX(chrEntityId, 40, 120, 120, -1, -1, -1);
    }
L0:
    WaitFor(
        (NPCPartHP(chrEntityId, 40) <= 0 && !CharacterHasSpEffect(chrEntityId, 12171))
            || CharacterHasSpEffect(chrEntityId, 12170));
    if (!CharacterHasSpEffect(chrEntityId, 12170)) {
        if (!CharacterHasSpEffect(chrEntityId, 12156)) {
            ForceAnimationPlayback(chrEntityId, 20006, false, true, false);
            CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 40, 120, 120, -1, -1, -1);
        } else {
L1:
            ForceAnimationPlayback(chrEntityId, 20010, false, true, false);
            CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 40, 120, 120, -1, -1, -1);
            Goto(L9);
        }
    }
L9:
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】高路ガーディアン_右脚部位破壊 -- [Common] Takaji Guardian_Right leg part destroyed
$Event(90005474, Restart, function(chrEntityId) {
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && CharacterHasSpEffect(chrEntityId, 12163)
            && !CharacterHasSpEffect(chrEntityId, 12170));
    if (ThisEventSlot()) {
        SetNPCPartHP(chrEntityId, 50, 9999999, false);
    } else {
        CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 75, 1, 3, false, false);
        SetNPCPartSEAndSFX(chrEntityId, 50, 120, 120, -1, -1, -1);
    }
L0:
    WaitFor(
        (NPCPartHP(chrEntityId, 50) <= 0 && !CharacterHasSpEffect(chrEntityId, 12171))
            || CharacterHasSpEffect(chrEntityId, 12170));
    if (!CharacterHasSpEffect(chrEntityId, 12170)) {
        if (!CharacterHasSpEffect(chrEntityId, 12156)) {
            ForceAnimationPlayback(chrEntityId, 20007, false, true, false);
            CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 50, 120, 120, -1, -1, -1);
        } else {
L1:
            ForceAnimationPlayback(chrEntityId, 20009, false, true, false);
            CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 75, 1, 3, false, false);
            SetNPCPartSEAndSFX(chrEntityId, 50, 120, 120, -1, -1, -1);
            Goto(L9);
        }
    }
L9:
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】ルーン狩りの騎士_騎乗イベント -- [Common] Rune Hunting Knight_Riding Event
$Event(90005476, Default, function(chrEntityId, chrEntityId2) {
    if (CharacterDead(chrEntityId)) {
        DisableCharacter(chrEntityId2);
        DisableCharacterCollision(chrEntityId2);
        EndEvent();
    }
L0:
    WaitFor(CharacterHasSpEffect(chrEntityId, 11805));
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, 230, chrEntityId2);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】隕鉄の獣_部位破壊 -- [Common] Meteor Beast_Part Destruction
$Event(90005480, Restart, function(chrEntityId) {
    WaitFor(
        CharacterBackreadStatus(chrEntityId)
            && !CharacterHasSpEffect(chrEntityId, 16472)
            && !CharacterHasSpEffect(chrEntityId, 16473)
            && !CharacterHasSpEffect(chrEntityId, 16474)
            && !CharacterHasSpEffect(chrEntityId, 16475));
    GotoIf(S0, !ThisEventSlot());
    GotoIf(S1, NPCPartHP(chrEntityId, 30) != 0);
S0:
    SetSpEffect(chrEntityId, 16498);
    CreateNPCPart(chrEntityId, 30, NPCPartType.Part3, 61, 1, 1, false, false);
    ChangeCharacterDispmask(chrEntityId, 10, ON);
S1:
    GotoIf(S2, !ThisEventSlot());
    GotoIf(S3, NPCPartHP(chrEntityId, 40) != 0);
S2:
    SetSpEffect(chrEntityId, 16498);
    CreateNPCPart(chrEntityId, 40, NPCPartType.Part4, 61, 1, 1, false, false);
    ChangeCharacterDispmask(chrEntityId, 11, ON);
S3:
    GotoIf(S4, !ThisEventSlot());
    GotoIf(S5, NPCPartHP(chrEntityId, 50) != 0);
S4:
    SetSpEffect(chrEntityId, 16498);
    CreateNPCPart(chrEntityId, 50, NPCPartType.Part5, 61, 1, 1, false, false);
    ChangeCharacterDispmask(chrEntityId, 12, ON);
S5:
    GotoIf(S6, !ThisEventSlot());
    GotoIf(S7, NPCPartHP(chrEntityId, 60) != 0);
S6:
    SetSpEffect(chrEntityId, 16498);
    CreateNPCPart(chrEntityId, 60, NPCPartType.Part6, 61, 1, 1, false, false);
    ChangeCharacterDispmask(chrEntityId, 13, ON);
S7:
L0:
    hp = NPCPartHP(chrEntityId, 30) <= 0;
    hp2 = NPCPartHP(chrEntityId, 40) <= 0;
    hp3 = NPCPartHP(chrEntityId, 50) <= 0;
    hp4 = NPCPartHP(chrEntityId, 60) <= 0;
    WaitFor(hp || hp2 || hp3 || hp4);
    GotoIf(L3, hp.Passed);
    GotoIf(L4, hp2.Passed);
    GotoIf(L5, hp3.Passed);
    GotoIf(L6, hp4.Passed);
L3:
    SetSpEffect(chrEntityId, 16497);
    SetSpEffect(chrEntityId, 16484);
    SetSpEffect(chrEntityId, 16472);
    ChangeCharacterDispmask(chrEntityId, 10, OFF);
    WaitFixedTimeFrames(2);
    if (!CharacterHasSpEffect(chrEntityId, 16485)) {
        ForceAnimationPlayback(chrEntityId, 20000, false, true, false);
    }
    Goto(L9);
L4:
    SetSpEffect(chrEntityId, 16497);
    SetSpEffect(chrEntityId, 16484);
    SetSpEffect(chrEntityId, 16473);
    ChangeCharacterDispmask(chrEntityId, 11, OFF);
    WaitFixedTimeFrames(2);
    if (!CharacterHasSpEffect(chrEntityId, 16485)) {
        ForceAnimationPlayback(chrEntityId, 20001, false, true, false);
    }
    Goto(L9);
L5:
    SetSpEffect(chrEntityId, 16497);
    SetSpEffect(chrEntityId, 16484);
    SetSpEffect(chrEntityId, 16474);
    ChangeCharacterDispmask(chrEntityId, 12, OFF);
    WaitFixedTimeFrames(2);
    if (!CharacterHasSpEffect(chrEntityId, 16485)) {
        ForceAnimationPlayback(chrEntityId, 20002, false, true, false);
    }
    Goto(L9);
L6:
    SetSpEffect(chrEntityId, 16497);
    SetSpEffect(chrEntityId, 16484);
    SetSpEffect(chrEntityId, 16475);
    ChangeCharacterDispmask(chrEntityId, 13, OFF);
    WaitFixedTimeFrames(2);
    if (!CharacterHasSpEffect(chrEntityId, 16485)) {
        ForceAnimationPlayback(chrEntityId, 20003, false, true, false);
    }
    Goto(L9);
L9:
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】隕鉄の獣_突進転倒 -- [Common] Meteor Beast_Charge fall
$Event(90005481, Restart, function(chrEntityId) {
    CreateNPCPart(chrEntityId, 10, NPCPartType.Part1, 9999, 1, 1, false, false);
    SetNPCPartSEAndSFX(chrEntityId, 0, 110, 110, -1, -1, -1);
    WaitFor(
        CharacterHasSpEffect(chrEntityId, 16499)
            && NPCPartAttributeDamage(chrEntityId, 10, 0, DamageType.Unspecified));
    ForceAnimationPlayback(chrEntityId, 20007, false, false, false);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】遠距離敵_セットアップ -- [Common] Long range enemy_Setup
$Event(90005485, Restart, function(chrEntityId) {
    DisableNetworkSync();
    if (!ThisEventSlot()) {
        EnableCharacterDefaultBackread(chrEntityId);
        SetCharacterEnableDistance(chrEntityId, 2000);
        DisableCharacterDisableOnHitUnload(chrEntityId);
        EnableDistancebasedNetworkUpdateAuthority(chrEntityId);
    }
L0:
    DisableCharacterGravity(chrEntityId);
    WaitFor(EntityInRadiusOfEntity(chrEntityId, 10000, 200, 1));
    EnableCharacterGravity(chrEntityId);
    WaitFor(EntityInRadiusOfEntity(chrEntityId, 10000, 220, 1));
    RestartEvent();
});

// 【共通】カタパルト -- [Common] Catapult
$Event(90005490, Restart, function(chrEntityId, chrEntityId2, assetEntityId, assetEntityId2, objactEventFlag, areaEntityId, value) {
    DisableCharacterGravity(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery5Frames);
    DisableCharacterDisableOnHitUnload(chrEntityId);
    SetCharacterEnableDistance(chrEntityId, 2000);
    IssueShortWarpRequest(chrEntityId, TargetEntityType.Asset, assetEntityId, 100);
    ReproduceAssetAnimation(assetEntityId, 0);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
    }
    WaitFor(
        (((CharacterType(10000, TargetType.BlackPhantom) && CharacterHasSpEffect(10000, 3710))
            || CharacterType(10000, TargetType.Alive)
            || CharacterType(10000, TargetType.GrayPhantom)
            || CharacterType(10000, TargetType.WhitePhantom)
            || CharacterType(10000, TargetType.BluePhantom))
            && InArea(10000, areaEntityId)
            && CharacterAIState(chrEntityId, AIStateType.Combat)
            && !CharacterDead(chrEntityId2))
            || ObjActEventFlag(objactEventFlag));
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AlwaysUpdate);
    SetSpEffect(chrEntityId, 16601);
    if (value != 0) {
        RequestCharacterAICommand(chrEntityId, 20, 0);
    } else {
        RequestCharacterAICommand(chrEntityId, 10, 0);
    }
    RequestCharacterAIReplan(chrEntityId);
    ForceAnimationPlayback(assetEntityId, 0, false, true, true);
    EnableObjAct(assetEntityId2, -1);
    RequestCharacterAICommand(chrEntityId, -1, 0);
    RequestCharacterAIReplan(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery5Frames);
    RestartEvent();
});

// 【共通】カタパルト_射手 -- [Common] Catapult_Archer
$Event(90005491, Restart, function(chrEntityId, assetEntityId, areaEntityId) {
    WaitFor(
        !CharacterDead(chrEntityId, GreaterOrEqual, 1)
            && EntityInRadiusOfEntity(chrEntityId, assetEntityId, 2, 1)
            && InArea(10000, areaEntityId));
    InitializeObjAct(assetEntityId, -1, -1);
    WaitFixedTimeSeconds(0.5);
    RestartEvent();
});

// 【共通】2フロア移動エレベータ -- [Common] 2-floor moving elevator
$Event(90005500, Default, function(eventFlagId, eventFlagId2, value, assetEntityId, assetEntityId2, objactEventFlag, assetEntityId3, objactEventFlag2, areaEntityId, areaEntityId2, eventFlagId3, eventFlagId4, eventFlagId5) {
    if (!(((EventFlag(eventFlagId) && EventFlag(eventFlagId2))
        || (!EventFlag(eventFlagId) && !EventFlag(eventFlagId2)))
        && EventFlag(eventFlagId3))) {
        if (EventFlag(eventFlagId2)) {
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                EnableObjAct(assetEntityId3, -1);
                DisableObjAct(assetEntityId2, -1);
            }
            obj = ObjActEventFlag(objactEventFlag2);
            flag = !EventFlag(eventFlagId);
            areaFlag &= InArea(10000, areaEntityId);
            if (eventFlagId5 != 0) {
                areaFlag &= EventFlag(eventFlagId5);
            }
            WaitFor(obj || flag || areaFlag);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                DisableObjAct(assetEntityId3, -1);
            }
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            }
            SetEventFlagID(eventFlagId2, OFF);
            if (!obj.Passed) {
                GotoIf(L1, EventFlag(eventFlagId4));
                GotoIf(S9, value == 10);
                GotoIf(S8, value == 9);
                GotoIf(S7, value == 8);
                GotoIf(S6, value == 7);
                GotoIf(S5, value == 6);
                GotoIf(S4, value == 5);
                GotoIf(S3, value == 4);
                GotoIf(S2, value == 3);
                GotoIf(S1, value == 2);
                GotoIf(S0, value == 1);
                ForceAnimationPlayback(assetEntityId, 21, false, true, true);
                Goto(L2);
S0:
                ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
                Goto(L2);
S1:
                ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
                Goto(L2);
S2:
                ForceAnimationPlayback(assetEntityId, 3000021, false, true, true);
                Goto(L2);
S3:
                ForceAnimationPlayback(assetEntityId, 4000021, false, true, true);
                Goto(L2);
S4:
                ForceAnimationPlayback(assetEntityId, 5000021, false, true, true);
                Goto(L2);
S5:
                ForceAnimationPlayback(assetEntityId, 6000021, false, true, true);
                Goto(L2);
S6:
                ForceAnimationPlayback(assetEntityId, 7000021, false, true, true);
                Goto(L2);
S7:
                ForceAnimationPlayback(assetEntityId, 8000021, false, true, true);
                Goto(L2);
S8:
                ForceAnimationPlayback(assetEntityId, 9000021, false, true, true);
                Goto(L2);
S9:
                ForceAnimationPlayback(assetEntityId, 10000021, false, true, true);
            } else {
L1:
                if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                    SetNetworkconnectedEventFlagID(eventFlagId4, ON);
                }
                WaitFixedTimeSeconds(2);
                GotoIf(S19, value == 10);
                GotoIf(S18, value == 9);
                GotoIf(S17, value == 8);
                GotoIf(S16, value == 7);
                GotoIf(S15, value == 6);
                GotoIf(S14, value == 5);
                GotoIf(S13, value == 4);
                GotoIf(S12, value == 3);
                GotoIf(S11, value == 2);
                GotoIf(S10, value == 1);
                ForceAnimationPlayback(assetEntityId, 21, false, true, true);
                Goto(L11);
S10:
                ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
                Goto(L11);
S11:
                ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
                Goto(L11);
S12:
                ForceAnimationPlayback(assetEntityId, 3000021, false, true, true);
                Goto(L11);
S13:
                ForceAnimationPlayback(assetEntityId, 4000021, false, true, true);
                Goto(L11);
S14:
                ForceAnimationPlayback(assetEntityId, 5000021, false, true, true);
                Goto(L11);
S15:
                ForceAnimationPlayback(assetEntityId, 6000021, false, true, true);
                Goto(L11);
S16:
                ForceAnimationPlayback(assetEntityId, 7000021, false, true, true);
                Goto(L11);
S17:
                ForceAnimationPlayback(assetEntityId, 8000021, false, true, true);
                Goto(L11);
S18:
                ForceAnimationPlayback(assetEntityId, 9000021, false, true, true);
                Goto(L11);
S19:
                ForceAnimationPlayback(assetEntityId, 10000021, false, true, true);
L11:
                ForceAnimationPlayback(assetEntityId3, 3, false, false, true);
                if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                    SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
                }
            }
L2:
            WaitFor(
                AssetBackread(assetEntityId)
                    && (!AllPlayersInArea(areaEntityId2) || EventFlag(eventFlagId)));
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
                GotoIf(S29, value == 10);
                GotoIf(S28, value == 9);
                GotoIf(S27, value == 8);
                GotoIf(S26, value == 7);
                GotoIf(S25, value == 6);
                GotoIf(S24, value == 5);
                GotoIf(S23, value == 4);
                GotoIf(S22, value == 3);
                GotoIf(S21, value == 2);
                GotoIf(S20, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, false, true);
                Goto(L12);
S20:
                ForceAnimationPlayback(assetEntityId, 1000110, false, false, true);
                Goto(L12);
S21:
                ForceAnimationPlayback(assetEntityId, 2000110, false, false, true);
                Goto(L12);
S22:
                ForceAnimationPlayback(assetEntityId, 3000110, false, false, true);
                Goto(L12);
S23:
                ForceAnimationPlayback(assetEntityId, 4000110, false, false, true);
                Goto(L12);
S24:
                ForceAnimationPlayback(assetEntityId, 5000110, false, false, true);
                Goto(L12);
S25:
                ForceAnimationPlayback(assetEntityId, 6000110, false, false, true);
                Goto(L12);
S26:
                ForceAnimationPlayback(assetEntityId, 7000110, false, false, true);
                Goto(L12);
S27:
                ForceAnimationPlayback(assetEntityId, 8000110, false, false, true);
                Goto(L12);
S28:
                ForceAnimationPlayback(assetEntityId, 9000110, false, false, true);
                Goto(L12);
S29:
                ForceAnimationPlayback(assetEntityId, 10000110, false, false, true);
            } else {
L3:
                GotoIf(S39, value == 10);
                GotoIf(S38, value == 9);
                GotoIf(S37, value == 8);
                GotoIf(S36, value == 7);
                GotoIf(S35, value == 6);
                GotoIf(S34, value == 5);
                GotoIf(S33, value == 4);
                GotoIf(S32, value == 3);
                GotoIf(S31, value == 2);
                GotoIf(S30, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, true, true);
                Goto(L12);
S30:
                ForceAnimationPlayback(assetEntityId, 1000110, false, true, true);
                Goto(L12);
S31:
                ForceAnimationPlayback(assetEntityId, 2000110, false, true, true);
                Goto(L12);
S32:
                ForceAnimationPlayback(assetEntityId, 3000110, false, true, true);
                Goto(L12);
S33:
                ForceAnimationPlayback(assetEntityId, 4000110, false, true, true);
                Goto(L12);
S34:
                ForceAnimationPlayback(assetEntityId, 5000110, false, true, true);
                Goto(L12);
S35:
                ForceAnimationPlayback(assetEntityId, 6000110, false, true, true);
                Goto(L12);
S36:
                ForceAnimationPlayback(assetEntityId, 7000110, false, true, true);
                Goto(L12);
S37:
                ForceAnimationPlayback(assetEntityId, 8000110, false, true, true);
                Goto(L12);
S38:
                ForceAnimationPlayback(assetEntityId, 9000110, false, true, true);
                Goto(L12);
S39:
                ForceAnimationPlayback(assetEntityId, 10000110, false, true, true);
            }
L12:
            RestartEvent();
        }
L0:
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            EnableObjAct(assetEntityId2, -1);
            DisableObjAct(assetEntityId3, -1);
        }
        obj2 = ObjActEventFlag(objactEventFlag);
        flag2 = EventFlag(eventFlagId);
        areaSpFlag &= InArea(10000, areaEntityId2) && !CharacterHasSpEffect(10000, 4800);
        if (eventFlagId5 != 0) {
            areaSpFlag &= EventFlag(eventFlagId5);
        }
        WaitFor(obj2 || flag2 || areaSpFlag);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            DisableObjAct(assetEntityId2, -1);
        }
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, ON);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
        SetEventFlagID(eventFlagId2, ON);
        if (!obj2.Passed) {
            GotoIf(L4, EventFlag(eventFlagId4));
            GotoIf(S49, value == 10);
            GotoIf(S48, value == 9);
            GotoIf(S47, value == 8);
            GotoIf(S46, value == 7);
            GotoIf(S45, value == 6);
            GotoIf(S44, value == 5);
            GotoIf(S43, value == 4);
            GotoIf(S42, value == 3);
            GotoIf(S41, value == 2);
            GotoIf(S40, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L5);
S40:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L5);
S41:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L5);
S42:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L5);
S43:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
            Goto(L5);
S44:
            ForceAnimationPlayback(assetEntityId, 5000012, false, true, true);
            Goto(L5);
S45:
            ForceAnimationPlayback(assetEntityId, 6000012, false, true, true);
            Goto(L5);
S46:
            ForceAnimationPlayback(assetEntityId, 7000012, false, true, true);
            Goto(L5);
S47:
            ForceAnimationPlayback(assetEntityId, 8000012, false, true, true);
            Goto(L5);
S48:
            ForceAnimationPlayback(assetEntityId, 9000012, false, true, true);
            Goto(L5);
S49:
            ForceAnimationPlayback(assetEntityId, 10000012, false, true, true);
        } else {
L4:
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, ON);
            }
            WaitFixedTimeSeconds(2);
            GotoIf(S59, value == 10);
            GotoIf(S58, value == 9);
            GotoIf(S57, value == 8);
            GotoIf(S56, value == 7);
            GotoIf(S55, value == 6);
            GotoIf(S54, value == 5);
            GotoIf(S53, value == 4);
            GotoIf(S52, value == 3);
            GotoIf(S51, value == 2);
            GotoIf(S50, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L14);
S50:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L14);
S51:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L14);
S52:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L14);
S53:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
            Goto(L14);
S54:
            ForceAnimationPlayback(assetEntityId, 5000012, false, true, true);
            Goto(L14);
S55:
            ForceAnimationPlayback(assetEntityId, 6000012, false, true, true);
            Goto(L14);
S56:
            ForceAnimationPlayback(assetEntityId, 7000012, false, true, true);
            Goto(L14);
S57:
            ForceAnimationPlayback(assetEntityId, 8000012, false, true, true);
            Goto(L14);
S58:
            ForceAnimationPlayback(assetEntityId, 9000012, false, true, true);
            Goto(L14);
S59:
            ForceAnimationPlayback(assetEntityId, 10000012, false, true, true);
L14:
            ForceAnimationPlayback(assetEntityId2, 3, false, false, true);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
            }
        }
L5:
        WaitFor(
            AssetBackread(assetEntityId)
                && (!AllPlayersInArea(areaEntityId) || !EventFlag(eventFlagId)));
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            GotoIf(S69, value == 10);
            GotoIf(S68, value == 9);
            GotoIf(S67, value == 8);
            GotoIf(S66, value == 7);
            GotoIf(S65, value == 6);
            GotoIf(S64, value == 5);
            GotoIf(S63, value == 4);
            GotoIf(S62, value == 3);
            GotoIf(S61, value == 2);
            GotoIf(S60, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, false, true);
            Goto(L15);
S60:
            ForceAnimationPlayback(assetEntityId, 1000120, false, false, true);
            Goto(L15);
S61:
            ForceAnimationPlayback(assetEntityId, 2000120, false, false, true);
            Goto(L15);
S62:
            ForceAnimationPlayback(assetEntityId, 3000120, false, false, true);
            Goto(L15);
S63:
            ForceAnimationPlayback(assetEntityId, 4000120, false, false, true);
            Goto(L15);
S64:
            ForceAnimationPlayback(assetEntityId, 5000120, false, false, true);
            Goto(L15);
S65:
            ForceAnimationPlayback(assetEntityId, 6000120, false, false, true);
            Goto(L15);
S66:
            ForceAnimationPlayback(assetEntityId, 7000120, false, false, true);
            Goto(L15);
S67:
            ForceAnimationPlayback(assetEntityId, 8000120, false, false, true);
            Goto(L15);
S68:
            ForceAnimationPlayback(assetEntityId, 9000120, false, false, true);
            Goto(L15);
S69:
            ForceAnimationPlayback(assetEntityId, 10000120, false, false, true);
        } else {
L6:
            GotoIf(S79, value == 10);
            GotoIf(S78, value == 9);
            GotoIf(S77, value == 8);
            GotoIf(S76, value == 7);
            GotoIf(S75, value == 6);
            GotoIf(S74, value == 5);
            GotoIf(S73, value == 4);
            GotoIf(S72, value == 3);
            GotoIf(S71, value == 2);
            GotoIf(S70, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, true, true);
            Goto(L15);
S70:
            ForceAnimationPlayback(assetEntityId, 1000120, false, true, true);
            Goto(L15);
S71:
            ForceAnimationPlayback(assetEntityId, 2000120, false, true, true);
            Goto(L15);
S72:
            ForceAnimationPlayback(assetEntityId, 3000120, false, true, true);
            Goto(L15);
S73:
            ForceAnimationPlayback(assetEntityId, 4000120, false, true, true);
            Goto(L15);
S74:
            ForceAnimationPlayback(assetEntityId, 5000120, false, true, true);
            Goto(L15);
S75:
            ForceAnimationPlayback(assetEntityId, 6000120, false, true, true);
            Goto(L15);
S76:
            ForceAnimationPlayback(assetEntityId, 7000120, false, true, true);
            Goto(L15);
S77:
            ForceAnimationPlayback(assetEntityId, 8000120, false, true, true);
            Goto(L15);
S78:
            ForceAnimationPlayback(assetEntityId, 9000120, false, true, true);
            Goto(L15);
S79:
            ForceAnimationPlayback(assetEntityId, 10000120, false, true, true);
        }
L15:
        RestartEvent();
    }
L9:
    WaitFor(!EventFlag(eventFlagId3));
    RestartEvent();
});

// 【共通】2フロア移動エレベータ_初期設定 -- [Common] 2-floor moving elevator_Initial settings
$Event(90005501, Restart, function(eventFlagId, eventFlagId2, value, assetEntityId, assetEntityId2, assetEntityId3, eventFlagId3) {
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    WaitFor(AssetBackread(assetEntityId));
    if (EventFlag(eventFlagId)) {
        if (value != 10) {
            GotoIf(S8, value == 9);
            GotoIf(S7, value == 8);
            GotoIf(S6, value == 7);
            GotoIf(S5, value == 6);
            GotoIf(S4, value == 5);
            GotoIf(S3, value == 4);
            GotoIf(S2, value == 3);
            GotoIf(S1, value == 2);
            GotoIf(S0, value == 1);
            ForceAnimationPlayback(assetEntityId, 20, false, false, false);
            Goto(L10);
S0:
            ForceAnimationPlayback(assetEntityId, 1000020, false, false, false);
            Goto(L10);
S1:
            ForceAnimationPlayback(assetEntityId, 2000020, false, false, false);
            Goto(L10);
S2:
            ForceAnimationPlayback(assetEntityId, 3000020, false, false, false);
            Goto(L10);
S3:
            ForceAnimationPlayback(assetEntityId, 4000020, false, false, false);
            Goto(L10);
S4:
            ForceAnimationPlayback(assetEntityId, 5000020, false, false, false);
            Goto(L10);
S5:
            ForceAnimationPlayback(assetEntityId, 6000020, false, false, false);
            Goto(L10);
S6:
            ForceAnimationPlayback(assetEntityId, 7000020, false, false, false);
            Goto(L10);
S7:
            ForceAnimationPlayback(assetEntityId, 8000020, false, false, false);
            Goto(L10);
S8:
            ForceAnimationPlayback(assetEntityId, 9000020, false, false, false);
        } else {
            ForceAnimationPlayback(assetEntityId, 10000020, false, false, false);
        }
L10:
        SetEventFlagID(eventFlagId2, ON);
        DisableObjAct(assetEntityId2, -1);
        EndEvent();
    }
L0:
    GotoIf(S18, value == 10);
    GotoIf(S17, value == 9);
    GotoIf(S16, value == 8);
    GotoIf(S15, value == 7);
    GotoIf(S14, value == 6);
    GotoIf(S13, value == 5);
    GotoIf(S12, value == 4);
    GotoIf(S11, value == 3);
    GotoIf(S10, value == 2);
    GotoIf(S9, value == 1);
    ForceAnimationPlayback(assetEntityId, 10, false, false, true);
    Goto(L15);
S9:
    ForceAnimationPlayback(assetEntityId, 1000010, false, false, true);
    Goto(L15);
S10:
    ForceAnimationPlayback(assetEntityId, 2000010, false, false, true);
    Goto(L15);
S11:
    ForceAnimationPlayback(assetEntityId, 3000010, false, false, true);
    Goto(L15);
S12:
    ForceAnimationPlayback(assetEntityId, 4000010, false, false, true);
    Goto(L15);
S13:
    ForceAnimationPlayback(assetEntityId, 5000010, false, false, true);
    Goto(L15);
S14:
    ForceAnimationPlayback(assetEntityId, 6000010, false, false, true);
    Goto(L15);
S15:
    ForceAnimationPlayback(assetEntityId, 7000010, false, false, true);
    Goto(L15);
S16:
    ForceAnimationPlayback(assetEntityId, 8000010, false, false, true);
    Goto(L15);
S17:
    ForceAnimationPlayback(assetEntityId, 9000010, false, false, true);
    Goto(L15);
S18:
    ForceAnimationPlayback(assetEntityId, 10000010, false, false, true);
L15:
    SetEventFlagID(eventFlagId2, OFF);
    DisableObjAct(assetEntityId3, -1);
    EndEvent();
});

// 【共通】2フロア移動エレベータ_初回起動 -- [Common] 2-floor moving elevator_first activation
$Event(90005502, Restart, function(eventFlagId, assetEntityId, areaEntityId) {
    DisableNetworkSync();
    EndIf(EventFlag(eventFlagId));
    WaitFixedTimeFrames(2);
    DisableObjAct(assetEntityId, -1);
    areaChr = InArea(10000, areaEntityId)
        && (CharacterType(10000, TargetType.Alive) || CharacterType(10000, TargetType.GrayPhantom));
    WaitFor(areaChr || ActionButtonInArea(8301, assetEntityId) || EventFlag(eventFlagId));
    if (!areaChr.Passed) {
        EndIf(EventFlag(eventFlagId));
        DisplayGenericDialog(4000, PromptType.OKCANCEL, NumberofOptions.OneButton, 0, 3);
        RestartEvent();
    }
L0:
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
    RestartEvent();
});

// 【共通】2フロア移動エレベータ_初回起動Ver2 -- [Common] 2-floor moving elevator_Initial startup Ver2
$Event(90015502, Restart, function(eventFlagId, assetEntityId, areaEntityId) {
    DisableNetworkSync();
    EndIf(EventFlag(eventFlagId));
    WaitFixedTimeFrames(2);
    DisableObjAct(assetEntityId, -1);
    areaChrHp = InArea(10000, areaEntityId)
        && (CharacterType(10000, TargetType.Alive) || CharacterType(10000, TargetType.GrayPhantom))
        && CharacterHPValue(10000) != 0;
    WaitFor(areaChrHp || ActionButtonInArea(8301, assetEntityId) || EventFlag(eventFlagId));
    if (!areaChrHp.Passed) {
        EndIf(EventFlag(eventFlagId));
        DisplayGenericDialog(4000, PromptType.OKCANCEL, NumberofOptions.OneButton, 0, 3);
        RestartEvent();
    }
L0:
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
    RestartEvent();
});

// 【共通】2軸移動エレベータ -- [Common] 2-axis moving elevator
$Event(90005503, Default, function(eventFlagId, eventFlagId2, value, assetEntityId, areaEntityId, areaEntityId2, areaEntityId3, areaEntityId4, eventFlagId3, eventFlagId4, eventFlagId5) {
    if (!(((EventFlag(eventFlagId) && EventFlag(eventFlagId2))
        || (!EventFlag(eventFlagId) && !EventFlag(eventFlagId2)))
        && EventFlag(eventFlagId3))) {
        if (EventFlag(eventFlagId2)) {
            flag = !EventFlag(eventFlagId);
            cond &= InArea(10000, areaEntityId) && !CharacterHasSpEffect(10000, 4800);
            if (eventFlagId5 != 0) {
                cond &= EventFlag(eventFlagId5);
            }
            areaSpFlag &= InArea(10000, areaEntityId4) && !CharacterHasSpEffect(10000, 4800);
            if (eventFlagId5 != 0) {
                areaSpFlag &= EventFlag(eventFlagId5);
            }
            WaitFor(flag || cond || areaSpFlag);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            }
            SetEventFlagID(eventFlagId2, OFF);
            GotoIf(S3, value == 4);
            GotoIf(S2, value == 3);
            GotoIf(S1, value == 2);
            GotoIf(S0, value == 1);
            ForceAnimationPlayback(assetEntityId, 21, false, true, true);
            Goto(L2);
S0:
            ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
            Goto(L2);
S1:
            ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
            Goto(L2);
S2:
            ForceAnimationPlayback(assetEntityId, 3000021, false, true, true);
            Goto(L2);
S3:
            ForceAnimationPlayback(assetEntityId, 4000021, false, true, true);
L2:
            WaitFor(
                AssetBackread(assetEntityId)
                    && ((!AllPlayersInArea(areaEntityId3) && !AllPlayersInArea(areaEntityId2))
                        || EventFlag(eventFlagId)));
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
                GotoIf(S7, value == 4);
                GotoIf(S6, value == 3);
                GotoIf(S5, value == 2);
                GotoIf(S4, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, false, true);
                Goto(L12);
S4:
                ForceAnimationPlayback(assetEntityId, 1000110, false, false, true);
                Goto(L12);
S5:
                ForceAnimationPlayback(assetEntityId, 2000110, false, false, true);
                Goto(L12);
S6:
                ForceAnimationPlayback(assetEntityId, 3000110, false, false, true);
                Goto(L12);
S7:
                ForceAnimationPlayback(assetEntityId, 4000110, false, false, true);
            } else {
L3:
                GotoIf(S11, value == 4);
                GotoIf(S10, value == 3);
                GotoIf(S9, value == 2);
                GotoIf(S8, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, true, true);
                Goto(L12);
S8:
                ForceAnimationPlayback(assetEntityId, 1000110, false, true, true);
                Goto(L12);
S9:
                ForceAnimationPlayback(assetEntityId, 2000110, false, true, true);
                Goto(L12);
S10:
                ForceAnimationPlayback(assetEntityId, 3000110, false, true, true);
                Goto(L12);
S11:
                ForceAnimationPlayback(assetEntityId, 4000110, false, true, true);
            }
L12:
            RestartEvent();
        }
L0:
        flag2 = EventFlag(eventFlagId);
        areaSpFlag2 &= InArea(10000, areaEntityId3) && !CharacterHasSpEffect(10000, 4800);
        if (eventFlagId5 != 0) {
            areaSpFlag2 &= EventFlag(eventFlagId5);
        }
        areaSpFlag3 &= InArea(10000, areaEntityId2) && !CharacterHasSpEffect(10000, 4800);
        if (eventFlagId5 != 0) {
            areaSpFlag3 &= EventFlag(eventFlagId5);
        }
        WaitFor(flag2 || areaSpFlag2 || areaSpFlag3);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            DisableObjAct(areaEntityId, -1);
        }
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, ON);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
        SetEventFlagID(eventFlagId2, ON);
        if (!flag2.Passed) {
            GotoIf(L4, EventFlag(eventFlagId4));
            GotoIf(S15, value == 4);
            GotoIf(S14, value == 3);
            GotoIf(S13, value == 2);
            GotoIf(S12, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L5);
S12:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L5);
S13:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L5);
S14:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L5);
S15:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
        } else {
L4:
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, ON);
            }
            WaitFixedTimeSeconds(2);
            GotoIf(S19, value == 4);
            GotoIf(S18, value == 3);
            GotoIf(S17, value == 2);
            GotoIf(S16, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L14);
S16:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L14);
S17:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L14);
S18:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L14);
S19:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
L14:
            ForceAnimationPlayback(areaEntityId, 3, false, false, true);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
            }
        }
L5:
        cond &= AssetBackread(assetEntityId)
            && ((!AllPlayersInArea(areaEntityId) && !AllPlayersInArea(areaEntityId4))
                || !EventFlag(eventFlagId));
        WaitFor(cond);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            GotoIf(S23, value == 4);
            GotoIf(S22, value == 3);
            GotoIf(S21, value == 2);
            GotoIf(S20, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, false, true);
            Goto(L15);
S20:
            ForceAnimationPlayback(assetEntityId, 1000120, false, false, true);
            Goto(L15);
S21:
            ForceAnimationPlayback(assetEntityId, 2000120, false, false, true);
            Goto(L15);
S22:
            ForceAnimationPlayback(assetEntityId, 3000120, false, false, true);
            Goto(L15);
S23:
            ForceAnimationPlayback(assetEntityId, 4000120, false, false, true);
        } else {
L6:
            GotoIf(S27, value == 4);
            GotoIf(S26, value == 3);
            GotoIf(S25, value == 2);
            GotoIf(S24, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, false, true);
            Goto(L15);
S24:
            ForceAnimationPlayback(assetEntityId, 1000120, false, false, true);
            Goto(L15);
S25:
            ForceAnimationPlayback(assetEntityId, 2000120, false, false, true);
            Goto(L15);
S26:
            ForceAnimationPlayback(assetEntityId, 3000120, false, false, true);
            Goto(L15);
S27:
            ForceAnimationPlayback(assetEntityId, 4000120, false, false, true);
        }
L15:
        RestartEvent();
    }
L9:
    WaitFor(!EventFlag(eventFlagId3));
    RestartEvent();
});

// 【共通】2軸移動エレベータ_初期設定 -- [Common] 2-axis moving elevator_Initial settings
$Event(90005504, Default, function(eventFlagId, eventFlagId2, value, entityId, eventFlagId3) {
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    if (EventFlag(eventFlagId)) {
        if (value != 4) {
            GotoIf(S2, value == 3);
            GotoIf(S1, value == 2);
            GotoIf(S0, value == 1);
            ForceAnimationPlayback(entityId, 20, false, false, false);
            Goto(L10);
S0:
            ForceAnimationPlayback(entityId, 1000020, false, false, false);
            Goto(L10);
S1:
            ForceAnimationPlayback(entityId, 2000020, false, false, false);
            Goto(L10);
S2:
            ForceAnimationPlayback(entityId, 3000020, false, false, false);
        } else {
            ForceAnimationPlayback(entityId, 4000020, false, false, false);
            Goto(L10);
        }
L10:
        SetEventFlagID(eventFlagId2, ON);
        EndEvent();
    }
L0:
    GotoIf(S6, value == 4);
    GotoIf(S5, value == 3);
    GotoIf(S4, value == 2);
    GotoIf(S3, value == 1);
    ForceAnimationPlayback(entityId, 10, false, false, true);
    Goto(L15);
S3:
    ForceAnimationPlayback(entityId, 1000010, false, false, true);
    Goto(L15);
S4:
    ForceAnimationPlayback(entityId, 2000010, false, false, true);
    Goto(L15);
S5:
    ForceAnimationPlayback(entityId, 3000010, false, false, true);
    Goto(L15);
S6:
    ForceAnimationPlayback(entityId, 4000010, false, false, true);
L15:
    SetEventFlagID(eventFlagId2, OFF);
    EndEvent();
});

// 【共通】神門エレベータ -- [Common] Shinmon Elevator
$Event(90005505, Default, function(eventFlagId, eventFlagId2, value, assetEntityId, assetEntityId2, objactEventFlag, assetEntityId3, objactEventFlag2, eventFlagId3, eventFlagId4, eventFlagId5) {
    if (!(((EventFlag(eventFlagId) && EventFlag(eventFlagId2))
        || (!EventFlag(eventFlagId) && !EventFlag(eventFlagId2)))
        && EventFlag(eventFlagId3))) {
        if (EventFlag(eventFlagId2)) {
            if (PlayerIsInOwnWorld()) {
                EnableObjAct(assetEntityId3, -1);
                DisableObjAct(assetEntityId2, -1);
            }
            obj = ObjActEventFlag(objactEventFlag2);
            flag = !EventFlag(eventFlagId);
            if (eventFlagId5 != 0) {
                flagAct &= EventFlag(eventFlagId5);
            }
            flagAct &= ActionButtonInArea(8320, assetEntityId);
            WaitFor(obj || flag || flagAct);
            if (PlayerIsInOwnWorld()) {
                DisableObjAct(assetEntityId3, -1);
            }
            if (PlayerIsInOwnWorld()) {
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            }
            SetEventFlagID(eventFlagId2, OFF);
            GotoIf(L1, flagAct.Passed);
            GotoIf(L2, obj.Passed);
            GotoIf(L2, EventFlag(eventFlagId4));
            GotoIf(S1, value == 2);
            GotoIf(S0, value == 1);
            ForceAnimationPlayback(assetEntityId, 21, false, true, true);
            Goto(L3);
S0:
            ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
            Goto(L3);
S1:
            ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
            Goto(L3);
L1:
            IssueShortWarpRequest(10000, TargetEntityType.Asset, assetEntityId, 191);
            ForceAnimationPlayback(10000, 60200, false, false, false);
            GotoIf(S3, value == 2);
            GotoIf(S2, value == 1);
            ForceAnimationPlayback(assetEntityId, 21, false, true, true);
            Goto(L3);
S2:
            ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
            Goto(L3);
S3:
            ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
            Goto(L3);
L2:
            SetNetworkconnectedEventFlagID(eventFlagId4, ON);
            WaitFixedTimeSeconds(2);
            if (value != 2) {
                GotoIf(S4, value == 1);
                ForceAnimationPlayback(assetEntityId, 21, false, true, true);
                Goto(L11);
S4:
                ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
            } else {
                ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
            }
L11:
            ForceAnimationPlayback(assetEntityId3, 3, false, false, true);
            SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
L3:
            WaitFor(AssetBackread(assetEntityId));
            if (PlayerIsInOwnWorld()) {
                SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
                GotoIf(S6, value == 2);
                GotoIf(S5, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, false, true);
                Goto(L12);
S5:
                ForceAnimationPlayback(assetEntityId, 1000110, false, false, true);
                Goto(L12);
S6:
                ForceAnimationPlayback(assetEntityId, 2000110, false, false, true);
            } else {
L4:
                if (value != 2) {
                    GotoIf(S7, value == 1);
                    ForceAnimationPlayback(assetEntityId, 110, false, true, true);
                    Goto(L12);
S7:
                    ForceAnimationPlayback(assetEntityId, 1000110, false, true, true);
                } else {
                    ForceAnimationPlayback(assetEntityId, 2000110, false, true, true);
                }
            }
L12:
            RestartEvent();
        }
L0:
        if (PlayerIsInOwnWorld()) {
            EnableObjAct(assetEntityId2, -1);
            DisableObjAct(assetEntityId3, -1);
        }
        obj2 = ObjActEventFlag(objactEventFlag);
        flag2 = EventFlag(eventFlagId);
        if (eventFlagId5 != 0) {
            flagAct2 &= EventFlag(eventFlagId5);
        }
        flagAct2 &= ActionButtonInArea(8320, assetEntityId);
        WaitFor(obj2 || flag2 || flagAct2);
        if (PlayerIsInOwnWorld()) {
            DisableObjAct(assetEntityId2, -1);
        }
        if (PlayerIsInOwnWorld()) {
            SetNetworkconnectedEventFlagID(eventFlagId3, ON);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
        SetEventFlagID(eventFlagId2, ON);
        GotoIf(L5, flagAct2.Passed);
        GotoIf(L6, obj2.Passed);
        GotoIf(L6, EventFlag(eventFlagId4));
        GotoIf(S9, value == 2);
        GotoIf(S8, value == 1);
        ForceAnimationPlayback(assetEntityId, 12, false, true, true);
        Goto(L7);
S8:
        ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
        Goto(L7);
S9:
        ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
        Goto(L7);
L5:
        IssueShortWarpRequest(10000, TargetEntityType.Asset, assetEntityId, 191);
        ForceAnimationPlayback(10000, 60200, false, false, false);
        GotoIf(S11, value == 2);
        GotoIf(S10, value == 1);
        ForceAnimationPlayback(assetEntityId, 12, false, true, true);
        Goto(L7);
S10:
        ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
        Goto(L7);
S11:
        ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
        Goto(L7);
L6:
        SetNetworkconnectedEventFlagID(eventFlagId4, ON);
        WaitFixedTimeSeconds(2);
        if (value != 2) {
            GotoIf(S12, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L14);
S12:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
        } else {
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
        }
L14:
        ForceAnimationPlayback(assetEntityId2, 3, false, false, true);
        SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
L7:
        WaitFor(AssetBackread(assetEntityId));
        if (PlayerIsInOwnWorld()) {
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            GotoIf(S14, value == 2);
            GotoIf(S13, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, false, true);
            Goto(L15);
S13:
            ForceAnimationPlayback(assetEntityId, 1000120, false, false, true);
            Goto(L15);
S14:
            ForceAnimationPlayback(assetEntityId, 2000120, false, false, true);
        } else {
L8:
            if (value != 2) {
                GotoIf(S15, value == 1);
                ForceAnimationPlayback(assetEntityId, 120, false, true, true);
                Goto(L15);
S15:
                ForceAnimationPlayback(assetEntityId, 1000120, false, true, true);
            } else {
                ForceAnimationPlayback(assetEntityId, 2000120, false, true, true);
            }
        }
L15:
        RestartEvent();
    }
L9:
    WaitFor(!EventFlag(eventFlagId3));
    RestartEvent();
});

// 【共通】神塔エレベータ -- [Common] Shrine tower elevator
$Event(90005507, Default, function(eventFlagId, eventFlagId2, value, assetEntityId, entityId, areaEntityId, entityId2, areaEntityId2, areaEntityId3, areaEntityId4, eventFlagId3, eventFlagId4, eventFlagId5) {
    if (!(((EventFlag(eventFlagId) && EventFlag(eventFlagId2))
        || (!EventFlag(eventFlagId) && !EventFlag(eventFlagId2)))
        && EventFlag(eventFlagId3))) {
        if (EventFlag(eventFlagId2)) {
            area = InArea(10000, areaEntityId2);
            flag = !EventFlag(eventFlagId);
            areaFlag &= InArea(10000, areaEntityId3);
            if (eventFlagId5 != 0) {
                areaFlag &= EventFlag(eventFlagId5);
            }
            WaitFor(area || flag || areaFlag);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, ON);
                SetNetworkconnectedEventFlagID(eventFlagId, OFF);
            }
            SetEventFlagID(eventFlagId2, OFF);
            if (!area.Passed) {
                GotoIf(L1, EventFlag(eventFlagId4));
                ForceAnimationPlayback(entityId2, 1, false, false, true);
                GotoIf(S9, value == 10);
                GotoIf(S8, value == 9);
                GotoIf(S7, value == 8);
                GotoIf(S6, value == 7);
                GotoIf(S5, value == 6);
                GotoIf(S4, value == 5);
                GotoIf(S3, value == 4);
                GotoIf(S2, value == 3);
                GotoIf(S1, value == 2);
                GotoIf(S0, value == 1);
                ForceAnimationPlayback(assetEntityId, 21, false, true, true);
                Goto(L2);
S0:
                ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
                Goto(L2);
S1:
                ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
                Goto(L2);
S2:
                ForceAnimationPlayback(assetEntityId, 3000021, false, true, true);
                Goto(L2);
S3:
                ForceAnimationPlayback(assetEntityId, 4000021, false, true, true);
                Goto(L2);
S4:
                ForceAnimationPlayback(assetEntityId, 5000021, false, true, true);
                Goto(L2);
S5:
                ForceAnimationPlayback(assetEntityId, 6000021, false, true, true);
                Goto(L2);
S6:
                ForceAnimationPlayback(assetEntityId, 7000021, false, true, true);
                Goto(L2);
S7:
                ForceAnimationPlayback(assetEntityId, 8000021, false, true, true);
                Goto(L2);
S8:
                ForceAnimationPlayback(assetEntityId, 9000021, false, true, true);
                Goto(L2);
S9:
                ForceAnimationPlayback(assetEntityId, 10000021, false, true, true);
            } else {
L1:
                if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                    SetNetworkconnectedEventFlagID(eventFlagId4, ON);
                }
                ForceAnimationPlayback(entityId2, 1, false, false, true);
                WaitFixedTimeSeconds(0.5);
                GotoIf(S19, value == 10);
                GotoIf(S18, value == 9);
                GotoIf(S17, value == 8);
                GotoIf(S16, value == 7);
                GotoIf(S15, value == 6);
                GotoIf(S14, value == 5);
                GotoIf(S13, value == 4);
                GotoIf(S12, value == 3);
                GotoIf(S11, value == 2);
                GotoIf(S10, value == 1);
                ForceAnimationPlayback(assetEntityId, 21, false, true, true);
                Goto(L11);
S10:
                ForceAnimationPlayback(assetEntityId, 1000021, false, true, true);
                Goto(L11);
S11:
                ForceAnimationPlayback(assetEntityId, 2000021, false, true, true);
                Goto(L11);
S12:
                ForceAnimationPlayback(assetEntityId, 3000021, false, true, true);
                Goto(L11);
S13:
                ForceAnimationPlayback(assetEntityId, 4000021, false, true, true);
                Goto(L11);
S14:
                ForceAnimationPlayback(assetEntityId, 5000021, false, true, true);
                Goto(L11);
S15:
                ForceAnimationPlayback(assetEntityId, 6000021, false, true, true);
                Goto(L11);
S16:
                ForceAnimationPlayback(assetEntityId, 7000021, false, true, true);
                Goto(L11);
S17:
                ForceAnimationPlayback(assetEntityId, 8000021, false, true, true);
                Goto(L11);
S18:
                ForceAnimationPlayback(assetEntityId, 9000021, false, true, true);
                Goto(L11);
S19:
                ForceAnimationPlayback(assetEntityId, 10000021, false, true, true);
L11:
                if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                    SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
                }
            }
L2:
            WaitFor(
                AssetBackread(assetEntityId)
                    && (!AllPlayersInArea(areaEntityId4) || EventFlag(eventFlagId)));
            ForceAnimationPlayback(entityId, 3, false, false, true);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
                GotoIf(S29, value == 10);
                GotoIf(S28, value == 9);
                GotoIf(S27, value == 8);
                GotoIf(S26, value == 7);
                GotoIf(S25, value == 6);
                GotoIf(S24, value == 5);
                GotoIf(S23, value == 4);
                GotoIf(S22, value == 3);
                GotoIf(S21, value == 2);
                GotoIf(S20, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, false, true);
                Goto(L12);
S20:
                ForceAnimationPlayback(assetEntityId, 1000110, false, false, true);
                Goto(L12);
S21:
                ForceAnimationPlayback(assetEntityId, 2000110, false, false, true);
                Goto(L12);
S22:
                ForceAnimationPlayback(assetEntityId, 3000110, false, false, true);
                Goto(L12);
S23:
                ForceAnimationPlayback(assetEntityId, 4000110, false, false, true);
                Goto(L12);
S24:
                ForceAnimationPlayback(assetEntityId, 5000110, false, false, true);
                Goto(L12);
S25:
                ForceAnimationPlayback(assetEntityId, 6000110, false, false, true);
                Goto(L12);
S26:
                ForceAnimationPlayback(assetEntityId, 7000110, false, false, true);
                Goto(L12);
S27:
                ForceAnimationPlayback(assetEntityId, 8000110, false, false, true);
                Goto(L12);
S28:
                ForceAnimationPlayback(assetEntityId, 9000110, false, false, true);
                Goto(L12);
S29:
                ForceAnimationPlayback(assetEntityId, 10000110, false, false, true);
            } else {
L3:
                GotoIf(S39, value == 10);
                GotoIf(S38, value == 9);
                GotoIf(S37, value == 8);
                GotoIf(S36, value == 7);
                GotoIf(S35, value == 6);
                GotoIf(S34, value == 5);
                GotoIf(S33, value == 4);
                GotoIf(S32, value == 3);
                GotoIf(S31, value == 2);
                GotoIf(S30, value == 1);
                ForceAnimationPlayback(assetEntityId, 110, false, true, true);
                Goto(L12);
S30:
                ForceAnimationPlayback(assetEntityId, 1000110, false, true, true);
                Goto(L12);
S31:
                ForceAnimationPlayback(assetEntityId, 2000110, false, true, true);
                Goto(L12);
S32:
                ForceAnimationPlayback(assetEntityId, 3000110, false, true, true);
                Goto(L12);
S33:
                ForceAnimationPlayback(assetEntityId, 4000110, false, true, true);
                Goto(L12);
S34:
                ForceAnimationPlayback(assetEntityId, 5000110, false, true, true);
                Goto(L12);
S35:
                ForceAnimationPlayback(assetEntityId, 6000110, false, true, true);
                Goto(L12);
S36:
                ForceAnimationPlayback(assetEntityId, 7000110, false, true, true);
                Goto(L12);
S37:
                ForceAnimationPlayback(assetEntityId, 8000110, false, true, true);
                Goto(L12);
S38:
                ForceAnimationPlayback(assetEntityId, 9000110, false, true, true);
                Goto(L12);
S39:
                ForceAnimationPlayback(assetEntityId, 10000110, false, true, true);
            }
L12:
            RestartEvent();
        }
L0:
        area2 = InArea(10000, areaEntityId);
        flag2 = EventFlag(eventFlagId);
        areaSpFlag &= InArea(10000, areaEntityId4) && !CharacterHasSpEffect(10000, 4800);
        if (eventFlagId5 != 0) {
            areaSpFlag &= EventFlag(eventFlagId5);
        }
        WaitFor(area2 || flag2 || areaSpFlag);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, ON);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
        SetEventFlagID(eventFlagId2, ON);
        if (!area2.Passed) {
            GotoIf(L4, EventFlag(eventFlagId4));
            ForceAnimationPlayback(entityId, 1, false, false, true);
            GotoIf(S49, value == 10);
            GotoIf(S48, value == 9);
            GotoIf(S47, value == 8);
            GotoIf(S46, value == 7);
            GotoIf(S45, value == 6);
            GotoIf(S44, value == 5);
            GotoIf(S43, value == 4);
            GotoIf(S42, value == 3);
            GotoIf(S41, value == 2);
            GotoIf(S40, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L5);
S40:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L5);
S41:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L5);
S42:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L5);
S43:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
            Goto(L5);
S44:
            ForceAnimationPlayback(assetEntityId, 5000012, false, true, true);
            Goto(L5);
S45:
            ForceAnimationPlayback(assetEntityId, 6000012, false, true, true);
            Goto(L5);
S46:
            ForceAnimationPlayback(assetEntityId, 7000012, false, true, true);
            Goto(L5);
S47:
            ForceAnimationPlayback(assetEntityId, 8000012, false, true, true);
            Goto(L5);
S48:
            ForceAnimationPlayback(assetEntityId, 9000012, false, true, true);
            Goto(L5);
S49:
            ForceAnimationPlayback(assetEntityId, 10000012, false, true, true);
        } else {
L4:
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, ON);
            }
            ForceAnimationPlayback(entityId, 1, false, false, true);
            WaitFixedTimeSeconds(0.5);
            GotoIf(S59, value == 10);
            GotoIf(S58, value == 9);
            GotoIf(S57, value == 8);
            GotoIf(S56, value == 7);
            GotoIf(S55, value == 6);
            GotoIf(S54, value == 5);
            GotoIf(S53, value == 4);
            GotoIf(S52, value == 3);
            GotoIf(S51, value == 2);
            GotoIf(S50, value == 1);
            ForceAnimationPlayback(assetEntityId, 12, false, true, true);
            Goto(L14);
S50:
            ForceAnimationPlayback(assetEntityId, 1000012, false, true, true);
            Goto(L14);
S51:
            ForceAnimationPlayback(assetEntityId, 2000012, false, true, true);
            Goto(L14);
S52:
            ForceAnimationPlayback(assetEntityId, 3000012, false, true, true);
            Goto(L14);
S53:
            ForceAnimationPlayback(assetEntityId, 4000012, false, true, true);
            Goto(L14);
S54:
            ForceAnimationPlayback(assetEntityId, 5000012, false, true, true);
            Goto(L14);
S55:
            ForceAnimationPlayback(assetEntityId, 6000012, false, true, true);
            Goto(L14);
S56:
            ForceAnimationPlayback(assetEntityId, 7000012, false, true, true);
            Goto(L14);
S57:
            ForceAnimationPlayback(assetEntityId, 8000012, false, true, true);
            Goto(L14);
S58:
            ForceAnimationPlayback(assetEntityId, 9000012, false, true, true);
            Goto(L14);
S59:
            ForceAnimationPlayback(assetEntityId, 10000012, false, true, true);
L14:
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
            }
        }
L5:
        WaitFor(
            AssetBackread(assetEntityId)
                && (!AllPlayersInArea(areaEntityId3) || !EventFlag(eventFlagId)));
        ForceAnimationPlayback(entityId2, 3, false, false, true);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId3, OFF);
            GotoIf(S69, value == 10);
            GotoIf(S68, value == 9);
            GotoIf(S67, value == 8);
            GotoIf(S66, value == 7);
            GotoIf(S65, value == 6);
            GotoIf(S64, value == 5);
            GotoIf(S63, value == 4);
            GotoIf(S62, value == 3);
            GotoIf(S61, value == 2);
            GotoIf(S60, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, false, true);
            Goto(L15);
S60:
            ForceAnimationPlayback(assetEntityId, 1000120, false, false, true);
            Goto(L15);
S61:
            ForceAnimationPlayback(assetEntityId, 2000120, false, false, true);
            Goto(L15);
S62:
            ForceAnimationPlayback(assetEntityId, 3000120, false, false, true);
            Goto(L15);
S63:
            ForceAnimationPlayback(assetEntityId, 4000120, false, false, true);
            Goto(L15);
S64:
            ForceAnimationPlayback(assetEntityId, 5000120, false, false, true);
            Goto(L15);
S65:
            ForceAnimationPlayback(assetEntityId, 6000120, false, false, true);
            Goto(L15);
S66:
            ForceAnimationPlayback(assetEntityId, 7000120, false, false, true);
            Goto(L15);
S67:
            ForceAnimationPlayback(assetEntityId, 8000120, false, false, true);
            Goto(L15);
S68:
            ForceAnimationPlayback(assetEntityId, 9000120, false, false, true);
            Goto(L15);
S69:
            ForceAnimationPlayback(assetEntityId, 10000120, false, false, true);
        } else {
L6:
            GotoIf(S79, value == 10);
            GotoIf(S78, value == 9);
            GotoIf(S77, value == 8);
            GotoIf(S76, value == 7);
            GotoIf(S75, value == 6);
            GotoIf(S74, value == 5);
            GotoIf(S73, value == 4);
            GotoIf(S72, value == 3);
            GotoIf(S71, value == 2);
            GotoIf(S70, value == 1);
            ForceAnimationPlayback(assetEntityId, 120, false, true, true);
            Goto(L15);
S70:
            ForceAnimationPlayback(assetEntityId, 1000120, false, true, true);
            Goto(L15);
S71:
            ForceAnimationPlayback(assetEntityId, 2000120, false, true, true);
            Goto(L15);
S72:
            ForceAnimationPlayback(assetEntityId, 3000120, false, true, true);
            Goto(L15);
S73:
            ForceAnimationPlayback(assetEntityId, 4000120, false, true, true);
            Goto(L15);
S74:
            ForceAnimationPlayback(assetEntityId, 5000120, false, true, true);
            Goto(L15);
S75:
            ForceAnimationPlayback(assetEntityId, 6000120, false, true, true);
            Goto(L15);
S76:
            ForceAnimationPlayback(assetEntityId, 7000120, false, true, true);
            Goto(L15);
S77:
            ForceAnimationPlayback(assetEntityId, 8000120, false, true, true);
            Goto(L15);
S78:
            ForceAnimationPlayback(assetEntityId, 9000120, false, true, true);
            Goto(L15);
S79:
            ForceAnimationPlayback(assetEntityId, 10000120, false, true, true);
        }
L15:
        RestartEvent();
    }
L9:
    WaitFor(!EventFlag(eventFlagId3));
    RestartEvent();
});

// 【共通】神塔エレベータ_初期設定 -- [Common] Shinto tower elevator_Initial settings
$Event(90005508, Restart, function(eventFlagId, eventFlagId2, value, entityId, assetEntityId, assetEntityId2, eventFlagId3) {
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    if (EventFlag(eventFlagId)) {
        if (value != 10) {
            GotoIf(S8, value == 9);
            GotoIf(S7, value == 8);
            GotoIf(S6, value == 7);
            GotoIf(S5, value == 6);
            GotoIf(S4, value == 5);
            GotoIf(S3, value == 4);
            GotoIf(S2, value == 3);
            GotoIf(S1, value == 2);
            GotoIf(S0, value == 1);
            ForceAnimationPlayback(entityId, 20, false, false, false);
            Goto(L10);
S0:
            ForceAnimationPlayback(entityId, 1000020, false, false, false);
            Goto(L10);
S1:
            ForceAnimationPlayback(entityId, 2000020, false, false, false);
            Goto(L10);
S2:
            ForceAnimationPlayback(entityId, 3000020, false, false, false);
            Goto(L10);
S3:
            ForceAnimationPlayback(entityId, 4000020, false, false, false);
            Goto(L10);
S4:
            ForceAnimationPlayback(entityId, 5000020, false, false, false);
            Goto(L10);
S5:
            ForceAnimationPlayback(entityId, 6000020, false, false, false);
            Goto(L10);
S6:
            ForceAnimationPlayback(entityId, 7000020, false, false, false);
            Goto(L10);
S7:
            ForceAnimationPlayback(entityId, 8000020, false, false, false);
            Goto(L10);
S8:
            ForceAnimationPlayback(entityId, 9000020, false, false, false);
        } else {
            ForceAnimationPlayback(entityId, 10000020, false, false, false);
        }
L10:
        SetEventFlagID(eventFlagId2, ON);
        ReproduceAssetAnimation(assetEntityId, 1);
        EndEvent();
    }
L0:
    GotoIf(S18, value == 10);
    GotoIf(S17, value == 9);
    GotoIf(S16, value == 8);
    GotoIf(S15, value == 7);
    GotoIf(S14, value == 6);
    GotoIf(S13, value == 5);
    GotoIf(S12, value == 4);
    GotoIf(S11, value == 3);
    GotoIf(S10, value == 2);
    GotoIf(S9, value == 1);
    ForceAnimationPlayback(entityId, 10, false, false, true);
    Goto(L15);
S9:
    ForceAnimationPlayback(entityId, 1000010, false, false, true);
    Goto(L15);
S10:
    ForceAnimationPlayback(entityId, 2000010, false, false, true);
    Goto(L15);
S11:
    ForceAnimationPlayback(entityId, 3000010, false, false, true);
    Goto(L15);
S12:
    ForceAnimationPlayback(entityId, 4000010, false, false, true);
    Goto(L15);
S13:
    ForceAnimationPlayback(entityId, 5000010, false, false, true);
    Goto(L15);
S14:
    ForceAnimationPlayback(entityId, 6000010, false, false, true);
    Goto(L15);
S15:
    ForceAnimationPlayback(entityId, 7000010, false, false, true);
    Goto(L15);
S16:
    ForceAnimationPlayback(entityId, 8000010, false, false, true);
    Goto(L15);
S17:
    ForceAnimationPlayback(entityId, 9000010, false, false, true);
    Goto(L15);
S18:
    ForceAnimationPlayback(entityId, 10000010, false, false, true);
L15:
    SetEventFlagID(eventFlagId2, OFF);
    ReproduceAssetAnimation(assetEntityId2, 1);
    EndEvent();
});

// 【共通】一方通行扉_鍵付き扉 -- [Common] One-way door_locked door
$Event(90005510, Default, function(eventFlagId, assetEntityId, objactEventFlag, objactParamId, messageId, value) {
    EndIf(!PlayerIsInOwnWorld());
    if (!EventFlag(eventFlagId)) {
        WaitFor(PlayerIsInOwnWorld() && ObjActEventFlag(objactEventFlag));
        WaitFixedTimeRealFrames(1);
        DisplayGenericDialog(messageId, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
        SetEventFlagID(eventFlagId, ON);
    }
L0:
    if (value != 1) {
        DisableObjAct(assetEntityId, objactParamId);
    }
    EndEvent();
});

// 【共通】一方通行扉_領域扉 -- [Common] One-way door_area door
$Event(90005511, Default, function(eventFlagId, assetEntityId, objactEventFlag, objactParamId, value) {
    if (!EventFlag(eventFlagId)) {
        WaitFor(ObjActEventFlag(objactEventFlag));
        SetEventFlagID(eventFlagId, ON);
    }
L0:
    EndIf(value == 1);
    DisableObjActAssignIdx(assetEntityId, objactParamId, 0);
    DisableObjActAssignIdx(assetEntityId, objactParamId, 1);
    DisableObjActAssignIdx(assetEntityId, objactParamId, 2);
    DisableObjActAssignIdx(assetEntityId, objactParamId, 3);
    EndEvent();
});

// 【共通】一方通行扉_領域扉_特殊効果付与 -- [Common] One-way door_Area door_Special effects added
$Event(90005512, Default, function(eventFlagId, areaEntityId, areaEntityId2) {
    DisableNetworkSync();
    if (!EventFlag(eventFlagId)) {
        WaitFor(EventFlag(eventFlagId) || (InArea(10000, areaEntityId) && PlayerIsInOwnWorld()));
        RestartIf(EventFlag(eventFlagId));
        SetSpEffect(10000, 4150);
        WaitFixedTimeSeconds(3);
        RestartEvent();
    }
L0:
    WaitFor(InArea(10000, areaEntityId) || InArea(10000, areaEntityId2));
    SetSpEffect(10000, 4150);
    WaitFixedTimeSeconds(3);
    RestartEvent();
});

// 【共通】一方通行扉_レバー扉 -- [Common] One-way door_Lever door
$Event(90005513, Restart, function(eventFlagId, assetEntityId, assetEntityId2, objactEventFlag, objactParamId, animationId, animationId2) {
    if (EventFlag(eventFlagId)) {
        DisableObjAct(assetEntityId2, objactParamId);
        ReproduceAssetAnimation(assetEntityId, animationId2);
        EndEvent();
    }
L0:
    WaitFor(!EventFlag(eventFlagId) && ObjActEventFlag(objactEventFlag));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    DisableObjAct(assetEntityId2, objactParamId);
    ForceAnimationPlayback(assetEntityId, animationId, false, false, false);
});

// 【共通】両開き扉_エラーメッセージ -- [Common] Double door_error message
$Event(90005515, Default, function(eventFlagId, entityId) {
    DisableNetworkSync();
    WaitFor((PlayerIsInOwnWorld() && ActionButtonInArea(7101, entityId)) || EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId));
    DisplayGenericDialog(4010, PromptType.OKCANCEL, NumberofOptions.OneButton, entityId, 3);
    RestartEvent();
});

// 【共通】蹴りおろし梯子 -- [Common] Kick-down ladder
$Event(90005520, Restart, function(eventFlagId, assetEntityId, eventFlagId2, eventFlagId3) {
    if (EventFlag(eventFlagId)) {
        ReproduceAssetAnimation(assetEntityId, 2);
        RegisterLadder(eventFlagId2, eventFlagId3, assetEntityId);
        EndEvent();
    }
L0:
    WaitFor(PlayerIsInOwnWorld() && ActionButtonInArea(9200, assetEntityId));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    if (PlayerIsInOwnWorld()) {
        RotateCharacter(10000, assetEntityId, 60210, false);
    }
    ForceAnimationPlayback(assetEntityId, 1, false, true, false);
    RegisterLadder(eventFlagId2, eventFlagId3, assetEntityId);
});

// 【共通】魔法壁 -- [Common] Magic wall
$Event(90005525, Restart, function(eventFlagId, assetEntityId) {
    if (!EventFlag(eventFlagId)) {
        WaitFor(
            PlayerIsInOwnWorld() && HasDamageType(assetEntityId, 20000, DamageType.Unspecified));
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
        ForceAnimationPlayback(assetEntityId, 1, false, true, false);
    }
L0:
    DisableAsset(assetEntityId);
});

// 【共通】魔法封印壁 -- [Common] Magic sealing wall
$Event(900055278, Restart, function(eventFlagId, assetEntityId, sfxId, actionButtonParameterId, messageId, value, value2, value3) {
    if (EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
L0:
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 101, sfxId);
    onlineAct = PlayerIsInOwnWorld() && ActionButtonInArea(actionButtonParameterId, assetEntityId);
    flag = EventFlag(eventFlagId);
    WaitFor(onlineAct || flag);
    if (!flag.Passed) {
        DisplayGenericDialog(messageId, PromptType.YESNO, NumberofOptions.NoButtons, eventFlagId, 3);
        WaitFixedTimeSeconds(1);
        RestartEvent();
    }
L1:
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    DeleteAssetfollowingSFX(assetEntityId, true);
    DisableAsset(assetEntityId);
    EndEvent();
    EndIf(Signed(value) == 0);
    EndIf(Signed(value2) == 0);
    EndIf(Signed(value3) == 0);
});

// 【共通】レバー操作ギミック -- [Common] Lever operation gimmick
$Event(90005540, Restart, function(eventFlagId, assetEntityId, assetEntityId2, objactEventFlag, objactParamId, animationId, animationId2) {
    if (EventFlag(eventFlagId)) {
        DisableObjAct(assetEntityId2, objactParamId);
        ReproduceAssetAnimation(assetEntityId, animationId2);
        EndEvent();
    }
L0:
    WaitFor(!EventFlag(eventFlagId) && ObjActEventFlag(objactEventFlag));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    DisableObjAct(assetEntityId2, objactParamId);
    ForceAnimationPlayback(assetEntityId, animationId, false, false, false);
});

// 【共通】宝箱 -- [Common] Treasure chest
$Event(90005550, Restart, function(eventFlagId, assetEntityId, objactEventFlag) {
    if (EventFlag(eventFlagId)) {
        ReproduceAssetAnimation(assetEntityId, 1);
        DisableObjAct(assetEntityId, -1);
        EnableAssetTreasure(assetEntityId);
        EndEvent();
    }
L0:
    DisableAssetTreasure(assetEntityId);
    WaitFor(ObjActEventFlag(objactEventFlag));
    WaitFixedTimeFrames(10);
    EnableAssetTreasure(assetEntityId);
    SetEventFlagID(eventFlagId, ON);
});

$Event(90005555, Restart, function(eventFlagId, itemLotId, assetEntityId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    CreateAssetfollowingSFX(assetEntityId, 100, 842050);
    WaitFor(PlayerIsInOwnWorld() && ActionButtonInArea(209200, assetEntityId));
    RotateCharacter(10000, assetEntityId, -1, true);
    ForceAnimationPlayback(10000, 61040, false, false, false);
    WaitFixedTimeSeconds(0.5);
    PlaySE(assetEntityId, SoundType.EnvironmentalSound, 420009000);
    WaitFixedTimeSeconds(1.5);
    DeleteAssetfollowingSFX(assetEntityId, true);
    SpawnOneshotSFX(TargetEntityType.Asset, assetEntityId, 100, 842051);
    WaitFixedTimeSeconds(1.5);
    AwardItemsIncludingClients(itemLotId);
});

$Event(90005556, Restart, function(assetEntityId, eventFlagId) {
    DisableAssetTreasure(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(EventFlag(eventFlagId));
    WaitFor(TimeOfDayInRange(20, 0, 0, 5, 59, 59));
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 100, 861245);
    EnableAssetTreasure(assetEntityId);
    WaitFor(!TimeOfDayInRange(20, 0, 0, 5, 59, 59) || EventFlag(eventFlagId));
    RestartEvent();
});

$Event(90005557, Restart, function(entityId) {
    ForceAnimationPlayback(entityId, 3, false, false, false);
    WaitFor(TimeOfDayInRange(20, 0, 0, 5, 59, 59));
    ForceAnimationPlayback(entityId, 2, false, false, false);
    WaitFixedTimeSeconds(6);
    ForceAnimationPlayback(entityId, 0, false, false, false);
    WaitFor(!TimeOfDayInRange(20, 0, 0, 5, 59, 59));
    ForceAnimationPlayback(entityId, 1, false, false, false);
    WaitFixedTimeSeconds(6);
    RestartEvent();
});

// 【共通】破壊アセット宝 -- [Common] Destruction asset treasure
$Event(90005560, Restart, function(eventFlagId, assetEntityId, value) {
    if (EventFlag(eventFlagId)) {
        ReproduceAssetDestruction(assetEntityId, 1);
        EnableAssetTreasure(assetEntityId);
        EndEvent();
    }
L0:
    if (Signed(value) == 0) {
        DeleteAssetfollowingSFX(assetEntityId, true);
        CreateAssetfollowingSFX(assetEntityId, 200, 803300);
    }
    DisableAssetTreasure(assetEntityId);
    WaitFor(AssetDestroyed(assetEntityId));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    EnableAssetTreasure(assetEntityId);
    if (Signed(value) == 0) {
        DeleteAssetfollowingSFX(assetEntityId, true);
    }
});

// 【共通】ジェスチャー入手 -- [Common] Get gesture
$Event(90005570, Default, function(eventFlagId, gestureParamId, assetEntityId, value, value2, value3) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    if (Signed(value2) == 3) {
        CreateAssetfollowingSFX(assetEntityId, 90, 6103);
    } else if (Signed(value2) == 2) {
        CreateAssetfollowingSFX(assetEntityId, 90, 6102);
    } else if (Signed(value2) == 1) {
        CreateAssetfollowingSFX(assetEntityId, 90, 6101);
    } else {
        CreateAssetfollowingSFX(assetEntityId, 90, 6100);
    }
L1:
    onlineFlagAct &= PlayerIsInOwnWorld() && !EventFlag(eventFlagId);
    if (Signed(value) == 2) {
        onlineFlagAct &= ActionButtonInArea(4250, assetEntityId);
    } else if (Signed(value) == 1) {
        onlineFlagAct &= ActionButtonInArea(4300, assetEntityId);
    } else {
        onlineFlagAct &= ActionButtonInArea(4200, assetEntityId);
    }
L2:
    WaitFor(onlineFlagAct || EventFlag(eventFlagId));
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(EventFlag(eventFlagId));
    WaitFixedTimeRealFrames(1);
    AwardGesture(gestureParamId);
    SetEventFlagID(eventFlagId, ON);
    EndIf(Signed(0) == value3);
});

// 【共通】ジェスチャー入手with宝 -- [Common] Gesture acquisition with treasure
$Event(900005571, Default, function(eventFlagId, gestureParamId, eventFlagId2, value) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(PlayerIsInOwnWorld() && EventFlag(eventFlagId2));
    AwardGesture(gestureParamId);
    SetEventFlagID(eventFlagId, ON);
    EndIf(Signed(0) == value);
});

$Event(900005580, Restart, function(eventFlagId, assetEntityId, eventFlagId2) {
    DisableAsset(assetEntityId);
    DisableAssetTreasure(assetEntityId);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId) || EventFlag(eventFlagId2));
    EndIf(EventFlag(eventFlagId));
    EnableAsset(assetEntityId);
    EnableAssetTreasure(assetEntityId);
    WaitFor(EventFlag(eventFlagId));
    DisableAsset(assetEntityId);
    DisableAssetTreasure(assetEntityId);
});

$Event(900005590, Default, function(eventFlagId, assetEntityId, eventFlagId2) {
    DisableAsset(assetEntityId);
    DisableAssetTreasure(assetEntityId);
    if (PlayerIsInOwnWorld()) {
        DisableObjAct(assetEntityId, -1);
    }
    EndIf(!EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId));
    EnableAsset(assetEntityId);
    if (eventFlagId2 != 0) {
        if (PlayerIsInOwnWorld()) {
            EnableObjAct(assetEntityId, -1);
        }
    }
    if (!(eventFlagId2 != 0 && !EventFlag(eventFlagId2))) {
        EnableAssetTreasure(assetEntityId);
    }
});

// 【共通】フィールド篝火登録 -- [Common] Field bonfire registration
$Event(90005600, Restart, function(eventFlagId, assetEntityId, enemyDeactivationDistance, chrEntityId) {
    RegisterBonfire(eventFlagId, assetEntityId, 0, 0, 0, enemyDeactivationDistance);
    if (0 != chrEntityId) {
        DisableCharacterCollision(chrEntityId);
    }
    if (!EventFlag(eventFlagId)) {
        WaitFor(
            PlayerIsInOwnWorld()
                && EntityInRadiusOfEntity(10000, assetEntityId, 5, 1)
                && EventFlag(eventFlagId));
        EndIf(0 == chrEntityId);
        DisableCharacterCollision(chrEntityId);
        SetSpEffect(chrEntityId, 530);
        WaitFixedTimeSeconds(1.5);
    }
L0:
    DisableCharacter(chrEntityId);
});

// 【共通】汎用ワープ -- [Common] General purpose warp
$Event(90005605, Restart, function(assetEntityId, areaId, blockId, regionId, indexId, initialAreaEntityId, subareaNamePopupMessageId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, messageId, timeSeconds, timeSeconds2) {
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId2, OFF);
    SetEventFlagID(eventFlagId3, OFF);
    if (!ThisEventSlot()) {
        DeleteAssetfollowingSFX(assetEntityId, true);
        SetEventFlagID(eventFlagId, OFF);
        WaitFixedTimeFrames(1);
    }
    onlineFlag |= HasMultiplayerState(MultiplayerState.Multiplayer)
        || HasMultiplayerState(MultiplayerState.MultiplayerPending);
    if (eventFlagId4 != 0) {
        onlineFlag |= !EventFlag(eventFlagId4);
    }
    if (!onlineFlag) {
        if (!EventFlag(eventFlagId)) {
            CreateAssetfollowingSFX(assetEntityId, 200, 806870);
            SetEventFlagID(eventFlagId, ON);
        }
    }
L1:
    onlineFlagAct &= PlayerIsInOwnWorld()
        && !(HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending));
    if (eventFlagId4 != 0) {
        if (Signed(messageId) == 0) {
            onlineFlagAct &= EventFlag(eventFlagId4) && EventFlag(eventFlagId);
        }
    }
    onlineFlagAct &= ActionButtonInArea(9140, assetEntityId);
    onlineFlag2 |= HasMultiplayerState(MultiplayerState.Multiplayer)
        || HasMultiplayerState(MultiplayerState.MultiplayerPending);
    if (eventFlagId4 != 0) {
        onlineFlag2 |= !EventFlag(eventFlagId4);
    }
    onlineFlag3 = onlineFlag2 && EventFlag(eventFlagId);
    onlineFlag4 |= HasMultiplayerState(MultiplayerState.Multiplayer)
        || HasMultiplayerState(MultiplayerState.MultiplayerPending);
    if (eventFlagId4 != 0) {
        onlineFlag4 |= !EventFlag(eventFlagId4);
    }
    onlineFlag5 = !onlineFlag4 && !EventFlag(eventFlagId);
    flag = EventFlagState(CHANGE, TargetEventFlagType.EventFlag, eventFlagId4);
    onlineFlagAct2 |= onlineFlagAct || onlineFlag3 || onlineFlag5;
    if (eventFlagId4 != 0) {
        onlineFlagAct2 |= flag;
    }
    WaitFor(onlineFlagAct2);
    if (!onlineFlagAct.Passed) {
        if (onlineFlag3.Passed) {
            DeleteAssetfollowingSFX(assetEntityId, true);
            SetEventFlagID(eventFlagId, OFF);
        }
L2:
        WaitFixedTimeSeconds(0.033);
        RestartEvent();
    }
L3:
    if (!(eventFlagId4 == 0 || Signed(messageId) == 0)) {
        if (!EventFlag(eventFlagId4)) {
            DisplayGenericDialog(messageId, PromptType.YESNO, NumberofOptions.NoButtons, assetEntityId, 3);
            WaitFixedTimeSeconds(1);
            RestartEvent();
        }
    }
L4:
    DisplayGenericDialogAndSetEventFlags(4300, PromptType.YESNO, NumberofOptions.TwoButtons, assetEntityId, 3, eventFlagId2, eventFlagId3, eventFlagId3);
    if (!EventFlag(eventFlagId2)) {
        WaitFixedTimeSeconds(1);
        RestartEvent();
    }
L6:
    RestartIf(
        HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending));
    RotateCharacter(10000, assetEntityId, -1, true);
    ForceAnimationPlayback(10000, 60490, false, false, false);
    WaitFixedTimeSeconds(3);
    WarpPlayer(areaId, blockId, regionId, indexId, initialAreaEntityId, subareaNamePopupMessageId);
    RestartEvent();
    WaitFixedTimeSeconds(timeSeconds);
    WaitFixedTimeSeconds(timeSeconds2);
});

// 【共通】馬禁止領域 -- [Common] Horse prohibited area
$Event(900005610, Default, function(assetEntityId, dummypolyId, sfxId, eventFlagId) {
    DisableNetworkSync();
    DeleteAssetfollowingSFX(assetEntityId, true);
    if (0 != eventFlagId) {
        flagChr &= EventFlag(eventFlagId);
    }
    flagChr &= CharacterRidingMount(10000);
    WaitFor(flagChr);
    CreateAssetfollowingSFX(assetEntityId, dummypolyId, sfxId);
    if (0 != eventFlagId) {
        flagChr2 |= !EventFlag(eventFlagId);
    }
    flagChr2 |= !CharacterRidingMount(10000);
    WaitFor(flagChr2);
    RestartEvent();
});

$Event(90005615, Default, function(areaEntityId, eventFlagId) {
    DisableNetworkSync();
    if (eventFlagId != 0) {
        flagAreaOnline &= EventFlag(eventFlagId);
    }
    flagAreaOnline &= InArea(20000, areaEntityId) && !HasMultiplayerState(MultiplayerState.Invasion);
    WaitFor(flagAreaOnline);
    SetSpEffect(20000, 9621);
    WaitFixedTimeSeconds(0.1);
    if (eventFlagId != 0) {
        flagAreaOnline2 |= !EventFlag(eventFlagId);
    }
    flagAreaOnline2 |= !InArea(20000, areaEntityId) || HasMultiplayerState(MultiplayerState.Invasion);
    WaitFor(flagAreaOnline2);
    WaitFixedTimeSeconds(0.1);
    ClearSpEffect(20000, 9621);
    RestartEvent();
});

// 【共通】震える死の根 -- [Common] Trembling roots of death
$Event(90005616, Default, function(eventFlagId, areaEntityId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(
        PlayerIsInOwnWorld()
            && !EventFlag(eventFlagId)
            && EventFlag(400239)
            && InArea(10000, areaEntityId));
    DisplayBlinkingMessage(20600);
});

// 【共通】ガーゴイル像 -- [Common] Gargoyle statue
$Event(90005620, Default, function(eventFlagId, assetEntityId, assetEntityId2, assetEntityId3, eventFlagId2, eventFlagId3, value) {
    DisableNetworkSync();
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    SetEventFlagID(eventFlagId2, OFF);
    SetEventFlagID(eventFlagId3, OFF);
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 200, 806040);
    if (assetEntityId3 != 0) {
        CreateAssetfollowingSFX(assetEntityId, 201, 806040);
    }
    DisableAsset(assetEntityId2);
    if (assetEntityId3 != 0) {
        DisableAsset(assetEntityId3);
    }
    WaitFor(
        (PlayerIsInOwnWorld() && ActionButtonInArea(9220, assetEntityId)) || EventFlag(eventFlagId));
    if (!EventFlag(eventFlagId)) {
        DisplayGenericDialogAndSetEventFlags(108000, PromptType.YESNO, NumberofOptions.TwoButtons, assetEntityId, 1.75, eventFlagId2, eventFlagId3, eventFlagId3);
        if (!EventFlag(eventFlagId2)) {
            WaitFixedTimeSeconds(0.5);
            RestartEvent();
        }
L1:
        StoreItemAmountHeldInEventValue(ItemType.Goods, 8000, 9580, 8);
        GotoIf(L2, assetEntityId3 != 0);
        GotoIf(L3, EventValue(9580, 8) >= 1);
L2:
        GotoIf(L4, EventValue(9580, 8) >= 2);
        ForceAnimationPlayback(10000, 50050, false, false, false);
        WaitFixedTimeSeconds(1.4);
        if (EventValue(9580, 8) < 1) {
            DisplayGenericDialog(308000, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
            RestartEvent();
        }
L5:
        DisplayGenericDialog(408000, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
        RestartEvent();
L3:
        IssueShortWarpRequest(10000, TargetEntityType.Asset, assetEntityId, 191);
        ForceAnimationPlayback(10000, 60810, false, false, false);
        WaitFixedTimeSeconds(2.7);
        DisplayGenericDialog(208000, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
        EnableAsset(assetEntityId2);
        RemoveItemFromPlayer(ItemType.Goods, 8000, 1);
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
        Goto(L8);
L4:
        IssueShortWarpRequest(10000, TargetEntityType.Asset, assetEntityId, 191);
        ForceAnimationPlayback(10000, 60810, false, false, false);
        WaitFixedTimeSeconds(2.67);
        EnableAsset(assetEntityId2);
        ForceAnimationPlayback(10000, 60811, false, false, false);
        WaitFixedTimeSeconds(1.5);
        DisplayGenericDialog(208000, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
        EnableAsset(assetEntityId3);
        RemoveItemFromPlayer(ItemType.Goods, 8000, 2);
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    } else {
L9:
        EnableAsset(assetEntityId2);
        EnableAsset(assetEntityId3);
    }
L8:
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndEvent();
    EndIf(Signed(0) == value);
});

// 【共通】ガーゴイル像_封印扉 -- [Common] Gargoyle statue_Sealed door
$Event(90005621, Default, function(eventFlagId, assetEntityId) {
    if (EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
L0:
    CreateAssetfollowingSFX(assetEntityId, 101, 806042);
    WaitFor(PlayerIsInOwnWorld() && EventFlag(eventFlagId));
    DeleteAssetfollowingSFX(assetEntityId, true);
    PlaySE(assetEntityId, SoundType.SFX, 90011);
    WaitFixedTimeSeconds(0.5);
    DisableAsset(assetEntityId);
});

// 【共通】遠見台 -- [Common] Far viewing platform
$Event(90005630, Restart, function(farviewId, assetEntityId, dummypolyId) {
    DisableNetworkSync();
    WaitFor(PlayerIsInOwnWorld() && ActionButtonInArea(9270, assetEntityId));
    UseFarviewCamera(farviewId, assetEntityId, dummypolyId);
    RotateCharacter(10000, assetEntityId, -1, true);
    RotateCharacter(10000, assetEntityId, 60480, false);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】剣碑解読 -- [Common] Sword monument decipherment
$Event(90005631, Restart, function(entityId, messageId) {
    DisableNetworkSync();
    WaitFor(ActionButtonInArea(9330, entityId));
    DisplayGenericDialog(messageId, PromptType.YESNO, NumberofOptions.NoButtons, entityId, 3);
    WaitFixedTimeSeconds(2);
    RestartEvent();
});

// 【共通】絵画宝探し_アトリエ -- [Common] Painting treasure hunt_Atelier
$Event(90005632, Restart, function(eventFlagId, assetEntityId, itemLotId) {
    EndIf(EventFlag(eventFlagId));
    EndIf(!PlayerIsInOwnWorld());
    DeleteAssetfollowingSFX(assetEntityId, false);
    CreateAssetfollowingSFX(assetEntityId, 200, 806840);
    WaitFor(PlayerIsInOwnWorld() && ActionButtonInArea(9310, assetEntityId));
    DeleteAssetfollowingSFX(assetEntityId, true);
    PlaySE(assetEntityId, SoundType.SFX, 806841);
    WaitFixedTimeSeconds(0.1);
    AwardItemsIncludingClients(itemLotId);
});

// 【共通】絵画宝探し_モチーフ -- [Common] Painting treasure hunt_motif
$Event(90005633, Restart, function(eventFlagId, eventFlagId2, chrEntityId, animationId, animationId2, assetEntityId, assetEntityId2) {
    SetSpEffect(eventFlagId, 10124);
    DisableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    DisableAsset(assetEntityId);
    DisableAsset(assetEntityId2);
    DisableAssetTreasure(assetEntityId2);
    EndIf(EventFlag(eventFlagId));
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        PlayerIsInOwnWorld()
            && EventFlag(eventFlagId2)
            && EntityInRadiusOfEntity(chrEntityId, 10000, 15, 1));
    EnableCharacter(chrEntityId);
    ClearSpEffect(eventFlagId, 10124);
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    EnableAsset(assetEntityId);
    EnableAsset(assetEntityId2);
    ForceAnimationPlayback(assetEntityId, 2, false, false, false);
    WaitFor(
        PlayerIsInOwnWorld()
            && EventFlag(eventFlagId2)
            && EntityInRadiusOfEntity(chrEntityId, 10000, 5, 1));
    ForceAnimationPlayback(chrEntityId, animationId2, false, false, false);
    ForceAnimationPlayback(assetEntityId, 1, false, false, false);
    WaitFixedTimeSeconds(3.8);
    DisableCharacter(chrEntityId);
    DisableAsset(assetEntityId);
    EnableAssetTreasure(assetEntityId2);
});

// 【共通】霊体キャンドル -- [Common] Spirit Candle
$Event(90005636, Restart, function(eventFlagId, chrEntityId, entityId, spEffectId, chrEntityId2, areaEntityId, eventFlagId2, patrolInformationEntityId, value) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        EndEvent();
    }
L0:
    if (!EventFlag(eventFlagId2)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        DisableCharacterAI(chrEntityId);
    }
L1:
    onlineFlag = PlayerIsInOwnWorld() && EventFlag(eventFlagId);
    flagArea = EventFlag(eventFlagId2) && InArea(chrEntityId, areaEntityId);
    onlineFlagAreaAct |= onlineFlag || flagArea;
    onlineFlagAreaAct2 &= PlayerIsInOwnWorld() && !EventFlag(eventFlagId);
    if (EventFlag(eventFlagId2)) {
        onlineFlagAreaAct2 &= !EntityInRadiusOfEntity(10000, chrEntityId, 30, 1);
    }
    onlineFlagAreaAct2 &= ActionButtonInArea(9300, entityId);
    onlineFlagAreaAct |= onlineFlagAreaAct2;
    WaitFor(onlineFlagAreaAct);
    if (EventFlag(eventFlagId2)) {
        SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 905, 643041);
        SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 960, 643040);
        WaitFixedTimeSeconds(0.2);
        DisableCharacter(chrEntityId);
        DisableCharacterAI(chrEntityId);
        if (flagArea.Passed) {
            WarpCharacterAndCopyFloor(chrEntityId, TargetEntityType.Area, chrEntityId2, -1, 10000);
            WaitFixedTimeSeconds(0.1);
        }
L2:
        GotoIf(L3, !onlineFlagAreaAct2.Passed);
    }
L1:
    if (!EventFlag(eventFlagId2)) {
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    }
    WarpCharacterAndCopyFloor(chrEntityId, TargetEntityType.Area, chrEntityId2, -1, 10000);
    if (0 != patrolInformationEntityId) {
        ChangeCharacterPatrolBehavior(chrEntityId, patrolInformationEntityId);
    }
    WaitFixedTimeFrames(1);
    EnableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    ForceAnimationPlayback(chrEntityId, 20028, false, false, false);
    WaitFixedTimeSeconds(0.5);
    EnableCharacterAI(chrEntityId);
    SetSpEffect(chrEntityId, spEffectId);
L3:
    RestartEvent();
    EndIf(Signed(0) == value);
});

// 【共通】霊体キャンドル_出現 -- [Common] Spirit candle_appearance
$Event(90005637, Restart, function(eventFlagId, chrEntityId, areaEntityId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId) || InArea(chrEntityId, areaEntityId));
    EndIf(EventFlag(eventFlagId));
    SetSpEffect(chrEntityId, 4463);
    WaitFixedTimeSeconds(3);
    RestartEvent();
});

$Event(90005638, Restart, function(eventFlagId, assetEntityId, assetEntityId2) {
    if (EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        DisableAsset(assetEntityId2);
        EndEvent();
    }
L0:
    EnableAssetInvunerability(assetEntityId);
    EnableAssetInvunerability(assetEntityId2);
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 100, 841075);
    DeleteAssetfollowingSFX(assetEntityId2, true);
    CreateAssetfollowingSFX(assetEntityId2, 100, 841076);
    WaitFor(PlayerIsInOwnWorld() && AssetHitBy(assetEntityId, 20000));
    DisableAssetInvunerability(assetEntityId);
    RequestAssetDestruction(assetEntityId, 0);
    DeleteAssetfollowingSFX(assetEntityId, true);
    DeleteAssetfollowingSFX(assetEntityId2, true);
    CreateAssetfollowingSFX(assetEntityId, 100, 841072);
    CreateAssetfollowingSFX(assetEntityId2, 100, 841072);
    DisableAssetInvunerability(assetEntityId2);
    WaitFixedTimeRealFrames(1);
    RequestAssetDestruction(assetEntityId2, 0);
    SetEventFlagID(eventFlagId, ON);
    WaitFixedTimeSeconds(2);
    DisplayGenericDialog(2020030, PromptType.OKCANCEL, NumberofOptions.OneButton, 0, 100);
});

$Event(90005639, Restart, function(eventFlagId, assetEntityId, assetEntityId2, assetEntityId3, timeSeconds) {
    if (EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        EnableAssetInvunerability(assetEntityId2);
        EnableAssetTreasure(assetEntityId3);
        EndEvent();
    }
L0:
    DisableAsset(assetEntityId3);
    DisableAssetTreasure(assetEntityId3);
    EnableAssetInvunerability(assetEntityId2);
    EnableAssetInvunerability(assetEntityId);
    WaitFor(PlayerIsInOwnWorld() && AssetHitBy(assetEntityId, 20000));
    DisableAssetInvunerability(assetEntityId);
    RequestAssetDestruction(assetEntityId, 0);
    WaitFixedTimeSeconds(timeSeconds);
    EnableAsset(assetEntityId3);
    EnableAssetTreasure(assetEntityId3);
    SetEventFlagID(eventFlagId, ON);
});

// 【共通】地下迷宮_入口扉 -- [Common] Underground labyrinth_entrance door
$Event(90005640, Restart, function(eventFlagId, assetEntityId) {
    if (EventFlag(eventFlagId)) {
        WaitFor(AssetBackread(assetEntityId));
        ReproduceAssetAnimation(assetEntityId, 2);
        EndEvent();
    }
L0:
    WaitFor(AssetBackread(assetEntityId) && EntityInRadiusOfEntity(10000, assetEntityId, 50, 1));
    SetEventFlagID(eventFlagId, ON);
    ForceAnimationPlayback(assetEntityId, 1, false, false, false);
});

// 【共通】地下小探索_迷宮脱出スペル[仮] -- [Common] Underground exploration_labyrinth escape spell [tentative]
$Event(90005645, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, assetEntityId, initialAreaEntityId, areaId, blockId, regionId, indexId) {
    if (!EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        WaitFor(
            PlayerIsInOwnWorld()
                && !EntityInRadiusOfEntity(10000, assetEntityId, 1, 1)
                && EventFlag(eventFlagId));
    }
L0:
    EnableAsset(assetEntityId);
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.MultiplayerPending)
            || HasMultiplayerState(MultiplayerState.Multiplayer))
            && ActionButtonInArea(9290, assetEntityId));
    DisplayGenericDialogAndSetEventFlags(4100, PromptType.YESNO, NumberofOptions.TwoButtons, assetEntityId, 3, eventFlagId2, eventFlagId3, eventFlagId3);
    if (!EventFlag(eventFlagId2)) {
        SetEventFlagID(eventFlagId3, ON);
        WaitFixedTimeSeconds(2);
        RestartEvent();
    }
L1:
    WaitFixedTimeSeconds(1);
    WarpPlayer(areaId, blockId, regionId, indexId, initialAreaEntityId, 0);
});

// 【共通】地下小探索_迷宮脱出スペル -- [Common] Underground exploration_labyrinth escape spell
$Event(90005646, Default, function(eventFlagId, eventFlagId2, eventFlagId3, assetEntityId, initialAreaEntityId, areaId, blockId, regionId, indexId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(PlayerIsInOwnWorld() && EventFlag(eventFlagId));
    if (!ThisEventSlot()) {
        CreateAssetfollowingSFX(assetEntityId, 190, 1300);
    }
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.MultiplayerPending)
            || HasMultiplayerState(MultiplayerState.Multiplayer))
            && ActionButtonInArea(9290, assetEntityId));
    DisplayGenericDialogAndSetEventFlags(4100, PromptType.YESNO, NumberofOptions.TwoButtons, assetEntityId, 3, eventFlagId2, eventFlagId3, eventFlagId3);
    if (!EventFlag(eventFlagId2)) {
        SetEventFlagID(eventFlagId3, ON);
        WaitFixedTimeSeconds(2);
        RestartEvent();
    }
L1:
    ForceAnimationPlayback(10000, 60460, false, false, false);
    WaitFixedTimeSeconds(2.5);
    WarpPlayer(areaId, blockId, regionId, indexId, initialAreaEntityId, 0);
});

// 【共通】英雄の墓_扉解放 -- [Common] Hero's Tomb_Door release
$Event(90005650, Default, function(eventFlagId, assetEntityId, assetEntityId2, objactEventFlag, objactParamId) {
    if (EventFlag(eventFlagId)) {
        ReproduceAssetAnimation(assetEntityId, 2);
        DisableObjAct(assetEntityId2, objactParamId);
        EndEvent();
    }
L0:
    WaitFor(PlayerIsInOwnWorld() && ObjActEventFlag(objactEventFlag));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    if (PlayerIsInOwnWorld()) {
        DisplayGenericDialog(4200, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId2, 5);
    } else {
        DisplayBlinkingMessage(4200);
    }
    ForceAnimationPlayback(assetEntityId, 1, false, false, false);
    EndEvent();
});

// 【共通】英雄の墓_扉解放_フラグ判定 -- [Common] Hero's Grave_Door Release_Flag Judgment
$Event(90005652, Default, function(eventFlagId, assetEntityId, eventFlagId2) {
    if (EventFlag(eventFlagId)) {
        ReproduceAssetAnimation(assetEntityId, 2);
        EndEvent();
    }
L0:
    WaitFor(PlayerIsInOwnWorld() && EventFlag(eventFlagId2));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    DisplayGenericDialog(4200, PromptType.OKCANCEL, NumberofOptions.NoButtons, 0, 5);
    ForceAnimationPlayback(assetEntityId, 1, false, false, false);
    EndEvent();
});

// 【共通】英雄の墓_扉エラーメッセージ -- [Common] Hero's Tomb_Door error message
$Event(90005651, Default, function(eventFlagId, entityId) {
    DisableNetworkSync();
    WaitFor(ActionButtonInArea(7200, entityId) || EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId));
    DisplayGenericDialog(4001, PromptType.OKCANCEL, NumberofOptions.NoButtons, entityId, 3);
    WaitFixedTimeFrames(1);
    RestartEvent();
});

// 【共通】英雄の墓_弓矢トラップ_TypeA -- [Common] Hero's Grave_Bow and Arrow Trap_TypeA
$Event(90005660, Default, function(chrEntityId, entityId, areaEntityId, behaviorId, entityId2, entityId3, entityId4) {
    CreateBulletOwner(chrEntityId);
    WaitFor(InArea(10000, areaEntityId));
    ForceAnimationPlayback(entityId, 1, false, true, false);
    WaitFixedTimeSeconds(0.5);
    if (Signed(behaviorId) != 0) {
        ShootBullet(chrEntityId, entityId2, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, behaviorId, 0, 0, 0);
    } else {
        ShootBullet(chrEntityId, entityId2, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, 102000, 0, 0, 0);
    }
    WaitFixedTimeSeconds(0.6);
    if (Signed(behaviorId) != 0) {
        ShootBullet(chrEntityId, entityId2, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, behaviorId, 0, 0, 0);
    } else {
        ShootBullet(chrEntityId, entityId2, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, 102000, 0, 0, 0);
    }
    WaitFixedTimeSeconds(0.6);
    if (Signed(behaviorId) != 0) {
        ShootBullet(chrEntityId, entityId2, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, behaviorId, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, behaviorId, 0, 0, 0);
    } else {
        ShootBullet(chrEntityId, entityId2, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId3, -1, 102000, 0, 0, 0);
        ShootBullet(chrEntityId, entityId4, -1, 102000, 0, 0, 0);
    }
    WaitFixedTimeSeconds(3);
    WaitFor(!AllPlayersInArea(areaEntityId));
    ForceAnimationPlayback(entityId, 3, false, true, false);
    RestartEvent();
});

// 【共通】英雄の墓_トラップエレベータ -- [Common] Hero's Tomb_Trap Elevator
$Event(90005670, Default, function(eventFlagId, eventFlagId2, eventFlagId3, entityId, areaEntityId, areaEntityId2, eventFlagId4) {
    if (!EventFlag(eventFlagId2)) {
        WaitFor(
            ((CharacterType(10000, TargetType.Alive)
                || CharacterType(10000, TargetType.BluePhantom)
                || CharacterType(10000, TargetType.WhitePhantom))
                && InArea(10000, areaEntityId)
                && !EventFlag(eventFlagId))
                || EventFlag(eventFlagId2));
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
        ForceAnimationPlayback(entityId, 12, false, true, false);
    }
L0:
    GotoIf(L10, !AllPlayersInArea(areaEntityId2));
    GotoIf(S0, 0 == eventFlagId4);
    GotoIf(L10, !EventFlag(eventFlagId4));
S0:
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    }
    SetEventFlagID(eventFlagId3, ON);
    ForceAnimationPlayback(entityId, 20, false, true, false);
    RestartEvent();
L10:
    WaitFixedTimeSeconds(0.1);
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
    }
    ForceAnimationPlayback(entityId, 21, false, true, false);
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
        ForceAnimationPlayback(entityId, 10, false, false, false);
    } else {
        ForceAnimationPlayback(entityId, 10, false, true, false);
    }
    RestartEvent();
});

// 【共通】英雄の墓_トラップエレベータ_闇霊排除 -- [Common] Hero's Tomb_Trap Elevator_Dark Spirit Elimination
$Event(90005673, Default, function(eventFlagId, areaEntityId) {
    WaitFor(
        (CharacterType(10000, TargetType.Alive)
            || CharacterType(10000, TargetType.WhitePhantom)
            || CharacterType(10000, TargetType.BluePhantom))
            && InArea(10000, areaEntityId));
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
    chrArea = (CharacterType(10000, TargetType.BlackPhantom)
        || CharacterType(10000, TargetType.Invader)
        || CharacterType(10000, TargetType.Invader2)
        || CharacterType(10000, TargetType.Invader3))
        && InArea(10000, areaEntityId);
    WaitFor(chrArea || !AllPlayersInArea(areaEntityId));
    if (chrArea.Passed) {
        WaitFixedTimeSeconds(1);
    }
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    }
    RestartEvent();
});

// 【共通】英雄の墓_針ダメージ -- [Common] Hero's Tomb_Needle damage
$Event(90005671, Default, function(eventFlagId, eventFlagId2, eventFlagId3, dummypolyId, behaviorId) {
    DisableNetworkSync();
    WaitFor(
        EventFlag(eventFlagId) && InArea(10000, eventFlagId3) && CharacterHasSpEffect(10000, 4195));
    WarpAssetToCharacter(eventFlagId2, 10000, 93);
    WaitFixedTimeFrames(1);
    CreateDamagingAsset(eventFlagId3, eventFlagId2, dummypolyId, behaviorId, DamageTargetType.Character, 2, 0.1, 0);
    WaitFixedTimeFrames(1);
    DeleteAssetEvent(eventFlagId2);
    WaitFixedTimeSeconds(0.5);
    RestartEvent();
});

// 【共通】英雄の墓_針ダメージ_特殊効果付与 -- [Common] Hero's Tomb_Needle damage_Special effects added
$Event(90005672, Default, function(eventFlagId, areaEntityId) {
    WaitFor(EventFlag(eventFlagId) && InArea(10000, areaEntityId));
    SetSpEffect(10000, 4195);
    WaitFixedTimeSeconds(0.5);
    RestartEvent();
});

// 【共通】英雄の墓_ギロチン -- [Common] Tomb of the Hero_Guillotine
$Event(90005675, Default, function(eventFlagId, eventFlagId2, assetEntityId, areaEntityId, behaviorId, timeSeconds, value) {
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0) && EventFlag(eventFlagId)) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
        SetThisEventSlot(OFF);
    }
L10:
    WaitFor((InArea(10000, areaEntityId) || ThisEventSlot()) && !EventFlag(eventFlagId));
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
    if (!ThisEventSlot()) {
        WaitFixedTimeSeconds(timeSeconds);
    }
    if (Signed(1) != value) {
        ForceAnimationPlayback(assetEntityId, 1, false, false, false);
    } else {
        ForceAnimationPlayback(assetEntityId, 2, false, false, false);
    }
    if (Signed(behaviorId) != 0) {
        CreateBigDamagingAsset(eventFlagId2, assetEntityId, 30, 31, behaviorId, DamageTargetType.Character, 0.1, 1, 0);
    } else {
        CreateBigDamagingAsset(eventFlagId2, assetEntityId, 30, 31, 103000, DamageTargetType.Character, 0.1, 1, 0);
    }
    WaitFixedTimeSeconds(1);
    DeleteAssetEvent(eventFlagId2);
    WaitFixedTimeSeconds(4.1);
    WaitFixedTimeSeconds(0.1);
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    }
    RestartEvent();
});

// 【共通】英雄の墓_火吹き像_初期設定 -- [Common] Tomb of the Hero_Fire-breathing statue_Initial settings
$Event(90005680, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, assetEntityId) {
    if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
        SetEventFlagID(eventFlagId4, OFF);
    }
    WaitFor(AssetBackread(assetEntityId));
    if (EventFlag(eventFlagId)) {
        ForceAnimationPlayback(assetEntityId, 20, false, false, false);
        SetEventFlagID(eventFlagId2, ON);
        SetEventFlagID(eventFlagId3, ON);
        EndEvent();
    }
L0:
    ForceAnimationPlayback(assetEntityId, 10, false, false, false);
    SetEventFlagID(eventFlagId2, OFF);
    SetEventFlagID(eventFlagId3, OFF);
    EndEvent();
});

// 【共通】英雄の墓_火吹き像_移動処理 -- [Common] Hero's Tomb_Fire-breathing statue_Movement process
$Event(90005681, Default, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, entityId) {
    if (!(((EventFlag(eventFlagId) && EventFlag(eventFlagId2))
        || (!EventFlag(eventFlagId) && !EventFlag(eventFlagId2)))
        && EventFlag(eventFlagId4))) {
        if (EventFlag(eventFlagId)) {
            WaitFor(
                !EventFlag(eventFlagId)
                    || (EventFlag(eventFlagId2)
                        && HasDamageType(entityId, 20000, DamageType.Unspecified)));
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId, OFF);
                SetNetworkconnectedEventFlagID(eventFlagId4, ON);
            }
            SetEventFlagID(eventFlagId2, OFF);
            SetEventFlagID(eventFlagId3, OFF);
            ForceAnimationPlayback(entityId, 21, false, true, false);
            if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
                SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
            }
            RestartEvent();
        }
L0:
        WaitFor(
            EventFlag(eventFlagId)
                || (!EventFlag(eventFlagId2) && HasDamageType(entityId, 20000, DamageType.Unspecified)));
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
            SetNetworkconnectedEventFlagID(eventFlagId4, ON);
        }
        SetEventFlagID(eventFlagId2, ON);
        ForceAnimationPlayback(entityId, 12, false, true, false);
        if (MapHasPermissionToUpdate(false, 0, 0, 0, 0)) {
            SetNetworkconnectedEventFlagID(eventFlagId4, OFF);
        }
        SetEventFlagID(eventFlagId3, ON);
        RestartEvent();
    }
L9:
    WaitFor(!EventFlag(eventFlagId4));
    RestartEvent();
});

// 【共通】英雄の墓_火吹き像_火炎処理 -- [Common] Hero's Tomb_Fire-breathing statue_Flame processing
$Event(90005682, Default, function(eventFlagId, entityId, areaEntityId, chrEntityId, behaviorId, behaviorId2, dummypolyId, dummypolyId2, dummypolyId3, dummypolyId4) {
    flagArea &= EventFlag(eventFlagId);
    if (areaEntityId != 0) {
        flagArea &= InArea(10000, areaEntityId);
    }
    WaitFor(flagArea);
    CreateBulletOwner(chrEntityId);
    if (Signed(dummypolyId) != 0) {
        if (Signed(behaviorId) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId, behaviorId, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId, 101100, 0, 0, 0);
        }
        if (Signed(behaviorId2) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId, behaviorId2, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId, 101102, 0, 0, 0);
        }
    }
L1:
    if (Signed(dummypolyId2) != 0) {
        if (Signed(behaviorId) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId2, behaviorId, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId2, 101100, 0, 0, 0);
        }
        if (Signed(behaviorId2) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId2, behaviorId2, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId2, 101102, 0, 0, 0);
        }
    }
L2:
    if (Signed(dummypolyId3) != 0) {
        if (Signed(behaviorId) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId3, behaviorId, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId3, 101100, 0, 0, 0);
        }
        if (Signed(behaviorId2) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId3, behaviorId2, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId3, 101102, 0, 0, 0);
        }
    }
L3:
    if (Signed(dummypolyId4) != 0) {
        if (Signed(behaviorId) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId4, behaviorId, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId4, 101100, 0, 0, 0);
        }
        if (Signed(behaviorId2) != 0) {
            ShootBullet(chrEntityId, entityId, dummypolyId4, behaviorId2, 0, 0, 0);
        } else {
            ShootBullet(chrEntityId, entityId, dummypolyId4, 101102, 0, 0, 0);
        }
    }
L4:
    WaitFixedTimeSeconds(7.2);
    RestartEvent();
});

// 【共通】英雄の墓_指示像 -- [Common] Hero's Tomb_Instruction Statue
$Event(90005683, Default, function(eventFlagId, assetEntityId, dummypolyId, eventFlagId2, eventFlagId3) {
    DisableNetworkSync();
    if (EventFlag(eventFlagId)) {
        DeleteAssetfollowingSFX(assetEntityId, true);
        SetEventFlagID(eventFlagId2, OFF);
        SetEventFlagID(eventFlagId3, OFF);
        EndEvent();
    }
L0:
    if (!EventFlag(eventFlagId2)) {
        WaitFor(ActionButtonInArea(9260, assetEntityId));
        DisplayGenericDialog(4210, PromptType.OKCANCEL, NumberofOptions.NoButtons, assetEntityId, 3);
        SetEventFlagID(eventFlagId2, ON);
        SetEventFlagID(eventFlagId3, ON);
    }
L1:
    if (1049551600 != assetEntityId) {
        CreateAssetfollowingSFX(assetEntityId, dummypolyId, 800530);
    } else {
L10:
        CreateAssetfollowingSFX(assetEntityId, dummypolyId, 800531);
    }
L1:
    WaitFor(EventFlag(eventFlagId));
    RestartEvent();
    CreateAssetfollowingSFX(assetEntityId, dummypolyId, 800530);
});

// 【共通】英雄の墓_メッセージ表示 -- [Common] Hero's Tomb_Message display
$Event(90005684, Default, function(entityId) {
    DisableNetworkSync();
    WaitFor(ActionButtonInArea(9260, entityId));
    DisplayGenericDialog(4210, PromptType.OKCANCEL, NumberofOptions.NoButtons, entityId, 3);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 【共通】英雄の墓_チャリオット初期設定 -- [Common] Hero's Tomb_Chariot initial settings
$Event(90005685, Default, function(chrEntityId) {
    EnableCharacterImmortality(chrEntityId);
    DisableCharacterInvincibility(chrEntityId);
    DisableLockOnPoint(chrEntityId, 220);
    DisableCharacterHPBarDisplay(chrEntityId);
    SetSpEffect(chrEntityId, 5000);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AlwaysUpdate);
});

// 【共通】英雄の墓_チャリオット弾丸作成 -- [Common] Hero's Tomb_Chariot bullet creation
$Event(90005686, Default, function(chrEntityId, eventFlagId) {
    WaitFor(EventFlag(eventFlagId));
    ShootBullet(chrEntityId, chrEntityId, 10, 244600980, 0, 0, 0);
    ShootBullet(chrEntityId, chrEntityId, 15, 244600980, 0, 0, 0);
    ShootBullet(chrEntityId, chrEntityId, 20, 244600981, 0, 0, 0);
    ShootBullet(chrEntityId, chrEntityId, 25, 244600981, 0, 0, 0);
    ShootBullet(chrEntityId, chrEntityId, 30, 244600981, 0, 0, 0);
    WaitFixedTimeFrames(1);
    RestartEvent();
});

// 【共通】英雄の墓_チャリオット巡回ルート指定_初回起動 -- [Common] Tomb of the Hero_Chariot patrol route specification_First launch
$Event(90005687, Default, function(chrEntityId, patrolInformationEntityId, areaEntityId) {
    EndIf(ThisEventSlot());
    WaitFor(InArea(10000, areaEntityId));
    ChangeCharacterPatrolBehavior(chrEntityId, patrolInformationEntityId);
    WaitFixedTimeFrames(1);
});

// 【共通】英雄の墓_チャリオット巡回ルート指定_XX -- [Common] Tomb of the Hero_Chariot patrol route specification_XX
$Event(90005688, Default, function(chrEntityId, areaEntityId, patrolInformationEntityId, areaEntityId2, patrolInformationEntityId2, areaEntityId3, patrolInformationEntityId3) {
    WaitFor(InArea(chrEntityId, areaEntityId));
    GotoIf(L1, InArea(10000, areaEntityId2));
    GotoIf(S0, 0 == areaEntityId3);
    GotoIf(L2, InArea(10000, areaEntityId3));
S0:
    ChangeCharacterPatrolBehavior(chrEntityId, patrolInformationEntityId);
    Goto(L20);
L1:
    ChangeCharacterPatrolBehavior(chrEntityId, patrolInformationEntityId2);
    Goto(L20);
L2:
    ChangeCharacterPatrolBehavior(30090400, patrolInformationEntityId3);
    Goto(L20);
L20:
    WaitFor(!InArea(chrEntityId, areaEntityId));
    RestartEvent();
});

// 【共通】落下死亡無効 -- [Common] Fall death invalidity
$Event(90005690, Restart, function(areaEntityId) {
    DisableNetworkSync();
    WaitFor(InArea(10000, areaEntityId));
    SetSpEffect(10000, 4080);
    WaitFor(!InArea(10000, areaEntityId));
    ClearSpEffect(10000, 4080);
    RestartEvent();
});

// 【共通】落下ダメージ無効 -- [Common] Falling damage disabled
$Event(90005691, Restart, function(areaEntityId) {
    DisableNetworkSync();
    WaitFor(InArea(10000, areaEntityId));
    SetSpEffect(10000, 4085);
    WaitFor(!InArea(10000, areaEntityId));
    ClearSpEffect(10000, 4085);
    RestartEvent();
});

// 【共通】常駐ダメージアセット -- [Common] Resident damage asset
$Event(90005694, Restart, function(eventFlagId, assetEntityId, dummypolyId, endingDummypolyId, behaviorId, radius, lifespan, repetitionTimeS) {
    DeleteAssetEvent(eventFlagId);
    if (Signed(0) == endingDummypolyId) {
        CreateDamagingAsset(eventFlagId, assetEntityId, dummypolyId, behaviorId, DamageTargetType.Character, radius, lifespan, repetitionTimeS);
    } else {
        CreateBigDamagingAsset(eventFlagId, assetEntityId, dummypolyId, endingDummypolyId, behaviorId, DamageTargetType.Character, radius, lifespan, repetitionTimeS);
    }
});

// 【共通】常駐ダメージアセット_破壊有り -- [Common] Permanent damage asset_destructed
$Event(90005695, Restart, function(eventFlagId, assetEntityId, dummypolyId, endingDummypolyId, behaviorId, radius, lifespan, repetitionTimeS) {
    DeleteAssetEvent(eventFlagId);
    EndIf(AssetDestroyed(assetEntityId));
    if (Signed(0) == endingDummypolyId) {
        CreateDamagingAsset(eventFlagId, assetEntityId, dummypolyId, behaviorId, DamageTargetType.Character, radius, lifespan, repetitionTimeS);
    } else {
        CreateBigDamagingAsset(eventFlagId, assetEntityId, dummypolyId, endingDummypolyId, behaviorId, DamageTargetType.Character, radius, lifespan, repetitionTimeS);
    }
    WaitFor(AssetDestroyed(eventFlagId));
    DeleteAssetEvent(eventFlagId);
});

// 【共通】NPC敵対化処理 -- [Common] NPC hostile processing
$Event(90005700, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, targetHPRatio, eventFlagId4, eventFlagId5, value) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!EventFlag(3000));
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
    SetEventFlagID(eventFlagId3, OFF);
    WaitFor(
        !EventFlag(eventFlagId)
            && !EventFlag(eventFlagId2)
            && HPRatio(chrEntityId) > 0
            && (((HasDamageType(chrEntityId, 10000, DamageType.Unspecified)
                || HasDamageType(chrEntityId, 40000, DamageType.Unspecified)
                || CharacterHasSpEffect(chrEntityId, 1650000))
                && HPRatio(chrEntityId) < targetHPRatio)
                || CharacterHasSpEffect(chrEntityId, 9641)
                || EventFlag(eventFlagId3)));
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    SetSpEffect(chrEntityId, 9628);
    SetSpEffect(chrEntityId, 9635);
    if (Signed(1) != value) {
        BatchSetNetworkconnectedEventFlags(eventFlagId4, eventFlagId5, OFF);
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    } else {
L0:
        BatchSetNetworkconnectedEventFlags(eventFlagId4, eventFlagId5, OFF);
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    }
L9:
    SaveRequest();
});

// 【共通】NPCがX回攻撃されたらフラグを立てる処理 -- [Common] Processing to set a flag when an NPC is attacked X times
$Event(90005701, Restart, function(entityId, eventFlagId, eventFlagId2, eventFlagId3, value) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!EventFlag(3000));
    WaitFixedTimeFrames(1);
    WaitFor(!EventFlag(eventFlagId) && !EventFlag(eventFlagId2));
    GotoIf(L0, Signed(9) == value);
    GotoIf(L1, Signed(8) == value);
    GotoIf(L2, Signed(7) == value);
    GotoIf(L3, Signed(6) == value);
    GotoIf(L4, Signed(5) == value);
    GotoIf(L5, Signed(4) == value);
    GotoIf(L6, Signed(3) == value);
    GotoIf(L7, Signed(2) == value);
    GotoIf(L8, Signed(1) == value);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L0:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L1:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L2:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L3:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L4:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L5:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L6:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L7:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    WaitFixedTimeFrames(1);
L8:
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified));
    SetEventFlagID(eventFlagId3, ON);
    RestartEvent();
});

// 【共通】NPC死亡処理 -- [Common] NPC death processing
$Event(90005702, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!EventFlag(eventFlagId) && CharacterDead(chrEntityId));
    BatchSetNetworkconnectedEventFlags(eventFlagId2, eventFlagId3, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    SaveRequest();
});

// 【共通】新_NPC敵対化処理 -- [Common] New_NPC hostile processing
$Event(90005703, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, value) {
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId3, OFF);
    if (!EventFlag(eventFlagId5)) {
        SetSpEffect(chrEntityId, 9628);
        SetSpEffect(chrEntityId, 9635);
        SetSpEffect(chrEntityId, 9643);
        if (!CharacterHasSpEffect(chrEntityId, 445)) {
            SetSpEffect(chrEntityId, 442);
        }
        SetSpEffect(chrEntityId, 9644);
    }
L0:
    WaitFor(!EventFlag(eventFlagId4) && EventFlag(eventFlagId5));
    SetSpEffect(chrEntityId, 9629);
    SetSpEffect(chrEntityId, 9634);
    SetSpEffect(chrEntityId, 9642);
    SetSpEffect(chrEntityId, 9647);
    if (!CharacterHasSpEffect(chrEntityId, 445)) {
        SetSpEffect(chrEntityId, 440);
    }
    SetSpEffect(chrEntityId, 9645);
    dmgSp = HasDamageType(chrEntityId, 10000, DamageType.Unspecified)
        || HasDamageType(chrEntityId, 40000, DamageType.Unspecified)
        || CharacterHasSpEffect(chrEntityId, 1650000);
    if (HPRatio(chrEntityId) >= 1) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.65;
    } else if (HPRatio(chrEntityId) >= 0.9) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.55;
    } else if (HPRatio(chrEntityId) >= 0.8) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.45;
    } else if (HPRatio(chrEntityId) >= 0.7) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.35;
    } else if (HPRatio(chrEntityId) >= 0.7) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.25;
    } else {
        hpDmgSp &= HPRatio(chrEntityId) < 0.15;
        Goto(L10);
    }
L10:
    hpDmgSp &= dmgSp;
    flag = EventFlag(eventFlagId) || EventFlag(eventFlagId2);
    hpFlagSpDmg = HPRatio(chrEntityId) > 0
        && (EventFlag(eventFlagId3) || CharacterHasSpEffect(chrEntityId, 9641) || flag || hpDmgSp);
    flag2 = EventFlag(eventFlagId4);
    WaitFor(flag2 || hpFlagSpDmg);
    RestartIf(flag2.Passed);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    SetSpEffect(chrEntityId, 9628);
    SetSpEffect(chrEntityId, 9635);
    SetSpEffect(chrEntityId, 9643);
    if (!CharacterHasSpEffect(chrEntityId, 445)) {
        SetSpEffect(chrEntityId, 442);
    }
    SetSpEffect(chrEntityId, 9644);
    if (!flag.Passed) {
        if (Signed(1) != value) {
            BatchSetNetworkconnectedEventFlags(eventFlagId5, eventFlagId6, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        } else {
L1:
            BatchSetNetworkconnectedEventFlags(eventFlagId5, eventFlagId6, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId2, ON);
        }
    }
L9:
    SaveRequest();
    RestartEvent();
});

// 【共通】新_NPCがX回攻撃されたらフラグを立てる処理 -- [Common] New_Processing to set a flag when an NPC is attacked X times
$Event(90005704, Restart, function(entityId, eventFlagId, eventFlagId2, eventFlagId3, value) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    WaitFor(!EventFlag(eventFlagId) && EventFlag(eventFlagId2));
    GotoIf(L4, Signed(4) == value);
    GotoIf(L3, Signed(3) == value);
    GotoIf(L2, Signed(2) == value);
    GotoIf(L1, Signed(1) == value);
    flag = EventFlag(eventFlagId) || !EventFlag(eventFlagId2);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || flag);
    RestartIf(flag.Passed);
    WaitFixedTimeFrames(1);
L4:
    flag2 = EventFlag(eventFlagId) || !EventFlag(eventFlagId2);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || flag2);
    RestartIf(flag2.Passed);
    WaitFixedTimeFrames(1);
L3:
    flag3 = EventFlag(eventFlagId) || !EventFlag(eventFlagId2);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || flag3);
    RestartIf(flag3.Passed);
    WaitFixedTimeFrames(1);
L2:
    flag4 = EventFlag(eventFlagId) || !EventFlag(eventFlagId2);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || flag4);
    RestartIf(flag4.Passed);
    WaitFixedTimeFrames(1);
L1:
    flag5 = EventFlag(eventFlagId) || !EventFlag(eventFlagId2);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || flag5);
    RestartIf(flag5.Passed);
    SetEventFlagID(eventFlagId3, ON);
    RestartEvent();
});

// 【共通】NPC101道標老婆_死亡遷移イベント -- [Common] NPC101 Signpost Old Woman_Death Transition Event
$Event(90005705, Restart, function(chrEntityId) {
    WaitFixedTimeFrames(1);
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    EndIf(!PlayerIsInOwnWorld());
    EnableCharacterImmortality(chrEntityId);
    WaitFor(HasDamageType(chrEntityId, 10000, DamageType.Unspecified));
    ForceAnimationPlayback(chrEntityId, 20022, false, false, false);
    WaitFixedTimeSeconds(10);
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    EndEvent();
});

// 【共通】NPC700話す死体_初期化イベント -- [Common] NPC700 talking corpse_Initialization event
$Event(90005706, Restart, function(chrEntityId, animationId, chrEntityId2) {
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacter(chrEntityId);
    DisableCharacterGravity(chrEntityId);
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    EndIf(chrEntityId2 == 0);
    WaitFor(CharacterHasSpEffect(chrEntityId, 9624));
    IssueShortWarpRequest(chrEntityId, TargetEntityType.Area, chrEntityId2, -1);
    DisableCharacterGravity(chrEntityId);
    EndEvent();
});

// 【共通】幻影敵対化 -- [Common] Phantom hostility
$Event(90005707, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, value, animationId, eventFlagId7, eventFlagId8) {
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId3, OFF);
    WaitFor(!EventFlag(eventFlagId4) && EventFlag(eventFlagId5));
L0:
    SetSpEffect(chrEntityId, 9642);
    dmgSp = HasDamageType(chrEntityId, 10000, DamageType.Unspecified)
        || HasDamageType(chrEntityId, 40000, DamageType.Unspecified)
        || CharacterHasSpEffect(chrEntityId, 1650000);
    if (HPRatio(chrEntityId) >= 1) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.65;
    } else if (HPRatio(chrEntityId) >= 0.9) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.55;
    } else if (HPRatio(chrEntityId) >= 0.8) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.45;
    } else if (HPRatio(chrEntityId) >= 0.7) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.35;
    } else if (HPRatio(chrEntityId) >= 0.7) {
        hpDmgSp &= HPRatio(chrEntityId) < 0.25;
    } else {
        hpDmgSp &= HPRatio(chrEntityId) < 0.15;
        Goto(L10);
    }
L10:
    hpDmgSp &= dmgSp;
    hpFlagSpDmg = HPRatio(chrEntityId) > 0
        && (EventFlag(eventFlagId3)
            || CharacterHasSpEffect(chrEntityId, 9641)
            || EventFlag(eventFlagId)
            || EventFlag(eventFlagId2)
            || hpDmgSp);
    flag = EventFlag(eventFlagId4);
    WaitFor(flag || hpFlagSpDmg);
    RestartIf(flag.Passed);
    if (!or5.Passed) {
        if (Signed(1) != value) {
            BatchSetNetworkconnectedEventFlags(eventFlagId5, eventFlagId6, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        } else {
L0:
            BatchSetNetworkconnectedEventFlags(eventFlagId5, eventFlagId6, OFF);
            SetNetworkconnectedEventFlagID(eventFlagId2, ON);
        }
    }
L9:
    SaveRequest();
    if (eventFlagId7 != 0) {
        WaitFixedTimeRealFrames(2);
        WaitFor(!EventFlag(eventFlagId7));
    }
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    SetEventFlagID(eventFlagId8, ON);
    RestartEvent();
});

// 【共通】椅子キャラ位置合わせワープ -- [Common] Chair character positioning warp
$Event(90005708, Restart, function(chrEntityId, eventFlagId, chrEntityId2) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(CharacterBackreadStatus(chrEntityId) && EventFlag(eventFlagId));
    WaitFixedTimeRealFrames(1);
    RestartIf(!EventFlag(eventFlagId));
    if (chrEntityId2 == 0) {
        ResetCharacterPosition(chrEntityId);
    } else {
        IssueShortWarpRequest(chrEntityId, TargetEntityType.Area, chrEntityId2, -1);
    }
});

// 【共通】幻影被ダメSFX -- [Common] Illusion damage SFX
$Event(90005709, Restart, function(entityId, dummypolyId, sfxId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(HasDamageType(entityId, 0, DamageType.Unspecified));
    SpawnOneshotSFX(TargetEntityType.Character, entityId, dummypolyId, sfxId);
    RestartEvent();
});

// 【共通】バディ召喚石碑_SFX再生 -- [Common] Buddy summoning stone monument_SFX playback
$Event(90005710, Restart, function(eventFlagId, assetEntityId, dummypolyId, sfxId) {
    WaitFor(!EventFlag(eventFlagId));
    CreateAssetfollowingSFX(assetEntityId, dummypolyId, sfxId);
    WaitFor(EventFlag(eventFlagId));
    WaitFixedTimeSeconds(2);
    DeleteAssetfollowingSFX(assetEntityId, true);
    RestartEvent();
});

// 【共通】バディ召喚石碑_バディ巡回ルート設定 -- [Common] Buddy summoning stone monument_Buddy patrol route setting
$Event(90005711, Restart, function(eventFlagId, patrolInformationEntityId) {
    if (!PlayerIsInOwnWorld()) {
        EndEvent();
    }
L0:
    SetNetworkUpdateAuthority(20000, AuthorityLevel.Forced);
    WaitFor(EventFlag(eventFlagId));
    ChangeCharacterPatrolBehavior(35000, patrolInformationEntityId);
    RestartEvent();
});

// 【共通】バディ召喚石碑_アクセス可SFX設定 -- [Common] Buddy Summon Stone Monument_Accessible SFX Settings
$Event(90005712, Restart, function(chrEntityId, assetEntityId, dummypolyId, sfxId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    CreateAssetfollowingSFX(assetEntityId, dummypolyId, sfxId);
    WaitFor(CharacterHasSpEffect(chrEntityId, 9502));
    DeleteAssetfollowingSFX(assetEntityId, true);
    WaitFor(CharacterHasSpEffect(chrEntityId, 9503));
    RestartEvent();
});

// 【共通】バディ召喚石碑_撃破対象リスト設定 -- [Common] Buddy summon stone monument_defeat target list setting
$Event(90005713, Restart, function(eventFlagId, chrEntityId, chrEntityId2) {
    if (!EventFlag(eventFlagId)) {
        WaitFor(
            (PlayerIsInOwnWorld() && CharacterHasSpEffect(chrEntityId, 9500))
                || (!PlayerIsInOwnWorld() && EventFlag(eventFlagId)));
        if (PlayerIsInOwnWorld()) {
            SetNetworkconnectedEventFlagID(eventFlagId, ON);
        }
    }
L0:
    EnableCharacterAI(chrEntityId2);
    WaitFor(
        (PlayerIsInOwnWorld() && CharacterHasSpEffect(20000, 202))
            || (!PlayerIsInOwnWorld() && !EventFlag(eventFlagId)));
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, OFF);
    }
    RestartEvent();
});

$Event(90005715, Restart, function(chrEntityId, chrEntityId2, eventFlagId, eventFlagId2, range) {
    EndIf(!PlayerIsInOwnWorld());
    SetCharacterTalkRange(chrEntityId, 17);
    if (0 != chrEntityId2) {
        SetCharacterTalkRange(chrEntityId2, 17);
    }
    EndIf(EventFlag(eventFlagId));
    GotoIf(L1, !EventFlag(eventFlagId2));
    Goto(L2);
L1:
    WaitFor(EventFlag(eventFlagId2));
    Goto(L2);
L2:
    SetCharacterTalkRange(chrEntityId, range);
    if (0 != chrEntityId2) {
        SetCharacterTalkRange(chrEntityId2, range);
    }
    EndEvent();
});

$Event(90005716, Restart, function(chrEntityId, eventFlagId, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterDead(chrEntityId));
    EnableCharacterDefaultBackread(chrEntityId);
    WaitFor(EventFlag(eventFlagId2) || ElapsedSeconds(30));
    DisableCharacterDefaultBackread(chrEntityId);
    EndEvent();
});

// 【共通】ジプシーバディ召喚 -- [Common] Gypsy Buddy Summon
$Event(90005720, Restart, function(chrEntityId, chrEntityId2, spEffectId, dummypolyId) {
    EndIf(CharacterHasSpEffect(chrEntityId, 11020));
    DisableCharacter(chrEntityId2);
    DisableCharacterCollision(chrEntityId2);
    WaitFor(
        CharacterHasSpEffect(chrEntityId, 10960) && CharacterHasSpEffect(chrEntityId, spEffectId));
    EnableCharacter(chrEntityId2);
    EnableCharacterCollision(chrEntityId2);
    SetSpEffect(chrEntityId2, 8551);
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, dummypolyId, chrEntityId);
    ForceAnimationPlayback(chrEntityId2, 20000, false, false, false);
    EndEvent();
});

// 【共通】ジプシーバディ死亡演出 -- [Common] Gypsy Buddy death performance
$Event(90005721, Restart, function(chrEntityId, chrEntityId2) {
    WaitFor(CharacterDead(chrEntityId));
    WaitRandomTimeSeconds(0.5, 1.5);
    ForceCharacterDeath(chrEntityId2, true);
    EndEvent();
});

// 【共通】ジプシー_敵対判定 -- [Common] Gypsy_hostile judgment
$Event(90005722, Restart, function(chrEntityId, chrEntityId2) {
    if (CharacterHasSpEffect(chrEntityId, 11020)) {
        SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
        SetCharacterTeamType(chrEntityId2, TeamType.HostileNPC);
    }
L0:
    WaitFor(HPRatio(chrEntityId) < 0.65 || HPRatio(chrEntityId2, GreaterOrEqual, 1) < 0.65);
    SetSpEffect(chrEntityId, 11012);
    SetSpEffect(chrEntityId, 11020);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    SetCharacterTeamType(chrEntityId2, TeamType.HostileNPC);
    EndEvent();
});

// 【共通】ジプシー_会話判定 -- [Common] Gypsy_Conversation judgment
$Event(90005723, Restart, function(chrEntityId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!CharacterHasSpEffect(chrEntityId, 11001) && !CharacterHasSpEffect(chrEntityId, 11020));
    SetSpEffect(chrEntityId, 11000);
    WaitFor(CharacterHasSpEffect(chrEntityId, 11001) || CharacterHasSpEffect(chrEntityId, 11020));
    ClearSpEffect(chrEntityId, 11000);
    RestartEvent();
});

// 【共通】ジプシー_リスポン処理 -- [Common] Gypsy_Respon processing
$Event(90005724, Restart, function(eventFlagId, chrEntityId, itemLotId, timeSeconds, value, chrEntityId2) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId2);
        DisableCharacterCollision(chrEntityId2);
        if (Signed(value) != 0) {
            DisableCharacter(chrEntityId);
            DisableCharacterCollision(chrEntityId);
            ForceCharacterTreasure(chrEntityId);
            EndEvent();
        }
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndEvent();
    }
L0:
    WaitFor(CharacterDead(chrEntityId));
    WaitFixedTimeSeconds(timeSeconds);
    SetEventFlagID(eventFlagId, ON);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(Signed(value) == 1);
    AwardItemsIncludingClients(itemLotId);
    EndEvent();
});

// 【共通】NPC801モブ赤目_初期化イベント -- [Common] NPC801 Mob Red Eye_Initialization event
$Event(90005725, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, chrEntityId, chrEntityId2, assetEntityId) {
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId) && EventFlag(eventFlagId4)) {
            SetEventFlagID(eventFlagId4, OFF);
        }
    }
L0:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableCharacter(chrEntityId2);
    SetCharacterBackreadState(chrEntityId2, true);
    DisableAsset(assetEntityId);
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L4, EventFlag(eventFlagId3));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    if (!CharacterHasSpEffect(chrEntityId, 11035)) {
        ForceAnimationPlayback(chrEntityId, 930003, false, false, false);
    }
    if (CharacterHasSpEffect(chrEntityId, 11035)) {
        ForceAnimationPlayback(chrEntityId, 930002, false, false, false);
    }
    EnableCharacter(chrEntityId2);
    SetCharacterBackreadState(chrEntityId2, false);
    EnableAsset(assetEntityId);
    Goto(L20);
L2:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    EnableCharacter(chrEntityId2);
    SetCharacterBackreadState(chrEntityId2, false);
    SetCharacterTeamType(chrEntityId2, TeamType.HostileNPC);
    EnableAsset(assetEntityId);
    Goto(L20);
L4:
    ForceCharacterTreasure(chrEntityId);
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableCharacter(chrEntityId2);
    SetCharacterBackreadState(chrEntityId2, true);
    DisableAsset(assetEntityId);
    Goto(L20);
L20:
    EndEvent();
});

// 【共通】NPC801モブ赤目_ロバ無し_初期化イベント -- [Common] NPC801 Mob Red Eye_No Donkey_Initialization Event
$Event(90005726, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, chrEntityId, assetEntityId) {
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId) && EventFlag(eventFlagId4)) {
            SetEventFlagID(eventFlagId4, OFF);
        }
    }
L0:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableAsset(assetEntityId);
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L4, EventFlag(eventFlagId3));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    ForceAnimationPlayback(chrEntityId, 930003, false, false, false);
    EnableAsset(assetEntityId);
    Goto(L20);
L2:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    EnableAsset(assetEntityId);
    Goto(L20);
L4:
    ForceCharacterTreasure(chrEntityId);
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableAsset(assetEntityId);
    Goto(L20);
L20:
    EndEvent();
});

// 【共通】NPC801モブ赤目_赤目ロバ相互敵対処理 -- [Common] NPC801 Mob Red Eye_Red Eye Donkey Mutual Hostility Processing
$Event(90005727, Restart, function(eventFlagId, chrEntityId, chrEntityId2, eventFlagId2, eventFlagId3) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId3));
    SetSpEffect(chrEntityId, 9629);
    SetSpEffect(chrEntityId, 9634);
    SetSpEffect(chrEntityId, 9642);
    SetSpEffect(chrEntityId, 440);
    SetSpEffect(chrEntityId, 9645);
    SetSpEffect(chrEntityId2, 9629);
    SetSpEffect(chrEntityId2, 9634);
    SetSpEffect(chrEntityId2, 9642);
    SetSpEffect(chrEntityId2, 440);
    SetSpEffect(chrEntityId2, 9645);
    WaitFor(
        EventFlag(eventFlagId)
            || (HasDamageType(chrEntityId, 20000, DamageType.Unspecified)
                && CharacterHPValue(chrEntityId) < 1)
            || (HasDamageType(chrEntityId2, 20000, DamageType.Unspecified)
                && CharacterHPValue(chrEntityId2) < 1));
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    EnableCharacterAI(chrEntityId);
    SetSpEffect(chrEntityId, 9628);
    SetSpEffect(chrEntityId, 9635);
    SetSpEffect(chrEntityId, 9643);
    SetSpEffect(chrEntityId, 442);
    SetSpEffect(chrEntityId, 9644);
    SetCharacterTeamType(chrEntityId2, TeamType.HostileNPC);
    EnableCharacterAI(chrEntityId2);
    SetSpEffect(chrEntityId2, 9628);
    SetSpEffect(chrEntityId2, 9635);
    SetSpEffect(chrEntityId2, 9643);
    SetSpEffect(chrEntityId2, 442);
    SetSpEffect(chrEntityId2, 9644);
    if (!EventFlag(eventFlagId3)) {
        BatchSetNetworkconnectedEventFlags(eventFlagId2, eventFlagId3, OFF);
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
    EndEvent();
});

// 【共通】NPC801モブ赤目_ロバ被ダメ台詞再生 -- [Common] NPC801 Mob Red Eye_Donkey damaged lines playback
$Event(90005728, Restart, function(entityId, eventFlagId, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        (HasDamageType(entityId, 20000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified))
            && !EventFlag(eventFlagId2));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    EndEvent();
});

// 【共通】NPC801モブ赤目_タイプA呼び掛け会話イベント -- [Common] NPC801 Mob Red Eye_Type A calling conversation event
$Event(90005729, Restart, function(eventFlagId, chrEntityId, range, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    SetCharacterTalkRange(chrEntityId, range);
    WaitForEventFlag(ON, TargetEventFlagType.EventFlag, eventFlagId2);
    WaitFixedTimeSeconds(30);
    SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

// 【共通】リマインド自動会話 -- [Common] Reminder automatic conversation
$Event(90005730, Restart, function(eventFlagId, targetTimeSeconds, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && EventFlag(eventFlagId3)
            && !EventFlag(eventFlagId4)
            && !EventFlag(eventFlagId5));
    if (!EventFlag(eventFlagId2)) {
        flag = EventFlag(eventFlagId)
            || !EventFlag(eventFlagId3)
            || EventFlag(eventFlagId4)
            || EventFlag(eventFlagId5);
        WaitFor(EventFlag(eventFlagId2) || flag);
        RestartIf(flag.Passed);
        SetEventFlagID(eventFlagId, ON);
        RestartEvent();
    }
L0:
    flag2 = EventFlag(eventFlagId)
        || !EventFlag(eventFlagId3)
        || EventFlag(eventFlagId4)
        || EventFlag(eventFlagId5)
        || !EventFlag(eventFlagId2);
    WaitFor(ElapsedSeconds(targetTimeSeconds) || flag2);
    RestartIf(flag2.Passed);
    SetEventFlagID(eventFlagId, ON);
    RestartEvent();
});

// 【共通】一定距離に入ったらフラグを立てる_チャタリング防止 -- [Common] Set a flag when you enter a certain distance_Chattering prevention
$Event(90005731, Restart, function(eventFlagId, entityId, targetDistance, targetDistance2) {
    EndIf(!PlayerIsInOwnWorld());
    if (!EventFlag(eventFlagId)) {
        WaitFor(EntityInRadiusOfEntity(10000, entityId, targetDistance, 1));
        SetEventFlagID(eventFlagId, ON);
    }
L0:
    WaitFor(
        !EntityInRadiusOfEntity(10000, entityId, targetDistance, 1)
            && !EntityInRadiusOfEntity(10000, entityId, targetDistance2, 1));
    SetEventFlagID(eventFlagId, OFF);
    RestartEvent();
});

// 【共通】領域に入ったらフラグを立てる_チャタリング防止 -- [Common] Set a flag when entering the area_Chattering prevention
$Event(90005732, Restart, function(eventFlagId, areaEntityId, areaEntityId2) {
    EndIf(!PlayerIsInOwnWorld());
    if (!EventFlag(eventFlagId)) {
        WaitFor(InArea(10000, areaEntityId));
        SetEventFlagID(eventFlagId, ON);
    }
L0:
    WaitFor(!InArea(10000, areaEntityId) && !InArea(10000, areaEntityId2));
    SetEventFlagID(eventFlagId, OFF);
    RestartEvent();
});

// 【共通】NPC322ユリア_同衾データサーバー打ち上げ -- [Common] NPC322 Yulia_Dojuku data server launch
$Event(90005733, Restart, function(eventFlagId) {
    EndIf(!PlayerIsInOwnWorld());
    DisableNetworkSync();
    SetEventFlagID(eventFlagId, OFF);
    WaitFor(EventFlag(eventFlagId) && PlayerIsInOwnWorld());
    SendCharacterDataToOnlinePlayers(0);
    RestartEvent();
});

$Event(90005734, Restart, function(eventFlagId, eventFlagId2, areaEntityId, areaEntityId2, eventFlagId3, value) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(!EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
    WaitFor(InArea(10000, areaEntityId));
    SetEventFlagID(eventFlagId3, ON);
    WaitFixedTimeFrames(1);
    WaitFor(!InArea(10000, areaEntityId) && !InArea(10000, areaEntityId2));
    if (Signed(-1) != value) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    RestartEvent();
});

$Event(90005735, Restart, function(chrEntityId, eventFlagId, eventFlagId2, entityId, targetDistance) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    DisableCharacterDefaultBackread(chrEntityId);
    EndIf(!EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
    WaitFor(
        !EventFlag(eventFlagId2) && EntityInRadiusOfEntity(entityId, chrEntityId, targetDistance, 1));
    EnableCharacterDefaultBackread(chrEntityId);
    WaitFor(
        !(!EventFlag(eventFlagId2)
            && EntityInRadiusOfEntity(entityId, chrEntityId, targetDistance, 1)));
    DisableCharacterDefaultBackread(chrEntityId);
    RestartEvent();
});

$Event(90005736, Restart, function(chrEntityId, assetEntityId, eventFlagId, eventFlagId2, targetDistance, range, eventFlagId3, eventFlagId4, value, animationId, value2, assetEntityId2) {
    if (Signed(1) != value) {
        if (Signed(0) != value2) {
            DisableAsset(assetEntityId2);
        }
    }
    if (PlayerIsInOwnWorld()) {
        EndIf(EventFlag(eventFlagId));
        if (Signed(1) != value) {
            if (Signed(0) != value2) {
                EnableAsset(assetEntityId2);
                CreateAssetfollowingSFX(assetEntityId2, 100, 600904);
            }
        }
        WaitFor(
            HasDamageType(assetEntityId, 20000, DamageType.Unspecified) && PlayerIsInOwnWorld());
        SetEventFlagID(eventFlagId2, ON);
        if (!EntityInRadiusOfEntity(20000, assetEntityId, targetDistance, 1)) {
            SetEventFlagID(eventFlagId3, ON);
        }
        DisableCharacterGravity(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
L0:
    WaitForEventFlag(ON, TargetEventFlagType.EventFlag, eventFlagId2);
    GotoIf(L1, Signed(1) == value);
    GotoIf(L2, Signed(0) == value);
L1:
    SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 900, 641012);
    WaitFixedTimeSeconds(0.5);
    DisableAsset(assetEntityId);
    WaitFixedTimeSeconds(0.3);
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    EnableCharacter(chrEntityId);
    EnableCharacterGravity(chrEntityId);
    EnableCharacterCollision(chrEntityId);
    SetCharacterMaphit(chrEntityId, true);
    Goto(L10);
L2:
    ForceAnimationPlayback(assetEntityId, 1, false, false, false);
    WaitFixedTimeSeconds(1);
    if (Signed(0) != value2) {
        DeleteAssetfollowingSFX(assetEntityId2, true);
    }
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    EnableCharacter(chrEntityId);
    SpawnOneshotSFX(TargetEntityType.Character, chrEntityId, 220, 302603);
    WaitFixedTimeSeconds(1);
    DisableAsset(assetEntityId);
    EnableCharacterGravity(chrEntityId);
    EnableCharacterCollision(chrEntityId);
    SetCharacterMaphit(chrEntityId, true);
    Goto(L10);
L10:
    WaitFor(EventFlag(eventFlagId4));
    SetCharacterTalkRange(chrEntityId, range);
    EndEvent();
});

$Event(90005737, Restart, function(eventFlagId, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    GotoIf(L0, !EventFlag(eventFlagId2));
    Goto(L1);
L0:
    WaitFor(
        HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending));
    SetEventFlagID(eventFlagId2, ON);
    RestartEvent();
L1:
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending)));
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

// 【共通】投げもどきアニメ再生_PC -- [Common] Throwback anime playback_PC
$Event(90005740, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, dummypolyId, assetEntityId, dummypolyId2, targetDistance, animationId, animationId2, spEffectId, targetDistance2) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId));
    if (Signed(dummypolyId) != 0) {
        GotoIf(L0, assetEntityId == 0);
        WarpAssetToCharacter(assetEntityId, chrEntityId, dummypolyId2);
        WaitFixedTimeRealFrames(1);
        area &= EntityInRadiusOfEntity(10000, assetEntityId, targetDistance, 1);
        GotoIf(L9, area);
        GotoIf(L9, 
            EntityInRadiusOfEntity(10000, assetEntityId, targetDistance2, 1)
                && EntityInRadiusOfEntity(10000, chrEntityId, targetDistance2, 1));
        RotateCharacter(10000, assetEntityId, -1, true);
        RotateCharacter(10000, assetEntityId, 90006, false);
        Goto(L8);
    }
L0:
    RotateCharacter(10000, chrEntityId, -1, true);
    area &= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    GotoIf(L9, area);
    RotateCharacter(10000, chrEntityId, 90006, false);
    Goto(L8);
L8:
    WaitFixedTimeRealFrames(1);
    sp = !CharacterHasSpEffect(10000, 9900);
    flagTime = !EventFlag(eventFlagId) || ElapsedSeconds(2);
    spFlagTimeArea |= sp || flagTime;
    if (Signed(dummypolyId) != 0) {
        GotoIf(S0, assetEntityId == 0);
        spFlagTimeArea |= EntityInRadiusOfEntity(10000, assetEntityId, targetDistance, 1);
    } else {
S0:
        spFlagTimeArea |= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    }
    WaitFor(spFlagTimeArea);
    if (!sp.Passed) {
        if (!flagTime.Passed) {
L9:
            SetEventFlagID(eventFlagId2, ON);
            if (eventFlagId3 != 0) {
                SetEventFlagID(eventFlagId3, ON);
            }
            if (Signed(dummypolyId) != 0) {
                IssueShortWarpRequest(10000, TargetEntityType.Character, chrEntityId, dummypolyId);
            }
            if (Signed(spEffectId) != -1) {
                RotateCharacter(10000, chrEntityId, animationId, false);
            } else {
                RotateCharacter(10000, chrEntityId, animationId, true);
            }
            Goto(L8);
L8:
            WaitFixedTimeRealFrames(1);
            sp2 = !CharacterHasSpEffect(10000, 9900);
            WaitFor(!EventFlag(eventFlagId) || sp2);
            if (!sp2.Passed) {
                if (Signed(animationId2) != -1) {
                    if (Signed(spEffectId) != -1) {
                        sp3 = !CharacterHasSpEffect(10000, 9900);
                        WaitFor(CharacterHasSpEffect(10000, spEffectId) || sp3);
                        GotoIf(L20, sp3.Passed);
                    }
L10:
                    SetEventFlagID(eventFlagId2, OFF);
                    ForceAnimationPlayback(10000, animationId2, false, true, false);
                    RestartEvent();
                }
L18:
                SetEventFlagID(eventFlagId2, OFF);
                RestartEvent();
            }
        }
L19:
        SetEventFlagID(eventFlagId, OFF);
        ForceAnimationPlayback(10000, 0, false, false, false);
        RestartEvent();
    }
L20:
    SetEventFlagID(eventFlagId, OFF);
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

// 【共通】投げもどきアニメ再生_話者 -- [Common] Throwback anime playback_Speaker
$Event(90005741, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, animationId, value, animationId2, spEffectId, timeSeconds) {
    EndIf(!PlayerIsInOwnWorld());
    if (eventFlagId3 != 0) {
        cond &= EventFlag(eventFlagId3);
    }
    cond &= EventFlag(eventFlagId);
    WaitFor(cond);
    SetEventFlagID(eventFlagId2, ON);
    if (eventFlagId3 != 0) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    if (value != 1) {
        if (Signed(spEffectId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
        } else {
            ForceAnimationPlayback(chrEntityId, animationId, false, true, false);
        }
    } else {
L0:
        if (Signed(spEffectId) != -1) {
            RotateCharacter(chrEntityId, 10000, animationId, false);
        } else {
            RotateCharacter(chrEntityId, 10000, animationId, true);
        }
        Goto(L10);
    }
L10:
    cond &= !EventFlag(eventFlagId);
    if (Signed(spEffectId) != -1) {
        cond &= CharacterHasSpEffect(chrEntityId, spEffectId);
    }
    WaitFor(cond);
    if (Signed(animationId2) != -1) {
        SetEventFlagID(eventFlagId2, OFF);
        ForceAnimationPlayback(chrEntityId, animationId2, false, true, false);
        WaitFixedTimeSeconds(timeSeconds);
        RestartEvent();
    }
L19:
    SetEventFlagID(eventFlagId2, OFF);
    WaitFixedTimeSeconds(timeSeconds);
    RestartEvent();
L20:
    SetEventFlagID(eventFlagId, OFF);
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

// 【共通】投げもどきアニメ再生_PC_ユリア用 -- [Common] Throwback anime playback_PC_for Yuria
$Event(90005742, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, dummypolyId, assetEntityId, dummypolyId2, targetDistance, animationId, animationId2, spEffectId, targetDistance2, eventFlagId4) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId));
    if (Signed(dummypolyId) != 0) {
        GotoIf(L0, assetEntityId == 0);
        WarpAssetToCharacter(assetEntityId, chrEntityId, dummypolyId2);
        WaitFixedTimeRealFrames(1);
        area &= EntityInRadiusOfEntity(10000, assetEntityId, targetDistance, 1);
        GotoIf(L9, area);
        areaFlag &= EntityInRadiusOfEntity(10000, assetEntityId, targetDistance2, 1)
            && EntityInRadiusOfEntity(10000, chrEntityId, targetDistance2, 1);
        GotoIf(L9, areaFlag);
        RotateCharacter(10000, assetEntityId, -1, true);
        RotateCharacter(10000, assetEntityId, 90006, false);
        Goto(L8);
    }
L0:
    RotateCharacter(10000, chrEntityId, -1, true);
    area &= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    GotoIf(L9, area);
    RotateCharacter(10000, chrEntityId, 90006, false);
    Goto(L8);
L8:
    WaitFixedTimeRealFrames(1);
    sp = !CharacterHasSpEffect(10000, 9900);
    flagTime = !EventFlag(eventFlagId) || ElapsedSeconds(2);
    spFlagTimeArea |= sp || flagTime;
    if (Signed(dummypolyId) != 0) {
        GotoIf(S0, assetEntityId == 0);
        spFlagTimeArea |= EntityInRadiusOfEntity(10000, assetEntityId, targetDistance, 1);
    } else {
S0:
        spFlagTimeArea |= EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1);
    }
    WaitFor(spFlagTimeArea);
    if (!sp.Passed) {
        if (!flagTime.Passed) {
L9:
            SetEventFlagID(eventFlagId2, ON);
            if (eventFlagId3 != 0) {
                SetEventFlagID(eventFlagId3, ON);
            }
            if (Signed(dummypolyId) != 0) {
                IssueShortWarpRequest(10000, TargetEntityType.Character, chrEntityId, dummypolyId);
            }
            if (Signed(spEffectId) != -1) {
                RotateCharacter(10000, chrEntityId, animationId, false);
            } else {
                RotateCharacter(10000, chrEntityId, animationId, true);
            }
            Goto(L8);
L8:
            WaitFixedTimeRealFrames(1);
            sp2 = !CharacterHasSpEffect(10000, 9900);
            areaFlag &= EventFlag(eventFlagId4);
            WaitFor(!EventFlag(eventFlagId) || sp2 || areaFlag);
            GotoIf(L20, sp2.Passed);
            GotoIf(L18, Signed(animationId2) == -1);
            GotoIf(L20, areaFlag.Passed);
            if (Signed(spEffectId) != -1) {
                sp3 = !CharacterHasSpEffect(10000, 9900);
                WaitFor(CharacterHasSpEffect(10000, spEffectId) || sp3);
                GotoIf(L20, sp3.Passed);
            }
L10:
            SetEventFlagID(eventFlagId2, OFF);
            ForceAnimationPlayback(10000, animationId2, false, true, false);
            RestartEvent();
L18:
            SetEventFlagID(eventFlagId2, OFF);
            RestartEvent();
        }
L19:
        SetEventFlagID(eventFlagId, OFF);
        ForceAnimationPlayback(10000, 0, false, false, false);
        RestartEvent();
    }
L20:
    SetEventFlagID(eventFlagId, OFF);
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

// 【共通】投げもどきアニメ再生_話者_ユリア用 -- [Common] Throwback anime playback_speaker_for Yuria
$Event(90005743, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, animationId, value, animationId2, spEffectId, timeSeconds, eventFlagId4) {
    EndIf(!PlayerIsInOwnWorld());
    if (eventFlagId3 != 0) {
        cond &= EventFlag(eventFlagId3);
    }
    cond &= EventFlag(eventFlagId);
    WaitFor(cond);
    SetEventFlagID(eventFlagId2, ON);
    if (eventFlagId3 != 0) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    if (value != 1) {
        if (Signed(spEffectId) != -1) {
            ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
        } else {
            ForceAnimationPlayback(chrEntityId, animationId, false, true, false);
        }
    } else {
L0:
        if (Signed(spEffectId) != -1) {
            RotateCharacter(chrEntityId, 10000, animationId, false);
        } else {
            RotateCharacter(chrEntityId, 10000, animationId, true);
        }
        Goto(L10);
    }
L10:
    cond &= !EventFlag(eventFlagId);
    if (Signed(spEffectId) != -1) {
        cond &= CharacterHasSpEffect(chrEntityId, spEffectId);
    }
    flag = EventFlag(eventFlagId4);
    WaitFor(cond || flag);
    GotoIf(L19, Signed(animationId2) == -1);
    GotoIf(L20, flag.Passed);
    SetEventFlagID(eventFlagId2, OFF);
    ForceAnimationPlayback(chrEntityId, animationId2, false, true, false);
    WaitFixedTimeSeconds(timeSeconds);
    RestartEvent();
L19:
    SetEventFlagID(eventFlagId2, OFF);
    WaitFixedTimeSeconds(timeSeconds);
    RestartEvent();
L20:
    SetEventFlagID(eventFlagId, OFF);
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

$Event(90005744, Restart, function(entityId, eventFlagId, eventFlagId2, animationId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId2));
    WaitFor(EventFlag(eventFlagId));
    ForceAnimationPlayback(entityId, animationId, false, false, false);
    WaitFor(!EventFlag(eventFlagId) || EventFlag(eventFlagId2));
    RestartIf(!EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
});

$Event(90005745, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, timeSeconds) {
    WaitFixedTimeFrames(1);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    if (EventFlag(eventFlagId2)) {
        WaitFor(EventFlag(eventFlagId) || EventFlag(eventFlagId3));
        EndIf(EventFlag(eventFlagId));
        WaitFixedTimeSeconds(timeSeconds);
        SetEventFlagID(eventFlagId3, OFF);
        RestartEvent();
    }
L10:
    WaitFor(EventFlag(eventFlagId2));
    RestartEvent();
});

$Event(90005746, Restart, function(eventFlagId, eventFlagId2, range) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId));
    SetCharacterTalkRange(eventFlagId, range);
    SetEventFlagID(eventFlagId2, ON);
});

$Event(90005747, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, targetTimeSeconds, eventFlagId4, eventFlagId5, targetTimeSeconds2) {
    WaitFixedTimeFrames(1);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    EndIf(!EventFlag(eventFlagId2));
    WaitFor(EventFlag(eventFlagId) || EventFlag(eventFlagId3));
    EndIf(EventFlag(eventFlagId));
    if (!EventFlag(eventFlagId5)) {
        Goto(L0);
L0:
        WaitFor(ElapsedSeconds(targetTimeSeconds) || EventFlag(eventFlagId4));
    } else {
L1:
        WaitFor(ElapsedSeconds(targetTimeSeconds2) || EventFlag(eventFlagId4));
        Goto(L20);
    }
L20:
    SetEventFlagID(eventFlagId3, OFF);
    RestartEvent();
});

$Event(90005748, Restart, function(entityId, actionButtonParameterId, messageId, displayDistance, eventFlagId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(ActionButtonInArea(actionButtonParameterId, entityId));
    DisplayGenericDialog(messageId, PromptType.YESNO, NumberofOptions.NoButtons, 0, displayDistance);
    SetEventFlagID(eventFlagId, ON);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

$Event(90005749, Restart, function(chrEntityId, chrEntityId2, eventFlagId, eventFlagId2) {
    WaitFixedTimeRealFrames(2);
    if (EventFlag(eventFlagId)) {
        EnableCharacterInvincibility(chrEntityId2);
        EnableCharacterImmortality(chrEntityId);
        if (PlayerIsInOwnWorld()) {
            WaitFor(EntityInRadiusOfEntity(10000, chrEntityId2, 100, 1));
            IssueShortWarpRequest(chrEntityId, TargetEntityType.Character, chrEntityId2, 11);
            WaitFor(HasDamageType(chrEntityId, 0, DamageType.Unspecified));
            SetSpEffect(chrEntityId2, 9910);
            DisableCharacter(chrEntityId);
            DisableCharacterCollision(chrEntityId2);
            SpawnOneshotSFX(TargetEntityType.Character, chrEntityId2, 200, 604220);
            SetNetworkconnectedEventFlagID(eventFlagId2, ON);
            WaitFixedTimeSeconds(5);
            DisableCharacter(chrEntityId2);
            SetCharacterBackreadState(chrEntityId2, true);
            EndEvent();
        }
L19:
        WaitFor(EventFlag(eventFlagId2));
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId2);
        WaitFixedTimeSeconds(5);
        DisableCharacter(chrEntityId2);
        EndEvent();
    }
L20:
    DisableCharacter(chrEntityId);
    WaitFor(EventFlag(eventFlagId));
    EnableCharacter(chrEntityId);
    RestartEvent();
});

// 【共通】会話NPCアイテム光 -- [Common] Conversation NPC item light
$Event(90005750, Default, function(assetEntityId, actionButtonParameterId, itemLotId, eventFlagId, eventFlagId2, eventFlagId3, sfxId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId3) && !AllBatchEventFlags(eventFlagId, eventFlagId2));
    if (Signed(sfxId) != 0) {
        CreateAssetfollowingSFX(assetEntityId, 90, sfxId);
    } else {
        CreateAssetfollowingSFX(assetEntityId, 90, 6101);
    }
    flag = !EventFlag(eventFlagId3) || AllBatchEventFlags(eventFlagId, eventFlagId2);
    WaitFor(ActionButtonInArea(actionButtonParameterId, assetEntityId) || flag);
    if (!flag.Passed) {
        DeleteAssetfollowingSFX(assetEntityId, true);
        AwardItemsIncludingClients(itemLotId);
        EzstateInstructionRequest(10000, 60070, 0);
        EndEvent();
    }
L0:
    DeleteAssetfollowingSFX(assetEntityId, true);
    RestartEvent();
});

// 【共通】会話NPCバリアSFX_ワンショット -- [Common] Conversation NPC Barrier SFX_One Shot
$Event(90005751, Restart, function(entityId, dummypolyId, sfxId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(HasDamageType(entityId, 20000, DamageType.Unspecified) && PlayerIsInOwnWorld());
    SpawnOneshotSFX(TargetEntityType.Asset, entityId, dummypolyId, sfxId);
    RestartEvent();
});

// 【共通】会話NPCバリアSFX_ループ -- [Common] Conversation NPC Barrier SFX_Loop
$Event(90005752, Default, function(assetEntityId, dummypolyId, sfxId, targetTimeSeconds) {
    DisableNetworkSync();
    if (ThisEventSlot()) {
        dmg = HasDamageType(assetEntityId, 20000, DamageType.Unspecified);
        WaitFor(PlayerIsInOwnWorld() && (ElapsedSeconds(targetTimeSeconds) || dmg));
        RestartIf(dmg.Passed);
        DeleteAssetfollowingSFX(assetEntityId, true);
    }
L0:
    WaitFor(PlayerIsInOwnWorld() && HasDamageType(assetEntityId, 20000, DamageType.Unspecified));
    CreateAssetfollowingSFX(assetEntityId, dummypolyId, sfxId);
    RestartEvent();
});

$Event(90005753, Restart, function(entityId, entityId2, eventFlagId, eventFlagId2, eventFlagId3, targetTimeSeconds, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7) {
    WaitFixedTimeFrames(1);
    EndIf(!PlayerIsInOwnWorld());
    WaitForEventFlag(ON, TargetEventFlagType.EventFlag, eventFlagId);
    GotoIf(L0, !EventFlag(eventFlagId6));
    GotoIf(L1, EventFlag(eventFlagId3));
L0:
    WaitFor(
        HasDamageType(entityId2, 20000, DamageType.Unspecified)
            && EntityInRadiusOfEntity(entityId, 20000, 10, 1));
    SetEventFlagID(eventFlagId6, ON);
    GotoIf(L13, EventFlag(eventFlagId3));
    Goto(L10);
L1:
    dmg = HasDamageType(entityId2, 20000, DamageType.Unspecified);
    WaitFor(ElapsedSeconds(targetTimeSeconds) || dmg);
    GotoIf(L11, dmg.Passed);
    Goto(L12);
L10:
    SetEventFlagID(eventFlagId2, ON);
    WaitFor(EventFlag(eventFlagId3));
    Goto(L20);
L11:
    if (!EventFlag(eventFlagId7)) {
        if (EntityInRadiusOfEntity(entityId, 20000, 10, 1)) {
            SetEventFlagID(eventFlagId2, ON);
            WaitFor(EventFlag(eventFlagId4));
            SetEventFlagID(eventFlagId4, OFF);
            SetEventFlagID(eventFlagId7, ON);
        }
    }
    Goto(L20);
L12:
    SetEventFlagID(eventFlagId5, ON);
    SetEventFlagID(eventFlagId6, OFF);
    Goto(L20);
L13:
    SetEventFlagID(eventFlagId2, ON);
    SetEventFlagID(eventFlagId5, OFF);
    WaitFor(EventFlag(eventFlagId4));
    SetEventFlagID(eventFlagId4, OFF);
    SetEventFlagID(eventFlagId7, ON);
    Goto(L20);
L20:
    SetEventFlagID(eventFlagId2, OFF);
    RestartEvent();
});

$Event(90005754, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, areaEntityId, eventFlagId5, eventFlagId6, eventFlagId7, chrEntityId, eventFlagId8, range, eventFlagId9, eventFlagId10, eventFlagId11, eventFlagId12) {
    EndIf(!PlayerIsInOwnWorld());
    SetCharacterBackreadState(chrEntityId, true);
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId6));
    EndIf(EventFlag(eventFlagId4));
    GotoIf(L1, 0 == eventFlagId10);
    Goto(L2);
L1:
    WaitFor(
        EventFlag(eventFlagId8)
            || (InArea(10000, areaEntityId)
                && (!AnyBatchEventFlags(eventFlagId2, eventFlagId3) || EventFlag(eventFlagId))));
    Goto(L3);
L2:
    WaitFor(
        EventFlag(eventFlagId8)
            || (InArea(10000, areaEntityId)
                && (!AnyBatchEventFlags(eventFlagId2, eventFlagId3) || EventFlag(eventFlagId))
                && (!EventFlag(eventFlagId10)
                    || (EventFlag(eventFlagId10) && EventFlag(eventFlagId11)))));
    Goto(L3);
L3:
    if (0 != eventFlagId8) {
        if (EventFlag(eventFlagId8)) {
            BatchSetEventFlags(eventFlagId2, eventFlagId3, OFF);
        }
    }
    if (0 != eventFlagId7) {
        EndIf(EventFlag(eventFlagId7));
    }
    SetEventFlagID(eventFlagId, ON);
    if (0 != eventFlagId12) {
        SetEventFlagID(eventFlagId12, ON);
    }
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTalkRange(chrEntityId, range);
    WaitFor(EventFlag(eventFlagId9) || !EventFlag(eventFlagId));
    if (!EventFlag(eventFlagId5)) {
        EndIf(EventFlag(eventFlagId9));
        RestartEvent();
    }
L0:
    SetEventFlagID(eventFlagId, OFF);
    SetEventFlagID(eventFlagId4, ON);
    EndEvent();
});

$Event(90005755, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, maximumAllowedValue) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId4));
    EndIf(EventFlag(eventFlagId2));
    WaitFor(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId2));
    if (0 != eventFlagId3) {
        SetEventFlagID(eventFlagId3, OFF);
    }
    IncrementEventValue(eventFlagId5, 4, maximumAllowedValue);
    if (EventValue(eventFlagId5, 4) == maximumAllowedValue) {
        SetEventFlagID(eventFlagId4, ON);
    }
    EndEvent();
});

$Event(90005756, Restart, function(eventFlagId, eventFlagId2, eventFlagId3) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    WaitFor(EventFlag(eventFlagId3));
    EndIf(!EventFlag(eventFlagId2));
    SetEventFlagID(eventFlagId, ON);
    EndEvent();
});

$Event(90005757, Restart, function(chrEntityId, chrEntityId2, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4) {
    WaitFixedTimeRealFrames(1);
    DisableCharacter(chrEntityId);
    DisableCharacter(chrEntityId2);
    EndIf(!EventFlag(eventFlagId) || EventFlag(eventFlagId4));
    GotoIf(L1, !EventFlag(eventFlagId2));
    EndIf(!PlayerIsInOwnWorld());
    Goto(L2);
L1:
    EnableCharacter(chrEntityId);
    ForceAnimationPlayback(chrEntityId, 30007, false, false, false);
    WaitFor(CharacterBackreadStatus(chrEntityId));
    WaitFixedTimeRealFrames(1);
    EndEvent();
L2:
    EnableCharacter(chrEntityId2);
    ForceAnimationPlayback(chrEntityId2, 30008, false, false, false);
    SetCharacterTeamType(chrEntityId2, TeamType.Disabled);
    DisableCharacterCollision(chrEntityId2);
    WaitFor(CharacterBackreadStatus(chrEntityId2));
    WaitFixedTimeRealFrames(1);
    EndEvent();
    SetEventFlagID(eventFlagId3, ON);
});

$Event(90005758, Restart, function(eventFlagId, eventFlagId2, animationId, entityId, eventFlagId3) {
    WaitFixedTimeFrames(2);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(!EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    EndIf(EventFlag(eventFlagId2));
    WaitFor(EventFlag(eventFlagId2));
    ForceAnimationPlayback(entityId, animationId, true, false, false);
});

$Event(90005759, Default, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7, eventFlagId8, eventFlagId9, eventFlagId10, timeSeconds, eventFlagId11, targetDistance) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId));
    EndIf(!EventFlag(eventFlagId2));
    EndIf(EventFlag(eventFlagId3));
    if (!EventFlag(eventFlagId11)) {
        if (EventFlag(eventFlagId11)) {
        }
L0:
        EndIf(EventFlag(eventFlagId4));
        WaitFor(
            CharacterRatioDead(chrEntityId)
                || CharacterHPValue(chrEntityId) <= 0
                || EventFlag(eventFlagId4));
        SetEventFlagID(eventFlagId4, ON);
        if (CountEventFlags(TargetEventFlagType.EventFlag, eventFlagId6, eventFlagId7) == 1) {
            SetEventFlagID(eventFlagId8, ON);
        }
        if (CountEventFlags(TargetEventFlagType.EventFlag, eventFlagId6, eventFlagId7) >= 2) {
            SetEventFlagID(eventFlagId9, ON);
            EndIf(EventFlag(eventFlagId10));
            SetEventFlagID(eventFlagId11, ON);
            WaitFixedTimeSeconds(timeSeconds);
            SetEventFlagID(eventFlagId5, ON);
            flag &= EventFlag(eventFlagId3);
        }
        WaitFor(flag);
        SetEventFlagID(eventFlagId11, OFF);
        EndEvent();
    }
L10:
    WaitFor(EntityInRadiusOfEntity(10000, chrEntityId, targetDistance, 1));
    EndIf(EventFlag(eventFlagId10));
    SetEventFlagID(eventFlagId5, ON);
    flag &= EventFlag(eventFlagId3);
    WaitFor(flag);
    SetEventFlagID(eventFlagId11, OFF);
    EndEvent();
});

// 【共通】会話NPC夜敵出現 -- [Common] Conversation NPC enemy appears at night
$Event(90005760, Restart, function(eventFlagId, chrEntityId, areaEntityId, eventFlagId2) {
    EndIf(EventFlag(eventFlagId));
    if (!ThisEventSlot()) {
        WaitFor(
            EventFlag(eventFlagId2)
                && !EventFlag(9000)
                && PlayerIsInOwnWorld()
                && InArea(10000, areaEntityId));
    }
L0:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    ForceAnimationPlayback(chrEntityId, 20000, false, false, false);
    EndEvent();
});

$Event(90005761, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, animationId, range) {
    DisableNetworkSync();
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId)) {
            SetEventFlagID(eventFlagId6, OFF);
        }
    }
L10:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    if (!EventFlag(eventFlagId5)) {
        WaitFor(EventFlag(eventFlagId5));
        RestartEvent();
    }
L0:
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L3, EventFlag(eventFlagId3));
    GotoIf(L4, EventFlag(eventFlagId4));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    if (Signed(-1) != animationId) {
        ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    }
    SetCharacterTalkRange(chrEntityId, range);
    Goto(L20);
L2:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L3:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L4:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    Goto(L20);
L20:
    WaitFor(!EventFlag(eventFlagId5));
    RestartEvent();
});

$Event(90005762, Restart, function(chrEntityId, assetEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7, range) {
    DisableNetworkSync();
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId)) {
            SetEventFlagID(eventFlagId7, OFF);
        }
    }
L10:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableAsset(assetEntityId);
    if (!EventFlag(eventFlagId5)) {
        WaitFor(EventFlag(eventFlagId5));
        RestartEvent();
    }
L0:
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L3, EventFlag(eventFlagId3));
    GotoIf(L4, EventFlag(eventFlagId4));
L1:
    GotoIf(L5, !EventFlag(eventFlagId6));
    Goto(L6);
L5:
    SetCharacterBackreadState(chrEntityId, false);
    DisableCharacter(chrEntityId);
    SetCharacterTeamType(chrEntityId, TeamType.FriendlyNPC);
    EnableAsset(assetEntityId);
    DisableCharacterCollision(chrEntityId);
    SetCharacterTalkRange(chrEntityId, range);
    GotoIf(L20, mainGroupAbuse);
L6:
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacter(chrEntityId);
    SetCharacterTeamType(chrEntityId, TeamType.FriendlyNPC);
    DisableAsset(assetEntityId);
    GotoIf(L20, mainGroupAbuse);
L2:
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacter(chrEntityId);
    DisableAsset(assetEntityId);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L3:
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacter(chrEntityId);
    DisableAsset(assetEntityId);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L4:
    DisableAsset(assetEntityId);
    Goto(L20);
L20:
    WaitFor(!EventFlag(eventFlagId5));
    RestartEvent();
});

$Event(90005763, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, range, assetEntityId, animationId) {
    DisableNetworkSync();
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
    }
L10:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    DisableAsset(assetEntityId);
    if (!EventFlag(eventFlagId3)) {
        WaitFor(EventFlag(eventFlagId3));
        RestartEvent();
    }
L0:
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L4, EventFlag(eventFlagId2));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.Disabled);
    SetCharacterTalkRange(chrEntityId, range);
    if (Signed(-1) != animationId) {
        ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    }
    EnableAsset(assetEntityId);
    WarpAssetToCharacter(assetEntityId, chrEntityId, -1);
    Goto(L20);
L4:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    ForceCharacterTreasure(chrEntityId);
    Goto(L20);
L20:
    WaitFor(!EventFlag(eventFlagId3));
    RestartEvent();
});

$Event(90005764, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, animationId, range, chrEntityId2, assetEntityId) {
    DisableNetworkSync();
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId)) {
            SetEventFlagID(eventFlagId6, OFF);
        }
    }
L10:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    EnableCharacterGravity(chrEntityId);
    DisableAssetInvunerability(assetEntityId);
    if (!EventFlag(eventFlagId5)) {
        WaitFor(EventFlag(eventFlagId5));
        RestartEvent();
    }
L0:
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L3, EventFlag(eventFlagId3));
    GotoIf(L4, EventFlag(eventFlagId4));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacterInvincibility(chrEntityId);
    EnableAssetInvunerability(assetEntityId);
    DisableCharacterGravity(chrEntityId);
    IssueShortWarpRequest(chrEntityId, TargetEntityType.Area, chrEntityId2, -1);
    ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    SetCharacterTalkRange(chrEntityId, range);
    Goto(L20);
L2:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L3:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    SetCharacterTeamType(chrEntityId, TeamType.HostileNPC);
    Goto(L20);
L4:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    Goto(L20);
L20:
    WaitFor(!EventFlag(eventFlagId5));
    RestartEvent();
});

$Event(90005765, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, animationId, range, eventFlagId7, timeSeconds) {
    DisableNetworkSync();
    WaitFixedTimeFrames(1);
    if (PlayerIsInOwnWorld()) {
        if (EventFlag(eventFlagId)) {
            SetEventFlagID(eventFlagId6, OFF);
        }
    }
L10:
    DisableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, true);
    if (!EventFlag(eventFlagId5)) {
        WaitFor(EventFlag(eventFlagId5));
        RestartEvent();
    }
L0:
    GotoIf(L1, EventFlag(eventFlagId));
    GotoIf(L2, EventFlag(eventFlagId2));
    GotoIf(L3, EventFlag(eventFlagId3));
    GotoIf(L4, EventFlag(eventFlagId4));
L1:
    EnableCharacter(chrEntityId);
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacterImmortality(chrEntityId);
    if (Signed(-1) != animationId) {
        ForceAnimationPlayback(chrEntityId, animationId, true, false, false);
    }
    SetCharacterTalkRange(chrEntityId, range);
    Goto(L20);
L2:
L3:
L4:
    Goto(L20);
L20:
    flag = !EventFlag(eventFlagId5);
    WaitFor(
        flag
            || (CountEventFlags(TargetEventFlagType.EventFlag, eventFlagId2, eventFlagId3) == 1
                && EventFlag(eventFlagId7)));
    RestartIf(flag.Passed);
    WaitFixedTimeSeconds(timeSeconds);
    SetEventFlagID(eventFlagId7, OFF);
    RestartEvent();
});

$Event(90005766, Restart, function(eventFlagId, chrEntityId, range, eventFlagId2, eventFlagId3) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId3));
    WaitFor(EventFlag(eventFlagId));
    SetCharacterTalkRange(chrEntityId, range);
    SetEventFlagID(eventFlagId2, ON);
    SetEventFlagID(eventFlagId3, ON);
});

$Event(90005767, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, eventFlagId4, chrEntityId2, eventFlagId5) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    WaitFor(CharacterRatioDead(chrEntityId) || CharacterRatioDead(chrEntityId2));
    BatchSetNetworkconnectedEventFlags(eventFlagId2, eventFlagId3, OFF);
    SetNetworkconnectedEventFlagID(eventFlagId3, ON);
    SetEventFlagID(eventFlagId, ON);
    SetEventFlagID(eventFlagId4, ON);
    SetEventFlagID(4895, OFF);
    if (CharacterRatioDead(chrEntityId2)) {
        SetEventFlagID(eventFlagId5, ON);
    }
    SaveRequest();
});

$Event(90005768, Restart, function(eventFlagId, itemLotId, eventFlagId2, itemLotId2, eventFlagId3, eventFlagId4) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2) && EventFlag(eventFlagId3));
    WaitFor(ElapsedSeconds(2) && EventFlag(eventFlagId));
    GotoIf(L0, EventValue(eventFlagId4, 4) == 0);
    Goto(L1);
L0:
    if (PlayerIsInOwnWorld()) {
        AwardItemsIncludingClients(itemLotId);
    }
    Goto(L5);
L1:
    if (PlayerIsInOwnWorld()) {
        AwardItemsIncludingClients(itemLotId2);
    }
    Goto(L5);
L5:
    EndEvent();
});

$Event(90005769, Restart, function(chrEntityId, eventFlagId, chrEntityId2, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5) {
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId4) || EventFlag(eventFlagId5));
    WaitFor(
        EventFlag(eventFlagId)
            && (CharacterHPValue(chrEntityId) <= 0 || CharacterDead(chrEntityId))
            && (EventFlag(eventFlagId2)
                || CharacterHPValue(chrEntityId2) <= 0
                || CharacterDead(chrEntityId2)));
    SetEventFlagID(eventFlagId3, ON);
});

// 【共通】会話NPCフラグON同期 -- [Common] Conversation NPC flag ON synchronization
$Event(90005770, Restart, function(eventFlagId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId));
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
});

// 【共通】特定篝火付近判定 -- [Common] Judgment near specific bonfires
$Event(90005771, Restart, function(entityId, eventFlagId) {
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, OFF);
    WaitFor(EntityInRadiusOfEntity(10000, entityId, 3, 1));
    SetEventFlagID(eventFlagId, ON);
    WaitFor(!EntityInRadiusOfEntity(10000, entityId, 3, 1));
    RestartEvent();
});

// 【共通】キャラ無効化 -- [Common] Character invalidation
$Event(90005772, Restart, function(chrEntityId) {
    SetCharacterBackreadState(chrEntityId, true);
    DisableCharacter(chrEntityId);
});

// 【共通】セーブ要求 -- [Common] Save request
$Event(90005773, Default, function(eventFlagId) {
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, OFF);
    WaitFor(EventFlag(eventFlagId));
    SaveRequest();
    RestartEvent();
});

// 【共通】疑似マルチ報酬取得 -- [Common] Obtain pseudo multi-reward
$Event(90005774, Default, function(eventFlagId, itemLotId, eventFlagId2) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId2));
    WaitFor(ElapsedSeconds(2) && EventFlag(eventFlagId));
    if (PlayerIsInOwnWorld()) {
        AwardItemsIncludingClients(itemLotId);
    }
    EndEvent();
});

// 【共通】会話NPC地図に情報を書き込む -- [Common] Conversation NPC Write information on the map
$Event(90005775, Restart, function(worldMapPointParamId, eventFlagId, distance) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId));
    OpenWorldMapPoint(worldMapPointParamId, distance);
});

$Event(90005776, Restart, function(eventFlagId, eventFlagId2, itemLotId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(ElapsedSeconds(2) && EventFlag(eventFlagId2));
    AwardItemLot(itemLotId);
    EndEvent();
});

$Event(90005777, Restart, function(chrEntityId, eventFlagId, eventFlagId2, eventFlagId3) {
    WaitFixedTimeFrames(1);
    DisableCharacter(chrEntityId);
    if (!EventFlag(eventFlagId) || EventFlag(eventFlagId2)) {
        EndEvent();
    }
    EndIf(EventFlag(eventFlagId3));
    EnableCharacter(chrEntityId);
    WaitFor(CharacterHPValue(chrEntityId) >= 1 && EventFlag(eventFlagId2));
    RestartEvent();
});

$Event(90005778, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, entityId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    SetEventFlagID(eventFlagId, ON);
    EndIf(EventFlag(eventFlagId2));
    EndIf(EventFlag(eventFlagId3));
    SetEventFlagID(eventFlagId, OFF);
    WaitFor(
        HasDamageType(entityId, 10000, DamageType.Unspecified)
            || HasDamageType(entityId, 40000, DamageType.Unspecified)
            || EventFlag(eventFlagId2)
            || EventFlag(eventFlagId3));
    SetEventFlagID(eventFlagId, ON);
});

$Event(90005779, Restart, function(chrEntityId, eventFlagId, animationId, eventFlagId2, eventFlagId3) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    EndIf(EventFlag(eventFlagId));
    EndIf(!EventFlag(eventFlagId2));
    EndIf(EventFlag(eventFlagId3));
    WaitFor(CharacterHasSpEffect(chrEntityId, 9617));
    EndIf(CharacterHPValue(chrEntityId) < 1);
    ForceAnimationPlayback(chrEntityId, animationId, false, true, false);
});

// 【共通】協力NPC_召喚 -- [Common] Cooperation NPC_Summon
$Event(90005780, Default, function(eventFlagId, eventFlagId2, eventFlagId3, npcEntityId, signType, areaEntityId, eventFlagId4, unknown, value) {
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(npcEntityId, AuthorityLevel.Forced);
    }
    DeleteNPCSummonSign(npcEntityId);
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    if (0 != eventFlagId4) {
        flagOnlineChrArea &= EventFlag(eventFlagId4);
    }
    flagOnlineChrArea &= PlayerIsInOwnWorld()
        && CharacterBackreadStatus(npcEntityId)
        && EntityInRadiusOfEntity(10000, npcEntityId, 10, 1);
    WaitFor(flagOnlineChrArea);
    PlaceNPCSummonSign(signType, npcEntityId, areaEntityId, eventFlagId2, eventFlagId3, unknown);
    EndIf(Signed(0) == value);
});

// 【共通】協力NPC_バックリート有効化 -- [Common] Cooperating NPC_Backleat Activation
$Event(90005781, Default, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId) {
    DisableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    DisableCharacterAI(chrEntityId);
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    WaitFor(EventFlag(eventFlagId2));
    SetCharacterBackreadState(chrEntityId, false);
    EnableCharacter(chrEntityId);
    EnableCharacterCollision(chrEntityId);
    EnableCharacterAI(chrEntityId);
    EnableCharacterDefaultBackread(chrEntityId);
    WaitFor(EventFlag(eventFlagId3));
    DisableCharacterDefaultBackread(chrEntityId);
});

// 【共通】協力NPC_ボス部屋入場 -- [Common] Cooperating NPC_Boss room entry
$Event(90005782, Default, function(eventFlagId, eventFlagId2, chrEntityId, entityId, areaEntityId, animationId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId) && EventFlag(eventFlagId2));
    RequestCharacterAICommand(chrEntityId, 10, 0);
    RequestCharacterAIReplan(chrEntityId);
    SetEventPoint(chrEntityId, areaEntityId, 0);
    WaitFor(InArea(chrEntityId, areaEntityId));
    if (Signed(animationId) != 0) {
        RotateCharacter(chrEntityId, entityId, animationId, true);
    } else {
        RotateCharacter(chrEntityId, entityId, 60060, true);
    }
    time = ElapsedSeconds(3);
    WaitFor(time || InArea(chrEntityId, eventFlagId2));
    RestartIf(time.Passed);
    RequestCharacterAICommand(chrEntityId, -1, 0);
    RequestCharacterAIReplan(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AlwaysUpdate);
});

// 【共通】協力NPC_ボス部屋入場Ver2 -- [Common] Cooperation NPC_Boss room entrance Ver2
$Event(90005784, Default, function(eventFlagId, eventFlagId2, chrEntityId, areaEntityId, areaEntityId2, animationId) {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId) && EventFlag(eventFlagId2));
    RequestCharacterAICommand(chrEntityId, 10, 0);
    RequestCharacterAIReplan(chrEntityId);
    SetEventPoint(chrEntityId, areaEntityId2, 0);
    WaitFor(InArea(chrEntityId, areaEntityId2));
    if (Signed(animationId) != 0) {
        RotateCharacter(chrEntityId, areaEntityId, animationId, true);
    } else {
        RotateCharacter(chrEntityId, areaEntityId, 60060, true);
    }
    time = ElapsedSeconds(3);
    WaitFor(time || InArea(chrEntityId, areaEntityId));
    RestartIf(time.Passed);
    RequestCharacterAICommand(chrEntityId, -1, 0);
    RequestCharacterAIReplan(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AlwaysUpdate);
});

// 【共通】協力NPC_帰還 -- [Common] Cooperation NPC_Return
$Event(90005783, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, npcEntityId, entityId, areaEntityId, value) {
    EndIf(EventFlag(eventFlagId));
    flag = EventFlag(eventFlagId) && EventFlag(eventFlagId2);
    onlineFlagChrArea &= PlayerIsInOwnWorld()
        && EventFlag(eventFlagId2)
        && CharacterAIState(npcEntityId, AIStateType.Combat, NotEqual, 1);
    if (areaEntityId == 0) {
        onlineFlagChrArea &= !EntityInRadiusOfEntity(10000, entityId, 75, 1);
    } else {
        onlineFlagChrArea &= !InArea(10000, areaEntityId);
    }
    onlineFlagArea &= PlayerIsInOwnWorld() && EventFlag(eventFlagId2);
    if (Signed(value) != 2) {
        GotoIf(S0, Signed(value) == 1);
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 180, 1);
        Goto(S1);
S0:
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 360, 1);
    } else {
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 720, 1);
    }
S1:
    WaitFor(flag || onlineFlagChrArea || onlineFlagArea);
    EndIf(EventFlag(eventFlagId) && EventFlag(eventFlagId3));
    SendNPCSummonHome(npcEntityId);
    EndEvent();
});

// 【共通】協力NPC_帰還Ver2 -- [Common] Cooperation NPC_Return Ver2
$Event(90005785, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, npcEntityId, entityId, areaEntityId, targetDistance) {
    EndIf(EventFlag(eventFlagId));
    flag = EventFlag(eventFlagId) && EventFlag(eventFlagId2);
    onlineFlagArea &= PlayerIsInOwnWorld() && EventFlag(eventFlagId2);
    if (areaEntityId == 0) {
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, targetDistance, 1);
    } else {
        onlineFlagArea &= !InArea(10000, areaEntityId);
    }
    WaitFor(flag || onlineFlagArea);
    EndIf(EventFlag(eventFlagId) && EventFlag(eventFlagId3));
    SendNPCSummonHome(npcEntityId);
    EndEvent();
});

// 【共通】敵対NPC_侵入 -- [Common] Hostile NPC_Intrusion
$Event(90005790, Default, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, npcEntityId, signType, areaEntityId, areaEntityId2, timeSeconds, eventFlagId5, unknown, value) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    if (0 != eventFlagId) {
        EndIf(EventFlag(eventFlagId));
    }
    EndIf(EventFlag(eventFlagId2));
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(npcEntityId, AuthorityLevel.Forced);
    }
    EndIf(EventFlag(eventFlagId4));
    onlineFlagArea &= PlayerIsInOwnWorld()
        && !EventFlag(eventFlagId)
        && !EventFlag(eventFlagId2)
        && !EventFlag(eventFlagId3);
    if (0 != eventFlagId5) {
        onlineFlagArea &= EventFlag(eventFlagId5);
    }
    onlineFlagArea &= InArea(10000, areaEntityId2) && !EventFlag(9000);
    WaitFor(onlineFlagArea);
    WaitFixedTimeSeconds(timeSeconds);
    PlaceNPCSummonSign(signType, npcEntityId, areaEntityId, eventFlagId3, eventFlagId4, unknown);
    WaitFixedTimeSeconds(1);
    RestartEvent();
    EndIf(Signed(0) == value);
});

// 【共通】敵対NPC_バックリート有効化 -- [Common] Hostile NPC_Backleat enabled
$Event(90005791, Default, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId) {
    DisableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    DisableCharacterAI(chrEntityId);
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId3));
    WaitFor(EventFlag(eventFlagId2));
    SetCharacterBackreadState(chrEntityId, false);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    EnableCharacter(chrEntityId);
    EnableCharacterCollision(chrEntityId);
    EnableCharacterAI(chrEntityId);
    EnableCharacterDefaultBackread(chrEntityId);
    WaitFor(EventFlag(eventFlagId3));
    DisableCharacterDefaultBackread(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
});

// 【共通】敵対NPC_撃破 -- [Common] Hostile NPC_Defeated
$Event(90005792, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, itemLotId, timeSeconds) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndEvent();
    }
L0:
    WaitFor(CharacterRatioDead(chrEntityId) && EventFlag(eventFlagId2));
    WaitFixedTimeSeconds(timeSeconds);
    SetEventFlagID(eventFlagId, ON);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(Signed(itemLotId) == 0);
    AwardItemsIncludingClients(itemLotId);
    EndEvent();
    flag = EventFlag(eventFlagId3);
});

// 【共通】敵対NPC_帰還 -- [Common] Hostile NPC_Return
$Event(90005793, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, npcEntityId, entityId, areaEntityId, value) {
    EndIf(EventFlag(eventFlagId));
    EndIf(!PlayerIsInOwnWorld());
    flag = EventFlag(eventFlagId);
    onlineFlagChrArea &= PlayerIsInOwnWorld()
        && EventFlag(eventFlagId2)
        && CharacterAIState(npcEntityId, AIStateType.Combat, NotEqual, 1);
    if (areaEntityId == 0) {
        onlineFlagChrArea &= !EntityInRadiusOfEntity(10000, entityId, 110, 1);
    } else {
        onlineFlagChrArea &= !InArea(10000, areaEntityId);
    }
    onlineFlagArea &= PlayerIsInOwnWorld() && EventFlag(eventFlagId2);
    if (Signed(value) != 2) {
        GotoIf(S0, Signed(value) == 1);
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 180, 1);
        Goto(S1);
S0:
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 360, 1);
    } else {
        onlineFlagArea &= !EntityInRadiusOfEntity(10000, entityId, 720, 1);
    }
S1:
    WaitFor(flag || onlineFlagChrArea || onlineFlagArea);
    EndIf(EventFlag(eventFlagId));
    SendNPCSummonHome(npcEntityId);
    EndEvent();
    flag2 = !EventFlag(eventFlagId3);
});

// 【共通】NPC疑似マルチ_開始 -- [Common] NPC pseudo multi_start
$Event(90005795, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, messageId, actionButtonParameterId, assetEntityId, sfxId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId4, OFF);
    SetEventFlagID(eventFlagId5, OFF);
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(EventFlag(eventFlagId));
    WaitFor(
        EventFlag(eventFlagId3)
            && PlayerIsInOwnWorld()
            && !(HasMultiplayerState(MultiplayerState.Multiplayer)
                || HasMultiplayerState(MultiplayerState.MultiplayerPending)));
    CreateAssetfollowingSFX(assetEntityId, 100, sfxId);
    online = HasMultiplayerState(MultiplayerState.Multiplayer)
        || HasMultiplayerState(MultiplayerState.MultiplayerPending);
    WaitFor(
        online
            || ActionButtonInArea(actionButtonParameterId, assetEntityId)
            || !EventFlag(eventFlagId3));
    RestartIf(online.Passed);
    RestartIf(!EventFlag(eventFlagId3));
    DisplayGenericDialogAndSetEventFlags(messageId, PromptType.YESNO, NumberofOptions.TwoButtons, assetEntityId, 2, eventFlagId4, eventFlagId5, eventFlagId5);
    RestartIf(!EventFlag(eventFlagId4));
    SetEventFlagID(eventFlagId2, ON);
    SetSpEffect(10000, 15);
    WaitFixedTimeSeconds(20);
    RestartEvent();
});

// 【共通】NPC疑似マルチ_終了 -- [Common] NPC pseudo-multi_end
$Event(90005796, Restart, function(eventFlagId, chrEntityId, bannerType, areaEntityId) {
    DisableNetworkSync();
    EndIf(PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterRatioDead(chrEntityId));
    SetEventFlagID(eventFlagId, ON);
    DisplayBanner(bannerType);
    if (areaEntityId != 0) {
        SetPsuedoMultiplayerReturnPosition(areaEntityId);
    }
    IssueEndOfPseudoMultiplayerNotification(true);
});

// 【共通】NPC疑似マルチ_終了Ver2 -- [Common] NPC pseudo multi_end Ver2
$Event(90005797, Restart, function(eventFlagId, chrEntityId, bannerType, areaEntityId, spEffectId) {
    DisableNetworkSync();
    EndIf(PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterRatioDead(chrEntityId));
    SetEventFlagID(eventFlagId, ON);
    DisplayBanner(bannerType);
    SetSpEffect(20000, spEffectId);
    if (areaEntityId != 0) {
        SetPsuedoMultiplayerReturnPosition(areaEntityId);
    }
    IssueEndOfPseudoMultiplayerNotification(true);
});

$Event(90005798, Restart, function(eventFlagId, chrEntityId, bannerType, areaEntityId, eventFlagId2, spEffectId) {
    DisableNetworkSync();
    EndIf(PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterRatioDead(chrEntityId));
    SetEventFlagID(eventFlagId, ON);
    DisplayBanner(bannerType);
    SetSpEffect(20000, spEffectId);
    if (areaEntityId != 0) {
        SetPsuedoMultiplayerReturnPosition(areaEntityId);
    }
    WaitFor(EventFlag(eventFlagId2));
    IssueEndOfPseudoMultiplayerNotification(true);
});

$Event(90005799, Restart, function(eventFlagId, chrEntityId, bannerType, areaEntityId, eventFlagId2, chrEntityId2, spEffectId) {
    DisableNetworkSync();
    EndIf(PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    DisableCharacterCollision(chrEntityId2);
    DisableCharacterGravity(chrEntityId2);
    WaitFor(CharacterRatioDead(chrEntityId));
    SetEventFlagID(eventFlagId, ON);
    DisplayBanner(bannerType);
    SetSpEffect(20000, spEffectId);
    if (areaEntityId != 0) {
        SetPsuedoMultiplayerReturnPosition(areaEntityId);
    }
    WaitFor(EventFlag(eventFlagId2));
    ForceCharacterDeath(chrEntityId2, false);
    IssueEndOfPseudoMultiplayerNotification(true);
});

// 【共通】ホストがボス部屋入場 -- [Common] Host enters the boss room
$Event(9005800, Restart, function(eventFlagId, entityId, areaEntityId, eventFlagId2, chrEntityId, actionButtonParameterId, eventFlagId3, areaEntityId2) {
    if (!EventFlag(eventFlagId)) {
        WaitFixedTimeFrames(1);
        if (eventFlagId3 != 0) {
            GotoIf(L0, EventFlag(eventFlagId3));
            if (areaEntityId2 != 0) {
                areaFlag |= InArea(10000, areaEntityId2);
            }
            areaFlag |= EventFlag(eventFlagId3);
            WaitFor((areaFlag && PlayerIsInOwnWorld()) || EventFlag(eventFlagId));
            RestartIf(EventFlag(eventFlagId));
            Goto(L1);
        }
L0:
        if (PlayerIsInOwnWorld()) {
            WaitFor(
                EventFlag(eventFlagId)
                    || (PlayerIsInOwnWorld()
                        && !EventFlag(eventFlagId)
                        && ActionButtonInArea(actionButtonParameterId, entityId)));
            GotoIf(L2, !PlayerIsInOwnWorld());
            RestartIf(EventFlag(eventFlagId));
            SuppressSoundForFogGate(5);
            if (!CharacterHasSpEffect(10000, 4250)) {
                RotateCharacter(10000, areaEntityId, 60060, true);
            } else {
                RotateCharacter(10000, areaEntityId, 60060, false);
            }
        }
L3:
        GotoIf(L1, EventFlag(eventFlagId2));
        time = ElapsedSeconds(3);
        WaitFor(
            ((InArea(10000, areaEntityId) || time)
                && PlayerIsInOwnWorld()
                && !EventFlag(eventFlagId))
                || EventFlag(eventFlagId));
        RestartIf(EventFlag(eventFlagId));
        RestartIf(time.Passed);
L1:
        if (PlayerIsInOwnWorld()) {
            IssueBossRoomEntryNotification();
            SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        }
L2:
        ActivateMultiplayerdependantBuffs(chrEntityId);
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
        EndIf(!PlayerIsInOwnWorld());
        RestartEvent();
    }
L10:
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        PlayerIsInOwnWorld()
            && EventFlag(eventFlagId)
            && (HasMultiplayerState(MultiplayerState.Invasion)
                || HasMultiplayerState(MultiplayerState.InvasionPending))
            && ActionButtonInArea(10000, entityId));
    RotateCharacter(10000, areaEntityId, 60060, true);
    SendInvadingPhantomsHome(0);
    RestartEvent();
});

// 【共通】ゲストがボス部屋入場 -- [Common] Guest enters the boss room
$Event(9005801, Restart, function(eventFlagId, entityId, areaEntityId, eventFlagId2, eventFlagId3, actionButtonParameterId) {
    DisableNetworkSync();
    EndIf(EventFlag(eventFlagId));
    WaitFor(
        !EventFlag(eventFlagId)
            && EventFlag(eventFlagId2)
            && CharacterType(10000, TargetType.WhitePhantom)
            && ActionButtonInArea(actionButtonParameterId, entityId));
    SuppressSoundForFogGate(5);
    RotateCharacter(10000, areaEntityId, 60060, true);
    time = ElapsedSeconds(3);
    WaitFor(CharacterType(10000, TargetType.WhitePhantom) && (InArea(10000, areaEntityId) || time));
    RestartIf(time.Passed);
    SetEventFlagID(eventFlagId3, ON);
    RestartEvent();
});

// 【共通】ボス用篝火処理 -- [Common] Bonfire processing for boss
$Event(9005810, Restart, function(eventFlagId, eventFlagId2, chrEntityId, assetEntityId, enemyDeactivationDistance) {
    if (!EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableAsset(assetEntityId);
        WaitFixedTimeSeconds(1);
        WaitFor(EventFlag(eventFlagId));
        SpawnOneshotSFX(TargetEntityType.Asset, assetEntityId, 200, 1060);
        WaitFixedTimeSeconds(0.5);
        EnableCharacter(chrEntityId);
        EnableAsset(assetEntityId);
    }
L0:
    RegisterBonfire(eventFlagId2, assetEntityId, 5, 180, 0, enemyDeactivationDistance);
});

// 【共通】ボス用白扉処理 -- [Common] White door treatment for boss
$Event(9005811, Restart, function(eventFlagId, assetEntityId, sfxId, eventFlagId2) {
    DisableNetworkSync();
    DisableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    chrFlag = (CharacterType(10000, TargetType.BlackPhantom)
        || CharacterType(10000, TargetType.Invader)
        || CharacterType(10000, TargetType.Invader2)
        || CharacterType(10000, TargetType.Invader3))
        && !EventFlag(eventFlagId);
    chrFlag2 = (CharacterType(10000, TargetType.WhitePhantom) || CharacterType(10000, TargetType.BluePhantom))
        && !EventFlag(eventFlagId);
    if (0 != eventFlagId2) {
        flag &= EventFlag(eventFlagId2);
    }
    flag &= !EventFlag(eventFlagId);
    WaitFor(
        chrFlag
            || chrFlag2
            || flag
            || ((HasMultiplayerState(MultiplayerState.Invasion)
                || HasMultiplayerState(MultiplayerState.InvasionPending))
                && EventFlag(eventFlagId)
                && !CharacterType(10000, TargetType.WhitePhantom))
            || ((HasMultiplayerState(MultiplayerState.Invasion)
                || HasMultiplayerState(MultiplayerState.InvasionPending))
                && EventFlag(eventFlagId)
                && CharacterType(10000, TargetType.WhitePhantom)
                && !EntityInRadiusOfEntity(10000, assetEntityId, 1, 1)));
    EnableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 101, sfxId);
    chrFlag3 = (CharacterType(10000, TargetType.BlackPhantom)
        || CharacterType(10000, TargetType.Invader)
        || CharacterType(10000, TargetType.Invader2)
        || CharacterType(10000, TargetType.Invader3))
        && !EventFlag(eventFlagId);
    chrFlag4 = (CharacterType(10000, TargetType.WhitePhantom) || CharacterType(10000, TargetType.BluePhantom))
        && !EventFlag(eventFlagId);
    if (0 != eventFlagId2) {
        flag2 &= EventFlag(eventFlagId2);
    }
    flag2 &= !EventFlag(eventFlagId);
    WaitFor(
        !chrFlag3
            && !chrFlag4
            && !flag2
            && !((HasMultiplayerState(MultiplayerState.Invasion)
                || HasMultiplayerState(MultiplayerState.InvasionPending))
                && EventFlag(eventFlagId)
                && !CharacterType(10000, TargetType.WhitePhantom))
            && !((HasMultiplayerState(MultiplayerState.Invasion)
                || HasMultiplayerState(MultiplayerState.InvasionPending))
                && EventFlag(eventFlagId)
                && CharacterType(10000, TargetType.WhitePhantom)
                && !EntityInRadiusOfEntity(10000, assetEntityId, 1, 1)));
    RestartEvent();
});

// 【共通】ボス用白扉処理Ver2 -- [Common] Boss white door processing Ver2
$Event(9005812, Restart, function(eventFlagId, assetEntityId, sfxId, eventFlagId2, sfxId2) {
    DisableNetworkSync();
    DisableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    if (!EventFlag(eventFlagId)) {
        if (0 != eventFlagId2) {
            flag &= EventFlag(eventFlagId2);
        }
        flag &= !EventFlag(eventFlagId);
        WaitFor(
            flag
                || (CharacterType(10000, TargetType.WhitePhantom)
                    || CharacterType(10000, TargetType.BluePhantom))
                || (CharacterType(10000, TargetType.BlackPhantom)
                    || CharacterType(10000, TargetType.Invader)
                    || CharacterType(10000, TargetType.Invader2)
                    || CharacterType(10000, TargetType.Invader3)));
        EnableAsset(assetEntityId);
        DeleteAssetfollowingSFX(assetEntityId, true);
        CreateAssetfollowingSFX(assetEntityId, 101, sfxId);
        if (0 != eventFlagId2) {
            flag2 &= EventFlag(eventFlagId2);
        }
        flag2 &= !EventFlag(eventFlagId);
        WaitFor(
            !flag2
                && !(CharacterType(10000, TargetType.WhitePhantom)
                    || CharacterType(10000, TargetType.BluePhantom))
                && !(CharacterType(10000, TargetType.BlackPhantom)
                    || CharacterType(10000, TargetType.Invader)
                    || CharacterType(10000, TargetType.Invader2)
                    || CharacterType(10000, TargetType.Invader3)));
        RestartEvent();
    }
L0:
    WaitFor(
        (HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending))
            || EventFlag(9982));
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending))
            && !EventFlag(9982));
    RestartEvent();
    CreateAssetfollowingSFX(assetEntityId, 101, sfxId2);
});

// 【共通】ボス用白扉処理Ver3 -- [Common] Boss white door processing Ver3
$Event(9005813, Restart, function(eventFlagId, assetEntityId, sfxId, eventFlagId2, sfxId2) {
    DisableNetworkSync();
    DisableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    if (!EventFlag(eventFlagId)) {
        if (0 != eventFlagId2) {
            flag &= EventFlag(eventFlagId2);
        }
        flag &= !EventFlag(eventFlagId);
        WaitFor(
            flag
                || (CharacterType(10000, TargetType.WhitePhantom)
                    || CharacterType(10000, TargetType.BluePhantom))
                || (CharacterType(10000, TargetType.BlackPhantom)
                    || CharacterType(10000, TargetType.Invader)
                    || CharacterType(10000, TargetType.Invader2)
                    || CharacterType(10000, TargetType.Invader3)));
        EnableAsset(assetEntityId);
        DeleteAssetfollowingSFX(assetEntityId, true);
        CreateAssetfollowingSFX(assetEntityId, 101, sfxId);
        if (0 != eventFlagId2) {
            flag2 &= EventFlag(eventFlagId2);
        }
        flag2 &= !EventFlag(eventFlagId);
        WaitFor(
            !flag2
                && !(CharacterType(10000, TargetType.WhitePhantom)
                    || CharacterType(10000, TargetType.BluePhantom))
                && !(CharacterType(10000, TargetType.BlackPhantom)
                    || CharacterType(10000, TargetType.Invader)
                    || CharacterType(10000, TargetType.Invader2)
                    || CharacterType(10000, TargetType.Invader3)));
        RestartEvent();
    }
L0:
    WaitFor(
        HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending)
            || HasMultiplayerState(MultiplayerState.Multiplayer));
    EnableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 101, sfxId2);
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending)
            || HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending)));
    RestartEvent();
});

// 【共通】ボス戦BGM再生_２曲 -- [Common] Boss battle BGM playback_2 songs
$Event(9005822, Restart, function(eventFlagId, bgmBossConvParamId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, value, value2) {
    DisableNetworkSync();
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId2, OFF);
    }
    flag &= EventFlag(eventFlagId2);
    if (!PlayerIsInOwnWorld()) {
        flag &= EventFlag(eventFlagId3);
    }
    if (0 != eventFlagId4) {
        flag &= EventFlag(eventFlagId4);
    }
    WaitFor(flag);
    WaitFixedTimeFrames(1);
    if (!EventFlag(eventFlagId5)) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Start);
    }
    WaitFor(EventFlag(eventFlagId5) || EventFlag(eventFlagId));
    if (!EventFlag(eventFlagId)) {
        WaitFixedTimeFrames(1);
        if (Signed(value) != 0) {
        }
        SetBossBGM(bgmBossConvParamId, BossBGMState.HeatUp);
        WaitFor(EventFlag(eventFlagId));
    }
L1:
    if (Signed(value2) != 1) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Stop2);
        EndEvent();
    }
    SetBossBGM(bgmBossConvParamId, BossBGMState.Stop1);
});

// 【共通】ボス戦BGM再生_３曲 -- [Common] Boss battle BGM playback_3 songs
$Event(9005823, Restart, function(eventFlagId, bgmBossConvParamId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, value, value2) {
    DisableNetworkSync();
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId2, OFF);
    }
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    flag &= EventFlag(eventFlagId2);
    if (!PlayerIsInOwnWorld()) {
        flag &= EventFlag(eventFlagId3);
    }
    if (0 != eventFlagId4) {
        flag &= EventFlag(eventFlagId4);
    }
    WaitFor(flag);
    SetBossBGM(bgmBossConvParamId, BossBGMState.Start);
    flag2 |= EventFlag(eventFlagId5) || EventFlag(eventFlagId6) || EventFlag(eventFlagId);
    WaitFor(flag2);
    if (!EventFlag(eventFlagId)) {
        if (!EventFlag(eventFlagId6)) {
            WaitFixedTimeFrames(1);
            if (Signed(value) != 1) {
            }
            SetBossBGM(bgmBossConvParamId, BossBGMState.HeatUp);
            flag2 |= EventFlag(eventFlagId6) || EventFlag(eventFlagId);
            WaitFor(flag2);
            GotoIf(L2, EventFlag(eventFlagId));
        }
L1:
        Unknown201008(90003003);
        WaitFor(EventFlag(eventFlagId));
    }
L2:
    if (Signed(value2) != 1) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Stop2);
        EndEvent();
    }
    SetBossBGM(bgmBossConvParamId, BossBGMState.Stop1);
});

$Event(9005824, Restart, function(eventFlagId, bgmBossConvParamId, eventFlagId2, eventFlagId3, eventFlagId4, eventFlagId5, eventFlagId6, value, value2) {
    DisableNetworkSync();
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(eventFlagId2, OFF);
    }
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    flag &= EventFlag(eventFlagId2);
    if (!PlayerIsInOwnWorld()) {
        flag &= EventFlag(eventFlagId3);
    }
    if (0 != eventFlagId4) {
        flag &= EventFlag(eventFlagId4);
    }
    WaitFor(flag);
    SetBossBGM(bgmBossConvParamId, BossBGMState.Start);
    flag2 |= EventFlag(eventFlagId5) || EventFlag(eventFlagId6) || EventFlag(eventFlagId);
    WaitFor(flag2);
    if (!EventFlag(eventFlagId)) {
        if (!EventFlag(eventFlagId6)) {
            WaitFixedTimeFrames(1);
            if (Signed(value) != 1) {
            }
            SetBossBGM(bgmBossConvParamId, BossBGMState.HeatUp);
            flag2 |= EventFlag(eventFlagId6) || EventFlag(eventFlagId);
            WaitFor(flag2);
            GotoIf(L2, EventFlag(eventFlagId));
        }
L1:
        SetBossBGM(bgmBossConvParamId, BossBGMState.HeatUp2);
        WaitFor(EventFlag(eventFlagId));
    }
L2:
    if (Signed(value2) != 1) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Stop2);
        EndEvent();
    }
    SetBossBGM(bgmBossConvParamId, BossBGMState.Stop1);
});

// 【共通】ボス戦入場時CS再生 -- [Common] CS playback when entering a boss battle
$Event(90005830, Restart, function(eventFlagId, areaEntityId) {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId) || (InArea(10000, areaEntityId) && PlayerIsInOwnWorld()));
    RestartIf(EventFlag(eventFlagId));
    SetSpEffect(10000, 4250);
    WaitFixedTimeSeconds(3);
    RestartEvent();
});

// 【共通】汎用ボス撃破 -- [Common] Defeat general-purpose boss
$Event(9005840, Restart, function(eventFlagId, eventFlagId2, chrEntityId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(CharacterHPValue(chrEntityId) <= 0);
    WaitFixedTimeSeconds(4);
    PlaySE(chrEntityId, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(chrEntityId));
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.DemigodFelled);
    SetEventFlagID(eventFlagId, ON);
    if (eventFlagId2 != 0) {
        SetEventFlagID(eventFlagId2, ON);
    }
});

// 【共通】汎用ボス出現 -- [Common] General boss appearance
$Event(9005845, Restart, function(eventFlagId, chrEntityId) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndEvent();
    }
L0:
    DisableCharacterAI(chrEntityId);
    if (!EventFlag(11000801)) {
        WaitFor(
            (PlayerIsInOwnWorld() && EntityInRadiusOfEntity(10000, 11000800, 20, 1))
                || HasDamageType(chrEntityId, 10000, DamageType.Unspecified));
        SetNetworkconnectedEventFlagID(11000801, ON);
    } else {
L1:
        WaitFor(EventFlag(11002805) && InArea(10000, 11002800));
    }
L2:
    EnableCharacterAI(11005800);
    SetNetworkUpdateRate(11005800, true, CharacterUpdateFrequency.AlwaysUpdate);
    DisplayBossHealthBar(Enabled, 11000800, 0, 0);
});

// 【共通】フィールドボス撃破 -- [Common] Defeat field boss
$Event(90005860, Restart, function(eventFlagId, eventFlagId2, chrEntityId, value, itemLotId, timeSeconds) {
    if (Signed(itemLotId) != 0) {
        Unknown200476(eventFlagId, itemLotId);
    }
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndIf(!PlayerIsInOwnWorld());
        EndIf(Signed(itemLotId) == 0);
        WaitFixedTimeSeconds(1);
        AwardItemsIncludingClients(itemLotId);
        EndEvent();
    }
L0:
    WaitFor(CharacterHPValue(chrEntityId) <= 0);
    WaitFixedTimeSeconds(2);
    PlaySE(chrEntityId, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(chrEntityId));
    GotoIf(S0, value == 3);
    if (value != 2) {
        if (value != 1) {
            HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.EnemyFelled);
            Goto(L1);
        }
        HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.GreatEnemyFelled);
    }
    Goto(L1);
S0:
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.DemigodFelled);
    Goto(L1);
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.LegendFelled);
L1:
    SetEventFlagID(eventFlagId, ON);
    if (eventFlagId2 != 0) {
        SetEventFlagID(eventFlagId2, ON);
    }
    EndIf(!PlayerIsInOwnWorld());
    EndIf(Signed(itemLotId) == 0);
    WaitFixedTimeSeconds(5);
    AwardItemsIncludingClients(itemLotId);
    EndEvent();
    WaitFixedTimeSeconds(timeSeconds);
});

// 【共通】フィールドボス撃破_竜餐 -- [Common] Defeat Field Boss_Dragon Dinner
$Event(90005861, Restart, function(eventFlagId, eventFlagId2, chrEntityId, value, itemLotId, messageId, timeSeconds) {
    if (Signed(itemLotId) != 0) {
        Unknown200476(eventFlagId, itemLotId);
    }
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        EndIf(!PlayerIsInOwnWorld());
        EndIf(Signed(itemLotId) == 0);
        WaitFixedTimeSeconds(1);
        AwardItemsIncludingClients(itemLotId);
        EndEvent();
    }
L0:
    WaitFor(CharacterHPValue(chrEntityId) <= 0);
    WaitFixedTimeSeconds(2);
    PlaySE(chrEntityId, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(chrEntityId));
    GotoIf(S0, value == 3);
    if (value != 2) {
        if (value != 1) {
            HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.EnemyFelled);
            Goto(L1);
        }
        HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.GreatEnemyFelled);
    }
    Goto(L1);
S0:
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.DemigodFelled);
    Goto(L1);
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.LegendFelled);
L1:
    SetEventFlagID(eventFlagId, ON);
    if (eventFlagId2 != 0) {
        SetEventFlagID(eventFlagId2, ON);
    }
    EndIf(!PlayerIsInOwnWorld());
    EndIf(Signed(itemLotId) == 0);
    WaitFixedTimeSeconds(5);
    AwardItemsIncludingClients(itemLotId);
    WaitFixedTimeSeconds(2);
    DisplayBlinkingMessage(messageId);
    EndEvent();
    WaitFixedTimeSeconds(timeSeconds);
});

// 【共通】フィールドボスHPゲージ -- [Common] Field boss HP gauge
$Event(90005870, Default, function(chrEntityId, nameId, npcThreatLevel) {
    DisableNetworkSync();
    WaitFor(
        CharacterAIState(chrEntityId, AIStateType.Combat)
            && FieldBattleBGMActive(npcThreatLevel)
            && !EventFlag(9000));
    GotoIf(L0, !EventFlag(9290));
    GotoIf(L1, !EventFlag(9291));
    WaitFixedTimeSeconds(5);
    RestartEvent();
L0:
    SetEventFlagID(9290, ON);
    WaitFixedTimeSeconds(1);
    DisplayBossHealthBar(Enabled, chrEntityId, 0, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    WaitFor(
        !(CharacterAIState(chrEntityId, AIStateType.Combat) && FieldBattleBGMActive(npcThreatLevel))
            || CharacterDead(chrEntityId)
            || EventFlag(9000));
    if (CharacterDead(chrEntityId)) {
        WaitFixedTimeSeconds(3);
    } else if (!EventFlag(9000)) {
        WaitFixedTimeSeconds(1);
    }
    DisplayBossHealthBar(Disabled, chrEntityId, 0, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    SetEventFlagID(9290, OFF);
    RestartEvent();
L1:
    SetEventFlagID(9291, ON);
    WaitFixedTimeSeconds(1);
    DisplayBossHealthBar(Enabled, chrEntityId, 1, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    WaitFor(
        !(CharacterAIState(chrEntityId, AIStateType.Combat) && FieldBattleBGMActive(npcThreatLevel))
            || CharacterDead(chrEntityId)
            || EventFlag(9000));
    if (CharacterDead(chrEntityId)) {
        WaitFixedTimeSeconds(3);
    } else if (!EventFlag(9000)) {
        WaitFixedTimeSeconds(1);
    }
    DisplayBossHealthBar(Disabled, chrEntityId, 1, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    SetEventFlagID(9291, OFF);
    RestartEvent();
});

// 【共通】フィールドボスHPゲージ_騎乗 -- [Common] Field Boss HP Gauge_Riding
$Event(90005871, Default, function(chrEntityId, nameId, npcThreatLevel, chrEntityId2) {
    DisableNetworkSync();
    WaitFor(
        CharacterAIState(chrEntityId, AIStateType.Combat)
            && FieldBattleBGMActive(npcThreatLevel)
            && !EventFlag(9000));
    GotoIf(L0, !EventFlag(9290));
    GotoIf(L1, !EventFlag(9291));
    WaitFixedTimeSeconds(5);
    RestartEvent();
L0:
    SetEventFlagID(9290, ON);
    WaitFixedTimeSeconds(1);
    DisplayBossHealthBar(Enabled, chrEntityId, 0, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
        SetNetworkUpdateAuthority(chrEntityId2, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId2, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    WaitFor(
        !(CharacterAIState(chrEntityId, AIStateType.Combat) && FieldBattleBGMActive(npcThreatLevel))
            || CharacterDead(chrEntityId)
            || EventFlag(9000));
    if (CharacterDead(chrEntityId)) {
        WaitFixedTimeSeconds(3);
    } else if (!EventFlag(9000)) {
        WaitFixedTimeSeconds(1);
    }
    DisplayBossHealthBar(Disabled, chrEntityId, 0, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
        SetNetworkUpdateAuthority(chrEntityId2, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId2, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    SetEventFlagID(9290, OFF);
    RestartEvent();
L1:
    SetEventFlagID(9291, ON);
    WaitFixedTimeSeconds(1);
    DisplayBossHealthBar(Enabled, chrEntityId, 1, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Forced);
        SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    WaitFor(
        !(CharacterAIState(chrEntityId, AIStateType.Combat) && FieldBattleBGMActive(npcThreatLevel))
            || CharacterDead(chrEntityId)
            || EventFlag(9000));
    if (CharacterDead(chrEntityId)) {
        WaitFixedTimeSeconds(3);
    } else if (!EventFlag(9000)) {
        WaitFixedTimeSeconds(1);
    }
    DisplayBossHealthBar(Disabled, chrEntityId, 1, nameId);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
        SetNetworkUpdateAuthority(chrEntityId, AuthorityLevel.Normal);
        SetNetworkUpdateRate(chrEntityId, false, CharacterUpdateFrequency.AtLeastEvery2Frames);
    }
    SetEventFlagID(9291, OFF);
    RestartEvent();
});

// 【共通】フィールドボス_HU通知 -- [Common] Field Boss_HU notification
$Event(90005872, Default, function(chrEntityId, npcThreatLevel, eventFlagId) {
    DisableNetworkSync();
    if (0 != eventFlagId) {
        flagHp &= EventFlag(eventFlagId);
    } else {
        flagHp &= HPRatio(chrEntityId) <= 0.55;
    }
    flagHp &= FieldBattleBGMActive(npcThreatLevel);
    WaitFor(flagHp);
    SetFieldBattleBGMHeatUp(npcThreatLevel, true);
    WaitFor(CharacterDead(chrEntityId) || !FieldBattleBGMActive(npcThreatLevel));
    SetFieldBattleBGMHeatUp(npcThreatLevel, false);
    WaitFixedTimeSeconds(0.3);
    RestartEvent();
});

// 【共通】円形サークルボス撃破 -- [Common] Defeat the circle boss
$Event(90005880, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, itemLotId, areaId, blockId, regionId, indexId, initialAreaEntityId) {
    EndIf(EventFlag(eventFlagId));
    EndIf(!PlayerIsInOwnWorld());
    EndIf(!EventFlag(eventFlagId2));
    WaitFor(CharacterDead(chrEntityId));
    WaitFixedTimeSeconds(3);
    HandleBossDefeatAndDisplayBanner(chrEntityId, TextBannerType.EnemyFelled);
    DeactivateGparamOverride(10);
    AwardItemsIncludingClients(itemLotId);
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    WaitFixedTimeSeconds(5);
    SetSpEffect(20000, 8870);
    WaitFixedTimeSeconds(2);
    SetEventFlagID(eventFlagId3, ON);
    SetEventFlagID(9295, ON);
    WarpPlayer(areaId, blockId, regionId, indexId, initialAreaEntityId, 0);
    EndEvent();
});

// 【共通】円形サークルボス開始 -- [Common] Circular circle boss start
$Event(90005881, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, eventFlagId4, messageId, entityId, areaId, blockId, regionId, indexId, initialAreaEntityId) {
    SetEventFlagID(eventFlagId3, OFF);
    SetEventFlagID(eventFlagId4, OFF);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId2));
    WaitFor(
        !HasMultiplayerState(MultiplayerState.MultiplayerPending)
            && HasMultiplayerState(MultiplayerState.Singleplayer)
            && ActionButtonInArea(9230, entityId));
    DisplayGenericDialogAndSetEventFlags(messageId, PromptType.YESNO, NumberofOptions.TwoButtons, entityId, 3, eventFlagId3, eventFlagId4, eventFlagId4);
    RestartIf(EventFlag(eventFlagId4));
    RestartIf(
        HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending));
    SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    SetSpEffect(10000, 514);
    WaitFixedTimeFrames(1);
    ForceAnimationPlayback(10000, 60450, false, false, false);
    WaitFixedTimeSeconds(1.5);
    WarpCharacterAndCopyFloorWithFadeout(10000, TargetEntityType.Area, initialAreaEntityId, -1, 10000, true, true);
    SetEventFlagID(9021, ON);
    EndEvent();
    WarpPlayer(areaId, blockId, regionId, indexId, initialAreaEntityId, 0);
});

// 【共通】円形サークルボス出現 -- [Common] Circular circle boss appears
$Event(90005882, Restart, function(eventFlagId, eventFlagId2, eventFlagId3, chrEntityId, eventFlagId4, chrEntityId2, assetEntityId, chrEntityId3, entityId, nameId, animationId, animationId2) {
    if (EventFlag(eventFlagId)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
        ForceCharacterDeath(chrEntityId, false);
        DisableAsset(assetEntityId);
        EndEvent();
    }
L0:
    DisableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    DisableCharacterAI(chrEntityId);
    DisableAsset(assetEntityId);
    EndIf(!EventFlag(eventFlagId2));
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    SetEventFlagID(1099002100, ON);
    SetEventFlagID(eventFlagId3, ON);
    SetSpEffect(10000, 190);
    ActivateGparamOverride(0, 0);
    ChangeWeather(Weather.PuffyClouds, -1, false);
    ShootBullet(chrEntityId3, entityId, 100, 100500, 0, 90, 0);
    DisableCharacter(chrEntityId2);
    DisableCharacterCollision(chrEntityId2);
    DisableCharacterAI(chrEntityId2);
    if (Signed(-1) != animationId) {
        ForceAnimationPlayback(chrEntityId, animationId, false, false, false);
    } else {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
    }
    DisableCharacterHPBarDisplay(chrEntityId);
    SetNetworkconnectedEventFlagID(eventFlagId2, OFF);
    SetSpEffect(10000, 514);
    EnableAsset(assetEntityId);
    CreateAssetfollowingSFX(assetEntityId, 200, 806700);
    ForceAnimationPlayback(10000, 60451, false, false, false);
    WaitFixedTimeSeconds(1);
    SetSpEffect(20000, 8870);
    WaitFor(
        !EntityInRadiusOfEntity(10000, assetEntityId, 12, 1)
            || HasDamageType(chrEntityId, 10000, DamageType.Unspecified)
            || HasDamageType(chrEntityId, 0, DamageType.Unspecified));
    SetEventFlagID(1099002100, OFF);
    if (Signed(-1) == animationId) {
        EnableCharacter(chrEntityId);
        EnableCharacterCollision(chrEntityId);
    }
    if (Signed(-1) != animationId2) {
        ForceAnimationPlayback(chrEntityId, animationId2, false, false, false);
    }
    EnableCharacterAI(chrEntityId);
    SetNetworkUpdateRate(chrEntityId, true, CharacterUpdateFrequency.AlwaysUpdate);
    SetEventFlagID(eventFlagId4, ON);
    WaitFixedTimeSeconds(1);
    DisplayBossHealthBar(Enabled, chrEntityId, 0, nameId);
});

// 【共通】円形サークルトリガー出現 -- [Common] Circular circle trigger appears
$Event(90005883, Restart, function(eventFlagId, eventFlagId2, entityId) {
    ForceAnimationPlayback(entityId, 0, true, false, false);
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    ForceAnimationPlayback(entityId, 10, true, false, false);
    EndIf(EventFlag(eventFlagId2));
    WaitFor(
        HasMultiplayerState(MultiplayerState.Singleplayer)
            && !HasMultiplayerState(MultiplayerState.MultiplayerPending));
    WaitFixedTimeFrames(1);
    ForceAnimationPlayback(entityId, 1, true, false, false);
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.Singleplayer)
            && !HasMultiplayerState(MultiplayerState.MultiplayerPending)));
    WaitFixedTimeFrames(1);
    RestartEvent();
});

// 【共通】円形サークルバディ石碑出現 -- [Common] Circular circle buddy stone monument appears
$Event(90005884, Restart, function(eventFlagId, eventFlagId2, chrEntityId, assetEntityId) {
    SetSpEffect(chrEntityId, 9531);
    DisableCharacterAI(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    DisableAsset(assetEntityId);
    EndIf(!EventFlag(eventFlagId));
    EndIf(!EventFlag(eventFlagId2));
    EndIf(!PlayerIsInOwnWorld());
    WaitFixedTimeFrames(1);
    SetSpEffect(chrEntityId, 9532);
    EnableCharacterCollision(chrEntityId);
    EnableAsset(assetEntityId);
});

// 【共通】円形サークルボス戦BGM再生_２曲 -- [Common] Circular circle boss battle BGM playback_2 songs
$Event(90005885, Restart, function(eventFlagId, bgmBossConvParamId, eventFlagId2, eventFlagId3, value, value2) {
    DisableNetworkSync();
    if (EventFlag(eventFlagId)) {
        EndEvent();
    }
L0:
    WaitFor(EventFlag(eventFlagId2));
    WaitFixedTimeFrames(1);
    if (Signed(0) != bgmBossConvParamId) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Start);
    } else {
        SetBossBGM(921100, BossBGMState.Start);
    }
    WaitFor(EventFlag(eventFlagId3) || EventFlag(eventFlagId));
    if (!EventFlag(eventFlagId)) {
        WaitFixedTimeFrames(1);
        if (Signed(value) != 1) {
            if (Signed(0) != bgmBossConvParamId) {
                SetBossBGM(bgmBossConvParamId, BossBGMState.HeatUp);
            } else {
                SetBossBGM(925000, BossBGMState.HeatUp);
            }
        }
        WaitFor(EventFlag(eventFlagId));
    }
L1:
    if (Signed(value2) != 1) {
        if (Signed(0) != bgmBossConvParamId) {
            SetBossBGM(bgmBossConvParamId, BossBGMState.Stop2);
        } else {
            SetBossBGM(925000, BossBGMState.Stop2);
        }
        EndEvent();
    }
    if (Signed(0) != bgmBossConvParamId) {
        SetBossBGM(bgmBossConvParamId, BossBGMState.Stop1);
    } else {
        SetBossBGM(925000, BossBGMState.Stop1);
    }
});

// 【共通】敵対マルチ用白壁対応 -- [Common] Compatible with white walls for enemy multiplayer
$Event(91005600, Restart, function(eventFlagId, assetEntityId, sfxId) {
    DisableNetworkSync();
    DisableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    WaitFor(
        (HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending)
            || HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending))
            || EventFlag(9982));
    EnableAsset(assetEntityId);
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 101, sfxId);
    WaitFor(
        !(HasMultiplayerState(MultiplayerState.Multiplayer)
            || HasMultiplayerState(MultiplayerState.MultiplayerPending)
            || HasMultiplayerState(MultiplayerState.Invasion)
            || HasMultiplayerState(MultiplayerState.InvasionPending))
            && !EventFlag(9982));
    RestartEvent();
    WaitFor(EventFlag(eventFlagId));
});

// 【共通】篝火の導き -- [Common] Bonfire Guidance
$Event(90005100, Restart, function(eventFlagId, eventFlagId2, assetEntityId, eventFlagId3, thresholdValue, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7, eventFlagId8, eventFlagId9, eventFlagId10, eventFlagId11, eventFlagId12, eventFlagId13) {
    if (!EventFlag(9000)) {
        DeleteAssetfollowingSFX(assetEntityId, false);
        WaitFixedTimeFrames(1);
    }
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId2) && !EventFlag(9000));
    CreateAssetfollowingSFX(assetEntityId, 100, 6400);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
    } else if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
    } else if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
    } else if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
    } else if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
    } else if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
    } else if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId10, ON);
    } else if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId11, ON);
    } else if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId12, ON);
    } else {
        SetEventFlagID(eventFlagId13, ON);
        Goto(L6);
    }
L6:
    if (PlayerIsInOwnWorld()) {
        if (!EventFlag(69080)) {
            WaitFor(PlayerIsInOwnWorld() && !CharacterHasSpEffect(10000, 100680));
            SetEventFlagID(710510, ON);
            ShowTutorialPopup(1510, true, true);
            DirectlyGivePlayerItem(ItemType.Goods, 9108, 710510, 1);
            SetEventFlagID(69080, ON);
        }
    }
L5:
    EndEvent();
    DeleteAssetfollowingSFX(assetEntityId, false);
    EndIf(!PlayerIsInOwnWorld());
    if (EventFlag(eventFlagId)) {
        SetEventFlagID(eventFlagId4, OFF);
        SetEventFlagID(eventFlagId5, OFF);
        SetEventFlagID(eventFlagId6, OFF);
        SetEventFlagID(eventFlagId7, OFF);
        SetEventFlagID(eventFlagId8, OFF);
        SetEventFlagID(eventFlagId9, OFF);
        SetEventFlagID(eventFlagId10, OFF);
        SetEventFlagID(eventFlagId11, OFF);
        SetEventFlagID(eventFlagId12, OFF);
        SetEventFlagID(eventFlagId13, OFF);
        EndEvent();
    }
L3:
    EndIf(EventValue(eventFlagId3, 4) > thresholdValue);
    WaitFor(EventFlag(eventFlagId) || (EventFlag(eventFlagId2) && !EventFlag(9000)));
    RestartIf(EventValue(eventFlagId3, 4) > thresholdValue);
    CreateAssetfollowingSFX(assetEntityId, 100, 6400);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
        EventValueOperation(eventFlagId3, 4, 0, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId4, OFF);
    }
    if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
        EventValueOperation(eventFlagId3, 4, 1, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId5, OFF);
    }
    if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
        EventValueOperation(eventFlagId3, 4, 2, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId6, OFF);
    }
    if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
        EventValueOperation(eventFlagId3, 4, 3, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId7, OFF);
    }
    if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
        EventValueOperation(eventFlagId3, 4, 4, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId8, OFF);
    }
    if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 5, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 6, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 7, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 8, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 9) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 9, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    WaitFor(EventValue(eventFlagId3, 4) != thresholdValue || EventFlag(eventFlagId));
    WaitFixedTimeFrames(1);
    RestartEvent();
});

// 【共通】篝火の導き_NT用 -- [Common] Bonfire Guidance_For NT
$Event(90005101, Restart, function(eventFlagId, eventFlagId2, assetEntityId, eventFlagId3, thresholdValue, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7, eventFlagId8, eventFlagId9, eventFlagId10, eventFlagId11, eventFlagId12, eventFlagId13) {
    if (!EventFlag(9000)) {
        DeleteAssetfollowingSFX(assetEntityId, false);
        WaitFixedTimeFrames(1);
    }
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId2) && !EventFlag(9000));
    CreateAssetfollowingSFX(assetEntityId, 100, 6401);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
    } else if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
    } else if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
    } else if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
    } else if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
    } else if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
    } else if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId10, ON);
    } else if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId11, ON);
    } else if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId12, ON);
    } else {
        SetEventFlagID(eventFlagId13, ON);
        Goto(L6);
    }
L6:
    if (PlayerIsInOwnWorld()) {
        if (!EventFlag(710510)) {
            WaitFor(PlayerIsInOwnWorld() && !CharacterHasSpEffect(10000, 100680));
            SetEventFlagID(710510, ON);
            ShowTutorialPopup(1510, true, true);
            DirectlyGivePlayerItem(ItemType.Goods, 9108, 710510, 1);
        }
    }
L5:
    EndEvent();
    DeleteAssetfollowingSFX(assetEntityId, false);
    EndIf(!PlayerIsInOwnWorld());
    if (EventFlag(eventFlagId)) {
        SetEventFlagID(eventFlagId4, OFF);
        SetEventFlagID(eventFlagId5, OFF);
        SetEventFlagID(eventFlagId6, OFF);
        SetEventFlagID(eventFlagId7, OFF);
        SetEventFlagID(eventFlagId8, OFF);
        SetEventFlagID(eventFlagId9, OFF);
        SetEventFlagID(eventFlagId10, OFF);
        SetEventFlagID(eventFlagId11, OFF);
        SetEventFlagID(eventFlagId12, OFF);
        SetEventFlagID(eventFlagId13, OFF);
        EndEvent();
    }
L3:
    EndIf(EventValue(eventFlagId3, 4) > thresholdValue);
    WaitFor(EventFlag(eventFlagId) || (EventFlag(eventFlagId2) && !EventFlag(9000)));
    RestartIf(EventValue(eventFlagId3, 4) > thresholdValue);
    CreateAssetfollowingSFX(assetEntityId, 100, 6401);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
        EventValueOperation(eventFlagId3, 4, 0, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId4, OFF);
    }
    if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
        EventValueOperation(eventFlagId3, 4, 1, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId5, OFF);
    }
    if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
        EventValueOperation(eventFlagId3, 4, 2, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId6, OFF);
    }
    if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
        EventValueOperation(eventFlagId3, 4, 3, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId7, OFF);
    }
    if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
        EventValueOperation(eventFlagId3, 4, 4, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId8, OFF);
    }
    if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 5, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 6, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 7, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 8, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 9) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 9, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    WaitFor(EventValue(eventFlagId3, 4) != thresholdValue || EventFlag(eventFlagId));
    WaitFixedTimeFrames(1);
    RestartEvent();
});

$Event(90005102, Restart, function(eventFlagId, eventFlagId2, assetEntityId, eventFlagId3, thresholdValue, eventFlagId4, eventFlagId5, eventFlagId6, eventFlagId7, eventFlagId8, eventFlagId9, eventFlagId10, eventFlagId11, eventFlagId12, eventFlagId13, eventFlagId14) {
    if (!EventFlag(9000)) {
        DeleteAssetfollowingSFX(assetEntityId, false);
        WaitFixedTimeFrames(1);
    }
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(eventFlagId2) && !EventFlag(9000) && EventFlag(eventFlagId14));
    CreateAssetfollowingSFX(assetEntityId, 100, 6400);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
    } else if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
    } else if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
    } else if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
    } else if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
    } else if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
    } else if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId10, ON);
    } else if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId11, ON);
    } else if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId12, ON);
    } else {
        SetEventFlagID(eventFlagId13, ON);
        Goto(L6);
    }
L6:
    if (PlayerIsInOwnWorld()) {
        if (!EventFlag(69080)) {
            WaitFor(PlayerIsInOwnWorld() && !CharacterHasSpEffect(10000, 100680));
            SetEventFlagID(710510, ON);
            ShowTutorialPopup(1510, true, true);
            DirectlyGivePlayerItem(ItemType.Goods, 9108, 710510, 1);
            SetEventFlagID(69080, ON);
        }
    }
L5:
    EndEvent();
    DeleteAssetfollowingSFX(assetEntityId, false);
    EndIf(!PlayerIsInOwnWorld());
    if (EventFlag(eventFlagId)) {
        SetEventFlagID(eventFlagId4, OFF);
        SetEventFlagID(eventFlagId5, OFF);
        SetEventFlagID(eventFlagId6, OFF);
        SetEventFlagID(eventFlagId7, OFF);
        SetEventFlagID(eventFlagId8, OFF);
        SetEventFlagID(eventFlagId9, OFF);
        SetEventFlagID(eventFlagId10, OFF);
        SetEventFlagID(eventFlagId11, OFF);
        SetEventFlagID(eventFlagId12, OFF);
        SetEventFlagID(eventFlagId13, OFF);
        EndEvent();
    }
L3:
    EndIf(EventValue(eventFlagId3, 4) > thresholdValue);
    WaitFor(EventFlag(eventFlagId) || (EventFlag(eventFlagId2) && !EventFlag(9000)));
    RestartIf(EventValue(eventFlagId3, 4) > thresholdValue);
    CreateAssetfollowingSFX(assetEntityId, 100, 6400);
    if (thresholdValue == 0) {
        SetEventFlagID(eventFlagId4, ON);
        EventValueOperation(eventFlagId3, 4, 0, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId4, OFF);
    }
    if (thresholdValue == 1) {
        SetEventFlagID(eventFlagId5, ON);
        EventValueOperation(eventFlagId3, 4, 1, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId5, OFF);
    }
    if (thresholdValue == 2) {
        SetEventFlagID(eventFlagId6, ON);
        EventValueOperation(eventFlagId3, 4, 2, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId6, OFF);
    }
    if (thresholdValue == 3) {
        SetEventFlagID(eventFlagId7, ON);
        EventValueOperation(eventFlagId3, 4, 3, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId7, OFF);
    }
    if (thresholdValue == 4) {
        SetEventFlagID(eventFlagId8, ON);
        EventValueOperation(eventFlagId3, 4, 4, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId8, OFF);
    }
    if (thresholdValue == 5) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 5, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 6) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 6, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 7) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 7, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 8) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 8, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    if (thresholdValue == 9) {
        SetEventFlagID(eventFlagId9, ON);
        EventValueOperation(eventFlagId3, 4, 9, 0, 1, CalculationType.Assign);
    } else {
        SetEventFlagID(eventFlagId9, OFF);
    }
    WaitFor(EventValue(eventFlagId3, 4) != thresholdValue || EventFlag(eventFlagId));
    WaitFixedTimeFrames(1);
    RestartEvent();
});

// 【共通】大ルーン取得 -- [Common] Obtain a large rune
$Event(90005110, Restart, function(eventFlagId, eventFlagId2, assetEntityId, itemLotId, itemId, sfxId, actionButtonParameterId, animationId, value) {
    EndIf(EventFlag(eventFlagId));
    EndIf(!PlayerIsInOwnWorld());
    EndIf(!EventFlag(eventFlagId2));
    DeleteAssetfollowingSFX(assetEntityId, true);
    CreateAssetfollowingSFX(assetEntityId, 100, sfxId);
    WaitFor(PlayerIsInOwnWorld() && ActionButtonInArea(actionButtonParameterId, assetEntityId));
    RotateCharacter(10000, assetEntityId, -1, true);
    ForceAnimationPlayback(10000, animationId, false, false, false);
    DeleteAssetfollowingSFX(assetEntityId, true);
    WaitFixedTimeSeconds(4);
    DisplayBanner(TextBannerType.GreatRuneRestored);
    AwardItemsIncludingClients(itemLotId);
    RemoveItemFromPlayer(ItemType.Goods, itemId, 1);
    SetEventFlagID(eventFlagId, ON);
    EndEvent();
    EndIf(Signed(value) == 0);
});

// 【共通】テスト_小篝火SFX -- [Common] Test_Small Bonfire SFX
$Event(9005910, Restart, function(assetEntityId, eventFlagId, eventFlagId2, value) {
    DeleteAssetfollowingSFX(assetEntityId, true);
    GotoIf(L1, !AnyBatchEventFlags(eventFlagId, eventFlagId2));
    GotoIf(L2, !AllBatchEventFlags(eventFlagId, eventFlagId2));
    Goto(L9);
L1:
    if (Signed(3) >= value) {
        CreateAssetfollowingSFX(assetEntityId, 201, 62);
    } else {
        CreateAssetfollowingSFX(assetEntityId, 201, 63);
    }
    WaitFor(AnyBatchEventFlags(eventFlagId, eventFlagId2));
    RestartEvent();
L2:
    CreateAssetfollowingSFX(assetEntityId, 201, 61);
    WaitFor(AllBatchEventFlags(eventFlagId, eventFlagId2));
    RestartEvent();
L9:
    DeleteAssetfollowingSFX(assetEntityId, true);
    EndEvent();
});

// 【共通】小篝火_お試しSFX -- [Common] Small Bonfire_Trial SFX
$Event(9005911, Restart, function(assetEntityId) {
    CreateAssetfollowingSFX(assetEntityId, 201, 40);
    WaitFor(EntityInRadiusOfEntity(10000, assetEntityId, 3, 1));
    DeleteAssetfollowingSFX(assetEntityId, true);
});

// 【共通】小篝火_お試し地名表示 -- [Common] Small Bonfire_Trial place name display
$Event(9005912, Restart, function(eventFlagId, messageId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(EventFlag(eventFlagId));
    DisplaySubareaWelcomeMessage(messageId);
});

// 【共通】いんちきランダム配置 -- [Common] Bogus random placement
$Event(9005920, Restart, function(chrEntityId, chrEntityId2, chrEntityId3, chrEntityId4, chrEntityId5, chrEntityId6, chrEntityId7, chrEntityId8, chrEntityId9, chrEntityId10) {
    if (!EventFlag(9800)) {
        DisableCharacter(chrEntityId);
        DisableCharacterCollision(chrEntityId);
    } else {
        EnableCharacter(chrEntityId);
        EnableCharacterCollision(chrEntityId);
    }
    if (!EventFlag(9801)) {
        DisableCharacter(chrEntityId2);
        DisableCharacterCollision(chrEntityId2);
    } else {
        EnableCharacter(chrEntityId2);
        EnableCharacterCollision(chrEntityId2);
    }
    if (!EventFlag(9802)) {
        DisableCharacter(chrEntityId3);
        DisableCharacterCollision(chrEntityId3);
    } else {
        EnableCharacter(chrEntityId3);
        EnableCharacterCollision(chrEntityId3);
    }
    if (!EventFlag(9803)) {
        DisableCharacter(chrEntityId4);
        DisableCharacterCollision(chrEntityId4);
    } else {
        EnableCharacter(chrEntityId4);
        EnableCharacterCollision(chrEntityId4);
    }
    if (!EventFlag(9804)) {
        DisableCharacter(chrEntityId5);
        DisableCharacterCollision(chrEntityId5);
    } else {
        EnableCharacter(chrEntityId5);
        EnableCharacterCollision(chrEntityId5);
    }
    if (!EventFlag(9805)) {
        DisableCharacter(chrEntityId6);
        DisableCharacterCollision(chrEntityId6);
    } else {
        EnableCharacter(chrEntityId6);
        EnableCharacterCollision(chrEntityId6);
    }
    if (!EventFlag(9806)) {
        DisableCharacter(chrEntityId7);
        DisableCharacterCollision(chrEntityId7);
    } else {
        EnableCharacter(chrEntityId7);
        EnableCharacterCollision(chrEntityId7);
    }
    if (!EventFlag(9807)) {
        DisableCharacter(chrEntityId8);
        DisableCharacterCollision(chrEntityId8);
    } else {
        EnableCharacter(chrEntityId8);
        EnableCharacterCollision(chrEntityId8);
    }
    if (!EventFlag(9808)) {
        DisableCharacter(chrEntityId9);
        DisableCharacterCollision(chrEntityId9);
    } else {
        EnableCharacter(chrEntityId9);
        EnableCharacterCollision(chrEntityId9);
    }
    if (!EventFlag(9809)) {
        DisableCharacter(chrEntityId10);
        DisableCharacterCollision(chrEntityId10);
    } else {
        EnableCharacter(chrEntityId10);
        EnableCharacterCollision(chrEntityId10);
    }
});

// 【共通】宝箱_視認性 -- [Common] Treasure Chest_Visibility
$Event(90005920, Restart, function(eventFlagId, assetEntityId, objactEventFlag) {
    EndIf(EventFlag(eventFlagId));
    CreateAssetfollowingSFX(assetEntityId, 100, 6150);
    WaitFor(ObjActEventFlag(objactEventFlag));
    SetEventFlagID(eventFlagId, ON);
    WaitFixedTimeSeconds(0.3);
    DeleteAssetfollowingSFX(assetEntityId, true);
});

// 【共通】特殊待機文字列確認用テスト -- [Common] Special standby character string confirmation test
$Event(9005990, Restart, function(timeSeconds) {
    WaitFixedTimeSeconds(timeSeconds);
});

// 【共通】闘技場_メイン処理 -- [Common] Arena_Main process
$Event(98005100, Restart, function(matchType, eventFlagId, messageId, messageId2) {
    DisableAreaWelcomeMessage();
    WaitFor(PlayerIsInOwnWorld() && ArenaMatchReady());
    WaitFixedTimeSeconds(5);
    DisplayBlinkingMessageWithPriority(messageId, 1, true);
    SetEventFlagID(280, ON);
    DisplayBanner(TextBannerType.Commence);
    if (PlayerIsInOwnWorld()) {
        WaitUntilArenaHalfTime(matchType, false);
    }
    WaitFor(PlayerIsInOwnWorld() && !EventFlag(eventFlagId));
    DisplayBlinkingMessageWithPriority(messageId2, 2, true);
    SetSpEffect(10000, 1160);
    if (PlayerIsInOwnWorld()) {
        WaitUntilArenaHalfTime(matchType, true);
    }
    WaitFor(PlayerIsInOwnWorld());
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
});

// 【共通】闘技場_サブ処理_決闘 -- [Common] Arena_Sub-processing_Duel
$Event(98005110, Restart, function(eventFlagId) {
    WaitFor(ArenaSoloScore() == 1 || EventFlag(eventFlagId));
    EndIf(EventFlag(eventFlagId));
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId, ON);
    }
});

// 【共通】闘技場_結果表示処理 -- [Common] Arena_Result display processing
$Event(98005120, Restart, function(eventFlagId) {
    DisableNetworkSync();
    WaitFor(EventFlag(eventFlagId));
    EnableCharacterInvincibility(10000);
    SetEventFlagID(280, OFF);
    DisplayBlinkingMessageWithPriority(88040, 0, true);
    WaitFixedTimeFrames(1);
    WaitFixedTimeSeconds(5);
    Unknown200383(0);
    if (!HasArenaMatchType(ArenaMatchType.OneVersusOne, false)) {
        GotoIf(L9, HasArenaMatchType(ArenaMatchType.OneVersusOne, false));
        GotoIf(L9, HasArenaMatchType(ArenaMatchType.TwoVersusTwo, false));
        GotoIf(L9, HasArenaMatchType(ArenaMatchType.ThreeVersusThree, false));
        GotoIf(L9, HasArenaMatchType(ArenaMatchType.TwoVersusTwo, true));
        GotoIf(L9, HasArenaMatchType(ArenaMatchType.ThreeVersusThree, true));
        online |= ArenaSoloResults(ArenaResult.Win);
        online2 |= ArenaSoloResults(ArenaResult.Draw);
        GotoIf(L0, online);
        GotoIf(L1, online2);
    } else {
L9:
        online |= ArenaTeamResults(ArenaResult.Win);
        online2 |= ArenaTeamResults(ArenaResult.Draw);
        GotoIf(L0, online);
        GotoIf(L1, online2);
        Goto(L2);
L0:
        DisplayBanner(TextBannerType.Victory);
        SetSpEffect(10000, 1140);
        WaitFixedTimeSeconds(5);
        DisplayBlinkingMessageWithPriority(88050, 0, true);
        WaitFixedTimeSeconds(0.5);
        SendAllPhantomsHomeAndUpdateServerPvpStats(0);
        EndEvent();
L1:
        DisplayBanner(TextBannerType.Stalemate);
        SetSpEffect(10000, 1150);
        WaitFixedTimeSeconds(5);
        DisplayBlinkingMessageWithPriority(88051, 0, true);
        WaitFixedTimeSeconds(0.5);
        SendAllPhantomsHomeAndUpdateServerPvpStats(0);
        EndEvent();
    }
L2:
    DisplayBanner(TextBannerType.Defeat);
    WaitFixedTimeSeconds(5);
    DisplayBlinkingMessageWithPriority(88052, 0, true);
    WaitFixedTimeSeconds(0.5);
    SendAllPhantomsHomeAndUpdateServerPvpStats(0);
    EndEvent();
});

// 【共通】闘技場_結果表示処理_決闘 -- [Common] Arena_Result display processing_Duel
$Event(98005121, Restart, function(eventFlagId) {
    DisableNetworkSync();
    WaitFor(EventFlag(eventFlagId));
    EnableCharacterInvincibility(10000);
    SetEventFlagID(280, OFF);
    if (ArenaSoloResults(ArenaResult.Draw)) {
        DisplayBlinkingMessageWithPriority(88040, 0, true);
        WaitFixedTimeSeconds(3.5);
    }
    WaitFixedTimeSeconds(1);
    Unknown200383(0);
    WaitFixedTimeFrames(1);
    online = ArenaSoloResults(ArenaResult.Win);
    online2 = ArenaSoloResults(ArenaResult.Draw);
    GotoIf(L0, online);
    GotoIf(L1, online2);
    Goto(L2);
L0:
    DisplayBanner(TextBannerType.Victory);
    SetSpEffect(10000, 1140);
    WaitFixedTimeSeconds(5);
    DisplayBlinkingMessageWithPriority(88050, 0, true);
    WaitFixedTimeSeconds(0.5);
    SendAllPhantomsHomeAndUpdateServerPvpStats(0);
    EndEvent();
L1:
    DisplayBanner(TextBannerType.Stalemate);
    WaitFixedTimeSeconds(5);
    DisplayBlinkingMessageWithPriority(88051, 0, true);
    WaitFixedTimeSeconds(0.5);
    SendAllPhantomsHomeAndUpdateServerPvpStats(0);
    EndEvent();
L2:
    DisplayBanner(TextBannerType.Defeat);
    WaitFixedTimeSeconds(5);
    DisplayBlinkingMessageWithPriority(88052, 0, true);
    WaitFixedTimeSeconds(0.5);
    SendAllPhantomsHomeAndUpdateServerPvpStats(0);
    EndEvent();
});


