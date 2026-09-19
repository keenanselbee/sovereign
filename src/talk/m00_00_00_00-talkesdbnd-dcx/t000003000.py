# -*- coding: utf-8 -*-
def t000003000_1():
    """State 0,1"""
    if not IsClientPlayer():
        """State 3"""
        Label('L0')
        call = t000003000_x46()
        def WhilePaused():
        # eventflag:400001:lot:100010:Rold Medallion
            GiveSpEffectToSelfIf(GetEventFlag(400001) == 0 or GetEventFlag(108) == 1, 9600)
        # eventflag:400001:lot:100010:Rold Medallion
            GiveSpEffectToSelfIf(GetEventFlag(400001) == 1 and GetEventFlag(108) == 0, 9601)
            GiveSpEffectToPlayerIf((GetRelativeAngleToPlayerWithAxis(90) < 90) == 1, 9600)
            GiveSpEffectToPlayerIf((GetRelativeAngleToPlayerWithAxis(90) < 90) == 0, 9603)
        assert IsClientPlayer()
    else:
        pass
    """State 4"""
    call = t000003000_x47()
    assert not IsClientPlayer()
    Goto('L0')
    """Unused"""
    """State 2"""
    # actionbutton:6000:"Talk"
    t000003000_x7(flag3=6000, flag4=6000, flag5=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                  flag6=6001, flag7=6000, flag8=4652, flag9=6000, flag10=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                  mode2=1, mode3=1)
    Quit()

def t000003000_x0(actionbutton1=6000, flag7=6000, flag11=6000, flag12=6000, flag13=6000, flag14=6000, flag6=6001):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 3"""
        assert (GetEventFlag(flag7) or GetEventFlag(flag11) or GetEventFlag(flag12) or GetEventFlag(flag13) or
                GetEventFlag(flag14))
        """State 4"""
        assert not GetEventFlag(flag6)
        """State 2"""
        if (GetEventFlag(flag6) or not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead()
            and not IsCharacterDisabled()) or (not GetEventFlag(flag7) and not GetEventFlag(flag11) and not GetEventFlag(flag12)
            and not GetEventFlag(flag13) and not GetEventFlag(flag14))):
            pass
        # actionbutton:6000:"Talk"
        elif CheckActionButtonArea(actionbutton1):
            break
    """State 5"""
    return 0

def t000003000_x1():
    """State 0,1"""
    if not CheckSpecificPersonTalkHasEnded(0):
        """State 7"""
        ClearTalkProgressData()
        StopEventAnimWithoutForcingConversationEnd(0)
        """State 6"""
        ReportConversationEndToHavokBehavior()
    else:
        pass
    """State 2"""
    if CheckSpecificPersonGenericDialogIsOpen(0):
        """State 3"""
        ForceCloseGenericDialog()
    else:
        pass
    """State 4"""
    if CheckSpecificPersonMenuIsOpen(-1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0):
        """State 5"""
        ForceCloseMenu()
    else:
        pass
    """State 8"""
    return 0

def t000003000_x2():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ForceCloseGenericDialog()
    ForceCloseMenu()
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t000003000_x3(lot1=_):
    """State 0,1"""
    AwardItemLot(lot1)
    assert not IsMenuOpen(MenuType.Bonfire) and GetCurrentStateElapsedFrames() > 1
    """State 2"""
    return 0

def t000003000_x4(action1=23241004):
    """State 0,1"""
    # action:23241004:"A red mark was made on the map"
    OpenGenericDialog(DialogBoxType.CenterBottom1, action1, DialogResult.Left, DialogBoxStyle.OrnateNoOptions, 1)
    assert not CheckSpecificPersonGenericDialogIsOpen(0)
    """State 2"""
    return 0

def t000003000_x5(val2=10, val3=12):
    """State 0,1"""
    assert GetDistanceToPlayer() < val2 and GetCurrentStateElapsedFrames() > 1
    """State 2"""
    if PlayerDiedFromFallInstantly() == False and PlayerDiedFromFallDamage() == False:
        """State 3,6"""
        call = t000003000_x21()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 5"""
            assert t000003000_x1()
    else:
        """State 4,7"""
        call = t000003000_x35()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 8"""
            assert t000003000_x1()
    """State 9"""
    return 0

def t000003000_x6():
    """State 0,1"""
    assert t000003000_x1()
    """State 2"""
    return 0

def t000003000_x7(flag3=6000, flag4=6000, flag5=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                  flag6=6001, flag7=6000, flag8=4652, flag9=6000, flag10=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                  mode2=1, mode3=1):
    """State 0"""
    assert GetCurrentStateElapsedTime() > 1.5
    while True:
        """State 2"""
        call = t000003000_x24(flag3=flag3, flag4=flag4, flag5=flag5, val1=val1, val2=val2, val3=val3, val4=val4,
                              val5=val5, actionbutton1=actionbutton1, flag6=flag6, flag7=flag7, flag8=flag8, flag9=flag9,
                              flag10=flag10, z1=z1, z2=z2, z3=z3, z4=z4, mode2=mode2, mode3=mode3)
        assert IsClientPlayer()
        """State 1"""
        call = t000003000_x23()
        assert not IsClientPlayer()
    """Unused"""
    """State 3"""
    return 0

def t000003000_x8(val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000, flag6=6001, flag7=6000, flag8=4652,
                  flag9=6000, flag10=6000, z1=1, z2=1000000, z3=1000000, z4=1000000, mode2=1, mode3=1):
    """State 0"""
    while True:
        """State 2"""
        call = t000003000_x11(actionbutton1=actionbutton1, flag6=flag6, flag7=flag7, z2=z2, z3=z3, z4=z4)
        def WhilePaused():
            RemoveMyAggroIf(IsAttackedBySomeone() == 1 and (DoesSelfHaveSpEffect(9626) == 1 and DoesSelfHaveSpEffect(9627) == 1))
            GiveSpEffectToPlayerIf(CheckSpecificPersonTalkHasEnded(0) == 0, 9640)
        if call.Done():
            """State 4"""
            Label('L0')
            ChangeCamera(1000000)
            call = t000003000_x15(val1=val1, z1=z1)
            def WhilePaused():
                ChangeCameraIf(GetDistanceToPlayer() > 2.5, -1)
                RemoveMyAggroIf(IsAttackedBySomeone() == 1 and (DoesSelfHaveSpEffect(9626) == 1 and DoesSelfHaveSpEffect(9627) == 1))
                GiveSpEffectToPlayer(9640)
                SetLookAtEntityForTalkIf(1 == (mode2 == 1), -1, 0)
                SetLookAtEntityForTalkIf(1 == (mode3 == 1), 0, -1)
            def ExitPause():
                ChangeCamera(-1)
            if call.Done():
                continue
            elif IsAttackedBySomeone():
                pass
        elif IsAttackedBySomeone() and not DoesSelfHaveSpEffect(9626) and not DoesSelfHaveSpEffect(9627):
            pass
        elif GetEventFlag(flag10):
            Goto('L0')
        elif GetEventFlag(flag8) and not GetEventFlag(flag9) and GetDistanceToPlayer() < val4:
            """State 5"""
            call = t000003000_x17(val5=val5)
            if call.Done():
                continue
            elif IsAttackedBySomeone():
                pass
        elif ((GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6) and not CheckSpecificPersonTalkHasEnded(0)
              and not DoesSelfHaveSpEffect(9625)):
            """State 6"""
            assert t000003000_x28() and CheckSpecificPersonTalkHasEnded(0)
            continue
        elif GetEventFlag(9000):
            """State 1"""
            assert not GetEventFlag(9000)
            continue
        """State 3"""
        def ExitPause():
            RemoveMyAggro()
        assert t000003000_x13(val2=val2, val3=val3)
    """Unused"""
    """State 7"""
    return 0

def t000003000_x9(val2=10, val3=12):
    """State 0,1"""
    call = t000003000_x19(val2=val2, val3=val3)
    assert IsPlayerDead()
    """State 2"""
    t000003000_x5(val2=val2, val3=val3)
    Quit()
    """Unused"""
    """State 3"""
    return 0

def t000003000_x10(flag3=6000, val2=10, val3=12):
    """State 0,8"""
    assert t000003000_x37()
    """State 1"""
    if GetEventFlag(flag3):
        """State 2"""
        pass
    else:
        """State 3"""
        if GetDistanceToPlayer() < val2:
            """State 4,6"""
            call = t000003000_x22()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t000003000_x1()
        else:
            """State 5"""
            pass
    """State 9"""
    return 0

def t000003000_x11(actionbutton1=6000, flag6=6001, flag7=6000, z2=1000000, z3=1000000, z4=1000000):
    """State 0,1"""
    call = t000003000_x12(machine1=2000, val6=2000)
    if call.Get() == 1:
        """State 2"""
        assert (t000003000_x0(actionbutton1=actionbutton1, flag7=flag7, flag11=6000, flag12=6000, flag13=6000,
                flag14=6000, flag6=flag6))
    elif call.Done():
        pass
    """State 3"""
    return 0

def t000003000_x12(machine1=_, val6=_):
    """State 0,1"""
    if MachineExists(machine1):
        """State 2"""
        assert GetCurrentStateElapsedFrames() > 1
        """State 4"""
        def WhilePaused():
            RunMachine(machine1)
        assert GetMachineResult() == val6
        """State 5"""
        return 0
    else:
        """State 3,6"""
        return 1

def t000003000_x13(val2=10, val3=12):
    """State 0"""
    assert GetCurrentStateElapsedFrames() > 1
    """State 5"""
    assert t000003000_x1()
    """State 3"""
    if GetDistanceToPlayer() < val2:
        """State 1"""
        if IsPlayerAttacking():
            """State 6"""
            call = t000003000_x14()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t000003000_x29()
        else:
            """State 4"""
            pass
    else:
        """State 2"""
        pass
    """State 8"""
    return 0

def t000003000_x14():
    """State 0,1"""
    assert t000003000_x12(machine1=1101, val6=1101)
    """State 2"""
    return 0

def t000003000_x15(val1=5, z1=1):
    """State 0,2"""
    assert t000003000_x25()
    """State 1"""
    call = t000003000_x16()
    if call.Done():
        pass
    elif (GetDistanceToPlayer() > val1 or GetTalkInterruptReason() == 6) and not DoesSelfHaveSpEffect(9625):
        """State 3"""
        assert t000003000_x27()
    """State 4"""
    return 0

def t000003000_x16():
    """State 0,1"""
    assert t000003000_x12(machine1=1000, val6=1000)
    """State 2"""
    return 0

def t000003000_x17(val5=12):
    """State 0,1"""
    call = t000003000_x18()
    if call.Done():
        pass
    elif GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6:
        """State 2"""
        assert t000003000_x28()
    """State 3"""
    return 0

def t000003000_x18():
    """State 0,1"""
    assert t000003000_x12(machine1=1100, val6=1100)
    """State 2"""
    return 0

def t000003000_x19(val2=10, val3=12):
    """State 0,5"""
    assert t000003000_x37()
    """State 2"""
    assert not GetEventFlag(3000)
    while True:
        """State 1"""
        assert GetDistanceToPlayer() < val2
        """State 3"""
        call = t000003000_x20()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 4"""
            assert t000003000_x30()
    """Unused"""
    """State 6"""
    return 0

