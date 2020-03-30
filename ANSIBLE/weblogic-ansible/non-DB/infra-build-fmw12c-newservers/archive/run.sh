#! /usr/bin/bash
#=======================================================================================================#
# USER		- the user id with sudo access which the scripts will use to log into the target server #
# PSWD		- the password for USER                                                                 #
# install_user	- the user (not USER) that will be used to install SOA/OSB                              #
# install_group	- the install_user’s group                                                              #
# install_pswd	- the install_user’s password                                                           #
# NODE_1	- the admin server’s IP                                                                 #
# NODE_2	- IP of managed node 2                                                                  #
# NODE_3	- IP of managed node 3                                                                  #
# DB_HOST 	- IP of the DB server                                                                   #
#########################################################################################################

USER=P2344719
PSWD=Password12
install_user=delvusr
install_group=delvgrp
install_pswd=charter123
NODE_1=22.85.211.64
NODE_2=22.85.211.65
NODE_3=22.85.211.66
DB_HOST=22.85.211.66

. ./Jenkins-FMW.sh 

