# #!/bin/bash
# #uncomment if you want most current
# #ver=0.12.0
# clear
# version = "0.11.14"
# echo $version
# prog="terraform_$version.zip"
# url="https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip"
# echo $ver $prog $url
# # https://releases.hashicorp.com/terraform/$ver/$prog /tmp
# # https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip
# #wget -q https://releases.hashicorp.com/terraform/0.12.0-rc1/terraform_0.12.0-rc1_linux_amd64.zip
# #comment out this one if you want to run most current
# # wget -q https://releases.hashicorp.com/terraform/0.11.13/$prog
# # wget -q https://releases.hashicorp.com/terraform/$ver/$prog /tmp
# # wget -q https://releases.hashicorp.com/terraform/0.12.0/terraform_0.12.0_linux_amd64.zip
# wget -q $url /tmp
# ls -al /tmp terr*
# #unzip terraform_0.12.0-rc1_linux_amd64.zip
# unzip /tmp/$prog
# mv -f terraform /usr/local/bin/terraform
# terraform version
# rm -rf terraform*

#!/bin/bash

function terraform-install() {
  [[ -f ${HOME}/bin/terraform ]] && echo "`${HOME}/bin/terraform version` already installed at ${HOME}/bin/terraform" && return 0
  LATEST_URL=$(curl -sL https://releases.hashicorp.com/terraform/index.json | jq -r '.versions[].builds[].url' | sort -t. -k 1,1n -k 2,2n -k 3,3n -k 4,4n | egrep -v 'rc|beta' | egrep 'linux.*amd64' |tail -1)
  curl ${LATEST_URL} > /tmp/terraform.zip
  mkdir -p ${HOME}/bin
  (cd ${HOME}/bin && unzip /tmp/terraform.zip)
  if [[ -z $(grep 'export PATH=${HOME}/bin:${PATH}' ~/.bashrc) ]]; then
  	echo 'export PATH=${HOME}/bin:${PATH}' >> ~/.bashrc
  fi
  rm -rf /tmp/terra*
  echo "Installed: `${HOME}/bin/terraform version`"
  
  cat - << EOF 
 
Run the following to reload your PATH with terraform:
  source ~/.bashrc
EOF
}

terraform-install