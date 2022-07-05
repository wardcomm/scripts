sudo apt update && sudo apt -y upgrade
#reboot optional
sudo apt install open-vm-tools-desktop
sudo apt install net-tools
sudo apt install git
sudo apt install python3-virtualenv
mkdir virtual
cd virtual
virtualenv awx
source awx/bin/activate
sudo apt -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
newgrp docker
docker version
sleep 4
pip3 install docker-compose
git clone -b 17.0.1 https://github.com/ansible/awx.git
#admin_password=(your secure password)
pip3 install ansible
ansible-playbook -i inventory install.yml

