#!/usr/bin/env python 
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
#os.system('clear') # clear screen
#variables
user = "p2906297"
password = "THem5dax"
url_api = "https://10.136.170.208:7002/ovm/core/wsapi/rest"
client = ovmclient.Client( url_api, user, password )
server_pool = "ndc-pool07-x86"
clone_template = "ol7-template-UEK-kernel"
#print(client)
case1 = sys.argv[1]
time.sleep(3)
print case1
# Make sure the manager is running
client.managers.wait_for_manager_state()

pool_id = client.server_pools.get_id_by_name( server_pool )

# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name( clone_template )

# Set to True to create a VM template, False for a regular VM
create_template = False
print  case1 
print "\nCloning VM"
print "##############"
print "Creating VM", case1, "from", clone_template


# Clone the VM
job = client.jobs.wait_for_job(
    client.vms.clone(vm_id, pool_id, create_template=create_template))
new_vm_id = job['resultId']

# Rename the VM template
data = client.vms.get_by_id(new_vm_id)
data["name"] = case1
client.jobs.wait_for_job(client.vms.update(new_vm_id, data))

# Delete the VM template
#client.jobs.wait_for_job(client.vms.delete(new_vm_id))
#
print (" -Done\n")

