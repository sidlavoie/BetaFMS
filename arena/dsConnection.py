import socket
from time import sleep


vert_ip_ds = '0.0.0.0'
jaune_ip_ds = '0.0.0.0'


def test():
    HOST = '10.0.100.5'
    PORT = 1750
    with socket.socket(socket.AF_INET, ) as s:
        vert_ip = 0
        jaune_ip = 0

        while True:
            if vert_ip == 0 or jaune_ip == 0:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    if '12.34' in addr and vert_ip == 0:
                        vert_ip = addr
                        print ("vert: %s", vert_ip)
                    elif '46.78' in addr and jaune_ip == 0:
                        jaune_ip = addr
                        print ("jaune: %s", jaune_ip)
                    else:
                        print('waiting for address')
                        sleep(1)
            else:
                break

