# This file represents the class for a Driver station
from datetime import datetime
import socket
import threading
from time import sleep

class DriverStation:
    def __init__(self, team_id, match_number):
        self.team_id = team_id
        self.match_number = match_number
        self._dsIP = None
        self.auto = None
        self.enabled = None
        self.estop = None
        self.ds_linked = None
        self.radio_linked = None
        self.robot_linked = None
        self.battery_voltage = None
        self.ds_robot_trip_time_ms = None
        self.missed_packet_count = None
        self.seconds_since_last_robot_link = None
        self.last_packet_time = None
        self.last_robot_linked_time = None
        self.packet_count = 0
        self.missed_packet_offset = None
        self.tcp_conn = None
        self.udp_conn = None
        self.running_flag = threading.Event()  # Clear to stop sending udp packets

    @property
    def dsIP(self):
        return self._dsIP

    # Create the socket upon discovering the IP Address
    @dsIP.setter
    def dsIP(self, value):
        self._dsIP = value
        self.create_socket()

    def encodeControlPacket(self):
        packet = [0] * 22

        packet[0] = (self.packet_count >> 8) & 0xFF
        packet[1] = self.packet_count & 0xFF

        packet[2] = 0  # version
        
        # op mode
        if self.auto is not None:
            packet[3] = 2
        elif self.enabled is not None:
            packet[3] = 4
        elif self.estop is not None:
            packet[3] = 8
        else:
            packet[3] = 0

        packet[4] = 0  # not used
        packet[5] = 0  # driver station ID (see what 0 does)

        # match type (set to qualification)
        packet[6] = 2

        packet[7] = (self.match_number >> 8) & 0xFF # match number
        packet[8] = self.match_number & 0xFF

        packet[9] = 1  # match repeat

        # encode current time
        currentTime = datetime.now()

        packet[10] = (currentTime.microsecond // 1000 >> 24) & 0xFF
        packet[11] = (currentTime.microsecond // 1000 >> 16) & 0xFF
        packet[12] = (currentTime.microsecond // 1000 >> 8) & 0xFF
        packet[13] = (currentTime.microsecond // 1000) & 0xFF
        packet[14] = currentTime.second
        packet[15] = currentTime.minute
        packet[16] = currentTime.hour
        packet[17] = currentTime.day
        packet[18] = currentTime.month
        packet[19] = (currentTime.year - 1900) & 0xFF

        # il reste les secondes à mettre
        packet[20] = 0
        packet[21] = 0

        ba = bytearray(packet)

        self.packet_count += 1
        return ba

    def create_socket(self):
        fms_ip = "10.0.100.5"
        self.udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_conn.bind((fms_ip, 0))

    def send_udp_fms_packet(self):
        """Encode and send an FMS packet to the specified IP address."""
        while self.running_flag.is_set():
            fms_port = 1121
            self.udp_conn.sendto(self.encodeControlPacket(), (self._dsIP, fms_port))
            sleep(0.25)
            print(self.team_id)  # TEST
