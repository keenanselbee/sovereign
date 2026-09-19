# -*- coding: utf-8 -*-
def t000001000_1():
    """State 0,1"""
    t000001000_x22()
    Quit()

def t000001000_x0(action7=_):
    """State 0,1"""
    OpenGenericDialog(DialogBoxType.CenterBottom2, action7, DialogResult.Leave, DialogBoxStyle.Unk, 2)
    assert not CheckSpecificPersonGenericDialogIsOpen(0)
    """State 2"""
    if GetGenericDialogButtonResult() == DialogResult.Left:
        """State 3"""
        return 0
    else:
        """State 4"""
        return 1

def t000001000_x1():
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

def t000001000_x2():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ForceCloseGenericDialog()
    ForceCloseMenu()
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

def t000001000_x3(actionbutton1=_, flag8=6001, flag9=6000):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 2"""
        assert CompareBonfireState(1)
        """State 4"""
        if GetEventFlag(flag9):
            """State 5"""
            assert GetEventFlag(flag8) and not GetEventFlag(flag9)
            """State 6"""
            assert GetCurrentStateElapsedTime() > 1
        elif GetEventFlag(flag8) and not GetEventFlag(flag9):
            pass
        """State 3"""
        if CompareBonfireState(0):
            pass
        elif CheckActionButtonArea(actionbutton1):
            break
        elif (not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled())
              or (not GetEventFlag(flag8) or GetEventFlag(flag9))):
            pass
    """State 7"""
    return 0

def t000001000_x4(action6=_):
    """State 0,1"""
    OpenGenericDialog(DialogBoxType.CenterBottom1, action6, DialogResult.Left, DialogBoxStyle.OrnateNoOptions, 1)
    assert not CheckSpecificPersonGenericDialogIsOpen(0)
    """State 2"""
    return 0

def t000001000_x5(actionbutton5=6100, flag6=6001, flag7=6000):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 3"""
        assert GetEventFlag(flag6) and not GetEventFlag(flag7)
        """State 2"""
        # actionbutton:6100:"Touch grace"
        if CheckActionButtonArea(actionbutton5):
            break
        elif (not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled())
              or (not GetEventFlag(flag6) or GetEventFlag(flag7))):
            pass
    """State 4"""
    return 0

def t000001000_x6(goods7=1000, goods8=10020):
    """State 0,14"""
    if GetEventFlag(720080):
        """State 15"""
        pass
    else:
        """State 16,17"""
        SetEventFlag(720080, FlagState.On)
    """State 1"""
    if GetTotalBonfireLevel() <= 13:
        """State 2,13,26"""
        # goods:1000:Flask of Crimson Tears
        # goods:1001:Flask of Crimson Tears
        # goods:1002:Flask of Crimson Tears +1
        # goods:1003:Flask of Crimson Tears +1
        # goods:1004:Flask of Crimson Tears +2
        # goods:1005:Flask of Crimson Tears +2
        # goods:1006:Flask of Crimson Tears +3
        # goods:1007:Flask of Crimson Tears +3
        # goods:1008:Flask of Crimson Tears +4
        # goods:1009:Flask of Crimson Tears +4
        # goods:1010:Flask of Crimson Tears +5
        # goods:1011:Flask of Crimson Tears +5
        # goods:1012:Flask of Crimson Tears +6
        # goods:1013:Flask of Crimson Tears +6
        # goods:1014:Flask of Crimson Tears +7
        # goods:1015:Flask of Crimson Tears +7
        # goods:1016:Flask of Crimson Tears +8
        # goods:1017:Flask of Crimson Tears +8
        # goods:1018:Flask of Crimson Tears +9
        # goods:1019:Flask of Crimson Tears +9
        # goods:1020:Flask of Crimson Tears +10
        # goods:1021:Flask of Crimson Tears +10
        # goods:1022:Flask of Crimson Tears +11
        # goods:1023:Flask of Crimson Tears +11
        # goods:1024:Flask of Crimson Tears +12
        # goods:1025:Flask of Crimson Tears +12
        call = t000001000_x17(goods7=goods7, goods10=0, z46=1)
        if call.Get() == 0:
            """State 12,25"""
            # action:13040150:"No Flask of Crimson Tears in inventory"
            assert t000001000_x4(action6=13040150)
        elif call.Done():
            """State 11,19"""
            SetWorkValue(1, 1)
            """State 20"""
            call = t000001000_x0(action7=20011000 + GetWorkValue(1))
            if call.Get() == 0:
                """State 6,10"""
                # goods:10020:Sacred Tear
                if (ComparePlayerInventoryNumber(ItemType.Goods, goods8, CompareType.GreaterOrEqual, GetWorkValue(1),
                    False)):
                    """State 4,8"""
                    BonfireActivation(GetTotalBonfireLevel() + 1)
                    """State 9"""
                    # goods:10020:Sacred Tear
                    PlayerEquipmentQuantityChange(ItemType.Goods, goods8, GetWorkValue(1) * -1)
                    """State 27"""
                    assert t000001000_x19(goods7=goods7)
                    """State 24"""
                    assert t000001000_x16(goods9=goods7)
                    """State 22"""
                    # action:13040020:"Increased the amount of HP/FP replenished by your flasks"
                    assert t000001000_x4(action6=13040020)
                    """State 18"""
                    SetWorkValue(1, 0)
                else:
                    """State 5,28"""
                    # action:20011000:"No Sacred Tear in inventory"
                    assert t000001000_x4(action6=20011000)
            elif call.Done():
                """State 7"""
                pass
    else:
        """State 3,21"""
        # action:13040000:"The amount of HP/FP your flasks replenish cannot be increased any further"
        assert t000001000_x4(action6=13040000)
    """State 29"""
    return 0
    """Unused"""
    """State 23"""
    t000001000_x11()
    Quit()

def t000001000_x7(goods5=1000, goods6=10010):
    """State 0,15"""
    if GetEventFlag(720070):
        """State 16"""
        pass
    else:
        """State 17,18"""
        SetEventFlag(720070, FlagState.On)
    """State 1"""
    if GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) < 13:
        """State 2,13,26"""
        # goods:1000:Flask of Crimson Tears
        # goods:1001:Flask of Crimson Tears
        # goods:1002:Flask of Crimson Tears +1
        # goods:1003:Flask of Crimson Tears +1
        # goods:1004:Flask of Crimson Tears +2
        # goods:1005:Flask of Crimson Tears +2
        # goods:1006:Flask of Crimson Tears +3
        # goods:1007:Flask of Crimson Tears +3
        # goods:1008:Flask of Crimson Tears +4
        # goods:1009:Flask of Crimson Tears +4
        # goods:1010:Flask of Crimson Tears +5
        # goods:1011:Flask of Crimson Tears +5
        # goods:1012:Flask of Crimson Tears +6
        # goods:1013:Flask of Crimson Tears +6
        # goods:1014:Flask of Crimson Tears +7
        # goods:1015:Flask of Crimson Tears +7
        # goods:1016:Flask of Crimson Tears +8
        # goods:1017:Flask of Crimson Tears +8
        # goods:1018:Flask of Crimson Tears +9
        # goods:1019:Flask of Crimson Tears +9
        # goods:1020:Flask of Crimson Tears +10
        # goods:1021:Flask of Crimson Tears +10
        # goods:1022:Flask of Crimson Tears +11
        # goods:1023:Flask of Crimson Tears +11
        # goods:1024:Flask of Crimson Tears +12
        # goods:1025:Flask of Crimson Tears +12
        call = t000001000_x17(goods7=goods5, goods10=0, z46=1)
        if call.Get() == 0:
            """State 12,25"""
            # action:13040150:"No Flask of Crimson Tears in inventory"
            assert t000001000_x4(action6=13040150)
        elif call.Done():
            """State 11,19"""
            SetWorkValue(1, GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) + -4)
            """State 28"""
            assert t000001000_x21(z33=1, z34=1, z35=2, z36=2, z37=3, z38=3, z39=4, z40=4, z41=5, z42=5, z43=1)
            """State 21"""
            call = t000001000_x0(action7=20011010 + GetWorkValue(1))
            if call.Get() == 0:
                """State 6,14"""
                # goods:10010:Golden Seed
                if (ComparePlayerInventoryNumber(ItemType.Goods, goods6, CompareType.GreaterOrEqual, GetWorkValue(1),
                    False)):
                    """State 4,8"""
                    # goods:10010:Golden Seed
                    PlayerEquipmentQuantityChange(ItemType.Goods, goods6, GetWorkValue(1) * -1)
                    """State 9"""
                    EstusAllocationUpdate(GetEstusAllocation(EstusType.HP) + 1, 0)
                    """State 27"""
                    assert t000001000_x16(goods9=goods5)
                    """State 22"""
                    # action:13040140:"Added a charge to Flask of Crimson Tears"
                    assert t000001000_x4(action6=13040140)
                    """State 20"""
                    SetWorkValue(1, 0)
                    """State 10"""
                else:
                    """State 5,23"""
                    # action:20011010:"Not enough Golden Seeds"
                    assert t000001000_x4(action6=20011010)
            elif call.Done():
                """State 7"""
                pass
    else:
        """State 3,24"""
        # action:13040120:"Flask charges already at maximum"
        assert t000001000_x4(action6=13040120)
    """State 29"""
    return 0

def t000001000_x8(goods11=1000):
    """State 0,1"""
    # goods:1001:Flask of Crimson Tears
    # goods:1000:Flask of Crimson Tears
    if (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 0 * 2) or DoesPlayerHaveItem(ItemType.Goods,
        goods11 + 0 + 0 * 50 + 0 * 2)):
        """State 2"""
        BonfireActivation(1)
        """State 13"""
        Label('L0')
        """State 18"""
        assert t000001000_x9(goods11=goods11)
    # goods:1003:Flask of Crimson Tears +1
    # goods:1002:Flask of Crimson Tears +1
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 1 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 1 * 2)):
        """State 3"""
        BonfireActivation(2)
        Goto('L0')
    # goods:1005:Flask of Crimson Tears +2
    # goods:1004:Flask of Crimson Tears +2
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 2 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 2 * 2)):
        """State 4"""
        BonfireActivation(3)
        Goto('L0')
    # goods:1007:Flask of Crimson Tears +3
    # goods:1006:Flask of Crimson Tears +3
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 3 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 3 * 2)):
        """State 5"""
        BonfireActivation(4)
        Goto('L0')
    # goods:1009:Flask of Crimson Tears +4
    # goods:1008:Flask of Crimson Tears +4
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 4 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 4 * 2)):
        """State 6"""
        BonfireActivation(5)
        Goto('L0')
    # goods:1011:Flask of Crimson Tears +5
    # goods:1010:Flask of Crimson Tears +5
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 5 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 5 * 2)):
        """State 7"""
        BonfireActivation(6)
        Goto('L0')
    # goods:1013:Flask of Crimson Tears +6
    # goods:1012:Flask of Crimson Tears +6
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 6 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 6 * 2)):
        """State 8"""
        BonfireActivation(7)
        Goto('L0')
    # goods:1015:Flask of Crimson Tears +7
    # goods:1014:Flask of Crimson Tears +7
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 7 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 7 * 2)):
        """State 9"""
        BonfireActivation(8)
        Goto('L0')
    # goods:1017:Flask of Crimson Tears +8
    # goods:1016:Flask of Crimson Tears +8
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 8 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 8 * 2)):
        """State 10"""
        BonfireActivation(9)
        Goto('L0')
    # goods:1019:Flask of Crimson Tears +9
    # goods:1018:Flask of Crimson Tears +9
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 9 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 9 * 2)):
        """State 11"""
        BonfireActivation(10)
        Goto('L0')
    # goods:1021:Flask of Crimson Tears +10
    # goods:1020:Flask of Crimson Tears +10
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 10 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 10 * 2)):
        """State 12"""
        BonfireActivation(11)
        Goto('L0')
    elif True:
        """State 15"""
        pass
    # goods:1023:Flask of Crimson Tears +11
    # goods:1022:Flask of Crimson Tears +11
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 11 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 11 * 2)):
        """State 16"""
        BonfireActivation(12)
        Goto('L0')
    # goods:1025:Flask of Crimson Tears +12
    # goods:1024:Flask of Crimson Tears +12
    elif (DoesPlayerHaveItem(ItemType.Goods, goods11 + 1 + 0 * 50 + 12 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods11 + 0 + 0 * 50 + 12 * 2)):
        """State 17"""
        BonfireActivation(13)
        Goto('L0')
    """State 14,19"""
    return 0

def t000001000_x9(goods11=1000):
    """State 0,15"""
    # goods:1000:Flask of Crimson Tears
    # goods:1002:Flask of Crimson Tears +1
    # goods:1004:Flask of Crimson Tears +2
    # goods:1006:Flask of Crimson Tears +3
    # goods:1008:Flask of Crimson Tears +4
    # goods:1010:Flask of Crimson Tears +5
    # goods:1012:Flask of Crimson Tears +6
    # goods:1014:Flask of Crimson Tears +7
    call = t000001000_x12(goods11=goods11, goods12=0, goods13=0)
    if call.Get() == 1:
        """State 1,11"""
        # goods:1000:Flask of Crimson Tears
        # goods:1002:Flask of Crimson Tears +1
        # goods:1004:Flask of Crimson Tears +2
        # goods:1006:Flask of Crimson Tears +3
        # goods:1008:Flask of Crimson Tears +4
        # goods:1010:Flask of Crimson Tears +5
        # goods:1012:Flask of Crimson Tears +6
        # goods:1014:Flask of Crimson Tears +7
        # goods:1016:Flask of Crimson Tears +8
        # goods:1018:Flask of Crimson Tears +9
        assert t000001000_x10(goods11=goods11, goods14=0, goods15=0)
    elif call.Done():
        """State 16"""
        # goods:1001:Flask of Crimson Tears
        # goods:1003:Flask of Crimson Tears +1
        # goods:1005:Flask of Crimson Tears +2
        # goods:1007:Flask of Crimson Tears +3
        # goods:1009:Flask of Crimson Tears +4
        # goods:1011:Flask of Crimson Tears +5
        # goods:1013:Flask of Crimson Tears +6
        # goods:1015:Flask of Crimson Tears +7
        call = t000001000_x12(goods11=goods11, goods12=0, goods13=1)
        if call.Get() == 1:
            """State 8,10"""
            # goods:1001:Flask of Crimson Tears
            # goods:1003:Flask of Crimson Tears +1
            # goods:1005:Flask of Crimson Tears +2
            # goods:1007:Flask of Crimson Tears +3
            # goods:1009:Flask of Crimson Tears +4
            # goods:1011:Flask of Crimson Tears +5
            # goods:1013:Flask of Crimson Tears +6
            # goods:1015:Flask of Crimson Tears +7
            # goods:1017:Flask of Crimson Tears +8
            # goods:1019:Flask of Crimson Tears +9
            assert t000001000_x10(goods11=goods11, goods14=0, goods15=1)
        elif call.Done():
            """State 2"""
            pass
    """State 5,17"""
    # goods:1050:Flask of Cerulean Tears
    # goods:1052:Flask of Cerulean Tears +1
    # goods:1054:Flask of Cerulean Tears +2
    # goods:1056:Flask of Cerulean Tears +3
    # goods:1058:Flask of Cerulean Tears +4
    # goods:1060:Flask of Cerulean Tears +5
    # goods:1062:Flask of Cerulean Tears +6
    # goods:1064:Flask of Cerulean Tears +7
    call = t000001000_x12(goods11=goods11, goods12=1, goods13=0)
    if call.Get() == 1:
        """State 3,13"""
        # goods:1050:Flask of Cerulean Tears
        # goods:1052:Flask of Cerulean Tears +1
        # goods:1054:Flask of Cerulean Tears +2
        # goods:1056:Flask of Cerulean Tears +3
        # goods:1058:Flask of Cerulean Tears +4
        # goods:1060:Flask of Cerulean Tears +5
        # goods:1062:Flask of Cerulean Tears +6
        # goods:1064:Flask of Cerulean Tears +7
        # goods:1066:Flask of Cerulean Tears +8
        # goods:1068:Flask of Cerulean Tears +9
        assert t000001000_x10(goods11=goods11, goods14=1, goods15=0)
    elif call.Done():
        """State 18"""
        # goods:1051:Flask of Cerulean Tears
        # goods:1053:Flask of Cerulean Tears +1
        # goods:1055:Flask of Cerulean Tears +2
        # goods:1057:Flask of Cerulean Tears +3
        # goods:1059:Flask of Cerulean Tears +4
        # goods:1061:Flask of Cerulean Tears +5
        # goods:1063:Flask of Cerulean Tears +6
        # goods:1065:Flask of Cerulean Tears +7
        call = t000001000_x12(goods11=goods11, goods12=1, goods13=1)
        if call.Get() == 1:
            """State 9,12"""
            # goods:1051:Flask of Cerulean Tears
            # goods:1053:Flask of Cerulean Tears +1
            # goods:1055:Flask of Cerulean Tears +2
            # goods:1057:Flask of Cerulean Tears +3
            # goods:1059:Flask of Cerulean Tears +4
            # goods:1061:Flask of Cerulean Tears +5
            # goods:1063:Flask of Cerulean Tears +6
            # goods:1065:Flask of Cerulean Tears +7
            # goods:1067:Flask of Cerulean Tears +8
            # goods:1069:Flask of Cerulean Tears +9
            assert t000001000_x10(goods11=goods11, goods14=1, goods15=1)
        elif call.Done():
            """State 4"""
            pass
    """State 6,14"""
    assert t000001000_x11()
    """State 7,19"""
    return 0

