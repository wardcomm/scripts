from sets import Set

#List of Declared Variables passed from Ansible
DEMO_WLHOME               = "{{ DEMO_WLHOME }}"

DEMO_DOMAIN_NAME          =  "{{ DEMO_DOMAIN_NAME }}"
DEMO_DOMAIN_HOME          =  "{{ DEMO_DOMAIN_HOME }}"
DEMO_APP_PATH             =  "{{ DEMO_APP_PATH }}"

DEMO_LOG_FOLDER           = "{{ DEMO_LOG_FOLDER }}"
ADMIN_SERVER              = "{{ ADMIN_SERVER }}"
ADMIN_ADDRESS             = "{{ AdminAddress }}"
ADMIN_LSTN_PORT           = "{{  PORT_A }}"
ADMIN_HOST_NAME                 = "{{ AdminHost }}"
 
JSSE_ENABLED             = "{{ JSSE_ENABLED }}"
DEVELOPMENT_MODE         = "{{ DEVELOPMENT_MODE }}"
WEBTIER_ENABLED          = "{{ WEBTIER_ENABLED }}"

ADMIN_USER               = "{{ WLS_USERNAME }}"
ADMIN_PASSWORD           = "{{ WLS_PASSWORD }}"

JAVA_HOME                = "{{ JAVA_HOME }}"

ADM_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+DEMO_LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+DEMO_LOG_FOLDER+'AdminServer_err.out'
DEMO_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1024m '
DEMO_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=752m -Xms1024m -Xmx1532m '

HOSTMACHINES = HOSTMACHINEIPS = []

MachineNames = "{{ groups['fmw'] | join(',') }}"
HOSTMACHINES = MachineNames.split(",")

ListOfIPs = "{{ groups['fmw'] | map('extract', hostvars, ['ansible_default_ipv4', 'address']) | join(',') }}"
HOSTMACHINEIPS = ListOfIPs.split(",")

noOfHosts = len(HOSTMACHINES)
JVMsPerNode               = "{{ JVMS_PER_NODE }}"

prosvr = "provdemo_server"
lport = 7003

def createBootPropertiesFile(directoryPath,fileName, username, password):
  serverDir = File(directoryPath)
  bool = serverDir.mkdirs()
  fileNew=open(directoryPath + '/'+fileName, 'w')
  fileNew.write('username=%s\n' % username)
  fileNew.write('password=%s\n' % password)
  fileNew.flush()
  fileNew.close()

def createAdminStartupPropertiesFile(directoryPath, args):
  adminserverDir = File(directoryPath)
  bool = adminserverDir.mkdirs()
  fileNew=open(directoryPath + '/startup.properties', 'w')
  args=args.replace(':','\\:')
  args=args.replace('=','\\=')
  fileNew.write('Arguments=%s\n' % args)
  fileNew.flush()
  fileNew.close()

def changeManagedServer(server,port,java_arguments):
  cd('/Servers/'+server)
  
  create(server,'ServerStart')
  cd('ServerStart/'+server)
  set('Arguments' , java_arguments+' -Dweblogic.Stdout='+DEMO_LOG_FOLDER+server+'.out -Dweblogic.Stderr='+DEMO_LOG_FOLDER+server+'_err.out')
  set('JavaVendor','Sun')
  set('JavaHome'  , JAVA_HOME)

  cd('/Server/'+server)
  create(server,'SSL')
  cd('SSL/'+server)
  set('Enabled'                    , 'False')
  set('HostNameVerificationIgnored', 'True')

  if JSSE_ENABLED == true:
    set('JSSEEnabled','True')
  else:
    set('JSSEEnabled','False')  

  cd('/Server/'+server)
  create(server,'Log')
  cd('/Server/'+server+'/Log/'+server)
  set('FileName'     , DEMO_LOG_FOLDER+server+'.log')
  set('FileCount'    , 10)
  set('FileMinSize'  , 5000)
  set('RotationType' ,'byTime')
  set('FileTimeSpan' , 24)

print('Start...wls domain with template {{ ORACLE_HOME }}/wlserver/common/templates/wls/wls.jar')
readTemplate('{{ ORACLE_HOME }}/wlserver/common/templates/wls/wls.jar')

