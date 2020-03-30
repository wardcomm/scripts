import requests
import sys
import urllib3
import ovmclient
import json

#variable
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

server_name = sys.argv[1]
new_memory = sys.argv[2]
new_memory_max = sys.argv[3]

vm_id = client.vms.get_id_by_name(server_name)
vm_value = str(vm_id['value'])
url = baseUri+'/Vm/' + vm_value
real_data = client.vms.get_by_id(vm_id)
real_data["memory"] = new_memory
real_data["memoryLimit"] = new_memory_max
data_put = s.put(url,data=json.dumps(real_data))# the line that does the magic of  modifying