def t000001000_x10(goods11=1000, goods14=_, goods15=_):
    """State 0,1"""
    if DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 0 * 2):
        """State 3"""
        ReplaceTool(goods11 + goods14 * 50 + 0 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 1 * 2):
        """State 4"""
        ReplaceTool(goods11 + goods14 * 50 + 1 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 2 * 2):
        """State 5"""
        ReplaceTool(goods11 + goods14 * 50 + 2 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 3 * 2):
        """State 6"""
        ReplaceTool(goods11 + goods14 * 50 + 3 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 4 * 2):
        """State 7"""
        ReplaceTool(goods11 + goods14 * 50 + 4 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 5 * 2):
        """State 8"""
        ReplaceTool(goods11 + goods14 * 50 + 5 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    elif DoesPlayerHaveItem(ItemType.Goods, goods11 + goods15 + goods14 * 50 + 6 * 2):
        """State 9"""
        ReplaceTool(goods11 + goods14 * 50 + 6 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                    1)
    else:
        """State 2"""
        pass
    """State 13"""
    return 0
    """Unused"""
    """State 10"""
    ReplaceTool(goods11 + goods14 * 50 + 7 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                1)
    Quit()
    """State 11"""
    ReplaceTool(goods11 + goods14 * 50 + 8 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                1)
    Quit()
    """State 12"""
    ReplaceTool(goods11 + goods14 * 50 + 9 * 2 + goods15, goods11 + goods14 * 50 + goods15 + 2 * (GetTotalBonfireLevel() - 1),
                1)
    Quit()

def t000001000_x11():
    """State 0,1,13,14"""
    return 0
    """Unused"""
    """State 2,3,4"""
    Quit()
    """State 5"""
    Quit()
    """State 6"""
    Quit()
    """State 7"""
    Quit()
    """State 8"""
    Quit()
    """State 9"""
    Quit()
    """State 10"""
    Quit()
    """State 11"""
    Quit()
    """State 12"""
    Quit()

def t000001000_x12(goods11=1000, goods12=_, goods13=_):
    """State 0,1"""
    if (not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13 + goods12 * 50 + 0 * 2) and not DoesPlayerHaveItem(ItemType.Goods,
        goods11 + goods13 + goods12 * 50 + 1 * 2) and not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13
        + goods12 * 50 + 2 * 2) and not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13 + goods12 * 50 + 3
        * 2) and not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13 + goods12 * 50 + 4 * 2) and not DoesPlayerHaveItem(ItemType.Goods,
        goods11 + goods13 + goods12 * 50 + 5 * 2) and not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13
        + goods12 * 50 + 6 * 2) and not DoesPlayerHaveItem(ItemType.Goods, goods11 + goods13 + goods12 * 50 + 7
        * 2)):
        """State 2,3"""
        return 0
    else:
        """State 4"""
        return 1

def t000001000_x13():
    """State 0,1"""
    if DoesPlayerHaveSpEffect(8990):
        """State 2"""
        GiveSpEffectToPlayer(8998)
        """State 3"""
        SetEventFlag(100210, FlagState.Off)
        SetEventFlag(100200, FlagState.Off)
    else:
        pass
    """State 4"""
    return 0

