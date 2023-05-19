import socket
import struct
import sys


# Run to discover the ip addresses to use
def discoverDS(vert, jaune):
    fms_ip = '10.0.100.5'
    fms_port = 1750
    addr_vert = '0'
    addr_jaune = '0'

    # create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((fms_ip, fms_port))
    except OSError:
        print('Ip address not found! Set one IP interface to 10.0.100.5 and restart BetaFMS')
        sys.exit()
    sock.setblocking(False)
    sock.listen()

    print(f'Listening for driver station packets on {fms_ip}:{fms_port}...')
    while True:
        try:
            # wait for a connection from the driver station
            conn, addr = sock.accept()
        except socket.timeout:
            continue
        except BlockingIOError:
            continue

        print(f'Received connection from {addr[0]}')
        packet = conn.recv(1024)

        # This unpacks the 4th and 5th bytes to discover the team number
        received_team = str((int(packet[3]) << 8) + int(packet[4]))
        # determine which team the driver station is for
        if received_team == vert:
            addr_vert = addr[0]
            print(f'This is the driver station for team {vert}')
        elif received_team == jaune:
            addr_jaune = addr[0]
            print(f'This is the driver station for team {jaune}')

        if addr_vert != '0' and addr_jaune != '0':
            break

    return [addr_vert, addr_jaune]

