#!/bin/bash
email="joseph.ward@orhp.com"
passhrase="pAvem5entbulgi1nessPoi'ntersma8sherstop;perla6unChpend-inggu[mminesSscarcecu>ddlygru?mbLecas\ually"

sftp   -i /REPO/cnb_private.key  oldrepub@mway.cnb.com:/oldrepub.fromcnb 
echo "sftp from cnb on `date +"%B %Y"` | mailx -s "sftp from cnb on `date`"  $email