def t000003000_x20():
    """State 0,2"""
    call = t000003000_x12(machine1=1102, val6=1102)
    if call.Get() == 1:
        """State 1"""
        Quit()
    elif call.Done():
        """State 3"""
        return 0

def t000003000_x21():
    """State 0,1"""
    assert t000003000_x12(machine1=1001, val6=1001)
    """State 2"""
    return 0

def t000003000_x22():
    """State 0,1"""
    assert t000003000_x12(machine1=1103, val6=1103)
    """State 2"""
    return 0

def t000003000_x23():
    """State 0"""
    Quit()
    """Unused"""
    """State 1"""
    return 0

def t000003000_x24(flag3=6000, flag4=6000, flag5=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                   flag6=6001, flag7=6000, flag8=4652, flag9=6000, flag10=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                   mode2=1, mode3=1):
    """State 0"""
    while True:
        """State 1"""
        RemoveMyAggro()
        call = t000003000_x8(val1=val1, val2=val2, val3=val3, val4=val4, val5=val5, actionbutton1=actionbutton1,
                             flag6=flag6, flag7=flag7, flag8=flag8, flag9=flag9, flag10=flag10, z1=z1, z2=z2, z3=z3,
                             z4=z4, mode2=mode2, mode3=mode3)
        if CheckSelfDeath() or GetEventFlag(flag3):
            """State 3"""
            Label('L0')
            call = t000003000_x10(flag3=flag3, val2=val2, val3=val3)
            if not CheckSelfDeath() and not GetEventFlag(flag3):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(flag4) or GetEventFlag(flag5):
            """State 2"""
            call = t000003000_x9(val2=val2, val3=val3)
            if CheckSelfDeath() or GetEventFlag(flag3):
                Goto('L0')
            elif not GetEventFlag(flag4) and not GetEventFlag(flag5):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(9000) or (IsPlayerDead() and not DoesSelfHaveSpEffect(9649)):
            pass
        """State 4"""
        assert t000003000_x36() and (not GetEventFlag(9000) and not IsPlayerDead())
    """Unused"""
    """State 5"""
    return 0

def t000003000_x25():
    """State 0,1"""
    assert t000003000_x26()
    """State 2"""
    return 0

def t000003000_x26():
    """State 0,1"""
    assert t000003000_x12(machine1=1104, val6=1104)
    """State 2"""
    return 0

def t000003000_x27():
    """State 0,1"""
    call = t000003000_x12(machine1=1201, val6=1201)
    if call.Get() == 1:
        """State 2"""
        assert t000003000_x6()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t000003000_x28():
    """State 0,1"""
    call = t000003000_x12(machine1=1300, val6=1300)
    if call.Get() == 1:
        """State 2"""
        assert t000003000_x6()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t000003000_x29():
    """State 0,1"""
    call = t000003000_x12(machine1=1301, val6=1301)
    if call.Get() == 1:
        """State 2"""
        assert t000003000_x6()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t000003000_x30():
    """State 0,1"""
    call = t000003000_x12(machine1=1302, val6=1302)
    if call.Get() == 1:
        """State 2"""
        assert t000003000_x6()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t000003000_x31(text3=_, flag1=_, mode6=1):
    """State 0,5"""
    assert t000003000_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text3, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 4"""
    if mode6 == 0:
        pass
    else:
        """State 3"""
        ReportConversationEndToHavokBehavior()
    """State 2"""
    SetEventFlag(flag1, FlagState.On)
    """State 6"""
    return 0

def t000003000_x32(text1=_, mode5=1):
    """State 0,4"""
    assert t000003000_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text1, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 3"""
    if mode5 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t000003000_x33(text4=10002100, mode4=1):
    """State 0,4"""
    assert t000003000_x34() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    # talk:10002100:" "
    TalkToPlayer(text4, -1, -1, 1)
    """State 3"""
    if mode4 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t000003000_x34():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t000003000_x35():
    """State 0,1"""
    assert t000003000_x12(machine1=1002, val6=1002)
    """State 2"""
    return 0

def t000003000_x36():
    """State 0,1"""
    assert t000003000_x1()
    """State 2"""
    return 0

def t000003000_x37():
    """State 0,1"""
    if CheckSpecificPersonGenericDialogIsOpen(0):
        """State 2"""
        ForceCloseGenericDialog()
    else:
        pass
    """State 3"""
    if CheckSpecificPersonMenuIsOpen(-1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0):
        """State 4"""
        ForceCloseMenu()
    else:
        pass
    """State 5"""
    return 0

def t000003000_x38():
    """State 0,1"""
    if not GetEventFlag(10000800):
        """State 2"""
        pass
    else:
        """State 3"""
        pass
    """State 4"""
    return 0

def t000003000_x39():
    """State 0,3"""
    # talk:10002000:"Shall I turn your runes to strength?"
    # talk:10002001:"Let my hand rest upon you, for but a moment."
    assert t000003000_x32(text1=10002000, mode5=1)
    """State 1"""
    SetWorkValue(2, GetPlayerStat(PlayerStat.RuneLevel))
    """State 4"""
    def ExitPause():
        SetWorkValue(0, 0)
        SetWorkValue(1, 0)
    assert t000003000_x44()
    """State 2"""
    SetWorkValue(2, 0)
    """State 5"""
    return 0

