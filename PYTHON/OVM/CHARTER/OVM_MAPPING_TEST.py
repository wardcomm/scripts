#!/usr/bin/python
# This Python Script is written by Kiran Rajendra

import json
import requests
from requests.auth import HTTPBasicAuth
import time
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass

PASSWORD = '<password>' # Please specify the password of OVM manager
#variable
user = 'p2906297'
password = 'THem5dax'
ovm_server = 'ovmdmgr04'
class OVMManager():
    def __init__(self, name):
        self.name = name
        self.baseuri = "https://" + ovm_server + ":7002/ovm/core/wsapi/rest"
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.session.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
        self.session.auth = (user, password)

    def getManager(self):
        response = requests.Response()
        response = self.session.get(self.baseuri + "/Manager", auth=HTTPBasicAuth(user,password))
        if response.status_code == 200:
            print("Successfully accessed Oracle VM Manager") + print(ovm_server)
            return response.json()
        else:
            return {"result": "an error occured"}

    def attach(self):
        VMNAME = raw_input("Enter guest VM name:")
        ISO = raw_input("Enter ISO/Disk name:")
        vm_id = self.get_id_from_name('Vm', VMNAME)
        iso_id = self.get_id_from_name('VirtualDisk',ISO)
        slot= raw_input("Enter the slot number:")
        uri = '{base}/Vm/{vmid}/VmDiskMapping'.format(base=self.baseuri, vmid=vm_id['value'])
        Data4 = {
            'virtualDiskId': iso_id,
            'diskTarget': slot, # here specify the slot number
        }
        createVmDiskMap = self.session.post(uri, data=json.dumps(Data4))
        createVmDiskMapJson = createVmDiskMap.json()
        VmDiskMapId = self.wait_for_job(createVmDiskMapJson['id']['uri'])
        print ("ISO/Disk attached")


    def get_id_from_name(self, resourceType, name):
        response = self.session.get(self.baseuri + "/" + resourceType + "/id" )
        for obj in response.json():
           if 'name' in obj.keys():
            if obj['name'] == name:
                return obj
        raise Exception('Failed to find id for {name}'.format(name=name))

    def wait_for_job(self, joburi):
        while True:
            time.sleep(1)
            r=self.session.get(joburi)
            job=r.json()
            if job['summaryDone']:
                print('{name}: {runState}'.format(name=job['name'], runState=job['jobRunState']))
                if job['jobRunState'].upper() == 'FAILURE':
                    raise Exception('Job failed: {error}'.format(error=job['error']))
                elif job['jobRunState'].upper() == 'SUCCESS':
                    if 'resultId' in job:
                        return job['resultId']
                    break
                else:
                    break

if __name__ == "__main__":
    OVM = OVMManager('ovmdmgr04') # Here <IP ADDRESS> is OVM manager IP address
    result = OVM.getManager()
    print(result)
    OVM.attach()
