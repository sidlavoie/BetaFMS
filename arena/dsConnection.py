import socket

HOST = '10.0.100.5'
PORT = 1750
vert_ip_ds = '0.0.0.0'
jaune_ip_ds = '0.0.0.0'

def test():
    with socket.socket(socket.AF_INET, ) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'Ip découverte: {addr}')
