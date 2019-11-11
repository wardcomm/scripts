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
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

argument = sys.argv[1]
argument2 = sys.argv[2]
argument3 = sys.argv[3]

vm_id = client.vms.get_id_by_name(argument)
vm_value = str(vm_id['value'])
data = client.vms.get_by_id(vm_value)
print(vm_value)
old_memory = (data['memory'])
old_memory_max = (data['memoryLimit'])
print(argument)
print(argument2)
print(data)
print(old_memory)
print(old_memory_max)
new_memory = argument2
new_memory_max = argument3
print(new_memory)
print(new_memory_max)
# Update the VM, e.g. setting a new name
# vm['name'] = 'vm2'
vm_id[old_memory] = new_memory
vm_id[old_memory_max] = new_memory_max
client.vms.update(vm_value, data = {'memory':new_memory})
client.vms.update(vm_value, data = {'memoryLimit':new_memory_max})
