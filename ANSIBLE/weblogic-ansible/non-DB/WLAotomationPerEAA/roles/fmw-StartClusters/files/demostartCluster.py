ASERVER_WPORT   = "{{ DEMO_ADMIN_wPORT }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
DEMO_NODEMGR_PORT    = "{{  DEMO_NODEMGR_PORT }}"
DEMO_DOMAIN_NAME     = "{{  DEMO_DOMAIN_NAME }}"
DEMO_DOMAIN_HOME     = "{{  DEMO_DOMAIN_HOME }}"
DEMO_CLUSTER_NAME    = sys.argv[1]

def StartCluster():
  try:
    connect(WLS_USERNAME, WLS_PASSWORD, "t3://"+ASERVER_WPORT)
    start( DEMO_CLUSTER_NAME,'Cluster')
    disconnect()
  except:
    dumpStack()
    raise

#Starting all Servers in Cluster
StartCluster()
