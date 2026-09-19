// ==EMEVD==
// @docs    er-common.emedf.json
// @compress    DCX_KRAK
// @game    Sekiro
// @string    "N:\\GR\\data\\Param\\event\\common_func.emevd\u0000N:\\GR\\data\\Param\\event\\common_macro.emevd\u0000\u0000\u0000\u0000\u0000\u0000"
// @linked    [0,82]
// @version    3.5
// ==/EMEVD==

$Event(0, Default, function() {
    $InitializeEvent(0, 2045442811, 2045440800, 30002, 20002, 2045440820, 15, 0, 0, 0, 0, 0);
    $InitializeCommonEvent(0, 90005870, 2045440800, 905860600, 22);
    $InitializeCommonEvent(0, 90005860, 2045440800, 0, 2045440800, 1, 30860, 0);
    $InitializeEvent(0, 2045442812);
    $InitializeCommonEvent(0, 90005200, 2045440200, 30001, 20001, 2045442200, 2, 0, 0, 0, 0);
    $InitializeCommonEvent(0, 90005200, 2045440201, 30001, 20001, 2045442200, 2, 0, 0, 0, 0);
    $InitializeCommonEvent(0, 90005200, 2045440202, 30001, 20001, 2045442200, 2, 0, 0, 0, 0);
    // SACRED
    $InitializeEvent(0, 5750220);
    // SACRED       
});

$Event(2045442810, Default, function(chrEntityId, nameId, npcThreatLevel) {
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
    EnableLockOnPoint(chrEntityId, 220);
    EnableLockOnPoint(chrEntityId, 224);
    EnableLockOnPoint(chrEntityId, 225);
    EnableLockOnPoint(chrEntityId, 226);
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
    EnableLockOnPoint(chrEntityId, 220);
    EnableLockOnPoint(chrEntityId, 224);
    EnableLockOnPoint(chrEntityId, 225);
    EnableLockOnPoint(chrEntityId, 226);
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

$Event(2045442811, Restart, function(chrEntityId, animationId, animationId2, eventFlagId, targetDistance, timeSeconds, value, value2, value3, value4) {
    EndIf(SpecialStandbyEndedFlag(chrEntityId));
    EndIf(EventFlag(eventFlagId));
    if (value != 0) {
        DisableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, false);
    }
    DisableLockOnPoint(chrEntityId, 220);
    DisableLockOnPoint(chrEntityId, 224);
    DisableLockOnPoint(chrEntityId, 225);
    DisableLockOnPoint(chrEntityId, 226);
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
            || CharacterAIState(chrEntityId, AIStateType.Combat)
            || sp
            || sp2
            || sp3
            || sp4
            || sp5);
    WaitFixedTimeSeconds(0.1);
    SetNetworkconnectedThisEventSlot(ON);
    SetSpecialStandbyEndedFlag(chrEntityId, ON);
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
    if (!(!CharacterHasSpEffect(chrEntityId, 5080) && !CharacterHasSpEffect(chrEntityId, 5450))) {
        WaitFixedTimeSeconds(timeSeconds);
        if (value != 0) {
            EnableCharacterGravity(chrEntityId);
            SetCharacterMaphit(chrEntityId, true);
        }
        ForceAnimationPlayback(chrEntityId, animationId2, true, false, false);
        EnableLockOnPoint(chrEntityId, 220);
        EnableLockOnPoint(chrEntityId, 224);
        EnableLockOnPoint(chrEntityId, 225);
        EnableLockOnPoint(chrEntityId, 226);
        EndEvent();
    }
L0:
    if (value != 0) {
        EnableCharacterGravity(chrEntityId);
        SetCharacterMaphit(chrEntityId, true);
    }
    EndEvent();
});

$Event(2045442812, Default, function() {
    EndIf(EventFlag(2045440820));
    SetSpEffect(2045440100, 9531);
    WaitForEventFlag(ON, TargetEventFlagType.EventFlag, 2045440820);
    SetSpEffect(2045440100, 9532);
});

// SACRED Dragon Communion Message
$Event(5750220, Restart, function() {
    EndIf(EventFlag(2045440800));
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(CharacterDead(2045440800));
    WaitFixedTimeSeconds(2);
    DisplayBlinkingMessage(30063);
});
