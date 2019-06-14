#!/bin/bash
terraform version
mkdir -p /opt/terraform/
INSTALL_DIR="${1:-/opt/terraform}"
URL="https://releases.hashicorp.com/terraform"

VER="$(curl -sL $URL | grep -v beta | grep -Po "_(\d*\.?){3}" | sed 's/_//' | sort -V | tail -1)"
ZIP="terraform_${VER}_linux_amd64.zip"

echo "* Downloading ${URL}/${VER}/terraform_${VER}_linux_amd64.zip"
curl -s ${URL}/${VER}/terraform_${VER}_linux_amd64.zip -o ${INSTALL_DIR}/${ZIP}
echo "* Extracting $ZIP into $INSTALL_DIR"
unzip -o ${INSTALL_DIR}/$ZIP -d $INSTALL_DIR && rm -v ${INSTALL_DIR}/$ZIP
rm -rf /root/bin/terraform
mv /opt/terraform/terraform /root/bin/terraform
terraform version
