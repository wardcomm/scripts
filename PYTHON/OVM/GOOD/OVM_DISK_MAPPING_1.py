import requests
import sys
import urllib3
import ovmclient
import json
import pprint

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

diskid = "0004fb0000120000daf6056c18e70eed.img"
# Sample script of VmDiskMapping:
# Create a VmDiskMapping to represent association of VirtualDisk to Vm

# uri4 = '{base}/Vm/{vmid}/VmDiskMapping'.format(base=s.baseUri, vmid=newVmId['value']) 
test = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/VmDiskMapping"
Data4 = {
'virtualDiskId': diskid,
'diskTarget': 3,
}
createVmDiskMap = s.post(test, data=json.dumps(Data4))
createVmDiskMapJson = createVmDiskMap.json()
# VmDiskMapId = s.wait_for_job(createVmDiskMapJson['id']['uri'])
print(createVmDiskMapJson)
print ("Disk attached") 