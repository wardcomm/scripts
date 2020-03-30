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
url = baseUri+'/Vm/' + vm_value
print(url)
data = client.vms.get_by_id(vm_value)
catcher = s.get(url)
json_data = catcher.json()
new_memory = argument2
new_memory_max = argument3
print("This is json data")
print(type(json_data))
print(json_data)
print("modify")
package = {'memory': new_memory}
modify = s.put(url, data = json.dumps(package))
print("what did i do")
print(modify)
print(modify.headers)
print(modify.content)
print('\n')
print(data)
print("This is pretty data")
cool = json.dumps(json_data, indent  = 4)
print(cool)
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
memory_change = vm_id["memory"] = new_memory
vm_id["memoryLimit"] = new_memory_max
# client.vms.update(vm_value, new_memory)
# client.vms.update(vm_value, new_memory_max)

# client.vms.update(memory_change, new_memory)
# client.vms.update(memory_change, new_memory)

# memory=dict(memory=4096, memoryLimit= 4096)


# 
# new_vm_id = job['resultId']
real_data = client.vms.get_by_id('0004fb00000600007f0ba7d45c0132ad')

print(real_data)# data = client.vms.get_by_id(new_vm_id)
print("This is a test")
real_data["memory"] = new_memory
real_data["memoryLimit"] = new_memory_max
print(real_data)
# 
data_put = s.put(url,data=json.dumps(real_data),params={},verify=False)
print("nice_nice_nice")
print(data_put)
print("come on and work")
# 
dict1 = { 'memory' : '4096'}
dict2 = { 'memoryLimit' : '4096'}
variable1 = requests.put(url,params=dict1,verify=False)
print(variable1)


# json_stuff = variable1.json()
# print(json_stuff)

# catcher = s.get(url)
# json_data = catcher.json()
# requests.put(url, dict1.update.(real_data))
data_for_server = s.put(url,data = { "memory" : "4096"},verify=False)
print(data_for_server.content)
# response = requests.put(url, real_data)
# response = requests.put(url, data = memory)
# response = requests.put(url, data = {'memory':'2096'})
# print(response.content)

# job = client.jobs.wait_for_job(
#     client.vms.clone(vm_id, pool_id, create_template=create_template))
# new_vm_id = job['resultId']