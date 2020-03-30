
# clusterData    = [ {% for item in clusterData %} "{{ item }}", {% endfor %} ] 

try:
   connect('{{ WLS_USERNAME }}', '{{ WLS_PASSWORD }}', "t3://{{ ADMIN_wPORT }}" )
   for c in cmo.getClusters() :
     n=c.getName()
     start( n,'Cluster')
     state( n,'Cluster')
   disconnect()
except:
  dumpStack()
  raise

