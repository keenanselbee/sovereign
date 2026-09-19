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
    if (PlayerIsInOwnWorld()) {
        $InitializeEvent(0, 18000020);
        $InitializeEvent(0, 18000021);
        $InitializeEvent(0, 18000022);
        $InitializeEvent(0, 18002023);
    }
L0:
    $InitializeEvent(0, 18000050);
    RegisterBonfire(18000000, 18001950, 0, 0, 0, 5);
    RegisterBonfire(18000001, 18001951, 0, 0, 0, 5);
    $InitializeEvent(0, 18002800);
    $InitializeEvent(0, 18002810);
    $InitializeEvent(0, 18000820);
    $InitializeCommonEvent(0, 90005646, 18000800, 18002190, 18002191, 18001190, 18002190, 18, 0, 0, 0);
    $InitializeEvent(0, 18002850);
    $InitializeEvent(0, 18002860);
    $InitializeEvent(0, 18000870);
    $InitializeEvent(0, 18002400);
    $InitializeEvent(0, 18002440, 18000600, 18001600, 18001601, 18002600, 2.33);
    $InitializeEvent(1, 18002440, 18000601, 18001602, 18001603, 18002601, 2.28);
    $InitializeEvent(2, 18002440, 18000602, 18001604, 18001605, 18002602, 2.28);
    $InitializeEvent(0, 18002450, 18000600, 18001600, 18002600);
    $InitializeEvent(1, 18002450, 18000601, 18001602, 18002601);
    $InitializeEvent(2, 18002450, 18000602, 18001604, 18002602);
    $InitializeEvent(0, 18002410);
    $InitializeEvent(0, 18002411, 18002431, 18003420, 18002421, 18003421, 0, 0);
    $InitializeEvent(1, 18002411, 18002432, 18003421, 18002422, 18003422, 0, 0);
    $InitializeEvent(2, 18002411, 18002433, 18003422, 18002423, 18003423, 0, 0);
    $InitializeEvent(3, 18002411, 18002434, 18003423, 18002424, 18003424, 0, 0);
    $InitializeEvent(4, 18002411, 18002435, 18003424, 18002425, 18003425, 18002426, 18003426);
    $InitializeCommonEvent(0, 90005680, 18000530, 18000531, 18000532, 18000533, 18001530);
    $InitializeCommonEvent(0, 900005610, 18001650, 100, 800, 0);
    $InitializeCommonEvent(0, 900005610, 18001651, 100, 800, 0);
    $InitializeCommonEvent(0, 90005501, 18000510, 18001510, 0, 18001510, 18001511, 18001512, 18000511);
    $InitializeCommonEvent(0, 90005501, 18000515, 18001515, 1, 18001515, 18001516, 18001517, 18000516);
    $InitializeEvent(0, 18002510);
    $InitializeCommonEvent(0, 90005511, 18000542, 18001542, 18003542, 227010, 0);
    $InitializeCommonEvent(0, 90005512, 18000542, 18002542, 18002543);
    $InitializeEvent(0, 18002580);
    $InitializeCommonEvent(0, 90005646, 18000800, 18002840, 18002841, 18001840, 18002840, 18, 0, 0, 0);
    $InitializeCommonEvent(0, 90005620, 18000570, 18001570, 18001571, 18001572, 18002570, 18002571, 18002572);
    $InitializeEvent(0, 18002569, 18000570, 18001573);
    $InitializeCommonEvent(0, 90005570, 60809, 9, 18001640, 0, 1, 0);
    $InitializeEvent(0, 18002270, 18000270);
    $InitializeEvent(0, 18002650, 18002650, 1010, 710010);
    $InitializeEvent(0, 18002640, 18002651, 1020, 710020, 9100, 69000);
    $InitializeEvent(1, 18002640, 18002656, 1070, 710070, 9112, 69120);
    $InitializeEvent(2, 18002640, 18002663, 1140, 710140, 9103, 69030);
    $InitializeCommonEvent(0, 90005261, 18000202, 18002202, 10, 0, 0);
    $InitializeEvent(3, 18002640, 18002665, 1160, 710160, 9104, 69040);
    $InitializeEvent(4, 18002640, 18002667, 1190, 710190, 9105, 69050);
    $InitializeEvent(5, 18002640, 18002670, 1200, 710200, 9129, 69290);
    $InitializeEvent(6, 18002640, 18002668, 1210, 710210, 9138, 69380);
    $InitializeEvent(7, 18002640, 18002659, 1100, 710100, 9140, 69400);
    $InitializeEvent(0, 18002651, 18002652, 1030, 710030);
    $InitializeEvent(1, 18002651, 18002653, 1040, 710040);
    $InitializeEvent(2, 18002651, 18002657, 1080, 710080);
    $InitializeEvent(3, 18002651, 18002658, 1090, 710090);
    $InitializeEvent(5, 18002651, 18002660, 1110, 710110);
    $InitializeEvent(7, 18002651, 18002664, 1150, 710150);
    $InitializeEvent(8, 18002651, 18002666, 1170, 710170);
    $InitializeEvent(0, 18002654, 18002654, 1050, 710050);
    $InitializeEvent(0, 18002655, 18002655, 1060, 18000655, 710060);
    $InitializeEvent(0, 18002662, 18002662, 1130, 18000662, 710130);
    $InitializeEvent(0, 18002663, 1180, 710180, 9106, 69060, 18000850);
    $InitializeEvent(0, 18002665, 710660, 1660, 9122, 69220);
    $InitializeEvent(0, 18002200, 18000200, 18002201, 18003200, 18002200);
    $InitializeEvent(0, 18002211, 18000211, 18002211);
    $InitializeEvent(1, 18002211, 18000220, 18000220);
    $InitializeEvent(0, 18002671, 710010);
    $InitializeEvent(1, 18002671, 710020);
    $InitializeEvent(2, 18002671, 710030);
    $InitializeEvent(3, 18002671, 710040);
    $InitializeEvent(4, 18002671, 710050);
    $InitializeEvent(5, 18002671, 18000655);
    $InitializeEvent(6, 18002671, 18000662);
    $InitializeEvent(7, 18002671, 710070);
    $InitializeEvent(8, 18002671, 710080);
    $InitializeEvent(9, 18002671, 710090);
    $InitializeEvent(10, 18002671, 710100);
    $InitializeEvent(11, 18002671, 710110);
    $InitializeEvent(12, 18002671, 710120);
    $InitializeEvent(13, 18002671, 710140);
    $InitializeEvent(14, 18002671, 710150);
    $InitializeEvent(15, 18002671, 710160);
    $InitializeEvent(16, 18002671, 710170);
    $InitializeEvent(17, 18002671, 710000);
    $InitializeEvent(18, 18002671, 710110);
    $InitializeEvent(19, 18002671, 710110);
    $InitializeEvent(20, 18002671, 710210);
    $InitializeEvent(21, 18002671, 710200);
    $InitializeEvent(22, 18002671, 710190);
    $InitializeEvent(0, 18002250, 18000850, 8041);
    $InitializeEvent(1, 18002250, 18000256, 8040);
    $InitializeEvent(0, 18002690);
    $InitializeCommonEvent(0, 90005706, 18000701, 30025, 0);
    // SACRED
    $InitializeEvent(0, 5750300);
    // SACRED   
});

// プリコンストラクタ -- preconstructor
$Event(50, Default, function() {
    SetCharacterBackreadState(18000701, true);
    $InitializeCommonEvent(0, 90005251, 18000201, 2, 0, -1);
    $InitializeCommonEvent(0, 90005250, 18000300, 18002300, 0, -1);
    $InitializeCommonEvent(0, 90005251, 18000313, 4, 0, -1);
    $InitializeCommonEvent(0, 90005251, 18000330, 8, 0, -1);
    $InitializeCommonEvent(0, 90005251, 18000342, 4, 0, 3000);
    $InitializeCommonEvent(0, 90005251, 18000343, 7, 0, -1);
    $InitializeCommonEvent(0, 90005251, 18000344, 5, 2, -1);
    $InitializeCommonEvent(0, 90005200, 18000350, 30002, 20002, 18002350, 0, 0, 0, 0, 0);
    $InitializeCommonEvent(0, 90005200, 18000351, 30002, 20002, 18002350, 3, 0, 0, 0, 0);
    $InitializeCommonEvent(0, 90005300, 18000350, 18000350, 18002000, 0, 0);
    $InitializeCommonEvent(0, 90005300, 18000351, 18000351, 18002010, 0, 0);
    $InitializeEvent(0, 18002520);
});

