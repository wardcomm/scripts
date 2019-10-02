#!/usr/bin/env python
import requests,json
from time import sleep

user = p2906297
password = THem5dax
baseUri='https://ovmdmgr04:7002/ovm/core/wsapi/rest'
s = requests.Session()
s.auth = ('user', 'password')
s.verify = False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
# s.cert='/path/to/mycertificate.pem

def get_id_from_name(object_type, object_name):
  response = s.get(baseUri+'/'+object_type+'/id')
  for e in response.json():
    if e['name'] == object_name:
      return e
  return None

repo_id = get_id_from_name(s,baseUri,'Repository','MyRepository')
sp_id = get_id_from_name(s,baseUri,'ServerPool','MyServerPool')

data = {
  'name': 'myServer',
  'description': 'my server',
  'repositoryId': get_id_from_name('Repository','repo1'),
  'serverPoolId': get_id_from_name('ServerPool','pool1'),
  'vmDomainType': 'XEN_HVM',
}
print json.dumps(data)
r = s.post(baseUri + '/Vm',data=json.dumps(data))
print r.json()