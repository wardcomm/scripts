#!/bin/bash
https://releases.hashicorp.com/packer/1.4.1/packer_1.4.1_linux_amd64.zip

#!/bin/bash
#varialbles
APP="packer"
INSTALL_DIR="${1:-/opt/${APP}}"
URL="https://releases.hashicorp.com/${APP}"
VER="$(curl -sL $URL | grep -v beta | grep -Po "_(\d*\.?){3}" | sed 's/_//' | sort -V | tail -1)"
ZIP="${APP}_${VER}_linux_amd64.zip"
#code
mkdir -p /opt/${APP}/
${APP} version
echo "* Downloading ${URL}/${VER}/${APP}_${VER}_linux_amd64.zip"
curl -s ${URL}/${VER}/${APP}_${VER}_linux_amd64.zip -o ${INSTALL_DIR}/${ZIP}
echo "* Extracting $ZIP into $INSTALL_DIR"
unzip -o ${INSTALL_DIR}/$ZIP -d $INSTALL_DIR && rm -v ${INSTALL_DIR}/$ZIP
rm -rf /root/bin/${APP}
mv /opt/${APP}/${APP} /root/bin/${APP}
${APP} version
${APP} -autocomplete-install