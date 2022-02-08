#!/bin/bash
mkdir -p /SRE
uname -a
tail /var/log/messages
date
uname -a
htop
ethtool eth0
dmidecode --type memory
ps -ef
top
df -h
df -i
iostat -xz 1
dmesg | tail
dmesg | tail -f /var/log/syslog
dmesg | tail -f /var/log/dmesg
sudo find /var/log -type f -mtime -1 -exec tail -Fn0 {} +