def t000001000_x14(text2=_, flag5=_, mode4=1):
    """State 0,5"""
    assert t000001000_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text2, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 4"""
    if mode4 == 0:
        pass
    else:
        """State 3"""
        ReportConversationEndToHavokBehavior()
    """State 2"""
    SetEventFlag(flag5, FlagState.On)
    """State 6"""
    return 0

def t000001000_x15(goods9=1000):
    """State 0,4,10"""
    # goods:1000:Flask of Crimson Tears
    # goods:1001:Flask of Crimson Tears
    # goods:1002:Flask of Crimson Tears +1
    # goods:1003:Flask of Crimson Tears +1
    # goods:1004:Flask of Crimson Tears +2
    # goods:1005:Flask of Crimson Tears +2
    # goods:1006:Flask of Crimson Tears +3
    # goods:1007:Flask of Crimson Tears +3
    # goods:1008:Flask of Crimson Tears +4
    # goods:1009:Flask of Crimson Tears +4
    # goods:1010:Flask of Crimson Tears +5
    # goods:1011:Flask of Crimson Tears +5
    # goods:1012:Flask of Crimson Tears +6
    # goods:1013:Flask of Crimson Tears +6
    # goods:1014:Flask of Crimson Tears +7
    # goods:1015:Flask of Crimson Tears +7
    # goods:1016:Flask of Crimson Tears +8
    # goods:1017:Flask of Crimson Tears +8
    # goods:1018:Flask of Crimson Tears +9
    # goods:1019:Flask of Crimson Tears +9
    # goods:1020:Flask of Crimson Tears +10
    # goods:1021:Flask of Crimson Tears +10
    # goods:1022:Flask of Crimson Tears +11
    # goods:1023:Flask of Crimson Tears +11
    # goods:1024:Flask of Crimson Tears +12
    # goods:1025:Flask of Crimson Tears +12
    call = t000001000_x17(goods7=goods9, goods10=0, z46=1)
    if call.Get() == 0:
        """State 2,8"""
        # action:13040150:"No Flask of Crimson Tears in inventory"
        assert t000001000_x4(action6=13040150)
    elif call.Done():
        """State 1,7,12"""
        # goods:1050:Flask of Cerulean Tears
        # goods:1051:Flask of Cerulean Tears
        # goods:1052:Flask of Cerulean Tears +1
        # goods:1053:Flask of Cerulean Tears +1
        # goods:1054:Flask of Cerulean Tears +2
        # goods:1055:Flask of Cerulean Tears +2
        # goods:1056:Flask of Cerulean Tears +3
        # goods:1057:Flask of Cerulean Tears +3
        # goods:1058:Flask of Cerulean Tears +4
        # goods:1059:Flask of Cerulean Tears +4
        # goods:1060:Flask of Cerulean Tears +5
        # goods:1061:Flask of Cerulean Tears +5
        # goods:1062:Flask of Cerulean Tears +6
        # goods:1063:Flask of Cerulean Tears +6
        # goods:1064:Flask of Cerulean Tears +7
        # goods:1065:Flask of Cerulean Tears +7
        # goods:1066:Flask of Cerulean Tears +8
        # goods:1067:Flask of Cerulean Tears +8
        # goods:1068:Flask of Cerulean Tears +9
        # goods:1069:Flask of Cerulean Tears +9
        # goods:1070:Flask of Cerulean Tears +10
        # goods:1071:Flask of Cerulean Tears +10
        # goods:1072:Flask of Cerulean Tears +11
        # goods:1073:Flask of Cerulean Tears +11
        # goods:1074:Flask of Cerulean Tears +12
        # goods:1075:Flask of Cerulean Tears +12
        call = t000001000_x17(goods7=goods9, goods10=1, z46=1)
        if call.Get() == 0:
            """State 6,11"""
            # action:13040160:"No Flask of Cerulean Tears in inventory"
            assert t000001000_x4(action6=13040160)
        elif call.Done():
            """State 5,3"""
            OpenEstusAllotMenu()
            assert not (CheckSpecificPersonMenuIsOpen(14, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
            """State 9"""
            assert t000001000_x16(goods9=goods9)
    """State 13"""
    return 0

def t000001000_x16(goods9=1000):
    """State 0,3"""
    # goods:1000:Flask of Crimson Tears
    # goods:1001:Flask of Crimson Tears
    # goods:1002:Flask of Crimson Tears +1
    # goods:1003:Flask of Crimson Tears +1
    # goods:1004:Flask of Crimson Tears +2
    # goods:1005:Flask of Crimson Tears +2
    # goods:1006:Flask of Crimson Tears +3
    # goods:1007:Flask of Crimson Tears +3
    # goods:1008:Flask of Crimson Tears +4
    # goods:1009:Flask of Crimson Tears +4
    # goods:1010:Flask of Crimson Tears +5
    # goods:1011:Flask of Crimson Tears +5
    # goods:1012:Flask of Crimson Tears +6
    # goods:1013:Flask of Crimson Tears +6
    # goods:1014:Flask of Crimson Tears +7
    # goods:1015:Flask of Crimson Tears +7
    # goods:1016:Flask of Crimson Tears +8
    # goods:1017:Flask of Crimson Tears +8
    # goods:1018:Flask of Crimson Tears +9
    # goods:1019:Flask of Crimson Tears +9
    # goods:1020:Flask of Crimson Tears +10
    # goods:1021:Flask of Crimson Tears +10
    # goods:1022:Flask of Crimson Tears +11
    # goods:1023:Flask of Crimson Tears +11
    # goods:1024:Flask of Crimson Tears +12
    # goods:1025:Flask of Crimson Tears +12
    call = t000001000_x17(goods7=goods9, goods10=0, z46=1)
    if call.Get() == 1:
        """State 4"""
        assert t000001000_x18(goods9=goods9, mode3=0, z45=GetWorkValue(1))
        """State 5"""
        assert t000001000_x18(goods9=goods9, mode3=1, z45=GetWorkValue(1))
    elif call.Done():
        """State 1"""
        pass
    """State 2"""
    SetWorkValue(1, 0)
    """State 6"""
    return 0

def t000001000_x17(goods7=1000, goods10=_, z46=1):
    """State 0,13"""
    SetWorkValue(z46, 0)
    if (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 0 * 2) or DoesPlayerHaveItem(ItemType.Goods,
        goods7 + 1 + goods10 * 50 + 0 * 2)):
        """State 1"""
        SetWorkValue(z46, 0)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 1 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 1 * 2)):
        """State 2"""
        SetWorkValue(z46, 1)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 2 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 2 * 2)):
        """State 3"""
        SetWorkValue(z46, 2)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 3 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 3 * 2)):
        """State 4"""
        SetWorkValue(z46, 3)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 4 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 4 * 2)):
        """State 5"""
        SetWorkValue(z46, 4)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 5 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 5 * 2)):
        """State 6"""
        SetWorkValue(z46, 5)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 6 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 6 * 2)):
        """State 7"""
        SetWorkValue(z46, 6)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 7 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 7 * 2)):
        """State 8"""
        SetWorkValue(z46, 7)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 8 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 8 * 2)):
        """State 9"""
        SetWorkValue(z46, 8)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 9 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 9 * 2)):
        """State 10"""
        SetWorkValue(z46, 9)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 10 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 10 * 2)):
        """State 11"""
        SetWorkValue(z46, 10)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 11 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 11 * 2)):
        """State 14"""
        SetWorkValue(z46, 11)
    elif (DoesPlayerHaveItem(ItemType.Goods, goods7 + 0 + goods10 * 50 + 12 * 2) or DoesPlayerHaveItem(ItemType.Goods,
          goods7 + 1 + goods10 * 50 + 12 * 2)):
        """State 15"""
        SetWorkValue(z46, 12)
    else:
        """State 12"""
        SetWorkValue(z46, 13)
        """State 16"""
        return 0
    """State 17"""
    return 1

def t000001000_x18(goods9=1000, mode3=_, z45=_):
    """State 0,6"""
    if not GetEstusAllocation(mode3) < 0:
        """State 7,12"""
        if (DoesPlayerHaveItem(ItemType.Goods, goods9 + 0 + mode3 * 50 + z45 * 2) or DoesPlayerHaveItem(ItemType.Goods,
            goods9 + 1 + mode3 * 50 + z45 * 2)):
            """State 13,1"""
            if DoesPlayerHaveItem(ItemType.Goods, goods9 + 0 + mode3 * 50 + z45 * 2):
                """State 2,4"""
                ReplaceTool(1000 + mode3 * 50 + z45 * 2 + 0, 1000 + mode3 * 50 + z45 * 2 + 1, 1)
            else:
                """State 3"""
                pass
            while True:
                """State 5"""
                if (not ComparePlayerInventoryNumber(ItemType.Goods, 1000 + 1 + mode3 * 50 + z45 * 2, CompareType.GreaterOrEqual,
                    GetEstusAllocation(mode3), False)):
                    """State 9,11"""
                    PlayerEquipmentQuantityChange(ItemType.Goods, 1000 + 1 + mode3 * 50 + z45 * 2, 1)
                else:
                    """State 10"""
                    break
        else:
            """State 14"""
            pass
    else:
        """State 8"""
        pass
    """State 15"""
    return 0

def t000001000_x19(goods7=1000):
    """State 0,3"""
    # goods:1000:Flask of Crimson Tears
    # goods:1001:Flask of Crimson Tears
    # goods:1002:Flask of Crimson Tears +1
    # goods:1003:Flask of Crimson Tears +1
    # goods:1004:Flask of Crimson Tears +2
    # goods:1005:Flask of Crimson Tears +2
    # goods:1006:Flask of Crimson Tears +3
    # goods:1007:Flask of Crimson Tears +3
    # goods:1008:Flask of Crimson Tears +4
    # goods:1009:Flask of Crimson Tears +4
    # goods:1010:Flask of Crimson Tears +5
    # goods:1011:Flask of Crimson Tears +5
    # goods:1012:Flask of Crimson Tears +6
    # goods:1013:Flask of Crimson Tears +6
    # goods:1014:Flask of Crimson Tears +7
    # goods:1015:Flask of Crimson Tears +7
    # goods:1016:Flask of Crimson Tears +8
    # goods:1017:Flask of Crimson Tears +8
    # goods:1018:Flask of Crimson Tears +9
    # goods:1019:Flask of Crimson Tears +9
    # goods:1020:Flask of Crimson Tears +10
    # goods:1021:Flask of Crimson Tears +10
    # goods:1022:Flask of Crimson Tears +11
    # goods:1023:Flask of Crimson Tears +11
    # goods:1024:Flask of Crimson Tears +12
    # goods:1025:Flask of Crimson Tears +12
    call = t000001000_x17(goods7=goods7, goods10=0, z46=1)
    if call.Get() == 1:
        """State 4"""
        assert t000001000_x20(goods7=goods7, z44=GetWorkValue(1))
        """State 2"""
        SetWorkValue(1, 0)
    elif call.Done():
        """State 1"""
        pass
    """State 5"""
    return 0

def t000001000_x20(goods7=1000, z44=_):
    """State 0,1"""
    ReplaceToolIf(DoesPlayerHaveItem(ItemType.Goods, 1000 + 0 + 0 * 50 + z44 * 2) == 1, goods7 + 0 * 50 + z44 * 2 + 0,
                  goods7 + 0 * 50 + 0 + 2 * (GetTotalBonfireLevel() - 1), 1)
    """State 2"""
    ReplaceToolIf(DoesPlayerHaveItem(ItemType.Goods, 1000 + 1 + 0 * 50 + z44 * 2) == 1, goods7 + 0 * 50 + z44 * 2 + 1,
                  goods7 + 0 * 50 + 1 + 2 * (GetTotalBonfireLevel() - 1), 1)
    """State 3"""
    ReplaceToolIf(DoesPlayerHaveItem(ItemType.Goods, 1000 + 0 + 1 * 50 + z44 * 2) == 1, goods7 + 1 * 50 + z44 * 2 + 0,
                  goods7 + 1 * 50 + 0 + 2 * (GetTotalBonfireLevel() - 1), 1)
    """State 4"""
    ReplaceToolIf(DoesPlayerHaveItem(ItemType.Goods, 1000 + 1 + 1 * 50 + z44 * 2) == 1, goods7 + 1 * 50 + z44 * 2 + 1,
                  goods7 + 1 * 50 + 1 + 2 * (GetTotalBonfireLevel() - 1), 1)
    """State 5"""
    return 0

def t000001000_x21(z33=1, z34=1, z35=2, z36=2, z37=3, z38=3, z39=4, z40=4, z41=5, z42=5, z43=1):
    """State 0"""
    if GetWorkValue(z43) == 0:
        """State 1"""
        SetWorkValue(z43, z33)
    elif GetWorkValue(z43) == 1:
        """State 2"""
        SetWorkValue(z43, z34)
    elif GetWorkValue(z43) == 2:
        """State 3"""
        SetWorkValue(z43, z35)
    elif GetWorkValue(z43) == 3:
        """State 4"""
        SetWorkValue(z43, z36)
    elif GetWorkValue(z43) == 4:
        """State 5"""
        SetWorkValue(z43, z37)
    elif GetWorkValue(z43) == 5:
        """State 6"""
        SetWorkValue(z43, z38)
    elif GetWorkValue(z43) == 6:
        """State 7"""
        SetWorkValue(z43, z39)
    elif GetWorkValue(z43) == 7:
        """State 8"""
        SetWorkValue(z43, z40)
    elif GetWorkValue(z43) == 8:
        """State 9"""
        SetWorkValue(z43, z41)
    elif GetWorkValue(z43) == 9:
        """State 10"""
        SetWorkValue(z43, z42)
    else:
        """State 11"""
        SetWorkValue(z43, 5)
    """State 12"""
    return 0

def t000001000_x22():
    """State 0"""
    if not GetEventFlag(9000):
        """State 3,1"""
        SetEventFlag(4652, FlagState.Off)
        SetEventFlag(4653, FlagState.Off)
        SetEventFlag(4654, FlagState.Off)
        SetEventFlag(4655, FlagState.Off)
        SetEventFlag(4656, FlagState.Off)
        SetEventFlag(4657, FlagState.Off)
        SetEventFlag(4651, FlagState.Off)
    else:
        """State 2"""
        pass
    while True:
        """State 4"""
        if IsMultiplayerInProgress() and not GetEventFlag(2051) and not GetEventFlag(2052):
            """State 6"""
            call = t000001000_x25()
            assert not IsMultiplayerInProgress() or GetEventFlag(2051) or GetEventFlag(2052)
        elif GetEventFlag(1042369415):
            """State 7"""
            call = t000001000_x63()
            assert not GetEventFlag(1042369415)
        else:
            """State 5"""
            def WhilePaused():
                GiveSpEffectToPlayerIf(GetEventFlag(9000) == 1 and (GetWorkValue(0) == 0) == 1, 9607)
                GiveSpEffectToPlayerIf(GetEventFlag(9000) == 1 and (GetWorkValue(0) == 10) == 1, 9608)
                GiveSpEffectToPlayerIf(GetEventFlag(9000) == 1 and GetDistanceToPlayer() < 1.05, 9609)
                GiveSpEffectToPlayerIf(GetEventFlag(4698) == 1 and GetEventFlag(9001) == 1, 9606)
            assert t000001000_x23()
    """Unused"""
    """State 8"""
    return 0

def t000001000_x23():
    """State 0,1"""
    if CompareBonfireLevel(CompareType.LessOrEqual, 0) or GetEventFlag(11102790):
        """State 2"""
        Label('L0')
        assert GetWhetherChrEventAnimHasEnded(10000)
    else:
        """State 3,32"""
        call = t000001000_x40()
        if call.Done():
            """State 7"""
            TurnCharacterToFaceEntity(-1, 10000, -1, -1)
            assert GetCurrentStateElapsedFrames() > 1 and GetWhetherChrEventAnimHasEnded(10000)
            """State 4"""
            OfferHumanity()
            assert CompareBonfireLevel(CompareType.LessOrEqual, 0)
            """State 9,10"""
            UpdatePlayerRespawnPoint()
            Goto('L0')
        elif CompareBonfireLevel(CompareType.LessOrEqual, 0) or GetEventFlag(11102790):
            pass
    """State 33"""
    call = t000001000_x40()
    if call.Done():
        """State 5"""
        ClearPlayerDamageInfo()
        """State 11"""
        GiveSpEffectToPlayer(202)
        """State 6"""
        SetTalkTime(1)
        """State 37"""
        assert t000001000_x67()
        """State 23"""
        SetEventFlag(4698, FlagState.Off)
        SetEventFlagIf(DoesSelfHaveSpEffect(9680) == 1 and GetEventFlag(953) == 0, 4698, FlagState.On)
        SetEventFlagIf((GetEventFlagValue(955, 3) > 2) == 1 and DoesSelfHaveSpEffect(9681) == 1 and GetEventFlag(953) == 0,
                       4698, FlagState.On)
        """State 30"""
        assert t000001000_x32()
        """State 8"""
        TurnCharacterToFaceEntity(-1, 10000, -1, -1)
        assert GetCurrentStateElapsedFrames() > 1 and GetWhetherChrEventAnimHasEnded(10000)
        """State 12"""
        UpdatePlayerRespawnPoint()
        """State 40"""
        assert t000001000_x82()
        """State 19"""
        StartBonfireAnimLoop(1, 1, 1, 1, GetWorkValue(0), 0.5)
        """State 13"""
        FadeOutAndPassTime(0, 0, 0, 0, 0, 0, 0, 0.1, 0, 1.5, 0, 0.75, 0.5)
        """State 18"""
        SetEventFlag(9000, FlagState.On)
        SetEventFlag(9020, FlagState.On)
        ChangeCameraIf(GetEventFlag(11102790) == 0, 1001000)
        ChangeCameraIf(GetEventFlag(11102790) == 1, 1001001)
        if not GetEventFlag(4698):
            """State 36"""
            assert t000001000_x66()
        else:
            """State 35"""
            assert t000001000_x64()
        """State 17"""
        if not GetEventFlag(9001):
            """State 21"""
            pass
        else:
            """State 20"""
            assert not GetEventFlag(9001)
        """State 41"""
        call = t000001000_x84()
        if call.Get() == 0:
            """State 26"""
            pass
        elif call.Get() == 1:
            """State 27,29"""
            assert t000001000_x30()
        """State 15"""
        if not GetEventFlag(4653):
            """State 22,39"""
            Label('L1')
            assert t000001000_x68()
            """State 31"""
            call = t000001000_x31()
            def WhilePaused():
                GiveSpEffectToPlayerIf(GetEventFlag(4651) == 1, 9620)
            def ExitPause():
                EndBonfireKindleAnimLoop(GetWorkValue(0))
            if call.Done():
                pass
            elif ((((GetDistanceToPlayer() > 3 and not GetEventFlag(11102790)) or GetDistanceToPlayer() > 7) and
                  GetCurrentStateElapsedFrames() > 1) or (CompareBonfireState(0) and GetCurrentStateElapsedFrames()
                  > 1) or (HasPlayerBeenAttacked() and GetCurrentStateElapsedFrames() > 1) or (IsMultiplayerInProgress()
                  and not GetEventFlag(2051) and not GetEventFlag(2052) and GetCurrentStateElapsedFrames() > 1)
                  or (GetEventFlag(1042369415) and GetCurrentStateElapsedFrames() > 1) or (CompareBonfireLevel(CompareType.Equal,
                  0) and not GetEventFlag(11102790) and GetCurrentStateElapsedFrames() > 1)):
                """State 28"""
                Label('L2')
                assert t000001000_x24()
        else:
            """State 16,34"""
            call = t000001000_x50()
            if call.Done():
                Goto('L1')
            elif ((GetEventFlag(1042369415) and GetCurrentStateElapsedFrames() > 1) or (IsMultiplayerInProgress()
                  and GetCurrentStateElapsedFrames() > 1) or (HasPlayerBeenAttacked() and GetCurrentStateElapsedFrames()
                  > 1) or (((GetDistanceToPlayer() > 3 and not GetEventFlag(11102790)) or GetDistanceToPlayer()
                  > 7) and GetCurrentStateElapsedFrames() > 1) or (CompareBonfireState(0) and GetCurrentStateElapsedFrames()
                  > 1)):
                """State 24"""
                def ExitPause():
                    EndBonfireKindleAnimLoop(GetWorkValue(0))
                Goto('L2')
        """State 38"""
        assert t000001000_x67()
        """State 14"""
        SetEventFlag(9000, FlagState.Off)
        SetEventFlag(9020, FlagState.Off)
        ChangeCamera(-1)
        SetCanOpenMap(False)
        assert GetCurrentStateElapsedFrames() > 1
        """State 25"""
        if not IsMultiplayerInProgress() and not GetEventFlag(1042369415):
            Goto('L0')
        else:
            pass
    elif (GetEventFlag(1042369415) or (CompareBonfireLevel(CompareType.Equal, 0) and not GetEventFlag(11102790))
          or (IsMultiplayerInProgress() and not GetEventFlag(2051) and not GetEventFlag(2052))):
        pass
    """State 42"""
    return 0

def t000001000_x24():
    """State 0,1"""
    assert t000001000_x1()
    """State 2"""
    return 0

def t000001000_x25():
    """State 0"""
    while True:
        """State 1"""
        call = t000001000_x26()
        assert IsClientPlayer()
        """State 2"""
        call = t000001000_x27()
        assert not IsClientPlayer()
    """Unused"""
    """State 3"""
    return 0

def t000001000_x26():
    """State 0,6"""
    call = t000001000_x1()
    if call.Done() and CompareBonfireLevel(CompareType.LessOrEqual, 0):
        pass
    elif call.Done():
        """State 2,7"""
        # actionbutton:6100:"Touch grace"
        call = t000001000_x3(actionbutton1=6100, flag8=6001, flag9=6000)
        if call.Done():
            """State 4"""
            TurnCharacterToFaceEntity(-1, 10000, -1, -1)
            assert GetCurrentStateElapsedFrames() > 1 and GetWhetherChrEventAnimHasEnded(10000)
            """State 3"""
            OfferHumanity()
            """State 5"""
            UpdatePlayerRespawnPoint()
            assert CompareBonfireLevel(CompareType.LessOrEqual, 0)
        elif CompareBonfireLevel(CompareType.LessOrEqual, 0):
            pass
    """State 1"""
    Quit()
    """Unused"""
    """State 8"""
    return 0

def t000001000_x27():
    """State 0,1"""
    assert t000001000_x1()
    """State 2"""
    return 0

def t000001000_x28():
    """State 0,1"""
    if not GetEventFlag(4651):
        """State 3"""
        if GetEventFlag(4698):
            """State 5,10"""
            assert t000001000_x35(z28=20006, val4=0.5, z29=1, z30=2, z31=60)
        elif GetEventFlag(108):
            """State 9,13"""
            assert t000001000_x35(z28=20000, val4=3.5, z29=1, z30=2, z31=60)
        else:
            """State 4,6"""
            # eventflag:400001:lot:100010:Rold Medallion
            if not GetEventFlag(400001):
                """State 7,11"""
                assert t000001000_x35(z28=20000, val4=3.5, z29=1, z30=2, z31=60)
            else:
                """State 8,12"""
                assert t000001000_x35(z28=20001, val4=3.5, z29=1, z30=2, z31=60)
    else:
        """State 2"""
        pass
    """State 14"""
    return 0

def t000001000_x29(z32=_):
    """State 0,1"""
    RemoveDynamicCharacter(z32, 1.4)
    """State 2"""
    SetEventFlag(4651, FlagState.Off)
    SetEventFlag(4652, FlagState.Off)
    SetEventFlag(4653, FlagState.Off)
    SetEventFlag(4654, FlagState.Off)
    SetEventFlag(4655, FlagState.Off)
    SetEventFlag(4656, FlagState.Off)
    SetEventFlag(4657, FlagState.Off)
    """State 3"""
    return 0

def t000001000_x30():
    """State 0"""
    if GetEventFlag(11102790):
        """State 3"""
        pass
    elif GetEventFlag(110):
        """State 1"""
        pass
    elif not GetEventFlag(953) or GetEventFlag(4698):
        """State 4"""
        assert t000001000_x59()
    elif not GetEventFlag(4680):
        """State 2"""
        pass
    elif GetEventFlag(108):
        """State 7"""
        assert t000001000_x62()
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(11009260) and not GetEventFlag(400001):
        """State 6"""
        assert t000001000_x61()
    else:
        """State 5"""
        assert t000001000_x60()
    """State 8"""
    return 0

def t000001000_x31():
    """State 0,10"""
    assert GetCurrentStateElapsedTime() > 0.1 or not GetEventFlag(4651)
    """State 11"""
    assert not GetEventFlag(9001)
    """State 27"""
    # goods:1001:Flask of Crimson Tears
    # goods:1000:Flask of Crimson Tears
    # goods:1003:Flask of Crimson Tears +1
    # goods:1002:Flask of Crimson Tears +1
    # goods:1005:Flask of Crimson Tears +2
    # goods:1004:Flask of Crimson Tears +2
    # goods:1007:Flask of Crimson Tears +3
    # goods:1006:Flask of Crimson Tears +3
    # goods:1009:Flask of Crimson Tears +4
    # goods:1008:Flask of Crimson Tears +4
    # goods:1011:Flask of Crimson Tears +5
    # goods:1010:Flask of Crimson Tears +5
    # goods:1013:Flask of Crimson Tears +6
    # goods:1012:Flask of Crimson Tears +6
    # goods:1015:Flask of Crimson Tears +7
    # goods:1014:Flask of Crimson Tears +7
    # goods:1017:Flask of Crimson Tears +8
    # goods:1016:Flask of Crimson Tears +8
    # goods:1019:Flask of Crimson Tears +9
    # goods:1018:Flask of Crimson Tears +9
    # goods:1021:Flask of Crimson Tears +10
    # goods:1020:Flask of Crimson Tears +10
    # goods:1023:Flask of Crimson Tears +11
    # goods:1022:Flask of Crimson Tears +11
    # goods:1025:Flask of Crimson Tears +12
    # goods:1024:Flask of Crimson Tears +12
    # goods:1050:Flask of Cerulean Tears
    # goods:1051:Flask of Cerulean Tears
    # goods:1052:Flask of Cerulean Tears +1
    # goods:1053:Flask of Cerulean Tears +1
    # goods:1054:Flask of Cerulean Tears +2
    # goods:1055:Flask of Cerulean Tears +2
    # goods:1056:Flask of Cerulean Tears +3
    # goods:1057:Flask of Cerulean Tears +3
    # goods:1058:Flask of Cerulean Tears +4
    # goods:1059:Flask of Cerulean Tears +4
    # goods:1060:Flask of Cerulean Tears +5
    # goods:1061:Flask of Cerulean Tears +5
    # goods:1062:Flask of Cerulean Tears +6
    # goods:1063:Flask of Cerulean Tears +6
    # goods:1064:Flask of Cerulean Tears +7
    # goods:1065:Flask of Cerulean Tears +7
    # goods:1067:Flask of Cerulean Tears +8
    # goods:1066:Flask of Cerulean Tears +8
    # goods:1069:Flask of Cerulean Tears +9
    # goods:1068:Flask of Cerulean Tears +9
    assert t000001000_x8(goods11=1000)
    """State 5"""
    ClearPreviousMenuSelection()
    while True:
        """State 1"""
        Label('L0')
        ClearTalkListData()
        """State 2"""
        # action:15000420:"Pass time"
        AddTalkListDataIf(GetEventFlag(9411) == 0 or GetEventFlag(9412) == 1, 1, 15000420, -1)
        # action:15000540:"Level Up"
        AddTalkListDataIf(GetEventFlag(4680) == 1 or GetEventFlag(4699) == 1, 2, 15000540, -1)
        """State 38"""
        # action:15000371:"Flasks"
        assert t000001000_x71(z20=3, action3=15000371)
        """State 41"""
        # action:20010001:"Shadow Realm Blessing"
        # goods:2010000:Scadutree Fragment
        # goods:2010100:Revered Spirit Ash
        assert t000001000_x80(z3=50, action1=20010001, goods1=2010000, goods2=2010100)
        """State 17"""
        # action:15000390:"Memorize spell"
        AddTalkListData(4, 15000390, -1)
        # goods:250:Flask of Wondrous Physick
        # goods:251:Flask of Wondrous Physick
        # action:15000510:"Mix Wondrous Physick"
        AddTalkListDataIf(ComparePlayerInventoryNumber(ItemType.Goods, 250, CompareType.Greater, 0, False) == 1 or ComparePlayerInventoryNumber(ItemType.Goods, 251, CompareType.Greater, 0, False) == 1,
                          5, 15000510, -1)
        # action:15000395:"Sort chest"
        AddTalkListData(6, 15000395, -1)
        # action:15000520:"Great Runes"
        AddTalkListDataIf(PlayerHasTool(15) == 1, 7, 15000520, -1)
        # goods:8590:Whetstone Knife
        # action:15000530:"Ashes of War"
        AddTalkListDataIf(ComparePlayerInventoryNumber(ItemType.Goods, 8590, CompareType.GreaterOrEqual, 1, False) == 1,
                          8, 15000530, -1)
        # goods:8163:Tailoring Tools
        # goods:8188:Golden Tailoring Tools
        # action:22230000:"Alter garments"
        AddTalkListDataIf(ComparePlayerInventoryNumber(ItemType.Goods, 8163, CompareType.Greater, 0, False) == 1 or ComparePlayerInventoryNumber(ItemType.Goods, 8188, CompareType.Greater, 0, False) == 1,
                          9, 22230000, -1)
        """State 56"""
        assert t000001000_x85()
        """State 51"""
        call = t000001000_x84()
        if call.Get() == 0:
            """State 25"""
            pass
        elif call.Get() == 1:
            """State 26,35"""
            assert t000001000_x52()
        """State 15"""
        if not GetEventFlag(1054539200) and GetEventFlag(4680) and not GetEventFlag(9431) and not DoesPlayerHaveSpEffect(9621):
            """State 44"""
            AddTalkListDataIf(GetEventFlag(4651) == 1, 22, 1055421042, -1)
            if GetEventFlag(4651):
                """State 49"""
                AddTalkListData(23, 1055421041, -1)
            else:
                """State 50"""
                AddTalkListData(23, 1055421040, -1)
        else:
            pass
        """State 55"""
        # action:20000009:"Leave"
        AddTalkListData(99, 20000009, -1)
        """State 6"""
        SetEventFlag(4652, FlagState.Off)
        SetEventFlag(4656, FlagState.Off)
        SetEventFlag(4654, FlagState.Off)
        SetEventFlag(4655, FlagState.Off)
        """State 3"""
        SetCanOpenMap(True)
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 8"""
        if GetTalkListEntryResult() == 1:
            """State 28"""
            SetCanOpenMap(False)
            ClearPreviousMenuSelection()
            def ExitPause():
                ClearPreviousMenuSelection()
            assert t000001000_x33()
        elif GetTalkListEntryResult() == 22:
            """State 47"""
            SetCanOpenMap(False)
            ClearPreviousMenuSelection()
            def ExitPause():
                ClearPreviousMenuSelection()
            assert t000001000_x2223()
        elif GetTalkListEntryResult() == 23:
            """State 48"""
            assert t000001000_x2222()
        elif GetTalkListEntryResult() == 2:
            """State 18"""
            if (not GetEventFlag(2051) and not GetEventFlag(2052) and not GetEventFlag(1054539200) and GetEventFlag(4680)
                and not GetEventFlag(9431)):
                """State 54"""
                assert t000001000_x28()
                """State 19,29"""
                assert t000001000_x34()
            elif not GetEventFlag(2051) and not GetEventFlag(2052):
                """State 53"""
                assert t000001000_x34()
            else:
                """State 20,39"""
                # action:20011032:"Cannot select while entering combat"
                assert t000001000_x4(action6=20011032)
        elif GetTalkListEntryResult() == 3:
            """State 34"""
            SetCanOpenMap(False)
            ClearPreviousMenuSelection()
            def ExitPause():
                ClearPreviousMenuSelection()
            assert t000001000_x47()
        elif GetTalkListEntryResult() == 4:
            """State 7"""
            OpenMagicEquip(-1, -1)
            assert not (CheckSpecificPersonMenuIsOpen(11, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 5:
            """State 12"""
            OpenPhysickMenu()
            assert not (CheckSpecificPersonMenuIsOpen(21, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 6:
            """State 9"""
            OpenRepository()
            assert not (CheckSpecificPersonMenuIsOpen(3, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 7:
            """State 13"""
            OpenGreatRuneEquipMenu()
            assert not (CheckSpecificPersonMenuIsOpen(24, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 8:
            """State 14"""
            OpenEquipmentChangeOfPurposeShop()
            assert not (CheckSpecificPersonMenuIsOpen(7, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 9:
            """State 16"""
            OpenTailoringShop(111000, 111399)
            assert not (CheckSpecificPersonMenuIsOpen(26, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 11:
            """State 30"""
            assert t000001000_x36(flag4=4655)
        elif GetTalkListEntryResult() == 12:
            """State 37"""
            assert t000001000_x36(flag4=4657)
        elif GetTalkListEntryResult() == 15:
            """State 36"""
            assert t000001000_x54()
        elif GetTalkListEntryResult() == 32:
            """State 32"""
            assert t000001000_x38()
        elif GetTalkListEntryResult() == 41 and GetEventFlag(120) and GetEventFlag(11102790):
            """State 21"""
            if not GetEventFlag(2051) and not GetEventFlag(2052):
                """State 22,33"""
                assert t000001000_x42()
            else:
                """State 23,40"""
                # action:20011031:"Cannot select while entering combat"
                assert t000001000_x4(action6=20011031)
        elif GetTalkListEntryResult() == 50:
            """State 24,42"""
            SetCanOpenMap(False)
            ClearPreviousMenuSelection()
            # goods:2010000:Scadutree Fragment
            # goods:2010100:Revered Spirit Ash
            def ExitPause():
                ClearPreviousMenuSelection()
            assert t000001000_x78(goods3=2010000, goods4=2010100)
        elif GetTalkListEntryResult() == 75:
            """State 57,58"""
            SetCanOpenMap(False)
            ClearPreviousMenuSelection()
            def ExitPause():
                ClearPreviousMenuSelection()
            assert t000001000_x87()
        else:
            """State 4,43"""
            assert t000001000_x83()
            """State 45"""
            return 0
    """Unused"""
    """State 31"""
    assert t000001000_x37()
    Goto('L0')

def t000001000_x32():
    """State 0,1"""
    if GetEventFlag(1054532702):
        """State 2,4"""
        Label('L0')
        """State 3"""
        SetWorkValue(0, 0)
    elif GetEventFlag(4698):
        """State 8"""
        Goto('L0')
    elif GetEventFlag(11102790):
        """State 6,7"""
        SetWorkValue(0, 30)
    else:
        """State 5,9"""
        assert t000001000_x39()
    """State 10"""
    return 0

def t000001000_x33():
    """State 0,5"""
    CloseShopMessage()
    while True:
        """State 1"""
        ClearTalkListData()
        """State 2"""
        # action:15000430:"Until morning"
        AddTalkListData(1, 15000430, -1)
        # action:15000440:"Until noon"
        AddTalkListData(2, 15000440, -1)
        # action:15000450:"Until nightfall"
        AddTalkListData(3, 15000450, -1)
        # action:15000460:"Cancel"
        AddTalkListData(99, 15000460, -1)
        """State 3"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 6"""
        if GetTalkListEntryResult() == 1:
            """State 7"""
            def ExitPause():
                HideClock(0.5)
            assert t000001000_x45(val1=0)
        elif GetTalkListEntryResult() == 2:
            """State 8"""
            def ExitPause():
                HideClock(0.5)
            assert t000001000_x45(val1=1)
        elif GetTalkListEntryResult() == 3:
            """State 9"""
            def ExitPause():
                HideClock(0.5)
            assert t000001000_x45(val1=2)
        else:
            """State 4,10"""
            assert t000001000_x72()
            """State 11"""
            return 0

def t000001000_x34():
    """State 0"""
    if not GetEventFlag(4651):
        """State 3,4"""
        OpenSoul()
        assert not (CheckSpecificPersonMenuIsOpen(10, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
    else:
        """State 2,1"""
        SetEventFlag(4652, FlagState.On)
        SetEventFlag(4656, FlagState.On)
        """State 5"""
        assert not GetEventFlag(4652)
        """State 6"""
        SetWorkValue(0, 0)
    """State 7"""
    return 0

def t000001000_x35(z28=_, val4=_, z29=1, z30=2, z31=60):
    """State 0,4"""
    assert not DoesPlayerHaveSpEffect(9600) and not DoesPlayerHaveSpEffect(9603)
    """State 1"""
    SpawnDynamicCharacter(2180, 21800000, 1, 3000, z28, z29, z30, z31)
    """State 2"""
    SetEventFlag(4651, FlagState.On)
    """State 3"""
    assert GetCurrentStateElapsedTime() > val4
    """State 5"""
    return 0

def t000001000_x36(flag4=_):
    """State 0"""
    if not GetEventFlag(4651):
        """State 1,8"""
        assert t000001000_x28()
    else:
        """State 4"""
        pass
    """State 3"""
    SetEventFlag(4652, FlagState.On)
    SetEventFlag(flag4, FlagState.On)
    """State 2"""
    assert (not GetEventFlag(4652) or (GetCurrentStateElapsedTime() > 5 and not DoesPlayerHaveSpEffect(9600) and
            not DoesPlayerHaveSpEffect(9603)))
    """State 5"""
    if not GetEventFlag(4680):
        """State 6,9"""
        assert t000001000_x29(z32=20010)
    else:
        """State 7"""
        pass
    """State 10"""
    return 0

def t000001000_x37():
    """State 0,1"""
    SetEventFlag(1054539200, FlagState.On)
    """State 4"""
    assert t000001000_x28()
    """State 2"""
    SetEventFlag(4652, FlagState.On)
    """State 3"""
    assert not GetEventFlag(4652)
    """State 5"""
    return 0

def t000001000_x38():
    """State 0,1"""
    SetEventFlag(1054539201, FlagState.On)
    """State 2"""
    SetEventFlag(1054539205, FlagState.On)
    """State 3"""
    assert GetCurrentStateElapsedTime() > 1.5
    """State 5"""
    SetEventFlag(9000, FlagState.Off)
    SetEventFlag(9020, FlagState.Off)
    """State 4"""
    ChangeCamera(-1)
    Quit()
    """Unused"""
    """State 6"""
    return 0

def t000001000_x39():
    """State 0,1"""
    if not CompareRNGValue(CompareType.Equal, 0) != -1:
        """State 3,4"""
        ShuffleRNGSeed(100)
    else:
        """State 2"""
        pass
    """State 5"""
    SetRNGSeed()
    """State 6"""
    if CompareRNGValue(CompareType.Less, 69) == True:
        """State 7,8"""
        SetWorkValue(0, 0)
    elif CompareRNGValue(CompareType.Less, 99) == True:
        """State 9,10"""
        SetWorkValue(0, 10)
    else:
        """State 11,12"""
        SetWorkValue(0, 0)
    """State 13"""
    return 0

def t000001000_x40():
    """State 0"""
    while True:
        """State 1"""
        if GetEventFlag(1054532702):
            """State 2,7"""
            # actionbutton:6100:"Touch grace"
            # actionbutton:6101:"Rest at site of grace"
            call = t000001000_x65(actionbutton1=6100, actionbutton2=6101, val2=45, z23=-120)
            if call.Done():
                break
            elif not GetEventFlag(1054532702):
                pass
        elif GetEventFlag(11102790):
            """State 4,6"""
            # actionbutton:6102:"Rest at table of lost grace"
            # actionbutton:6103:"Rest at table of lost grace"
            call = t000001000_x44(actionbutton3=6102, actionbutton4=6103, val3=45)
            if call.Done():
                break
            elif not GetEventFlag(11102790):
                pass
        else:
            """State 3,5"""
            # actionbutton:6100:"Touch grace"
            # actionbutton:6101:"Rest at site of grace"
            call = t000001000_x41(actionbutton1=6100, actionbutton2=6101)
            if call.Done():
                break
            elif GetEventFlag(1054532702) or GetEventFlag(11102790):
                pass
    """State 8"""
    return 0

def t000001000_x41(actionbutton1=_, actionbutton2=_):
    """State 0,1"""
    if CompareBonfireLevel(CompareType.Equal, 0):
        """State 2,4"""
        assert t000001000_x3(actionbutton1=actionbutton1, flag8=6001, flag9=6000)
    else:
        """State 3,5"""
        assert t000001000_x3(actionbutton1=actionbutton2, flag8=6001, flag9=6000)
    """State 6"""
    return 0

def t000001000_x42():
    """State 0,7"""
    # action:20011080:"Begin Journey <?nextLoopCount?>?"
    call = t000001000_x0(action7=20011080)
    if call.Get() == 0:
        """State 2,8"""
        # action:20011081:"If you begin Journey <?nextLoopCount?>, you will not be able\nto return to the present world of Journey <?loopCount?>.\nBegin Journey <?nextLoopCount?>?"
        call = t000001000_x0(action7=20011081)
        if call.Get() == 0:
            """State 3,5"""
            SetEventFlag(3001, FlagState.On)
            """State 6"""
            Quit()
        elif call.Done():
            """State 4"""
            pass
    elif call.Done():
        """State 1"""
        pass
    """State 9"""
    return 0

def t000001000_x43(z24=11, z25=12):
    """State 0,2"""
    SetEventFlag(1042379200, FlagState.Off)
    SetEventFlag(1042379202, FlagState.Off)
    SetEventFlag(1042379206, FlagState.Off)
    SetEventFlag(1046389201, FlagState.Off)
    SetEventFlag(1043349250, FlagState.Off)
    SetEventFlag(1038509250, FlagState.Off)
    SetEventFlag(1043539250, FlagState.Off)
    SetEventFlag(11009255, FlagState.Off)
    SetEventFlag(1043509200, FlagState.Off)
    SetEventFlag(1054559200, FlagState.Off)
    SetEventFlag(1036489250, FlagState.Off)
    SetEventFlag(1039519250, FlagState.Off)
    SetEventFlag(1037519200, FlagState.Off)
    SetEventFlag(10009656, FlagState.Off)
    SetEventFlag(11009270, FlagState.Off)
    SetEventFlag(11009275, FlagState.Off)
    SetEventFlag(1054539210, FlagState.Off)
    SetEventFlag(35009350, FlagState.Off)
    SetEventFlag(35009352, FlagState.Off)
    SetEventFlag(1054539215, FlagState.Off)
    """State 4"""
    SetEventFlag(1042379208, FlagState.Off)
    SetEventFlag(11009265, FlagState.Off)
    SetEventFlag(35009355, FlagState.Off)
    SetEventFlag(35009358, FlagState.Off)
    if not GetEventFlag(953):
        """State 1"""
        if not GetEventFlag(4699):
            pass
        else:
            """State 8"""
            assert t000001000_x46(z25=z24)
    elif GetEventFlag(11102790):
        """State 3"""
        pass
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(11009260) and not GetEventFlag(400001):
        """State 5"""
        pass
    elif GetEventFlag(108):
        """State 7"""
        pass
    elif GetEventFlag(110):
        """State 6"""
        pass
    else:
        """State 9"""
        assert t000001000_x49(z24=z24, z25=z25)
    """State 10"""
    return 0

def t000001000_x44(actionbutton3=6102, actionbutton4=6103, val3=45):
    """State 0"""
    if GetRelativeAngleBetweenPlayerAndSelf() < val3:
        """State 1"""
        Label('L0')
        """State 3"""
        call = t000001000_x41(actionbutton1=actionbutton3, actionbutton2=actionbutton4)
        if call.Done():
            """State 4"""
            return 0
        elif not GetRelativeAngleBetweenPlayerAndSelf() < val3:
            pass
    else:
        pass
    """State 2"""
    assert GetRelativeAngleBetweenPlayerAndSelf() < val3
    Goto('L0')

def t000001000_x45(val1=_):
    """State 0,8"""
    assert t000001000_x13()
    """State 10"""
    assert t000001000_x74(val1=val1)
    """State 4"""
    if val1 == 0:
        """State 1"""
        ShowClock(2)
        SetCurrentTime(0, 0, 0, 0, GetMorningHours(), GetMorningMinutes(), GetMorningSeconds(), 2.5, 0.75, 2, 0, 0.75, 0.5)
    elif val1 == 1:
        """State 2"""
        ShowClock(2)
        SetCurrentTime(0, 0, 0, 0, GetNoonHours(), GetNoonMinutes(), GetNoonSeconds(), 2.5, 0.75, 2, 0, 0.75, 0.5)
    elif val1 == 2:
        """State 3"""
        ShowClock(2)
        SetCurrentTime(0, 0, 0, 0, GetNightHours(), GetNightMinutes(), GetNightSeconds(), 2.5, 0.75, 2, 0, 0.75, 0.5)
    """State 5"""
    assert GetCurrentStateElapsedTime() > 0.8
    """State 9"""
    assert t000001000_x29(z32=0)
    """State 6"""
    assert IsTimePassFadeOutInProgress() == False
    """State 7"""
    assert GetCurrentStateElapsedTime() > 2.5
    """State 11"""
    return 0

def t000001000_x46(z25=_):
    """State 0,1"""
    # action:99990301:"Speak with Merina"
    AddTalkListData(z25, 99990301, -1)
    """State 2"""
    return 0

def t000001000_x47():
    """State 0,13"""
    assert t000001000_x48()
    """State 5"""
    CloseShopMessage()
    while True:
        """State 1"""
        ClearTalkListData()
        """State 14"""
        # action:15000370:"Add charge to flask"
        assert t000001000_x69(z22=1, action5=15000370)
        """State 15"""
        # action:15000380:"Increase amount replenished by flasks"
        assert t000001000_x70(z21=2, action4=15000380)
        """State 2"""
        # action:15000385:"Allocate flask charges"
        AddTalkListData(3, 15000385, -1)
        # action:15000372:"Cancel"
        AddTalkListData(99, 15000372, -1)
        """State 3"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 6"""
        if GetTalkListEntryResult() == 1:
            """State 10"""
            # goods:1000:Flask of Crimson Tears
            # goods:1001:Flask of Crimson Tears
            # goods:1002:Flask of Crimson Tears +1
            # goods:1003:Flask of Crimson Tears +1
            # goods:1004:Flask of Crimson Tears +2
            # goods:1005:Flask of Crimson Tears +2
            # goods:1006:Flask of Crimson Tears +3
            # goods:1007:Flask of Crimson Tears +3
            # goods:1008:Flask of Crimson Tears +4
            # goods:1009:Flask of Crimson Tears +4
            # goods:1010:Flask of Crimson Tears +5
            # goods:1011:Flask of Crimson Tears +5
            # goods:1012:Flask of Crimson Tears +6
            # goods:1013:Flask of Crimson Tears +6
            # goods:1014:Flask of Crimson Tears +7
            # goods:1015:Flask of Crimson Tears +7
            # goods:1016:Flask of Crimson Tears +8
            # goods:1017:Flask of Crimson Tears +8
            # goods:1018:Flask of Crimson Tears +9
            # goods:1019:Flask of Crimson Tears +9
            # goods:1020:Flask of Crimson Tears +10
            # goods:1021:Flask of Crimson Tears +10
            # goods:1022:Flask of Crimson Tears +11
            # goods:1023:Flask of Crimson Tears +11
            # goods:1024:Flask of Crimson Tears +12
            # goods:1025:Flask of Crimson Tears +12
            # goods:10010:Golden Seed
            assert t000001000_x7(goods5=1000, goods6=10010)
        elif GetTalkListEntryResult() == 2:
            """State 7"""
            if not GetEventFlag(2051) and not GetEventFlag(2052):
                """State 8,11"""
                # goods:1000:Flask of Crimson Tears
                # goods:1001:Flask of Crimson Tears
                # goods:1002:Flask of Crimson Tears +1
                # goods:1003:Flask of Crimson Tears +1
                # goods:1004:Flask of Crimson Tears +2
                # goods:1005:Flask of Crimson Tears +2
                # goods:1006:Flask of Crimson Tears +3
                # goods:1007:Flask of Crimson Tears +3
                # goods:1008:Flask of Crimson Tears +4
                # goods:1009:Flask of Crimson Tears +4
                # goods:1010:Flask of Crimson Tears +5
                # goods:1011:Flask of Crimson Tears +5
                # goods:1012:Flask of Crimson Tears +6
                # goods:1013:Flask of Crimson Tears +6
                # goods:1014:Flask of Crimson Tears +7
                # goods:1015:Flask of Crimson Tears +7
                # goods:1016:Flask of Crimson Tears +8
                # goods:1017:Flask of Crimson Tears +8
                # goods:1018:Flask of Crimson Tears +9
                # goods:1019:Flask of Crimson Tears +9
                # goods:1020:Flask of Crimson Tears +10
                # goods:1021:Flask of Crimson Tears +10
                # goods:1022:Flask of Crimson Tears +11
                # goods:1023:Flask of Crimson Tears +11
                # goods:1024:Flask of Crimson Tears +12
                # goods:1025:Flask of Crimson Tears +12
                # goods:10020:Sacred Tear
                assert t000001000_x6(goods7=1000, goods8=10020)
            else:
                """State 9,16"""
                # action:20011030:"Cannot select while entering combat"
                assert t000001000_x4(action6=20011030)
        elif GetTalkListEntryResult() == 3:
            """State 12"""
            # goods:1000:Flask of Crimson Tears
            # goods:1050:Flask of Cerulean Tears
            # goods:1001:Flask of Crimson Tears
            # goods:1051:Flask of Cerulean Tears
            # goods:1002:Flask of Crimson Tears +1
            # goods:1052:Flask of Cerulean Tears +1
            # goods:1003:Flask of Crimson Tears +1
            # goods:1053:Flask of Cerulean Tears +1
            # goods:1004:Flask of Crimson Tears +2
            # goods:1054:Flask of Cerulean Tears +2
            # goods:1005:Flask of Crimson Tears +2
            # goods:1055:Flask of Cerulean Tears +2
            # goods:1006:Flask of Crimson Tears +3
            # goods:1056:Flask of Cerulean Tears +3
            # goods:1007:Flask of Crimson Tears +3
            # goods:1057:Flask of Cerulean Tears +3
            # goods:1008:Flask of Crimson Tears +4
            # goods:1058:Flask of Cerulean Tears +4
            # goods:1009:Flask of Crimson Tears +4
            # goods:1059:Flask of Cerulean Tears +4
            # goods:1010:Flask of Crimson Tears +5
            # goods:1060:Flask of Cerulean Tears +5
            # goods:1011:Flask of Crimson Tears +5
            # goods:1061:Flask of Cerulean Tears +5
            # goods:1012:Flask of Crimson Tears +6
            # goods:1062:Flask of Cerulean Tears +6
            # goods:1013:Flask of Crimson Tears +6
            # goods:1063:Flask of Cerulean Tears +6
            # goods:1014:Flask of Crimson Tears +7
            # goods:1064:Flask of Cerulean Tears +7
            # goods:1015:Flask of Crimson Tears +7
            # goods:1065:Flask of Cerulean Tears +7
            # goods:1016:Flask of Crimson Tears +8
            # goods:1066:Flask of Cerulean Tears +8
            # goods:1017:Flask of Crimson Tears +8
            # goods:1067:Flask of Cerulean Tears +8
            # goods:1018:Flask of Crimson Tears +9
            # goods:1068:Flask of Cerulean Tears +9
            # goods:1019:Flask of Crimson Tears +9
            # goods:1069:Flask of Cerulean Tears +9
            # goods:1020:Flask of Crimson Tears +10
            # goods:1070:Flask of Cerulean Tears +10
            # goods:1021:Flask of Crimson Tears +10
            # goods:1071:Flask of Cerulean Tears +10
            # goods:1022:Flask of Crimson Tears +11
            # goods:1072:Flask of Cerulean Tears +11
            # goods:1023:Flask of Crimson Tears +11
            # goods:1073:Flask of Cerulean Tears +11
            # goods:1024:Flask of Crimson Tears +12
            # goods:1074:Flask of Cerulean Tears +12
            # goods:1025:Flask of Crimson Tears +12
            # goods:1075:Flask of Cerulean Tears +12
            assert t000001000_x15(goods9=1000)
        else:
            """State 4,17"""
            return 0

def t000001000_x48():
    """State 0"""
    if not GetEventFlag(720070) or not GetEventFlag(720080):
        """State 1,3"""
        SetEventFlag(720070, FlagState.On)
        SetEventFlag(720080, FlagState.On)
        """State 4"""
    else:
        """State 2"""
        pass
    """State 5"""
    return 0

def t000001000_x49(z24=11, z25=12):
    """State 0"""
    assert GetCurrentStateElapsedFrames() > 1
    """State 1"""
    assert t000001000_x57(z24=z24)
    """State 2"""
    assert t000001000_x58(z25=z25)
    """State 3"""
    return 0

def t000001000_x50():
    """State 0,9"""
    assert t000001000_x28()
    """State 7"""
    SetEventFlag(4652, FlagState.On)
    """State 4"""
    assert (not GetEventFlag(4652) or (GetCurrentStateElapsedTime() > 5 and not DoesPlayerHaveSpEffect(9600) and
            not DoesPlayerHaveSpEffect(9603)))
    """State 1"""
    if not GetEventFlag(4680):
        """State 2,8"""
        Label('L0')
        assert t000001000_x29(z32=20010) and GetCurrentStateElapsedTime() > 3
    elif GetEventFlag(108):
        """State 6"""
        Goto('L0')
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(11009260) and not GetEventFlag(400001):
        """State 5"""
        Goto('L0')
    else:
        """State 3"""
        pass
    """State 10"""
    return 0

def t000001000_x51(z27=15):
    """State 0"""
    if not GetEventFlag(12019257):
        """State 1"""
        if not GetEventFlag(12019255):
            """State 5"""
            # action:21060900:"Talk to miniature Ranni"
            AddTalkListDataAlt(z27, 21060900, -1, 0, False)
        elif not GetEventFlag(12019256):
            """State 6"""
            # action:21060901:"Talk to miniature Ranni"
            AddTalkListDataAlt(z27, 21060901, -1, 0, False)
        else:
            """State 7"""
            # action:21060902:"Talk to miniature Ranni"
            AddTalkListDataAlt(z27, 21060902, -1, 0, False)
    elif not GetEventFlag(12019260):
        """State 2"""
        if not GetEventFlag(12012711):
            """State 8"""
            # action:21060903:"Talk to Ranni"
            AddTalkListDataAltIf(GetEventFlag(12019258) == 0, z27, 21060903, -1, 0, False)
            # action:21060903:"Talk to Ranni"
            AddTalkListDataAltIf(GetEventFlag(12019258) == 1, z27, 21060903, -1, 0, False)
        elif GetEventFlag(1045379208):
            """State 9"""
            # action:21060910:"Talk to Ranni"
            AddTalkListDataAlt(z27, 21060910, -1, 0, True)
        else:
            """State 13"""
            # action:21060911:"Talk to Ranni"
            AddTalkListDataAlt(z27, 21060911, -1, 0, True)
    elif not GetEventFlag(12019265):
        """State 3"""
        if not GetEventFlag(12012712) or not GetEventFlag(1045379208):
            """State 10"""
            # action:21060912:"Talk to Ranni"
            AddTalkListDataAltIf(GetEventFlag(12019261) == 0, z27, 21060912, -1, 0, False)
            # action:21060912:"Talk to Ranni"
            AddTalkListDataAltIf(GetEventFlag(12019261) == 1, z27, 21060912, -1, 0, False)
        else:
            """State 11"""
            # action:21060920:"Talk to Ranni"
            AddTalkListDataAlt(z27, 21060920, -1, 0, True)
    else:
        """State 4,12"""
        # action:21060921:"Talk to Ranni"
        AddTalkListDataAltIf(GetEventFlag(12019266) == 0, z27, 21060921, -1, 0, True)
        # action:21060921:"Talk to Ranni"
        AddTalkListDataAltIf(GetEventFlag(12019266) == 1, z27, 21060921, -1, 0, False)
    """State 14"""
    return 0

def t000001000_x52():
    """State 0"""
    # eventflag:400394:lot:103940:Miniature Ranni
    if (GetEventFlag(400394) and not GetEventFlag(12019280) and (GetEventFlag(12012710) or GetEventFlag(12012711)
        or GetEventFlag(12012712))):
        """State 4"""
        assert t000001000_x51(z27=15)
    # eventflag:400394:lot:103940:Miniature Ranni
    elif GetEventFlag(400394) and GetEventFlag(1034509406) and GetEventFlag(12012713):
        """State 5"""
        assert t000001000_x53(z26=15)
    else:
        """State 3"""
        assert t000001000_x43(z24=11, z25=12)
    """State 1"""
    # action:20010101:"Listen to the sounds of flame"
    AddTalkListDataAltIf(GetEventFlag(1054532702) == 1 and GetEventFlag(108) == 1 and GetEventFlag(110) == 0, 32,
                         20010101, -1, 0, True)
    # action:20010080:"Begin Journey <?nextLoopCount?>"
    AddTalkListDataIf(GetEventFlag(120) == 1 and GetEventFlag(11102790) == 1, 41, 20010080, -1)
    """State 6"""
    return 0
    """Unused"""
    """State 2"""
    Quit()

def t000001000_x53(z26=15):
    """State 0"""
    if not GetEventFlag(12019275):
        """State 1"""
        # action:21060930:"Talk to miniature Ranni"
        AddTalkListDataAlt(z26, 21060930, -1, 0, False)
    else:
        """State 2"""
        # action:21060931:"Talk to Ranni"
        AddTalkListDataAltIf(GetEventFlag(12019276) == 0, z26, 21060931, -1, 0, False)
        # action:21060931:"Talk to Ranni"
        AddTalkListDataAltIf(GetEventFlag(12019276) == 1, z26, 21060931, -1, 0, False)
    """State 3"""
    return 0

def t000001000_x54():
    """State 0"""
    if not GetEventFlag(12012713):
        """State 1"""
        assert t000001000_x55()
    else:
        """State 2"""
        assert t000001000_x56()
    """State 3"""
    return 0

def t000001000_x55():
    """State 0"""
    if not GetEventFlag(12019257):
        """State 1"""
        if not GetEventFlag(12019255):
            """State 5"""
            # talk:10619000:"..."
            assert t000001000_x14(text2=10619000, flag5=12019255, mode4=1)
        elif not GetEventFlag(12019256):
            """State 6"""
            # talk:10619100:"..."
            assert t000001000_x14(text2=10619100, flag5=12019256, mode4=1)
        else:
            """State 7"""
            # talk:10619200:"..."
            # talk:10619201:"Oh? A dogged fellow, aren't we?"
            # talk:10619202:"Or is it merely thy habit, to talk to dolls?"
            # talk:10619203:"Fine...fine."
            # talk:10619204:"I hadn't expected any soul to recognise me in this guise."
            # talk:10619205:"But now the cat is out the bag, I cannot allow thee thy freedoms."
            # talk:10619206:"Perform for me a service, as recompense."
            # talk:10619207:"Eliminate the Baleful Shadows which prowl these lands."
            # talk:10619208:"The name of Ranni the Witch is already sullied by thee."
            # talk:10619209:"I will not brook disobedience in this matter."
            call = t000001000_x14(text2=10619200, flag5=12019257, mode4=1)
            assert call.Done() or call.Done()
    elif not GetEventFlag(12019260):
        """State 2"""
        if not GetEventFlag(12012711):
            """State 11"""
            # talk:10619300:"Perform for me a service, as recompense."
            # talk:10619301:"Eliminate the Baleful Shadows which prowl these lands."
            # talk:10619302:"The name of Ranni the Witch is already sullied by thee."
            # talk:10619303:"I will not brook disobedience in this matter."
            assert t000001000_x14(text2=10619300, flag5=12019258, mode4=1)
        elif GetEventFlag(1045379208):
            """State 8"""
            # talk:10620000:"Let us speak of the past, a while."
            # talk:10620001:"I was once an Empyrean."
            # talk:10620002:"Of the demigods, only I, Miquella, and Malenia could claim that title."
            # talk:10620003:"Each of us was chosen by our own Two Fingers, as a candidate to succeed Queen Marika,\nto become the new god of the coming age."
            # talk:10620004:"Which is when I received Blaidd. In the form of a vassal tailored for an Empyrean."
            # talk:10620005:"But I would not acquiesce to the Two Fingers."
            # talk:10620006:"I stole the Rune of Death, slew mine own Empyrean flesh, casting it away."
            # talk:10620007:"I would not be controlled by that thing."
            # talk:10620008:"The Two Fingers and I have been cursing each other ever since..."
            # talk:10620009:"And the Baleful Shadows...are their assassins."
            assert t000001000_x14(text2=10620000, flag5=12019260, mode4=1)
        else:
            """State 9"""
            # talk:10603000:"Let us speak of the past, a while."
            # talk:10603001:"I was once an Empyrean."
            # talk:10603002:"Of the demigods, only I, Miquella, and Malenia could claim that title."
            # talk:10603003:"Each of us was chosen by our own Two Fingers, as a candidate to succeed Queen Marika, to become the new god of the coming age."
            # talk:10603004:"But I would not acquiesce to the Two Fingers."
            # talk:10603005:"I stole the Rune of Death, slew mine own Empyrean flesh, casting it away."
            # talk:10603006:"I would not be controlled by that thing."
            # talk:10603007:"The Two Fingers and I have been cursing each other ever since..."
            # talk:10603008:"And the Baleful Shadows...are their assassins."
            assert t000001000_x14(text2=10603000, flag5=12019260, mode4=1)
    elif not GetEventFlag(12019265):
        """State 3"""
        if not GetEventFlag(12012712) or not GetEventFlag(1045379208):
            """State 12"""
            # talk:10620100:"I turned my back on the Two Fingers and we have each been cursing the other since."
            # talk:10620101:"The Baleful Shadows...are their assassins."
            assert t000001000_x14(text2=10620100, flag5=12019261, mode4=1)
        else:
            """State 10"""
            # talk:10621000:"Even when I turned my back upon the Two Fingers."
            # talk:10621001:"Blaidd remained my loyal ally."
            # talk:10621002:"Heh."
            # talk:10621003:"Though he was created a vassal for an Empyrean,"
            # talk:10621004:"He was a colossal failure, on the part of the Two Fingers."
            # talk:10621005:"Blaidd, and Iji both... Art willing to give too much to me."
            # talk:10621006:"Yet they both understand. What lieth beyond the dark path..."
            # talk:10621007:"That I must betray everything, and rid the world of what came before."
            # talk:10621008:"Ah, should I add thee to the list?"
            # talk:10621009:"Another one, kind of heart. As kind of heart as they."
            assert t000001000_x14(text2=10621000, flag5=12019265, mode4=1)
    else:
        """State 4,13"""
        # talk:10621100:"Ach, this form hath loosened my tongue."
        # talk:10621101:"I've let slip too much."
        # talk:10621102:"Forget what thou'st heard. Forget."
        assert t000001000_x14(text2=10621100, flag5=12019266, mode4=1)
    """State 14"""
    return 0

def t000001000_x56():
    """State 0"""
    if not GetEventFlag(12019275):
        """State 2"""
        # talk:10625000:"..."
        # talk:10625001:"I take it thou'st noticed? I shouldn't be surprised."
        # talk:10625002:"I thought I might expound a little further..."
        # talk:10625003:"Upon the order I envision."
        # talk:10625004:"Mine will be an order not of gold, but the stars and moon of the chill night."
        # talk:10625005:"I would keep them far from the earth beneath our feet."
        # talk:10625006:"As it is now, life, and souls, and order are bound tightly together, but I would have them at a great remove."
        # talk:10625007:"And have the certainties of sight, emotion, faith, and touch..."
        # talk:10625008:"All become impossibilities."
        # talk:10625009:"Which is why I would abandon this soil, with mine order."
        # talk:10625010:"Wouldst thou come to me, even now, my one and only Lord?"
        assert t000001000_x14(text2=10625000, flag5=12019275, mode4=1)
    else:
        """State 3"""
        # talk:10625100:"Mine will be an order not of gold, but the stars and moon of the chill night."
        # talk:10625101:"And I would abandon this soil, with mine Order."
        # talk:10625102:"Wouldst thou come to me, even now, my one and only Lord?"
        assert t000001000_x14(text2=10625100, flag5=12019276, mode4=1)
    """State 1"""
    SetEventFlag(1034509407, FlagState.On)
    """State 4"""
    return 0

def t000001000_x57(z24=11):
    """State 0,7"""
    if not GetEventFlag(4680):
        """State 4"""
        if not GetEventFlag(1042372700):
            """State 2"""
            # action:21000001:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000001, -1, 0, True)
            SetEventFlag(1042379200, FlagState.On)
        elif GetEventFlag(4699):
            """State 31"""
            assert t000001000_x46(z25=z24)
        else:
            """State 5"""
            pass
    else:
        """State 6"""
        if (GetEventFlag(10009655) and not GetEventFlag(105) and not DoesPlayerHaveSpEffect(4270) and not DoesPlayerHaveSpEffect(4271)
            and not DoesPlayerHaveSpEffect(4272) and not DoesPlayerHaveSpEffect(4280) and not DoesPlayerHaveSpEffect(4282)
            and not DoesPlayerHaveSpEffect(4286)):
            """State 18"""
            # action:21000050:"Tell her you're off to Roundtable Hold"
            AddTalkListDataAlt(z24, 21000050, -1, 0, True)
            SetEventFlag(10009656, FlagState.On)
        elif GetEventFlag(1042372701) and not GetEventFlag(1042379203) and not GetEventFlag(10009655):
            """State 3"""
            # action:21000002:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000002, -1, 0, True)
            SetEventFlag(1042379202, FlagState.On)
        elif GetEventFlag(1042372703):
            """State 28"""
            SetEventFlag(1042379208, FlagState.On)
            # action:21000004:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1042379209) == 0, z24, 21000004, -1, 0, True)
            # action:21000004:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1042379209) == 1, z24, 21000004, -1, 0, False)
        elif (not GetEventFlag(1042372702) and not GetEventFlag(1042379207) and GetEventFlag(1042379203) and not
              GetEventFlag(10009655)):
            """State 8"""
            # action:21000003:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000003, -1, 0, True)
            SetEventFlag(1042379206, FlagState.On)
        elif GetEventFlag(1046382701) and not GetEventFlag(1046389202):
            """State 9"""
            SetEventFlag(1046389201, FlagState.On)
            # action:21000005:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1046389203) == 0 and GetEventFlag(1046382700) == 0, z24, 21000005,
                                 -1, 0, True)
            # action:21000005:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1046389203) == 1 and GetEventFlag(1046382700) == 0, z24, 21000005,
                                 -1, 0, False)
            # action:21000006:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000006, -1)
        elif GetEventFlag(1043342700) and not GetEventFlag(1043349251):
            """State 10"""
            SetEventFlag(1043349250, FlagState.On)
            # action:21000007:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043349252) == 0 and GetEventFlag(1046382700) == 0, z24, 21000007,
                                 -1, 0, True)
            # action:21000007:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043349252) == 1 and GetEventFlag(1046382700) == 0, z24, 21000007,
                                 -1, 0, False)
            # action:21000008:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000008, -1)
        elif GetEventFlag(1038502710) and not GetEventFlag(1038509251):
            """State 11"""
            SetEventFlag(1038509250, FlagState.On)
            # action:21000009:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1038509252) == 0 and GetEventFlag(1046382700) == 0, z24, 21000009,
                                 -1, 0, True)
            # action:21000009:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1038509252) == 1 and GetEventFlag(1046382700) == 0, z24, 21000009,
                                 -1, 0, False)
            # action:21000010:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000010, -1)
        elif GetEventFlag(1043532710) and not GetEventFlag(1043539251):
            """State 12"""
            SetEventFlag(1043539250, FlagState.On)
            # action:21000011:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043539252) == 0 and GetEventFlag(1046382700) == 0, z24, 21000011,
                                 -1, 0, True)
            # action:21000011:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043539252) == 1 and GetEventFlag(1046382700) == 0, z24, 21000011,
                                 -1, 0, False)
            # action:21000012:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000012, -1)
        elif GetEventFlag(11002740) and not GetEventFlag(11009256):
            """State 13"""
            SetEventFlag(11009255, FlagState.On)
            # action:21000013:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(11009257) == 0 and GetEventFlag(1046382700) == 0, z24, 21000013,
                                 -1, 0, True)
            # action:21000013:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(11009257) == 1 and GetEventFlag(1046382700) == 0, z24, 21000013,
                                 -1, 0, False)
            # action:21000014:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000014, -1)
        elif GetEventFlag(1043502700) and not GetEventFlag(1043509201):
            """State 25"""
            SetEventFlag(1043509200, FlagState.On)
            # action:21000015:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043509202) == 0 and GetEventFlag(1046382700) == 0, z24, 21000015,
                                 -1, 0, True)
            # action:21000015:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1043509202) == 1 and GetEventFlag(1046382700) == 0, z24, 21000015,
                                 -1, 0, False)
            # action:21000016:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000016, -1)
        elif GetEventFlag(1054552700) and not GetEventFlag(1054559201):
            """State 14"""
            SetEventFlag(1054559200, FlagState.On)
            # action:21000017:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1054559202) == 0 and GetEventFlag(1046382700) == 0, z24, 21000017,
                                 -1, 0, True)
            # action:21000017:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1054559202) == 1 and GetEventFlag(1046382700) == 0, z24, 21000017,
                                 -1, 0, False)
            # action:21000018:"Talk to Melina"
            AddTalkListDataIf(GetEventFlag(1046382700) == 1, z24, 21000018, -1)
        # eventflag:400001:lot:100010:Rold Medallion
        elif (not GetEventFlag(1037519201) and not GetEventFlag(11009260) and not GetEventFlag(400001) and (GetEventFlag(1037512700)
              or GetEventFlag(1038512700) or GetEventFlag(1038502711) or GetEventFlag(1039512711) or GetEventFlag(1037522700))):
            """State 17"""
            # action:21000022:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000022, -1, 0, True)
            SetEventFlag(1037519200, FlagState.On)
        elif GetEventFlag(1036482710) and GetEventFlag(1036489213) and GetEventFlag(3940) and not GetEventFlag(1036489251):
            """State 15"""
            # action:21000020:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000020, -1, 0, True)
            SetEventFlag(1036489250, FlagState.On)
        elif (GetEventFlag(1039512710) and GetEventFlag(1039519209) and GetEventFlag(1036489210) and GetEventFlag(3940)
              and not GetEventFlag(1039519251)):
            """State 16"""
            SetEventFlag(1039519250, FlagState.On)
            # action:21000021:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000021, -1, 0, True)
        elif GetEventFlag(11002745):
            """State 29"""
            # action:21000023:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(11009266) == 0, z24, 21000023, -1, 0, False)
            # action:21000023:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(11009266) == 1, z24, 21000023, -1, 0, False)
            SetEventFlag(11009265, FlagState.On)
        elif ((GetEventFlag(1054552701) or GetEventFlag(1052562700) or GetEventFlag(1052542700) or GetEventFlag(1051532700)
              or GetEventFlag(1052532710)) and not GetEventFlag(1054539211)):
            """State 21"""
            SetEventFlag(1054539210, FlagState.On)
            # action:21000026:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000026, -1, 0, True)
        elif GetEventFlag(1054532702):
            """State 22"""
            SetEventFlag(1054539215, FlagState.On)
            # action:21000027:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1054539216) == 0, z24, 21000027, -1, 0, True)
            # action:21000027:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(1054539216) == 1, z24, 21000027, -1, 0, True)
        elif (GetEventFlag(35002730) or GetEventFlag(35002731)) and not GetEventFlag(35009351):
            """State 23"""
            SetEventFlag(35009350, FlagState.On)
            # action:21000028:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000028, -1, 0, True)
        elif GetEventFlag(35002731) and not GetEventFlag(35009353):
            """State 24"""
            SetEventFlag(35009352, FlagState.On)
            # action:21000030:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000030, -1, 0, True)
        elif GetEventFlag(35002732) and not GetEventFlag(35002733):
            """State 26"""
            # action:21000029:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(35009356) == 0 and GetEventFlag(35009357) == 0, z24, 21000029, -1,
                                 0, False)
            # action:21000029:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(35009356) == 1 or GetEventFlag(35009357) == 1, z24, 21000029, -1,
                                 0, False)
            SetEventFlag(35009355, FlagState.On)
        elif GetEventFlag(35002733):
            """State 27"""
            # action:21000031:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(35009359) == 0, z24, 21000031, -1, 0, False)
            # action:21000031:"Talk to Melina"
            AddTalkListDataAltIf(GetEventFlag(35009359) == 1, z24, 21000031, -1, 0, False)
            SetEventFlag(35009358, FlagState.On)
        elif GetEventFlag(11109387) and not GetEventFlag(11009271):
            """State 19"""
            SetEventFlag(11009270, FlagState.On)
            # action:21000024:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000024, -1, 0, True)
        elif GetEventFlag(1049539207) and not GetEventFlag(11009276):
            """State 20"""
            SetEventFlag(11009275, FlagState.On)
            # action:21000025:"Talk to Melina"
            AddTalkListDataAlt(z24, 21000025, -1, 0, True)
        elif GetEventFlag(4699):
            """State 30"""
            assert t000001000_x46(z25=z24)
        else:
            """State 1"""
            pass
    """State 32"""
    return 0

