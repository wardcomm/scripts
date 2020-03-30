from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
adminUrl        = "t3://{{ SOA_ADMIN_wPORT }}"
SAF_AGENT_LIST  = "{{ SAF_AGENT_LIST }}"

## List of derived variables

SAF_AGENTS = SAF_AGENT_LIST.split(',')

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
def createSAFAgent():
    for saf in range(len(SAF_AGENTS)):
	  saf_name=SAF_AGENTS[saf].split(':')[0]
	  saf_fs=SAF_AGENTS[saf].split(':')[1]
	  saf_target=SAF_AGENTS[saf].split(':')[2]
	  try:
	    cd('/')
	    cmo.createSAFAgent(saf_name)
	    cd('/SAFAgents/'+saf_name)
            cmo.setStore(getMBean('/FileStores/'+saf_fs))
            set('Targets',jarray.array([ObjectName('com.bea:Name='+saf_target+',Type=Server')], ObjectName))
            cmo.setServiceType('Sending-only')
          except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createSAFAgent()
disconnect_wlst_editSession()
