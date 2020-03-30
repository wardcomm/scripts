import requests
import sys
import urllib3
import ovmclient
import json
import pprint

#variable
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
pp = pprint.PrettyPrinter(indent=4)
server_name = sys.argv[1]
s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
vm_get = client.vms.get_id_by_name(server_name)
# print(vm_get)
vm_value = str(vm_get['value'])
url = baseUri+'/Vm/' + vm_value
vm_get = s.get(url)
print(vm_value)