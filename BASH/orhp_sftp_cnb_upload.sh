#!/bin/bash
email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"

#sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb
echo "sftp from cnb on" 'date +"%B %Y' | mailx -s "sftp from cnb on 'date' "  $email
# smbclient  '\\corp.orhp.com\' -U joward@corp.orhp.com
smbclient -L \\s1-fs01\DFS\Departments\IT\chad_testing -U joward@corp.orhp.com
smbclient   //s1-fs01.corp.orhp.com/Departments/ -U joward@corp.orhp.com -m SMB3
smbclient //s1-fs01.corp.orhp.com/Departments -U joward@corp.orhp.com -m SMB3 -D IT/chad_testing

