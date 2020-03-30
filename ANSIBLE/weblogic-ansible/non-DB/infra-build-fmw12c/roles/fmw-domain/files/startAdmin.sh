DH="{{ DOMAIN_HOME }}"
LOG="{{ DOMAIN_HOME }}/servers/AdminServer/logs/AdminServer.out"
#SOA_USER_MEM_ARGS="-Xms2048m -Xmx2048m -Xmn1024m -XX:PermSize=1024m -XX:MaxPermSize=1024m"
pid=`ps -elf | grep "Dweblogic.Name=SoaAdmin" | grep -v "grep" | grep $DH | awk '{print $4}'`

if [ "$PID" = "" ]
then
 echo "Starting SoaAdmin..."
 cd $DH
 nohup ./startWebLogic.sh >| $LOG 2>&1 &
 echo "Server Outfile = $LOG"
 echo "Sleeping for 60s"
 sleep 60
else
 echo "SoaAdmin is already running at PID = $pid"
fi
