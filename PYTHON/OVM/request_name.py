import json
import requests
import warnings
from requests.auth import HTTPBasicAuth
from requests.auth import AuthBase
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

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
    "memory":"1024",
    "memoryLimit":"1024",
    "osType":"Oracle Linux 7",
    "osVersion":"Oracle Linux Server release 7.6"
}



#variable
# url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/"
url = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm'
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
s = requests.Session()
s.auth = ('user', 'password')
s.verify = False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
#authorization

headers = {
    'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "7c4fe2a4-d1cc-48af-9d07-bb09de6eccd7,4e7a46ea-58ae-4e23-91fb-eb778068ca8e",
    'Host': "ovmdmgr04:7002",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "JSESSIONID=qUiNxlPHC8Z5j7REXLnEB9G7LQIHeAEf0l_IcF8oo2FHzVnMNjBa!-209135736; _WL_AUTHCOOKIE_JSESSIONID=KVUaS22fIk9-wWP.09az",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, verify=False)
resp = requests.post(url, headers, PAYLOAD, verify=False )
print(response.text)
vm_id = client.vms.get_id_by_name('test001')
# #variables
# rest_api='https://ovmdmgr04:7002/ovm/core/wsapi/rest'
# url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/"
# # defining a data dict for the parameters to be sent to the API
# data = {
#   'name': 'myServer',
#   'description': 'my server',
#   'vmDomainType': 'vmDomainType',
#   'repositoryId': 'ndc2-pool07-repo',
#   'serverPoolId'; 'my_server_pool_id',
# }

# # sending get request and saving the response as response object
# r = requests.get(url = rest_api, params = data)

# # extracting data in json format 
# data = r.json() 
# #printing the output
# #extract_data = data['results']

# print(data)
# output = requests.get('https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm', verify=False)

# print(output)
