import sys
from netaddr import EUI
import netaddr
import os
import subprocess
import re
import requests
from filecmp import cmp
from ntc_templates.parse import parse_output
import napalm

class Device:
    def __init__(self):
        pass
    def listToString(self, list):
        # initialize an empty string
        self.list = []
        str1 = ""
        for element in list:
            str1 += str(element)
        return str1

class Router:
    pass

class Switch:
    pass

class Access_list:
    running_conf_file = "acl_current.txt"
    running_conf_file = "acl_current.txt"
    pass

    

if __name__ == '__main__':
    D = Device()
    print(D.listToString(list=[1,2]))
