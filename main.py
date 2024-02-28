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

d_acl_new = {}
d_acl_current = {}
acl_number = 0
acl_list = []
for line in f_acl_new:
    if "no access-list" in line:
        d_acl_new[acl_number]= acl_list
        acl_number = line.split()[2]
        #print(acl_list)
        acl_list = []
    else:
        acl_list.append(line)
        #print(acl_list)
d_acl_new[acl_number]= acl_list
#print(d_acl_new)

for key in d_acl_new:
    print(str(d_acl_new[key]))
    print()

