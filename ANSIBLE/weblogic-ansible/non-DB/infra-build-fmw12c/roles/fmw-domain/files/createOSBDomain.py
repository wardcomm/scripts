from sets import Set

#List of Declared Variables passed from Ansible
OSB_WLHOME               = "{{ OSB_WLHOME }}"

OSB_DOMAIN_NAME          =  "{{ OSB_DOMAIN_NAME }}"
OSB_DOMAIN_HOME          =  "{{ OSB_DOMAIN_HOME }}"
OSB_APP_PATH             =  "{{ OSB_APP_PATH }}"

OSB_LOG_FOLDER           = "{{ OSB_LOG_FOLDER }}"
ADMIN_SERVER             = "{{ ADMIN_SERVER }}"
ADMIN_ADDRESS            = "{{ NODE_1 }}"

OSB_MSERVER2_SERVER      = "{{ OSB_MSERVER2_SERVER }}"
OSB_MSERVER3_SERVER      = "{{ OSB_MSERVER3_SERVER }}"

MSERVER2_ADDRESS         = "{{ NODE_2 }}"
MSERVER3_ADDRESS         = "{{ NODE_3 }}"

JSSE_ENABLED             = "{{ JSSE_ENABLED }}"
DEVELOPMENT_MODE         = "{{ DEVELOPMENT_MODE }}"
WEBTIER_ENABLED          = "{{ WEBTIER_ENABLED }}"

ADMIN_SERVER             = "{{ ADMIN_SERVER }}"
ADMIN_USER               = "{{ WLS_USERNAME }}"
ADMIN_PASSWORD           = "{{ WLS_PASSWORD }}"

JAVA_HOME                = "{{ JAVA_HOME }}"

ADM_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+OSB_LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+OSB_LOG_FOLDER+'AdminServer_err.out'
OSB_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1024m '
OSB_JAVA_ARGUMENTS       = '-XX:PermSize=256m -XX:MaxPermSize=752m -Xms1024m -Xmx1532m '

JDBC_URL                 = "{{ JDBC_URL }}"
OSB_REPOS_DBUSER_PREFIX  = "{{ OSB_REPOS_DBUSER_PREFIX }}"
OSB_REPOS_DBPASSWORD     = "{{ OSB_REPOS_DBPASSWORD }}"

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

def changeDatasourceToXA(datasource):
  print 'Change datasource '+datasource
  cd('/')
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
  set('UseXADataSourceInterface','True') 
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
  set('GlobalTransactionsProtocol','TwoPhaseCommit')
  cd('/')

def changeManagedServer(server,port,java_arguments):
  cd('/Servers/'+server)
  #set('Machine'      ,'LocalMachine')
  #set('ListenAddress',ADMIN_ADDRESS)
  #set('ListenPort'   ,port)

  create(server,'ServerStart')
  cd('ServerStart/'+server)
  set('Arguments' , java_arguments+' -Dweblogic.Stdout='+OSB_LOG_FOLDER+server+'.out -Dweblogic.Stderr='+OSB_LOG_FOLDER+server+'_err.out')
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
  set('FileName'     , OSB_LOG_FOLDER+server+'.log')
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
#set('FileName'    ,OSB_LOG_FOLDER+DOMAIN+'.log')
set('FileCount'   ,10)
set('FileMinSize' ,5000)
set('RotationType','byTime')
set('FileTimeSpan',24)

cd('/Servers/AdminServer')
# name of adminserver
set('Name',ADMIN_SERVER )

cd('/Servers/'+ADMIN_SERVER)

# address and port
set('ListenAddress',ADMIN_ADDRESS)
set('ListenPort'   ,11400)

setOption( "AppDir", OSB_APP_PATH )

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
set('FileName'    ,OSB_LOG_FOLDER+ADMIN_SERVER+'.log')
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
writeDomain(OSB_DOMAIN_HOME)
closeTemplate()

