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
# constants = DISK_TYPE_VIRTUAL_DISK = "VIRTUAL_DISK"
# print(repo_value)
pp = pprint.PrettyPrinter(indent=4)
# server_name = sys.argv[1]
server_name = sys.argv[1]
drive_size = sys.argv[2]

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

math = 1024 * 1024 * 1024 / 4096
answer = int(drive_size) * 4096 * int(math)
print("THIS IS MY FINAL ANSWER")
print(answer)
vm_id = client.vms.get_id_by_name(server_name)
vm_value = str(vm_id['value'])
url = baseUri + '/Vm/' + vm_value + '/VmDiskMapping'
data = s.get(url)
print(data)
json_data = data.json()
# print(json_data)
x = json_data[0]
disk_id = (x['virtualDiskId']['value'])




vm_id = client.vms.get_id_by_name(server_name)
url = baseUri + '/Vm/' + vm_value + '/VmDiskMapping/'
print(vm_id)
vm_value = str(vm_id['value'])
print(vm_value)
disk_id = client.vms.get_by_id(vm_value)

print(disk_id)

# increment += 1
# print(increment)
# disk_naming = server_name + increment
# print(disk_naming)
disk_naming = 'dummy_'+ server_name.lower() +'.img'
print(disk_naming)

disk_data = {
    'diskType': "VIRTUAL_DISK",
    'size': answer,
    'shareable': True,
    'name': disk_naming,
}
image = "0004fb0000120000daf6056c18e70eed.img"
# image = "dummy.img"
# Map the virtual disk
vm_disk_mapping_data = {
   "virtualDiskId":image,
   "diskWriteMode":"READ_WRITE",
   "emulatedBlockDevice":False,
   "storageElementId":"None",
   "diskTarget":3
}

print("A")
print(disk_naming)
print("B")
print(vm_id)
print("C")
print(vm_disk_mapping_data)
print("D")
print(repo_value)
print("E")
print(disk_data)
print("F")

map = "0004fb00000600006d8682d0a02325d4"

# abc_url = baseUri + '/Repositories/0004fb0000030000b7b4973509ec4981/VirtualMachines/0004fb00000600006d8682d0a02325d4/vm.cfg'
# xyz_url = baseUri + '/VmDiskMapping/0004fb0000130000a0e46130e576e5ac'
# test = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/VmDiskMapping/"
test = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/"
# test = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/VmDiskMapping/"
# test_url = baseUri + /VmDiskMapping/'
# print("this is repository id virtualmachine id")
# print(abc_url)
# print("this is virtualdiskmapping")
# print(xyz_url)
# get_data = s.get(abc_url)
# get_more = s.get(xyz_url)
# json_data = get_data.json()
# json_data_2 = get_more.json()
# print(json.dumps(json_data, indent=4))
# print(json.dumps(get_more, indent=4))
image = "0004fb0000120000daf6056c18e70eed.img"
# superman = baseUri + "/Vm/"+ vm_id + "/VmDiskMapping"
print(test)
get_data = s.get(test)
pretty_json = json.dumps(get_data.json(), indent=4)
# superman = baseUri + "/Vm/"+ vm_id + "/VmDiskMapping"
dictionary = json.loads(pretty_json)
get_data = s.get(url)
print(pretty_json)
print(dictionary)
# mapping_uri = baseUri + '/Vm/' + vm_id + '/VmDiskMapping/'
# print(mapping_uri)
# # print(disk_data)
# client.repository_virtual_disks(repo_value).create(disk_data, sparse='true')
# client.vm_disk_mappings(map).create(vm_disk_mapping_data)
# img_url = (get_uri_from_disk_mapping_rename)
vm_get = client.vms.get_id_by_name(server_name)
vm_value = str(vm_get['value'])
url = baseUri+'/Vm/' + vm_value
get_data = s.get(url)
final_data = test + image
print(test)
print(final_data)
# client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data)
data_put = s.post(test, data=json.dumps(vm_disk_mapping_data))
print(data_put)
print(data_put.content)
print(data_put.text)
# post url data