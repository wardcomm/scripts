#!/bin/bash
email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"
reply_email="joseph.ward@orhp.com"
the_date="`date +"%B %d %Y"`"
hmmmm="`TZ='America/Los_Angeles' date +"%B %d %Y"`"
TZ_PST="`TZ='America/Los_Angeles' date`"
TZ_EST="`TZ='America/New_York' date`"
subject="sftp from cnb on  $TZ_PST"
#data_file="`touch /tmp/data_file`" 
#report=" `echo '$subject $the_date' > '$data_file'`"


echo $TZ_PST
echo $TZ_EST
#subject="sftp from cnb on `$date`"

body="SFTP from cnb on $TZ_PST"
#body="SFTP from cnb on `$date`"

testing="`cat /etc/hosts`"
#the_date="`date +%B %Y`"
attachment="orhp_sftp_cnb.sh"
#wow="`cat  $data_file`"
#echo $the_date > $data_file

#sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb
echo "$body" | mailx -s "$subject"  "$email" -r "$reply_email" # -a "$testing" 
