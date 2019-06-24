# #!/bin/bash
# export APP="packer"
# export VERSION="1.4.1"
# APP="packer"
# wget https://releases.hashicorp.com/${APP}/${VERSION}/${APP}_${VERION}_linux_amd64.zip -P /opt/${APP}/S
# #https://releases.hashicorp.com/packer/1.4.1/packer_1.4.1_linux_arm64.zip
# #!/bin/bash
# #varialbles
# APP="packer"
# mkdir -p /opt/${APP}/
# INSTALL_DIR="${/opt}/${APP}/"
# URL="https://releases.hashicorp.com/${APP}"
# VER="$(curl -sL $URL | grep -v beta | grep -Po "_(\d*\.?){3}" | sed 's/_//' | sort -V | tail -1)"
# ZIP="${APP}_${VER}_linux_amd64.zip"
# #code
# echo "DEBUG ONE"
# mkdir -p /opt/${APP}/
# #${APP} version
# echo "* Downloading ${URL}/${VER}/${APP}_${VER}_linux_amd64.zip"
# echo "DEBUG TWO"
# curl -s ${URL}/${VER}/${APP}_${VER}_linux_amd64.zip -o ${INSTALL_DIR}/${ZIP}
# echo "DEBUG THREE"
# echo "* Extracting ${ZIP} into ${INSTALL_DIR}"
# unzip -o ${INSTALL_DIR}/$ZIP -d ${INSTALL_DIR} 
# #rm -rf ${INSTALL_DIR}/${ZIP}
# echo "DEBUG FOUR"
# # rm -rf /root/bin/${APP}
# echo "DEBUG FIVE"
# mv /opt/${APP}/${APP} /root/bin/${APP}
# echo "DEBUG SIX"
# ${APP} version
# ${APP} -autocomplete-install
#!/bin/bash
# packer version
mkdir -p /opt/packer/
INSTALL_DIR="${1:-/opt/packer}"
URL="https://releases.hashicorp.com/packer"

VER="$(curl -sL $URL | grep -v beta | grep -Po "_(\d*\.?){3}" | sed 's/_//' | sort -V | tail -1)"
ZIP="packer_${VER}_linux_amd64.zip"

echo "* Downloading ${URL}/${VER}/packer_${VER}_linux_amd64.zip"
curl -s ${URL}/${VER}/packer_${VER}_linux_amd64.zip -o ${INSTALL_DIR}/${ZIP}
echo "* Extracting $ZIP into $INSTALL_DIR"
unzip -o ${INSTALL_DIR}/$ZIP -d $INSTALL_DIR && rm -v ${INSTALL_DIR}/$ZIP
rm -rf /root/bin/packer
mv /opt/packer/packer /root/bin/packer
/root/bin/packer version
