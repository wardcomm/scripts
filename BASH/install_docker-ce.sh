#!/bin/bash
yum update
yum install yum-utils device-mapper-persistent-data lvm2 -y
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce -y
systemctl start docker
systemctl enable docker
systemctl status docker
docker pull jenkins/jenkins
docker pull openshift/origin
docker -v
docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
