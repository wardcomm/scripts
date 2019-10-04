#!/usr/bin/env python

# importing the requests and json library
import json
import requests
import warnings
from urllib3.exceptions import  InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)

url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm"

querystring = {"name":"ovm_test_api_100","description":"A%20Test%20server%20for%20ORacle%20%20api","vmDomainType":"Xen%20HVM%20PV%20Drivers","repositoryId":"ndc2-pool07-repo","serverPoolId":"ndc-pool07-x86"}

payload = ""
headers = {
    'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "2dbbbe87-a4da-4278-80f1-a42d7a29d8d6,c969aaeb-d86a-4624-ba15-92bc8b1ec848",
    'Host': "ovmdmgr04:7002",
    'Accept-Encoding': "gzip, deflate",
    'Cookie': "JSESSIONID=swWSnT_hHSlNPPDXzMUt6pwGT4DGiz0hsV0Ssbfc2jARLop2dg83!-209135736; _WL_AUTHCOOKIE_JSESSIONID=SbweymLQ3L-ltK-Ss9Dw",
    'Content-Length': "0",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)