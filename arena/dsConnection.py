import socket
import struct


# NE FONCTIONNE PAS ENCORE!
def discoverDS(vert, jaune):
    fms_ip = '10.0.100.5'
    fms_port = 1750
    addr_vert = '0'
    addr_jaune = '0'

    # create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((fms_ip, fms_port))
    sock.listen(1)

    print(f'Listening for driver station packets on {fms_ip}:{fms_port}...')
    while True:
    # wait for a connection from the driver station
        conn, addr = sock.accept()
        print(f'Received connection from {addr[0]}')

    # determine which team the driver station is for
        if addr[0].startswith(f'10.{vert[:2]}.{vert[2:4]}'):
            addr_vert = addr[0]
            print(f'This is the driver station for team {vert}')
        elif addr[0].startswith(f'10.{jaune[:2]}.{jaune[2:4]}'):
            addr_jaune = addr[0]
            print(f'This is the driver station for team {jaune}')
        elif addr_vert != '0' and addr_jaune != '0':
            break
        else:
            print('')

    # receive data from the driver station
    #while True:
       # data = conn.recv(1024)
       # if not data:
          #  break

        # decode the data
        #decoded_data = data.decode()

        # do something with the data (e.g. respond with FMS packets)
        # ...
    conn.close()
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

