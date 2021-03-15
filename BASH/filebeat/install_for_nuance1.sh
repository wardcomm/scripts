#!/bin/bash
cd /tmp
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.11.2-x86_64.rpm
sudo rpm -vi filebeat-7.11.2-x86_64.rpm
curl -L -O https://github.com/wardcomm/scripts/blob/master/BASH/filebeat/filebeat.yml
cp filebeat.yml /etc/filebeat/filebeat.yml
sudo systemctl start filebeat
sudo systemctl enable filebeat
