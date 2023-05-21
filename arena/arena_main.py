from db_main import *
from config_net import init_net
from arena.driverStation import DriverStation
from arena.dsConnection import discoverDS
from time import sleep
import threading

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

    print("DS decouvert. Envoi de packets")

    # Starts communication with the DS
    thread_vert = threading.Thread(target=vert.send_udp_fms_packet())
    vert.running_flag.set()
    thread_vert.start()
    thread_jaune = threading.Thread(target=jaune.send_udp_fms_packet())
    jaune.running_flag.set()
    thread_jaune.start()

    sleep(10)
    print('Fin de match')
    vert.running_flag.clear()
    thread_vert.join()
    jaune.running_flag.clear()
    thread_jaune.join()
    print("Fin du programme")


