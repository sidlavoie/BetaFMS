# This file represents the class for a Driver station

class DriverStation:
    def __init__(self, team_id):
        self.team_id = team_id
        self.dsIP = None
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
        self.packet_count = None
        self.missed_packet_offset = None
        self.tcp_conn = None
        self.udp_conn = None
