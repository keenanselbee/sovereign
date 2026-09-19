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
    RegisterBonfire(76305, 1041521951, 0, 0, 0, 5);
    $InitializeEvent(0, 1041522320, 1041520800, 904510600, 28);
    $InitializeCommonEvent(0, 90005860, 1041520800, 0, 1041520800, 1, 30300, 0);
    $InitializeEvent(0, 1041522270, 1041520270, 1041522270, 1041522271);
    $InitializeEvent(1, 1041522270, 1041520270, 1041522270, 1041522271);
    $InitializeEvent(2, 1041522270, 1041520280, 1041522280, 1041522281);
    $InitializeEvent(3, 1041522270, 1041520280, 1041522280, 1041522281);
    $InitializeCommonEvent(0, 90005633, 580320, 580020, 1041520300, 30015, 20015, 1041521300, 1041521310);
    $InitializeCommonEvent(0, 90005631, 1041521400, 61030);
    // SACRED
    $InitializeEvent(0, 5750215);
    // SACRED       
});

// プリコンストラクタ -- preconstructor
$Event(50, Default, function() {
    $InitializeEvent(0, 1041522300, 1041520800);
});

// 雷地帯_弾丸イベント_XX -- Thunder Zone_Bullet Event_XX
$Event(1041522270, Restart, function(chrEntityId, areaEntityId, entityId) {
    DisableNetworkSync();
    CreateBulletOwner(chrEntityId);
    WaitFor(InArea(10000, areaEntityId));
    WaitRandomTimeSeconds(1, 10);
    if (EventFlag(50)) {
        ShootBullet(chrEntityId, entityId, 900, 802103000, 0, 0, 0);
    }
    if (EventFlag(51)) {
        ShootBullet(chrEntityId, entityId, 900, 802103010, 0, 0, 0);
    }
    if (EventFlag(52)) {
        ShootBullet(chrEntityId, entityId, 900, 802103020, 0, 0, 0);
    }
    if (EventFlag(53)) {
        ShootBullet(chrEntityId, entityId, 900, 802103030, 0, 0, 0);
    }
    if (EventFlag(54)) {
        ShootBullet(chrEntityId, entityId, 900, 802103040, 0, 0, 0);
    }
    if (EventFlag(55)) {
        ShootBullet(chrEntityId, entityId, 900, 802103050, 0, 0, 0);
    }
    if (EventFlag(56)) {
        ShootBullet(chrEntityId, entityId, 900, 802103060, 0, 0, 0);
    }
    if (EventFlag(57)) {
        ShootBullet(chrEntityId, entityId, 900, 802103070, 0, 0, 0);
    }
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// 守護者の末裔_出現演出 -- Descendants of the Guardian_Appearance
$Event(1041522300, Restart, function(chrEntityId) {
    if (!EventFlag(1041520800)) {
        if (!EventFlag(1037510800)) {
            if (!EventFlag(1041522810)) {
                DisableCharacter(chrEntityId);
                DisableCharacterCollision(chrEntityId);
                WaitFor(CharacterType(10000, TargetType.Alive) && InArea(10000, 1041522800));
                SetEventFlagID(1041520820, ON);
                SetEventFlagID(1041522810, ON);
                EnableCharacterFadeOnEnable(chrEntityId);
                EnableCharacter(chrEntityId);
                EnableCharacterCollision(chrEntityId);
                ForceAnimationPlayback(chrEntityId, 20019, false, false, false);
            }
L1:
            EndEvent();
        }
    }
L0:
    DisableCharacter(chrEntityId);
    DisableCharacterCollision(chrEntityId);
    EndEvent();
});

// 高山崖上守護者の末裔_フィールドボスHPゲージ -- Descendant of the Alpine Cliff Guardian_Field Boss HP Gauge
$Event(1041522320, Default, function(chrEntityId, nameId, npcThreatLevel) {
    DisableNetworkSync();
    DisableCharacterHPBarDisplay(chrEntityId);
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
    if (EventFlag(1037510810)) {
        SetSpEffect(chrEntityId, 4401);
    }
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
    if (EventFlag(1037510810)) {
        SetSpEffect(chrEntityId, 4401);
    }
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

// SACRED Ancient Dragon Communion Message
$Event(5750215, Restart, function() {
    EndIf(EventFlag(1041520800));
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(CharacterDead(1041520800));
    WaitFixedTimeSeconds(2);
    if (EventFlag(1055420240)) {
        DisplayBlinkingMessage(1055421000);
    }
});
