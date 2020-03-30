#! /bin/bash

#set -x

export NODEMGR_HOME={{ COMMON }}/nodemanager
export JAVA_PROPERTIES="-Xms1g -Xmx1g -Xmn512m"
export JAVA_HOME={{ JAVA_HOME }}

function NMscan {
   ps -flu {{ install_user }}  | grep "weblogic.NodeManager" | grep -v "grep" | grep DListenPort={{ SOA_NODEMGR_PORT }} | awk '{print $4}'
}

tries=3
xit=1 # assume an error

trap '' HUP # ignore hangups 

SOA_NM_LOG=$PWD/soanm.out
>| $SOA_NM_LOG # truncate/create
echo "NodeManager log file: $SOA_NM_LOG"
ls -l $SOA_NM_LOG

NM_PID=$( NMscan )

echo "NM PID is : $NM_PID" 

if [ "$NM_PID" != "" ]
then echo "NodeManager currently running as PID $NM_PID"
     echo "Killing it with prejudice"
     kill -KILL $NM_PID
     sleep 5
fi

echo "SOA NM POrt is: $SOA_NODEMGR_PORT:"

cmd="$PWD/startNodeManager.sh $HOSTNAME {{ SOA_NODEMGR_PORT }} >| $SOA_NM_LOG 2>&1 &"
while (( tries-- ))
do NM_PID=$( NMscan )

echo "NM PID is : $NM_PID" 

   if [[ "$NM_PID" = "" ]]
   then echo "NodeManager is not running now"
        echo "executing [ $cmd ]" 
        echo "(remaining tries: $tries)"
        eval "$cmd"
        echo "Sleeping for 20s..."
        sleep 20
   else echo "NodeManager is running as PID = $NM_PID"
        xit=0
        break
   fi

done

echo "NM PID is : $NM_PID" 

echo "SOA NM POrt is: $SOA_NODEMGR_PORT:"

echo "Log to this point:"
cat $SOA_NM_LOG

exit $xit # raise an error unless we see it running
