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

class OVMManager():
    def __init__(self, name):
        self.name = name
        self.baseuri = "https://" + self.name + ":7002/ovm/core/wsapi/rest"
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.session.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
        self.session.auth = (user, password)

    def get_id_from_name(self, resourceType, name):
        response = self.session.get(self.baseuri + "/" + resourceType + "/id" )
        for obj in response.json():
            if 'name' in obj.keys():
             if obj['name'] == name:
                 return obj
        raise Exception('Failed to find id for {name}'.format(name=name))

    def attach(self):
        VMNAME = input("Enter guest VM name:")
        ISO = input("Enter ISO/Disk name:")
        vm_id = self.get_id_from_name('Vm', VMNAME)
        iso_id = self.get_id_from_name('VirtualDisk',ISO)
        slot= input("Enter the slot number:")
        uri = '{base}/Vm/{vmid}/VmDiskMapping'.format(base=self.baseuri, vmid=vm_id['value'])
        Data4 = {
            'virtualDiskId': iso_id,
            'diskTarget': slot, # here specify the slot number
        }
        createVmDiskMap = self.session.post(uri, data=json.dumps(Data4))
        createVmDiskMapJson = createVmDiskMap.json()
        VmDiskMapId = self.wait_for_job(createVmDiskMapJson['id']['uri'])
        print ("ISO/Disk attached")

    def wait_for_job(self, job, sleep_seconds=.5):
        while not job.get('summaryDone'):
            time.sleep(sleep_seconds)
            job = self.get_by_id(job['id'])

        if job['jobRunState'].upper() == constants.JOB_RUN_STATE_FAILURE:
            raise exception.JobFailureException(job)
        return job

# OVMManager.attach()

# vm_id = OVMManager.get_id_from_name('Vm', server_name)
# iso_id = OVMManager.get_id_from_name('VirtualDisk',ISO)
# slot = input("Enter the slot number:")
# vm_disk_mapping_data = {
# 	"virtualDiskId": "0004fb0000120000daf6056c18e70eed.img",
# 	"diskWriteMode": "READ_WRITE",
# 	"emulatedBlockDevice": "false",
# 	"storageElementId": "None",
# 	"diskTarget": "3"
# }
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
    # 'storageElementId': None,
    'diskTarget': slot,
    }

createVmDiskMap = s.post(test, data=json.dumps(vm_disk_mapping_data))
print(createVmDiskMap)
print(createVmDiskMap)
print(createVmDiskMap.headers)
print(createVmDiskMap)
print(createVmDiskMap.content)
print(createVmDiskMap.text)
print(createVmDiskMap.raw)
# createVmDiskMap = OVMManager.s.post(uri, data=json.dumps(data_mapping))
# createVmDiskMapJson = createVmDiskMap.json()
# VmDiskMapId = OVMManager.wait_for_job(createVmDiskMapJson['id']['uri'])
# print ("ISO/Disk attached")
# vmCreateDiskMapping
# VmDiskMapping
# get_data = s.get(test)
# json_convert = get_data.json()
# print(get_data)
# # print(json_convert)
# glossary = json.dumps(json_convert, indent = 4)
# print(glossary)
# d = json.loads(glossary)
# print(d)
# client.vm_disk_mappings("0004fb00000600006d8682d0a02325d4").create(vm_disk_mapping_data)
# data_post = s.post(test, data=json.dumps(d), stream=True)
# data_post = s.post(test, data=json.dumps(vm_disk_mapping_data))

# data_post = s.post(test, data=json.dumps(vm_disk_mapping_data))
# data_post = s.options(test, data=json.dumps(vm_disk_mapping_data))
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