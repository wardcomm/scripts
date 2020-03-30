from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
adminUrl        = "t3://{{ SOA_ADMIN_wPORT }}"
JMS_SERVER_LIST = "{{ JMS_SERVER_LIST }}"

## List of derived variables

JMS_SERVERS = JMS_SERVER_LIST.split(',')

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

## Function to create JMSServers with File Store
def createJMSServer():
    for jm in range(len(JMS_SERVERS)):
		jm_name=JMS_SERVERS[jm].split(':')[0]
		js_name=JMS_SERVERS[jm].split(':')[1]
		jm_target=JMS_SERVERS[jm].split(':')[2]
		try:
			cd('/')	  
			cmo.createJMSServer(jm_name)
			cd('/JMSServers/'+jm_name)
			cmo.setPersistentStore(getMBean('/JDBCStores/'+js_name))
			set('Targets',jarray.array([ObjectName('com.bea:Name='+jm_target+',Type=Server')], ObjectName))
		except:
			print (dumpStack())
      
print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createJMSServer()
disconnect_wlst_editSession()

