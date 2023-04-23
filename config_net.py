from netmiko import *
import re


scoreswitch = {
        'device_type': 'cisco_ios',
        'host': '10.0.100.1',
        'username': 'beta-admin',
        'password': 'b3t4b0ts!',
        'secret': 'b3t4b0ts!',
    }
# Call to add network information. Must provide a 4 number string for ip address
def init_net(team1, team2):
    vert = re.findall("..?", team1)
    jaune = re.findall("..?", team2)



    ssh = ConnectHandler(**scoreswitch)
    ssh.enable()
    ssh.config_mode()
    commands = [
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


# Call to remove all network information
def reset_net():
    ssh = ConnectHandler(**scoreswitch)
    ssh.enable()
    ssh.config_mode()
    commands = ["interface vlan 10",
                "no ip address",
                "exit",
                "interface vlan 20",
                "no ip address",
                'no ip dhcp pool vert',
                'no ip dhcp pool jaune'
                ]
    ssh.send_config_set(commands)
    ssh.disconnect()
