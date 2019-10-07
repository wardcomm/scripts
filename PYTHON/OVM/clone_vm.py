#!/usr/bin/python
import requests
import urllib3
import ovmclient
import sys
#case1 = sys.argv[1]
print (len(sys.argv)

#requests.packages.urllib3.disable_warnings()


headers = {
    'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "7c4fe2a4-d1cc-48af-9d07-bb09de6eccd7,4e7a46ea-58ae-4e23-91fb-eb778068ca8e",
    'Host': "ovmdmgr04:7002",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "JSESSIONID=qUiNxlPHC8Z5j7REXLnEB9G7LQIHeAEf0l_IcF8oo2FHzVnMNjBa!-209135736; _WL_AUTHCOOKIE_JSESSIONID=KVUaS22fIk9-wWP.09az",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

#variables
user = 'p2906297'
password = 'THem5dax'

client = ovmclient.Client(
    'https://10.136.170.208:7002/ovm/core/wsapi/rest', 'user', 'password')

# Make sure the manager is running
client.managers.wait_for_manager_state()

pool_id = client.server_pools.get_id_by_name('ndc-pool07-x86')

# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name('ol7-template-UEK-kernel')

# Set to True to create a VM template, False for a regular VM
create_template = False

print("""
print "\nCloning VM"
print "##############"
print "Creating VM",case1,"from" vm_il"
""")

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
print( " -Done\n")
