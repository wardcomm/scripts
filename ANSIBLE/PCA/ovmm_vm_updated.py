#!/usr/bin/python
#
# Ansible is an open source software project and is licensed under the GNU General Public License version 3, 
# as detailed in the Ansible source code: https://github.com/ansible/ansible/blob/devel/COPYING


DOCUMENTATION = '''
---

module: ovmm_vm_updated
short_description: This is the Infrastructure Lifecycle module for Oracle VM and Oracle Private Cloud Appliance. It manages creation, deletion, start and stop of Virtual Machines inside Oracle-VM
description:
  - Module to manage Virtual Machine definitions inside Oracle-VM
notes:
    - This module works with OVM 3.3 and 3.4 and Oracle PCA 2.3.1 +
    - Author: Sonit Tayal
requirements:
    - requests package
    - json package
options:
    state:
        description:
            - The desired state of the Virtual Machine
                - Present - Create a new VM if it doesn't exist. The VM of desired config, along with Virtual NICs attached to specified networks and virtual disks will be created using play.yml playbook
                - Absent - Delete an existing VM with its Virtual Disks using deletevm.yml playbook
                - start - Start a VM if it is stopped on OVM using startvm.yml playbook
                - stop - Stop a running VM on OVM using stopvm.yml playbook
		- clone_template - Create a VM from a user specified VM Template using a Clone Customizer
		- clone_assembly - Clone a VM assembly (*.ova) to VMs on PCA
    name:
        description:
            - The virtual-machine name, inside oracle-vm the vm-name is
            - not unique. It uses the vm-id as the unique identifier.
        required: True
    ovm_user:
        description:
            - The OVM admin-user used to connect to the OVM-Manager. It is required for authentication if certificate authentication for Oracle VM is not enabled.
        required: True 
    ovm_pass:
        description:
            - The password of the OVM admin-user. Required if certificate authentication is not enabled
        required: True
    ovm_hostname:
        description:
            - The hostname/IP address for Oracle-VM. For Oracle PCA, this is the VIP of the Management Nodes.
        required: True
    ovm_port:
        description:
	    - The port number that OVM listens on
        required: True
    server_pool:
        description:
            - The Oracle-VM server-pool where to create/find the
            - Virtual Machine. It is required when a new VM needs to be created.
        required: False
    repository:
        description:
            - The Oracle-VM storage repository where to store the Oracle-VM
            - definition. Needs to be specified when a new VM needs to be created.
        required: False
    networks:
        description:
	    - The networks for the Virtual NICs to be attached to a new VM. The networks are supplied as a list. If a VM needs multiple VNICs on the same network, that network name should be entered multiple times.
	required: False
    disks:
        description:
	    - The specs of virtual disks to be attached to the new VM. These have to be specified as a list of lists [['diskname1', disk1_size in bytes, 'Repository_name'], [['diskname2', disk2_size in bytes, 'Repository_name'],...]
        required: False
    memory:
        description:
            - The amount of memory in MB for the VM
    vcpu_cores:
        description:
            - The number of physical CPU cores to be assigned to the VM
    max_vcpu_cores:
        description:
            - The max number of processors that can be assigned to VM. This number depends on domain object_type
                - XEN_PVM- 256
                - XEN_HVM- 128
    operating_system:
        description:
            - The OS of the virtual machine
    vm_domain_type:
        description:
            - The domain type specifies the Virtual-Machine
            - virtualization mode.
        required: False
        default: "XEN_HVM"
        choices: [ XEN_HVM, XEN_HVM_PV_DRIVERS, XEN_PVM, LDOMS_PVM, UNKNOWN ]
    vmTemplate:
        description:
            - The VM Template (*.tgz) that you want to clone to a VM. This paramter is needed when you use state=clone_template
        required: False
    vmCloneDefinition:
        description:
            - The name of VM Clone Customizer to be used while cloning the specified VM Template. You can use a clone customizer to have the clone deploy to a different server pool or repository, with changed memory, virtual CPU number, network settings, and so on.
        required: False
    assembly:
        description:
            - The name of the VM assembly to be used for cloning a VM. This is used when the state = clone_assembly
    vmrootpassword:
        description:
	    - The password for 'root' user on the newly created VM.
	required: False

'''

EXAMPLES = '''
    - name: Create a Virtual Machine
      ovmm_vm_updated:
        state: present
        name: ST_vm33
        ovm_user: admin
        ovm_pass: Welcome1
        ovm_host: dhcp-10-211-54-59
        ovm_port: 7002
        server_pool: SP1
        repository: MyRepo
        memory: 4096
        vcpu_cores: 4
        boot_order: PXE
        networks: ['VMnet', 'VMnet']
        disks: [['disk1', 1073741824, 'MyRepo'], ['disk2', 1073741824, 'MyRepo']]

'''

