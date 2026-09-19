# -*- coding: utf-8 -*-
def t112001100_1():
    """State 0"""
    while True:
        """State 2"""
        # actionbutton:6000:"Talk"
        call = t112001100_x5(flag1=6000, flag2=6000, flag3=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                             flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000,
                             z4=1000000, mode1=1, mode2=1)
        assert GetEventFlag(1040542710)
        """State 1"""
        assert not GetEventFlag(1040542710)

def t112001100_1000():
    """State 0,2,3"""
    assert t112001100_x33()
    """State 1"""
    EndMachine(1000)
    Quit()

def t112001100_x0(actionbutton1=6000, flag5=6001, flag9=6000, flag10=6000, flag11=6000, flag12=6000, flag4=6000):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 3"""
        assert GetEventFlag(flag5) or GetEventFlag(flag9) or GetEventFlag(flag10) or GetEventFlag(flag11) or GetEventFlag(flag12)
        """State 4"""
        assert not GetEventFlag(flag4)
        """State 2"""
        if (GetEventFlag(flag4) or not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead()
            and not IsCharacterDisabled()) or (not GetEventFlag(flag5) and not GetEventFlag(flag9) and not GetEventFlag(flag10)
            and not GetEventFlag(flag11) and not GetEventFlag(flag12))):
            pass
        # actionbutton:6000:"Talk"
        elif CheckActionButtonArea(actionbutton1):
            break
    """State 5"""
    return 0

def t112001100_x1():
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

def t112001100_x2():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ForceCloseGenericDialog()
    ForceCloseMenu()
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t112001100_x3(val2=10, val3=12):
    """State 0,1"""
    assert GetDistanceToPlayer() < val2 and GetCurrentStateElapsedFrames() > 1
    """State 2"""
    if PlayerDiedFromFallInstantly() == False and PlayerDiedFromFallDamage() == False:
        """State 3,6"""
        call = t112001100_x19()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 5"""
            assert t112001100_x1()
    else:
        """State 4,7"""
        call = t112001100_x30()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 8"""
            assert t112001100_x1()
    """State 9"""
    return 0

def t112001100_x4():
    """State 0,1"""
    assert t112001100_x1()
    """State 2"""
    return 0

def t112001100_x5(flag1=6000, flag2=6000, flag3=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                  flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                  mode1=1, mode2=1):
    """State 0"""
    assert GetCurrentStateElapsedTime() > 1.5
    while True:
        """State 2"""
        call = t112001100_x22(flag1=flag1, flag2=flag2, flag3=flag3, val1=val1, val2=val2, val3=val3, val4=val4,
                              val5=val5, actionbutton1=actionbutton1, flag4=flag4, flag5=flag5, flag6=flag6, flag7=flag7,
                              flag8=flag8, z1=z1, z2=z2, z3=z3, z4=z4, mode1=mode1, mode2=mode2)
        assert IsClientPlayer()
        """State 1"""
        call = t112001100_x21()
        assert not IsClientPlayer()
    """Unused"""
    """State 3"""
    return 0

def t112001100_x6(val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000, flag4=6000, flag5=6001, flag6=6000,
                  flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000, mode1=1, mode2=1):
    """State 0"""
    while True:
        """State 2"""
        call = t112001100_x9(actionbutton1=actionbutton1, flag4=flag4, flag5=flag5, z2=z2, z3=z3, z4=z4)
        def WhilePaused():
            RemoveMyAggroIf(IsAttackedBySomeone() == 1 and (DoesSelfHaveSpEffect(9626) == 1 and DoesSelfHaveSpEffect(9627) == 1))
            GiveSpEffectToPlayerIf(CheckSpecificPersonTalkHasEnded(0) == 0, 9640)
        if call.Done():
            """State 4"""
            Label('L0')
            ChangeCamera(1000000)
            call = t112001100_x13(val1=val1, z1=z1)
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
            call = t112001100_x15(val5=val5)
            if call.Done():
                continue
            elif IsAttackedBySomeone():
                pass
        elif ((GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6) and not CheckSpecificPersonTalkHasEnded(0)
              and not DoesSelfHaveSpEffect(9625)):
            """State 6"""
            assert t112001100_x26() and CheckSpecificPersonTalkHasEnded(0)
            continue
        elif GetEventFlag(9000):
            """State 1"""
            assert not GetEventFlag(9000)
            continue
        """State 3"""
        def ExitPause():
            RemoveMyAggro()
        assert t112001100_x11(val2=val2, val3=val3)
    """Unused"""
    """State 7"""
    return 0

def t112001100_x7(val2=10, val3=12):
    """State 0,1"""
    call = t112001100_x17(val2=val2, val3=val3)
    assert IsPlayerDead()
    """State 2"""
    t112001100_x3(val2=val2, val3=val3)
    Quit()
    """Unused"""
    """State 3"""
    return 0

def t112001100_x8(flag1=6000, val2=10, val3=12):
    """State 0,8"""
    assert t112001100_x32()
    """State 1"""
    if GetEventFlag(flag1):
        """State 2"""
        pass
    else:
        """State 3"""
        if GetDistanceToPlayer() < val2:
            """State 4,6"""
            call = t112001100_x20()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t112001100_x1()
        else:
            """State 5"""
            pass
    """State 9"""
    return 0

def t112001100_x9(actionbutton1=6000, flag4=6000, flag5=6001, z2=1000000, z3=1000000, z4=1000000):
    """State 0,1"""
    call = t112001100_x10(machine1=2000, val6=2000)
    if call.Get() == 1:
        """State 2"""
        assert (t112001100_x0(actionbutton1=actionbutton1, flag5=flag5, flag9=6000, flag10=6000, flag11=6000, flag12=6000,
                flag4=flag4))
    elif call.Done():
        pass
    """State 3"""
    return 0

def t112001100_x10(machine1=_, val6=_):
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

def t112001100_x11(val2=10, val3=12):
    """State 0"""
    assert GetCurrentStateElapsedFrames() > 1
    """State 5"""
    assert t112001100_x1()
    """State 3"""
    if GetDistanceToPlayer() < val2:
        """State 1"""
        if IsPlayerAttacking():
            """State 6"""
            call = t112001100_x12()
            if call.Done():
                pass
            elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
                """State 7"""
                assert t112001100_x27()
        else:
            """State 4"""
            pass
    else:
        """State 2"""
        pass
    """State 8"""
    return 0

def t112001100_x12():
    """State 0,1"""
    assert t112001100_x10(machine1=1101, val6=1101)
    """State 2"""
    return 0

def t112001100_x13(val1=5, z1=1):
    """State 0,2"""
    assert t112001100_x23()
    """State 1"""
    call = t112001100_x14()
    if call.Done():
        pass
    elif (GetDistanceToPlayer() > val1 or GetTalkInterruptReason() == 6) and not DoesSelfHaveSpEffect(9625):
        """State 3"""
        assert t112001100_x25()
    """State 4"""
    return 0

def t112001100_x14():
    """State 0,1"""
    assert t112001100_x10(machine1=1000, val6=1000)
    """State 2"""
    return 0

def t112001100_x15(val5=12):
    """State 0,1"""
    call = t112001100_x16()
    if call.Done():
        pass
    elif GetDistanceToPlayer() > val5 or GetTalkInterruptReason() == 6:
        """State 2"""
        assert t112001100_x26()
    """State 3"""
    return 0

def t112001100_x16():
    """State 0,1"""
    assert t112001100_x10(machine1=1100, val6=1100)
    """State 2"""
    return 0

def t112001100_x17(val2=10, val3=12):
    """State 0,5"""
    assert t112001100_x32()
    """State 2"""
    assert not GetEventFlag(3000)
    while True:
        """State 1"""
        assert GetDistanceToPlayer() < val2
        """State 3"""
        call = t112001100_x18()
        if call.Done():
            pass
        elif GetDistanceToPlayer() > val3 or GetTalkInterruptReason() == 6:
            """State 4"""
            assert t112001100_x28()
    """Unused"""
    """State 6"""
    return 0

def t112001100_x18():
    """State 0,2"""
    call = t112001100_x10(machine1=1102, val6=1102)
    if call.Get() == 1:
        """State 1"""
        Quit()
    elif call.Done():
        """State 3"""
        return 0

def t112001100_x19():
    """State 0,1"""
    assert t112001100_x10(machine1=1001, val6=1001)
    """State 2"""
    return 0

def t112001100_x20():
    """State 0,1"""
    assert t112001100_x10(machine1=1103, val6=1103)
    """State 2"""
    return 0

def t112001100_x21():
    """State 0"""
    Quit()
    """Unused"""
    """State 1"""
    return 0

def t112001100_x22(flag1=6000, flag2=6000, flag3=6000, val1=5, val2=10, val3=12, val4=10, val5=12, actionbutton1=6000,
                   flag4=6000, flag5=6001, flag6=6000, flag7=6000, flag8=6000, z1=1, z2=1000000, z3=1000000, z4=1000000,
                   mode1=1, mode2=1):
    """State 0"""
    while True:
        """State 1"""
        RemoveMyAggro()
        call = t112001100_x6(val1=val1, val2=val2, val3=val3, val4=val4, val5=val5, actionbutton1=actionbutton1,
                             flag4=flag4, flag5=flag5, flag6=flag6, flag7=flag7, flag8=flag8, z1=z1, z2=z2, z3=z3,
                             z4=z4, mode1=mode1, mode2=mode2)
        if CheckSelfDeath() or GetEventFlag(flag1):
            """State 3"""
            Label('L0')
            call = t112001100_x8(flag1=flag1, val2=val2, val3=val3)
            if not CheckSelfDeath() and not GetEventFlag(flag1):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(flag2) or GetEventFlag(flag3):
            """State 2"""
            call = t112001100_x7(val2=val2, val3=val3)
            if CheckSelfDeath() or GetEventFlag(flag1):
                Goto('L0')
            elif not GetEventFlag(flag2) and not GetEventFlag(flag3):
                continue
            elif GetEventFlag(9000):
                pass
        elif GetEventFlag(9000) or (IsPlayerDead() and not DoesSelfHaveSpEffect(9649)):
            pass
        """State 4"""
        assert t112001100_x31() and (not GetEventFlag(9000) and not IsPlayerDead())
    """Unused"""
    """State 5"""
    return 0

def t112001100_x23():
    """State 0,1"""
    assert t112001100_x24()
    """State 2"""
    return 0

def t112001100_x24():
    """State 0,1"""
    assert t112001100_x10(machine1=1104, val6=1104)
    """State 2"""
    return 0

def t112001100_x25():
    """State 0,1"""
    call = t112001100_x10(machine1=1201, val6=1201)
    if call.Get() == 1:
        """State 2"""
        assert t112001100_x4()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t112001100_x26():
    """State 0,1"""
    call = t112001100_x10(machine1=1300, val6=1300)
    if call.Get() == 1:
        """State 2"""
        assert t112001100_x4()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t112001100_x27():
    """State 0,1"""
    call = t112001100_x10(machine1=1301, val6=1301)
    if call.Get() == 1:
        """State 2"""
        assert t112001100_x4()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t112001100_x28():
    """State 0,1"""
    call = t112001100_x10(machine1=1302, val6=1302)
    if call.Get() == 1:
        """State 2"""
        assert t112001100_x4()
    elif call.Done():
        pass
    """State 3"""
    return 0

def t112001100_x29(text1=_, mode3=1):
    """State 0,4"""
    assert t112001100_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text1, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 3"""
    if mode3 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t112001100_x30():
    """State 0,1"""
    assert t112001100_x10(machine1=1002, val6=1002)
    """State 2"""
    return 0

