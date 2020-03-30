#! /bin/bash

#set -x

export NODEMGR_HOME={{ COMMON }}/nodemanager
export JAVA_PROPERTIES="-Xms1g -Xmx1g -Xmn512m"
export JAVA_HOME={{ JAVA_HOME }}

function NMscan {
   ps -flu {{ install_user }}  | grep "weblogic.NodeManager" | grep -v "grep" | grep DListenPort={{ OSB_NODEMGR_PORT }} | awk '{print $4}'
}

tries=3
xit=1 # assume an error

trap '' HUP # ignore hangups 

OSB_NM_LOG=$PWD/soanm.out
>| $OSB_NM_LOG # truncate/create
echo "NodeManager log file: $OSB_NM_LOG"
ls -l $OSB_NM_LOG

OSB_NM_PID=$( NMscan )
echo "NodeManager pid is: $OSB_NM_PID"

if [ "$OSB_NM_PID" != "" ]
then echo "NodeManager currently running as PID $OSB_NM_PID"
     echo "Killing it with prejudice"
     kill -KILL $OSB_NM_PID
     sleep 5
fi

echo "NodeManager pid is: $OSB_NM_PID"

echo "NodeManager psten port is: $OSB_NODEMGR_PORT"

cmd="$PWD/startNodeManager.sh $HOSTNAME {{ OSB_NODEMGR_PORT }} >| $OSB_NM_LOG 2>&1 &"
while (( tries-- ))
do OSB_NM_PID=$( NMscan )

echo "NodeManager pid is: $OSB_NM_PID"

   if [[ "$OSB_NM_PID" = "" ]]
   then echo "NodeManager is not running now"
        echo "executing [ $cmd ]" 
        echo "(remaining tries: $tries)"
        eval "$cmd"
        echo "Sleeping for 20s..."
        sleep 20
   else echo "NodeManager is running as PID = $OSB_NM_PID"
        xit=0
        break
   fi

done

echo "NodeManager pid is: $OSB_NM_PID"
echo "NodeManager psten port is: $OSB_NODEMGR_PORT"

echo "Log to this point:"
cat $OSB_NM_LOG

exit $xit # raise an error unless we see it running