// チュートリアル開始 -- Start tutorial
$Event(18000020, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    if (!(ThisEventSlot() && !EventFlag(60000))) {
        EndIf(ThisEventSlot());
        WaitFor(EventFlag(10010020) && PlayerInMap(18, 0, 0, 0));
        SetEventFlagID(101, ON);
        SetPlayerRespawnPoint(18002020);
        SaveRequest();
        DisableCharacterImmortality(10000);
        BonfirelikeRecovery();
        Unknown200461(9999);
        SetSpEffect(10000, 4291);
        SetSpEffect(10000, 4790);
        EndIf(!EventFlag(2000));
        SetEventFlagID(9021, ON);
        PlayCutsceneToPlayer(60430000, CutscenePlayMode.SkippableWithFadeOutSkip, 10000);
        WaitFixedTimeRealFrames(1);
        SetCameraAngle(6.98, 106.96);
    }
L0:
    item = PlayerHasItem(ItemType.Goods, 201)
        || PlayerHasItem(ItemType.Goods, 203)
        || PlayerHasItem(ItemType.Goods, 205)
        || PlayerHasItem(ItemType.Goods, 207)
        || PlayerHasItem(ItemType.Goods, 209)
        || PlayerHasItem(ItemType.Goods, 211)
        || PlayerHasItem(ItemType.Goods, 213)
        || PlayerHasItem(ItemType.Goods, 215)
        || PlayerHasItem(ItemType.Goods, 217)
        || PlayerHasItem(ItemType.Goods, 219);
    item2 = PlayerHasItem(ItemType.Goods, 221)
        || PlayerHasItem(ItemType.Goods, 223)
        || PlayerHasItem(ItemType.Goods, 225)
        || PlayerHasItem(ItemType.Goods, 227)
        || PlayerHasItem(ItemType.Goods, 229)
        || PlayerHasItem(ItemType.Goods, 221)
        || PlayerHasItem(ItemType.Goods, 223)
        || PlayerHasItem(ItemType.Goods, 225)
        || PlayerHasItem(ItemType.Goods, 227)
        || PlayerHasItem(ItemType.Goods, 229);
    item3 = item;
    item4 = item2;
    if (!item3) {
        AwardItemsIncludingClients(2000);
        EndEvent();
    }
L10:
    SetEventFlagID(60000, ON);
});

// チュートリアル時間固定 -- Fixed tutorial time
$Event(18000021, Restart, function() {
    DisableNetworkSync();
    EndIf(EventFlag(102));
    EndIf(EventFlag(2002));
    SetCurrentTime(10, 30, 0, false, false, false, 0, 0, 0);
    FreezeTime(true);
    WaitFor(PlayerIsInOwnWorld() && EventFlag(1042368540));
    FreezeTime(false);
    SetEventFlagID(71801, ON);
    SetThisEventSlot(ON);
    SetEventFlagID(102, ON);
    ChangeWeather(Weather.Default, 3600, false);
});

// チュートリアル時間固定_保険 -- Tutorial time fixed_insurance
$Event(18000022, Restart, function() {
    EndIf(EventFlag(18000021));
    EndIf(EventFlag(102));
    EndIf(EventFlag(2002));
    WaitFor(InArea(10000, 18002022));
    SetCurrentTime(10, 30, 0, false, false, false, 0, 0, 0);
});

// チュートリアル案内 -- Tutorial guide
$Event(18002023, Restart, function() {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(710820));
    WaitFor(
        PlayerIsInOwnWorld()
            && InArea(10000, 18002680)
            && !(HasMultiplayerState(MultiplayerState.Multiplayer)
                || HasMultiplayerState(MultiplayerState.MultiplayerPending))
            && !CharacterHasSpEffect(10000, 9640));
    SetEventFlagID(710820, ON);
});

// チュートリアルPlayGo対応 -- Tutorial PlayGo compatible
$Event(18000050, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(2030));
    DisableObjAct(18001542, -1);
    flag = EventFlag(2030);
    act = ActionButtonInArea(7200, 18001542);
    WaitFor(flag || act);
    if (act.Passed) {
        DisplayFullScreenMessage(2000);
        WaitFixedTimeSeconds(1);
        RestartIf(!EventFlag(2030));
    }
L0:
    EnableObjAct(18001542, -1);
});

// チュートリアル王軍兵士位置移動 -- Tutorial royal army soldier position movement
$Event(18002200, Restart, function(chrEntityId, areaEntityId, patrolInformationEntityId, eventFlagId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(InArea(10000, areaEntityId));
    ClearCharactersAITarget(chrEntityId);
    ChangeCharacterPatrolBehavior(chrEntityId, patrolInformationEntityId);
    SetEventFlagID(eventFlagId, ON);
});

// チュートリアル貴人攻撃 -- Tutorial noble attack
$Event(18002211, Restart, function(entityId, eventFlagId) {
    EndIf(EventFlag(eventFlagId));
    WaitFor(EntityInRadiusOfEntity(10000, entityId, 3, 1));
    ForceAnimationPlayback(entityId, 3001, false, true, false);
    SetEventFlagID(eventFlagId, ON);
});

// チュートリアル特殊効果 -- tutorial special effects
$Event(18002250, Restart, function(chrEntityId, spEffectId) {
    SetSpEffect(chrEntityId, spEffectId);
});

// 話す死体_アニメ再生 -- Talking corpse_anime playback
$Event(18002270, Restart, function(entityId) {
    ForceAnimationPlayback(entityId, 930025, false, false, false);
    EndEvent();
});

// チャリオット初期設定 -- Chariot initial settings
$Event(18002400, Restart, function() {
    if (EventFlag(18000400)) {
        DisableCharacter(18000400);
        DisableCharacterCollision(18000400);
        DisableCharacterAI(18000400);
        EndEvent();
    }
    WaitFor(PlayerInMap(18, 0, 0, 0));
    DisableCharacterInvincibility(18000400);
    EnableCharacterImmortality(18000400);
    DisableLockOnPoint(18000400, 220);
    DisableCharacterHPBarDisplay(18000400);
    SetSpEffect(18000400, 5000);
    SetNetworkUpdateRate(18000400, true, CharacterUpdateFrequency.AlwaysUpdate);
    EnableCharacterDefaultBackread(18000400);
    if (PlayerIsInOwnWorld()) {
        SetNetworkUpdateAuthority(18000400, AuthorityLevel.Forced);
    }
});

// チャリオット巡回ルート指定_初回起動 -- Chariot patrol route specification_first launch
$Event(18002410, Restart, function() {
    EndIf(EventFlag(18000400));
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        CountEventFlags(TargetEventFlagType.EventFlag, 18002411, 18002411) >= 0
            && InArea(10000, 18002400));
    ChangeCharacterPatrolBehavior(18000400, 18003420);
    WaitFixedTimeFrames(1);
});

// チャリオット巡回ルート指定_XX -- Chariot patrol route specification_XX
$Event(18002411, Restart, function(areaEntityId, patrolInformationEntityId, areaEntityId2, patrolInformationEntityId2, areaEntityId3, patrolInformationEntityId3) {
    EndIf(EventFlag(18000400));
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(InArea(18000400, areaEntityId));
    GotoIf(L1, InArea(10000, areaEntityId2));
    GotoIf(S0, 0 == areaEntityId3);
    GotoIf(L2, InArea(10000, areaEntityId3));
S0:
    ChangeCharacterPatrolBehavior(18000400, patrolInformationEntityId);
    Goto(L20);
L1:
    ChangeCharacterPatrolBehavior(18000400, patrolInformationEntityId2);
    Goto(L20);
L2:
    ChangeCharacterPatrolBehavior(18000400, patrolInformationEntityId3);
    Goto(L20);
L20:
    WaitFor(!InArea(18000400, areaEntityId));
    RestartEvent();
});

// 吊り下げ火炎樽_XX -- Hanging flame barrel_XX
$Event(18002440, Restart, function(eventFlagId, assetEntityId, assetEntityId2, eventFlagId2, timeSeconds) {
    if (EventFlag(eventFlagId2)) {
        DisableAsset(assetEntityId);
        DeleteAssetEvent(eventFlagId);
        DisableAsset(assetEntityId2);
        EndEvent();
    }
    EnableAsset(assetEntityId);
    WaitFor(AssetDestroyed(assetEntityId2));
    RequestAssetDestruction(assetEntityId, 0);
    DeleteAssetEvent(eventFlagId);
    CreateDamagingAsset(eventFlagId, assetEntityId, 200, 200500, DamageTargetType.Character, 2, 0, 0.1);
    SetEventFlagID(eventFlagId2, ON);
    WaitFixedTimeSeconds(timeSeconds);
    if (!CharacterHasSpEffect(18000400, 19300)) {
        if (EventFlag(50)) {
            ShootBullet(18000600, assetEntityId, 200, 803301800, 0, 0, 0);
        }
        if (EventFlag(51)) {
            ShootBullet(18000600, assetEntityId, 200, 803301810, 0, 0, 0);
        }
        if (EventFlag(52)) {
            ShootBullet(18000600, assetEntityId, 200, 803301820, 0, 0, 0);
        }
        if (EventFlag(53)) {
            ShootBullet(18000600, assetEntityId, 200, 803301830, 0, 0, 0);
        }
        if (EventFlag(54)) {
            ShootBullet(18000600, assetEntityId, 200, 803301840, 0, 0, 0);
        }
        if (EventFlag(55)) {
            ShootBullet(18000600, assetEntityId, 200, 803301850, 0, 0, 0);
        }
        if (EventFlag(56)) {
            ShootBullet(18000600, assetEntityId, 200, 803301860, 0, 0, 0);
        }
        if (EventFlag(57)) {
            ShootBullet(18000600, assetEntityId, 200, 803301870, 0, 0, 0);
        }
        DisableAsset(assetEntityId);
        DeleteAssetEvent(eventFlagId);
    }
L0:
    NoOp();
});

