# import the requests library to handle HTTP requests and session maintenance
import requests
# import the json library for JSON translation (not required for this example)
import json

# instantiate a session object and populate it with authentication credentials
s=requests.Session()
s.auth=('user','password')
s.verify=False #disables SSL certificate verification
# configure the session to always use JSON
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

# set up a baseUri object to contain the URI to the Utilities API
baseUri='https://127.0.0.1:7002/ovm/core/wsapi/rest/Utilities'

# construct the URI according to the requirements set out in the documentation
uri='{base}/BusinessManagement/availableEthernetPorts'.format(
    base=baseUri)

# configure the query parameters
params={
    "serverId": "00:e0:81:4d:40:f5:00:e0:81:4d:40:be:00:e0:81:4d",
    "networkId": "0aac4c00"
}

# submit a get request to the uri and store the response
r=s.get(uri,params=params)
# use the requests library's native json parser to obtain a usable python object
availPorts=r.json()