def t000003000_x40():
    """State 0"""
    if GetEventFlag(110):
        """State 1"""
        pass
    elif not GetEventFlag(4681):
        """State 3"""
        assert t000003000_x73()
    elif not GetEventFlag(4680):
        """State 2"""
        pass
    elif GetEventFlag(108):
        """State 6"""
        assert t000003000_x75()
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(11009260) and not GetEventFlag(400001):
        """State 4"""
        assert t000003000_x74()
    else:
        """State 5"""
        assert t000003000_x72()
    """State 7"""
    return 0

def t000003000_x41():
    """State 0,8"""
    assert GetCurrentStateElapsedTime() > 2
    """State 10"""
    # talk:10001000:"Have you heard of the Finger Maidens?"
    # talk:10001001:"They serve the Two Fingers, offering guidance, and aid, to the Tarnished."
    # talk:10001002:"But you, I am afraid, are maidenless."
    # talk:10001003:"I can play the role of maiden."
    # talk:10001004:"Turning runes into strength."
    # talk:10001005:"To aid you in your search for the Elden Ring."
    # talk:10001006:"You need only take me with you."
    # talk:10001007:"To the foot of the Erdtree."
    assert t000003000_x31(text3=10001000, flag1=4681, mode6=1)
    """State 4"""
    ClearTalkListData()
    ClearPreviousMenuSelection()
    """State 5"""
    # action:21001000:"Accept"
    AddTalkListData(1, 21001000, -1)
    # action:21001001:"Refuse"
    AddTalkListData(2, 21001001, -1)
    """State 6"""
    OpenConversationChoicesMenu(0)
    assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 1"""
    if GetTalkListEntryResult() == 1:
        """State 2,11"""
        assert t000003000_x81()
    else:
        """State 7,9"""
        # talk:10001200:"I understand. I'm asking you to put faith in but a stranger."
        # talk:10001201:"Yet I'm certain that we can reach an understanding."
        # talk:10001202:"Summon me by grace if you should reconsider."
        assert t000003000_x31(text3=10001200, flag1=1042372700, mode6=1)
    """State 3"""
    SetEventFlag(4670, FlagState.Off)
    SetEventFlag(4698, FlagState.Off)
    """State 12"""
    return 0

def t000003000_x42():
    """State 0,1"""
    assert DoesSelfHaveSpEffect(9606)
    """State 2"""
    GiveSpEffectToPlayer(9602)
    def WhilePaused():
        GiveSpEffectToPlayer(9602)
    def ExitPause():
        GiveSpEffectToPlayer(9602)
    assert GetCurrentStateElapsedTime() > 9
    """State 3"""
    SetEventFlag(1054539205, FlagState.On)
    SetEventFlag(1054539200, FlagState.On)
    GiveSpEffectToPlayer(9601)
    def WhilePaused():
        GiveSpEffectToPlayer(9601)
    def ExitPause():
        GiveSpEffectToPlayer(9601)
    assert GetCurrentStateElapsedTime() > 2
    """State 5"""
    SetEventFlag(9000, FlagState.Off)
    SetEventFlag(9020, FlagState.Off)
    """State 4"""
    ChangeCamera(-1)
    Quit()
    """Unused"""
    """State 6"""
    return 0

def t000003000_x43():
    """State 0,1"""
    if GetEventFlag(10009656):
        """State 16"""
        assert t000003000_x61()
    elif GetEventFlag(1042379200):
        """State 4"""
        assert t000003000_x50()
    elif GetEventFlag(1042379202):
        """State 5"""
        assert t000003000_x51()
    elif GetEventFlag(1042372703):
        """State 26"""
        assert t000003000_x54()
    elif GetEventFlag(1042379206):
        """State 6"""
        assert t000003000_x52()
    elif GetEventFlag(1046389201):
        """State 7"""
        # talk:10004100:"Very well. In Marika's own words."
        # talk:10004101:"My Lord, and thy warriors. I divest each of thee of thy grace."
        # talk:10004102:"With thine eyes dimmed, ye will be driven from the Lands Between."
        # talk:10004103:"Ye will wage war in a land afar, where ye will live, and die."
        # talk:10004104:"Well? Perhaps that might serve you in lieu of a maiden's guidance."
        assert t000003000_x56(text3=10004100, flag1=1046389202, flag2=1046389203)
    elif GetEventFlag(1043349250):
        """State 8"""
        # talk:10004400:"In Marika's own words."
        # talk:10004401:"Then, after thy death, I will give back what I once claimed."
        # talk:10004402:"Return to the Lands Between, wage war, and brandish the Elden Ring."
        # talk:10004403:"Grow strong in the face of death. Warriors of my lord. Lord Godfrey."
        assert t000003000_x56(text3=10004400, flag1=1043349251, flag2=1043349252)
    elif GetEventFlag(1038509250):
        """State 9"""
        # talk:10004500:"In Marika's own words."
        # talk:10004501:"The Erdtree governs all. The choice is thine."
        # talk:10004502:"Become one with the Order. Or divest thyself of it."
        # talk:10004503:"To wallow at the fringes; a powerless upstart."
        assert t000003000_x56(text3=10004500, flag1=1038509251, flag2=1038509252)
    elif GetEventFlag(1043539250):
        """State 10"""
        # talk:10010100:"In Marika's own words."
        # talk:10010101:"Hear me, Demigods. My children beloved."
        # talk:10010102:"Make of thyselves that which ye desire. Be it a Lord. Be it a God."
        # talk:10010103:"But should ye fail to become aught at all, ye will be forsaken."
        # talk:10010104:"Amounting only to sacrifices..."
        assert t000003000_x56(text3=10010100, flag1=1043539251, flag2=1043539252)
    elif GetEventFlag(11009255):
        """State 11"""
        # talk:10010200:"In Marika's own words."
        # talk:10010201:"O Radagon, leal hound of the Golden Order."
        # talk:10010202:"Thou'rt yet to become me. Thou'rt yet to become a god."
        # talk:10010203:"Let us be shattered, both. Mine other self."
        assert t000003000_x56(text3=10010200, flag1=11009256, flag2=11009257)
    elif GetEventFlag(1043509200):
        """State 23"""
        # talk:10010300:"In Marika's own words."
        # talk:10010301:"I declare mine intent, to search the depths of the Golden Order."
        # talk:10010302:"Through understanding of the proper way, our faith, our grace, is increased."
        # talk:10010303:"Those blissful early days of blind belief are long past."
        # talk:10010304:"My comrades; why must ye falter?"
        assert t000003000_x56(text3=10010300, flag1=1043509201, flag2=1043509202)
    elif GetEventFlag(1054559200):
        """State 12"""
        # talk:10010400:"In Marika's own words."
        # talk:10010401:"Hark, brave warriors. Hark, my lord Godfrey. We commend your deeds."
        # talk:10010402:"Guidance hath delivered ye through each ordeal, to the place ye stand."
        # talk:10010403:"Put the Giants to the sword, and confine the flame atop the mount."
        # talk:10010404:"Let a new epoch begin. An epoch glistening with life."
        # talk:10010405:"Brandish the Elden Ring, for the Age of the Erdtree!"
        assert t000003000_x56(text3=10010400, flag1=1054559201, flag2=1054559202)
    elif GetEventFlag(1036489250):
        """State 13"""
        assert t000003000_x57()
    elif GetEventFlag(1039519250):
        """State 14"""
        assert t000003000_x58()
    elif GetEventFlag(11009265):
        """State 27"""
        assert t000003000_x62()
    elif GetEventFlag(1037519200):
        """State 15"""
        assert t000003000_x59()
    elif GetEventFlag(1054539210):
        """State 19"""
        assert t000003000_x65()
    elif GetEventFlag(1054539215):
        """State 20"""
        assert t000003000_x66()
    elif GetEventFlag(35009350):
        """State 21"""
        assert t000003000_x67()
    elif GetEventFlag(35009352):
        """State 22"""
        assert t000003000_x68()
    elif GetEventFlag(35009355):
        """State 24"""
        assert t000003000_x69()
    elif GetEventFlag(35009358):
        """State 25"""
        assert t000003000_x70()
    elif GetEventFlag(11009270):
        """State 17"""
        assert t000003000_x63()
    elif GetEventFlag(11009275):
        """State 18"""
        assert t000003000_x64()
    elif GetEventFlag(4699):
        """State 3"""
        # talk:999999997:""
        assert t000003000_x31(text3=999999997, flag1=11009251, mode6=1)
    else:
        """State 2"""
        pass
    """State 28"""
    return 0

def t000003000_x44():
    """State 0,1"""
    OpenSoul()
    """State 2"""
    # talk:10002100:" "
    assert t000003000_x33(text4=10002100, mode4=1) and not (CheckSpecificPersonMenuIsOpen(10, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 3"""
    return 0

