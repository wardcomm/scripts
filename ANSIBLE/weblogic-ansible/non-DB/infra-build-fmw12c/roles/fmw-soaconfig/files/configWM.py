import sys
import os
import jarray
import dircache
from java.io import File
from java.lang import String

SOA_ADMIN_wPORT    = "{{ SOA_ADMIN_wPORT      }}"
SOA_DOMAIN_NAME     = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
adminUrl            = "t3://{{ SOA_ADMIN_wPORT }}"

PROPERTIES_FILE     = "{{ STAGE_DIR }}/workmanager.properties"

#Loading Properties

wmProps = Properties()
wmProps.load(FileInputStream(PROPERTIES_FILE))


#Function to createWM for given index

def createWM(index):

 wmName                    = wmProps.get("WM_NAME."+index)
 domainName                = wmProps.get("DM_NAME."+index)
 wmTarget                  = wmProps.get("WM_TARGET."+index)
 wmTargetType              = wmProps.get("WM_TARGET_TYPE."+index)
 maxThreadConstraintName   = wmProps.get("WM_MaxThreadConstraint_NAME."+index)
 minThreadConstraintName   = wmProps.get("WM_MaxThreadConstraint_NAME."+index)
 CapacityConstraintName    = wmProps.get("WM_CapacityConstraint_Name."+index)
 maxThread                 = wmProps.get("WM_TC_MAX."+index)
 capThread                 = wmProps.get("WM_TC_CAP."+index)
 minThread                 = wmProps.get("WM_TC_MIN."+index)
 
 
 cd ('/')
 cmo.createWorkManager(wmName)
 cd('/SelfTuning/' + domainName + '/WorkManagers/' + wmName)
 cmo.setName(wmName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 
 
 cd('/SelfTuning/' + domainName)
 cmo.createMaxThreadsConstraint(maxThreadConstraintName)
 cd('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName)
 cmo.setName(maxThreadConstraintName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 set('MinThread',int(minThread))
 set('MaxThread',int(maxThread))
 #cmo.setCount(20)
 cmo.unSet('ConnectionPoolName')
 
 
 #creating MinThreads Constraint
 
 #cd('/SelfTuning/' + domainName)
 #cmo.createMinThreadsConstraint(minThreadConstraintName)
 #cd('/SelfTuning/' + domainName + '/MinThreadsConstraints/' + minThreadConstraintName)
 #cmo.setName(minThreadConstraintName)
 #set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 #set('MinThread',int(minThread))
 #cmo.unSet('ConnectionPoolName')
 
 
 cd('/SelfTuning/' + domainName)
 cmo.createCapacity(CapacityConstraintName)
 cd('/SelfTuning/' + domainName + '/Capacities/' + CapacityConstraintName)
 cmo.setName(CapacityConstraintName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 set('CapacityThread',int(capThread))
 
 cd('/SelfTuning/' + domainName + '/WorkManagers/' + wmName)
 cmo.setMaxThreadsConstraint(getMBean('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName))
 cmo.setCapacity(getMBean('/SelfTuning/' + domainName + '/Capacities/' + CapacityConstraintName))
 cmo.setIgnoreStuckThreads(true)
 
#Looping through properties
 
try:

 connect(WLS_USERNAME,WLS_PASSWORD,"t3://"+SOA_ADMIN_wPORT)
 edit()
 startEdit()

 TOTAL_WM = wmProps.get("TOTAL_WM")
  
 for i in range(1,int(TOTAL_WM)+1):
  try:
   createWM(str(i))
  except:
   dumpstatck()
   exit(1)
   
 save()
 activate(block="true")
 disconnect()
 
except:
 dumpstack()
 exit(1)