RETURN = '''

'''

################################################################
try:
    import json
    import requests
    requests.packages.urllib3.disable_warnings()
    import logging
    try:
        # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    #enable logging for request calls (put, post, delete) to make it easier to debug in case of an error
    logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.DEBUG)
    urllib3_logger.propagate = True

    import time
except ImportError:
    requests_exists=False

 
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
disable_warnings()	
    


def auth(ovm_user, ovm_pass):
    """ Set authentication-credentials.
    Oracle-VM usually generates a self-signed certificate,
    Set Accept and Content-Type headers to application/json to
    tell Oracle-VM we want json, not XML. The Basic Authorization sends Oracle VM username and password with each request for authentication. If certificate based authenitication is set up, user name and password are not needed.
    """
    session = requests.Session()
    session.auth = (ovm_user, ovm_pass)
#    session.cert ='/etc/ansible/OVMSignedCertificateNew.pem'
    session.verify=False #'/etc/ansible/ovmca.pem'  
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json' })
    return session 

#Function to make sure each job gets completed before going to the next step in code execution
def wait_for_job(joburi,restsession):
    while True:
        time.sleep(1)
        r=restsession.get(joburi)
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

def get_VM_from_name(restsession,baseUri, module):
    uri='{base}/Vm/id'.format(base=baseUri)
    r=restsession.get(uri)
    for obj in r.json():
        if 'name' in obj.keys():
            if obj['name']==module.params['name']:
                return obj
        raise Exception('Failed to find object named {name}'.format(name=obj_name))

def get_id_from_name(restsession,baseUri, resource, resource_name):
    uri='{base}/{res}/id'.format(base=baseUri, res=resource)
    r=restsession.get(uri)
    for obj in r.json():
        if 'name' in obj.keys(): 
            if obj['name']==resource_name:
                return obj
    raise Exception('Failed to find id for {name}'.format(name=resource_name))

def get_VM_Info_by_Id(module, baseUri, VMId, restsession):
    uri='{base}/Vm/{VMId}'.format(base=baseUri, VMId=VMId)
    info=restsession.get(uri)
    infoJson=json.loads(info.text)
    return infoJson


def vmExists(module, restsession, baseUri):
    uri='{base}/Vm/id'.format(base=baseUri)
    vmResult=restsession.get(uri)
    for obj in vmResult.json():
        if 'name' in obj.keys():
            if obj['name']==module.params['name']:
                return True
    return False


def get_VirtDisk_Info_by_DiskMap_ID(restsession, baseUri, module, VMDiskMapID):
    uri='{base}/VmDiskMapping/{VMDiskMapID}/VirtualDisk'.format(base=baseUri, VMDiskMapID=VMDiskMapID)
    virtdiskinfo=restsession.get(uri)
    virtdiskinfoJson=json.loads(virtdiskinfo.text)
    return virtdiskinfoJson


def delVmDiskMap(restsession, baseUri, module, VMDiskMapID):
    id=get_id_from_name(restsession,baseUri,'Vm',module.params['name'])['value']
    vminfo=get_VM_Info_by_Id(module, baseUri, id, restsession)
    uri='{base}/Vm/{VMId}/VmDiskMapping/{VMDiskMapId}'.format(base=baseUri, VMId=id, VMDiskMapId=VMDiskMapID)

    delVmDiskMapResult=restsession.delete(uri)
    delVmDiskMapJson=json.loads(delVmDiskMapResult.text)
    wait=wait_for_job(delVmDiskMapJson['id']['uri'], restsession)


def delVirtualDisk(restsession, baseUri, module, virtualDisk):
    
    uri='{base}/Repository/{repo_id}/VirtualDisk/{VirtualDiskID}'.format(base=baseUri, repo_id=virtualDisk['repositoryId']['value'], VirtualDiskID=virtualDisk['id']['value'])
    delVirtualDiskRes=restsession.delete(uri)
    delVirtualDiskJson=json.loads(delVirtualDiskRes.text)
    wait=wait_for_job(delVirtualDiskJson['id']['uri'], restsession)