def t000003000_x45():
    """State 0,7"""
    assert not GetEventFlag(9001)
    """State 10"""
    assert not DoesSelfHaveSpEffect(9606) or GetCurrentStateElapsedTime() > 10
    """State 5"""
    if GetEventFlag(4653):
        """State 1,12"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x40()
    elif GetEventFlag(4654):
        """State 2,13"""
        assert t000003000_x38()
    elif GetEventFlag(4655):
        """State 3,15"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x43()
    elif GetEventFlag(4657):
        """State 9,16"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x53()
    elif GetEventFlag(4656):
        """State 4,11"""
        SetWorkValue(1, 0)
        def WhilePaused():
            GiveSpEffectToPlayer(9605)
            SetWorkValueIf((GetWorkValue(1) > 1) == 0 and DoesPlayerHaveSpEffect(9604) == 1, 1, 1)
            RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
            GiveSpEffectToPlayerIf((GetWorkValue(0) > 1) == 1, 9601)
            SetWorkValueIf((GetWorkValue(0) > 1) == 0 and DoesSelfHaveSpEffect(9605) == 1, 0, 1)
            GiveSpEffectToSelfIf((GetWorkValue(1) > 1) == 1, 9602)
            SetWorkValueIf((GetWorkValue(0) > 1) == 1 and DoesSelfHaveSpEffect(9605) == 0, 0, 0)
        def ExitPause():
            SetWorkValue(1, 0)
            SetWorkValue(0, 0)
        assert t000003000_x39()
    elif GetEventFlag(1054539200):
        """State 8,14"""
        t000003000_x42()
        def WhilePaused():
            RequestAnimation(20007, -1)
        Quit()
    else:
        """State 6"""
        pass
    """State 17"""
    return 0

def t000003000_x46():
    """State 0"""
    while True:
        """State 1"""
        assert GetEventFlag(4652)
        """State 2"""
        def ExitPause():
            SetEventFlag(4652, FlagState.Off)
            SetEventFlag(4653, FlagState.Off)
            SetEventFlag(4654, FlagState.Off)
            SetEventFlag(4655, FlagState.Off)
            SetEventFlag(4656, FlagState.Off)
            SetEventFlag(4657, FlagState.Off)
        assert t000003000_x2222() or not GetEventFlag(4652)
        """State 3"""
        assert t000003000_x1()
    """Unused"""
    """State 4"""
    return 0

def t000003000_x47():
    """State 0"""
    Quit()
    """Unused"""
    """State 1"""
    return 0

def t000003000_x48():
    """State 0"""
    if GetEventFlag(10000851):
        """State 7,10"""
        # talk:10010500:"Forgive me. I've been...testing you."
        # talk:10010501:"To see whether or not grace truly does guide you."
        # talk:10010502:"And...whether you are fit to face the challenge that entails."
        # talk:10010503:"It seems my worries were unfounded."
        # talk:10010504:"Torrent had your measure from the very start."
        # talk:10010505:"Whereas I merely pretended."
        # talk:10010506:"There is but one other thing I can do to offer you guidance."
        # talk:10010507:"I can take you to the Roundtable Hold..."
        # talk:10010508:"Gathering place of Tarnished champions, guided by Grace..."
        assert t000003000_x32(text1=10010500, mode5=1)
    else:
        """State 8,11"""
        # talk:10010700:"Forgive me. I've been...testing you."
        # talk:10010701:"To determine if the Elden Ring would truly have you."
        # talk:10010702:"If you had the mettle to endure this long and arduous path."
        # talk:10010703:"It seems my worries were unfounded."
        # talk:10010704:"Torrent had your measure from the very start."
        # talk:10010705:"Whereas I merely pretended."
        # talk:10010706:"There is but one other thing I can do to offer you guidance."
        # talk:10010707:"I can take you to the Roundtable Hold..."
        # talk:10010708:"Gathering place of Tarnished champions, guided by Grace..."
        assert t000003000_x32(text1=10010700, mode5=1)
    """State 9"""
    SetEventFlag(10009655, FlagState.On)
    """State 3"""
    ClearTalkListData()
    ClearPreviousMenuSelection()
    """State 4"""
    # action:21001004:"Go to the Roundtable Hold"
    AddTalkListData(1, 21001004, -1)
    """State 5"""
    OpenConversationChoicesMenu(0)
    assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 1"""
    if GetTalkListEntryResult() == 1:
        """State 2,12"""
        assert t000003000_x78()
    else:
        """State 6"""
        pass
    """State 13"""
    return 0

def t000003000_x49():
    """State 0,6"""
    # talk:10014000:"Hello again, old friend."
    # talk:10014001:"Allow me a moment to converse with you."
    # talk:10014002:"You were unable to enter the Erdtree, no?"
    # talk:10014003:"Prevented by the mantle of barbs."
    # talk:10014004:"The thorns are impenetrable."
    # talk:10014005:"A husk of the Erdtree's being; that spurns all that exists without."
    # talk:10014006:"The only way to stand before the Elden Ring..."
    # talk:10014007:"and become the Elden Lord...is to pass the thorns."
    # talk:10014008:"My purpose serves to aid in that very act."
    # talk:10014009:"So I'd like you to undertake a new journey, with me."
    # talk:10014010:"To the flame of ruin, far above the clouds, upon the snowy mountaintops of the giants."
    # talk:10014011:"Then I can set the Erdtree aflame."
    # talk:10014012:"And guide you. Down the path to becoming Elden Lord."
    assert t000003000_x31(text3=10014000, flag1=11009251, mode6=1)
    """State 1"""
    SetEventFlag(11002745, FlagState.On)
    """State 2"""
    SetEventFlag(11109687, FlagState.On)
    """State 5"""
    SetEventFlag(11009252, FlagState.On)
    """State 7"""
    # lot:100010:Rold Medallion
    call = t000003000_x3(lot1=100010)
    if call.Done() and not GetEventFlag(62528):
        """State 3,8"""
        # action:23241004:"A red mark was made on the map"
        assert t000003000_x4(action1=23241004)
    elif call.Done():
        """State 4"""
        pass
    """State 9"""
    return 0

