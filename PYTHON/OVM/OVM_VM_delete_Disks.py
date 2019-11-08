#!/usr/bin/env python
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json

client = ovmclient.Client('base_Uri', 'user', 'password')
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)

s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
#s.cert='/path/to/mycertificate.pem

def check_manager_state(baseUri,s):
        while True:
            r=s.get(baseUri+'Vm/')
            Virtual_Machine=r.json()
            if Virtual_Machine[0]['vmRunState'].upper() == 'RUNNING':
                break
            time.sleep(1)
        return

response=s.get(baseUri+'/Vm')
for i in response.json():
  data_array =  print ('{name} is {state} and drive is {DiskMapping}'.format(name=i['name'],state=i['vmRunState'],DiskMapping=i['vmDiskMappingIds']))
  server = "BAT_MAN" in response
  json_data = json.loads(response.text)
  print(json_data)
  print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
  print(server)
  print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
  print(data_array)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# jdata = json.loads("vmDiskMappingId")
# Get an existing VM or a VM template
vm_id = client.vms.get_id_by_name('BAT_MAN')
print(vm_id)
# disk_id = client.disk_mappings.get_id_by_name()
# print(disk_id)
test = client.
print(test)
       # do something with the content
# if i == server:

    #   print ('{name} is {state} and drive is {DiskMapping}'.format(name=i['name'],state=i['vmRunState'],DiskMapping=i['vmDiskMappingIds']))

# data array =  ['r']
# servertoDelete = input (server.find)

# print(json.dumps(server))