def startVM(restsession, module, baseUri):
    vminfo=get_VM_Info_by_Id(module, baseUri, get_id_from_name(restsession,baseUri,'Vm', module.params['name'])['value'], restsession)

    if vminfo["vmRunState"]=='STOPPED':
        uri='{base}/Vm/{id}/start'.format(base=baseUri, id=vminfo['id']['value'])
        startVM=restsession.put(uri)
        jsonstartVM=json.loads(startVM.text)
        wait=wait_for_job(jsonstartVM['id']['uri'], restsession)
	module.exit_json(msg="VM started", changed=True)
    
    else:
	module.exit_json(msg="VM already running", changed=False)
	 

def stopVM(restsession, module, baseUri):
    
    vminfo=get_VM_Info_by_Id(module, baseUri, get_id_from_name(restsession,baseUri,'Vm',module.params['name'])['value'], restsession)

    if vminfo["vmRunState"]=='RUNNING':
        uri='{base}/Vm/{id}/stop'.format(base=baseUri, id=vminfo['id']['value'])
        stopVM=restsession.put(uri)
        jsonstopVM=json.loads(stopVM.text)
        wait=wait_for_job(jsonstopVM['id']['uri'], restsession)
	module.exit_json(msg="VM stopped", changed = True)

    else:
	module.exit_json(msg="VM is already stopped", changed = False)

def createsp(restsession, module, baseUri):
    data = {
            'name': 'MyServerPool',
        }
    uri='{base}/ServerPool'.format(base=baseUri)
    r=restsession.post(uri, data=json.dumps(data))
    job=r.json()
# wait for the job to complete
    sp_id=wait_for_job(job['id']['uri'],restsession)
    module.exit_json(msg="ServerPool created", changed=True)



def configVm(restsession, module, baseUri, newVmId):

# Create a Virtual Disk of the specified config
    disklist=module.params['disks']

    for i in range(len(disklist)):
       repo_id=get_id_from_name(restsession, baseUri, 'Repository', disklist[i][2])['value']
       Data3={
             'name': disklist[i][0],
             'size': disklist[i][1],
#            'shareable': false,
#            'readOnly': false,
#            'locked': false,
             }
       payload={
               'sparse': True
               }
       uri3='{base}/Repository/{repoid}/VirtualDisk'.format(base=baseUri, repoid=repo_id)
       createdisk=restsession.post(uri3, data=json.dumps(Data3), params = payload)
       jsoncreatedisk=createdisk.json()
       diskid=wait_for_job(jsoncreatedisk['id']['uri'], restsession)


# Create a VmDiskMapping to represent association of VirtualDisk to Vm

       uri4='{base}/Vm/{vmid}/VmDiskMapping'.format(base=baseUri, vmid=newVmId['value'])
       Data4={
             'virtualDiskId': diskid,
             'diskTarget': i,
             }
       createVmDiskMap=restsession.post(uri4, data=json.dumps(Data4))
       createVmDiskMapJson=createVmDiskMap.json()
       VmDiskMapId=wait_for_job(createVmDiskMapJson['id']['uri'], restsession)


# Create a VNic on the desired network
    netlist=module.params['networks']
    for net in range(len(netlist)):
       networkid=get_id_from_name(restsession, baseUri, 'Network', netlist[net])
       Data={
         'networkId': networkid,
       }

       uri2 ='{base}/Vm/{vmId}/VirtualNic'.format(base=baseUri, vmId=newVmId['value'])
       addNic=restsession.post(uri2, data=json.dumps(Data))
       jsonaddNic=addNic.json()
       wait=wait_for_job(jsonaddNic['id']['uri'], restsession)


    module.exit_json(msg="VM created with id {vmID}".format(vmID=newVmId['value']), changed=True)


def configVM_afterStartup(restsession, module, baseUri, newVmId):
    uri='{base}/Vm/{vmid}/sendMessage'.format(base=baseUri,vmid=newVmId)

    payload=[
	    {
            "key": "com.oracle.linux.network.hostname",
	    "value": module.params["name"]
	    },
	    {
	    "key": "com.oracle.linux.network.device.0",
	    "value": "eth0"
	    },
	    {
	    "key": "com.oracle.linux.network.onboot.0",
   	    "value": "yes"
	    },
	]

    configvm=restsession.put(uri, data=json.dumps(payload))
    configvmjson=configvm.json()
    wait=wait_for_job(configvmjson['id']['uri'], restsession)
    
    #Sleep for 10 sec for changes to take effect
    time.sleep(10)

    payload=[
            {
            "key": "com.oracle.linux.root-password",
            "value": module.params["vmrootpassword"]
            },
            ]
    result=restsession.put(uri, data=json.dumps(payload))
    resultjson=result.json()
    wait=wait_for_job(resultjson['id']['uri'], restsession)


