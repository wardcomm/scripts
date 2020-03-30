import requests
import sys
import urllib3
import ovmclient
import json
import pprint
import time
from pprint import pprint

#variable
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
# server_name = sys.argv[1]
# drive_size = sys.argv[2]
repo_id = (repo_name['value'])

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.trust_env = False
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

url = baseUri+'/Server/' + 'id'
get_data = s.get(url)
get_server_info = get_data.json()
# pprint(get_server_info[0])
data = (get_server_info)
new_data = json.dumps(get_server_info)
python_dict = json.loads(new_data)
pprint(new_data)
pprint(type(new_data))
pprint(type(python_dict))

r=s.get(baseUri+'/Server')
for i in r.json():
 # do something with the content
      print('{name} is {state}'.format(name=i['name'],state=i['serverRunState']))
print(type(r))
# d = dict(get_server_info
print(type(get_server_info))
print(new_data[0:])
print("This is the beginning")
# request = s.get(baseUri + '/Server')
# for i in request.json():
#       print('{name} is {get_uri}'.format(name=i['name'], get_uri=i['uri']))

# test = new_data[uri]
# print(get.name(new_data))
# pprint(data)
# pprint(type(get_server_info))

# more_data = dict(get_server_info)
# for index in get_server_info.json():
#     if 'name' in index.keys():
#      if index['name'] == name:
#          quit()

# for index in range(len(get_server_info)):
    # for element in range(int(index)):
    #     print(element)
#    print(get_server_info[index])
#    print(type(get_server_info))
#    print(get_server_info)