def t000003000_x50():
    """State 0"""
    if not GetEventFlag(4681):
        """State 7,11"""
        # talk:10001000:"Have you heard of the Finger Maidens?"
        # talk:10001001:"They serve the Two Fingers, offering guidance, and aid, to the Tarnished."
        # talk:10001002:"But you, I am afraid, are maidenless."
        # talk:10001003:"I can play the role of maiden."
        # talk:10001004:"Turning runes into strength."
        # talk:10001005:"To aid you in your search for the Elden Ring."
        # talk:10001006:"You need only take me with you."
        # talk:10001007:"To the foot of the Erdtree."
        assert t000003000_x31(text3=10001000, flag1=1042379201, mode6=1)
    else:
        """State 8,10"""
        # talk:10001300:"Have you reconsidered my offer?"
        assert t000003000_x31(text3=10001300, flag1=1042379201, mode6=1)
    """State 3"""
    ClearTalkListData()
    ClearPreviousMenuSelection()
    """State 4"""
    # action:21001000:"Accept"
    AddTalkListData(1, 21001000, -1)
    # action:21001001:"Refuse"
    AddTalkListData(2, 21001001, -1)
    """State 5"""
    OpenConversationChoicesMenu(0)
    assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 1"""
    if GetTalkListEntryResult() == 1:
        """State 2,12"""
        assert t000003000_x81()
    else:
        """State 6,9"""
        # talk:10001200:"I understand. I'm asking you to put faith in but a stranger."
        # talk:10001201:"Yet I'm certain that we can reach an understanding."
        # talk:10001202:"Summon me by grace if you should reconsider."
        assert t000003000_x31(text3=10001200, flag1=1042372700, mode6=1)
    """State 13"""
    return 0

def t000003000_x51():
    """State 0,2"""
    # talk:10003000:"This tiny golden aura is the grace of the Erdtree."
    # talk:10003001:"This light once shone in the eyes of your Tarnished brethren."
    # talk:10003002:"But now it is all that guides you. Or so I hear."
    # talk:10003003:"You can see them, can't you?"
    # talk:10003004:"The rays of grace, that guide you through your burden."
    assert t000003000_x31(text3=10003000, flag1=1042379203, mode6=1)
    """State 1"""
    SetEventFlag(1042372703, FlagState.On)
    """State 3"""
    return 0

def t000003000_x52():
    """State 0,1"""
    # talk:10003100:"Me?"
    # talk:10003101:"I'm searching."
    # talk:10003102:"For my purpose, given to me by my mother inside the Erdtree, long ago."
    # talk:10003103:"For the reason that I yet live, burned and bodiless."
    # talk:10003104:"There is something for which I must apologise."
    # talk:10003105:"I've acted the Finger Maiden, yet can offer no guidance."
    # talk:10003106:"I am no maiden. My purpose…was long ago lost."
    assert t000003000_x31(text3=10003100, flag1=1042379207, mode6=1)
    """State 2"""
    return 0

def t000003000_x53():
    """State 0,1,2,3"""
    return 0

def t000003000_x54():
    """State 0,1"""
    # talk:10003200:"Upon the cliff, in Castle Stormveil, is a shardbearer."
    # talk:10003201:"A demigod who inherited a fragment of the shattered Elden Ring."
    # talk:10003202:"If the rays of grace signal the castle,"
    # talk:10003203:"then the Elden Ring beckons you."
    # talk:10003204:"As an ally by pact,"
    # talk:10003205:"...I pray that you are fit..."
    # talk:10003206:"To face the challenge presented by the Ring."
    assert t000003000_x31(text3=10003200, flag1=1042379209, mode6=1)
    """State 2"""
    return 0

def t000003000_x55():
    """State 0"""
    if not GetEventFlag(1046389200):
        """State 5,8"""
        # talk:10004000:"Spoken echoes linger here."
        # talk:10004001:"Words of Queen Marika, who vanished long ago."
        # talk:10004002:"If you wish, I will share them with you."
        assert t000003000_x32(text1=10004000, mode5=1)
    else:
        """State 6,7"""
        # talk:10004300:"Spoken echoes of Queen Marika linger here, as well."
        # talk:10004301:"Shall I share them with you?"
        assert t000003000_x32(text1=10004300, mode5=1)
    """State 2"""
    ClearTalkListData()
    ClearPreviousMenuSelection()
    """State 3"""
    # action:21001002:"I'm interested"
    AddTalkListData(1, 21001002, -1)
    # action:21001003:"I'm not interested"
    AddTalkListData(2, 21001003, -1)
    """State 4"""
    OpenConversationChoicesMenu(0)
    assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 1"""
    if GetTalkListEntryResult() == 1:
        """State 9"""
        return 0
    else:
        """State 10"""
        return 1

def t000003000_x56(text3=_, flag1=_, flag2=_):
    """State 0,3"""
    SetEventFlag(flag2, FlagState.On)
    if not GetEventFlag(1046382700):
        """State 4"""
        call = t000003000_x55()
        if call.Get() == 0:
            """State 5"""
            Label('L0')
            assert t000003000_x31(text3=text3, flag1=flag1, mode6=1)
            """State 2"""
            SetEventFlag(1046389200, FlagState.On)
            """State 7"""
            assert t000003000_x76()
        elif call.Done():
            """State 6"""
            # talk:10004200:"Of course. Perhaps there is no need."
            # talk:10004201:"Tell me if you should change your mind."
            assert t000003000_x31(text3=10004200, flag1=1046382700, mode6=1)
    else:
        """State 1"""
        Goto('L0')
    """State 8"""
    return 0

def t000003000_x57():
    """State 0,1"""
    # talk:10011000:"Your seamster, Boc..."
    # talk:10011001:"He is always eager to see your return."
    # talk:10011002:"Please, will you talk to him, when you can?"
    # talk:10011003:"I'm sure he would be much contented."
    assert t000003000_x31(text3=10011000, flag1=1036489251, mode6=1)
    """State 2"""
    return 0

def t000003000_x58():
    """State 0,1"""
    # talk:10011100:"Your seamster, Boc..."
    # talk:10011101:"I see him crying, from time to time."
    # talk:10011102:"I think he misses his mother."
    # talk:10011103:"He wants someone to tell him he's beautiful."
    # talk:10011104:"Does being born of a mother..."
    # talk:10011105:"Mean one behaves in such a manner?"
    assert t000003000_x31(text3=10011100, flag1=1039519251, mode6=1)
    """State 2"""
    return 0

def t000003000_x59():
    """State 0,1"""
    # talk:10013000:"The Erdtree...is close."
    # talk:10013001:"Only a little further till the foot of the Erdtree, and the accord is fulfilled."
    # talk:10013002:"It takes me back."
    # talk:10013003:"I was born at the foot of the Erdtree."
    # talk:10013004:"Where mother gave me my purpose."
    # talk:10013005:"Though now, everything is lost to me."
    # talk:10013006:"I...have to ascertain for myself."
    # talk:10013007:"The reason for which I live, burned and bodiless."
    assert t000003000_x31(text3=10013000, flag1=1037519201, mode6=1)
    """State 2"""
    return 0

def t000003000_x60():
    """State 0,1"""
    # talk:10013100:"My utmost thanks."
    # talk:10013101:"For bringing me to the base of the Erdtree."
    # talk:10013102:"Here, I can govern my own movement."
    # talk:10013103:"And thus, the accord is fulfilled."
    # talk:10013104:"I shall depart to ascertain the purpose I was given."
    # talk:10013105:"Farewell."
    # talk:10013106:"I shall leave Torrent, and the power to turn runes into strength, here with you."
    # talk:10013107:"I wish you luck, in realising your ambition."
    # talk:10013108:"You have fought long and hard."
    # talk:10013109:"I have no doubt you will become Elden Lord. May you take the throne."
    assert t000003000_x31(text3=10013100, flag1=11009260, mode6=1)
    """State 2"""
    return 0

def t000003000_x61():
    """State 0,1"""
    assert t000003000_x78()
    """State 2"""
    return 0

def t000003000_x62():
    """State 0,1"""
    # talk:10014100:"I wish to journey with you once more."
    # talk:10014101:"To the flame of ruin, far above the clouds, upon the snowy mountaintops of the giants."
    # talk:10014102:"Then I can set the Erdtree aflame."
    # talk:10014103:"And guide you. Down the path to becoming Elden Lord."
    assert t000003000_x31(text3=10014100, flag1=11009266, mode6=1)
    """State 2"""
    return 0

def t000003000_x63():
    """State 0,1"""
    # talk:10015000:"Think not, of the kindling."
    # talk:10015001:"I shall see to that."
    # talk:10015002:"All I ask of you is to make the journey."
    # talk:10015003:"To the snowy mountaintops of the giants, far above the clouds."
    # talk:10015004:"I know..."
    # talk:10015005:"I'm asking you to commit a cardinal sin."
    # talk:10015006:"But it must be done to reach the path beyond."
    # talk:10015007:"And that is the path I wish to travel."
    # talk:10015008:"What is your mind?"
    assert t000003000_x31(text3=10015000, flag1=11009271, mode6=1)
    """State 2"""
    return 0

def t000003000_x64():
    """State 0,1"""
    # talk:10016000:"There is something I'd like to say."
    # talk:10016001:"My purpose was given to me by my mother."
    # talk:10016002:"But now, I act of my own volition."
    # talk:10016003:"I have set my heart upon the world that I would have."
    # talk:10016004:"Regardless of my mother's designs."
    # talk:10016005:"I won't allow anyone to speak ill of that."
    # talk:10016006:"Not even you."
    assert t000003000_x31(text3=10016000, flag1=11009276, mode6=1)
    """State 2"""
    return 0

