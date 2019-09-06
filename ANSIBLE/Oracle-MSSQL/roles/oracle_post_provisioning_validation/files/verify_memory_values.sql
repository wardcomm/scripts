set line 100
set pagesize 100
set tab off

col name format a50
col display_value format a40
col inst_id for 99

select inst_id,name, Display_value from gv$parameter
where name in ('shared_pool','large_pool_size','db_cache_size','streams_pool_size','pga_aggregate_target','sga_max_size','sga_target') order by inst_id;
EXIT
