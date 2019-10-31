# importing the requests and json library
import json
import requests
import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

#variable
#url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/"
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
s = requests.Session()
s.auth = ('user', 'password')
s.verify = False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})






url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/"

# payload = {\r\n    \"name\":\"ovm_test_api\",\r\n    \"description\":\"A Test server for ORacle  api\",\r\n    \"vmDomainType\":\"Xen HVM PV Drivers\",\r\n    \"repositoryId\":\"ndc2-pool07-repo\",\r\n    \"serverPoolId\":\"ndc-pool07-x86\",\r\n    \"cpuCount\":\"1\",\r\n    \"cpuCountLimit\":\"1\",\r\n    \"cpuPriority\":\"50\",\r\n    \"cpuUtilizationCap\":\"100\",\r\n    \"hugePagesEnabled\":\"False\",\r\n    \"memory\":\"1024\",\r\n    \"memoryLimit\":\"1024\",\r\n    \"osType\":\"Oracle Linux 7\",\r\n    \"osVersion\":\"Oracle Linux Server release 7.6\"\r\n }

payload = {
    "name":"WONDER_WOMAN",
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



headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Cache-Control': "no-cache",
    'Postman-Token': "431c60f2-8109-462a-9c6d-f062c37cc795,ce167c43-2f95-4601-b2df-8c6616bfe381",
    'Host': "ovmdmgr04:7002",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "477",
    'Cookie': "JSESSIONID=TBWXvH2bw17BlC7xx08ECcibPZi8g7d5n_2ECy-XPp-sIWYrQART!-1473086762; _WL_AUTHCOOKIE_JSESSIONID=JMkwEFrfUDwkltPzHv9O",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.post(url, data=payload, headers=headers, json=True, verify=False)

data = response.json()
print(data)
print(response.text)