def t000003000_x65():
    """State 0,1"""
    # talk:10017000:"We're almost there."
    # talk:10017001:"The flame of ruin lies just ahead."
    # talk:10017002:"I'm glad it was you I travelled with."
    # talk:10017003:"I must tender my thanks to Torrent, too."
    # talk:10017004:"Thank you, Torrent."
    # talk:10017005:"Please continue to lend your aid. Till the end."
    assert t000003000_x31(text3=10017000, flag1=1054539211, mode6=1)
    """State 2"""
    return 0

def t000003000_x66():
    """State 0"""
    if not GetEventFlag(1054539216):
        """State 7"""
        # talk:10017100:"I have long observed the Lands Between."
        # talk:10017101:"This world is in dire need of repair..."
        # talk:10017102:"and Death...indiscriminate..."
        # talk:10017103:"Are you prepared..."
        # talk:10017104:"To commit a cardinal sin?"
        assert t000003000_x31(text3=10017100, flag1=1054539216, mode6=1)
    else:
        """State 8"""
        # talk:10017400:"Are you ready to commit a cardinal sin?"
        assert t000003000_x31(text3=10017400, flag1=1054539216, mode6=1)
    """State 3"""
    ClearTalkListData()
    ClearPreviousMenuSelection()
    """State 4"""
    # action:21001005:"I'm ready"
    AddTalkListData(1, 21001005, -1)
    # action:21001006:"I'd like you to wait"
    AddTalkListData(2, 21001006, -1)
    """State 5"""
    OpenConversationChoicesMenu(0)
    assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    """State 1"""
    if GetTalkListEntryResult() == 1:
        """State 2,9"""
        # talk:10017200:"Very well."
        # talk:10017201:"Let my hand rest upon you, for but a moment."
        assert t000003000_x32(text1=10017200, mode5=1)
        """State 11"""
        t000003000_x42()
        def WhilePaused():
            RequestAnimation(20007, -1)
        Quit()
    else:
        """State 6,10"""
        # talk:10017300:"Very well."
        # talk:10017301:"Tell me, when you are fully prepared."
        assert t000003000_x32(text1=10017300, mode5=1)
        """State 12"""
        return 0

def t000003000_x67():
    """State 0,2"""
    # talk:10018000:"If you intend to claim the frenzied flame,"
    # talk:10018001:"I ask that you cease."
    # talk:10018002:"It is not to be meddled with."
    # talk:10018003:"It is chaos, devouring life and thought unending."
    # talk:10018004:"However ruined this world has become, however mired in torment and despair..."
    # talk:10018005:"Life endures. Births continue."
    # talk:10018006:"There is beauty in that, is there not?"
    # talk:10018007:"If you would become Lord, do not deny this notion."
    # talk:10018008:"Please, leave the frenzied flame alone."
    assert t000003000_x31(text3=10018000, flag1=35009351, mode6=1)
    """State 1"""
    SetEventFlag(35002732, FlagState.On)
    """State 3"""
    return 0

def t000003000_x68():
    """State 0,2"""
    # talk:10018500:"I ask you, one more time."
    # talk:10018501:"Please, seek not the frenzied flame."
    # talk:10018502:"As one who strives to become a Lord,"
    # talk:10018503:"deny not the lives, the new births of this world."
    # talk:10018504:"Those who would are not fit to be called Lord."
    # talk:10018505:"When the land they preside over is lifeless."
    assert t000003000_x31(text3=10018500, flag1=35009353, mode6=1)
    """State 1"""
    SetEventFlag(35002733, FlagState.On)
    """State 3"""
    return 0

def t000003000_x69():
    """State 0"""
    if GetEventFlag(35009356):
        """State 1,7"""
        # talk:10018100:"I shall see to the kindling."
        # talk:10018101:"It is a purpose which I choose to fulfil."
        # talk:10018102:"So, please... Leave the frenzied flame alone."
        assert t000003000_x32(text1=10018100, mode5=1)
    elif GetEventFlag(35009357):
        """State 2,8"""
        # talk:10018200:"The frenzied flame is not to be meddled with."
        # talk:10018201:"It is chaos, devouring life and thought unending."
        # talk:10018202:"So, please... Leave the frenzied flame alone."
        assert t000003000_x32(text1=10018200, mode5=1)
    elif GetEventFlag(1049539207):
        """State 3,5"""
        # talk:10018100:"I shall see to the kindling."
        # talk:10018101:"It is a purpose which I choose to fulfil."
        # talk:10018102:"So, please... Leave the frenzied flame alone."
        assert t000003000_x31(text3=10018100, flag1=35009356, mode6=1)
    else:
        """State 4,6"""
        # talk:10018200:"The frenzied flame is not to be meddled with."
        # talk:10018201:"It is chaos, devouring life and thought unending."
        # talk:10018202:"So, please... Leave the frenzied flame alone."
        assert t000003000_x31(text3=10018200, flag1=35009357, mode6=1)
    """State 9"""
    return 0

def t000003000_x70():
    """State 0,1"""
    # talk:10018600:"Please, put a stop to this madness."
    # talk:10018601:"The Lord of Frenzied Flame is no lord at all."
    # talk:10018602:"When the land they preside over is lifeless."
    assert t000003000_x31(text3=10018600, flag1=35009359, mode6=1)
    """State 2"""
    return 0

def t000003000_x71():
    """State 0"""
    # eventflag:400001:lot:100010:Rold Medallion
    if not GetEventFlag(400001):
        """State 2,4"""
        # talk:10019000:"You...have inherited the frenzied flame."
        # talk:10019001:"A pity. You are no longer fit."
        # talk:10019002:"Our accord ends here."
        # talk:10019003:"But remember..."
        # talk:10019004:"Should you rise, as the Lord of Chaos,"
        # talk:10019005:"I will kill you, as sure as night follows day."
        # talk:10019006:"Such is my duty, for allowing you the strength of runes."
        # talk:10019007:"Goodbye, my companion."
        # talk:10019008:"Goodbye, Torrent..."
        assert t000003000_x32(text1=10019000, mode5=1)
    else:
        """State 3,5"""
        # talk:10019100:"You...have inherited the frenzied flame."
        # talk:10019101:"A pity. You are no longer fit."
        # talk:10019102:"Our journey together ends here."
        # talk:10019103:"And remember..."
        # talk:10019104:"Should you rise as the Lord of Chaos,"
        # talk:10019105:"I will kill you, as sure as night follows day."
        # talk:10019106:"Such is my duty, for allowing you the strength of runes."
        # talk:10019107:"Goodbye, my companion."
        # talk:10019108:"Goodbye, Torrent..."
        assert t000003000_x32(text1=10019100, mode5=1)
    """State 1"""
    SetEventFlag(35009360, FlagState.On)
    """State 6"""
    return 0

def t000003000_x72():
    """State 0"""
    if (GetEventFlag(10000851) and not GetEventFlag(10009655) and not DoesPlayerHaveSpEffect(4270) and not DoesPlayerHaveSpEffect(4271)
        and not DoesPlayerHaveSpEffect(4272) and not DoesPlayerHaveSpEffect(4280) and not DoesPlayerHaveSpEffect(4282)
        and not DoesPlayerHaveSpEffect(4286)):
        """State 2"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x48()
    elif ((GetEventFlag(3062) or GetEventFlag(3063) or GetEventFlag(3064) or GetEventFlag(3065)) and not GetEventFlag(10009655)
          and not DoesPlayerHaveSpEffect(4270) and not DoesPlayerHaveSpEffect(4271) and not DoesPlayerHaveSpEffect(4272)
          and not DoesPlayerHaveSpEffect(4280) and not DoesPlayerHaveSpEffect(4282) and not DoesPlayerHaveSpEffect(4286)):
        """State 4"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x48()
    # eventflag:400001:lot:100010:Rold Medallion
    elif (not GetEventFlag(11009260) and not GetEventFlag(400001) and (GetEventFlag(11002741) or GetEventFlag(11002742)
          or GetEventFlag(11002743) or GetEventFlag(11002744))):
        """State 5"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x60()
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(9104) and not GetEventFlag(400001):
        """State 3"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x49()
    else:
        """State 1"""
        pass
    """State 6"""
    return 0

def t000003000_x73():
    """State 0,1"""
    assert t000003000_x41()
    """State 2"""
    return 0