def createVM(restsession, module, baseUri):
    repo_id=get_id_from_name(restsession,baseUri,'Repository', module.params['repository'])
    sp_id=get_id_from_name(restsession,baseUri,'ServerPool',module.params['server_pool'])
    Data={
        'name': module.params['name'],
        'description': 'A virtual machine created using the REST API',
        'vmDomainType': module.params['vm_domain_type'],
        'repositoryId': repo_id,
        'serverPoolId': sp_id,
        'memory': module.params['memory'],
        'memoryLimit': module.params['max_memory'],
        'cpuCount': module.params['vcpu_cores'],
        'cpuCountLimit': module.params['max_vcpu_cores'],
        'bootOrder': module.params['boot_order'],
    }
    uri='{base}/Vm'.format(base=baseUri)
#    print("Data = %s\n", Data)
#    print("URI=%s\n", uri)
    createVMvar=restsession.post(uri, data=json.dumps(Data))
    job=createVMvar.json()
    # wait for the job to complete
    vm_id=wait_for_job(job['id']['uri'], restsession)

    configVm(restsession, module, baseUri, vm_id)

def createVM_assembly(restsession, module, baseUri):
    repo_id=get_id_from_name(restsession,baseUri,'Repository', module.params['repository'])
    sp_id=get_id_from_name(restsession,baseUri,'ServerPool',module.params['server_pool'])['value']

    assembly_id=get_id_from_name(restsession,baseUri,'Assembly',module.params['assembly'])['value']

    assembly=restsession.get('{base}/Assembly/{id}'.format(base=baseUri,id=assembly_id))
    assemblyjson=assembly.json()
    for i in assemblyjson['assemblyVmIds']:
        uri='{base}/AssemblyVm/{id}/createVm'.format(base=baseUri,id=i['value'])
#        Data5={
#	    'serverPoolId': sp_id,
 #           'createTemplate': False,
#	    }
        r=restsession.put(uri)
        job=r.json()
        # wait for the job to complete
        vmid=wait_for_job(job['id']['uri'], restsession)
        print("vmid =%s\n",vmid)
        
    modifyVm(restsession, module, baseUri, vmid['value'])
    module.exit_json(msg="VM created with id {vmID}".format(vmID=vmid), changed=True)

def modifyVm(restsession, module, baseUri, newVmId):
    
    jsonVmInfo=get_VM_Info_by_Id(module, baseUri, newVmId, restsession)
    uri='{base}/Vm/{vmid}'.format(base=baseUri,vmid=newVmId)

    Data={
        'name': module.params['name'],
        'description': module.params['description'],
        'vmDomainType': module.params['vm_domain_type'],
        'memory': module.params['memory'],
        'memoryLimit': module.params['max_memory'],
        'cpuCount': module.params['vcpu_cores'],
        'cpuCountLimit': module.params['max_vcpu_cores'],
        'bootOrder': module.params['boot_order'],
    }
    
    for key,value in Data.items():
        jsonVmInfo[key] = value

    modifyvm=restsession.put(uri, data=json.dumps(jsonVmInfo))
    modifyvmjson=modifyvm.json()
    # wait for the job to complete
    wait_for_job(modifyvmjson['id']['uri'], restsession)
    
#    configVm(restsession, module, baseUri, newVmId)
#    module.exit_json(msg="VM created with id {vmID}".format(vmID=newVmId), changed=True)

def cloneVM_template(restsession, module, baseUri):
    
    vm_id=get_id_from_name(restsession,baseUri,'Vm',module.params['vmTemplate'])['value']
    uri='{base}/Vm/{vmid}/clone'.format(base=baseUri, vmid=vm_id)
    
    sp_id=get_id_from_name(restsession,baseUri,'ServerPool',module.params['server_pool'])['value']
    clonedef_id=get_id_from_name(restsession,baseUri,'VmCloneDefinition',module.params['vmCloneDefinition'])['value']
    Data6={
         'vmCloneDefinitionId': clonedef_id,
         'serverPoolId': sp_id,
         'createTemplate': False,
         }

    clonetemplate=restsession.put(uri, params=Data6)
    clonetemplatejson=clonetemplate.json()
    newvmid=wait_for_job(clonetemplatejson['id']['uri'], restsession)

    modifyVm(restsession, module, baseUri, newvmid['value'])

    uri2='{base}/Vm/{id}/start'.format(base=baseUri, id=newvmid['value'])
    startVM=restsession.put(uri2)
    jsonstartVM=startVM.json()
    wait=wait_for_job(jsonstartVM['id']['uri'], restsession)

    configVM_afterStartup(restsession, module, baseUri, newvmid['value'])
 
    module.exit_json(msg="VM created and started with id {vmID}".format(vmID=newvmid['value']), changed=True)

