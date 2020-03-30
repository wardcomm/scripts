from sets import Set

#List of Declared Variables passed from Ansible

SOA_WLHOME                =  "{{ SOA_WLHOME }}"

SOA_DOMAIN_NAME           =  "{{ SOA_DOMAIN_NAME }}"
SOA_DOMAIN_HOME           =  "{{ SOA_DOMAIN_HOME }}"
SOA_APP_PATH              =  "{{ SOA_APP_PATH }}"

SOA_LOG_FOLDER            =  "{{ SOA_LOG_FOLDER }}"

ADMIN_SERVER              =  "{{ ADMIN_SERVER }}"
ADMIN_ADDRESS             =  "{{ NODE_1 }}"
SOA_NODEMGR_PORT          =  "{{ SOA_NODEMGR_PORT }}" 

SOA_MSERVER2_SERVER       =  "{{ SOA_MSERVER2_SERVER }}"
SOA_MSERVER3_SERVER       =  "{{ SOA_MSERVER3_SERVER }}"

MSERVER2_ADDRESS          =  "{{ NODE_2 }}"
MSERVER3_ADDRESS          =  "{{ NODE_3 }}"

JSSE_ENABLED              =  "{{ JSSE_ENABLED }}"
DEVELOPMENT_MODE          =  "{{ DEVELOPMENT_MODE }}"
WEBTIER_ENABLED           =  "{{ WEBTIER_ENABLED }}"


ADMIN_SERVER              =  "{{ ADMIN_SERVER }}"
ADMIN_USER                =  "{{ WLS_USERNAME }}"
ADMIN_PASSWORD            =  "{{ WLS_PASSWORD }}"

JAVA_HOME                 =  "{{ JAVA_HOME }}"

ADM_JAVA_ARGUMENTS        = '-XX:PermSize=256m -XX:MaxPermSize=512m -Xms1024m -Xmx1532m -Dweblogic.Stdout='+SOA_LOG_FOLDER+'AdminServer.out -Dweblogic.Stderr='+SOA_LOG_FOLDER+'AdminServer_err.out'
SOA_JAVA_ARGUMENTS        = '-XX:PermSize=256m -XX:MaxPermSize=752m -Xms1024m -Xmx1532m '

JDBC_URL                  = "{{ JDBC_URL }}"
SOA_REPOS_DBUSER_PREFIX   = "{{ SOA_REPOS_DBUSER_PREFIX }}"
SOA_REPOS_DBPASSWORD      = "{{ SOA_REPOS_DBPASSWORD }}"

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
  #set('Machine'      ,'cdpqa05soa01_machine')
  #set('ListenAddress',ADMIN_ADDRESS)
  set('ListenPort'   ,port)

  create(server,'ServerStart')
  cd('ServerStart/'+server)
  set('Arguments' , java_arguments+' -Dweblogic.Stdout='+SOA_LOG_FOLDER+server+'.out -Dweblogic.Stderr='+SOA_LOG_FOLDER+server+'_err.out')
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
  set('FileName'     , SOA_LOG_FOLDER+server+'.log')
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
#set('FileName'    ,SOA_LOG_FOLDER+DOMAIN+'.log')
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
set('ListenPort'   ,5081)

setOption( "AppDir", SOA_APP_PATH )

create(ADMIN_SERVER,'ServerStart')
cd('ServerStart/'+ADMIN_SERVER)
#set('Arguments' , ADM_JAVA_ARGUMENTS)
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
set('FileName'    ,SOA_LOG_FOLDER+ADMIN_SERVER+'.log')
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
writeDomain(SOA_DOMAIN_HOME)
closeTemplate()

createAdminStartupPropertiesFile(SOA_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/data/nodemanager',ADM_JAVA_ARGUMENTS)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/'+ADMIN_SERVER+'/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/config/nodemanager','nm_password.properties',ADMIN_USER,ADMIN_PASSWORD)

#Avoiding the password Encryortion from Domain Creation

#es = encrypt(ADMIN_PASSWORD,SOA_DOMAIN_HOME)

readDomain(SOA_DOMAIN_HOME)

#print('set domain password...') 
#cd('/SecurityConfiguration/'+SOA_DOMAIN_NAME)
#set('CredentialEncrypted',es)

#print('Set nodemanager password')
#set('NodeManagerUsername'         ,ADMIN_USER )
#set('NodeManagerPasswordEncrypted',es )

cd('/')

setOption( "AppDir", SOA_APP_PATH )

addTemplate('{{ ORACLE_HOME }}/oracle_common/common/templates/wls/oracle.wls-webservice-template.jar')

print 'Adding ApplCore Template'
addTemplate('{{ ORACLE_HOME }}/oracle_common/common/templates/wls/oracle.applcore.model.stub_template.jar')

print 'Adding SOA Template'
addTemplate('{{ ORACLE_HOME }}/soa/common/templates/wls/oracle.soa_template.jar')

dumpStack()

print 'Change datasources'

