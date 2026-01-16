from netmiko import ConnectHandler
from db_main import *
from misc import *
import re

last_vert = '0000'
last_jaune = '0000'


def set_last(vert, jaune):
    global last_vert
    global last_jaune
    last_vert = vert
    last_jaune = jaune


scoreswitch = {
        'device_type': 'cisco_ios',
        'host': '10.0.100.1',
        'username': 'beta-admin',
        'password': 'b3t4b0ts!',
        'secret': 'b3t4b0ts!',
    }

beta_ap = {
    'device_type': 'cisco_ios',
    'host': '10.0.100.2',
    'username': 'beta-admin',
    'password': 'b3t4b0ts!',
    'secret': 'b3t4b0ts!',
}


# Call to add network information. Must provide a 4 number string for ip address
def init_net(teamvert, teamjaune):
    set_last(teamvert, teamjaune)
    vert = re.findall("..?", teamvert)
    jaune = re.findall("..?", teamjaune)

    # scoreswitch config
    print("Configuring scoreswitch for team %s and %s..." % (teamvert, teamjaune))
    with Spinner():
        ssh = ConnectHandler(**scoreswitch)
        ssh.enable()
        ssh.config_mode()
        commands = [
                    'access-list 110 permit ip 10.%s.%s.0 0.0.0.255 host 10.0.100.5' % (vert[0], vert[1]),
                    'access-list 110 permit udp any eq bootpc any eq bootps',
                    'access-list 120 permit ip 10.%s.%s.0 0.0.0.255 host 10.0.100.5' % (jaune[0], jaune[1]),
                    'access-list 120 permit udp any eq bootpc any eq bootps',
                    'interface vlan 10',
                    'ip address 10.%s.%s.4 255.255.255.0' % (vert[0], vert[1]),
                    'interface vlan 20',
                    'ip address 10.%s.%s.4 255.255.255.0' % (jaune[0], jaune[1]),
                    'exit',
                    'ip dhcp excluded-address 10.%s.%s.1 10.%s.%s.10' % (vert[0], vert[1], vert[0], vert[1]),
                    'ip dhcp excluded-address 10.%s.%s.1 10.%s.%s.10' % (jaune[0], jaune[1], jaune[0], jaune[1]),
                    'ip dhcp pool vert',
                    'lease 3',
                    'network 10.%s.%s.0 255.255.255.0' % (vert[0], vert[1]),
                    'default-router 10.%s.%s.4' % (vert[0], vert[1]),
                    'domain-name beta.local',
                    'exit',
                    'ip dhcp pool jaune',
                    'lease 3',
                    'network 10.%s.%s.0 255.255.255.0' % (jaune[0], jaune[1]),
                    'default-router 10.%s.%s.4' % (jaune[0], jaune[1]),
                    'domain-name beta.local'
                    ]
        ssh.send_config_set(commands)
        ssh.disconnect()

        # get SSID and WPA key from the database
        wifiVert = get_teamWifi(teamvert)
        wifiJaune = get_teamWifi(teamjaune)

        # ap config
    print("Configuring beta-ap with ssid %s and ssid %s..." % (wifiVert[0], wifiJaune[0]))
    with Spinner():
        ssh = ConnectHandler(**beta_ap)
        ssh.enable()
        ssh.config_mode()
        commands = [
            ''
            'dot11 ssid %s' % wifiVert[0],
            'vlan 10',
            'authentication open',
            'authentication key-management wpa version 2',
            'wpa-psk ascii %s' % wifiVert[1],
            'dot11 ssid %s' % wifiJaune[0],
            'vlan 20',
            'authentication open',
            'authentication key-management wpa version 2',
            'wpa-psk ascii %s' % wifiJaune[1],
            'interface dot11Radio 1',
            'ssid %s' % wifiVert[0],
            'ssid %s' % wifiJaune[0]
        ]
        ssh.send_config_set(commands)
        ssh.disconnect()
    print("Network init complete!")


# Call to remove all network information
def reset_net():
    # Reset AP
    print("Network reset requested...")
    with Spinner():
        ssh = ConnectHandler(**beta_ap)
        ssh.enable()
        output = ssh.send_command_timing("configure replace nvram:startup-config")
        if 'This' in output:
            output += ssh.send_command_timing("y")
        ssh.disconnect()

    print("AP reset complete!")
    with Spinner():
        # Reset scoreswitch
        ssh = ConnectHandler(**scoreswitch)
        ssh.enable()
        output = ssh.send_command_timing("configure replace nvram:startup-config")
        if 'This' in output:
            output += ssh.send_command_timing("y")
        ssh.disconnect()
    print("Scoreswitch reset complete!")

