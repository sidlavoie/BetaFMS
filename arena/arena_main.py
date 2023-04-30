from db_main import *
from config_net import init_net
from arena.driverStation import DriverStation
from arena.dsConnection import discoverDS

CURRENT_MATCH = 0


def loadNextMatch():
    global CURRENT_MATCH
    CURRENT_MATCH += 1
    match = getMatchInfo(CURRENT_MATCH)
    print(match)
    init_net(match[0], match[1])
    vert = DriverStation(match[0])
    jaune = DriverStation(match[1])
    vert.dsIP, jaune.dsIP = discoverDS(vert.team_id, jaune.team_id)
    print(vert.team_id, vert.dsIP)
    print(jaune.team_id, jaune.dsIP)