def t000001000_x58(z25=12):
    """State 0,5"""
    if not GetEventFlag(4680):
        """State 2"""
        if GetEventFlag(4699):
            """State 7"""
            assert t000001000_x46(z25=z25)
        else:
            """State 3"""
            pass
    else:
        """State 4"""
        if GetEventFlag(4699):
            """State 6"""
            assert t000001000_x46(z25=z25)
        else:
            """State 1"""
            pass
    """State 8"""
    return 0

def t000001000_x59():
    """State 0"""
    if GetEventFlag(953):
        """State 3,1"""
        SetEventFlag(4653, FlagState.On)
    else:
        """State 2"""
        pass
    """State 4"""
    return 0

def t000001000_x60():
    """State 0"""
    if (GetEventFlag(10000851) and not GetEventFlag(10009655) and not DoesPlayerHaveSpEffect(4270) and not DoesPlayerHaveSpEffect(4271)
        and not DoesPlayerHaveSpEffect(4272) and not DoesPlayerHaveSpEffect(4280) and not DoesPlayerHaveSpEffect(4282)
        and not DoesPlayerHaveSpEffect(4286)):
        """State 2,3"""
        Label('L0')
        SetEventFlag(4653, FlagState.On)
    elif ((GetEventFlag(3062) or GetEventFlag(3063) or GetEventFlag(3064) or GetEventFlag(3065)) and not GetEventFlag(10009655)
          and not DoesPlayerHaveSpEffect(4270) and not DoesPlayerHaveSpEffect(4271) and not DoesPlayerHaveSpEffect(4272)
          and not DoesPlayerHaveSpEffect(4280) and not DoesPlayerHaveSpEffect(4282) and not DoesPlayerHaveSpEffect(4286)):
        """State 4"""
        Goto('L0')
    # eventflag:400001:lot:100010:Rold Medallion
    elif (not GetEventFlag(11009260) and not GetEventFlag(400001) and not GetEventFlag(9104) and (GetEventFlag(11002741)
          or GetEventFlag(11002742) or GetEventFlag(11002743) or GetEventFlag(11002744))):
        """State 5"""
        Goto('L0')
    # eventflag:400001:lot:100010:Rold Medallion
    elif GetEventFlag(9104) and not GetEventFlag(400001):
        """State 6"""
        Goto('L0')
    else:
        """State 1"""
        pass
    """State 7"""
    return 0