cd('/')

print('Set domain log')
create('base_domain','Log')

cd('/Log/base_domain')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

cd('/Servers/AdminServer')

# set name of adminserver

set('Name',ADMIN_SERVER )
cd('/Servers/'+ADMIN_SERVER)

# set address and port
print (ADMIN_LSTN_PORT)
set('ListenAddress',ADMIN_ADDRESS)
set('ListenPort'   ,int(ADMIN_LSTN_PORT))

setOption( "AppDir", DEMO_APP_PATH )

create(ADMIN_SERVER,'ServerStart')
cd('ServerStart/'+ADMIN_SERVER)
set('Arguments' , ADM_JAVA_ARGUMENTS)
set('JavaVendor','Sun')
set('JavaHome'  , JAVA_HOME)

cd('/Server/'+ADMIN_SERVER)
create(ADMIN_SERVER,'SSL')
cd('SSL/'+ADMIN_SERVER)
set('Enabled'                    , 'False')
set('HostNameVerificationIgnored', 'True')

if JSSE_ENABLED == true:
  set('JSSEEnabled','True')
else:
  set('JSSEEnabled','False')


cd('/Server/'+ADMIN_SERVER)

create(ADMIN_SERVER,'Log')
cd('/Server/'+ADMIN_SERVER+'/Log/'+ADMIN_SERVER)
set('FileName'    ,DEMO_LOG_FOLDER+ADMIN_SERVER+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

print('Set password...')
cd('/')
cd('Security/base_domain/User/weblogic')

# weblogic user name + password
set('Name',ADMIN_USER)
cmo.setPassword(ADMIN_PASSWORD)

if DEVELOPMENT_MODE == true:
  setOption('ServerStartMode', 'dev')
else:
  setOption('ServerStartMode', 'prod')

setOption('JavaHome', JAVA_HOME)

print('write domain...')

# write path + domain name
writeDomain(DEMO_DOMAIN_HOME)
closeTemplate()

createAdminStartupPropertiesFile(DEMO_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

readDomain(DEMO_DOMAIN_HOME)

cd('/')

setOption( "AppDir", DEMO_APP_PATH )

dumpStack();

addTemplate('{{ ORACLE_HOME }}/oracle_common/common/templates/wls/oracle.wls-webservice-template.jar')

setOption( "AppDir", DEMO_APP_PATH )

## Creating a Cluster

print 'Create provdemo_cluster'
cd('/')
create('provdemo_cluster', 'Cluster')

#Adding Machines, Creating Servers (jVMs), Adding Servers (jVMs)to machines

print('Create host machines of type UnixMachine')

i = 0
k = 1

while i < noOfHosts:
	j = 1
	HOSTMACHINE = HOSTMACHINES[i]
	HOSTIPADD = HOSTMACHINEIPS[i]  
	cd('/')
	create(HOSTMACHINE,'UnixMachine')
	cd('UnixMachine/'+HOSTMACHINE)
	create(HOSTMACHINE,'NodeManager')
	cd('NodeManager/'+HOSTMACHINE)
	set('ListenAddress',HOSTIPADD)
	set( 'NMType', 'SSL' )  
	
	while j <= int(JVMsPerNode):

		print ("Create provdemo_server" + str(k))
		demo_jvm = (prosvr + str(k))
		cd('/')	
		create(demo_jvm, 'Server')
		changeManagedServer(demo_jvm,lport,DEMO_JAVA_ARGUMENTS)
			
		print ("Attaching JVMs to machine: " +HOSTMACHINE)
		cd('/Servers/'+demo_jvm)
		set('Machine',HOSTMACHINE)
			
		# Adding Servers(jvms) to cluster)	
		cd('/')
		assign('Server',demo_jvm,'Cluster','provdemo_cluster')
			
		lport += 2
		k += 1
		j += 1			

	i += 1

#Adding Admin Server  

print 'Change AdminServer'
cd('/Servers/'+ADMIN_SERVER)
set('Machine',ADMIN_HOST_NAME)

updateDomain()
closeDomain();

createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server2/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server3/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server4/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server5/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(DEMO_DOMAIN_HOME+'/servers/provdemo_server6/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

dumpStack();
print('Exiting...')
exit()
