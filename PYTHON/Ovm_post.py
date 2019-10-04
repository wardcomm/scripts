#!/usr/bin/env python

# importing the requests and json library
import json
import requests
import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

#variable
PYTHONHTTPSVERIFY = 0
url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/"
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
s = requests.Session()
s.auth = ('user', 'password')
s.verify = False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})


#authorization
data = {
  'name': 'myServer',
  'description': 'my server',
  'vmDomainType': 'Xen HVM PV Drivers',
  'repositoryId': 'ndc2-pool07-repo',
  'serverPoolId': 'ndc-pool07-x86',
}
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
#r = requests.post(url = url, data = data)
#requests.get('https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/', verify=False)
#response = requests.request("GET", url, headers=headers, verify=False)
#response = requests.request("POST", url, headers=headers, verify=False)
response = requests.post( url, headers=headers, data = {'key' : 'value'}, verify=False)
#print(r.text)
#print(response.text)
#requests.get('baseUri', verify=False)
# #variables
# rest_api='https://ovmdmgr04:7002/ovm/core/wsapi/rest'
# url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Server/id/"
# # defining a data dict for the parameters to be sent to the API


# # sending get request and saving the response as response object
# r = requests.get(url = rest_api, params = data)

# # extracting data in json format 
# data = r.json() 
# #printing the output
# #extract_data = data['results']

# print(data)