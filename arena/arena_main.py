from db_main import *
from config_net import init_net
from arena.driverStation import DriverStation
from arena.dsConnection import discoverDS
from time import sleep

CURRENT_MATCH = 0


def loadNextMatch():
    global CURRENT_MATCH
    CURRENT_MATCH += 1
    match = getMatchInfo(CURRENT_MATCH)
    print(match)
    init_net(match[0], match[1])
    vert = DriverStation(match[0], CURRENT_MATCH)
    jaune = DriverStation(match[1], CURRENT_MATCH)
    vert.dsIP, jaune.dsIP = discoverDS(vert.team_id, jaune.team_id)
    vert.auto = True
    jaune.auto = True
    vert.enabled = True
    print("DS decouvert. Envoi de packets")
    while True:
        jaune.send_udp_fms_packet()
        vert.send_udp_fms_packet()
        sleep(0.25)
