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

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

argument = sys.argv[1]
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
print(repo_name)
repo_value = (repo_name['value'])
print(repo_value)

vm_id = client.vms.get_id_by_name(argument)
virtual_machine = (vm_id['value'])
print(virtual_machine)
print(vm_id)
vm_value = str(vm_id['value'])
url = baseUri+'/'+'Vm/' + vm_value + '/VmDiskMapping'
print(url)
vm_url = baseUri +'/Vm/'+ virtual_machine +'/VmDiskMapping'
print(vm_url)
data = s.get(url)
print(data)
json_data = data.json()
print(json_data)
x = json_data[0]
disk_id = print(x['virtualDiskId']['value'])

client.vms.stop(vm_id)
client.vms.delete(vm_id)
tests = client.repository_virtual_disks(repo_value).delete(disk_id)
print(tests)