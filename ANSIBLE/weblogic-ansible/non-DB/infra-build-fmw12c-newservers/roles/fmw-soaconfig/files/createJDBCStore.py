from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME  = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME     = "{{ WLS_USERNAME }}"
WLS_PASSWORD     = "{{ WLS_PASSWORD }}"
adminUrl         = "t3://{{ SOA_ADMIN_wPORT }}"

#Loading Properties
JDBC_STORE_LIST = "{{ JDBC_STORE_LIST }}"

## List of derived variables

JDBC_STORES = JDBC_STORE_LIST.split(',')

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

## Function to create JDBC Store
def createJDBCStore():
    for js in range(len(JDBC_STORES)):
      js_name=JDBC_STORES[js].split(':')[0]
      ds_name=JDBC_STORES[js].split(':')[1]
      pf_name=JDBC_STORES[js].split(':')[2]
      js_target=JDBC_STORES[js].split(':')[3]
      try:
        print "Updating data sources statement timeout values"
        print js_name
        cd('/')
        cmo.createJDBCStore(js_name)
        cd('/JDBCStores/'+js_name)
        cmo.setDataSource(getMBean('/JDBCSystemResources/'+ds_name))
        cmo.setPrefixName(pf_name)	   
        set('Targets',jarray.array([ObjectName('com.bea:Name='+js_target+',Type=Server')], ObjectName))
      except:
        print (dumpStack())

## Function to update Synch Policy in JDBC Store
def updateSynchPolicy():
    for js in range(len(JDBC_STORES)):
        js_name=JDBC_STORES[js].split(':')[0]
        ds_name=JDBC_STORES[js].split(':')[1]
        pf_name=JDBC_STORES[js].split(':')[2]
        js_target=JDBC_STORES[js].split(':')[3]
        try:
            print "Updating data sources statement timeout values"
            print js_name
            cd('/JDBCStores/'+js_name)
            cmo.setSynchronousWritePolicy('Direct-Write-With-Cache')
        except:
            print (dumpStack())

print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createJDBCStore()
disconnect_wlst_editSession()
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
updateSynchPolicy()
disconnect_wlst_editSession()