// チャリオット吊り下げ火炎樽で破壊_XX -- Destroyed by Chariot hanging flame barrel_XX
$Event(18002450, Restart, function(eventFlagId, assetEntityId, eventFlagId2) {
    EndIf(EventFlag(18000400));
    WaitFor(CharacterHasSpEffect(18000400, 19300) && EventFlag(eventFlagId2));
    if (EventFlag(50)) {
        ShootBullet(18000600, assetEntityId, 200, 803301800, 0, 0, 0);
    }
    if (EventFlag(51)) {
        ShootBullet(18000600, assetEntityId, 200, 803301810, 0, 0, 0);
    }
    if (EventFlag(52)) {
        ShootBullet(18000600, assetEntityId, 200, 803301820, 0, 0, 0);
    }
    if (EventFlag(53)) {
        ShootBullet(18000600, assetEntityId, 200, 803301830, 0, 0, 0);
    }
    if (EventFlag(54)) {
        ShootBullet(18000600, assetEntityId, 200, 803301840, 0, 0, 0);
    }
    if (EventFlag(55)) {
        ShootBullet(18000600, assetEntityId, 200, 803301850, 0, 0, 0);
    }
    if (EventFlag(56)) {
        ShootBullet(18000600, assetEntityId, 200, 803301860, 0, 0, 0);
    }
    if (EventFlag(57)) {
        ShootBullet(18000600, assetEntityId, 200, 803301870, 0, 0, 0);
    }
    DisableAsset(assetEntityId);
    DeleteAssetEvent(eventFlagId);
    DisableCharacterImmortality(18000400);
    ForceCharacterDeath(18000400, true);
    ClearSpEffect(18000400, 19300);
    WaitFixedTimeSeconds(3);
    EndIf(EventFlag(18000400));
    if (PlayerIsInOwnWorld()) {
        AwardItemsIncludingClients(18000900);
    }
    SetEventFlagID(18000400, ON);
});

// エレベータイベント起動 -- Elevator event activation
$Event(18002510, Default, function() {
    $InitializeCommonEvent(0, 90005500, 18000510, 18001510, 0, 18001510, 18001511, 18003511, 18001512, 18003512, 18002511, 18002512, 18000511, 18002512, 0);
    $InitializeCommonEvent(0, 90005500, 18000515, 18001515, 1, 18001515, 18001516, 18003516, 18001517, 18003517, 18002516, 18002517, 18000516, 18002517, 0);
    $InitializeCommonEvent(0, 90005681, 18000530, 18000531, 18000532, 18000533, 18001530);
    if (EventFlag(57)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100770, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(56)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100760, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(55)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100750, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(54)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100740, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(53)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100730, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(52)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100720, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(51)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100710, 801100705, 102, 0, 0, 0);
    }
    if (EventFlag(50)) {
        $InitializeCommonEvent(0, 90005682, 18000532, 18001530, 18002530, 18000530, 801100700, 801100705, 102, 0, 0, 0);
    }
});

// エレベーター用初期フラグ設定 -- Initial flag setting for elevator
$Event(18002520, Default, function() {
    EndIf(ThisEventSlot());
    SetEventFlagID(18000530, ON);
});

// ガーゴイル像_封印扉_大 -- Gargoyle statue_Sealed door_Large
$Event(18002569, Default, function(eventFlagId, assetEntityId) {
    if (EventFlag(eventFlagId)) {
        DisableAsset(assetEntityId);
        EndEvent();
    }
L0:
    CreateAssetfollowingSFX(assetEntityId, 101, 806043);
    WaitFor(EventFlag(eventFlagId));
    DeleteAssetfollowingSFX(assetEntityId, true);
    PlaySE(assetEntityId, SoundType.SFX, 90011);
    WaitFixedTimeSeconds(0.5);
    DisableAsset(assetEntityId);
});

// 梯子登録 -- ladder registration
$Event(18002580, Restart, function() {
    RegisterLadder(18000580, 18000581, 18001580);
});

// チュートリアルメッセージ_イベント_XX -- Tutorial message_event_XX
$Event(18002640, Restart, function(areaEntityId, tutorialParamId, eventFlagId, itemId, eventFlagId2) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!EventFlag(eventFlagId) && InArea(10000, areaEntityId) && PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
    EndIf(EventFlag(eventFlagId2));
    DirectlyGivePlayerItem(ItemType.Goods, itemId, eventFlagId, 1);
    SetEventFlagID(eventFlagId2, ON);
});

// チュートリアルメッセージ_イベントアイテム -- Tutorial message_event item
$Event(18002650, Restart, function(areaEntityId, tutorialParamId, eventFlagId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && InArea(10000, areaEntityId)
            && HPRatio(10000) < 100
            && PlayerIsInOwnWorld());
    WaitFixedTimeSeconds(2);
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
});

// チュートリアルメッセージ_イベント_再読みアイテム無し_XX -- Tutorial message_Event_No reread items_XX
$Event(18002651, Restart, function(areaEntityId, tutorialParamId, eventFlagId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(!EventFlag(eventFlagId) && InArea(10000, areaEntityId) && PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
});

// チュートリアルメッセージ_イベント素性魔術師以外 -- Tutorial message_Events other than magicians
$Event(18002654, Restart, function(areaEntityId, tutorialParamId, eventFlagId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && InArea(10000, areaEntityId)
            && !PlayerHasItem(ItemType.Weapon, 33000000)
            && !PlayerHasItem(ItemType.Weapon, 33040000)
            && !PlayerHasItem(ItemType.Weapon, 33050000)
            && !PlayerHasItem(ItemType.Weapon, 33060000)
            && !PlayerHasItem(ItemType.Weapon, 33090000)
            && !PlayerHasItem(ItemType.Weapon, 33120000)
            && !PlayerHasItem(ItemType.Weapon, 33130000)
            && !PlayerHasItem(ItemType.Weapon, 33170000)
            && !PlayerHasItem(ItemType.Weapon, 33180000)
            && !PlayerHasItem(ItemType.Weapon, 33190000)
            && !PlayerHasItem(ItemType.Weapon, 33200000)
            && !PlayerHasItem(ItemType.Weapon, 33210000)
            && !PlayerHasItem(ItemType.Weapon, 33230000)
            && !PlayerHasItem(ItemType.Weapon, 33240000)
            && !PlayerHasItem(ItemType.Weapon, 33250000)
            && !PlayerHasItem(ItemType.Weapon, 33260000)
            && !PlayerHasItem(ItemType.Weapon, 33270000)
            && !PlayerHasItem(ItemType.Weapon, 33280000)
            && !PlayerHasItem(ItemType.Weapon, 34000000)
            && !PlayerHasItem(ItemType.Weapon, 34010000)
            && !PlayerHasItem(ItemType.Weapon, 34020000)
            && !PlayerHasItem(ItemType.Weapon, 34030000)
            && !PlayerHasItem(ItemType.Weapon, 34040000)
            && !PlayerHasItem(ItemType.Weapon, 34060000)
            && !PlayerHasItem(ItemType.Weapon, 34070000)
            && !PlayerHasItem(ItemType.Weapon, 34080000)
            && !PlayerHasItem(ItemType.Weapon, 34090000)
            && PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
});

// チュートリアルメッセージ_イベント素性魔術師 -- Tutorial message_Event Magician
$Event(18002655, Restart, function(areaEntityId, tutorialParamId, eventFlagId, eventFlagId2) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && InArea(10000, areaEntityId)
            && PlayerIsInOwnWorld()
            && (PlayerHasItem(ItemType.Weapon, 33000000)
                || PlayerHasItem(ItemType.Weapon, 33040000)
                || PlayerHasItem(ItemType.Weapon, 33050000)
                || PlayerHasItem(ItemType.Weapon, 33060000)
                || PlayerHasItem(ItemType.Weapon, 33090000)
                || PlayerHasItem(ItemType.Weapon, 33120000)
                || PlayerHasItem(ItemType.Weapon, 33130000)
                || PlayerHasItem(ItemType.Weapon, 33170000)
                || PlayerHasItem(ItemType.Weapon, 33180000)
                || PlayerHasItem(ItemType.Weapon, 33190000)
                || PlayerHasItem(ItemType.Weapon, 33200000)
                || PlayerHasItem(ItemType.Weapon, 33210000)
                || PlayerHasItem(ItemType.Weapon, 33230000)
                || PlayerHasItem(ItemType.Weapon, 33240000)
                || PlayerHasItem(ItemType.Weapon, 33250000)
                || PlayerHasItem(ItemType.Weapon, 33260000)
                || PlayerHasItem(ItemType.Weapon, 33270000)
                || PlayerHasItem(ItemType.Weapon, 33280000)
                || PlayerHasItem(ItemType.Weapon, 34000000)
                || PlayerHasItem(ItemType.Weapon, 34010000)
                || PlayerHasItem(ItemType.Weapon, 34020000)
                || PlayerHasItem(ItemType.Weapon, 34030000)
                || PlayerHasItem(ItemType.Weapon, 34040000)
                || PlayerHasItem(ItemType.Weapon, 34060000)
                || PlayerHasItem(ItemType.Weapon, 34070000)
                || PlayerHasItem(ItemType.Weapon, 34080000)
                || PlayerHasItem(ItemType.Weapon, 34090000)));
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
    SetEventFlagID(eventFlagId2, ON);
});

