import requests
import sys
import urllib3
import ovmclient
import json
import pprint

#variable
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)
repo_name = client.repositories.get_id_by_name('pool07-virt1-repo')
repo_value = (repo_name['value'])
pp = pprint.PrettyPrinter(indent=4)

s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

server_name = sys.argv[1]

test_url = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/VirtualDisk/0004fb0000120000b7f435cb18f66a1a.img'
get_name = s.get(test_url)
chad = get_name.json()
dictionary = json.dumps(chad)
d = json.loads(dictionary)
next = str(int('0') + 1)
rename = "disk_" + server_name + "_" + next

d['name'] = rename
data_put = s.put(test_url, data=json.dumps(d),stream=True)