def deleteVM(restsession, module, baseUri):
    vmid=get_id_from_name(restsession, baseUri, 'Vm', module.params['name'])['value']
    vminfo=get_VM_Info_by_Id(module, baseUri, get_id_from_name(restsession, baseUri, 'Vm', module.params['name'])['value'], restsession)
    if vminfo["vmRunState"]=='RUNNING':
        vmuri='{base}/Vm/{id}/stop'.format(base=baseUri, id=vmid)
        vmstop=restsession.put(vmuri)
        jsonvmstop=json.loads(vmstop.text)
        wait=wait_for_job(jsonvmstop['id']['uri'], restsession)
    else:
	pass    
 
#Remove the disk mapping to Vm and then remove the disk
    for obj in vminfo['vmDiskMappingIds']:
        vmDiskinfo=get_VirtDisk_Info_by_DiskMap_ID(restsession,baseUri, module, obj['value'])
        delVmDiskMap(restsession, baseUri, module, obj['value'])
        delVirtualDisk(restsession, baseUri, module, vmDiskinfo)

    uri='{base}/Vm/{VMId}'.format(base=baseUri, VMId=vmid)
    delVMRes=restsession.delete(uri)
    delVMResJson=json.loads(delVMRes.text)
    wait=wait_for_job(delVMResJson['id']['uri'], restsession)

    module.exit_json(msg="VM Deleted", changed=True)

#    else:
#       stopVM(restsession, module, baseUri)
	
#        module.exit_json(msg="VM needs to be stopped before it can be deleted", changed=False)



def main():
    changed = False
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=['present', 'absent', 'start', 'stop', 'clone_assembly', 'clone_template']),
            name=dict(required=True),
            description=dict(required=False),
            ovm_user=dict(required=False),
            ovm_pass=dict(required=False),
            ovm_host=dict(required=True),
            ovm_port=dict(required=True),
            server_pool=dict(required=False),
            repository=dict(required=False),
            vm_domain_type=dict(default='XEN_HVM', choices=[
                    "XEN_HVM",
                    "XEN_HVM_PV_DRIVERS",
                    "XEN_PVM",
                    "LDOMS_PVM",
                    "UNKNOWN"]),
            memory=dict(required=False, default=4096, type='int'),
            max_memory=dict(required=False, default=None, type='int'),
            vcpu_cores=dict(required=False, default=2, type='int'),
            max_vcpu_cores=dict(required=False, default=None, type='int'),
            operating_system=dict(required=False),
            networks=dict(type='list', required=False),
            disks=dict(required=False, type='list'),
            boot_order=dict(required=False, type='list'),
            assembly=dict(required=False),
            vmTemplate=dict(required=False),
            vmCloneDefinition=dict(required=False),
	    vmrootpassword=dict(required=False),
        )
    )

    restsession=auth(module.params['ovm_user'], module.params['ovm_pass'])
    baseUri='https://{hostName}:{port}/ovm/core/wsapi/rest'.format(hostName=module.params['ovm_host'],port=module.params['ovm_port'])

    if module.params['state']=="present":
        if not vmExists(module, restsession, baseUri):
            createVM(restsession, module, baseUri)
#            module.exit_json(msg='CreateVM successful', changed=True)

        else:
            id=get_id_from_name(restsession,baseUri,'Vm',module.params['name'])['value']
            module.exit_json(msg='VM exists and has id {vmID}'.format(vmID=id), changed=False)
     
    elif module.params['state']=="clone_assembly":
        createVM_assembly(restsession, module, baseUri)
#            module.exit_json(msg='CreateVM successful', changed=True)


    elif module.params['state']=="clone_template":
        cloneVM_template(restsession, module, baseUri)

    elif module.params['state']=="start":
        if not vmExists(module, restsession, baseUri):
            module.exit_json(msg="VM doesn't exist", changed=False)

        else:
            startVM(restsession, module, baseUri)
          
    elif module.params['state']=="stop":
        if not vmExists(module, restsession, baseUri):
            module.exit_json(msg="VM doesn't exist", changed=False)

        else:
            stopVM(restsession, module, baseUri)
            
    elif module.params['state']=="absent":
        if vmExists(module, restsession, baseUri):
            deleteVM(restsession, module, baseUri)

        else:
            module.exit_json(msg="VM doesn't exist", changed=False)



from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()