def t000001000_x61():
    """State 0"""
    # eventflag:400001:lot:100010:Rold Medallion
    if GetEventFlag(9104) and not GetEventFlag(400001):
        """State 2,1"""
        SetEventFlag(4653, FlagState.On)
    else:
        """State 3"""
        pass
    """State 4"""
    return 0

def t000001000_x62():
    """State 0"""
    if not GetEventFlag(35009360):
        """State 3,1"""
        SetEventFlag(4653, FlagState.On)
    else:
        """State 2"""
        pass
    """State 4"""
    return 0

def t000001000_x63():
    """State 0"""
    while True:
        """State 1"""
        if CompareBonfireLevel(CompareType.Equal, 0):
            """State 2"""
            # actionbutton:6100:"Touch grace"
            assert t000001000_x5(actionbutton5=6100, flag6=6001, flag7=6000)
        else:
            """State 3"""
            # actionbutton:6101:"Rest at site of grace"
            assert t000001000_x3(actionbutton1=6101, flag8=6001, flag9=6000)
        """State 4"""
        # action:20011020:"Cannot rest at sites of grace right now"
        assert t000001000_x4(action6=20011020)
    """Unused"""
    """State 5"""
    return 0

def t000001000_x64():
    """State 0,2"""
    if GetCurrentStateElapsedTime() > 0.8:
        """State 3"""
        GiveSpEffectToPlayer(9606)
        def WhilePaused():
            GiveSpEffectToPlayer(9606)
        def ExitPause():
            GiveSpEffectToPlayer(9606)
        if IsTimePassFadeOutInProgress() == False:
            pass
        elif GetEventFlag(9001):
            """State 1"""
            Label('L0')
    elif GetEventFlag(9001):
        Goto('L0')
    """State 4"""
    return 0

