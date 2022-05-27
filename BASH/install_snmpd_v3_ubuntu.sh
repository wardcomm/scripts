#!/bin/bash
#this script has been tested on ubuntu 20.04
#install snmpd
apt update && apt install snmpd snmp libsnmp-de


#make a backup of snmp config file
cp /etc/snmp/snmpd.conf{,.bak}
#Create SNMP v3 Authentication User
net-snmp-create-v3-user -ro -A STrP@SSWRD -a SHA -X STr0ngP@SSWRD -x AES snmpadmin

systemctl start snmpd
systemctl enable snmpd
#verify snmp v3 connection
snmpwalk -v3 -a SHA -A STrP@SSWRD -x AES -X STr0ngP@SSWRD -l authPriv -u snmpadmin localhost | head
#from a remote host would look like this
# snmpwalk -v3 -a SHA -A STrP@SSWRD -x AES -X STr0ngP@SSWRD -l authPriv -u snmpadmin 192.168.58.18 | head
netstat -nlpu|grep snmp