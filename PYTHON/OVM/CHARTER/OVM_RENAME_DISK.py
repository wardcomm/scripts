import requests
import sys
import urllib3
import ovmclient
import json

#variable
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

server_name = sys.argv[1]
# processors = sys.argv[2]
# processors_limit = sys.argv[3]
# processor_cap = sys.argv [4]

vm_id = client.vms.get_id_by_name(server_name)
print(vm_id)
vm_value = str(vm_id['value'])
print(vm_value)
url = baseUri+'/Vm/' + vm_value + '/VmDiskMapping'
# new_url = baseUri+"VirtualDisk"+
print(url)
# data = s.get(url)
# print(data.json())
data = s.get(url)
print(data.content)
print(data)
# print(data)
json_data = data.json()
# print(json_data)
x = json_data[0]
# x = json.loads(json_data)
print("This is good starting point x is below")
print(x)
# print(x.content)
print('\n')
print("place holder")
print(json_data)
disk_id = (x['virtualDiskId']['value'])
print(disk_id)
disk_name = (x['virtualDiskId']['name'])
print(disk_name)
system_name = (x['vmId']['name'])
print("Star Wars")
diskurl =baseUri+"/VirtualDisk/" + disk_id
rename = "disk_" + server_name + "_"
some_data = x
some_data['virtualDiskId']["name"] = rename
print(some_data)
put = s.put(url,data=json.dumps(some_data))
print(put)
print("Some Kind of DATA")
print(put.content)
# print(b)
# print(content)
print("anikin")
print(diskurl)
print("I love JAR JAR BINKS")
rename_get = s.get(diskurl)
rename_data = rename_get.json()
print(rename_get)
print(type(rename_get))
print("ewok")
print()
# print(number)
print('\n')
data = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/VmDiskMapping/0004fb0000130000dc39eae9fb04e143'
get = s.get(data)
some_data = get.json()
# rename_data = some_data
print("before")
print(rename_data)
rename = "disk_" + server_name + "_"
# rename_data['virtualDiskId']["name"] = rename
some_data['virtualDiskId']["name"] = rename
chad = s.put(url,data=json.dumps(some_data, indent = 4 ))
print(type(chad))
print("LINE BREAK1")
print('\n')
print(chad)
print('\n')
print("LINE BREAK2")
print(some_data)
print('\n')
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print(chad)
print("This is The DEATH STAR")
print(some_data)
print("HAN SOLO")
print("I am your father, nooooooooo")
print(rename_data)
rename = "disk_" + server_name + "_"
rename_data["name"] = rename

darth = s.put(url,data=json.dumps(rename_data, indent = 4 ))
print("WHERE IS NABOO")
print(darth)
print(darth.content)
print("Darth Maul")
print(darth)
# rec=0 
# def autoIncrement(value): 
#  global rec 
#  pStart = 1  
#  pInterval = 1 
#  if (rec == 0):  
#   rec = pStart  
#  else:  
#   rec += pInterval  
#  return rec
# autoIncrement(1)
# print(autoIncrement)
# n=[0]
# num = list(n + 1)

# number = (0 + 1)
# print(number)
rename_data = rename_get.json()
print(type(rename_data))
print("Y")
print(rename_get)
print("8*******************************************************8")
print(rename_data)
rename = "disk_" + server_name + "_"
print(rename)
# rename_data = (rename_data['id']['name'])
print("scooby doo")
print(type(rename_data))
rename_data["name"] = rename
print(type(rename_data))
# rename_data["virtualDiskId"]["name"] = rename
rename_data["name"] = rename
penguin_put = s.put(url,data=json.dumps(rename_data, indent = 4 ))
print("The penguin has the power")
print(type(penguin_put))
print(penguin_put)
# print(chad)
print(disk_name)
print("USMC")
# https://ovmdmgr04:7002/ovm/core/wsapi/rest/VirtualDisk/0004fb0000120000b7f435cb18f66a1a.img

print(system_name)
print("A")
print(disk_id)
print("B")
print(x)
print("C")
real_data = client.vms.get_by_id(vm_id)
print(real_data)
print("this")
stupid = json.dumps(real_data, indent  = 4)
print(stupid)

# rename_data = (x)
# rename_data = x[""]
print("D")
rename = "disk_" + server_name+"_"
print(rename)
# rename_data["name"] = rename #  one is what you ar changing second is the value
# rename_data["name"] = rename
# rename_data = x
# data = s.get(url)
# json_data = data.json()
# x = json_data
rename_data = x['virtualDiskId']["name"] = rename
# rename_data["name"] = rename
print("THIS IS WHAT YOU NEED TO LOOK AT")
print(rename_data)
# rename_data["name"] = rename
rename_data = ({'name': rename})
# rename_put = s.put(url,data=json.dumps(rename_data))
rename_put = s.put(url,data=json.dumps(rename_data))
print(rename_put.status_code)
print("what is this")
print(type(rename_put))

cool = json.dumps(x, indent  = 4)
print("cool data")
print(cool)
print(type(cool))
# real_data["cpuCount"] = processors
# real_data["cpuCountLimit"] = processors_limit
# print(cool)
# real_data["pinnedCpus"] = processor_cap
# data_put = s.put(url,data=json.dumps(real_data))# the line that does the magic of  modifying
