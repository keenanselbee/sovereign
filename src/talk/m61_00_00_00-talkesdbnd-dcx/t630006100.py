# -*- coding: utf-8 -*-
def t630006100_1():
    """State 0,1"""
    t630006100_x0(shop1=102350, shop2=102351)
    Quit()

def t630006100_x0(shop1=102350, shop2=102351):
    """State 0"""
    if not IsClientPlayer():
        """State 1"""
        Label('L0')
        call = t630006100_x1(shop1=shop1, shop2=shop2)
        if IsClientPlayer():
            """State 2"""
            Label('L1')
            call = t630006100_x2()
            if not IsClientPlayer():
                Goto('L0')
            elif IsPlayerDead():
                pass
        elif IsPlayerDead():
            pass
    else:
        Goto('L1')
    """State 3"""
    call = t630006100_x4()
    assert not IsPlayerDead()
    Goto('L0')
    """Unused"""
    """State 4"""
    return 0

def t630006100_x1(shop1=102350, shop2=102351):
    """State 0"""
    while True:
        """State 2"""
        # actionbutton:206060:"Examine altar"
        assert (t630006100_x5(actionbutton1=206060, flag1=6001, flag2=6000, flag3=6000, flag4=6000, flag5=6000,
                flag6=2049392720))
        """State 1"""
        TurnCharacterToFaceEntity(-1, 10000, -1, -1)
        ClearPlayerDamageInfo()
        assert GetCurrentStateElapsedFrames() > 1 and GetWhetherChrEventAnimHasEnded(10000)
        """State 3"""
        ClearTalkActionState()
        def WhilePaused():
            GiveSpEffectToPlayerIf(DidYouDoSomethingInTheMenu(0) == 0, 9611)
            GiveSpEffectToPlayerIf((DoesPlayerHaveSpEffect(9611) == 1 or DoesPlayerHaveSpEffect(9612) == 1) and DidYouDoSomethingInTheMenu(0) == 1,
                                   9613)
        assert t630006100_x3(shop1=shop1, shop2=shop2) or (GetDistanceToPlayer() > 7 or HasPlayerBeenAttacked())
        """State 4"""
        assert t630006100_x6()
    """Unused"""
    """State 5"""
    return 0

def t630006100_x2():
    """State 0"""
    Quit()
    """Unused"""
    """State 1"""
    return 0

def t630006100_x3(shop1=102350, shop2=102351):
    """State 0,10"""
    ClearPreviousMenuSelection()
    while True:
        """State 1"""
        ClearTalkListData()
        """State 2"""
        # action:26010000:"Ritual of Dragon Communion"
        AddTalkListData(1, 26010000, -1)
        if GetEventFlag(1055420240) and GetEventFlag(2054390800):
            # action:26302010:"Ritual of Dragon Communion"
            AddTalkListData(2, 26302010, -1)
             # action:26302000:"Communion with Bayle"
            AddTalkListData(3, 26302000, -1)
        elif GetEventFlag(1055420240):
            # action:26302010:"Ritual of Dragon Communion"
            AddTalkListData(2, 26302010, -1)
        elif GetEventFlag(2054390800):
            # action:26302000:"Communion with Bayle"
            AddTalkListData(3, 26302000, -1)
        # action:20000009:"Leave"
        AddTalkListData(9, 20000009, -1)
        """State 3"""
        ShowShopMessage(TalkOptionsType.Regular)
        assert not (CheckSpecificPersonMenuIsOpen(1, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        """State 4"""
        if GetTalkListEntryResult() == 1:
            """State 5,7"""
            OpenDragonCommunionShop(101950, 101974)
            assert not (CheckSpecificPersonMenuIsOpen(22, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 2:
            """State 12"""
            OpenDragonCommunionShop(102355, 102455)
            assert not (CheckSpecificPersonMenuIsOpen(22, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        elif GetTalkListEntryResult() == 3:
            """State 8,9"""
            OpenDragonCommunionShop(shop1, shop2)
            assert not (CheckSpecificPersonMenuIsOpen(22, 0) and not CheckSpecificPersonGenericDialogIsOpen(0))
        else:
            """State 6,11"""
            return 0

def t630006100_x4():
    """State 0,2"""
    assert t630006100_x6()
    """State 1"""
    Quit()
    """Unused"""
    """State 3"""
    return 0

def t630006100_x5(actionbutton1=206060, flag1=6001, flag2=6000, flag3=6000, flag4=6000, flag5=6000, flag6=2049392720):
    """State 0"""
    while True:
        """State 1"""
        assert not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead() and not IsCharacterDisabled()
        """State 3"""
        assert GetEventFlag(flag1) or GetEventFlag(flag2) or GetEventFlag(flag3) or GetEventFlag(flag4) or GetEventFlag(flag5)
        """State 4"""
        assert not GetEventFlag(flag6)
        """State 2"""
        if (GetEventFlag(flag6) or not (not GetOneLineHelpStatus() and not IsClientPlayer() and not IsPlayerDead()
            and not IsCharacterDisabled()) or (not GetEventFlag(flag1) and not GetEventFlag(flag2) and not GetEventFlag(flag3)
            and not GetEventFlag(flag4) and not GetEventFlag(flag5))):
            pass
        # actionbutton:206060:"Examine altar"
        elif CheckActionButtonArea(actionbutton1):
            break
    """State 5"""
    return 0

def t630006100_x6():
    """State 0,1"""
    ClearTalkProgressData()
    StopEventAnimWithoutForcingConversationEnd(0)
    ForceCloseGenericDialog()
    ForceCloseMenu()
    ReportConversationEndToHavokBehavior()
    """State 2"""
    return 0

