#!/bin/bash
#echo "Server Name, Security Errata,Bugfix,Enhancement" > /SRE/scripts/sec-up.csv
email=joseph.c.ward@charter.com
hostame='hostname'
mkdir -p /SRE/scripts
touch /SRE/scripts/sec-up.csv
echo "Server Name, Security Errata,Bugfix,Enhancement" > /SRE/scripts/sec-up.csv
for server in $hostname
do
sec=`$server yum updateinfo summary | grep 'Security' | grep -v 'Important|Moderate' | tail -1 | awk '{print $1}'`
bug=`$server yum updateinfo summary | grep 'Bugfix' | tail -1 | awk '{print $1}'`
enhance=`$server yum updateinfo summary | grep 'Enhancement' | tail -1 | awk '{print $1}'`
echo "$server,$sec,$bug,$enhance" >> /SRE/scripts/sec-up.csv
done
echo "Patching Report for `date +"%B %Y"`" | mailx -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv $email
# rm /SRE/scripts/sec-up.csv