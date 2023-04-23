from netmiko import *
import re


def init_net(team1, team2):
    side1 = re.findall("..?", team1)
    side2 = re.findall("..?", team2)
    print("side1: ", side1)

    scoreswitch = {
        'device_type': 'cisco_ios',
        'host': '172.16.0.1',
        'username': 'beta-admin',
        'password': 'b3t4b0ts!',
        'secret': 'b3t4b0ts!',
    }

    ssh = ConnectHandler(**scoreswitch)
    ssh.send_command('configure terminal'
                     'interface vlan 10'
                     'ip address 10.%s.%s.4 255.255.255.0' %(side1[0],side1[1]))
    ssh.disconnect()