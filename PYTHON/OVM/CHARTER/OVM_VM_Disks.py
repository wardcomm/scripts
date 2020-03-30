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

user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client( baseUri, user, password )
s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
#s.cert='/path/to/mycertificate.pem

# client.managers.wait_for_manager_state()

# Find server by name and take ownership

vm_id = client.vms.get_by_name('CHARLES')
# vm_value = client.vms.get_by_id(vm_id)
# print(vm_value)
# print(vm_id)
vm_key = vm_id.keys()
vm_values = vm_id.values()
vm_items = vm_id.items()
# x = vm_id.get("id")
x = vm_id["id"]
t = list(vm_id)
c = vm_values
y = vm_id.values()
# for item in vm_id:
#     if "id" in item:
#         print item.get("id").get("value")
# print(t)
print(x)
# print(vm_id['id'], vm_id['id'])
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
vm_value = print (x['value'])
print(type(vm_value))
print(vm_value)
oneline = print(str(baseUri)+"/Vm/"+ str(x['value']) +"/VmDiskMapping")
print(oneline)
print("!!!!!!!!!!!!!!!!!!!!!!")
# print type(vm_value)
print(vm_value)
# test_uri = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/VirtualDisk/0004fb000012000057d918986ad26e5e.img"
# client.vms.delete(test_uri)
# print(y)
# print(c)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

# print(chad)
# pprint.pprint(vm_key, indent=4)
# print(vm_values)
print("ZZZZZZZZZZZZZZZZZZZZZZZZZZ")
# print(vm_values["value"])
# pprint.pprint(vm_items, indent=4)
print("YYYYYYYYYYYYYYYYYYYYYYYYYYY")
# pprint.pprint(vm_values, indent=4)
print("***************************")
# pprint.pprint(vm_id, indent=4)
# pprint.pprint(vm_id)
# pprint.pprint(vm_value, indent=4)
# print("This is the vm id of\n" + str(vm_id))
# print(vm_id)

# disk_id = client.vms.get_id_by_name('Mapping for disk Id (0004fb0000120000857212a164441335.img)')

# client.vms.delete(vm_id)
# client.vms.delete(disk_id)