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
# drive_size = sys.argv[2]
repo_id = (repo_name['value'])

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.trust_env = False
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
math = 1024 * 1024 * 1024 / 4096
# answer = int(drive_size) * 4096 * int(math)
vm_id = client.vms.get_id_by_name(server_name)
disk_size = 1024 * 1024 * 1024
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
DISK_TYPE_VIRTUAL_DISK = "VIRTUAL_DISK"
next = str(int('0') + 1)
secondary_disk = str(int(next) + 1)
rename = "disk_" + server_name + "_" + next
asm_data_fist_disk = "asm_" + "data_" + next
asm_data_second_desk = "asm_" + "data_" + secondary_disk
asm_data_drive_size = 500
asm_reco_drive_size = 150
asm_grid_drive_size = 50
asm_acfs_drive_size = 100
# Create a virtual disk
asm_data_1 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_data_drive_size) ,
    'shareable': True,
    'name': 'asm_data_1_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_data_1, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_data_1 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "2"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data_1))

# Create a virtual disk
asm_data_2 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_data_drive_size) ,
    'shareable': True,
    'name': 'asm_data_2_'+ server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_data_2, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_data_2 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "3"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data_2))

# Create a virtual disk
asm_data_3 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_data_drive_size) ,
    'shareable': True,
    'name': 'asm_data_3_' +  server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_data_3, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_data_3 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "4"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data_3))
# Create a virtual disk
asm_data_4 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_data_drive_size) ,
    'shareable': True,
    'name': 'asm_data_4_' + server_name ,
}

job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_data_4, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_data_4 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "5"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data_4))

# ASM RECO DISK
# Create a virtual disk
asm_reco_1 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_reco_drive_size) ,
    'shareable': True,
    'name': 'asm_reco_1_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_reco_1, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_reco_1 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "6"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_reco_1))
# Create a virtual disk
asm_reco_2 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_reco_drive_size) ,
    'shareable': True,
    'name': 'asm_reco_2_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_reco_2, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_reco_2 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "7"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_reco_2))
# Create a virtual disk
asm_reco_3 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_reco_drive_size) ,
    'shareable': True,
    'name': 'asm_reco_3_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_reco_3, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_reco_3 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "8"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_reco_3))
# Create a virtual disk
asm_reco_4 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_reco_drive_size) ,
    'shareable': True,
    'name': 'asm_reco_4_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_reco_4, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_reco_4 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "9"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_reco_4))
#ASM GRID DISK
# Create a virtual disk
asm_grid_1 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_grid_drive_size) ,
    'shareable': True,
    'name': 'asm_grid_1_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_grid_1, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_grid_1 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "10"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_grid_1))
#ASM GRID DISK
# Create a virtual disk
asm_grid_2 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_grid_drive_size) ,
    'shareable': True,
    'name': 'asm_grid_2_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_grid_2, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_grid_2 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "11"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_grid_2))
#ASM GRID DISK
# Create a virtual disk
asm_grid_3 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_grid_drive_size) ,
    'shareable': True,
    'name': 'asm_grid_3_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_grid_3, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_grid_3 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "12"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_grid_3))
#ASM ACFS DISK
# Create a virtual disk
asm_acfs_1 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_acfs_drive_size) ,
    'shareable': True,
    'name': 'asm_acfs_1_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_acfs_1, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_acfs_1 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "13"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_acfs_1))
# Create a virtual disk
asm_acfs_2 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_acfs_drive_size) ,
    'shareable': True,
    'name': 'asm_acfs_2_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_acfs_2, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_acfs_2 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "14"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_acfs_2))
# Create a virtual disk
asm_acfs_3 = {
    'diskType': (DISK_TYPE_VIRTUAL_DISK),
    'size': int(disk_size) * int(asm_acfs_drive_size) ,
    'shareable': True,
    'name': 'asm_acfs_3_' + server_name ,
}
job = client.jobs.wait_for_job(client.repository_virtual_disks(repo_id).create(asm_acfs_3, sparse='true'))
disk_id = job['resultId']
#This is disk mapping
vm_disk_mapping_acfs_3 = {
	"virtualDiskId": disk_id,
	#  "diskWriteMode": "READ_WRITE",
	#  "emulatedBlockDevice": "false",
	# "storageElementId": "None",
	 "diskTarget": "15"
}
job = client.jobs.wait_for_job(client.vm_disk_mappings(vm_id).create(vm_disk_mapping_acfs_3))







