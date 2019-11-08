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
import array as arr

pp = pprint.PrettyPrinter(indent=4)
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
vm_id = client.vms.get_id_by_name('NAGA')
print(vm_id)
vm_value = str(vm_id['value'])
print(vm_value)
print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
def check_manager_state(baseUri,s):
        while True:
            r=s.get(baseUri+'Vm/')
            Virtual_Machine=r.json()
            if Virtual_Machine[0]['vmRunState'].upper() == 'RUNNING':
                break
            time.sleep(1)
        return
# def get_disk_id(baseUri,s):
#         while True:
#             r.s.get(baseUri + vm_value/+'VmDiskMapping')
#             Virtual_Machine=r.json()
#             print(get_disk_id)
#         return        
# get_disk_id(vm_value)        
# response = s.get(baseUri) + (vm_value/)+ ('VmDiskMapping')
print("\n\n\n\n\n\n   THIS IS THE BEGINNING")

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
data = s.get(baseUri)
print(data)

# data_map = (baseUri,s,+vm_value/+"VmDiskMapping")
# disk_id = response.json()
# print(data_map)
url = baseUri+'/'+'Vm/' + vm_value + '/VmDiskMapping'
print(url)
print("\n\n\n\n\n\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
response = s.get(url)
data = response.json()

print('RESPONSE HTTP ERROR CODE',response.status_code)
print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
print(type(data))
print(data)
print("TRYING TO PARSE THE DATA")


# def Convert(a): 
#     it = iter(data) 
#     res_dct = dict(zip(it, it)) 
#     return res_dct
# print(Convert(data))    

# print(data['id'],['value'])

# data = json.loads(response)
# print (data['value'])
# if filename:
#     with open(filename.json, 'w') as file:
#         json.dump(respoonse, f)
# dictionary = json.dumps(response)
# load_json = json.loads(dictionary)
# dictionary.get(['virtualDiskId'])
# print(response['virtualDiskId'])
x = response.json()
# print("disk id" + str(type(data[9]['value'])))
# print(type(x))
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
# print(x[0])
# for key, value in mapping.items():
#     print(f'{key}: {value}')
# print([key for key in x.keys()][1])
# for key in response:
#     print(key)
# print(x["value"])
# print(x.json())
print("))))))))))))))))))))))))))))))))))))))")
data = json.dumps(x)
# with open('disk_id_data.json', 'r') as fp:
json_data = json.loads(data)
# print(json_data)
print(json_data)
print("\n\n\n\n\n\nprinting json loads")
# print(data['value'])
python_dictionary = json.loads(data)
print(python_dictionary)
print("pooooooooooooooooooooooop is this an array")
print(data[50:120])
# print (json_data['value'])
# print(data['id'])
# print(variable)
# print(x.value,x.uri)
# print(dude)
# real_data =x["value"]
# print(real_data).
# for i in data["id"]:
#     print({i["value"]})
print(type(data))
# print(data([0]))
print("$$$$$$$$$$$$$$$$")
print(response.raw)
print("!!!!!!!!!!!!!!!!!!")
print(type(x))
print("\n\n\n\n\n\npretty print")
a = (response.text)
pp.pprint(type(a))
disk_id = print(a[229:265])
print(disk_id)
pp.pprint(response.ok)
pp.pprint(response.headers)
pp.pprint(response.raw)