def t000003000_x74():
    """State 0"""
    # eventflag:400001:lot:100010:Rold Medallion
    if GetEventFlag(9104) and not GetEventFlag(400001):
        """State 2"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x49()
    else:
        """State 1"""
        pass
    """State 3"""
    return 0

def t000003000_x75():
    """State 0,1"""
    assert t000003000_x71()
    """State 2"""
    return 0

def t000003000_x76():
    """State 0"""
    if GetEventFlag(1043509200):
        """State 1"""
        if not GetEventFlag(60846):
            """State 3"""
            # gesture:104:Outer Order
            AcquireGesture(104)
            SetEventFlag(60846, FlagState.On)
            assert GetCurrentStateElapsedTime() > 1 and not IsMenuOpen(MenuType.Bonfire)
        else:
            """State 4"""
            pass
    else:
        """State 2"""
        pass
    """State 5"""
    return 0

def t000003000_x77():
    """State 0,2"""
    # talk:10010600:"Very well."
    # talk:10010601:"Let my hand rest upon you, for but a moment."
    assert t000003000_x79(text2=10010600, mode1=1) and (DoesPlayerHaveSpEffect(9601) or CheckSpecificPersonTalkHasEnded(0))
    """State 1"""
    RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    def WhilePaused():
        RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    def ExitPause():
        RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    assert t000003000_x80()
    """State 3"""
    return 0

def t000003000_x78():
    """State 0,1"""
    SetWorkValue(0, 0)
    SetWorkValue(1, 0)
    def WhilePaused():
        SetWorkValueIf((GetWorkValue(1) > 1) == 0 and DoesPlayerHaveSpEffect(9604) == 1, 1, 1)
        SetWorkValueIf((GetWorkValue(0) > 1) == 0 and DoesSelfHaveSpEffect(9605) == 1, 0, 1)
        GiveSpEffectToPlayer(9605)
        GiveSpEffectToPlayerIf((GetWorkValue(0) > 1) == 1, 9601)
        GiveSpEffectToSelfIf((GetWorkValue(1) > 1) == 1, 9602)
    def ExitPause():
        SetWorkValue(0, 0)
        SetWorkValue(1, 0)
    assert t000003000_x77()
    """State 2"""
    return 0

def t000003000_x79(text2=10010600, mode1=1):
    """State 0,4"""
    assert t000003000_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    # talk:10010600:"Very well."
    # talk:10010601:"Let my hand rest upon you, for but a moment."
    TalkToPlayer(text2, -1, -1, 0)
    """State 3"""
    if mode1 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t000003000_x80():
    """State 0,3"""
    RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    def WhilePaused():
        RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    def ExitPause():
        RequestAnimationIf((GetWorkValue(1) > 1) == 1, 20002, -1)
    assert DoesPlayerHaveSpEffect(9601)
    """State 4"""
    assert GetCurrentStateElapsedTime() > 11 and CheckSpecificPersonTalkHasEnded(0)
    """State 2,1"""
    SetEventFlag(11109786, FlagState.On)
    SetEventFlag(104, FlagState.On)
    """State 5"""
    return 0

def t000003000_x81():
    """State 0"""
    # goods:130:Spectral Steed Whistle
    if ComparePlayerInventoryNumber(ItemType.Goods, 130, CompareType.Equal, 0, False):
        """State 1,3"""
        # talk:10001100:"Then it's settled."
        # talk:10001101:"Summon me by grace to turn runes into strength."
        # talk:10001102:"Ahh, another matter."
        # talk:10001103:"I bequeath to you this ring."
        assert t000003000_x31(text3=10001100, flag1=4680, mode6=1)
        """State 4"""
        # lot:100000:Spectral Steed Whistle
        assert t000003000_x3(lot1=100000)
        """State 5"""
        # talk:10001105:"Use it to traverse great distances."
        # talk:10001106:"It will summon a spectral steed named Torrent."
        # talk:10001107:"Torrent has chosen you."
        # talk:10001108:"Treat him with respect."
        assert t000003000_x32(text1=10001105, mode5=1)
    else:
        """State 2,7"""
        # talk:10001110:"Then it's settled."
        # talk:10001111:"Summon me by grace to turn runes into strength."
        # talk:10001112:"Ahh, another matter."
        # talk:10001113:"Torrent has chosen you."
        # talk:10001114:"Treat him with respect."
        assert t000003000_x31(text3=10001110, flag1=4680, mode6=1)
        """State 6"""
        # lot:100000:Spectral Steed Whistle
        assert t000003000_x3(lot1=100000)
    """State 8"""
    return 0

def t000003000_x2222():
    """State 0,7"""
    assert not GetEventFlag(9001)
    """State 10"""
    assert not DoesSelfHaveSpEffect(9606) or GetCurrentStateElapsedTime() > 10
    """State 5"""
    if GetEventFlag(1062265210):
        """State 18"""
        assert t000003000_x2227()
        """State 19"""
        return 0
    elif GetEventFlag(4653):
        """State 1,12"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x40()
    elif GetEventFlag(4654):
        """State 2,13"""
        assert t000003000_x38()
    elif GetEventFlag(4655):
        """State 3,15"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x43()
    elif GetEventFlag(4657):
        """State 9,16"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        assert t000003000_x53()
    elif GetEventFlag(4656):
        """State 4,11"""
        SetWorkValue(1, 0)
        def WhilePaused():
            GiveSpEffectToPlayer(9605)
            SetWorkValueIf((GetWorkValue(1) > 1) == 0 and DoesPlayerHaveSpEffect(9604) == 1, 1, 1)
            RequestAnimationIf(GetWorkValue(1) > 1, 20002, -1)
            GiveSpEffectToPlayerIf(GetWorkValue(0) > 1, 9601)
            SetWorkValueIf((GetWorkValue(0) > 1) == 0 and DoesSelfHaveSpEffect(9605) == 1, 0, 1)
            GiveSpEffectToSelfIf(GetWorkValue(1) > 1, 9602)
            SetWorkValueIf(GetWorkValue(0) > 1 and DoesSelfHaveSpEffect(9605) == 0, 0, 0)
        def ExitPause():
            SetWorkValue(1, 0)
            SetWorkValue(0, 0)
        assert t000003000_x39()
    elif GetEventFlag(1054539200):
        """State 8,14"""
        t000003000_x42()
        def WhilePaused():
            RequestAnimation(20007, -1)
        Quit()
    else:
        """State 6"""
        pass
    """State 17"""
    return 0

def t000003000_x2224(text1=_):
    """State 0"""
    assert t000003000_x2225()
    """State 1"""
    assert t000003000_x32(text1=text1, mode5=1)
    """State 2"""
    return 0

def t000003000_x2225():
    """State 0"""
    SetEventFlag(1062265200, FlagState.On)
    SetEventFlag(1062265201, FlagState.On)
    SetEventFlag(1062265202, FlagState.Off)
    SetEventFlag(1062265203, FlagState.Off)
    SetEventFlag(1062265204, FlagState.Off)
    SetEventFlag(1062265210, FlagState.Off)
    return 0

