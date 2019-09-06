-- select DIRECTORY_PATH,DIRECTORY_NAME from dba_directories;
spool /u01/tmp/postval/directory_name_check.lst
set tab off
Set line 200
col directory_path format a200
col directory_name format a20

select DIRECTORY_PATH,DIRECTORY_NAME from dba_directories;
 Spool off
EXIT
