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
file2test=(`echo $today_file | cut -c -6`)
nameoffile=(`ls -lA /IFS | awk '{print $9}'`)
TZ_PST="`TZ='America/Los_Angeles' date`"
TZ_EST="`TZ='America/New_York' date`"
location="//corp.orhp.com/Applications/Environments"
directory="/Production/Lockbox/Transport"
make_dir=(`mkdir -p /IFS`)
# smb_command=('get 060922_Lookup7500.csv; exit')
smb_command=('get $today_file; exit')
smb_user="svc_cnb_sftp@corp.orhp.com"
file_name="_Lookup7500.csv"
today_file=($today_date"_Lookup7500.csv")
today_date=()
make_archive=(`mkdir -p /IFS/archive`)
today_archive=(/IFS/archive/$today_date"_Lookup7500.csv")

#code
$make_dir
$make_archive
cd /IFS
smbclient $location -c "get $today_file; exit" -U $smb_user -m SMB3 -D $directory
mkdir -p /IFS/mount
sshfs -o allow_other,IdentityFile=/REPO/cnb_private.key oldrepub@mway.cnb.com:/oldrepub.tocnb:downloaded /IFS/mount
cd /IFS
cp -r $today_file /IFS/mount
cp -r $today_file /IFS/archive 
tree /IFS
umount /IFS/mount
tree /IFS 
# sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch_upload.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
$today_file" | mailx -s "sftp from cnb on  $TZ_PST"  $email $cc1 $cc2 -r $reply_email
cp $today_file archive

# #cp $today_file archive
# if [[ -e "$today_archive" ]]; then
# echo "file exists"
# sleep 4
# fi
# exit 0
# cp $today_file archive
# cd /IFS
# sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
# $today_file" | mailx -s "sftp from cnb on  $TZ_PST"  $email $cc1 $cc2 -r $reply_email



