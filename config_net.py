from netmiko import *
from db_main import *
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
    print("last_jaune: ", last_jaune)
    print("last_vert: ", last_vert)
    vert = re.findall("..?", teamvert)
    jaune = re.findall("..?", teamjaune)

    # scoreswitch config
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

    # get SSID and WPA key
    wifiVert = get_teamWifi(teamvert)
    wifiJaune = get_teamWifi(teamjaune)

    # ap config
    ssh = ConnectHandler(**beta_ap)
    ssh.enable()
    ssh.config_mode()
    commands = [
        'dot11 ssid %s' % wifiVert[0],
        'vlan 10',
        'authentication open',
        'authentication key-management wpa version 2',
        'mbssid guest-mode',
        'wpa-psk ascii %s' % wifiVert[1],
        'dot11 ssid %s' % wifiJaune[0],
        'vlan 20',
        'authentication open',
        'authentication key-management wpa version 2',
        'mbssid guest-mode',
        'wpa-psk ascii %s' % wifiJaune[1],
        'interface dot11Radio 1',
        'ssid %s' % wifiVert[0],
        'ssid %s' % wifiJaune[0]
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
                "no ip dhcp pool vert",
                "no ip dhcp pool jaune"
                ]
    ssh.send_config_set(commands)
    ssh.disconnect()


def reset_ap():
    ssh = ConnectHandler(**beta_ap)
    ssh.enable()
    ssh.config_mode()
    del_vert = get_teamWifi(last_vert)[0]
    del_jaune = get_teamWifi(last_jaune)[0]
    commands = ["interface dot11Radio 1",
                "no ssid %s" % del_vert,
                "no ssid %s" % del_jaune,
                "exit"
                "no dot11 ssid %s" % del_vert,
                "no dot11 ssid %s" % del_jaune
                ]
    ssh.send_config_set(commands)
    ssh.disconnect()
