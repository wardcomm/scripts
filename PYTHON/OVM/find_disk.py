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
# repo_id = client.repositories.get_id_by_name('ndc2-pool07-repo')
# pool_id = client.server_pools.get_id_by_name('pool07-virt1-repo')
# network_id = client.networks.get_id_by_name('22.244.4.0')

# Make sure the manager is running
client.managers.wait_for_manager_state()

# Find server by name and take ownership

vm_id = client.vms.get_id_by_name('BAT_MAN')
print("This is the vm id of\n" + str(vm_id))
print(vm_id)



# vm_id_disk = client.vms.get_id_by_name.VmDiskMapping('BAT_MAN')
# print(vm_id_disk)

server = client.servers.discover('BAT_MAN')
print(server)
# https://10.136.170.208:7002/ovm/core/wsapi/rest/VmDiskMapping/?name=BAT_MAN
# client.vms.delete(vm_id)
# client.VirtualDiskManager
# disk = client.vm_disk_mappings.discover('BAT_MAN')
# print(disk)
# # Make sure the manager is running
# client.managers.wait_for_manager_stat
# e()
# print("make sure manager is running")
# print(vm_id)

# # Discover a new host and take ownership
# vm_discover = client.servers.discover(vm_id)
# print("discover server")
# print(vm_discover)
# def vmList(s,baseUri):
#     print ("\nVM List:")
#     print ("########")
#     r=s.get(baseUri+'/Vm')
#     for i in r.json():
#     # print '{:20} {:20}'.format(i['vmRunState'],i['name'])
#         print ('{:20} {:35} {:30}'.format(i['vmRunState'],i['name'],i['id']['value'])),
#     for d in i['vmDiskMappingIds']:
#         print(d['value']),
#     print
    # print '{name} '.format(name=i['name'])
    # print i
 # Get an existing VM or a VM template
# job = client.jobs.wait_for_job(
#     client.vm_disk_mappings(vm_id).create(vm_disk_mapping_data))
# print(job)
# disk_id = client.discover('BAT_MAN')
# print(disk_id)
repo_id = client.repositories.get_id_by_name('ndc2-pool07-repo')
# pool_id = client.server_pools.get_id_by_name('pool07-virt1-repo')
network_id = client.networks.get_id_by_name('22.244.4.0')
print("This is REPO")
print(repo_id)
# print("This is pool id")
# print(pool_id)
print("this is network")
print(network_id)