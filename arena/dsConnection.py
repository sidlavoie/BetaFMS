import socket
import re


def dsDiscover(vert, jaune):
    vert_ds_ip = '0'
    jaune_ds_ip = '0'
    teamIPvert = re.findall("..?", vert)
    teamIPjaune = re.findall("..?", jaune)

    s = socket.socket()

    s.bind(('10.0.100.5', 1750))
    s.listen()

    while True:
        conn, addr = s.accept()
        if vert_ds_ip == '0' or jaune_ds_ip == '0':
            if teamIPvert in addr[0]:
                vert_ds_ip = addr[0]
                print("vert_ds_ip: ", vert_ds_ip)
            elif teamIPjaune in addr[0]:
                jaune_ds_ip = addr[0]
                print("vert_ds_ip: ", jaune_ds_ip)
            else:
                print("No DS yet!")

        else:
            print("vert_ds_ip: ", vert_ds_ip, " jaune_ds_ip: ", jaune_ds_ip)
            break
