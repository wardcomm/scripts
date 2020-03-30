from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME   = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME      = "{{ WLS_USERNAME }}"
WLS_PASSWORD      = "{{ WLS_PASSWORD }}"
adminUrl          = "t3://{{ SOA_ADMIN_wPORT }}"
SAF_CONTEXT_LIST  = "{{ SAF_CONTEXT_LIST }}"

## List of derived variables

SAF_CONTEXTS = SAF_CONTEXT_LIST.split(',')

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
def createSAFContext():
    for sc in range(len(SAF_CONTEXTS)):
	  sc_name=SAF_CONTEXTS[sc].split('%')[0]
	  sc_module_name=SAF_CONTEXTS[sc].split('%')[1]
	  sc_URL=SAF_CONTEXTS[sc].split('%')[2]
	  sc_username=SAF_CONTEXTS[sc].split('%')[3]
	  sc_password=SAF_CONTEXTS[sc].split('%')[4]
	  try:
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name)
           cmo.createSAFRemoteContext(sc_name)
	   cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFRemoteContexts/'+sc_name+'/SAFLoginContext/'+sc_name)
	   cmo.setLoginURL(sc_URL)
	   cmo.setUsername(sc_username)
	   cmo.setPassword(sc_password)
          except:
            print (dumpStack())

## Function to update Remote SAF Context
def updateSAFContext():
    for sc in range(len(SAF_CONTEXTS)):
          sc_name=SAF_CONTEXTS[sc].split('%')[0]
          sc_module_name=SAF_CONTEXTS[sc].split('%')[1]
          sc_remote=SAF_CONTEXTS[sc].split('%')[5]
          try:
           cd('/JMSSystemResources/'+sc_module_name+'/JMSResource/'+sc_module_name+'/SAFRemoteContexts/'+sc_name)
           cmo.setReplyToSAFRemoteContextName(sc_remote)
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFContext()
disconnect_wlst_editSession()
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
updateSAFContext()
disconnect_wlst_editSession()
