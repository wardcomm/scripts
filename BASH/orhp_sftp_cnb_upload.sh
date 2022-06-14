#!/bin/bash
email="joseph.ward@orhp.com"
#cc1="kyla@orhp.com"
#cc2="chamun@orhp.com"
reply_email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"
source_loc="Applications"
source_dir="/Environments/Production/Lockbox/Transport"
today_date=(date +%m%d%y)
email_date=(date +%B%Y)
TZ_PST="`TZ='America/Los_Angeles' date`"
TZ_EST="`TZ='America/New_York' date`"
clear
#smbclient //s1-FS02/Environments -c get $today_date* -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport
smbclient //s1-FS02/Environments -c'get 060922_Lookup7500.csv; exit'  -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport
#sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
echo "sftp to cnb on $email_date $TZ_PST" | mailx -s "sftp from cnb on  $TZ_PST"  $email $cc1 $cc2 -r $reply_email.com
# smbclient  '\\corp.orhp.com\' -U joward@corp.orhp.com
#smbclient -L \\s1-fs01\DFS\Departments\IT\chad_testing -U joward@corp.orhp.com
#smbclient   //s1-fs01.corp.orhp.com/Departments/ -U joward@corp.orhp.com -m SMB3
#smbclient //s1-fs01.corp.orhp.com/Departments -U joward@corp.orhp.com -m SMB3 -D IT/chad_testing 
#smbclient //s1-FS02/Environments -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport -c get $today_date_Lookup7500 /REPO
#smbclient//s1-fs01.corp.orhp.com/$source_loc -U joward@corp.orhp.com -m SMB3 -D $source_dir
echo $today_date
