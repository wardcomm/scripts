ASERVER_WPORT   = "{{ OSB_ADMIN_wPORT }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
OSB_NODEMGR_PORT    = "{{ OSB_NODEMGR_PORT }}"
OSB_DOMAIN_NAME     = "{{ OSB_DOMAIN_NAME }}"
OSB_DOMAIN_HOME     = "{{ OSB_DOMAIN_HOME }}"
OSB_CLUSTER_NAME    = sys.argv[1]

def StartCluster():
  try:
    connect(WLS_USERNAME, WLS_PASSWORD, "t3://"+ASERVER_WPORT)
    start(OSB_CLUSTER_NAME,'Cluster')
    disconnect()
  except:
    dumpStack()
    raise

#Starting all Servers in Cluster
StartCluster()