// チュートリアルメッセージ_イベント素性弓持ち -- Tutorial Message_Event Character Bow Holder
$Event(18002662, Restart, function(areaEntityId, tutorialParamId, eventFlagId, eventFlagId2) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && InArea(10000, areaEntityId)
            && PlayerIsInOwnWorld()
            && (PlayerHasItem(ItemType.Weapon, 40000000)
                || PlayerHasItem(ItemType.Weapon, 40010000)
                || PlayerHasItem(ItemType.Weapon, 40020000)
                || PlayerHasItem(ItemType.Weapon, 40030000)
                || PlayerHasItem(ItemType.Weapon, 40050000)
                || PlayerHasItem(ItemType.Weapon, 41000000)
                || PlayerHasItem(ItemType.Weapon, 41010000)
                || PlayerHasItem(ItemType.Weapon, 41020000)
                || PlayerHasItem(ItemType.Weapon, 41030000)
                || PlayerHasItem(ItemType.Weapon, 41040000)
                || PlayerHasItem(ItemType.Weapon, 41060000)
                || PlayerHasItem(ItemType.Weapon, 41070000)
                || PlayerHasItem(ItemType.Weapon, 42000000)
                || PlayerHasItem(ItemType.Weapon, 42000000)
                || PlayerHasItem(ItemType.Weapon, 42030000)
                || PlayerHasItem(ItemType.Weapon, 42040000)
                || PlayerHasItem(ItemType.Weapon, 43000000)
                || PlayerHasItem(ItemType.Weapon, 43020000)
                || PlayerHasItem(ItemType.Weapon, 43030000)
                || PlayerHasItem(ItemType.Weapon, 43050000)
                || PlayerHasItem(ItemType.Weapon, 43060000)
                || PlayerHasItem(ItemType.Weapon, 43080000)
                || PlayerHasItem(ItemType.Weapon, 43100000)
                || PlayerHasItem(ItemType.Weapon, 43110000)));
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
    SetEventFlagID(eventFlagId2, ON);
});

// チュートリアルメッセージ_イベントガードカウンター -- Tutorial message_Event guard counter
$Event(18002663, Restart, function(tutorialParamId, eventFlagId, itemId, eventFlagId2, entityId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(
        !EventFlag(eventFlagId)
            && EntityInRadiusOfEntity(entityId, 10000, 10, 1)
            && PlayerIsInOwnWorld());
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
    EndIf(HasMultiplayerState(MultiplayerState.Multiplayer));
    EndIf(EventFlag(eventFlagId2));
    DirectlyGivePlayerItem(ItemType.Goods, itemId, eventFlagId, 1);
    SetEventFlagID(eventFlagId2, ON);
});

// チュートリアルメッセージ_マルチプレイ協力 -- Tutorial message_Multiplayer cooperation
$Event(18002665, Restart, function(eventFlagId, tutorialParamId, itemId, eventFlagId2) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(eventFlagId));
    WaitFor(
        PlayerIsInOwnWorld()
            && EventFlag(eventFlagId)
            && !(HasMultiplayerState(MultiplayerState.Multiplayer)
                || HasMultiplayerState(MultiplayerState.MultiplayerPending)));
    SetEventFlagID(eventFlagId, ON);
    ShowTutorialPopup(tutorialParamId, true, true);
    EndIf(EventFlag(eventFlagId2));
    DirectlyGivePlayerItem(ItemType.Goods, itemId, eventFlagId, 1);
    SetEventFlagID(eventFlagId2, ON);
});

// チュートリアルメッセージ_リセット_XX -- Tutorial message_Reset_XX
$Event(18002671, Restart, function(eventFlagId) {
    DisableNetworkSync();
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(InArea(10000, 18002671) || !PlayerInMap(18, 0, 0, 0));
    SetEventFlagID(eventFlagId, OFF);
});

// ジェスチャーアイテム解禁 -- Gesture items unlocked
$Event(18002690, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(18007090));
    WaitFor(EventFlag(18007090));
    AwardGesture(9);
});

// ボス撃破 -- Defeat the boss
$Event(18002800, Restart, function() {
    EndIf(EventFlag(18000800));
    WaitFor(CharacterHPValue(18000800) <= 0);
    WaitFixedTimeSeconds(4);
    PlaySE(18000800, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(18000800));
    HandleBossDefeatAndDisplayBanner(18000800, TextBannerType.EnemyFelled);
    SetEventFlagID(18000800, ON);
    SetEventFlagID(9128, ON);
    if (PlayerIsInOwnWorld()) {
        SetEventFlagID(61128, ON);
    }
});

// ボス出現 -- Boss appears
$Event(18002810, Restart, function() {
    if (EventFlag(18000800)) {
        DisableCharacter(18000800);
        DisableCharacterCollision(18000800);
        ForceCharacterDeath(18000800, false);
        EndEvent();
    }
L0:
    DisableCharacterAI(18000800);
    WaitFor(EventFlag(18002805) && InArea(10000, 18002800));
L2:
    EnableCharacterAI(18000800);
    SetNetworkUpdateRate(18000800, true, CharacterUpdateFrequency.AlwaysUpdate);
    DisplayBossHealthBar(Enabled, 18000800, 0, 904640000);
});

// ボス共通イベント起動 -- Boss common event activation
$Event(18000820, Restart, function() {
    $InitializeCommonEvent(0, 9005800, 18000800, 18001800, 18002800, 18002805, 18005800, 10000, 0, 0);
    $InitializeCommonEvent(0, 9005801, 18000800, 18001800, 18002800, 18002805, 18002806, 10000);
    $InitializeCommonEvent(0, 9005811, 18000800, 18001800, 3, 0);
    $InitializeCommonEvent(0, 9005822, 18000800, 920600, 18002805, 18002806, 0, 18002802, 0, 0);
});

// SACRED Rick, Soldier of God (Boss defeat_tutorial)
$Event(18002850, Restart, function() {
    EndIf(EventFlag(18000850));
    WaitFor(CharacterHPValue(18000850) <= 0);
    WaitFixedTimeSeconds(4);
    PlaySE(18000850, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(18000850));
    HandleBossDefeatAndDisplayBanner(18000850, TextBannerType.LegendFelled);
});

// ボス出現_チュートリアル -- Boss appearance_tutorial
$Event(18002860, Restart, function() {
    if (EventFlag(18000850)) {
        DisableCharacter(18000850);
        DisableCharacterCollision(18000850);
        ForceCharacterDeath(18000850, false);
        EndEvent();
    }
L0:
    DisableCharacterAI(18000850);
    WaitFor(EventFlag(18002855) && InArea(10000, 18002850));
L2:
    EnableCharacterAI(18000850);
    SetNetworkUpdateRate(18000850, true, CharacterUpdateFrequency.AlwaysUpdate);
    DisplayBossHealthBar(Enabled, 18000850, 0, 904311000);
});

