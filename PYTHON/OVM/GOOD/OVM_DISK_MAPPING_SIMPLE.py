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
disk_id = '0004fb0000120000e8b20d9d1b3cc1b7.img'
slot = '3'
s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.trust_env = False
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

test = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/VmDiskMapping'

vm_disk_mapping_data = {
'virtualDiskId': disk_id,
'diskWriteMode':"READ_WRITE",
'emulatedBlockDevice': False,
'storageElementId': None,
'diskTarget': slot,
}
createVmDiskMap = s.post(test, data=json.dumps(vm_disk_mapping_data))