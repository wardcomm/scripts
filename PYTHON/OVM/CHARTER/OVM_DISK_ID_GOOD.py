#!/usr/bin/env python
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json
import pprint
import array as arr

#variable
pp = pprint.PrettyPrinter(indent=4)
client = ovmclient.Client('base_Uri', 'user', 'password')
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)

s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

vm_id = client.vms.get_id_by_name('NAGA')
vm_value = str(vm_id['value'])
url = baseUri+'/'+'Vm/' + vm_value + '/VmDiskMapping'
response = s.get(url)
a = (response.text)
disk_id = print(a[229:265])

