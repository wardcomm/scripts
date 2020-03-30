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
# print(repo_name)
repo_value = (repo_name['value'])
# print(repo_value) 


time.sleep(3)
vm_id = client.vms.get_id_by_name(argument)
vm_value = str(vm_id['value'])
url = baseUri+'/'+'Vm/' + vm_value + '/VmDiskMapping'
response = s.get(url)
a = (response.text)
disk_id = (a[229:265])

client.vms.delete(vm_id)
client.repository_virtual_disks(repo_value).delete(disk_id)