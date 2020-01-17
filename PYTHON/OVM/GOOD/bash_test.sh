#!/bin/bash
username="p2906297"
passowrd="THem5dax"
url = "https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm/0004fb00000600006d8682d0a02325d4/VmDiskMapping"

curl -x POST -u "$usernname:$password" $url