def t000001000_x65(actionbutton1=6100, actionbutton2=6101, val2=45, z23=-120):
    """State 0"""
    if RelativeAngleBetweenTwoPlayersWithAxis(z23) < val2:
        """State 1"""
        Label('L0')
        """State 3"""
        call = t000001000_x41(actionbutton1=actionbutton1, actionbutton2=actionbutton2)
        if call.Done():
            """State 4"""
            return 0
        elif not RelativeAngleBetweenTwoPlayersWithAxis(z23) < val2:
            pass
    else:
        pass
    """State 2"""
    assert RelativeAngleBetweenTwoPlayersWithAxis(z23) < val2
    Goto('L0')

def t000001000_x66():
    """State 0,2"""
    if GetCurrentStateElapsedTime() > 0.8:
        """State 3"""
        GiveSpEffectToPlayer(9610)
        def WhilePaused():
            GiveSpEffectToPlayer(9610)
        def ExitPause():
            GiveSpEffectToPlayer(9610)
        if IsTimePassFadeOutInProgress() == False:
            pass
        elif GetEventFlag(9001):
            """State 1"""
            Label('L0')
    elif GetEventFlag(9001):
        Goto('L0')
    """State 4"""
    return 0

def t000001000_x67():
    """State 0"""
    # eventflag:400001:lot:100010:Rold Medallion
    if GetEventFlag(400001) and not GetEventFlag(108) and not GetEventFlag(11002745):
        """State 1,3"""
        assert t000001000_x29(z32=20011)
    else:
        """State 2,4"""
        assert t000001000_x29(z32=20010)
    """State 5"""
    return 0

