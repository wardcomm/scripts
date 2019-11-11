import ovmclient
import json
import requests
import warnings
import sys
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

#vars
user = 'p2906297'
password = 'THem5dax'

client = ovmclient.Client(
    'https://ovmdmgr04:7002/ovm/core/wsapi/rest', user, password)

# Make sure the manager is running
client.managers.wait_for_manager_state()
# type in argument after script
argument = sys.argv[1]

# Find server by name and take ownership

vm_id = client.vms.get_id_by_name(argument)
# print("This is the vm id of\n" + str(vm_id))
# print(vm_id)
# disk_id = client.vms.get_id_by_name('Mapping for disk Id (0004fb0000120000857212a164441335.img)')
# client.vms.delete(vm_id)
# client.vms.delete(disk_id)
client.vms.stop(vm_id)
