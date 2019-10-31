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

# Find server by name and take ownership

vm_id = client.vms.get_id_by_name('THOR')
print("This is the vm id of\n" + str(vm_id))
print(vm_id)

client.vms.delete(vm_id)

# # Make sure the manager is running
# client.managers.wait_for_manager_stat
# e()
# print("make sure manager is running")
# print(vm_id)

# # Discover a new host and take ownership
# vm_discover = client.servers.discover(vm_id)
# print("discover server")
# print(vm_discover)
