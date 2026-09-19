# -*- coding: utf-8 -*-
def t213001110_1():
    """State 0,1"""
    t213001110_x6(flag1=3223, flag2=3221, flag3=3222, val1=5, val2=10, val3=12, val4=30, val5=30, actionbutton1=6210,
                  flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                  mode1=1, mode2=1)
    Quit()

def t213001110_1000():
    """State 0,2,3"""
    assert t213001110_x36()
    """State 1"""
    EndMachine(1000)
    Quit()

def t213001110_2000():
    """State 0,2,3"""
    assert t213001110_x37()
    """State 1"""
    EndMachine(2000)
    Quit()

def t213001110_x0(actionbutton1=6210, flag5=6001, flag10=6000, flag11=6000, flag12=6000, flag13=6000, flag4=6000):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 3"""
        assert (GetEventFlag(flag5) or GetEventFlag(flag10) or GetEventFlag(flag11) or GetEventFlag(flag12) or
                GetEventFlag(flag13))
        """State 4"""
        assert not GetEventFlag(flag4)
        """State 2"""
        if (GetEventFlag(flag4) or not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead()
            and not IsCharacterDisabled()) or (not GetEventFlag(flag5) and not GetEventFlag(flag10) and not GetEventFlag(flag11)
            and not GetEventFlag(flag12) and not GetEventFlag(flag13))):
            pass
        elif CheckActionButtonArea(actionbutton1):
            break
    """State 5"""
    return 0

def t213001110_x1():
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

def t213001110_x2():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ForceCloseGenericDialog()
    ForceCloseMenu()
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t213001110_x3(action1=22131010):
    """State 0,1"""
    OpenGenericDialog(DialogBoxType.CenterBottom1, action1, DialogResult.Left, DialogBoxStyle.OrnateNoOptions, 1)
    assert not CheckSpecificPersonGenericDialogIsOpen(0)
    """State 2"""
    return 0

def t213001110_x4(val2=10, val3=12):
    """State 0,1"""
    assert GetDistanceToPlayer() < val2 and GetCurrentStateElapsedFrames() > 1
    """State 2"""
    if PlayerDiedFromFallInstantly() == False and PlayerDiedFromFallDamage() == False:
        """State 3,6"""
        call = t213001110_x20()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 5"""
            assert t213001110_x1()
    else:
        """State 4,7"""
        call = t213001110_x33()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 8"""
            assert t213001110_x1()
    """State 9"""
    return 0

def t213001110_x5():
    """State 0,1"""
    assert t213001110_x1()
    """State 2"""
    return 0

def t213001110_x6(flag1=3223, flag2=3221, flag3=3222, val1=5, val2=10, val3=12, val4=30, val5=30, actionbutton1=6210,
                  flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                  mode1=1, mode2=1):
    """State 0"""
    assert GetCurrentStateElapsedTime() > 1.5
    while True:
        """State 2"""
        call = t213001110_x23(flag1=flag1, flag2=flag2, flag3=flag3, val1=val1, val2=val2, val3=val3, val4=val4,
                              val5=val5, actionbutton1=actionbutton1, flag4=flag4, flag5=flag5, flag6=flag6, flag7=flag7,
                              flag8=flag8, z1=z1, z2=z2, z3=z3, z4=z4, mode1=mode1, mode2=mode2)
        assert IsClientPlayer()
        """State 1"""
        call = t213001110_x22()
        assert not IsClientPlayer()
    """Unused"""
    """State 3"""
    return 0

def t213001110_x7(val1=5, val2=10, val3=12, val4=30, val5=30, actionbutton1=6210, flag4=6000, flag5=6001, flag6=6000,
                  flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000, mode1=1, mode2=1):
    """State 0"""
    while True:
        """State 2"""
        call = t213001110_x10(actionbutton1=actionbutton1, flag4=flag4, flag5=flag5, z2=z2, z3=z3, z4=z4)
        def WhilePaused():
            RemoveMyAggroIf(IsAttackedBySomeone() == 1 and (DoesSelfHaveSpEffect(9626) == 1 and DoesSelfHaveSpEffect(9627) == 1))
            GiveSpEffectToPlayerIf(CheckSpecificPersonTalkHasEnded(0) == 0, 9640)
        if call.Done():
            """State 4"""
            Label('L0')
            ChangeCamera(1000000)
            call = t213001110_x14(val1=val1, z1=z1)
            def WhilePaused():
                ChangeCameraIf(GetDistanceToPlayer() > 2.5, -1)
                RemoveMyAggroIf(IsAttackedBySomeone() == 1 and (DoesSelfHaveSpEffect(9626) == 1 and DoesSelfHaveSpEffect(9627) == 1))
                GiveSpEffectToPlayer(9640)
                SetLookAtEntityForTalkIf(1 == (mode1 == 1), -1, 0)
                SetLookAtEntityForTalkIf(1 == (mode2 == 1), 0, -1)
            def ExitPause():
                ChangeCamera(-1)
            if call.Done():
                continue
            elif IsAttackedBySomeone():
                pass
        elif IsAttackedBySomeone() and not DoesSelfHaveSpEffect(9626) and not DoesSelfHaveSpEffect(9627):
            pass
        elif GetEventFlag(flag8):
            Goto('L0')
        elif GetEventFlag(flag6) and not GetEventFlag(flag7) and GetDistanceToPlayer() < val4:
            """State 5"""
            call = t213001110_x16(val5=val5)
            if call.Done():
                continue
            elif IsAttackedBySomeone():
                pass
        elif ((GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6) and not CheckSpecificPersonTalkHasEnded(0)
              and not DoesSelfHaveSpEffect(9625)):
            """State 6"""
            assert t213001110_x27() and CheckSpecificPersonTalkHasEnded(0)
            continue
        elif GetEventFlag(9000):
            """State 1"""
            assert not GetEventFlag(9000)
            continue
        """State 3"""
        def ExitPause():
            RemoveMyAggro()
        assert t213001110_x12(val2=val2, val3=val3)
    """Unused"""
    """State 7"""
    return 0

def t213001110_x8(val2=10, val3=12):
    """State 0,1"""
    call = t213001110_x18(val2=val2, val3=val3)
    assert IsPlayerDead()
    """State 2"""
    t213001110_x4(val2=val2, val3=val3)
    Quit()
    """Unused"""
    """State 3"""
    return 0

def t213001110_x9(flag1=3223, val2=10, val3=12):
    """State 0,8"""
    assert t213001110_x35()
    """State 1"""
    if GetEventFlag(flag1):
        """State 2"""
        pass
    else:
        """State 3"""
        if GetDistanceToPlayer() < val2:
            """State 4,6"""
            call = t213001110_x21()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t213001110_x1()
        else:
            """State 5"""
            pass
    """State 9"""
    return 0

def t213001110_x10(actionbutton1=6210, flag4=6000, flag5=6001, z2=1000000, z3=1000000, z4=1000000):
    """State 0,1"""
    call = t213001110_x11(machine1=2000, val6=2000)
    if call.Get() == 1:
        """State 2"""
        assert (t213001110_x0(actionbutton1=actionbutton1, flag5=flag5, flag10=6000, flag11=6000, flag12=6000,
                flag13=6000, flag4=flag4))
    elif call.Done():
        pass
    """State 3"""
    return 0

def t213001110_x11(machine1=_, val6=_):
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

def t213001110_x12(val2=10, val3=12):
    """State 0"""
    assert GetCurrentStateElapsedFrames() > 1
    """State 5"""
    assert t213001110_x1()
    """State 3"""
    if GetDistanceToPlayer() < val2:
        """State 1"""
        if IsPlayerAttacking():
            """State 6"""
            call = t213001110_x13()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t213001110_x28()
        else:
            """State 4"""
            pass
    else:
        """State 2"""
        pass
    """State 8"""
    return 0

def t213001110_x13():
    """State 0,1"""
    assert t213001110_x11(machine1=1101, val6=1101)
    """State 2"""
    return 0

def t213001110_x14(val1=5, z1=1):
    """State 0,2"""
    assert t213001110_x24()
    """State 1"""
    call = t213001110_x15()
    if call.Done():
        pass
    elif (GetDistanceToPlayer() > val1 or GetTalkInterruptReason() == 6) and not DoesSelfHaveSpEffect(9625):
        """State 3"""
        assert t213001110_x26()
    """State 4"""
    return 0

def t213001110_x15():
    """State 0,1"""
    assert t213001110_x11(machine1=1000, val6=1000)
    """State 2"""
    return 0

def t213001110_x16(val5=30):
    """State 0,1"""
    call = t213001110_x17()
    if call.Done():
        pass
    elif GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6:
        """State 2"""
        assert t213001110_x27()
    """State 3"""
    return 0

def t213001110_x17():
    """State 0,1"""
    assert t213001110_x11(machine1=1100, val6=1100)
    """State 2"""
    return 0

def t213001110_x18(val2=10, val3=12):
    """State 0,5"""
    assert t213001110_x35()
    """State 2"""
    assert not GetEventFlag(3000)
    while True:
        """State 1"""
        assert GetDistanceToPlayer() < val2
        """State 3"""
        call = t213001110_x19()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 4"""
            assert t213001110_x29()
    """Unused"""
    """State 6"""
    return 0