print 'Change datasource LocalScvTblDataSource'
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL',JDBC_URL)
set('PasswordEncrypted',SOA_REPOS_DBPASSWORD)
cd('Properties/NO_NAME_0/Property/user')
set('Value',SOA_REPOS_DBUSER_PREFIX+'_STB')

print 'Call getDatabaseDefaults which reads the service table'
getDatabaseDefaults()    
dumpStack()

changeDatasourceToXA('EDNDataSource')
changeDatasourceToXA('OraSDPMDataSource')
changeDatasourceToXA('SOADataSource')

setOption( "AppDir", SOA_APP_PATH )

#Adding Machines

print('Create machine cdpqa05soa01_machine with type UnixMachine')
cd('/')
create('cdpqa05soa01_machine','UnixMachine')
cd('UnixMachine/cdpqa05soa01_machine')
create('cdpqa05soa01_machine','NodeManager')
cd('NodeManager/cdpqa05soa01_machine')
set('ListenAddress',ADMIN_ADDRESS)
#set('ListenPort',SOA_NODEMGR_PORT)
set('ListenPort'   ,5558)
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

#print 'Change provsoa_server2'
#cd('/Servers/'+SOA_MSERVER2_SERVER)
#set('Machine','cdpqa05soa02_machine')

#print 'Change provsoa_server3'
#cd('/Servers/'+SOA_MSERVER3_SERVER)
#set('Machine','cdpqa05soa03_machine')

### Server Creation 
print 'Create provsoa_cluster'
cd('/')
create('provsoa_cluster', 'Cluster')

print 'Create provsoa_server1'
cd('/')
create('provsoa_server1', 'Server')
changeManagedServer('provsoa_server1',7002,SOA_JAVA_ARGUMENTS)

print 'Create provsoa_server2'
cd('/')
create('provsoa_server2', 'Server')
changeManagedServer('provsoa_server2',7010,SOA_JAVA_ARGUMENTS)

print 'Create provsoa_server3'
cd('/')
create('provsoa_server3', 'Server')
changeManagedServer('provsoa_server3',7011,SOA_JAVA_ARGUMENTS)

print 'Create provsoa_server4'
cd('/')
create('provsoa_server4', 'Server')
changeManagedServer('provsoa_server4',7012,SOA_JAVA_ARGUMENTS)

print 'Create provsoa_server5'
cd('/')
create('provsoa_server5', 'Server')
changeManagedServer('provsoa_server5',7013,SOA_JAVA_ARGUMENTS)

print 'Create provsoa_server6'
cd('/')
create('provsoa_server6', 'Server')
changeManagedServer('provsoa_server6',7014,SOA_JAVA_ARGUMENTS)

# Attaching provsoa_server1 and provsoa_server2 to machine cdpqa05soa01_machine

print 'Change provsoa_server1'
cd('/Servers/provsoa_server1')
set('Machine','cdpqa05soa01_machine')

print 'Change provsoa_server2'
cd('/Servers/provsoa_server2')
set('Machine','cdpqa05soa01_machine')

print 'Change provsoa_server3'
cd('/Servers/provsoa_server3')
set('Machine','cdpqa05soa02_machine')

print 'Change provsoa_server4'
cd('/Servers/provsoa_server4')
set('Machine','cdpqa05soa02_machine')

print 'Change provsoa_server5'
cd('/Servers/provsoa_server5')
set('Machine','cdpqa05soa03_machine')

print 'Change provsoa_server6'
cd('/Servers/provsoa_server6')
set('Machine','cdpqa05soa03_machine')

cd('/')
assign('Server','provsoa_server1','Cluster','provsoa_cluster')
assign('Server','provsoa_server2','Cluster','provsoa_cluster')
assign('Server','provsoa_server3','Cluster','provsoa_cluster')
assign('Server','provsoa_server4','Cluster','provsoa_cluster')
assign('Server','provsoa_server5','Cluster','provsoa_cluster')
assign('Server','provsoa_server6','Cluster','provsoa_cluster')

print 'Add server groups WSM-CACHE-SVR WSMPM-MAN-SVR JRF-MAN-SVR to AdminServer'
serverGroup = ["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"]
setServerGroups(ADMIN_SERVER, serverGroup)                      

print 'Add server group SOA-MGD-SVRS to SoaServer1 2 3 4 5 6'
serverGroup = ["SOA-MGD-SVRS"]
setServerGroups('provsoa_server1', serverGroup)                      
setServerGroups('provsoa_server2', serverGroup)                      
setServerGroups('provsoa_server3', serverGroup)
setServerGroups('provsoa_server4', serverGroup)
setServerGroups('provsoa_server5', serverGroup)
setServerGroups('provsoa_server6', serverGroup)


print 'end server groups'

updateDomain()
dumpStack();
closeDomain();

createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server1/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server2/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server3/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server4/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server5/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)
createBootPropertiesFile(SOA_DOMAIN_HOME+'/servers/provsoa_server6/security','boot.properties',ADMIN_USER,ADMIN_PASSWORD)

print('Exiting...')
exit()