// ボス共通イベント起動_チュートリアル -- Boss common event activation_tutorial
$Event(18000870, Restart, function() {
    $InitializeCommonEvent(0, 9005800, 18000850, 18001850, 18002850, 18002855, 18005850, 10000, 0, 0);
    $InitializeCommonEvent(0, 9005801, 18000850, 18001850, 18002850, 18002855, 18002856, 10000);
    $InitializeCommonEvent(0, 9005811, 18000850, 18001850, 3, 0);
    $InitializeCommonEvent(0, 9005811, 18000850, 18001851, 4, 0);
    $InitializeCommonEvent(0, 9005822, 18000850, 931000, 18002855, 18002856, 0, 18002852, 0, 0);
});

// SACRED Hadeon reward reconciliation. The item lot owns collection flag 1055420916.
$Event(5750290, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    EndIf(EventFlag(1055420916));
    if (!EventFlag(1055420915)) {
        WaitFor(EventFlag(1055420915));
        WaitFixedTimeSeconds(8);
    }
    WaitFor(!CharacterDead(10000));
    EndIf(EventFlag(1055420916));
    AwardItemLot(6050);
    EndEvent();
});

// SACRED crystal: reveal after Hadeon, unlock Nemesis hardcore once per journey.
$Event(5750291, Restart, function() {
    if (!EventFlag(1055420915)) {
        DisableAsset(18002346);
        WaitFor(EventFlag(1055420915));
    }
    if (EventFlag(1055420918)) {
        DisableAsset(18002346);
        EndEvent();
    }
    EnableAsset(18002346);
    if (PlayerIsInOwnWorld()) {
        WaitFor(AssetDestroyed(18002346));
        SetEventFlagID(1055420918, ON);
    } else {
        WaitFor(EventFlag(1055420918));
    }
    DisableAsset(18002346);
    EndEvent();
});

// SACRED Nemesis Shrine Startup
$Event(5750300, Restart, function() {
    // Journey-persistent flags reset naturally in NG+, not on map load.
    $InitializeEvent(0, 5750290);
    $InitializeEvent(0, 5750291);
    if (PlayerIsInOwnWorld()) {
        $InitializeCommonEvent(0, 90005300, 1055420915, 18002354, 0, 0, 0);
    }
    DisableAsset(18000352);
    DisableAsset(18000353);
    DisableAsset(18000354);
    DisableAsset(18000355);
    DisableAsset(18000356);
    DisableAsset(18000357);
    DisableAsset(18000358);
    $InitializeEvent(0, 5750309);
    if (EventFlag(1055420915)) {
        DisableCharacter(18002354);
        DisableCharacterCollision(18002354);
        ForceCharacterDeath(18002354, false);
        DisplayBossHealthBar(Disabled, 18002354, 0, 999900100);
        SetBossBGM(472000, BossBGMState.Stop1);
        DisableAsset(18002347);
        DeleteAssetfollowingSFX(18002347, true);
        DisableAsset(18002379);
        DeleteAssetfollowingSFX(18002379, true);
    } else {
        $InitializeEvent(0, 5750302);
        EnableAsset(18002347);
        EnableAsset(18002379);
        DeleteAssetfollowingSFX(18002347, true);
        CreateAssetfollowingSFX(18002347, 101, 7505236);
        DeleteAssetfollowingSFX(18002379, true);
        CreateAssetfollowingSFX(18002379, 101, 7505236);
    }
    $InitializeEvent(0, 5750320);
    $InitializeEvent(0, 5750321);
    $InitializeEvent(0, 5750322);
    $InitializeEvent(0, 5750323);
    $InitializeEvent(0, 5750324);
    $InitializeEvent(0, 5750325);
    $InitializeEvent(0, 5750326);
    $InitializeEvent(0, 5750327);
    $InitializeEvent(0, 5750328);
    $InitializeEvent(0, 5750329);
    $InitializeEvent(0, 5750330);
    $InitializeEvent(0, 5750331);
    EndEvent();
});

// SACRED Crucible Lord Hadeon 1
$Event(5750302, Restart, function() {
    EndIf(EventFlag(1055420915));
    DisableCharacter(18002354);
    WaitFor(EventFlag(1055420915) || (InArea(10000, 18000359) && !InArea(10000, 18002367)));
    EndIf(EventFlag(1055420915));
    SetBossBGM(472000, BossBGMState.Start);
    WaitFixedTimeSeconds(5);
    PlaySE(10000, SoundType.SFX, 440621);
    WaitFixedTimeSeconds(0.2);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 7505235);
    WaitFixedTimeSeconds(1);
    PlaySE(10000, SoundType.SFX, 440621);
    WaitFixedTimeSeconds(0.2);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 7505235);
    WaitFixedTimeSeconds(1);
    PlaySE(10000, SoundType.SFX, 440621);
    WaitFixedTimeSeconds(0.2);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 7505235);
    WaitFixedTimeSeconds(1);
    PlaySE(10000, SoundType.SFX, 440621);
    WaitFixedTimeSeconds(0.2);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 7505235);
    WaitFixedTimeSeconds(1.5);
    PlaySE(10000, SoundType.SFX, 6800);
    PlaySE(10000, SoundType.SFX, 440470);
    PlaySE(10000, SoundType.SFX, 440481);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440481);
    SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440621);
    EnableCharacter(18002354);
    $InitializeEvent(0, 5750303);
    $InitializeEvent(0, 5750304);
    $InitializeEvent(0, 5750305);
    EndEvent();
});

// SACRED Crucible Lord Hadeon 2
$Event(5750303, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(CharacterAIState(18002354, AIStateType.Combat) && !InArea(10000, 18002367) && !InArea(10000, 18000361) 
    && !InArea(10000, 18000362) && !InArea(10000, 18002348) && !InArea(10000, 18002349) && !InArea(10000, 18002375));
    DisplayBossHealthBar(Enabled, 18002354, 0, 999900100);
    SetBossBGM(472000, BossBGMState.Start);
    WaitFor(CharacterHPValue(18002354) <= 0 || !CharacterAIState(18002354, AIStateType.Combat) || InArea(10000, 18002367));
    if (CharacterHPValue(18002354) > 0 && (!CharacterAIState(18002354, AIStateType.Combat) || InArea(10000, 18002367))) {
        WaitFixedTimeSeconds(6);
        SpawnOneshotSFX(TargetEntityType.Character, 18002354, 220, 440621);
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002366, -1, 18002366);
        PlaySE(10000, SoundType.SFX, 6800);
        PlaySE(10000, SoundType.SFX, 440470);
        PlaySE(10000, SoundType.SFX, 440481);
        SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440481);
        SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440621);
        RequestCharacterAnimationReset(18002354, 0);
        DisplayBossHealthBar(Disabled, 18002354, 0, 999900100);
        SetBossBGM(472000, BossBGMState.Stop1);
        $InitializeEvent(0, 5750302);
        RestartEvent();
    }
    WaitFixedTimeSeconds(4);
    DisplayBossHealthBar(Disabled, 18002354, 0, 999900100);
    SetBossBGM(472000, BossBGMState.Stop1);
    PlaySE(18002354, SoundType.SFX, 888880000);
    WaitFor(CharacterDead(18002354));
    HandleBossDefeatAndDisplayBanner(18002354, TextBannerType.GreatEnemyFelled);
    WaitFixedTimeSeconds(4);
    DisableAsset(18002347);
    DeleteAssetfollowingSFX(18002347, true);
    DisableAsset(18002379);
    DeleteAssetfollowingSFX(18002379, true);
    EndEvent();
});