def t213001110_x19():
    """State 0,2"""
    call = t213001110_x11(machine1=1102, val6=1102)
    if call.Get() == 1:
        """State 1"""
        Quit()
    elif call.Done():
        """State 3"""
        return 0

def t213001110_x20():
    """State 0,1"""
    assert t213001110_x11(machine1=1001, val6=1001)
    """State 2"""
    return 0

def t213001110_x21():
    """State 0,1"""
    assert t213001110_x11(machine1=1103, val6=1103)
    """State 2"""
    return 0

def t213001110_x22():
    """State 0"""
    Quit()
    """Unused"""
    """State 1"""
    return 0

def t213001110_x23(flag1=3223, flag2=3221, flag3=3222, val1=5, val2=10, val3=12, val4=30, val5=30, actionbutton1=6210,
                   flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                   mode1=1, mode2=1):
    """State 0"""
    while True:
        """State 1"""
        RemoveMyAggro()
        call = t213001110_x7(val1=val1, val2=val2, val3=val3, val4=val4, val5=val5, actionbutton1=actionbutton1,
                             flag4=flag4, flag5=flag5, flag6=flag6, flag7=flag7, flag8=flag8, z1=z1, z2=z2, z3=z3,
                             z4=z4, mode1=mode1, mode2=mode2)
        if CheckSelfDeath() or GetEventFlag(flag1):
            """State 3"""
            Label('L0')
            call = t213001110_x9(flag1=flag1, val2=val2, val3=val3)
            if not CheckSelfDeath() and not GetEventFlag(flag1):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(flag2) or GetEventFlag(flag3):
            """State 2"""
            call = t213001110_x8(val2=val2, val3=val3)
            if CheckSelfDeath() or GetEventFlag(flag1):
                Goto('L0')
            elif not GetEventFlag(flag2) and not GetEventFlag(flag3):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(9000) or (IsPlayerDead() and not DoesSelfHaveSpEffect(9649)):
            pass
        """State 4"""
        assert t213001110_x34() and (not GetEventFlag(9000) and not IsPlayerDead())
    """Unused"""
    """State 5"""
    return 0

