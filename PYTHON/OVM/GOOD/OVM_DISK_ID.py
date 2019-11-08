import ovmclient
import json
import requests
import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

#vars
user = 'p2906297'
password = 'THem5dax'

client = ovmclient.Client(
    'https://ovmdmgr04:7002/ovm/core/wsapi/rest', user, password)
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
# Make sure the manager is running
client.managers.wait_for_manager_state()
vm_id = client.vms.get_id_by_name('NAGA')
print(vm_id)
vm_value = str(vm_id['value'])
print(vm_value)
print(vm_value)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
print(repo_name)
repo_value = str(repo_name['value'])
print(repo_value) 
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
disk_id = client.vms.get_by_id(vm_value)
print(disk_id)
disk_map = client.vms.get_all()
disk_value = (disk_map['vmDiskMappingIds'])
print(disk_value)
print("***************")
# disk_id = client.virtual_disks.get_all_ids()
# print(disk_id)
disk_id = str("https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/"+ str(repo_value) +"/VmDiskMapping/")
print(disk_id)
# response = requests.get(basedisk_id, user, password, verify_cert=False)
# response.text
data = client.disk_mappings._get_id_value(vm_id)
print(data)
print("X")
print(disk_id)
# disk_id_value = client.repository_virtual_disks(vm_value).get_by_id(vm_id)
# print(disk_id_value)

# x = vm_id["id"]
# print(x)
# repo_num = print (x['value'])
# print(repo_num)
# print(vm_id + /'Vm'+ )
# # repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
# print(repo_name)
# repo_value = print (repo_name['value'])
# print(repo_value) 
# repo_value = client.vms.get_id_by_name + (repo_name['value'])
# print(repo_value)