import requests
import urllib3
import ovmclient
import sys
import os
import time
import json
import pprint
import array as arr
# import simplejson as json

#variable
pp = pprint.PrettyPrinter(indent=4)
client = ovmclient.Client('base_Uri', 'user', 'password')
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

argument = sys.argv[1]
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])

time.sleep(3)
vm_id = client.vms.get_id_by_name(argument)
vm_value = str(vm_id['value'])
url = baseUri+'/'+'Vm/' + vm_value + '/VmDiskMapping'
print(url)
# print(url)
data = s.get(url)

# json_stuff = data.json
# print(json_stuff['id'])


# what = data.url()
# print(what['value'])
# print(what)
print(data)
# value = str(url['VmDiskMappingIds'])
# print(value)
# disk_id = (data['value'])
# print(disk_id)
print("this is naked response")
response = s.get(url)
chad = response.json()
MY_DATA = chad
serialized_data = json.dumps(MY_DATA)
file = open("data_file.json", "w")
file.write(serialized_data)
print(type(serialized_data))
print(serialized_data)
file.close()
print('\n')
print("this is dict in a array cool site https://jsoneditoronline.org/")
x = chad[0]
print(type(x))
print(x)
print('\n')
print("chad the shit")
chad_the_shit = print(x['virtualDiskId']['value'])
print(chad_the_shit)
print('\n', '\n')
# dictOfWords = dict.fromkeys(response , 2)
# array_json = MY_DATA
# # list_data = json.loads(chad)
# dictionary_data = json.loads(dictOfWords)
# print(type(list_data))
# print(list_data)
# print(type(dictionary_data))
# print(dictionary_data)
# what_is_json = data.json()
# dell = json.dump(what_is_json)
print("what is dell")
# print(type(dell))
# print(dell)
# print(chad['value'])
print("chad")
print(type(chad))
# charles = chad['value']
# print(charles)
# mylist = [0]['value']
# print(mylist)
print(chad)
# print(chad['value'])
print ('\n')
print("This is get method")
# test = dict.get('virtualDiskId', default = None)
print(type(chad))
print(chad)
print('\n')
print("hope this is a dict")
dictOfWords = dict.fromkeys(response , 2)
print(type(dictOfWords))
print(dictOfWords)
dictionary = dictOfWords.get('virtualDiskId')
print("tony")
print(dictionary)
# with open('data.json', 'w') as json_file:
#   json.dumps(chad)
# print("")
# print(chad.index('value'))
# value = (chad["name"])
# file = open("data.json")
# data = json.loads(file)
jd = json.dumps(chad, indent = 4)
d = json.loads(jd)
print(d)
print(type(d))
# print(d['value'])
print("make a dict")
python_dict = json.loads(jd)
print(type(python_dict))
print(python_dict)
# dict = eval(chad)
# print(type(dict))
# print(dict)
# with open('data.txt' as jd):
#     data = json.load(jd)
#     for i in data['value']:
#     print(['value'])
print("cool")
cool = json.dumps(chad, indent  = 4)
print(type(cool))
print(cool)
print("this is jd")
print(type(jd))
print(jd)

print(type(data))
# print(data['value'])
print(type(chad))
print(chad)
print("test")
json_data = json.loads(jd)
print(type(json_data))

print(json_data)
print("This would be cool if it works")
# value = (cool)
disk_id = cool.find('value')
print(disk_id)
print(chad)
mylist = ['value']
mylist = list(chad[0])
mylist2 = list(chad[1])
# mydict = dict(chad)
# mylist3 = list(chad[9])
# mydict = (chad.get("value"))
print("george")
# for i in json_data["id"]:
#     print({i["virtualDiskId"]})
print("vicky")
print(mylist[9])
print("steve")
# print(mydict)
# print(type(mydict))
bob = ('nested_list', json.dumps(chad,indent=4))
print("bob")
# print(chad(id['value']))
# print(type(bob))
# for i in bob:
#     print(i)
# print(bob[4])
# a = (response.text)
# disk_id = (a[229:265])

# client.vms.delete(vm_id)
# client.repository_virtual_disks(repo_value).delete(disk_id)