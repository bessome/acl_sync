#!/root/tools/mac_address/venv/bin/python
from pprint import pprint
import sys
from netaddr import EUI
import netaddr
import os
import subprocess
import re
import requests
from filecmp import cmp
from nornir import InitNornir
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.inventory import ConnectionOptions
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_commands
from nornir_scrapli.tasks import send_configs_from_file
from ntc_templates.parse import parse_output
import pynetbox

nb = pynetbox.api(
    'http://10.250.0.105:8000',
    token='f25ecda0b3c6496c80bc07455c8d194075bc1086'
)

def telegram_send_message(bot_message):

    bot_token = 'bot1280830109:AAHrVZcopCAGs5EaRHGM7q7NaKnzi-OSmRo'
    bot_chatID = '502743941'
    send_text = 'https://api.telegram.org/' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def telegram_send_message_1007(bot_message):

    bot_token = 'bot1280830109:AAHrVZcopCAGs5EaRHGM7q7NaKnzi-OSmRo'
    bot_chatID = '424910303'
    send_text = 'https://api.telegram.org/' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

nr = InitNornir(
    config_file="/root/tools/cisco_acl/config.yaml"
)
#Coonect to NETBOX
nr.inventory.defaults.connection_options['scrapli'] = ConnectionOptions(extras={"transport":"ssh2", "auth_strict_key": False, "auth_secondary": "neh,byf9", "auth_username": "6696", "auth_password": "vjrhfz*rehbwf"})
devices = nr.filter(F(name__contains=sys.argv[1]))
for key in devices.inventory.hosts:
    devices.inventory.hosts[key].platform = "eos"

command_int = "int " + sys.argv[2]
#if not sys.argv[3]:
#    descr = "descr did-" + sys.argv[19] + ".cid-" + sys.argv[20]
#else:
#    descr = "descr " + sys.argv[3]
#print(descr)
print(command_int)
no_native = "no switchport trunk native vlan"
no_allowed = "no switchport trunk allowed vlan"
no_accesss = "no switchport access vlan"

interface_info = nb.dcim.interfaces.get(sys.argv[19])
device_id = interface_info.link_peers[0].device.id
cable_id = interface_info.link_peers[0].cable.id
if not sys.argv[3]:
    descr = "did_" + interface_info.link_peers[0].device.id + ".cid_" + (interface_info.link_peers[0].cable.id
else:
    descr = "descr " + sys.argv[3]

#cable_info = nb.dcim.cables.get(sys.argv[20])
#print(dict(interface_info))
#rint(interface_info.link_peers[0].device.id)
#print(cable_info.a_terminations[0].object.device.name)
print(descr)
if sys.argv[4] == "access":
    mode = sys.argv[4]
    access_vlan = "switchport access vlan " + sys.argv[5]
    results = devices.run(task=send_commands, commands=["conf t", command_int, no_native, no_allowed, descr, "switchport mode access", access_vlan, "write"])
    #rint_result(results)
elif sys.argv[4] == "tagged-all":
    mode = "trunk"
    if sys.argv[5]:
        native = "switchport trunk native vlan " + sys.argv[5]
        results = devices.run(task=send_commands, commands=["conf t", command_int, no_accesss, no_native, no_allowed, descr, "switchport mode trunk", native, "write"])
    else:
        results = devices.run(task=send_commands, commands=["conf t", command_int, no_accesss, no_native, no_allowed, descr, "switchport mode trunk", "write"])
    print_result(results)
elif sys.argv[4] == "tagged":
    count = 0
    mode = "trunk"
    native = "switchport trunk native vlan " + sys.argv[5]
    if sys.argv[5]:
        allowed = "switchport trunk allowed vlan " + sys.argv[5]
    else:
         allowed = "switchport trunk allowed vlan " + sys.argv[6]
    for i in (sys.argv):
       count +=1
       if count > 6:
           #print(i)
           if i:
               allowed = allowed + "," + i
               #allowed = allowed + sys.argv[5] + "," + sys.argv[6] + "," + sys.argv[7] + "," + sys.argv[8] + "," + sys.argv[9]
    results = devices.run(task=send_commands, commands=["conf t", command_int, no_accesss, no_native, no_allowed, descr, "switchport mode trunk", native, allowed, "write"])
    #rint_result(results)
else:
    results = devices.run(task=send_commands, commands=["conf t", command_int, descr, "write"])
    print(sys.argv[4] +  ' UNKNOWN')
    print_result(results)
#results = devices.run(task=send_commands, commands=["conf t", command_int, descr])
#print_result(results)
