import socket


def createSccSockets(fms_port):
    fms_ip = '10.0.100.5'
    sockscc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockscc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sockscc.bind((fms_ip, fms_port))


    return sockscc


class SCC:
    def __init__(self, port):
        self.port = port
        self.sock = createSccSockets(self.port)
        self.estopEnabled = True

    def receiveStatus(self):
        self.sock.setblocking(False)
        self.sock.listen()

        print(f'Listening for SCC packets on port {self.port}...')
        print(self.sock.getsockname())
        while True:
            try:
                # wait for a connection from the scc
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue
            except BlockingIOError:
                continue

            print(f'Received connection from {addr[0]}')
            packet = conn.recv(24)
            print(packet)
