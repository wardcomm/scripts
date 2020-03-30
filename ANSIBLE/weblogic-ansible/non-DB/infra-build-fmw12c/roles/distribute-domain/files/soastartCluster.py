ASERVER_WPORT   = "{{ SOA_ADMIN_wPORT }}"
WLS_USERNAME    = "{{ WLS_USERNAME }}"
WLS_PASSWORD    = "{{ WLS_PASSWORD }}"
SOA_NODEMGR_PORT    = "{{ SOA_NODEMGR_PORT }}"
SOA_DOMAIN_NAME     = "{{ SOA_DOMAIN_NAME }}"
SOA_DOMAIN_HOME     = "{{ SOA_DOMAIN_HOME }}"
SOA_CLUSTER_NAME    = sys.argv[1]

def StartCluster():
  try:
    connect(WLS_USERNAME, WLS_PASSWORD, "t3://"+ASERVER_WPORT)
    start(SOA_CLUSTER_NAME,'Cluster')
    disconnect()
  except:
    dumpStack()
    raise

#Starting all Servers in Cluster
StartCluster()
