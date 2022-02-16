#!/bin/bash
#echo "Server Name, Security Errata,Bugfix,Enhancement" > /SRE/scripts/sec-up.csv
email="joseph.c.ward@charter.com"
hostname="$(hostnamectl |grep 'Static hostname' | awk '{print $3}')"
# hostname=$hostname
server=$hostname
#   date=$(date +"%B %Y)
mkdir -p /SRE/scripts
mkdir -p /SRE/reports
touch /SRE/reports/sec-up.csv
touch /SRE/reports/labels.csv
touch /SRE/reports/sec-combo.csv

sec=`yum updateinfo summary | grep 'Security' | grep -v 'Important|Moderate' | tail -1 | awk '{print $1}'`
bug=`yum updateinfo summary | grep 'Bugfix' | tail -1 | awk '{print $1}'`
enhance=`yum updateinfo summary | grep 'Enhancement' | tail -1 | awk '{print $1}'`
uptime=`uptime -p`
env=`echo "${HOSTNAME: -3}" | cut -c -1`
echo "Server Name,    Security Errata,        Bugfix,       Enhancement,        uptime,            Environment" > /SRE/reports/labels.csv
echo $hostname,"       security"   $sec,   "   Bug"   $bug,"    enhancement"   $enhance ,"      uptime "$uptime,"    Environment" $env >> /SRE/reports/sec-combo.csv
echo $hostname, $sec, $bug,$enhance ,$uptime, $env > /SRE/reports/security_data.csv


echo "Patching Report for `date +"%B %Y"`" | mailx   -s "Patching Report on `date`" -a /SRE/reports/securit_data.csv joseph.c.ward@charter.com #$email
    
clear
ls -al /SRE/reports/
cat /SRE/reports/sec-up.csv
cat /SRE/reports/security_data.csv
cat /SRE/reports/labels.csv
cat /SRE/reports/sec-combo.csv
rm /SRE/reports/sec-up.csv
rm /SRE/reports/security_data.csv
rm /SRE/reports/labels.csv
rm /SRE/reports/sec-combo.csv
#  done
    #  echo "Patching Report `date +"%B %Y"` | mailx -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv $email
    #  echo "Patching Report for `date +"%B %Y"`" | mailx -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv $email