def t000001000_x68():
    """State 0"""
    if GetEventFlag(1054532702):
        """State 1"""
        if GetEventFlag(110) and not GetEventFlag(1054532703) and not GetEventFlag(9116):
            """State 3,7"""
            SetEventFlag(9000, FlagState.Off)
            SetEventFlag(9020, FlagState.Off)
            """State 6"""
            ChangeCamera(-1)
            """State 5"""
            SetEventFlag(1054539206, FlagState.On)
            assert GetCurrentStateElapsedTime() > 15
            """State 8"""
            ChangeCameraIf(GetEventFlag(11102790) == 0, 1001000)
            SetEventFlag(9000, FlagState.On)
            SetEventFlag(9020, FlagState.On)
            SetEventFlag(1054539206, FlagState.Off)
        else:
            """State 4"""
            pass
    else:
        """State 2"""
        pass
    """State 9"""
    return 0

def t000001000_x69(z22=1, action5=15000370):
    """State 0,5"""
    SetWorkValue(1, GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) + -4)
    """State 6"""
    assert t000001000_x21(z33=1, z34=1, z35=2, z36=2, z37=3, z38=3, z39=4, z40=4, z41=5, z42=5, z43=1)
    """State 3"""
    # goods:10010:Golden Seed
    if (ComparePlayerInventoryNumber(ItemType.Goods, 10010, CompareType.GreaterOrEqual, GetWorkValue(1), False)
        and GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) < 13):
        """State 1"""
        # action:15000370:"Add charge to flask"
        AddTalkListDataAlt(z22, action5, -1, 0, True)
    else:
        """State 2"""
        # action:15000370:"Add charge to flask"
        AddTalkListDataAlt(z22, action5, -1, 0, False)
    """State 4"""
    SetWorkValue(1, 0)
    """State 7"""
    return 0

def t000001000_x70(z21=2, action4=15000380):
    """State 0,3"""
    # goods:10020:Sacred Tear
    if (ComparePlayerInventoryNumber(ItemType.Goods, 10020, CompareType.GreaterOrEqual, 1, False) and GetTotalBonfireLevel()
        <= 13):
        """State 1"""
        # action:15000380:"Increase amount replenished by flasks"
        AddTalkListDataAlt(z21, action4, -1, 0, True)
    else:
        """State 2"""
        # action:15000380:"Increase amount replenished by flasks"
        AddTalkListDataAlt(z21, action4, -1, 0, False)
    """State 4"""
    return 0

def t000001000_x71(z20=3, action3=15000371):
    """State 0,4"""
    SetWorkValue(1, GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) + -4)
    """State 7"""
    assert t000001000_x21(z33=1, z34=1, z35=2, z36=2, z37=3, z38=3, z39=4, z40=4, z41=5, z42=5, z43=1)
    """State 3"""
    # goods:10010:Golden Seed
    if (ComparePlayerInventoryNumber(ItemType.Goods, 10010, CompareType.NotEqual, GetWorkValue(1), False) or not
        GetEstusAllocation(EstusType.HP) + GetEstusAllocation(EstusType.FP) < 13):
        """State 2"""
        # goods:10020:Sacred Tear
        if (ComparePlayerInventoryNumber(ItemType.Goods, 10020, CompareType.Less, 0, False) or not GetTotalBonfireLevel()
            <= 13):
            """State 5"""
            # action:15000371:"Flasks"
            AddTalkListDataAlt(z20, action3, -1, 0, False)
        else:
            """State 1"""
            Label('L0')
            # action:15000371:"Flasks"
            AddTalkListDataAlt(z20, action3, -1, 0, True)
    else:
        Goto('L0')
    """State 6"""
    SetWorkValue(1, 0)
    """State 8"""
    return 0

def t000001000_x72():
    """State 0,1"""
    SetEventFlag(4820, FlagState.Off)
    SetEventFlag(4821, FlagState.Off)
    SetEventFlag(4822, FlagState.Off)
    """State 2"""
    SetEventFlag(4825, FlagState.Off)
    SetEventFlag(4826, FlagState.Off)
    SetEventFlag(4827, FlagState.Off)
    """State 3"""
    return 0

def t000001000_x73(flag1=_, flag2=_, flag3=_):
    """State 0,1"""
    SetEventFlag(flag1, FlagState.On)
    """State 2"""
    SetEventFlag(flag2, FlagState.Off)
    SetEventFlag(flag3, FlagState.Off)
    """State 3"""
    return 0

def t000001000_x74(val1=_):
    """State 0,1"""
    if val1 == 0:
        """State 2,18"""
        assert t000001000_x73(flag1=4825, flag2=4826, flag3=4827)
        """State 5"""
        if IsTimeOfDayInRange(6, 0, 0, 11, 59, 59):
            """State 6,21"""
            Label('L0')
            assert t000001000_x73(flag1=4822, flag2=4820, flag3=4821)
        elif IsTimeOfDayInRange(12, 0, 0, 19, 59, 59):
            """State 7,22"""
            Label('L1')
            assert t000001000_x73(flag1=4821, flag2=4820, flag3=4822)
        elif IsTimeOfDayInRange(20, 0, 0, 5, 59, 59):
            """State 8,23"""
            Label('L2')
            assert t000001000_x73(flag1=4820, flag2=4821, flag3=4822)
        else:
            """State 9"""
            Label('L3')
    elif val1 == 1:
        """State 3,19"""
        assert t000001000_x73(flag1=4826, flag2=4825, flag3=4827)
        """State 10"""
        if IsTimeOfDayInRange(6, 0, 0, 11, 59, 59):
            """State 11"""
            Goto('L2')
        elif IsTimeOfDayInRange(12, 0, 0, 19, 59, 59):
            """State 12"""
            Goto('L0')
        elif IsTimeOfDayInRange(20, 0, 0, 5, 59, 59):
            """State 13"""
            Goto('L1')
        else:
            Goto('L3')
    elif val1 == 2:
        """State 4,20"""
        assert t000001000_x73(flag1=4827, flag2=4825, flag3=4826)
        """State 14"""
        if IsTimeOfDayInRange(6, 0, 0, 11, 59, 59):
            """State 15"""
            Goto('L1')
        elif IsTimeOfDayInRange(12, 0, 0, 19, 59, 59):
            """State 16"""
            Goto('L2')
        elif IsTimeOfDayInRange(20, 0, 0, 5, 59, 59):
            """State 17"""
            Goto('L0')
        else:
            Goto('L3')
    else:
        Goto('L3')
    """State 24"""
    return 0

def t000001000_x75(goods3=2010000):
    """State 0,1"""
    if GetEventFlag(720300):
        """State 2"""
        pass
    else:
        """State 3,5"""
        SetEventFlag(720300, FlagState.On)
    """State 6,4"""
    if GetScadutreeLevel() <= 20:
        """State 7,21"""
        assert t000001000_x81(z5=1, z6=2, z7=3, z8=2)
        """State 18"""
        call = t000001000_x0(action7=20011039 + GetWorkValue(2))
        if call.Get() == 0:
            """State 9,11"""
            # goods:2010000:Scadutree Fragment
            if (ComparePlayerInventoryNumber(ItemType.Goods, goods3, CompareType.GreaterOrEqual, GetWorkValue(2),
                False)):
                """State 12,13"""
                # goods:2010000:Scadutree Fragment
                PlayerEquipmentQuantityChange(ItemType.Goods, goods3, GetWorkValue(2) * -1)
                """State 15"""
                SetScadutreeLevel(GetScadutreeLevel() + 1)
                """State 20"""
                # action:20011062:"Scadutree Blessing empowered"
                assert t000001000_x4(action6=20011062)
                """State 16"""
                SetWorkValue(2, 0)
            else:
                """State 14,19"""
                # action:20011060:"Not enough Scadutree Fragments"
                assert t000001000_x4(action6=20011060)
        elif call.Done():
            """State 10"""
            pass
    else:
        """State 8,17"""
        # action:20011064:"Scadutree Blessing cannot be empowered any further"
        assert t000001000_x4(action6=20011064)
    """State 22"""
    return 0

def t000001000_x76(goods4=2010100):
    """State 0,1"""
    if GetEventFlag(720310):
        """State 2"""
        pass
    else:
        """State 3,4"""
        SetEventFlag(720310, FlagState.On)
    """State 5,6"""
    if GetReveredSpiritAshLevel() <= 10:
        """State 7,18"""
        assert t000001000_x77(z9=1, z10=1, z11=1, z12=2, z13=2, z14=3, z15=3, z16=3, z17=4, z18=5, z19=2, mode2=1)
        """State 19"""
        call = t000001000_x0(action7=20011049 + GetWorkValue(2))
        if call.Get() == 0:
            """State 9,11"""
            # goods:2010100:Revered Spirit Ash
            if (ComparePlayerInventoryNumber(ItemType.Goods, goods4, CompareType.GreaterOrEqual, GetWorkValue(2),
                False)):
                """State 12,13"""
                # goods:2010100:Revered Spirit Ash
                PlayerEquipmentQuantityChange(ItemType.Goods, goods4, GetWorkValue(2) * -1)
                """State 15"""
                SetReveredSpiritAshLevel(GetReveredSpiritAshLevel() + 1)
                """State 21"""
                # action:20011063:"Revered Spirit Ash Blessing empowered"
                assert t000001000_x4(action6=20011063)
                """State 16"""
                SetWorkValue(2, 0)
            else:
                """State 14,20"""
                # action:20011061:"Not enough Revered Spirit Ashes"
                assert t000001000_x4(action6=20011061)
        elif call.Done():
            """State 10"""
            pass
    else:
        """State 8,17"""
        # action:20011065:"Revered Spirit Ash Blessing cannot be empowered any further"
        assert t000001000_x4(action6=20011065)
    """State 22"""
    return 0

def t000001000_x77(z9=1, z10=1, z11=1, z12=2, z13=2, z14=3, z15=3, z16=3, z17=4, z18=5, z19=2, mode2=_):
    """State 0,13"""
    SetWorkValue(z19, 0)
    """State 14"""
    if mode2 == 0:
        """State 15,16"""
        SetWorkValue(z19, GetScadutreeLevel())
    else:
        """State 17,18"""
        SetWorkValue(z19, GetReveredSpiritAshLevel())
    """State 19,1"""
    if GetWorkValue(z19) == 0:
        """State 2"""
        SetWorkValue(z19, z9)
    elif GetWorkValue(z19) == 1:
        """State 3"""
        SetWorkValue(z19, z10)
    elif GetWorkValue(z19) == 2:
        """State 4"""
        SetWorkValue(z19, z11)
    elif GetWorkValue(z19) == 3:
        """State 5"""
        SetWorkValue(z19, z12)
    elif GetWorkValue(z19) == 4:
        """State 6"""
        SetWorkValue(z19, z13)
    elif GetWorkValue(z19) == 5:
        """State 7"""
        SetWorkValue(z19, z14)
    elif GetWorkValue(z19) == 6:
        """State 8"""
        SetWorkValue(z19, z15)
    elif GetWorkValue(z19) == 7:
        """State 9"""
        SetWorkValue(z19, z16)
    elif GetWorkValue(z19) == 8:
        """State 10"""
        SetWorkValue(z19, z17)
    elif GetWorkValue(z19) == 9:
        """State 11"""
        SetWorkValue(z19, z18)
    else:
        """State 12"""
        SetWorkValue(z19, 999)
    """State 20"""
    return 0

def t000001000_x78(goods3=2010000, goods4=2010100):
    """State 0,2"""
    CloseShopMessage()
    while True:
        """State 1"""
        ClearTalkListData()
        """State 3,8"""
        # action:20010002:"Scadutree Blessing (<?dlcPlayerDopingLevel?>)"
        assert t000001000_x79(z4=1, action2=20010002, mode2=0, goods3=goods3)
        """State 9"""
        # action:20010003:"Revered Spirit Ash Blessing (<?dlcBuddyDopingLevel?>)"
        assert t000001000_x79(z4=2, action2=20010003, mode2=1, goods3=goods4)
        """State 4"""
        # action:20010004:"Cancel"
        AddTalkListData(99, 20010004, -1)
        """State 5"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 6"""
        if GetTalkListEntryResult() == 1:
            """State 10"""
            assert t000001000_x75(goods3=goods3)
        elif GetTalkListEntryResult() == 2:
            """State 11"""
            assert t000001000_x76(goods4=goods4)
        else:
            """State 7,12"""
            return 0

def t000001000_x79(z4=_, action2=_, mode2=_, goods3=_):
    """State 0,4,5"""
    if mode2 == 0:
        """State 6,8"""
        if GetScadutreeLevel() <= 20:
            """State 9,17"""
            assert t000001000_x81(z5=1, z6=2, z7=3, z8=2)
            """State 1"""
            Label('L0')
            if (ComparePlayerInventoryNumber(ItemType.Goods, goods3, CompareType.GreaterOrEqual, GetWorkValue(2),
                False)):
                """State 2,12"""
                AddTalkListDataAlt(z4, action2, -1, 0, True)
            else:
                """State 3,13"""
                Label('L1')
                AddTalkListDataAlt(z4, action2, -1, 0, False)
        else:
            """State 10"""
            Label('L2')
            Goto('L1')
    else:
        """State 7,11"""
        if GetReveredSpiritAshLevel() <= 10:
            """State 15,16"""
            assert (t000001000_x77(z9=1, z10=1, z11=1, z12=2, z13=2, z14=3, z15=3, z16=3, z17=4, z18=5, z19=2,
                    mode2=mode2))
            Goto('L0')
        else:
            Goto('L2')
    """State 14"""
    SetWorkValue(2, 0)
    """State 18"""
    return 0

def t000001000_x80(z3=50, action1=20010001, goods1=2010000, goods2=2010100):
    """State 0,1,2"""
    if GetEntityID() > 20000000 and GetEntityID() < 28999999:
        """State 3"""
        Label('L0')
        """State 7,16"""
        assert t000001000_x81(z5=1, z6=2, z7=3, z8=2)
        """State 8"""
        # goods:2010000:Scadutree Fragment
        if ComparePlayerInventoryNumber(ItemType.Goods, goods1, CompareType.NotEqual, GetWorkValue(2), False):
            """State 9,15"""
            assert t000001000_x77(z9=1, z10=1, z11=1, z12=2, z13=2, z14=3, z15=3, z16=3, z17=4, z18=5, z19=2, mode2=1)
            """State 10"""
            # goods:2010100:Revered Spirit Ash
            if ComparePlayerInventoryNumber(ItemType.Goods, goods2, CompareType.NotEqual, GetWorkValue(2), False):
                """State 12"""
                # action:20010001:"Shadow Realm Blessing"
                AddTalkListDataAlt(z3, action1, -1, 0, False)
            else:
                """State 13"""
                Label('L1')
                """State 11"""
                # action:20010001:"Shadow Realm Blessing"
                AddTalkListDataAlt(z3, action1, -1, 0, True)
        else:
            Goto('L1')
        """State 14"""
        SetWorkValue(2, 0)
    else:
        """State 4"""
        if GetEntityID() > 40000000 and GetEntityID() < 43999999:
            Goto('L0')
        else:
            """State 5"""
            if GetEntityID() > 2000000000 and GetEntityID() < 2099999999:
                Goto('L0')
            else:
                """State 6"""
                pass
    """State 17"""
    return 0

def t000001000_x81(z5=1, z6=2, z7=3, z8=2):
    """State 0,6"""
    SetWorkValue(z8, 0)
    """State 7,8"""
    SetWorkValue(z8, GetScadutreeLevel())
    """State 9,1"""
    if GetWorkValue(z8) <= 1:
        """State 2"""
        SetWorkValue(z8, z5)
    elif GetWorkValue(z8) <= 9:
        """State 3"""
        SetWorkValue(z8, z6)
    elif GetWorkValue(z8) <= 20:
        """State 4"""
        SetWorkValue(z8, z7)
    else:
        """State 5"""
        SetWorkValue(z8, 999)
    """State 10"""
    return 0

def t000001000_x82():
    """State 0,5"""
    SetEventFlag(4828, FlagState.Off)
    SetEventFlag(4829, FlagState.Off)
    SetEventFlag(4830, FlagState.Off)
    """State 1"""
    if GetEntityID() > 2045420950 and GetEntityID() < 2045420950:
        """State 2,3"""
        SetEventFlag(4828, FlagState.On)
        """State 8"""
        SetEventFlag(4830, FlagState.On)
    elif GetEntityID() > 21010953 and GetEntityID() < 21010953:
        """State 6,7"""
        SetEventFlag(4829, FlagState.On)
    else:
        """State 4"""
        pass
    """State 9"""
    return 0

