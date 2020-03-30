from sets import Set

#List of all variables, These are substituted by ansible while template copy

OSB_DOMAIN_HOME     = "{{ OSB_DOMAIN_HOME }}"
user            = "{{ WLS_USERNAME }}"
passwd          = "{{ WLS_PASSWORD }}"
adminUrl        = "t3://{{ OSB_ADMIN_wPORT }}"
NM_HOME  	= "{{ COMMON }}/nodemanager"

## Function to connect to Weblogic
def connect_wlst_editSession(user,passwd,adminUrl):
    try:
      connect(user,passwd,adminUrl)
      edit()
      startEdit()
    except:
      print(dumpStack())

## Function to diconnect from Weblogic
def disconnect_wlst_editSession():
    save()
    activate(block="true")
    disconnect()

## Function to Untarget Apps
def RegisterNM():
     try:
       print "Resgistering Node Manager"
       nmEnroll( OSB_DOMAIN_HOME, NM_HOME )
     except:
      print ( dumpStack() )

connect_wlst_editSession(user,passwd,adminUrl)
RegisterNM()
disconnect_wlst_editSession()
