from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME      = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME         = "{{ WLS_USERNAME }}"
WLS_PASSWORD         = "{{ WLS_PASSWORD }}"
adminUrl             = "t3://{{ SOA_ADMIN_wPORT }}"
SAF_IMPORT_DEST_LIST = "{{ SAF_IMPORT_DEST_LIST }}"

## List of derived variables

SAF_IMPORT_DESTS = SAF_IMPORT_DEST_LIST.split(',')

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
def createSAFImportDest():
    for sc in range(len(SAF_IMPORT_DESTS)):
	  saf_import_dest_name=SAF_IMPORT_DESTS[sc].split(':')[0]
	  sc_module_name=SAF_IMPORT_DESTS[sc].split(':')[1]
	  sub_deploy_name=SAF_IMPORT_DESTS[sc].split(':')[2]
	  remote_saf_name=SAF_IMPORT_DESTS[sc].split(':')[3]
	  saf_error_handler=SAF_IMPORT_DESTS[sc].split(':')[4]
	  saf_ttl=SAF_IMPORT_DESTS[sc].split(':')[5]
	  try:
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name)
	   cmo.createSAFImportedDestinations(saf_import_dest_name)
  	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFImportedDestinations/'+saf_import_dest_name)
	   cmo.setJNDIPrefix(saf_import_dest_name)
	   cmo.setSubDeploymentName(sub_deploy_name)
	   cmo.setSAFRemoteContext(getMBean('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFRemoteContexts/'+remote_saf_name))
	   cmo.setSAFErrorHandling(getMBean('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFErrorHandlings/'+saf_error_handler))
	   cmo.setTimeToLiveDefault(saf_ttl)
	   cmo.setUseSAFTimeToLiveDefault(false)
	   cmo.setDefaultTargetingEnabled(false)
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFImportDest()
disconnect_wlst_editSession()
