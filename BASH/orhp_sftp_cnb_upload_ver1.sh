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

# smb_command=('get 060922_Lookup7500.csv; exit')
smb_command=('get $today_file; exit')
smb_user="svc_cnb_sftp@corp.orhp.com"
file_name="_Lookup7500.csv"
today_file=(/IFS/transport/$today_date"_Lookup7500.csv")

make_dir=(`mkdir -p /IFS`)
make_transport=(`mkdir -p /IFS/transport`)
make_archive=(`mkdir -p /IFS/archive`)
today_archive=(/IFS/archive/$today_date"_Lookup7500.csv")

#code
$make_dir
$make_archive
cd /IFS/transport
#echo debug area

echo "============================="
echo " today_file $today_file"
echo "today_archive $today_archive"

echo "============================="

if [[ -e "$today_archive" ]]; then
echo "file exists"
else
smbclient $location -c "get $today_file; exit" -U $smb_user -m SMB3 -D $directory
cd /IFS/transport
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch_upload.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
cp $today_file archive
###EMAIL SECTION
echo "SFTP TRANSFER TO CNB
__________________________
$email_date
$today_file
$TZ_PST
__________________________" | mailx -s "sftp from cnb on  $TZ_PST"  $email $cc1 $cc2 -r $reply_email
fi

# function clean() {
#     rm -rf /IFS/transport/*
# }
#  clean

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



