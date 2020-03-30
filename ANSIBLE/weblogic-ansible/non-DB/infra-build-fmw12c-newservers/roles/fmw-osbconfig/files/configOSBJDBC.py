OSB_ADMIN_wPORT     = "{{ OSB_ADMIN_wPORT }}"
WLS_USERNAME        = "{{ WLS_USERNAME }}"
WLS_PASSWORD        = "{{ WLS_PASSWORD }}"

OSB_SCHEMA_PREFIX   = "{{ OSB_SCHEMA_PREFIX }}"
OSB_SCHEMA_PREFIX   = "{{ OSB_SCHEMA_PREFIX }}"
JDBC_URL            = "{{ JDBC_URL }}"

PROPERTIES_FILE     = "{{ STAGE_DIR }}/OSB_JDBC.properties"

#Loading Properties

jdbcProps = Properties()
jdbcProps.load(FileInputStream(PROPERTIES_FILE))

def createDS( index ):
 dsName       = jdbcProps.get("JDBC_NAME."+index)
 dsJndi       = "jdbc/"+dsName                               # jdbcProps.get("JDBC_JNDI."+index)
 dsDriver     = "oracle.jdbc.OracleDriver"                   # jdbcProps.get("JDBC_DRIVER."+index)
 dsUrl        = "{{ JDBC_URL }}"                             # jdbcProps.get("JDBC_URL."+index)
 dsUser       = "{{ DB_USER }}"                              # jdbcProps.get("JDBC_USERNAME."+index)
 dsPass       = "{{ OSB_SCHEMA_PREFIX }}"                      # jdbcProps.get("JDBC_PASSWORD."+index)
 dsTarget     = "SoaCluster"                                 # jdbcProps.get("JDBC_TARGET."+index)
 dsTargetType = "Cluster"                                    # jdbcProps.get("JDBC_TARGET_TYPE."+index)
# dsMin        = jdbcProps.get("JDBC_MIN."+index)
# dsMax        = jdbcProps.get("JDBC_MAX."+index)
# dsInit       = jdbcProps.get("JDBC_INIT."+index)

 cd('/')
 cmo.createJDBCSystemResource(dsName)
 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
 cmo.setName(dsName)

 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
 set('JNDINames',jarray.array([String( dsJndi )], String))

 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
 cmo.setUrl(dsUrl)
 cmo.setDriverName( dsDriver)
 cmo.setPassword(dsPass)

 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
 cmo.createProperty('user')
 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
 cmo.setValue(dsUser)

 cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
 set('MinCapacity', 0 ) # int(dsMin))
 set('MaxCapacity', 1 ) # int(dsMax))
 set('InitialCapacity', 0 ) # int(dsInit))

 cd('/SystemResources/' + dsName )
 set('Targets',jarray.array([ObjectName('com.bea:Name=' + dsTarget + ',Type='+dsTargetType)], ObjectName))


#Looping through properties
try:

 connect(WLS_USERNAME,WLS_PASSWORD,"t3://"+OSB_ADMIN_wPORT)
 edit()
 startEdit()

 TOTAL_DS = jdbcProps.get("TOTAL_DS")

 for i in range(1,int(TOTAL_DS)+1):
  try:
   createDS(str(i))
  except:
   dumpStack()
   pass

 save()
 activate(block="true")
 disconnect()

except:
 dumpStack()
 pass

