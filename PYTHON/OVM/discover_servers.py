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

# Discover a new host and take ownership
# r = client.servers.discover()
#  print(client)
# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name('test001')
print(vm_id)

vm_template = client.vms.get_by_name('ol7-template-UEK-kernel')
print(vm_template)