// SACRED Crucible Lord Hadeon 3
$Event(5750304, Restart, function() {
    EndIf(EventFlag(1055420915));
    WaitFor(EventFlag(1055420915) || InArea(18002354, 18002367) || InArea(18002354, 18002349));
    EndIf(EventFlag(1055420915));
    WaitFixedTimeSeconds(0.1);
    if (InArea(18002354, 18002349) && !InArea(10000, 18002348) && !InArea(10000, 18002349)) {
        SpawnOneshotSFX(TargetEntityType.Character, 18002354, 220, 440621);
        PlaySE(10000, SoundType.SFX, 6800);
        PlaySE(10000, SoundType.SFX, 440470);
        PlaySE(10000, SoundType.SFX, 440481);
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002374, -1, 18002374);
        SpawnOneshotSFX(TargetEntityType.Area, 18002374, -1, 440481);
        RequestCharacterAnimationReset(18002354, 0);
        WaitFixedTimeSeconds(1);
        RestartEvent();
    } else if (InArea(18002354, 18002349) && (InArea(10000, 18002348) || InArea(10000, 18002349))) {
        SpawnOneshotSFX(TargetEntityType.Character, 18002354, 220, 440621);
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002366, -1, 18002366);
        PlaySE(10000, SoundType.SFX, 6800);
        PlaySE(10000, SoundType.SFX, 440470);
        PlaySE(10000, SoundType.SFX, 440481);
        SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440481);
        SpawnOneshotSFX(TargetEntityType.Area, 18002366, -1, 440621);
        RequestCharacterAnimationReset(18002354, 0);
        DisplayBossHealthBar(Disabled, 18002354, 0, 999900100);
        SetBossBGM(472000, BossBGMState.Stop1);
        $InitializeEvent(0, 5750302);
        RestartEvent();
    }
    BatchSetEventFlags(1055422920, 1055422925, OFF); 
    RandomlySetEventFlagInRange(1055422920, 1055422925, ON);
    SpawnOneshotSFX(TargetEntityType.Character, 18002354, 220, 440621);
    PlaySE(10000, SoundType.SFX, 6800);
    PlaySE(10000, SoundType.SFX, 440470);
    PlaySE(10000, SoundType.SFX, 440481);
    if (EventFlag(1055422920)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002368, -1, 18002368);
        SpawnOneshotSFX(TargetEntityType.Area, 18002368, -1, 440481);
    } else if (EventFlag(1055422921)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002369, -1, 18002369);
        SpawnOneshotSFX(TargetEntityType.Area, 18002369, -1, 440481);
    } else if (EventFlag(1055422922)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002370, -1, 18002370);
        SpawnOneshotSFX(TargetEntityType.Area, 18002370, -1, 440481);
    } else if (EventFlag(1055422923)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002371, -1, 18002371);
        SpawnOneshotSFX(TargetEntityType.Area, 18002371, -1, 440481);
    } else if (EventFlag(1055422924)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002372, -1, 18002372);
        SpawnOneshotSFX(TargetEntityType.Area, 18002372, -1, 440481);
    } else if (EventFlag(1055422925)) {
        WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, 18002373, -1, 18002373);
        SpawnOneshotSFX(TargetEntityType.Area, 18002373, -1, 440481);
    }
    RequestCharacterAnimationReset(18002354, 0);
    WaitFixedTimeSeconds(1);
    RestartEvent();
});

// SACRED Crucible Lord Hadeon Nemesis Blessings 1
$Event(5750305, Restart, function() {
    WaitFixedTimeSeconds(30);
    EndIf(EventFlag(1055420915));
    $InitializeEvent(0, 5750306);
    EndEvent();
});

// SACRED Crucible Lord Hadeon Nemesis Blessings 2
$Event(5750306, Restart, function() {
    WaitFor(InArea(10000, 18000359) && !InArea(10000, 18002367) && CharacterHPValue(18002354) > 0);
    if (!InArea(10000, 18000359) || InArea(10000, 18002367) || CharacterHPValue(18002354) <= 0) {
        EndEvent();
    }
    if (!EventFlag(1055422049)) {
        WaitRandomTimeSeconds(5, 10);
        SetSpEffect(10000, 1626986);
        SetSpEffect(10000, 1626991);
        SetSpEffect(10000, 1626993);
    }
    BatchSetEventFlags(1055422050, 1055422055, OFF);
    RandomlySetEventFlagInRange(1055422050, 1055422055, ON);
    SetEventFlagID(1055422049, OFF); 
    if (EventFlag(1055422050) || EventFlag(1055422051)) {
        if (CharacterHasSpEffect(10000, 239)) {
            SetEventFlagID(1055422049, ON);
            RestartEvent();
        }
        $InitializeEvent(0, 5750340);
        SpawnOneshotSFX(TargetEntityType.Character, 10000, 220, 7505981);
        PlaySE(10000, SoundType.SFX, 523875);
        SetSpEffect(10000, 1626935);
        WaitFixedTimeSeconds(1);
        RestartEvent();
    } else if (EventFlag(1055422052) || EventFlag(1055422053) || EventFlag(1055422054)) {
        if (CharacterHasSpEffect(10000, 1626916)) {
            SetEventFlagID(1055422049, ON);
            RestartEvent();
        }
        SetSpEffect(10000, 1626926);
        ClearSpEffect(10000, 1626916);
        ClearSpEffect(10000, 1626917);
        ClearSpEffect(10000, 1626918);
        ClearSpEffect(10000, 1626926);
        SetSpEffect(10000, 1626915);
        WaitFixedTimeSeconds(0.1);
        $InitializeEvent(0, 5750340);
        SetSpEffect(10000, 1626916);
        $InitializeEvent(0, 5750308);
        WaitFixedTimeSeconds(1);
        RestartEvent();
    } else if (EventFlag(1055422055)) {
        PlaySE(10000, SoundType.SFX, 530181);
        WaitFixedTimeSeconds(0.1);
        PlaySE(10000, SoundType.SFX, 450264);
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.2);
        SetSpEffect(10000, 1626976);
        WaitFixedTimeSeconds(1);
        RestartEvent();
    }
    RestartEvent();
});

// SACRED Nemesis Thorn Ward
$Event(5750308, Default, function() {
    WaitFor(!CharacterHasSpEffect(10000, 1626916));
    if (CharacterHasSpEffect(10000, 153)) {
        SetSpEffect(10000, 1626922);
    }
    WaitFor(!CharacterHasSpEffect(10000, 1626917));
    if (CharacterHasSpEffect(10000, 153)) {
        SetSpEffect(10000, 1626923);
    } 
    WaitFor(!CharacterHasSpEffect(10000, 1626918));
    if (CharacterHasSpEffect(10000, 153)) {
        SetSpEffect(10000, 1626924);
    } 
    EndEvent();
});

