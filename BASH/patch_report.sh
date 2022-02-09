      #!/bin/bash
      #echo "Server Name, Security Errata,Bugfix,Enhancement" > /SRE/scripts/sec-up.csv
email="joseph.c.ward@charter.com"
hostname="$(hostnamectl |grep 'Static hostname' | awk '{print $3}')"
      # hostname=$hostname
server=$hostname
    #   date=$(date +"%B %Y)
mkdir -p /SRE/scripts
touch /SRE/scripts/sec-up.csv
echo "Server Name, Security Errata,Bugfix,Enhancement" > /SRE/scripts/sec-up.csv
    #  for server in $hostname
    #  do
    #  server=`$server`
sec=`yum updateinfo summary | grep 'Security' | grep -v 'Important|Moderate' | tail -1 | awk '{print $1}'`
bug=`yum updateinfo summary | grep 'Bugfix' | tail -1 | awk '{print $1}'`
enhance=`yum updateinfo summary | grep 'Enhancement' | tail -1 | awk '{print $1}'`
echo $hostname,"    security"   $sec,   "   Bug"   $bug,"    enhancement"   $enhance >> /SRE/scripts/sec-up.csv
echo "Patching Report for `date +"%B %Y"`" | mailx   -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv joseph.c.ward@charter.com #$email
    
clear
cat /SRE/scripts/sec-up.csv
# rm /SRE/scripts/sec-up.csv
    #  done
    #  echo "Patching Report `date +"%B %Y"` | mailx -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv $email
    #  echo "Patching Report for `date +"%B %Y"`" | mailx -s "Patching Report on `date`" -a /SRE/scripts/sec-up.csv $email
