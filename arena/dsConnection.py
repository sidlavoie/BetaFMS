import socket
import struct


# Run to discover the ip addresses to use
def discoverDS(vert, jaune):
    fms_ip = '10.0.100.5'
    fms_port = 1750
    addr_vert = '0'
    addr_jaune = '0'

    # create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((fms_ip, fms_port))
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
        packet, addr = sock.recvfrom(1024)

        received_team = str((int(packet[4]) << 8) + int(packet[5]))
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


def send_fms_packet(ip_address, fms_packet):
    """Send an FMS packet to the specified IP address."""
    FMS_PORT = 1150

    # Create a UDP socket and send the packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(fms_packet, (ip_address, FMS_PORT))
    sock.close()


def handle_ds_packet(packet, vert, jaune):
    """Handle an incoming driver station packet."""
    # Parse the packet to extract the team number and joystick data
    team_number, joystick_data = struct.unpack('!B6s', packet)

    # Convert the joystick data to a tuple of six 8-bit values
    joystick_values = tuple(joystick_data[i] for i in range(6))

    # Determine which side of the field the team is on
    if team_number == vert:
        side = "green"
    elif team_number == jaune:
        side = "yellow"
    else:
        return

