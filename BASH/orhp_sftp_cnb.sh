#!/bin/bash
email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"
reply_email="joseph.ward@orhp.com"
subject="sftp from cnb on `date`" 
body="SFTP from cnb on `date +%B %Y`"

#sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb
echo "$body" | mailx -s "$subject"  $email -r "$reply_email"