def t213001110_x24():
    """State 0,1"""
    assert t213001110_x25()
    """State 2"""
    return 0

def t213001110_x25():
    """State 0,1"""
    assert t213001110_x11(machine1=1104, val6=1104)
    """State 2"""
    return 0

def t213001110_x26():
    """State 0,1"""
    call = t213001110_x11(machine1=1201, val6=1201)
    if call.Get() == 1:
        """State 2"""
        assert t213001110_x5()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t213001110_x27():
    """State 0,1"""
    call = t213001110_x11(machine1=1300, val6=1300)
    if call.Get() == 1:
        """State 2"""
        assert t213001110_x5()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t213001110_x28():
    """State 0,1"""
    call = t213001110_x11(machine1=1301, val6=1301)
    if call.Get() == 1:
        """State 2"""
        assert t213001110_x5()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t213001110_x29():
    """State 0,1"""
    call = t213001110_x11(machine1=1302, val6=1302)
    if call.Get() == 1:
        """State 2"""
        assert t213001110_x5()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t213001110_x30(text2=_, mode4=1):
    """State 0,4"""
    assert t213001110_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text2, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 3"""
    if mode4 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t213001110_x31(text1=_, flag9=_, mode3=1):
    """State 0,5"""
    assert t213001110_x32() and CheckSpecificPersonTalkHasEnded(0)
    """State 2"""
    SetEventFlag(flag9, FlagState.On)
    """State 1"""
    TalkToPlayer(text1, -1, -1, 1)
    """State 4"""
    if mode3 == 0:
        pass
    else:
        """State 3"""
        ReportConversationEndToHavokBehavior()
    """State 6"""
    return 0

def t213001110_x32():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t213001110_x33():
    """State 0,1"""
    assert t213001110_x11(machine1=1002, val6=1002)
    """State 2"""
    return 0

def t213001110_x34():
    """State 0,1"""
    assert t213001110_x1()
    """State 2"""
    return 0

def t213001110_x35():
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

def t213001110_x36():
    """State 0,1"""
    if GetEventFlag(3225):
        """State 4"""
        def WhilePaused():
            GiveSpEffectToSelfIf(GetEventFlag(11102707) == 1 and GetEventFlag(11109339) == 0, 9620)
        assert t213001110_x41()
        """State 3"""
        Label('L0')
        assert CheckSpecificPersonTalkHasEnded(0)
        """State 8"""
        assert t213001110_x39()
    elif GetEventFlag(3226):
        """State 5"""
        assert t213001110_x44()
        Goto('L0')
    elif GetEventFlag(3227):
        """State 6"""
        assert t213001110_x46()
        Goto('L0')
    elif GetEventFlag(3228):
        """State 7"""
        assert t213001110_x49()
        Goto('L0')
    else:
        """State 2"""
        pass
    """State 9"""
    return 0

def t213001110_x37():
    """State 0,1"""
    if GetEventFlag(3225):
        """State 3"""
        assert t213001110_x42()
    else:
        """State 2"""
        assert (t213001110_x0(actionbutton1=6210, flag5=6001, flag10=6000, flag11=6000, flag12=6000, flag13=6000,
                flag4=6000))
    """State 4"""
    return 0

def t213001110_x38():
    """State 0,5"""
    if not GetEventFlag(11102702):
        """State 1"""
        if not GetEventFlag(11109205) and not GetEventFlag(11102702):
            """State 9"""
            assert t213001110_x30(text2=21300100, mode4=1)
            """State 2"""
            SetEventFlag(11109205, FlagState.On)
        elif GetEventFlag(11102703) and not GetEventFlag(11109209):
            """State 13"""
            def WhilePaused():
                RequestAnimation(20016, -1)
            assert t213001110_x30(text2=21304200, mode4=1)
            """State 8"""
            SetEventFlag(11109209, FlagState.On)
        elif GetEventFlag(11102707) and not GetEventFlag(11109339):
            """State 14"""
            def WhilePaused():
                RequestAnimation(20018, -1)
            assert t213001110_x30(text2=21308100, mode4=1)
            """State 6"""
            SetEventFlag(11109339, FlagState.On)
        elif (GetEventFlag(9101) or GetEventFlag(9104) or GetEventFlag(9112) or GetEventFlag(9120) or GetEventFlag(9122)
              or GetEventFlag(9130)):
            """State 7"""
            if not GetEventFlag(11109206):
                """State 10"""
                assert t213001110_x30(text2=21303000, mode4=1)
                """State 4"""
                SetEventFlag(11109206, FlagState.On)
            else:
                """State 11"""
                Label('L0')
                assert t213001110_x30(text2=21301000, mode4=1)
        else:
            Goto('L0')
        """State 3"""
        SetEventFlag(11102702, FlagState.On)
    else:
        """State 12"""
        assert t213001110_x30(text2=21300200, mode4=1)
    """State 15"""
    return 0

def t213001110_x39():
    """State 0,8"""
    ClearPreviousMenuSelection()
    while True:
        """State 1"""
        ClearTalkListData()
        """State 33"""
        assert t213001110_x64()
        """State 11"""
        if GetEventFlag(3225):
            """State 17"""
            assert t213001110_x51()
        elif GetEventFlag(3226):
            """State 26"""
            assert t213001110_x58()
        elif GetEventFlag(3227):
            """State 30"""
            assert t213001110_x62()
        else:
            """State 12"""
            pass
        """State 3"""
        AddTalkListData(1, 22130001, -1)
        AddTalkListData(2, 22130003, -1)
        AddTalkListDataIf(GetEventFlag(65800) == 1, 20, 22130018, -1)
        AddTalkListData(4, 20000011, -1)
        AddTalkListDataIf(GetEventFlag(11109217) == 1, 5, 22130004, -1)
        AddTalkListDataIf(GetEventFlag(11109218) == 1, 6, 22130005, -1)
        AddTalkListDataIf(GetEventFlag(11109219) == 1, 7, 22130006, -1)
        AddTalkListDataIf(GetEventFlag(11109331) == 1, 8, 22130007, -1)
        AddTalkListDataIf(GetEventFlag(11109332) == 1, 9, 22130008, -1)
        AddTalkListDataIf(GetEventFlag(11109333) == 1, 10, 22130009, -1)
        AddTalkListDataIf(GetEventFlag(11109334) == 1, 11, 22130010, -1)
        AddTalkListDataIf(GetEventFlag(11109335) == 1, 12, 22130011, -1)
        if not GetEventFlag(1055420700):
            if GetEventFlag(9114) and GetEventFlag(32080800) and GetEventFlag(1041500800) and GetEventFlag(1036540800):
                AddTalkListData(13, 22130012, -1)
            else:
                AddTalkListData(13, 22139901, -1)
        AddTalkListDataIf(GetEventFlag(11109234) == 1, 14, 22130013, -1)
        AddTalkListDataIf(GetEventFlag(11109235) == 1, 15, 22130014, -1)
        AddTalkListDataIf(GetEventFlag(11109236) == 1, 16, 22130015, -1)
        AddTalkListDataIf(GetEventFlag(11109248) == 1, 17, 22130016, -1)
        AddTalkListData(99, 20000009, -1)
        """State 6"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 2"""
        if GetTalkListEntryResult() == 1:
            """State 14"""
            if not GetEventFlag(2051) and not GetEventFlag(2052):
                """State 15,5"""
                CombineMenuFlagAndEventFlag(6001, 232)
                CombineMenuFlagAndEventFlag(6001, 233)
                CombineMenuFlagAndEventFlag(6001, 234)
                CombineMenuFlagAndEventFlag(6001, 235)
                RecordPlayLog(9)
                """State 4"""
                OpenEnhanceShop(EnhanceType.UnlimitedRange)
                assert not (CheckSpecificPersonMenuIsOpen(9, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
                continue
            else:
                """State 16,34"""
                assert t213001110_x3(action1=22131010)
                continue
        elif GetTalkListEntryResult() == 2:
            """State 9"""
            OpenEquipmentChangeOfPurposeShop()
            RecordPlayLog(7)
            assert not (CheckSpecificPersonMenuIsOpen(7, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
            continue
        elif GetTalkListEntryResult() == 20:
            """State 13"""
            OpenAshOfWarShop(112000, 112150)
            assert not (CheckSpecificPersonMenuIsOpen(27, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
            continue
        elif GetTalkListEntryResult() == 4:
            """State 7"""
            OpenSellShop(-1, -1)
            RecordPlayLog(6)
            assert not (CheckSpecificPersonMenuIsOpen(6, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
            continue
        elif GetTalkListEntryResult() == 5:
            """State 18"""
            assert t213001110_x52()
        elif GetTalkListEntryResult() == 6:
            """State 19"""
            assert t213001110_x53()
        elif GetTalkListEntryResult() == 7:
            """State 20"""
            assert t213001110_x40()
        elif GetTalkListEntryResult() == 8:
            """State 21"""
            assert t213001110_x50()
        elif GetTalkListEntryResult() == 9:
            """State 22"""
            assert t213001110_x54()
        elif GetTalkListEntryResult() == 10:
            """State 23"""
            assert t213001110_x55()
        elif GetTalkListEntryResult() == 11:
            """State 24"""
            assert t213001110_x56()
        elif GetTalkListEntryResult() == 12:
            """State 25"""
            assert t213001110_x57()
        elif GetTalkListEntryResult() == 13:
            """State 27"""
            assert t213001110_x59()
        elif GetTalkListEntryResult() == 14:
            """State 28"""
            assert t213001110_x60()
        elif GetTalkListEntryResult() == 15:
            """State 29"""
            assert t213001110_x45()
        elif GetTalkListEntryResult() == 16:
            """State 32"""
            assert t213001110_x61()
        elif GetTalkListEntryResult() == 17:
            """State 31"""
            assert t213001110_x63()
        else:
            """State 35"""
            return 0
        """State 10"""
        assert CheckSpecificPersonTalkHasEnded(0)

def t213001110_x40():
    """State 0,7"""
    assert t213001110_x30(text2=21305100, mode4=1)
    while True:
        """State 5"""
        ClearPreviousMenuSelection()
        """State 1"""
        ClearTalkListData()
        """State 3"""
        AddTalkListDataIf(GetEventFlag(11109213) == 0, 1, 22131000, -1)
        AddTalkListDataIf(GetEventFlag(11109213) == 0, 2, 22131001, -1)
        AddTalkListDataIf(GetEventFlag(11109213) == 1, 3, 22131002, -1)
        AddTalkListDataIf(GetEventFlag(11109213) == 1, 4, 22131003, -1)
        """State 4"""
        OpenConversationChoicesMenu(0)
        assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 2"""
        if GetTalkListEntryResult() == 1:
            """State 8"""
            assert t213001110_x30(text2=21305200, mode4=1)
            """State 6"""
            SetEventFlag(11109213, FlagState.On)
            continue
        elif GetTalkListEntryResult() == 2:
            pass
        elif GetTalkListEntryResult() == 3:
            """State 9"""
            assert t213001110_x30(text2=21305300, mode4=1)
        elif GetTalkListEntryResult() == 4:
            pass
        """State 10"""
        return 0

def t213001110_x41():
    """State 0,1"""
    assert t213001110_x38()
    """State 2"""
    return 0

def t213001110_x42():
    """State 0"""
    while True:
        """State 3"""
        call = t213001110_x0(actionbutton1=6210, flag5=6001, flag10=6000, flag11=6000, flag12=6000, flag13=6000,
                             flag4=6000)
        if call.Done():
            break
        elif GetEventFlag(11102704) and not GetEventFlag(11102703) and not GetEventFlag(11109209):
            pass
        elif GetEventFlag(11102708) and not GetEventFlag(11102707) and not GetEventFlag(11109339):
            Goto('L0')
        """State 4"""
        call = t213001110_x31(text1=21304000, flag9=11102703, mode3=1)
        if call.Done():
            continue
        elif GetEventFlag(11102702):
            """State 1"""
            continue
        """State 5"""
        Label('L0')
        call = t213001110_x31(text1=21308000, flag9=11102707, mode3=1)
        if call.Done():
            pass
        elif GetEventFlag(11102702):
            """State 2"""
            pass
    """State 6"""
    return 0

def t213001110_x43():
    """State 0,1"""
    if not GetEventFlag(11109238):
        """State 4"""
        assert t213001110_x30(text2=21310000, mode4=1)
        """State 2"""
        SetEventFlag(11109238, FlagState.On)
    else:
        """State 3"""
        if not GetEventFlag(9114):
            """State 5"""
            assert t213001110_x30(text2=21310100, mode4=1)
        else:
            """State 6"""
            assert t213001110_x30(text2=21312300, mode4=1)
    """State 7"""
    return 0

def t213001110_x44():
    """State 0,1"""
    assert t213001110_x43()
    """State 2"""
    return 0

def t213001110_x45():
    """State 0,2"""
    assert t213001110_x30(text2=21311000, mode4=1)
    """State 1"""
    SetEventFlag(11109227, FlagState.On)
    """State 3"""
    return 0

def t213001110_x46():
    """State 0,1"""
    assert t213001110_x47()
    """State 2"""
    return 0

def t213001110_x47():
    """State 0,2"""
    assert t213001110_x30(text2=21314000, mode4=1)
    """State 1"""
    SetEventFlag(11109246, FlagState.On)
    """State 3"""
    return 0

def t213001110_x48():
    """State 0,2"""
    assert t213001110_x30(text2=21315000, mode4=1)
    """State 1,3"""
    return 0

def t213001110_x49():
    """State 0,1"""
    assert t213001110_x48()
    """State 2"""
    return 0

def t213001110_x50():
    """State 0,2"""
    assert t213001110_x30(text2=21306000, mode4=1)
    """State 1"""
    SetEventFlag(11109207, FlagState.On)
    """State 3"""
    return 0

def t213001110_x51():
    """State 0,2"""
    if not GetEventFlag(11109336) and GetEventFlag(11102703):
        """State 1"""
        SetEventFlag(11109217, FlagState.On)
    elif GetEventFlag(3707) and not GetEventFlag(11109210):
        """State 3"""
        SetEventFlag(11109218, FlagState.On)
    elif GetEventFlag(11109256) and not GetEventFlag(11109213):
        """State 4"""
        SetEventFlag(11109219, FlagState.On)
    elif GetEventFlag(3708) and GetEventFlag(11109213) and not GetEventFlag(11109207):
        """State 5"""
        SetEventFlag(11109331, FlagState.On)
    elif GetEventFlag(11109267) and not GetEventFlag(11109211):
        """State 6"""
        SetEventFlag(11109332, FlagState.On)
    elif not GetEventFlag(110) and GetEventFlag(1054539216) and not GetEventFlag(11109229):
        """State 7"""
        SetEventFlag(11109333, FlagState.On)
    elif not GetEventFlag(11109212):
        """State 8"""
        SetEventFlag(11109334, FlagState.On)
    elif GetEventFlag(11109212) and not GetEventFlag(11109216):
        """State 9"""
        SetEventFlag(11109335, FlagState.On)
    else:
        """State 10"""
        pass
    """State 11"""
    return 0

def t213001110_x52():
    """State 0,2"""
    assert t213001110_x30(text2=21304100, mode4=1)
    """State 1"""
    SetEventFlag(11109336, FlagState.On)
    """State 3"""
    return 0

def t213001110_x53():
    """State 0,2"""
    assert t213001110_x30(text2=21305000, mode4=1)
    """State 1"""
    SetEventFlag(11109210, FlagState.On)
    """State 3"""
    return 0

def t213001110_x54():
    """State 0,2"""
    assert t213001110_x30(text2=21307000, mode4=1)
    """State 1"""
    SetEventFlag(11109211, FlagState.On)
    """State 3"""
    return 0

def t213001110_x55():
    """State 0,2"""
    assert t213001110_x30(text2=21309000, mode4=1)
    """State 1"""
    SetEventFlag(11109229, FlagState.On)
    """State 3"""
    return 0

def t213001110_x56():
    """State 0,2"""
    assert t213001110_x30(text2=21302000, mode4=1)
    """State 1"""
    SetEventFlag(11109212, FlagState.On)
    """State 3"""
    return 0

def t213001110_x57():
    """State 0,2"""
    assert t213001110_x30(text2=21302100, mode4=1)
    """State 1"""
    SetEventFlag(11109216, FlagState.On)
    """State 3"""
    return 0

def t213001110_x58():
    """State 0,1"""
    if not GetEventFlag(11109227) and GetEventFlag(11109275):
        """State 2"""
        SetEventFlag(11109235, FlagState.On)
    elif not GetEventFlag(11109232) and GetEventFlag(11109276):
        """State 3"""
        SetEventFlag(11109236, FlagState.On)
    else:
        """State 4"""
        pass
    """State 5"""
    # Withholding the masterpiece must not withhold the separate farewell.
    if GetEventFlag(9114) and not GetEventFlag(11109231):
        """State 8"""
        SetEventFlag(11109234, FlagState.On)
    else:
        """State 6"""
        pass
    """State 9"""
    return 0

def t213001110_x59():
    """State 0"""
    if GetEventFlag(1055420700):
        pass
    elif not (GetEventFlag(9114) and GetEventFlag(32080800) and GetEventFlag(1041500800)
              and GetEventFlag(1036540800)):
        """State 1"""
        assert t213001110_x3(action1=22139900)
    else:
        """State 2"""
        assert t213001110_x2()
        """State 3"""
        SetEventFlag(1055420702, FlagState.Off)
        SetEventFlag(1055420701, FlagState.On)
        assert GetEventFlag(1055420702) or not GetEventFlag(1055420701)
        """State 4"""
        if not GetEventFlag(1055420702):
            pass
        else:
            """State 5"""
            if GetEventFlag(3227) or GetEventFlag(3228):
                """State 6"""
                assert t213001110_x30(text2=21313200, mode4=1)
            else:
                """State 7"""
                assert t213001110_x30(text2=21313000, mode4=1)
            """State 8"""
            if not GetEventFlag(1055420700) and GetEventFlag(9114) and GetEventFlag(32080800) and GetEventFlag(1041500800) and GetEventFlag(1036540800):
                """State 9"""
                AwardItemLot(7700)
                SetEventFlag(11109230, FlagState.On)
    """State 10"""
    return 0

def t213001110_x60():
    """State 0,2"""
    assert t213001110_x30(text2=21313100, mode4=1)
    """State 1"""
    SetEventFlag(11109231, FlagState.On)
    """State 3"""
    return 0

def t213001110_x61():
    """State 0,2"""
    assert t213001110_x30(text2=21311100, mode4=1)
    """State 1"""
    SetEventFlag(11109232, FlagState.On)
    """State 3"""
    return 0

def t213001110_x62():
    """State 0,2"""
    if not GetEventFlag(11109247):
        """State 1"""
        SetEventFlag(11109248, FlagState.On)
    else:
        """State 3"""
        pass
    """State 4"""
    return 0

def t213001110_x63():
    """State 0,2"""
    assert t213001110_x30(text2=21314100, mode4=1)
    """State 1"""
    SetEventFlag(11109247, -1)
    """State 3"""
    return 0

def t213001110_x64():
    """State 0,1"""
    SetEventFlag(11109217, FlagState.Off)
    SetEventFlag(11109218, FlagState.Off)
    SetEventFlag(11109219, FlagState.Off)
    SetEventFlag(11109331, FlagState.Off)
    SetEventFlag(11109332, FlagState.Off)
    SetEventFlag(11109333, FlagState.Off)
    SetEventFlag(11109334, FlagState.Off)
    SetEventFlag(11109335, FlagState.Off)
    """State 2"""
    SetEventFlag(11109235, FlagState.Off)
    SetEventFlag(11109236, FlagState.Off)
    SetEventFlag(11109233, FlagState.Off)
    SetEventFlag(11109234, FlagState.Off)
    """State 3"""
    SetEventFlag(11109248, FlagState.Off)
    """State 4"""
    return 0
