from db_main import *
from config_net import init_net

CURRENT_MATCH = 0


def loadNextMatch():
    global CURRENT_MATCH
    CURRENT_MATCH += 1
    match = getMatchInfo(CURRENT_MATCH)
    init_net(match[0], match[1])

