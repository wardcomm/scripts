set tab off
set linesize 200
col owner for a5
col object_name for a40
col status for a15
select owner, object_name, status from dba_objects where object_name like '%F_PWD_VERIFY%';
EXIT
