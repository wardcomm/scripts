#!/bin/bash
wget -q https://releases.hashicorp.com/terraform/0.12.0-rc1/terraform_0.12.0-rc1_linux_amd64.zip
unzip terraform_0.12.0-rc1_linux_amd64.zip
mv terraform /usr/local/bin/terraform
terraform version