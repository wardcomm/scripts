#!/usr/bin/env python
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json

user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'

s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
#s.cert='/path/to/mycertificate.pem

def check_manager_state(baseUri,s):
        while True:
            r=s.get(baseUri+'/Manager')
            manager=r.json()
            if manager[0]['managerRunState'].upper() == 'RUNNING':
                break
            time.sleep(1)
        return

r=s.get(baseUri+'/Server')
for i in r.json():
       # do something with the content
       print ('{name} is {state}'.format(name=i['name'],state=i['serverRunState']))
