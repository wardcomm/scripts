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
TZ_UTC="`TZ='UTC' date`"
location="//corp.orhp.com/Applications/Environments"
directory="

# smb_command=('get 060922_Lookup7500.csv; exit')
smb_command=('get $today_file; exit')
smb_user="svc_cnb_sftp@corp.orhp.com"
file_name="_Lookup7500.csv"

today_date=(`date +%m%d5y`)
today_file_location=(/IFS/transport/$today_date"_Lookup7500.csv")
today_file=($today_date"_Lookup7500.csv")
today_archive=(/IFS/archive/$today_date"_Lookup7500.csv")
today_archive_location=(/IFS/archive/$today_date"_Lookup7500.csv")
# today_archive_location=/IFS/archive
make_dir=(`mkdir -p /IFS`)
make_transport=(`mkdir -p /IFS/transport`)
make_archive=(`mkdir -p /IFS/archive`)

list_IFS="$(ls -al /IFS)"

clear

#echo debug area
echo "                             "
echo "============================="
echo "Today_file $today_file"
echo "Today_file location $today_file_location"
echo "Today_archive $today_archive"
echo "Today_archive_location $today_archive_location"
echo "Today Date UTC         $TZ_UTC"
echo "The Tree of IFS $tree_IFS"
echo "The smb user $smb_user"
echo "The location $location"
echo "The directory $directory"
echo "============================="
echo "                             "
#code
$make_dir
$make_transport
$make_archive
cd /IFS/transport
smbclient $location -c "get $today_file; exit" -U $smb_user -m SMB3 -D $directory
#smbclient "//corp.orhp.com/Applications/Environments" -c "get $today_file; exit" -U svc_cnb_sftp@corp.orhp.com -m SMB3 -D "/Production/Lockbox/Transport"

if [[ -e "$today_archive_location" ]]; then
echo "file exists"
else

cd /IFS/transport
sftp -b /REPO/scripts/BATCH/orhp_cnb_sftp_batch_upload.bat  -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.tocnb
cp $today_file_location  $today_archive_location
###EMAIL SECTION
echo "SFTP TRANSFER TO CNB
__________________________
$email_date
$today_file

$TZ_PST
$TZ_EST
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



