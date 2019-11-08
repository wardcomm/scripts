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

vm_id = client.vms.get_id_by_name('THE_WASP')
print(vm_id)
# print("This is the vm id of\n" + str(vm_id))
# print(vm_id)
# disk_id = client.__init__.get_by_name('ol7-template-uek (9)')
# client.vms.delete(vm_id)
# client.vms.delete(disk_id)

# # Make sure the manager is running
# client.managers.wait_for_manager_stat
# e()
# print("make sure manager is running")
# print(vm_id)

# # Discover a new host and take ownership
# vm_discover = client.servers.discover(vm_id)
# print("discover server")
# print(vm_discover)
# Delete the virtual disk

# client.jobs.wait_for_job(
#     client.repository_virtual_disks(repo_id).delete(disk_id))
client.vms.delete(vm_id)
client.repository_virtual_disks('0004fb000003000038a326c390954c23').delete('0004fb000012000057d918986ad26e5e.img')    

    # def __init__(self, conn, repository_id=None):
    #     if repository_id:
    #         rel_path = "Repository/%s/VirtualDisk" % self._get_id_value(
    #             repository_id)
    #     else:
    #         rel_path = 'VirtualDisk'
    #     super(VirtualDiskManager, self).__init__(conn, rel_path)