def t112001100_x31():
    """State 0,1"""
    assert t112001100_x1()
    """State 2"""
    return 0

def t112001100_x32():
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

def t112001100_x33():
    """State 0,1"""
    if GetEventFlag(1040549254):
        """State 19"""
        # talk:11201000:"..."
        assert t112001100_x29(text1=11201000, mode3=1)
        """State 2"""
        SetEventFlag(1040549255, FlagState.On)
    elif GetEventFlag(11009554):
        """State 17"""
        SetEventFlag(11009557, FlagState.On)
        """State 4"""
        if not GetEventFlag(11009555):
            """State 6,20"""
            # talk:11201010:"..."
            assert t112001100_x29(text1=11201010, mode3=1)
            """State 12"""
            if GetEventFlag(11009556):
                """State 7"""
                ClearPreviousMenuSelection()
                ClearTalkListData()
                """State 8"""
                # action:21121000:"Tell him that Radagon is Marika"
                AddTalkListData(1, 21121000, -1)
                # action:20000009:"Leave"
                AddTalkListData(2, 20000009, -1)
                """State 9"""
                OpenConversationChoicesMenu(0)
                assert not (CheckSpecificPersonMenuIsOpen(12, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
                """State 10"""
                if GetTalkListEntryResult() == 1:
                    """State 22"""
                    # talk:11201020:"..."
                    assert t112001100_x29(text1=11201020, mode3=1)
                    """State 15"""
                    if not GetEventFlag(60848):
                        """State 14"""
                        # gesture:106:Golden Order Totality
                        AwardItemLot(6900)
                        AcquireGesture(106)
                        SetEventFlag(60848, FlagState.On)
                    else:
                        """State 16"""
                        pass
                    """State 3"""
                    SetEventFlag(11009555, -1)
                else:
                    """State 13"""
                    pass
            else:
                pass
        else:
            """State 11,21"""
            # talk:11201030:"..."
            assert t112001100_x29(text1=11201030, mode3=1)
    elif GetEventFlag(1051569454):
        """State 18"""
        SetEventFlag(1051569455, FlagState.On)
        """State 23"""
        # talk:11201040:"..."
        assert t112001100_x29(text1=11201040, mode3=1)
    else:
        """State 5"""
        pass
    """State 24"""
    return 0

