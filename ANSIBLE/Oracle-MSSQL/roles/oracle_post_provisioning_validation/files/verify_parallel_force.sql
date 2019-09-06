 set tab off
 set linesize 180
 col inst_id for 99
 col name format a30
 col value format a10
 select inst_id,name, value from gv$parameter where name like '%parallel_force_local%' order by inst_id;
 EXIT