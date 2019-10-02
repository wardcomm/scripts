#!/usr/bin/env python3
import json

from time import sleep

user=p2906297
password=THem5dax
baseUri='https://ovmdmgr04:7002/ovm/core/wsapi/rest'
repo_id=get_id_from_name(s,baseUri,'Repository','MyRepository')
sp_id=get_id_from_name(s,baseUri,'ServerPool','MyServerPool')
s = requests.Session()
s.auth = ('user', 'password')
s.verify = False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
# s.cert='/path/to/mycertificate.pem

data={
        'name': 'MyVirtualMachine',
        'description': 'A virtual machine created using the REST API',
        'vmDomainType': 'XEN_PVM',
        'repositoryId': repo_id,
        'serverPoolId': sp_id,
    }
uri='{base}/Vm'.format(base=baseUri)
r=s.post(uri,data=json.dumps(data))
job=r.json()
# wait for the job to complete
vm_id=wait_for_job(job['id']['uri'],s)