createAdminStartupPropertiesFile(OSB_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

#es = encrypt(ADMIN_PASSWORD,OSB_DOMAIN_HOME)

readDomain(OSB_DOMAIN_HOME)

#Avoiding the password Encryortion from Domain Creation
 
#print('set domain password...') 
#cd('/SecurityConfiguration/'+OSB_DOMAIN_NAME)
#set('CredentialEncrypted',es)

#print('Set nodemanager password')
#set('NodeManagerUsername'         ,ADMIN_USER )
#set('NodeManagerPassword'         ,ADMIN_PASSWORD )
#set('NodeManagerPasswordEncrypted',es )

cd('/')

setOption( "AppDir", OSB_APP_PATH )

print 'Adding EM Template'
addTemplate('{{ ORACLE_HOME }}/em/common/templates/wls/oracle.em_wls_template.jar')

dumpStack();

addTemplate('{{ ORACLE_HOME }}/oracle_common/common/templates/wls/oracle.wls-webservice-template.jar')

print 'Adding OSB Template'
addTemplate('{{ ORACLE_HOME }}/osb/common/templates/wls/oracle.osb_template.jar')

print 'Change datasources'

print 'Change datasource LocalScvTblDataSource'
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',JDBC_URL)
set('PasswordEncrypted',OSB_REPOS_DBPASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',OSB_REPOS_DBUSER_PREFIX+'_STB')

print 'Call getDatabaseDefaults which reads the service table'
getDatabaseDefaults()    
dumpStack()

changeDatasourceToXA('wlsbjmsrpDataSource')
changeDatasourceToXA('OraSDPMDataSource')
#changeDatasourceToXA('SOADataSource')

setOption( "AppDir", OSB_APP_PATH )

#Adding Machines

print('Create machine cdpqa05soa01_machine with type UnixMachine')
cd('/')
create('cdpqa05soa01_machine','UnixMachine')
cd('UnixMachine/cdpqa05soa01_machine')
create('cdpqa05soa01_machine','NodeManager')
cd('NodeManager/cdpqa05soa01_machine')
set('ListenAddress',ADMIN_ADDRESS)
set( 'NMType', 'SSL' )

print('Create machine cdpqa05soa02_machine with type UnixMachine')
cd('/')
create('cdpqa05soa02_machine','UnixMachine')
cd('UnixMachine/cdpqa05soa02_machine')
create('cdpqa05soa02_machine','NodeManager')
cd('NodeManager/cdpqa05soa02_machine')
set('ListenAddress',MSERVER2_ADDRESS)
set( 'NMType', 'SSL' )

print('Create machine cdpqa05soa03_machine with type UnixMachine')
cd('/')
create('cdpqa05soa03_machine','UnixMachine')
cd('UnixMachine/cdpqa05soa03_machine')
create('cdpqa05soa03_machine','NodeManager')
cd('NodeManager/cdpqa05soa03_machine')
set('ListenAddress',MSERVER3_ADDRESS)
set( 'NMType', 'SSL' )

print 'Change AdminServer'
cd('/Servers/'+ADMIN_SERVER)
set('Machine','cdpqa05soa01_machine')

#print 'Change AdminServer'
#cd('/Servers/'+OSB_MSERVER2_SERVER)
#set('Machine','cdpqa05soa02_machine')

#print 'Change AdminServer'
#cd('/Servers/'+OSB_MSERVER3_SERVER)
#set('Machine','cdpqa05soa03_machine')

## Adding Servers
print 'Create provosb_cluster'
cd('/')
create('provosb_cluster', 'Cluster')

print 'Create provosb_server1'
cd('/')
create('provosb_server1', 'Server')
changeManagedServer('provosb_server1',11411,OSB_JAVA_ARGUMENTS)

print 'Create provosb_server2'
cd('/')
create('provosb_server2', 'Server')
changeManagedServer('provosb_server2',11412,OSB_JAVA_ARGUMENTS)

print 'Create provosb_server3'
cd('/')
create('provosb_server3', 'Server')
changeManagedServer('provosb_server3',11413,OSB_JAVA_ARGUMENTS)

print 'Create provosb_server4'
cd('/')
create('provosb_server4', 'Server')
changeManagedServer('provosb_server4',11414,OSB_JAVA_ARGUMENTS)

print 'Create provosb_server5'
cd('/')
create('provosb_server5', 'Server')
changeManagedServer('provosb_server5',11415,OSB_JAVA_ARGUMENTS)

print 'Create provosb_server6'
cd('/')
create('provosb_server6', 'Server')
changeManagedServer('provosb_server6',11416,OSB_JAVA_ARGUMENTS)

# Attaching provosb_server1 and provosb_server2 to machine cdpqa05soa01_machine

print 'Change provosb_server1'
cd('/Servers/provosb_server1')
set('Machine','cdpqa05soa01_machine')

print 'Change provosb_server2'
cd('/Servers/provosb_server2')
set('Machine','cdpqa05soa01_machine')

print 'Change provosb_server3'
cd('/Servers/provosb_server3')
set('Machine','cdpqa05soa02_machine')

print 'Change provosb_server4'
cd('/Servers/provosb_server4')
set('Machine','cdpqa05soa02_machine')

print 'Change provosb_server5'
cd('/Servers/provosb_server5')
set('Machine','cdpqa05soa03_machine')

print 'Change provosb_server6'
cd('/Servers/provosb_server6')
set('Machine','cdpqa05soa03_machine')

cd('/')
assign('Server','provosb_server1','Cluster','provosb_cluster')
assign('Server','provosb_server2','Cluster','provosb_cluster')
assign('Server','provosb_server3','Cluster','provosb_cluster')

assign('Server','provosb_server4','Cluster','provosb_cluster')
assign('Server','provosb_server5','Cluster','provosb_cluster')
assign('Server','provosb_server6','Cluster','provosb_cluster')


print 'Add server groups WSM-CACHE-SVR WSMPM-MAN-SVR JRF-MAN-SVR to AdminServer'
serverGroup = ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"]
setServerGroups(ADMIN_SERVER, serverGroup)                      

print 'Add server group OSB-MGD-SVRS-COMBINED to provosb_server1 2 3'
serverGroup = ["OSB-MGD-SVRS-COMBINED"]
setServerGroups('provosb_server1', serverGroup)                      
setServerGroups('provosb_server2', serverGroup)                      
setServerGroups('provosb_server3', serverGroup)

setServerGroups('provosb_server4', serverGroup)
setServerGroups('provosb_server5', serverGroup)
setServerGroups('provosb_server6', serverGroup)

print 'end server groups'

updateDomain()
closeDomain();

createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server2/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server3/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server4/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server5/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(OSB_DOMAIN_HOME+'/servers/provosb_server6/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)


print('Exiting...')
exit()