def t000001000_x83():
    """State 0,1"""
    if GetEntityID() > 2048420950 and GetEntityID() < 2048420950:
        """State 2,3"""
        SetEventFlag(2048422709, FlagState.On)
    elif GetEntityID() > 21010953 and GetEntityID() < 21010953:
        """State 4,6"""
        SetEventFlag(21012732, FlagState.On)
    elif GetEntityID() > 2049390950 and GetEntityID() < 2049390950:
        """State 7,8"""
        SetEventFlag(2049392710, FlagState.On)
    else:
        """State 5"""
        pass
    """State 9"""
    return 0

def t000001000_x84():
    """State 0,1"""
    if ((GetEntityID() > 20000000 and GetEntityID() < 28999999) or (GetEntityID() > 40000000 and GetEntityID()
        < 43999999) or (GetEntityID() > 2000000000 and GetEntityID() < 2099999999)):
        """State 2,4"""
        return 0
    else:
        """State 3,5"""
        return 1

def t000001000_x85():
    """State 0,2"""
    if GetEventFlag(69560):
        """State 3,1"""
        Label('L0')
        AddTalkListData(75, 20010070, -1)
    else:
        """State 4,5"""
        if (ComparePlayerInventoryNumber(ItemType.Goods, 2009600, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods,
            2009610, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 2009620,
            CompareType.GreaterOrEqual, 1, False)):
            """State 6,8"""
            SetEventFlag(69560, FlagState.On)
            """State 9"""
            assert t000001000_x86()
            Goto('L0')
        else:
            """State 7"""
            pass
    """State 10"""
    return 0

def t000001000_x86():
    """State 0,1"""
    assert GetCurrentStateElapsedTime() > 0.5
    """State 2"""
    assert t000001000_x4(action6=20011070)
    """State 3"""
    return 0

def t000001000_x87():
    """State 0,1"""
    CloseShopMessage()
    while True:
        """State 2"""
        ClearTalkListData()
        """State 11"""
        assert t000001000_x89(flag2=6700)
        """State 12"""
        assert t000001000_x88(goods1=2009600, flag3=6701, z1=2, action3=20010076, action4=20010072)
        """State 13"""
        assert t000001000_x88(goods1=2009610, flag3=6702, z1=3, action3=20010077, action4=20010073)
        """State 14"""
        assert t000001000_x88(goods1=2009620, flag3=6703, z1=4, action3=20010078, action4=20010074)
        """State 3"""
        AddTalkListData(99, 20010079, -1)
        """State 4"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 5"""
        if GetTalkListEntryResult() == 1:
            """State 6,15"""
            assert t000001000_x90(flag1=6700, action1=20011075, action2=20011071)
        elif GetTalkListEntryResult() == 2:
            """State 7,16"""
            assert t000001000_x90(flag1=6701, action1=20011076, action2=20011072)
        elif GetTalkListEntryResult() == 3:
            """State 8,17"""
            assert t000001000_x90(flag1=6702, action1=20011077, action2=20011073)
        elif GetTalkListEntryResult() == 4:
            """State 9,18"""
            assert t000001000_x90(flag1=6703, action1=20011078, action2=20011074)
        else:
            """State 10,19"""
            return 0

def t000001000_x88(goods1=_, flag3=_, z1=_, action3=_, action4=_):
    """State 0,6"""
    if ComparePlayerInventoryNumber(ItemType.Goods, goods1, CompareType.GreaterOrEqual, 1, False):
        """State 7,1"""
        if GetEventFlag(flag3):
            """State 2,3"""
            AddTalkListData(z1, action3, -1)
        else:
            """State 4,5"""
            AddTalkListData(z1, action4, -1)
    else:
        """State 8"""
        pass
    """State 9"""
    return 0

def t000001000_x89(flag2=6700):
    """State 0,1"""
    if GetEventFlag(flag2):
        """State 4,3"""
        AddTalkListData(1, 20010075, -1)
    else:
        """State 5,2"""
        AddTalkListData(1, 20010071, -1)
    """State 6"""
    return 0

def t000001000_x90(flag1=_, action1=_, action2=_):
    """State 0,1"""
    if GetEventFlag(flag1):
        """State 2,6"""
        assert t000001000_x4(action6=action1)
    else:
        """State 3,5"""
        SetEventFlag(6700, FlagState.Off)
        SetEventFlag(6701, FlagState.Off)
        SetEventFlag(6702, FlagState.Off)
        SetEventFlag(6703, FlagState.Off)
        """State 4"""
        SetEventFlag(flag1, FlagState.On)
        """State 7"""
        assert t000001000_x4(action6=action2)
    """State 8"""
    return 0

def t000001000_x2032(text1=_, mode1=1):
    """State 0,4"""
    assert t000001000_x2() and CheckSpecificPersonTalkHasEnded(0)
    """State 1"""
    TalkToPlayer(text1, -1, -1, 0)
    assert CheckSpecificPersonTalkHasEnded(0)
    """State 3"""
    if mode1 == 0:
        pass
    else:
        """State 2"""
        ReportConversationEndToHavokBehavior()
    """State 5"""
    return 0

def t000001000_x2222():
    """State 0"""
    if not GetEventFlag(4651):
        """State 1"""
        assert t000001000_x35(z28=20001, val4=1, z29=1, z30=2, z31=60)
    else:
        """State 2"""
        assert t000001000_x29(z32=20010)
    """State 3"""
    return 0

def t000001000_x2223():
    while True:
        """State 0"""
        CloseShopMessage()
        ClearTalkListData()
        AddTalkListDataIf(GetEventFlag(35009359) == 1, 17, 1055421059, -1)
        AddTalkListDataIf(GetEventFlag(35009353) == 1, 16, 1055421058, -1)
        AddTalkListDataIf(GetEventFlag(35009356) == 1, 15, 1055421057, -1)
        AddTalkListDataIf(GetEventFlag(35009351) == 1, 14, 1055421056, -1)
        AddTalkListDataIf(GetEventFlag(11009276) == 1, 13, 1055421055, -1)
        AddTalkListDataIf(GetEventFlag(1043539251) == 1, 12, 1055421054, -1)
        AddTalkListDataIf(GetEventFlag(11009271) == 1, 11, 1055421053, -1)
        call = t000001000_x2228()
        if call.Get() == 1:
            """State 1"""
            AddTalkListDataIf(GetEventFlag(11009251) == 1, 10, 1055421052, -1)
            AddTalkListDataIf(GetEventFlag(11009251) == 0, 9, 1055421051, -1)
        elif call.Done():
            pass
        """State 2"""
        AddTalkListDataIf(GetEventFlag(1038509251) == 1, 8, 1055421050, -1)
        AddTalkListDataIf(GetEventFlag(1043349251) == 1, 7, 1055421049, -1)
        AddTalkListDataIf(GetEventFlag(1046389202) == 1, 6, 1055421048, -1)
        AddTalkListDataIf(GetEventFlag(1054559201) == 1, 5, 1055421047, -1)
        AddTalkListDataIf(GetEventFlag(1043509201) == 1, 4, 1055421046, -1)
        AddTalkListDataIf(GetEventFlag(11009256) == 1, 3, 1055421045, -1)
        AddTalkListDataIf(GetEventFlag(1042379203) == 1, 2, 1055421044, -1)
        AddTalkListDataIf(GetEventFlag(1042379207) == 1, 1, 1055421043, -1)
        # action:15000460:"Cancel"
        AddTalkListData(99, 15000460, -1)
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 3"""
        call = t000001000_x2226(z2=GetTalkListEntryResult())
        if call.Get() == 1:
            """State 4"""
            assert t000001000_x36(flag4=4655)
        elif call.Done():
            """State 5"""
            return 0
    """Unused"""
    """State 6"""
    return 0

def t000001000_x2226(z2=_):
    """State 0"""
    def WhilePaused():
        RequestAnimation(20004, -1)
    """State 1"""
    if z2 == 0:
        """State 2"""
        return 0
    elif z2 == 1:
        """State 3"""
        # talk:10003100:"Me?"
        # talk:10003101:"I'm searching."
        # talk:10003102:"For my purpose, given to me by my mother inside the Erdtree, long ago."
        # talk:10003103:"For the reason that I yet live, burned and bodiless."
        # talk:10003104:"There is something for which I must apologise."
        # talk:10003105:"I've acted the Finger Maiden, yet can offer no guidance."
        # talk:10003106:"I am no maiden. My purpose…was long ago lost."
        assert t000001000_x2032(text1=10003100, mode1=1)
    elif z2 == 12:
        """State 4"""
        # talk:10010100:"In Marika's own words."
        # talk:10010101:"Hear me, Demigods. My children beloved."
        # talk:10010102:"Make of thyselves that which ye desire. Be it a Lord. Be it a God."
        # talk:10010103:"But should ye fail to become aught at all, ye will be forsaken."
        # talk:10010104:"Amounting only to sacrifices..."
        assert t000001000_x2032(text1=10010100, mode1=1)
    elif z2 == 3:
        """State 5"""
        # talk:10010200:"In Marika's own words."
        # talk:10010201:"O Radagon, leal hound of the Golden Order."
        # talk:10010202:"Thou'rt yet to become me. Thou'rt yet to become a god."
        # talk:10010203:"Let us be shattered, both. Mine other self."
        assert t000001000_x2032(text1=10010200, mode1=1)
    elif z2 == 4:
        """State 6"""
        # talk:10010300:"In Marika's own words."
        # talk:10010301:"I declare mine intent, to search the depths of the Golden Order."
        # talk:10010302:"Through understanding of the proper way, our faith, our grace, is increased."
        # talk:10010303:"Those blissful early days of blind belief are long past."
        # talk:10010304:"My comrades; why must ye falter?"
        assert t000001000_x2032(text1=10010300, mode1=1)
    elif z2 == 5:
        """State 7"""
        # talk:10010400:"In Marika's own words."
        # talk:10010401:"Hark, brave warriors. Hark, my lord Godfrey. We commend your deeds."
        # talk:10010402:"Guidance hath delivered ye through each ordeal, to the place ye stand."
        # talk:10010403:"Put the Giants to the sword, and confine the flame atop the mount."
        # talk:10010404:"Let a new epoch begin. An epoch glistening with life."
        # talk:10010405:"Brandish the Elden Ring, for the Age of the Erdtree!"
        assert t000001000_x2032(text1=10010400, mode1=1)
    elif z2 == 6:
        """State 8"""
        # talk:10004100:"Very well. In Marika's own words."
        # talk:10004101:"My Lord, and thy warriors. I divest each of thee of thy grace."
        # talk:10004102:"With thine eyes dimmed, ye will be driven from the Lands Between."
        # talk:10004103:"Ye will wage war in a land afar, where ye will live, and die."
        # talk:10004104:"Well? Perhaps that might serve you in lieu of a maiden's guidance."
        assert t000001000_x2032(text1=10004100, mode1=1)
    elif z2 == 7:
        """State 9"""
        # talk:10004400:"In Marika's own words."
        # talk:10004401:"Then, after thy death, I will give back what I once claimed."
        # talk:10004402:"Return to the Lands Between, wage war, and brandish the Elden Ring."
        # talk:10004403:"Grow strong in the face of death. Warriors of my lord. Lord Godfrey."
        assert t000001000_x2032(text1=10004400, mode1=1)
    elif z2 == 8:
        """State 10"""
        # talk:10004500:"In Marika's own words."
        # talk:10004501:"The Erdtree governs all. The choice is thine."
        # talk:10004502:"Become one with the Order. Or divest thyself of it."
        # talk:10004503:"To wallow at the fringes; a powerless upstart."
        assert t000001000_x2032(text1=10004500, mode1=1)
    elif z2 == 9:
        """State 11"""
        # talk:10012000:"..."
        # talk:10012001:"Is there...another person inside of you?"
        # talk:10012002:"Did you...want that to happen?"
        # talk:10012003:"I sense no malice. Do as you think best."
        # talk:10012004:"Hello, other you."
        # talk:10012005:"I am Melina, and I have an accord with this person."
        # talk:10012006:"We might be together for some time."
        # talk:10012007:"Pleased to meet you."
        assert t000001000_x2032(text1=10012000, mode1=1)
    elif z2 == 10:
        """State 12"""
        # talk:10012100:"..."
        # talk:10012101:"Is there...another person inside of you?"
        # talk:10012102:"Did you...want that to happen?"
        # talk:10012103:"I sense no malice. Do as you think best."
        # talk:10012104:"Hello, other you."
        # talk:10012105:"I am Melina, and I am travelling with this person."
        # talk:10012106:"We might be together for some time."
        # talk:10012107:"Pleased to meet you."
        assert t000001000_x2032(text1=10012100, mode1=1)
    elif z2 == 11:
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
        assert t000001000_x2032(text1=10015000, mode1=1)
    elif z2 == 2:
        """State 14"""
        # talk:10003000:"This tiny golden aura is the grace of the Erdtree."
        # talk:10003001:"This light once shone in the eyes of your Tarnished brethren."
        # talk:10003002:"But now it is all that guides you. Or so I hear."
        # talk:10003003:"You can see them, can't you?"
        # talk:10003004:"The rays of grace, that guide you through your burden."
        assert t000001000_x2032(text1=10003000, mode1=1)
    elif z2 == 13:
        """State 15"""
        # talk:10016000:"There is something I'd like to say."
        # talk:10016001:"My purpose was given to me by my mother."
        # talk:10016002:"But now, I act of my own volition."
        # talk:10016003:"I have set my heart upon the world that I would have."
        # talk:10016004:"Regardless of my mother's designs."
        # talk:10016005:"I won't allow anyone to speak ill of that."
        # talk:10016006:"Not even you."
        assert t000001000_x2032(text1=10016000, mode1=1)
    elif z2 == 14:
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
        assert t000001000_x2032(text1=10018000, mode1=1)
    elif z2 == 15:
        """State 17"""
        # talk:10018100:"I shall see to the kindling."
        # talk:10018101:"It is a purpose which I choose to fulfil."
        # talk:10018102:"So, please... Leave the frenzied flame alone."
        assert t000001000_x2032(text1=10018100, mode1=1)
    elif z2 == 16:
        """State 18"""
        # talk:10018500:"I ask you, one more time."
        # talk:10018501:"Please, seek not the frenzied flame."
        # talk:10018502:"As one who strives to become a Lord,"
        # talk:10018503:"deny not the lives, the new births of this world."
        # talk:10018504:"Those who would are not fit to be called Lord."
        # talk:10018505:"When the land they preside over is lifeless."
        assert t000001000_x2032(text1=10018500, mode1=1)
    elif z2 == 17:
        """State 19"""
        # talk:10018600:"Please, put a stop to this madness."
        # talk:10018601:"The Lord of Frenzied Flame is no lord at all."
        # talk:10018602:"When the land they preside over is lifeless."
        assert t000001000_x2032(text1=10018600, mode1=1)
    else:
        """State 20"""
        return 0
    """State 21"""
    return 1

def t000001000_x2227(z1=_):
    """State 0,1"""
    AwardItemLot(z1)
    assert not IsMenuOpen(MenuType.Bonfire) and GetCurrentStateElapsedFrames() > 1
    """State 2"""
    return 0

def t000001000_x2228():
    """State 0"""
    # goods:207000:Mimic Tear Ashes
    # goods:207001:Mimic Tear Ashes +1
    # goods:207002:Mimic Tear Ashes +2
    # goods:207003:Mimic Tear Ashes +3
    # goods:207004:Mimic Tear Ashes +4
    # goods:207005:Mimic Tear Ashes +5
    # goods:207006:Mimic Tear Ashes +6
    # goods:207007:Mimic Tear Ashes +7
    # goods:207008:Mimic Tear Ashes +8
    # goods:207009:Mimic Tear Ashes +9
    # goods:207010:Mimic Tear Ashes +10
    if (ComparePlayerInventoryNumber(ItemType.Goods, 207000, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods,
        207001, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 207002, CompareType.GreaterOrEqual,
        1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 207003, CompareType.GreaterOrEqual, 1, False)
        or ComparePlayerInventoryNumber(ItemType.Goods, 207004, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods,
        207005, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 207006, CompareType.GreaterOrEqual,
        1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 207007, CompareType.GreaterOrEqual, 1, False)
        or ComparePlayerInventoryNumber(ItemType.Goods, 207008, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods,
        207009, CompareType.GreaterOrEqual, 1, False) or ComparePlayerInventoryNumber(ItemType.Goods, 207010, CompareType.GreaterOrEqual,
        1, False)):
        """State 1"""
        return 1
    else:
        """State 2"""
        return 0

