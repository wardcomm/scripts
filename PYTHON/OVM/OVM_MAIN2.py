import requests
import json
from ovm_lib import *
#import logging

s=requests.Session()
s.auth=('admin','mypassword')
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

ovmmServer="192.168.1.223:7002"
print "Running against OVM Manager Server: " + ovmmServer
baseUri='https://'+ovmmServer+'/ovm/core/wsapi/rest'

#logging.basicConfig(level=logging.DEBUG)

## Create VM still failing
## GENERAL_JSON_PARSING_ERROR', u'message': u'GEN_000031:An error occurred parsing the JSON request'

def createVm(s,baseUri,repository,serverpool,vmName):
  #file:///home/rrosso/OvmSDK_3.4.2.1384/doc/api/webservices_r/resource_VmRs.html#path__Vm.html
  #repo_id=get_id_from_name(s,baseUri,'Repository','ovs1')
  #sp_id=get_id_from_name(s,baseUri,'ServerPool','ovs-home')
  repo_id=get_id_from_name(s,baseUri,'Repository',repository)
  sp_id=get_id_from_name(s,baseUri,'ServerPool',serverpool)
  #print 'repo_id {:20} ServerPool Id {:55}'.format(repo_id,sp_id)
  #OVM> create Vm name=MyVM repository=MyRepository domainType=XEN_HVM \ 
  #server=MyServer startPolicy=USE_POOL_POLICY on ServerPool name=MyServerPool

  data={ "name": vmName,
         "description": "A virtual machine created using the REST API",
         "vmDomainType": "XEN_PVM",
	 "repositoryId": repo_id,
         "serverPoolId": sp_id }

#  data={'serverPoolId':'0004fb00000200006aa35973e4d0e5af','repositoryId':'0004fb00000300000c6c2c52c5708b65'}
  print data
  uri='{base}/Vm'.format(base=baseUri)
  print uri
  #print json.dumps(data)
  r=s.post(uri,data=json.dumps(data))
  job=r.json()
  print job
  # wait for the job to complete
  vm_id=wait_for_job(job['id']['uri'],s)

## CloneVM failing
## The value for the argument "serverPoolId" was found to be null
def cloneVm(s,baseUri,templateVm,vmName):
  repo_id=get_id_from_name(s,baseUri,'Repository','ovs1')
  sp_id=get_id_from_name(s,baseUri,'ServerPool','ovs-home')
  template_id=get_id_from_name(s,baseUri,'Vm',templateVm)
  
  print 'clone {} into repo_id {:20} ServerPool Id {:55}'.format(template_id,repo_id,sp_id)  
  
  data={ "serverPoolId": sp_id,
  	 "repositoryId": repo_id,
  	 "createTemplate": False
        }

  uri='{base}/Vm/{vmId}/clone'.format(base=baseUri,vmId=template_id)
  r=s.put(uri,data=json.dumps(data))
  job=r.json()
  print job
  # wait for the job to complete
  vm_id=wait_for_job(job['id']['uri'],s)
  print "new vm id:" + vm_id

  ## change vm name here?

if __name__ == "__main__":
  print
  print

  #check_manager_state(baseUri,s)

  #createVm(s,baseUri,'VM3')
  createVm(s,baseUri,'ovs2','ovs-home','ovs2-VM3')
  #cloneVm(s,baseUri,'Ubuntu.0','VM4')
  
  serverList(s,baseUri)
  vmList(s,baseUri)

  #updateVmMemory(s,baseUri,'VM2','512')

  #updateVmDiskNames(s,baseUri,'VM2')
  #showVm(s,baseUri,'VM2')

  #cmdVm(s,baseUri,'start','VM2')
  #cmdVm(s,baseUri,'stop','VM2')