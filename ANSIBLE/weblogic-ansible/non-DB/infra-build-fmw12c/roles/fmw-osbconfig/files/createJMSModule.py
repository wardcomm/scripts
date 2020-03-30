from sets import Set

#List of all variables, These are substituted by ansible while template copy

OSB_DOMAIN_NAME     = "{{ OSB_DOMAIN_NAME }}"
WLS_USERNAME        = "{{ WLS_USERNAME }}"
WLS_PASSWORD        = "{{ WLS_PASSWORD }}"
adminUrl            = "t3://{{ OSB_ADMIN_wPORT }}"
JMS_MODULE_LIST     = "{{ JMS_MODULE_LIST }}"

## List of derived variables

JMS_MODULES = JMS_MODULE_LIST.split(',')

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
def createJMSModule():
    for jm in range(len(JMS_MODULES)):
	  jm_name=JMS_MODULES[jm].split(':')[0]
	  jm_target=JMS_MODULES[jm].split(':')[1]
	  try:
	   cd('/')
	   cmo.createJMSSystemResource(jm_name)
  	   cd('/SystemResources/'+jm_name)
	   set('Targets',jarray.array([ObjectName('com.bea:Name='+jm_target+',Type=Cluster')], ObjectName))
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createJMSModule()
disconnect_wlst_editSession()
