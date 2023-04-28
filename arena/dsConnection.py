from threading import *
import socket
import sys


def clientthread(conn):
    buffer = ""
    while True:
        data = conn.recv(8192)
        buffer += data
        print(buffer)
    conn.close()


def dsDiscover():
    try:
        host = '10.0.100.5'
        port = 1750
        tot_socket = 2
        list_sock = []
        for i in range (tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(10)
            list_sock.append(s)

        while 1:
            for j in range(len(list_sock)):
                conn, addr = list_sock[j].accept()
                print("Connected with ", addr[0], ":", str(addr[1]))
                x = Thread(target=clientthread(conn))
        s.close()

    except KeyboardInterrupt as msg:
        sys.exit(0)
