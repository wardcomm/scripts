from sets import Set

#List of all variables, These are substituted by ansible while template copy

OSB_DOMAIN_NAME    = "{{ OSB_DOMAIN_NAME }}"
WLS_USERNAME   = "{{ WLS_USERNAME }}"
WLS_PASSWORD   = "{{ WLS_PASSWORD }}"
adminUrl           = "t3://{{ OSB_ADMIN_wPORT }}"
SAF_ERROR_LIST = "{{ SAF_ERROR_LIST }}"

## List of derived variables

SAF_ERRORS = SAF_ERROR_LIST.split(',')

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
def createSAFErrorHandler():
    for sq in range(len(SAF_ERRORS)):
	  saf_error_redirect=SAF_ERRORS[sq].split(':')[2]
	  sc_module_name=SAF_ERRORS[sq].split(':')[1]
	  saf_error_name=SAF_ERRORS[sq].split(':')[0]
	  saf_import_dest=SAF_ERRORS[sq].split(':')[3]
          try:
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name)
	   cmo.createSAFErrorHandling(saf_error_name)
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFErrorHandlings/'+saf_error_name)
	   cmo.setSAFErrorDestination(getMBean('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFImportedDestinations/'+saf_import_dest+'/SAFQueues/'+saf_error_redirect))
	   cmo.setPolicy('Redirect')
	   cmo.setLogFormat('%header%, %properties%, %body%')
	  except: 
	    print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFErrorHandler()
disconnect_wlst_editSession()
