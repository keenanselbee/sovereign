// ==EMEVD==
// @docs    er-common.emedf.json
// @compress    DCX_KRAK
// @game    Sekiro
// @string    "N:\\GR\\data\\Param\\event\\common_func.emevd\u0000N:\\GR\\data\\Param\\event\\common_macro.emevd\u0000\u0000\u0000\u0000\u0000\u0000"
// @linked    [0,82]
// @version    3.5
// ==/EMEVD==

// コンストラクタ -- constructor
$Event(0, Default, function() {
    RegisterBonfire(76310, 1043501950, 0, 0, 0, 5);
    $InitializeCommonEvent(0, 90005771, 1043500950, 1043502700);
    // SACRED
    $InitializeEvent(0, 1055420900, 1055420905, 1055420905, 1055420900, 1055420910, 1, 6100);
    $InitializeEvent(0, 1055420901, 1055420905, 1055420905, 1055420900, 1055420910, 1);
    $InitializeCommonEvent(0, 90005870, 1055420910, 903560600, 27);
    // SACRED
});

// SACRED GEQ's Grave (Transforming slime_defeat)
$Event(1055420900, Restart, function(eventFlagId, eventFlagId2, entityId, chrEntityId, value, itemLotId) {
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
    SetSpEffect(chrEntityId, 4305);
    WaitFixedTimeSeconds(3);
    DisableCharacter(chrEntityId);
    EndIf(!PlayerIsInOwnWorld());
    if (Signed(itemLotId) != 0) {
        AwardItemsIncludingClients(itemLotId);
    }
    SetNetworkconnectedEventFlagID(eventFlagId, ON);
});

// SACRED GEQ's Grave (Transformation slime_transformation)
$Event(1055420901, Restart, function(eventFlagId, eventFlagId2, chrEntityId, chrEntityId2, value) {
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
    WaitFixedTimeSeconds(0.8);
    WarpCharacterAndCopyFloor(chrEntityId2, TargetEntityType.Character, chrEntityId, 900, chrEntityId);
    WaitFixedTimeSeconds(0.5);
    SetSpEffect(chrEntityId, 4305);
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
    TriggerAISound(6410, 1055420900, TargetEntityType.Area);
    WaitFor(CharacterHPValue(1055420910) <= 0);
    if (PlayerIsInOwnWorld()) {
        SetNetworkconnectedEventFlagID(eventFlagId2, ON);
    }
});
