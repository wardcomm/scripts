#!/bin/bash

#variables
email="joseph.ward@orhp.com"
#cc1="kyla@orhp.com"
#cc2="chamun@orhp.com"
reply_email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"
source_loc="Applications"
source_dir="/Environments/Production/Lockbox/Transport"
today_date=(`date +%m%d%y`)
email_date=(`date +%B%Y`)
TZ_PST="`TZ='America/Los_Angeles' date`"
TZ_EST="`TZ='America/New_York' date`"
location="//corp.orhp.com/Applications/Environments"
directory="/Production/Lockbox/Transport"
make_dir=(`mkdir -p /IFS`)
# smb_command=('get 060922_Lookup7500.csv; exit')
smb_command=('get $today_file; exit')
smb_user="joward@corp.orhp.com"
file_name="_Lookup7500.csv"
today_file=($today_date"_Lookup7500.csv")
clear
#smbclient //s1-FS02/Environments -c get $today_date* -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport
#\\corp.orhp.com\Applications\Environments\Production\Lockbox\Transport
#smbclient //s1-FS02/Environments -c'get 060922_Lookup7500.csv; exit'  -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport
echo "make dir" && sleep 2
$make_dir
cd $make_dir
echo "smb connection" && sleep 2
smbclient $location -c $smb_command -U $smb_user -m SMB3 -D $directory

#sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
echo "sftp session" && sleep 2
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
echo "email notification" && sleep 2
echo "sftp to cnb on $email_date $TZ_PST" | mailx -s "sftp from cnb on  $TZ_PST"  $email $cc1 $cc2 -r $reply_email.com
# smbclient  '\\corp.orhp.com\' -U joward@corp.orhp.com
#smbclient -L \\s1-fs01\DFS\Departments\IT\chad_testing -U joward@corp.orhp.com
#smbclient   //s1-fs01.corp.orhp.com/Departments/ -U joward@corp.orhp.com -m SMB3
#smbclient //s1-fs01.corp.orhp.com/Departments -U joward@corp.orhp.com -m SMB3 -D IT/chad_testing 
#smbclient //s1-FS02/Environments -U joward@corp.orhp.com -m SMB3 -D /Production/Lockbox/Transport -c get $today_date_Lookup7500 /REPO
#smbclient//s1-fs01.corp.orhp.com/$source_loc -U joward@corp.orhp.com -m SMB3 -D $source_dir
echo $today_date
