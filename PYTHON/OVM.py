import json
from time import sleep
 
def get_id_from_name(s,baseUri,obj,name):
  #sp_id=get_id_from_name(s,baseUri,'ServerPool','ovs-home')
  r=s.get(baseUri+'/'+obj)
  for i in r.json():
    if i['name'] == name:
      id = i['id']['value']
  return id
 
def wait_for_job(joburi,s):
        while True:
            time.sleep(1)
            r=s.get(joburi)
            job=r.json()
            if job['summaryDone']:
                print '{name}: {runState}'.format(name=job['name'], runState=job['jobRunState'])
                if job['jobRunState'].upper() == 'FAILURE':
                    raise Exception('Job failed: {error}'.format(error=job['error']))
                elif job['jobRunState'].upper() == 'SUCCESS':
                    if 'resultId' in job:
                        return job['resultId']
                    break
                else:
                    break    
 
def check_manager_state(baseUri,s):
  #https://hostname:port/ovm/core/wsapi/rest/Manager
  while True:
    r=s.get(baseUri+'/Manager')
    manager=r.json()
    if manager[0]['managerRunState'].upper() == 'RUNNING':
      break
      time.sleep(1)
      return;
 
def serverList(s,baseUri):
  print "\nServer List:"
  print "##############"
  r=s.get(baseUri+'/Server')
  for i in r.json():
    # do something with the content
    print '{:20} {:20}'.format(i['serverRunState'],i['name'])
 
def vmList(s,baseUri):
  print "\nVM List:"
  print "########"
  r=s.get(baseUri+'/Vm')
  for i in r.json():
    # print '{:20} {:20}'.format(i['vmRunState'],i['name'])
    print '{:20} {:35} {:30}'.format(i['vmRunState'],i['name'],i['id']['value']),
    for d in i['vmDiskMappingIds']:
      print d['value'],
    print
    # print '{name} '.format(name=i['name'])
    # print i
 
def showVm(s,baseUri,name):
  print "\nVM Show:"
  print "##########"
  r=s.get(baseUri+'/Vm')
  for i in r.json():
    if i['name'] == name:
      print '{:20} {:55}'.format(i['vmRunState'],i['name']), 
      for d in i['vmDiskMappingIds']:
   if 'CDROM' not in d['name']:
          print d['value'],
          disk=s.get(baseUri+'/VmDiskMapping/'+d['value'])
     d = disk.json()
     if "obiee" in d['virtualDiskId']['name']:
       dName = d['virtualDiskId']['name'].replace('obiee_template',i['name'])
       dName = dName.split('img')[0]+'img'
           print 'value: {} and name {} should be renamed -> {}'.format(d['virtualDiskId']['value'],d['virtualDiskId']['name'],dName),
       print
 
def cmdVm(s,baseUri,cmd,name):
  print "\nVM " + cmd
  print "##########"
  vm_id=get_id_from_name(s,baseUri,'Vm',name)
  print vm_id
  r=s.put(baseUri+'/Vm/'+vm_id+'/'+cmd)
  job=r.json()
  # print job
  # wait for the job to complete
  vm_id=wait_for_job(job['id']['uri'],s)
 
def updateVm(s,baseUri,name):
  print "\nVM Update Vm Disk Names:"
  print "##########################"
  r=s.get(baseUri+'/Vm')
  for i in r.json():
    if i['name'] == name:
      #print i
      print '{:20} {:20} {:55}'.format(i['id']['value'],i['vmRunState'],i['name'])
      for disk in i['vmDiskMappingIds']:
        if 'CDROM' not in disk['name']:
          #print disk['value'],
          value=s.get(baseUri+'/VmDiskMapping/'+disk['value'])
          d = value.json()
     oldName = d['virtualDiskId']['name']
          newName = d['virtualDiskId']['name'].replace('obiee_template',i['name'])
          newName = newName.split('img')[0]+'img'
     d['virtualDiskId']['name']=newName
     d['id']['name']=newName
     d['name']=newName
           
          #print 'value: {:20} name: {:55} new name {}'.format(d['virtualDiskId']['value'],d['virtualDiskId']['name'],dName),
          print 'value: {:20} name: {:55} new name {}'.format(disk['value'],oldName,newName)
          #print d
          uri='{base}/VmDiskMapping/{id}'.format(base=baseUri,id=d['id']['value'])
     #print uri
          r1=s.put(uri,data=json.dumps(d))
          job=r1.json()
         #print job
          # wait for the job to complete
          wait_for_job(job['id']['uri'],s)
 
      i['vmDiskMappingIds'][0]['name']='new.img'
      #print i
      uri='{base}/Vm/{id}'.format(base=baseUri,id=i['id']['value'])
      #print uri
       
      r=s.put(uri,data=json.dumps(i))
      job=r.json()
      #print job
      # wait for the job to complete
      wait_for_job(job['id']['uri'],s)
 
def updateVmMemory(s,baseUri,name,memory):
  print "\nVM Update Vm Memory for " + name
  print "########################################"
  vm_id=get_id_from_name(s,baseUri,'Vm',name)
  uri='{base}/Vm/{id}'.format(base=baseUri,id=vm_id)
  r=s.get(uri)
  d=r.json()
  #print d
  d['memory']='512'
 
  r=s.put(uri,data=json.dumps(d))
  job=r.json()
  #print job
  # wait for the job to complete
  wait_for_job(job['id']['uri'],s)
 
def updateVirtualDisk(s,baseUri,id,newDiskName):
  print "\nVM Update Vm Disk Mapping for " + id
  print "########################################"
  uri='{base}/VirtualDisk/{id}'.format(base=baseUri,id=id)
 
  r=s.get(uri)
  disk=r.json()
  #print disk
 
  #oldName = disk['virtualDiskId']['name']
  #newName = disk['virtualDiskId']['name'].replace('obiee_template',d['name'])
  #newName = newName.split('img')[0]+'img'
      
  disk['name']=newDiskName
 
  #disk['name']='newname_system.img'
    
  r=s.put(uri,data=json.dumps(disk))
  job=r.json()
  # wait for the job to complete
  wait_for_job(job['id']['uri'],s)
 
def updateVmDiskNames(s,baseUri,name):
  print "\nVM Update Vm Disk Names for " + name
  print "########################################"
  vm_id=get_id_from_name(s,baseUri,'Vm',name)
  uri='{base}/Vm/{id}'.format(base=baseUri,id=vm_id)
  r=s.get(uri)
  vm=r.json()
 
  dNum=0 
  for disk in vm['vmDiskMappingIds']:
        if 'CDROM' not in disk['name']:
     dNum = dNum +1
     newDiskName=name + "_disk" + str(dNum)
     #if "system" in disk['name']:
     #  newDiskName=name + "_system.img"
      #if "data1" in disk['name']:
     #  newDiskName=name + "_data1.img"
 
     ## update VmDiskMapping as shown in Repository
     dMapping=s.get(baseUri+'/VmDiskMapping/'+disk['value'])
     dm=dMapping.json()
     updateVirtualDisk(s,baseUri,dm['virtualDiskId']['value'],newDiskName)