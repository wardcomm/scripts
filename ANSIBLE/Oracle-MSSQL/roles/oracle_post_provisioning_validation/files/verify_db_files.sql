set tab off
set linesize 200
col name format a20
col inst_id for 99

select inst_id,name, value from gv$parameter where name like '%db_files%';
EXIT
