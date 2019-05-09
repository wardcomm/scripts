#!/bin/bash
yum update yum -y
yum update * -y

yum groupinstall "GNOME Desktop" "Graphical Administration Tools" "Server with GUI" -y
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install ansible -y
#yum install perl gcc dkms kernel-devel kernel-headers make bzip2 wget  curl -y
yum groupinstall "Development Tools" -y
#yum install gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel -y

yum remove git -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install git2u-all -y
#yum install https://code.visualstudio.com/docs/?dv=linux64_rpm&build=insiders/code-insiders-1.34.0-1557206804.el7.x86_64.rpm -y
cd /REPO

# yum install htop ncdu -y
#yum install code-insiders
# yum upgrade git

git --version
git clone https://github.com/wardcomm/scripts.git
cd /REPO/scripts/ANSIBLE
ansible-playbook  /REPO/scripts/ANSIBLE/install_linux.yml
#wget https://go.microsoft.com/fwlink/?LinkID=760866
#yum localinstall code-insiders*x86_64.rpm

snap install code-insiders
snap refresh code-insiders
# rpm --import https://packages.microsoft.com/keys/microsoft.asc
# sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

#ln- sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target
systemctl get-default graphical.target
systemctl isolate graphical.target
systemctl set-default graphical.target
yum groupinstall "MATE Desktop" -y
update-alternatives --config x-session-manager
#yum install https://centos.pkgs.org/7/epel-x86_64/ansible-lint-3.5.1-1.el7.noarch.rpm -y
yum check-update -y
#yum install snapd -y
systemctl enable --now snapd.socket
ln -sfn /var/lib/snapd/snap /snap
snap install code-insiders
systemctl isolate graphical.target
#yum install code-insiders
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=10800'
#init 5
#systemctl halt
#shutdown -h now
#reboot

