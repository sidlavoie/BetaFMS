import socket


def createSccSockets(fms_port):
    fms_ip = '10.0.100.5'
    sockscc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockscc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sockscc.bind((fms_ip, fms_port))


    return sockscc


class SCC:
    def __init__(self, port):
        self.port = port
        self.sock = createSccSockets(self.port)
        self.estopEnabled = True  # Enabled by default

    def receiveStatus(self):
        data, addr = self.sock.recvfrom(1024)
        print("received message: %s" % data)
        if data == "b'0'":
            self.estopEnabled = False

