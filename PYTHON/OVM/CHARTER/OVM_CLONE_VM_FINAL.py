#!/usr/bin/env python 
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json
import pprint

#variables
user = "p2906297"
password = "THem5dax"
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client( baseUri, user, password )
server_pool = "ndc-pool07-x86"
clone_template = "ol7-template-UEK-kernel"
new_server = sys.argv[1]
time.sleep(3)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
pp = pprint.PrettyPrinter(indent=4)
server_name = sys.argv[1]
s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

# Make sure the manager is running
client.managers.wait_for_manager_state()

pool_id = client.server_pools.get_id_by_name( server_pool )

# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name( clone_template )

# Set to True to create a VM template, False for a regular VM
create_template = False

# Clone the VM
try:
  job = client.jobs.wait_for_job(
    client.vms.clone(vm_id, pool_id, create_template=create_template))

except NameError:
  print("arguement was not given")
except IndexError:
  print("arguement was not given")
except:
  print("need to type example: .\OVM_CLONE_VM.py YODA in command line ")
new_vm_id = job['resultId']

data = client.vms.get_by_id(new_vm_id )
data["name"] = new_server
client.jobs.wait_for_job(client.vms.update(new_vm_id, data))

vm_get = client.vms.get_id_by_name(server_name)
vm_value = str(vm_get['value'])
url = baseUri+'/Vm/' + vm_value
get_data = s.get(url)
get_vm_id = get_data.json()
pretty_json = json.dumps(get_data.json(), indent=4)
dictionary = json.loads(pretty_json)
get_uri_from_disk_mapping = (dictionary['vmDiskMappingIds'][0])
get_uri = (get_uri_from_disk_mapping['uri'])
get_data_from_uri = s.get(get_uri)
get_data_from_uri_pretty = json.dumps(get_data_from_uri.json(), indent=4)
create_dictionary = json.loads(get_data_from_uri_pretty)
get_uri_from_disk_mapping_rename = (create_dictionary['virtualDiskId']['uri'])
img_url = (get_uri_from_disk_mapping_rename)
get_name = s.get(img_url)
json_convert = get_name.json()
glossary = json.dumps(json_convert)
d = json.loads(glossary)
next = str(int('0') + 1)
rename = "disk_" + server_name.lower() + "_" + next
d['name'] = rename
data_put = s.put(img_url, data=json.dumps(d),stream=True)

