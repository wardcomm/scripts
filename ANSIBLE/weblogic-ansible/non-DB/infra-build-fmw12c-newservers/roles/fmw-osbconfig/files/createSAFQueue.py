from sets import Set

#List of all variables, These are substituted by ansible while template copy

OSB_DOMAIN_NAME = "{{ OSB_DOMAIN_NAME }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
adminUrl        = "t3://{{ OSB_ADMIN_wPORT }}"
SAF_QUEUE_LIST  = "{{ SAF_QUEUE_LIST }}"

## List of derived variables

SAF_QUEUES = SAF_QUEUE_LIST.split(',')

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

## Function to create SAF Imported Destination
def createSAFQueue():
    for sq in range(len(SAF_QUEUES)):
	  saf_import_dest_name=SAF_QUEUES[sq].split(':')[2]
	  sc_module_name=SAF_QUEUES[sq].split(':')[1]
	  saf_queue_name=SAF_QUEUES[sq].split(':')[0]
	  saf_remote_jndi=SAF_QUEUES[sq].split(':')[3]
	  try:
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFImportedDestinations/'+saf_import_dest_name)
	   cmo.createSAFQueue(saf_queue_name)
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFImportedDestinations/'+saf_import_dest_name+'/SAFQueues/'+saf_queue_name)
	   cmo.setRemoteJNDIName(saf_remote_jndi)
          except:
            print (dumpStack())

## Function to create SAF Imported Destination
def updateSAFQueue():
    for sq in range(len(SAF_QUEUES)):
          saf_import_dest_name=SAF_QUEUES[sq].split(':')[2]
          sc_module_name=SAF_QUEUES[sq].split(':')[1]
          saf_queue_name=SAF_QUEUES[sq].split(':')[0]
          saf_remote_jndi=SAF_QUEUES[sq].split(':')[3]
          try:
           cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFImportedDestinations/'+saf_import_dest_name+'/SAFQueues/'+saf_queue_name)
           cmo.setNonPersistentQos('Exactly-Once')
          except:
            print (dumpStack())


print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFQueue()
disconnect_wlst_editSession()
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
updateSAFQueue()
disconnect_wlst_editSession()
