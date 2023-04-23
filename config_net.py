from netmiko import *
import re


def init_net(team1, team2):
    vert = re.findall("..?", team1)
    jaune = re.findall("..?", team2)

    scoreswitch = {
        'device_type': 'cisco_ios',
        'host': '10.0.100.1',
        'username': 'beta-admin',
        'password': 'b3t4b0ts!',
        'secret': 'b3t4b0ts!',
    }

    ssh = ConnectHandler(**scoreswitch)
    ssh.enable()
    ssh.config_mode()
    commands = [
                'no ip dhcp pool vert',
                'no ip dhcp pool jaune',
                'interface vlan 10',
                'ip address 10.%s.%s.4 255.255.255.0' % (vert[0], vert[1]),
                'interface vlan 20',
                'ip address 10.%s.%s.4 255.255.255.0' % (jaune[0], jaune[1]),
                'exit',
                'ip dhcp excluded-address 10.%s.%s.1 10.%s.%s.10' % (vert[0], vert[1], vert[0], vert[1]),
                'ip dhcp excluded-address 10.%s.%s.1 10.%s.%s.10' % (jaune[0], jaune[1], jaune[0], jaune[1]),
                'no ip dhcp pool vert',
                'ip dhcp pool vert',
                'lease 3',
                'network 10.%s.%s.0 255.255.255.0' % (vert[0], vert[1]),
                'default-router 10.%s.%s.4' % (vert[0], vert[1]),
                'domain-name beta.local'
                'exit',
                'ip dhcp pool jaune',
                'lease 3',
                'network 10.%s.%s.0 255.255.255.0' % (jaune[0], jaune[1]),
                'default-router 10.%s.%s.4' % (jaune[0], jaune[1]),
                'domain-name beta.local'
                ]
    ssh.send_config_set(commands)
    ssh.disconnect()
