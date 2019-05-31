#!/bin/bash
#uncomment if you want most current
#ver=0.12.0
ver=0.11.14
prog=terraform_$ver_linux_amd64.zip
#wget -q https://releases.hashicorp.com/terraform/0.12.0-rc1/terraform_0.12.0-rc1_linux_amd64.zip
#comment out this one if you want to run most current
# wget -q https://releases.hashicorp.com/terraform/0.11.13/$prog
wget -q https://releases.hashicorp.com/terraform/$ver/$prog
#unzip terraform_0.12.0-rc1_linux_amd64.zip
unzip terraform_$ver_linux_amd64.zip
mv -f terraform /usr/local/bin/terraform
terraform version
rm -rf terraform*