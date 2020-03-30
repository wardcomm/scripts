import sys
import os
import jarray
import dircache
from java.io import File
from java.lang import String

OSB_ADMIN_wPORT  = "{{ OSB_ADMIN_wPORT }}"
OSB_DOMAIN_NAME  = "{{ OSB_DOMAIN_NAME }}"
WLS_USERNAME     = "{{ WLS_USERNAME }}"
WLS_PASSWORD     = "{{ WLS_PASSWORD }}"
adminUrl         = "t3://{{ OSB_ADMIN_wPORT }}"

PROPERTIES_FILE  = "{{ STAGE_DIR }}/workmanager.properties"

#Loading Properties

wmProps = Properties()
wmProps.load(FileInputStream(PROPERTIES_FILE))

# Function to create MinThread Constraints

def createMinTC(index):
 minThreadConstraintName  = wmProps.get("WM_MinThreadConstraint_NAME."+index)
 minThread                = wmProps.get("WM_TC_MIN."+index)
 wm_target                = wmProps.get("WM_TARGET."+index)
 wmTargetType             = wmProps.get("WM_TARGET_TYPE."+index)
 cd('/SelfTuning/' + domainName + '/MinThreadsConstraints/')
 create(minThreadConstraintName,'MinThreadsConstraints')
 cd('/SelfTuning/' + domainName + '/MinThreadsConstraints/' + minThreadConstraintName)
 cmo.setName(minThreadConstraintName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 cmo.setCount(int(minThread))

# Function to create MaxThread Constraints
def createMaxTC(index):
 maxThreadConstraintName   = wmProps.get("WM_MaxThreadConstraint_NAME."+index)
 maxThread                 = wmProps.get("WM_TC_MAX."+index)
 wm_target                 = wmProps.get("WM_TARGET."+index)
 wmTargetType              = wmProps.get("WM_TARGET_TYPE."+index)
 cd('/SelfTuning/' + domainName + '/MaxThreadsConstraints/')
 create(maxThreadConstraintName,'MaxThreadsConstraints')
 cd('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName)
 cmo.setName(maxThreadConstraintName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 cmo.setCount(int(maxThread))
 cmo.unSet('ConnectionPoolName')

# Function to create Capacity Constraints
def createCAPC(index):
 CapacityConstraintName    = wmProps.get("WM_CapacityConstraint_NAME."+index)
 capThread                 = wmProps.get("WM_TC_CAP."+index)
 wm_target                 = wmProps.get("WM_TARGET."+index)
 wmTargetType              = wmProps.get("WM_TARGET_TYPE."+index)
 cd('/SelfTuning/' + domainName + '/Capacities/')
 create(CapacityConstraintName,'Capacities')
 cd('/SelfTuning/' + domainName + '/Capacities/' + CapacityConstraintName)
 cmo.setName(CapacityConstraintName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 cmo.setCount(int(capThread))

# Function to create WorkManagers
def createWM(index):
 wmName                    = wmProps.get("WM_NAME."+index)
 domainName                = wmProps.get("DM_NAME."+index)
 wm_target                 = wmProps.get("WM_TARGET."+index)
 wmTargetType              = wmProps.get("WM_TARGET_TYPE."+index)
 minThreadConstraintName   = wmProps.get("WM_MinThreadConstraint_NAME."+index)
 maxThreadConstraintName   = wmProps.get("WM_MaxThreadConstraint_NAME."+index)
 CapacityConstraintName    = wmProps.get("WM_CapacityConstraint_NAME."+index)
 cd('/SelfTuning/' + domainName + '/WorkManagers/')
 create(wmName,'WorkManagers')
 cd('/SelfTuning/' + domainName + '/WorkManagers/' + wmName)
 cmo.setName(wmName)
 set('Targets',jarray.array([ObjectName('com.bea:Name=' +wm_target+',Type=Cluster')], ObjectName))
 cd('/SelfTuning/' + domainName + '/WorkManagers/' + wmName)
 cmo.setMinThreadsConstraint(getMBean('/SelfTuning/' + domainName + '/MinThreadsConstraints/' + minThreadConstraintName))
 cmo.setMaxThreadsConstraint(getMBean('/SelfTuning/' + domainName + '/MaxThreadsConstraints/' + maxThreadConstraintName))
 cmo.setCapacity(getMBean('/SelfTuning/' + domainName + '/Capacities/' + CapacityConstraintName))
 cmo.setIgnoreStuckThreads(true)

#Looping through properties

adminUser=wmProps.get("adminUser")
adminPassword=wmProps.get("adminPassword")
adminURL=wmProps.get("adminURL")

#Looping through properties
 
try:

 connect(WLS_USERNAME,WLS_PASSWORD,"t3://"+OSB_ADMIN_wPORT)
 edit()
 startEdit()
 
 TOTAL_MinTC = wmProps.get("TOTAL_MinTC")
 TOTAL_MaxTC = wmProps.get("TOTAL_MaxTC")
 TOTAL_CAPC  = wmProps.get("TOTAL_CAPC")
 TOTAL_WM    = wmProps.get("TOTAL_WM")

 for h in range(1,int(TOTAL_MinTC)+1):
  try:
   createMinTC(str(h))
  except Exception, inst:
      print('Some diagnostic message here')
      print inst
      print sys.exc_info()[1]

 for i in range(1,int(TOTAL_MaxTC)+1):
  try:
   createMaxTC(str(i))
  except Exception, inst:
      print('Some diagnostic message here')
      print inst
      print sys.exc_info()[1]

 for j in range(1,int(TOTAL_CAPC)+1):
  try:
   createCAPC(str(j))
  except Exception, inst:
      print('Some diagnostic message here')
      print inst
      print sys.exc_info()[1]

 for k in range(1,int(TOTAL_WM)+1):
  try:
   createWM(str(k))
  except Exception, inst:
      print('Some diagnostic message here')
      print inst
      print sys.exc_info()[1]

 save()
 activate(block="true")
 disconnect()

except Exception, inst:
    print('Some diagnostic message here')
    print inst
    print sys.exc_info()[1]
