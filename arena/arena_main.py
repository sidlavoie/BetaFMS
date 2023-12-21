from db_main import *
from config_net import init_net
from arena.driverStation import DriverStation
from arena.dsConnection import discoverDS
import threading

CURRENT_MATCH = 0


def loadNextMatch():
    global CURRENT_MATCH
    CURRENT_MATCH += 1
    match = getMatchInfo(CURRENT_MATCH)
    print(match)
    if "Dîner" in match or "Pause" in match:
        CURRENT_MATCH += 1
        match = getMatchInfo(CURRENT_MATCH)

    # Initialize Network
    init_net(match[0], match[1])
    # Create DriverStation objects
    vert = DriverStation(match[0], CURRENT_MATCH)
    jaune = DriverStation(match[1], CURRENT_MATCH)
    # Find IP of the DS and write it to the object
    vert.dsIP, jaune.dsIP = discoverDS(vert.team_id, jaune.team_id)

    # Starts communication with the DS
    vert.udpThread = threading.Thread(target=vert.send_udp_fms_packet)
    vert.running_flag.set()
    vert.udpThread.start()
    jaune.udpThread = threading.Thread(target=jaune.send_udp_fms_packet)
    jaune.running_flag.set()
    jaune.udpThread.start()
    return vert, jaune


def end_match(vert, jaune):
    # This stops the threads. DO NOT REMOVE!!!
    vert.running_flag.clear()
    vert.udpThread.join()
    jaune.running_flag.clear()
    jaune.udpThread.join()
    # Deallocate the objects
    vert = None
    jaune = None