def t000003000_x2227():
    """State 0"""
    if True:
        """State 1"""
        def WhilePaused():
            RequestAnimation(20004, -1)
        if (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
            * 2 + GetEventFlag(1062265200) * 1 == 0):
            """State 2"""
            # talk:10611300:"Oh, is that so?"
            # talk:10611301:"Thou wouldst render me aid, is that thy proposal?"
            # talk:10611302:"Affording thyself opportunity to grope about for the cursemark's location, no doubt?"
            # talk:10611303:"..."
            # talk:10611304:"Very well..."
            # talk:10611305:"There's nothing wrong with a well-laid scheme."
            # talk:10611306:"What's more, if my past and past wounds beckon to thee,"
            # talk:10611307:"I am curious enough to see what thy destiny portends..."
            # talk:10611308:"I'll allow it. Enter my service."
            # talk:10611309:"And good hunting to thee."
            assert t000003000_x31(text3=10611300, flag1=4651, mode6=1)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 1):
            """State 3"""
            # talk:10003100:"Me?"
            # talk:10003101:"I'm searching."
            # talk:10003102:"For my purpose, given to me by my mother inside the Erdtree, long ago."
            # talk:10003103:"For the reason that I yet live, burned and bodiless."
            # talk:10003104:"There is something for which I must apologise."
            # talk:10003105:"I've acted the Finger Maiden, yet can offer no guidance."
            # talk:10003106:"I am no maiden. My purpose…was long ago lost."
            assert t000003000_x2224(text1=10003100)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 12):
            """State 4"""
            # talk:10010100:"In Marika's own words."
            # talk:10010101:"Hear me, Demigods. My children beloved."
            # talk:10010102:"Make of thyselves that which ye desire. Be it a Lord. Be it a God."
            # talk:10010103:"But should ye fail to become aught at all, ye will be forsaken."
            # talk:10010104:"Amounting only to sacrifices..."
            assert t000003000_x2224(text1=10010100)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 3):
            """State 5"""
            # talk:10010200:"In Marika's own words."
            # talk:10010201:"O Radagon, leal hound of the Golden Order."
            # talk:10010202:"Thou'rt yet to become me. Thou'rt yet to become a god."
            # talk:10010203:"Let us be shattered, both. Mine other self."
            assert t000003000_x2224(text1=10010200)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 4):
            """State 6"""
            # talk:10010300:"In Marika's own words."
            # talk:10010301:"I declare mine intent, to search the depths of the Golden Order."
            # talk:10010302:"Through understanding of the proper way, our faith, our grace, is increased."
            # talk:10010303:"Those blissful early days of blind belief are long past."
            # talk:10010304:"My comrades; why must ye falter?"
            assert t000003000_x2224(text1=10010300)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 5):
            """State 7"""
            # talk:10010400:"In Marika's own words."
            # talk:10010401:"Hark, brave warriors. Hark, my lord Godfrey. We commend your deeds."
            # talk:10010402:"Guidance hath delivered ye through each ordeal, to the place ye stand."
            # talk:10010403:"Put the Giants to the sword, and confine the flame atop the mount."
            # talk:10010404:"Let a new epoch begin. An epoch glistening with life."
            # talk:10010405:"Brandish the Elden Ring, for the Age of the Erdtree!"
            assert t000003000_x2224(text1=10010400)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 6):
            """State 8"""
            # talk:10004100:"Very well. In Marika's own words."
            # talk:10004101:"My Lord, and thy warriors. I divest each of thee of thy grace."
            # talk:10004102:"With thine eyes dimmed, ye will be driven from the Lands Between."
            # talk:10004103:"Ye will wage war in a land afar, where ye will live, and die."
            # talk:10004104:"Well? Perhaps that might serve you in lieu of a maiden's guidance."
            assert t000003000_x2224(text1=10004100)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 7):
            """State 9"""
            # talk:10004400:"In Marika's own words."
            # talk:10004401:"Then, after thy death, I will give back what I once claimed."
            # talk:10004402:"Return to the Lands Between, wage war, and brandish the Elden Ring."
            # talk:10004403:"Grow strong in the face of death. Warriors of my lord. Lord Godfrey."
            assert t000003000_x2224(text1=10004400)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 8):
            """State 10"""
            # talk:10004500:"In Marika's own words."
            # talk:10004501:"The Erdtree governs all. The choice is thine."
            # talk:10004502:"Become one with the Order. Or divest thyself of it."
            # talk:10004503:"To wallow at the fringes; a powerless upstart."
            assert t000003000_x2224(text1=10004500)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 9):
            """State 11"""
            # talk:10012000:"..."
            # talk:10012001:"Is there...another person inside of you?"
            # talk:10012002:"Did you...want that to happen?"
            # talk:10012003:"I sense no malice. Do as you think best."
            # talk:10012004:"Hello, other you."
            # talk:10012005:"I am Melina, and I have an accord with this person."
            # talk:10012006:"We might be together for some time."
            # talk:10012007:"Pleased to meet you."
            assert t000003000_x2224(text1=10012000)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 10):
            """State 12"""
            # talk:10012100:"..."
            # talk:10012101:"Is there...another person inside of you?"
            # talk:10012102:"Did you...want that to happen?"
            # talk:10012103:"I sense no malice. Do as you think best."
            # talk:10012104:"Hello, other you."
            # talk:10012105:"I am Melina, and I am travelling with this person."
            # talk:10012106:"We might be together for some time."
            # talk:10012107:"Pleased to meet you."
            assert t000003000_x2224(text1=10012100)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 11):
            """State 13"""
            # talk:10015000:"Think not, of the kindling."
            # talk:10015001:"I shall see to that."
            # talk:10015002:"All I ask of you is to make the journey."
            # talk:10015003:"To the snowy mountaintops of the giants, far above the clouds."
            # talk:10015004:"I know..."
            # talk:10015005:"I'm asking you to commit a cardinal sin."
            # talk:10015006:"But it must be done to reach the path beyond."
            # talk:10015007:"And that is the path I wish to travel."
            # talk:10015008:"What is your mind?"
            assert t000003000_x2224(text1=10015000)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 2):
            """State 14"""
            # talk:10003000:"This tiny golden aura is the grace of the Erdtree."
            # talk:10003001:"This light once shone in the eyes of your Tarnished brethren."
            # talk:10003002:"But now it is all that guides you. Or so I hear."
            # talk:10003003:"You can see them, can't you?"
            # talk:10003004:"The rays of grace, that guide you through your burden."
            assert t000003000_x2224(text1=10003000)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 13):
            """State 15"""
            # talk:10016000:"There is something I'd like to say."
            # talk:10016001:"My purpose was given to me by my mother."
            # talk:10016002:"But now, I act of my own volition."
            # talk:10016003:"I have set my heart upon the world that I would have."
            # talk:10016004:"Regardless of my mother's designs."
            # talk:10016005:"I won't allow anyone to speak ill of that."
            # talk:10016006:"Not even you."
            assert t000003000_x2224(text1=10016000)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 14):
            """State 16"""
            # talk:10018000:"If you intend to claim the frenzied flame,"
            # talk:10018001:"I ask that you cease."
            # talk:10018002:"It is not to be meddled with."
            # talk:10018003:"It is chaos, devouring life and thought unending."
            # talk:10018004:"However ruined this world has become, however mired in torment and despair..."
            # talk:10018005:"Life endures. Births continue."
            # talk:10018006:"There is beauty in that, is there not?"
            # talk:10018007:"If you would become Lord, do not deny this notion."
            # talk:10018008:"Please, leave the frenzied flame alone."
            assert t000003000_x2224(text1=10018000)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 15):
            """State 17"""
            # talk:10018100:"I shall see to the kindling."
            # talk:10018101:"It is a purpose which I choose to fulfil."
            # talk:10018102:"So, please... Leave the frenzied flame alone."
            assert t000003000_x2224(text1=10018100)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 16):
            """State 18"""
            # talk:10018500:"I ask you, one more time."
            # talk:10018501:"Please, seek not the frenzied flame."
            # talk:10018502:"As one who strives to become a Lord,"
            # talk:10018503:"deny not the lives, the new births of this world."
            # talk:10018504:"Those who would are not fit to be called Lord."
            # talk:10018505:"When the land they preside over is lifeless."
            assert t000003000_x2224(text1=10018500)
        elif (GetEventFlag(1062265204) * 16 + GetEventFlag(1062265203) * 8 + GetEventFlag(1062265202) * 4 + GetEventFlag(1062265201)
              * 2 + GetEventFlag(1062265200) * 1 == 17):
            """State 19"""
            # talk:10018600:"Please, put a stop to this madness."
            # talk:10018601:"The Lord of Frenzied Flame is no lord at all."
            # talk:10018602:"When the land they preside over is lifeless."
            assert t000003000_x2224(text1=10018600)
        else:
            """State 20"""
            # talk:10603000:"Let us speak of the past, a while."
            # talk:10603001:"I was once an Empyrean."
            # talk:10603002:"Of the demigods, only I, Miquella, and Malenia could claim that title."
            # talk:10603003:"Each of us was chosen by our own Two Fingers, as a candidate to succeed Queen Marika, to become the new god of the coming age."
            # talk:10603004:"But I would not acquiesce to the Two Fingers."
            # talk:10603005:"I stole the Rune of Death, slew mine own Empyrean flesh, casting it away."
            # talk:10603006:"I would not be controlled by that thing."
            # talk:10603007:"The Two Fingers and I have been cursing each other ever since..."
            # talk:10603008:"And the Baleful Shadows...are their assassins."
            assert t000003000_x31(text3=10603000, flag1=4651, mode6=1)
    else:
        """State 21"""
        assert t000003000_x2225()
    """State 22"""
    return 0

