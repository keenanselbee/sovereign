# -*- coding: utf-8 -*-
def t999801800_1():
    """State 0"""
    # Keep subtitle updates active across the arena's expanded native talk range.
    SetUpdateDistance(100)
    while True:
        """State 1"""
        assert GetEventFlag(1055422946)
        """State 2"""
        ClearTalkProgressData()
        StopEventAnimWithoutForcingConversationEnd(0)
        ReportConversationEndToHavokBehavior()
        assert CheckSpecificPersonTalkHasEnded(0) or not GetEventFlag(1055422946)
        if not GetEventFlag(1055422946):
            continue
        else:
            pass
        # The map event sets exactly one selector before raising the active flag.
        # Each contiguous TalkParam block is one native subtitle conversation.
        """State 3"""
        if GetEventFlag(1055425200):
            TalkToPlayer(99980000, -1, -1, 1)
        elif GetEventFlag(1055425201):
            TalkToPlayer(99980110, -1, -1, 1)
        elif GetEventFlag(1055425202):
            TalkToPlayer(99980120, -1, -1, 1)
        elif GetEventFlag(1055425203):
            TalkToPlayer(99980130, -1, -1, 1)
        elif GetEventFlag(1055425204):
            TalkToPlayer(99980140, -1, -1, 1)
        elif GetEventFlag(1055425205):
            TalkToPlayer(99980150, -1, -1, 1)
        elif GetEventFlag(1055425206):
            TalkToPlayer(99980160, -1, -1, 1)
        elif GetEventFlag(1055425207):
            TalkToPlayer(99980170, -1, -1, 1)
        elif GetEventFlag(1055425208):
            TalkToPlayer(99980180, -1, -1, 1)
        elif GetEventFlag(1055425209):
            TalkToPlayer(99980190, -1, -1, 1)
        elif GetEventFlag(1055425210):
            TalkToPlayer(99980200, -1, -1, 1)
        elif GetEventFlag(1055425211):
            TalkToPlayer(99980210, -1, -1, 1)
        elif GetEventFlag(1055425212):
            TalkToPlayer(99980220, -1, -1, 1)
        elif GetEventFlag(1055425213):
            TalkToPlayer(99980230, -1, -1, 1)
        elif GetEventFlag(1055425214):
            TalkToPlayer(99980240, -1, -1, 1)
        elif GetEventFlag(1055425215):
            TalkToPlayer(99980250, -1, -1, 1)
        else:
            # A missing selector is an aborted request, never a fallback line.
            assert not GetEventFlag(1055422946)
            continue
        """State 4"""
        ReportConversationEndToHavokBehavior()
        assert (CheckSpecificPersonTalkHasEnded(0) or not GetEventFlag(1055422947)
                or not GetEventFlag(1055422946))
        if GetEventFlag(1055422946) and not CheckSpecificPersonTalkHasEnded(0):
            # Opening speech may release combat before its subtitles finish.
            """State 5"""
            ReportConversationEndToHavokBehavior()
            assert CheckSpecificPersonTalkHasEnded(0) or not GetEventFlag(1055422946)
        else:
            pass
        """State 6"""
        if not CheckSpecificPersonTalkHasEnded(0):
            ForceEndTalk(0)
        else:
            pass
        """State 7"""
        ClearTalkProgressData()
        ReportConversationEndToHavokBehavior()
        assert not GetEventFlag(1055422946)
