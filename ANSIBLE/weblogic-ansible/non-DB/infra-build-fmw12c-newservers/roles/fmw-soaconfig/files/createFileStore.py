from sets import Set

#List of all variables, These are substituted by ansible while template copy

SOA_DOMAIN_NAME  = "{{ SOA_DOMAIN_NAME }}"
WLS_USERNAME     = "{{ WLS_USERNAME }}"
WLS_PASSWORD     = "{{ WLS_PASSWORD }}"
adminUrl         = "t3://{{ SOA_ADMIN_wPORT }}"

#Loading Properties
FILE_STORE_LIST = "{{ FILE_STORE_LIST }}"

## List of derived variables

FILE_STORES = FILE_STORE_LIST.split(',')

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
def createFileStore():
    for fs in range(len(FILE_STORES)):
	  fs_name=FILE_STORES[fs].split(':')[0]
	  fs_directory=FILE_STORES[fs].split(':')[1]
	  fs_target=FILE_STORES[fs].split(':')[2]
	  try:
            print "Updating data sources statement timeout values"
            print fs_name
	    cd('/')
	    cmo.createFileStore(fs_name)
	    cd('/FileStores/'+fs_name)
	    set('Directory',fs_directory)
	    set('Targets',jarray.array([ObjectName('com.bea:Name='+fs_target+',Type=Server')], ObjectName))
          except:
            print (dumpStack())

## Function to update Synch Policy in File Store
def updateSynchPolicy():
    for fs in range(len(FILE_STORES)):
          fs_name=FILE_STORES[fs].split(':')[0]
          fs_directory=FILE_STORES[fs].split(':')[1]
          fs_target=FILE_STORES[fs].split(':')[2]
          try:
            print "Updating data sources statement timeout values"
            print fs_name
            cd('/FileStores/'+fs_name)
            cmo.setSynchronousWritePolicy('Direct-Write-With-Cache')
          except:
            print (dumpStack())


print('Connecting to Server : '+adminUrl)
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
createFileStore()
disconnect_wlst_editSession()
connect_wlst_editSession(WLS_USERNAME,WLS_PASSWORD,adminUrl)
updateSynchPolicy()
disconnect_wlst_editSession()
