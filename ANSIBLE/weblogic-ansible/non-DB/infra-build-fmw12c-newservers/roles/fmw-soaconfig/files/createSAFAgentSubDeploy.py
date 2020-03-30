from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME  = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME     = "{{ WLS_USERNAME }}"
WLS_PASSWORD     = "{{ WLS_PASSWORD }}"
adminUrl         = "t3://{{ SOA_ADMIN_wPORT }}"
SUB_DEPLOY_LIST  = "{{ SUB_DEPLOY_LIST }}"

## List of derived variables

SUB_DEPLOYS = SUB_DEPLOY_LIST.split(',')

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

## Function to create SAF Error Imported Destination Name
def createSAFSubDeploy():
    for sc in range(len(SUB_DEPLOYS)):
	  sub_deploy_name=SUB_DEPLOYS[sc].split(':')[0]
	  sc_module_name=SUB_DEPLOYS[sc].split(':')[1]
	  targets=SUB_DEPLOYS[sc].split(':')[2].split('%')
	  try:
	    cd('/SystemResources/'+sc_module_name)
	    cmo.createSubDeployment(sub_deploy_name)
	    cd('/SystemResources/'+sc_module_name+'/SubDeployments/'+sub_deploy_name)
	    for t in range(len(targets)):
		target=targets[t]
		print 'target='+target
		set('Targets',jarray.array([ObjectName('com.bea:Name='+target+',Type=SAFAgent')], ObjectName))
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFSubDeploy()
disconnect_wlst_editSession()
