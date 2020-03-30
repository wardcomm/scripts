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

# Make sure the manager is running
client.managers.wait_for_manager_state()
vm_id = client.vms.get_id_by_name('NAGA')
print(vm_id)
# x = vm_id["id"]
# print(x)
# repo_num = print (x['value'])
# print(repo_num)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
print(repo_name)
repo_value = print (repo_name['value'])
print(repo_value) 
# repo_value = client.vms.get_id_by_name + (repo_name['value'])
# print(repo_value)