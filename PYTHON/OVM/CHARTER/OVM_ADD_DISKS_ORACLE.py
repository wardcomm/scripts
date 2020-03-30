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
# constants = DISK_TYPE_VIRTUAL_DISK = "VIRTUAL_DISK"
# print(repo_value)
pp = pprint.PrettyPrinter(indent=4)
# server_name = sys.argv[1]
drive_size = sys.argv[1]
s = requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
# math = "1024"
# math2 = * 1024
#1024 * 1024 * 1024 mib equals one gib
# Create a virtual disk
# disk_calc = int(1024 * 1024 * 1024) * drive_size
# print(disk_calc)
# total = (drive_size * disk_calc)
# print(total)

# print(drive_size)
math = 1024 * 1024 * 1024 / 4096
# print(math)
answer = int(drive_size) * 4096 * int(math)
# print(answer)

# one_gig = int(1073741824)
# total = int(one_gig) + int(drive_size)
# print(total)
disk_data = {
    'diskType': "VIRTUAL_DISK",
    'size': answer,
    'shareable': True,
    'name': 'dummy.img',
}
print(disk_data)
client.repository_virtual_disks(repo_value).create(disk_data, sparse='true')



# post url data