// SACRED Nemesis Rapture
$Event(5750309, Restart, function() {
    EndIf(!PlayerIsInOwnWorld());
    WaitFor(EventFlag(1055420915)
        && InArea(10000, 18002377) && !CharacterDead(10000) && !PlayerHasItem(ItemType.Ring, 6800));
    SetSpEffect(10000, 1626974);
    SetSpEffect(10000, 1626998);
    if (!EventFlag(1055420009)) {
        WaitFixedTimeSeconds(1.95);
        SetSpEffect(10000, 1626974);
        SetSpEffect(10000, 1626982);
        SetSpEffect(10000, 1626990);
        PlaySE(10000, SoundType.SFX, 530181);
        WaitFixedTimeSeconds(0.1);
        PlaySE(10000, SoundType.SFX, 450264);
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(1);
        SetSpEffect(10000, 1626974);
        SetSpEffect(10000, 1626982);
        SetSpEffect(10000, 1626990);
        WaitFixedTimeSeconds(3);
        AwardGesture(102);
        SetEventFlagID(1055420009, ON); 
    }
    WaitFor(CharacterHasSpEffect(10000, 1626966) && InArea(10000, 18002377));
    SuppressSE(SoundType.BGM, 0, true);
    //SetBossBGM(921700, BossBGMState.Start);
    WaitFixedTimeSeconds(3);
    EnableAsset(18000352);
    EnableAsset(18000353);
    EnableAsset(18000354);
    EnableAsset(18000355);
    EnableAsset(18000356);
    EnableAsset(18000357);
    EnableAsset(18000358);
    WaitFixedTimeSeconds(3);
    SetSpEffect(10000, 1626597);
    SetSpEffect(10000, 1626962);
    SetSpEffect(10000, 1626998);
    WaitFixedTimeSeconds(1);
    $InitializeEvent(0, 5750310);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    WaitFixedTimeSeconds(3);
    $InitializeEvent(0, 5750341);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    SetSpEffect(10000, 1626963);
    SetSpEffect(10000, 1626918);
    WaitFixedTimeSeconds(3);
    $InitializeEvent(0, 5750341);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    WaitFixedTimeSeconds(3);
    $InitializeEvent(0, 5750341);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    SetSpEffect(10000, 1626964);
    SetSpEffect(10000, 1626917);
    WaitFixedTimeSeconds(3);
    $InitializeEvent(0, 5750341);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    WaitFixedTimeSeconds(3);
    $InitializeEvent(0, 5750341);
    if (!CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    SetSpEffect(10000, 1626965);
    SetSpEffect(10000, 1626916);
    SetSpEffect(10000, 1626999);
    WaitFixedTimeSeconds(5);
    if (!CharacterDead(10000) && !CharacterHasSpEffect(10000, 1626967)) {
        RestartEvent();
    }
    SetSpEffect(10000, 1626969);
    ClearSpEffect(10000, 1626965);
    PlaySE(10000, SoundType.SFX, 450264);
    PlaySE(10000, SoundType.SFX, 302501);
    PlaySE(10000, SoundType.SFX, 302511);
    PlaySE(10000, SoundType.SFX, 302521);
    PlaySE(10000, SoundType.SFX, 302531);
    PlaySE(10000, SoundType.SFX, 302541);
    PlaySE(10000, SoundType.SFX, 302551);
    SpawnOneshotSFX(TargetEntityType.Asset, 18000352, -1, 7505981);
    SpawnOneshotSFX(TargetEntityType.Asset, 18000353, -1, 7505981);  
    SpawnOneshotSFX(TargetEntityType.Asset, 18000354, -1, 7505981);
    SpawnOneshotSFX(TargetEntityType.Asset, 18000355, -1, 7505981);
    SpawnOneshotSFX(TargetEntityType.Asset, 18000356, -1, 7505981);
    SpawnOneshotSFX(TargetEntityType.Asset, 18000357, -1, 7505981);  
    SpawnOneshotSFX(TargetEntityType.Asset, 18000358, -1, 7505981);
    AwardItemLot(6800);
    SetEventFlagID(1055420010, OFF);
    SetEventFlagID(1055420001, OFF);
    if (EventFlag(1055420918)) {
        SetEventFlagID(1055420002, OFF);
        SetEventFlagID(1055420003, ON);
        SetEventFlagID(1055420010, ON);
    } else {
        SetEventFlagID(1055420002, ON);
        SetEventFlagID(1055420003, OFF);
    }
    SetEventFlagID(1055420000, ON);
    WaitFixedTimeSeconds(0.5);
    if (!EventFlag(1055420001) && !CharacterHasSpEffect(10000, 1626910)) {
        SetEventFlagID(1055420000, OFF);
    }
    $InitializeEvent(0, 5750340);
    ClearSpEffect(10000, 1626999);
    RestartEvent();
});

// SACRED Nemesis Rapture Icon
$Event(5750310, Default, function() {
    WaitFor(!CharacterHasSpEffect(10000, 1626967));
    ClearSpEffect(10000, 1626962);
    ClearSpEffect(10000, 1626963);
    ClearSpEffect(10000, 1626964);
    ClearSpEffect(10000, 1626965);
    ClearSpEffect(10000, 1626999);
    SetSpEffect(10000, 1626998);
    SetSpEffect(10000, 1626974);
    WaitFixedTimeSeconds(3);
    SetSpEffect(10000, 1626996);
    //SetBossBGM(921700, BossBGMState.Stop2); 
    SuppressSE(SoundType.BGM, 0, false);
    WaitFixedTimeSeconds(3);
    DisableAsset(18000352);
    DisableAsset(18000353);
    DisableAsset(18000354);
    DisableAsset(18000355);
    DisableAsset(18000356);
    DisableAsset(18000357);
    DisableAsset(18000358);
    EndEvent();
});

// SACRED Nemesis Candles 1
$Event(5750320, Restart, function() {
    WaitFixedTimeSeconds(0.1);
    DisableAsset(18009800);
    DisableAsset(18009801);
    DisableAsset(18009802);
    DisableAsset(18009803);
    DisableAsset(18009804);
    DisableAsset(18009805);
    DisableAsset(18009806);
    DisableAsset(18009807);
    DisableAsset(18009808);
    DisableAsset(18009809);
    DisableAsset(18009810);
    DisableAsset(18009811);
    DisableAsset(18009812);
    DisableAsset(18009813);
    DisableAsset(18009814);
    DisableAsset(18009815);   
    WaitFor(InArea(10000, 18002355));
    WaitFixedTimeSeconds(1.5);
    EnableAsset(18009800);
    EnableAsset(18009801);
    EnableAsset(18009802);
    EnableAsset(18009803);
    EnableAsset(18009804);
    EnableAsset(18009805);
    EnableAsset(18009806);
    EnableAsset(18009807);
    EnableAsset(18009808);
    EnableAsset(18009809);
    EnableAsset(18009810);
    EnableAsset(18009811);
    EnableAsset(18009812);
    EnableAsset(18009813);
    EnableAsset(18009814);
    EnableAsset(18009815);
    EndEvent();
});

// SACRED Nemesis Candles 2
$Event(5750321, Restart, function() {
    WaitFixedTimeSeconds(0.15);
    DisableAsset(18009820);
    DisableAsset(18009821);
    DisableAsset(18009822);
    DisableAsset(18009823);
    DisableAsset(18009824);
    DisableAsset(18009825);
    DisableAsset(18009826);
    DisableAsset(18009827);
    DisableAsset(18009828);    
    WaitFor(InArea(10000, 18002356));
    EnableAsset(18009820);
    EnableAsset(18009821);
    EnableAsset(18009822);
    EnableAsset(18009823); 
    EnableAsset(18009824);
    EnableAsset(18009825);
    EnableAsset(18009826);
    EnableAsset(18009827);  
    EnableAsset(18009828); 
    EndEvent();
});

// SACRED Nemesis Candles 3
$Event(5750322, Restart, function() {
    WaitFixedTimeSeconds(0.2);
    DisableAsset(18009830);
    DisableAsset(18009831);
    DisableAsset(18009832);
    DisableAsset(18009833);
    DisableAsset(18009834);
    DisableAsset(18009835);
    DisableAsset(18009836);
    DisableAsset(18009837);
    DisableAsset(18009838); 
    DisableAsset(18009839);
    DisableAsset(18009840);  
    WaitFor(InArea(10000, 18002357));
    EnableAsset(18009830);
    EnableAsset(18009831);
    EnableAsset(18009832);
    EnableAsset(18009833); 
    EnableAsset(18009834);
    EnableAsset(18009835);
    EnableAsset(18009836);
    EnableAsset(18009837);  
    EnableAsset(18009838); 
    EnableAsset(18009839);
    EnableAsset(18009840);  
    EndEvent();
});

// SACRED Nemesis Candles 4
$Event(5750323, Restart, function() {
    WaitFixedTimeSeconds(0.25);
    DisableAsset(18009850);
    DisableAsset(18009851);
    DisableAsset(18009852);
    DisableAsset(18009853);
    DisableAsset(18009854);
    DisableAsset(18009855);
    DisableAsset(18009856);
    DisableAsset(18009857);
    DisableAsset(18009858); 
    DisableAsset(18009859);
    DisableAsset(18009860); 
    DisableAsset(18009861);
    DisableAsset(18009862);
    DisableAsset(18009863);
    DisableAsset(18009864);
    DisableAsset(18009865);
    DisableAsset(18009866);
    DisableAsset(18009867);
    DisableAsset(18009868); 
    DisableAsset(18009869);
    DisableAsset(18009870); 
    WaitFor(InArea(10000, 18002358));
    EnableAsset(18009850);
    EnableAsset(18009851);
    EnableAsset(18009852);
    EnableAsset(18009853); 
    EnableAsset(18009854);
    EnableAsset(18009855);
    EnableAsset(18009856);
    EnableAsset(18009857);  
    EnableAsset(18009858); 
    EnableAsset(18009859);
    EnableAsset(18009860);  
    EnableAsset(18009861);
    EnableAsset(18009862);
    EnableAsset(18009863); 
    EnableAsset(18009864);
    EnableAsset(18009865);
    EnableAsset(18009866);
    EnableAsset(18009867);  
    EnableAsset(18009868); 
    EnableAsset(18009869);
    EnableAsset(18009870); 
    EndEvent();
});

// SACRED Nemesis Candles 5
$Event(5750324, Restart, function() {
    WaitFixedTimeSeconds(0.3);
    DisableAsset(18009880);
    DisableAsset(18009881);
    DisableAsset(18009882);
    DisableAsset(18009883);
    WaitFor(InArea(10000, 18002359));
    EnableAsset(18009880);
    EnableAsset(18009881);
    EnableAsset(18009882);
    EnableAsset(18009883);
    EndEvent();
});

// SACRED Nemesis Candles 6
$Event(5750325, Restart, function() {
    WaitFixedTimeSeconds(0.35);
    DisableAsset(18009890);
    DisableAsset(18009891);
    DisableAsset(18009892);
    DisableAsset(18009893);
    WaitFor(InArea(10000, 18002360));
    EnableAsset(18009890);
    EnableAsset(18009891);
    EnableAsset(18009892);
    EnableAsset(18009893);
    EndEvent();
});

// SACRED Nemesis Candles 7
$Event(5750326, Restart, function() {
    WaitFixedTimeSeconds(0.4);
    DisableAsset(18009900);
    DisableAsset(18009901);
    DisableAsset(18009902);
    DisableAsset(18009903);
    WaitFor(InArea(10000, 18002361));
    EnableAsset(18009900);
    EnableAsset(18009901);
    EnableAsset(18009902);
    EnableAsset(18009903);
    EndEvent();
});

// SACRED Nemesis Candles 8
$Event(5750327, Restart, function() {
    WaitFixedTimeSeconds(0.45);
    DisableAsset(18009910);
    DisableAsset(18009911);
    DisableAsset(18009912);
    DisableAsset(18009913);
    DisableAsset(18009914);
    DisableAsset(18009915);
    DisableAsset(18009916);
    DisableAsset(18009917);
    DisableAsset(18009918); 
    DisableAsset(18009919);
    DisableAsset(18009920);  
    WaitFor(InArea(10000, 18002362));
    EnableAsset(18009910);
    EnableAsset(18009911);
    EnableAsset(18009912);
    EnableAsset(18009913); 
    EnableAsset(18009914);
    EnableAsset(18009915);
    EnableAsset(18009916);
    EnableAsset(18009917);  
    EnableAsset(18009918); 
    EnableAsset(18009919);
    EnableAsset(18009920);
    EndEvent();
});

// SACRED Nemesis Candles 9
$Event(5750328, Restart, function() {
    DisableAsset(18009930);
    DisableAsset(18009931);
    DisableAsset(18009932);
    DisableAsset(18009933);
    DisableAsset(18009934);
    DisableAsset(18009935);
    DisableAsset(18009936);
    DisableAsset(18009937);
    DisableAsset(18009938); 
    DisableAsset(18009939);
    DisableAsset(18009940);  
    DisableAsset(18009941);
    DisableAsset(18009942);
    WaitFor(InArea(10000, 18002363));
    EnableAsset(18009930);
    EnableAsset(18009931);
    EnableAsset(18009932);
    EnableAsset(18009933); 
    EnableAsset(18009934);
    EnableAsset(18009935);
    EnableAsset(18009936);
    EnableAsset(18009937);  
    EnableAsset(18009938); 
    EnableAsset(18009939);
    EnableAsset(18009940);
    EnableAsset(18009941);
    EnableAsset(18009942);
    EndEvent();
});

// SACRED Nemesis Candles 10
$Event(5750329, Restart, function() {
    WaitFixedTimeSeconds(0.5);
    DisableAsset(18009950);
    DisableAsset(18009951);
    DisableAsset(18009952);
    DisableAsset(18009953);
    DisableAsset(18009954);
    DisableAsset(18009955);
    DisableAsset(18009956);
    WaitFor(InArea(10000, 18002364));
    EnableAsset(18009950);
    EnableAsset(18009951);
    EnableAsset(18009952);
    EnableAsset(18009953); 
    EnableAsset(18009954);
    EnableAsset(18009955);
    EnableAsset(18009956);
    EndEvent();
});

// SACRED Nemesis Candles 11
$Event(5750330, Restart, function() {
    WaitFixedTimeSeconds(0.55);
    DisableAsset(18009960);
    DisableAsset(18009961);
    DisableAsset(18009962);
    DisableAsset(18009963);
    DisableAsset(18009964);
    DisableAsset(18009965);
    DisableAsset(18009966);
    DisableAsset(18009967);
    DisableAsset(18009968); 
    DisableAsset(18009969);
    DisableAsset(18009970);  
    DisableAsset(18009971);
    DisableAsset(18009972);
    DisableAsset(18009973);
    DisableAsset(18009974);
    DisableAsset(18009975);
    DisableAsset(18009976);
    DisableAsset(18009977);
    DisableAsset(18009978); 
    WaitFor(InArea(10000, 18002365));
    EnableAsset(18009960);
    EnableAsset(18009961);
    EnableAsset(18009962);
    EnableAsset(18009963); 
    EnableAsset(18009964);
    EnableAsset(18009965);
    EnableAsset(18009966);
    EnableAsset(18009967);  
    EnableAsset(18009968); 
    EnableAsset(18009969);
    EnableAsset(18009970);
    EnableAsset(18009971);
    EnableAsset(18009972);
    EnableAsset(18009973); 
    EnableAsset(18009974);
    EnableAsset(18009975);
    EnableAsset(18009976);
    EnableAsset(18009977);  
    EnableAsset(18009978);
    EndEvent();
});

// SACRED Nemesis Candles 12
$Event(5750331, Restart, function() {
    WaitFixedTimeSeconds(0.6);
    DisableAsset(18009980);
    DisableAsset(18009981);
    DisableAsset(18009982);
    DisableAsset(18009983);
    DisableAsset(18009984);
    DisableAsset(18009985);
    DisableAsset(18009986);
    DisableAsset(18009987);
    WaitFor(InArea(10000, 18002378));
    EnableAsset(18009980);
    EnableAsset(18009981);
    EnableAsset(18009982);
    EnableAsset(18009983); 
    EnableAsset(18009984);
    EnableAsset(18009985);
    EnableAsset(18009986);
    EnableAsset(18009987);  
    EndEvent();
});

// SACRED Nemesis Speaks 1
$Event(5750340, Default, function() {
    BatchSetEventFlags(1055422060, 1055422069, OFF);
    RandomlySetEventFlagInRange(1055422060, 1055422069, ON);
    if (EventFlag(1055422060)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.35);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.22);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.28);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.23);
        PlaySE(10000, SoundType.SFX, 302551);
    } else if (EventFlag(1055422061)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.13);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302531);
    } else if (EventFlag(1055422062)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.19);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.25);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.12);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.20);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302541);
    } else if (EventFlag(1055422063)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.13);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.26);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.15);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302541);
    } else if (EventFlag(1055422064)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.25);
        PlaySE(10000, SoundType.SFX, 302531);
    } else if (EventFlag(1055422065)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.12);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.22);
        PlaySE(10000, SoundType.SFX, 302501);
    } else if (EventFlag(1055422066)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.15);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.28);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.13);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.32);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302511);
    } else if (EventFlag(1055422067)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.33);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.12);
        PlaySE(10000, SoundType.SFX, 302551);
    } else if (EventFlag(1055422068)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.22);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.19);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.31);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.15);
        PlaySE(10000, SoundType.SFX, 302521);
    } else if (EventFlag(1055422069)) {
        PlaySE(10000, SoundType.SFX, 450264);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.23);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302501);
    }
    EndEvent();
});

