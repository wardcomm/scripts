set tab off
set linesize 200
col name format a15
col value format a10
col inst_id format 99
select inst_id,name, value from gv$parameter where name like '%recyclebin%' order by inst_id;
EXIT
