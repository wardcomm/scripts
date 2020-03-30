#!/bin/bash

echo $TMP >> tmp.txt

unset TMP
TMP=/mytmp
export TMP

echo $TMP >> tmp.txt

./runInstaller -silent -responseFile /stage/grid/response/grid_install.rsp -ignorePrereq -ignoreSysPrereqs -waitforcompletion