// SACRED Nemesis Speaks 2
$Event(5750341, Default, function() {
    BatchSetEventFlags(1055422070, 1055422081, OFF);
    RandomlySetEventFlagInRange(1055422070, 1055422081, ON);
    if (EventFlag(1055422070)) {
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.22);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.28);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.23);
        PlaySE(10000, SoundType.SFX, 302551);
    } else if (EventFlag(1055422071)) {
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.13);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302541);
    } else if (EventFlag(1055422072)) {
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.25);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.12);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.20);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302541);
    } else if (EventFlag(1055422073)) {
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.26);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.15);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302541);
    } else if (EventFlag(1055422074)) {
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.29);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.25);
        PlaySE(10000, SoundType.SFX, 302531);
    } else if (EventFlag(1055422075)) {
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.22);
        PlaySE(10000, SoundType.SFX, 302501);
    } else if (EventFlag(1055422076)) {
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.28);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.13);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.32);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302511);
    } else if (EventFlag(1055422077)) {
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.18);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.21);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.33);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.12);
        PlaySE(10000, SoundType.SFX, 302551);
    } else if (EventFlag(1055422078)) {
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.19);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.31);
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.17);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.24);
        PlaySE(10000, SoundType.SFX, 302501);
        WaitFixedTimeSeconds(0.15);
        PlaySE(10000, SoundType.SFX, 302521);
    } else if (EventFlag(1055422079)) {
        PlaySE(10000, SoundType.SFX, 302511);
        WaitFixedTimeSeconds(0.27);
        PlaySE(10000, SoundType.SFX, 302521);
        WaitFixedTimeSeconds(0.14);
        PlaySE(10000, SoundType.SFX, 302531);
        WaitFixedTimeSeconds(0.23);
        PlaySE(10000, SoundType.SFX, 302541);
        WaitFixedTimeSeconds(0.11);
        PlaySE(10000, SoundType.SFX, 302551);
        WaitFixedTimeSeconds(0.16);
        PlaySE(10000, SoundType.SFX, 302501);
    } else if (EventFlag(1055422080)) {
        $InitializeEvent(0, 5750343);
    } else if (EventFlag(1055422081)) {
        WaitFixedTimeSeconds(1);
    }
    EndEvent();
});

// SACRED Nemesis Speaks 3
$Event(5750343, Default, function() {
    WaitFixedTimeSeconds(0.1);
    BatchSetEventFlags(1055422086, 1055422089, OFF); 
    RandomlySetEventFlagInRange(1055422086, 1055422089, ON);
    if (EventFlag(1055422086) || EventFlag(1055422087) || EventFlag(1055422088)) {
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
    } else if (EventFlag(1055422089)) {
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
        $InitializeEvent(0, 5750341);
        WaitRandomTimeSeconds(0.75, 2);
    }
    EndEvent();
});
