#!/bin/bash
cd /etc/yum.repos.d
wget http://download.virtualbox.org/virtualbox/rpm/rhel/virtualbox.repo
yum --enablerepo=epel install dkms -y
yum groupinstall "Development Tools" -y
yum install kernel-devel -y
yum install VirtualBox-6.0 -y
