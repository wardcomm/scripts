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
repo_id = (repo_name['value'])

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.trust_env = False
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
math = 1024 * 1024 * 1024 / 4096
answer = int(drive_size) * 4096 * int(math)
vm_id = client.vms.get_id_by_name(server_name)
disk_size = 1024 * 1024 * 1024
print("This is vm id value")
print(vm_id.get('value'))
print("This is vm id uri")
print(vm_id.get('uri'))
print("this is vm id")
print(vm_id)
print("This is the type of vm id")
print(type(vm_id))
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
DISK_TYPE_VIRTUAL_DISK = "VIRTUAL_DISK"
# Create a virtual disk
disk_data = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(drive_size) ,
    'shareable': True,
    'name': 'A_TEST_DISK.img',
}

job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(disk_data, sparse='true'))
disk_id = job['resultId']
print("this is disk id that was created")
print(disk_id)
vm_disk_mapping_data = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "3"
}
print("this is vm disk mapping post data that was sent")
print(vm_disk_mapping_data)
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data))
print("this is job")
print(job)
