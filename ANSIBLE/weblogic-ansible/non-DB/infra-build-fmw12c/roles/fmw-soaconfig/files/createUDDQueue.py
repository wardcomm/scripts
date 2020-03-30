from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
adminUrl        = "t3://{{ SOA_ADMIN_wPORT }}"
UDD_QUEUE_LIST  = "{{ UDD_QUEUE_LIST }}"

## List of derived variables

UDD_QUEUES = UDD_QUEUE_LIST.split(',')

## Function to connect to Weblogic
def connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,srvUrl):
    try:
      connect(WLS_USERNAME,WLS_PASSWORD,srvUrl)
      edit()
      startEdit()
    except:
      print(dumpStack())

## Function to diconnect from Weblogic
def disconnect_wlst_editSession():
    save()
    activate(block="true")
    disconnect()

## Function to create File Store
def createUDDQueue():
    for udd in range(len(UDD_QUEUES)):
	  udd_name=UDD_QUEUES[udd].split(':')[0]
	  udd_module_name=UDD_QUEUES[udd].split(':')[1]
	  try:
	   cd('/JMSSystemResources/'+udd_module_name+'/JMSResource/'+udd_module_name)
	   cmo.createUniformDistributedQueue(udd_name)
	   cd('/JMSSystemResources/'+udd_module_name+'/JMSResource/'+udd_module_name+'/UniformDistributedQueues/'+udd_name)
	   cmo.setJNDIName(udd_name)
	   cmo.setDefaultTargetingEnabled(true)
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createUDDQueue()
disconnect_wlst_editSession()
