#!/bin/bash
# wget http://people.canonical.com/~bjoern/snappy/libreoffice_5.2.0.0.beta2_amd64.snap{,.sha512sum}
# sha512sum -c libreoffice_5.2.0.0.beta2_amd64.snap.sha512sum && sudo snap install --devmode libreoffice_5.2.0.0.beta2_amd64.snap
# /snap/bin/libreoffice

# wget https://www.libreoffice.org/donate/dl/rpm-x86_64/6.2.4/en-US/LibreOffice_6.2.4_Linux_x86-64_rpm.tar.gz -P /tmp
# # sudo su -
# tar xvf /tmp/LibreOffice_6.2.4_Linux_x86-64_rpm.tar.gz
# yum install /tmp/LibreOffice_6.2.4_Linux_x86-64_rpm
# rm -rf /tmp/LibreOffice*
# ls -al /tmp/Lib*
sudo snap install libreoffice