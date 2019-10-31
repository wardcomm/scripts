#!/usr/bin/env python
#imports libraries
import requests
import urllib3
import ovmclient
import sys
import os
import time
import json

client = ovmclient.Client('base_Uri', 'user', 'password')
user = 'p2906297'
password = 'THem5dax'
baseUri = 'https://ovmdmgr04:7002/ovm/core/wsapi/rest'
client = ovmclient.Client(baseUri, user, password)

s=requests.Session()
s.auth=( user, password )
s.verify=False #disables SSL certificate verification
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
#s.cert='/path/to/mycertificate.pem

delete_drive  = requests.delete(baseUri, 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb0000060000d10b10b137e9af73/VmDiskMapping') 