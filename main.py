import sys
from netaddr import EUI
import netaddr
import os
import subprocess
import re
import requests
from filecmp import cmp
from ntc_templates.parse import parse_output

acl_current="acl_current.txt"
acl_new="acl_new.txt"

f_acl_new = open(acl_new, 'r')
f_acl_current = open(acl_current, 'r')

def acl_file_to_dict(file):
    acl_number = 0
    acl_list = []
    acl_dict = {}
    f_acl = open(file, 'r')
    for line in f_acl:
        if "no access-list" in line:
            acl_dict[acl_number]= acl_list
            acl_number = line.split()[2]
            #print(acl_list)
            acl_list = []
        else:
            acl_list.append(line)
            #print(acl_list)
    acl_dict[acl_number]= acl_list
    f_acl.close()
    return(acl_dict)

if __name__ == '__main__':
    acl_dict_new = acl_file_to_dict(acl_new)
    acl_dict_current = acl_file_to_dict(acl_current)

for key in acl_dict_new:
    print(str(acl_dict_new[key]))
    print()

