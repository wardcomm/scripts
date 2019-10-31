#!/usr/bin/python3
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user = 'p2906297'
password = 'THem5dax'

# client = ovmclient.Client(
#     'https://ovmdmgr04:7002/ovm/core/wsapi/rest', user, password)
s=requests.Session()
s.auth=(user, password)
s.verify=False #disables SSL certificate verification
 
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
 
baseUri='https://ovmdmgr04:7002/ovm/core/wsapi/rest'
web='https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm'

headers = {
    'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "3b586e29-5242-4410-b462-802abd857197,255a3209-6637-4c18-a0c1-00e127a825a7",
    'Host': "10.136.170.208:7002",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "JSESSIONID=64u3QJc4eaH0HnOWAh8hEFrdT9UcbuIgzcRCDKsBL9-F3WEOGgP1!-1473086762; _WL_AUTHCOOKIE_JSESSIONID=7uRadtrrj2ypuubyud3s",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

# print("\nPool List:")
# print("##############")
# r=s.get(baseUri+'/ServerPool')
# for i in r.json():
#   # do something with the content
#   print( '{:20} {:20}'.format(i['serverRunState'],i['name'])

print("\nServer List:")
print("##############")
r=s.get(baseUri+'/Server')
for i in r.json():
  # do something with the content
  print( '{:20} {:20}'.format(i['serverRunState'],i['name']))
 
print("\nVM List:")
print("########")
r=s.get(baseUri+'/Vm')
for i in r.json():
  # do something with the content
  print ('{:20} {:20}'.format(i['vmRunState'],i['name']))
  #print '{name} '.format(name=i['name'])

PAYLOAD = {
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
    "memory":"512",
    "memoryLimit":"512",
    "osType":"Oracle Linux 7",
    "osVersion":"Oracle Linux Server release 7.6"
}
# print("Post requests:")
# print("##############")
print(PAYLOAD)
url = "https://10.136.170.208:7002/ovm/core/wsapi/rest/Vm"
response = requests.post(url, data={name : ovm_test_api}, json={}, headers=headers)

print(response.status_code)
response = requests.post(web, data=json.dumps(PAYLOAD), headers=headers, auth=(user, password), verify=False)
# print(response)

if response.status_code == 200:
    print('Success!')
elif response.status_code == 404:
    print('Not Found.')
    print('''The origin server did not find a current representation for the target resource or is not willing to disclose that one exists.
    ''')
elif response.status_code == 415:
    print ('415 Unsupported Media Type')
    print ('''
    The origin server is refusing to service the request because the payload is in a format not supported by this method on the target resource.
    ''')   
else:
    response.status_code == 400
    print('Dude you like have 400 Bad Request')
    print('''
    The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).
    ''')
req = requests.get(web)
req = requests.encoding 
print(req)
my_object = {
    'name' : 'BIG_server'
}
# x = requests.get(web, data=PAYLOAD, headers=headers, auth = (user, password), verify=False)
# print(x.text)

# print("Post requests:")
# print("##############")
x = requests.post(web, data=PAYLOAD, headers=headers, auth = (user, password), verify=False)
print(x.status_code)