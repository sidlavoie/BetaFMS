import socket


def dsDiscover():
    host = '10.0.100.5'
    port = 1750

    s = socket.socket()

    s.bind((host, port))
    s.listen()

    print("Server started! Waiting...")

    while True:
        conn, addr = s.accept()
        print("ip: ", addr)
        conn.close()