col member for a80
col group# format 99
col status format a10
col inst_id format 99
set pages 100
set linesize 180 
set tab off
select inst_id, group#, status, member from gv$logfile order by inst_id,group#;
EXIT