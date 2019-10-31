#!/usr/bin/env python
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json

user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'

s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

response = s.get(baseUri+'/Vm')
print(response.text)
# print(type(response))
for i in response.json():
#   print(i)
#   print(type(i))
  with open("data_file.json", "w") as write_file:
    data = json.dump(i, write_file, indent = 4, sort_keys=False)
    # dataload = json.loads(data)
  with open('data_file.json') as file:
    read_data = json.load(file)
    # print(type(read_data))
    read_data['BAT_MAN'] = "SPIDER_MAN";
    print(read_data['name'])
    #  print(data)
    # string = "BAT_MAN"
    # print(json.dumps(string))
    # print(read_data)
    # print(type(read_data))
    # obj = print (read_data['name'])
    # obj['BAT_MAN'] = 'SPIDER_MAN';
    # print(obj)
    # superhero = obj['BAT_MAN']
    # print(superhero)
    #   print(json.dumps({id} , {name}))
#   json_data = (response.json(i)
#   json_data = json.loads()
    # for item in  read_data:
    #     if item.get('id') == "name":
    #        item['BAT_MAN']  = SPIDER_MAN
# print(json_data)
#   print(i)
#   print()
#   print(type,(i))
  #print(json.dumps(response))
  #print(type(response.json))
  #json_data = json.loads(response)
#   print(json_data)
#   print(json.loads(response))
#   print(response.ok)
#   print(response.status_code)
#   print(response)
#   data_array =  print ('{name} is {state} and drive is {DiskMapping}'.format(name=i['name'],state=i['vmRunState'],DiskMapping=i['vmDiskMappingIds']), end='\n')
#   print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#   print_array = print('{name} is running {state}'.format(name=i['name'],state=i['vmRunState']))
#  x = print('{name}{diskmapping}'.format(name=i['name'],diskmapping=i['vmDiskMappingId']['value']))
#   print(data_array'{name}'.format(name=i['BAT_MAN'])

# repo_id = get_id_from_name(s,baseUri,'Repository','pool07-virt1-repo')
# serverpool_id = get_id_from_name(s,baseUri,'ServerPool','ndc-pool07-x86')

data_json = {
    "name":"ovm_test_api",
    "description":"A Test server for ORacle  api",
    "vmDomainType":"Xen HVM PV Drivers",
    "repositoryId":"ndc2-pool07-repo",
    "serverPoolId":"ndc-pool07-x86",
    "cpuCount":"1",
    "cpuCountLimit":"1",
    "cpuPriority":"50",
    "cpuUtilizationCap":"100",
    "hugePagesEnabled":"False",
    "memory":"1024",
    "memoryLimit":"1024",
    "osType":"Oracle Linux 7",
    "osVersion":"Oracle Linux Server release 7.6"
 }

response = s.post(baseUri+'/Vm', data = data_json )
print('RESPONSE HTTP ERROR CODE',response.status_code)
print(response.raw)