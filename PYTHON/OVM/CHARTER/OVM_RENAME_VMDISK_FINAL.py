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
server_name = sys.argv[1]
s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

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

