#!/bin/bash
mkdir -p /usr/local/src
cd /usr/local/src

wget http://nginxcp.com/latest/nginxadmin.tar

tar xf nginxadmin.tar

cd publicnginx

./nginxinstaller installS
