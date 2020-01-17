import requests
import sys
import urllib3
import ovmclient
import json
import pprint
import time

#variable
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
server_name = sys.argv[1]
drive_size = sys.argv[2]

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.trust_env = False
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
math = 1024 * 1024 * 1024 / 4096
answer = int(drive_size) * 4096 * int(math)

vm_disk_mapping_data = {
	"virtualDiskId": "0004fb0000120000daf6056c18e70eed.img",
	"diskWriteMode": "READ_WRITE",
	"emulatedBlockDevice": "false",
	"storageElementId": "None",
	"diskTarget": "3"
}

# data_mapping = {
#     'virtualDiskId': iso_id,
#     'diskTarget': slot, # here specify the slot number
#     }
# image = "0004fb0000120000daf6056c18e70eed.img"
#  0004fb00000600006d8682d0a02325d4
test = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/VmDiskMapping"
id = "0004fb0000120000daf6056c18e70eed.img"
disk_name = input("enter disk name:")
slot = input("Enter Slot Number:")
VM_name = input("Enter Server name:")
iso_id = ('vm',VM_name)
vm_disk_mapping_data = {
    'virtualDiskId': iso_id,
    'diskWriteMode':"READ_WRITE",
    'emulatedBlockDevice': False,
    'storageElementId': None,
    'diskTarget': slot,
    }

VMNAME = raw_input("Enter guest VM name:")
ISO = raw_input("Enter ISO/Disk name:")
vm_id = self.get_id_from_name('Vm', VMNAME)
iso_id = self.get_id_from_name('VirtualDisk',ISO)
slot= raw_input("Enter the slot number:")
uri = '{base}/Vm/{vmid}/VmDiskMapping'.format(base=self.baseuri, vmid=vm_id['value'])
Data4 = {
    'virtualDiskId': iso_id,
    'diskTarget': slot, # here specify the slot number
}
createVmDiskMap = self.session.post(uri, data=json.dumps(Data4))
createVmDiskMapJson = createVmDiskMap.json()
VmDiskMapId = self.wait_for_job(createVmDiskMapJson['id']['uri'])
print ("ISO/Disk attached")

createVmDiskMap = s.post(test, data=json.dumps(vm_disk_mapping_data))
print(createVmDiskMap)
print(createVmDiskMap)
print(createVmDiskMap.headers)
print(createVmDiskMap)
print(createVmDiskMap.content)
print(createVmDiskMap.text)
print(createVmDiskMap.raw)

data_post = s.head(test, data=json.dumps(vm_disk_mapping_data))

uri = str(baseUri + "/Vm/" + id)
r = s.get(uri)
vm = r.json()
print(vm)
print(data_post)
print(data_post.headers)
print(data_post)
print(data_post.content)
print(data_post.text)
print(data_post.raw)

get_options = s.options(test)
# get_json_options = get_options.json()
print(get_options)