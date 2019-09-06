set trimspool on
set SERVEROUTPUT ON
declare
l_sql varchar2(2000);
qt varchar2(255) := '''';
Begin
  dbms_output.put_line('-- Loop 1 -- Add New Log Members on +RECO');
 for c1 in (
 select group#, count(*) count1 from v$logfile where member like '%RECO%' group by group# order by 1 
 ) loop
  --dbms_output.put_line('--'|| c1.member);
if c1.count1 <= 1 then
  l_sql := replace('alter database add logfile member ~+RECO~ to group '||c1.group#,'~',qt);
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
end if;
 end loop;
  dbms_output.put_line('-- Loop 2 -- Drop Log Members on +DATA');
 for c1 in (
 select a.group#,a.thread#, a.status, a.bytes/1024/1024 size_mb,
 b.member
 from v$log a, v$logfile b where a.group#=b.group# 
 and b.member like '%DATA%'
-- and b.member like '%orad%'

 order by a.status desc
 ) loop
  dbms_output.put_line('-- Status '|| c1.status);
  If c1.status like 'CURRENT' then
   dbms_output.put_line(c1.member);
  l_sql := 'alter system checkpoint global';
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
  l_sql := 'alter system archive log current';
  l_sql := 'alter system switch logfile';
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
  l_sql := 'alter system checkpoint global';
  execute immediate l_sql; 
  dbms_lock.sleep(5);
  dbms_output.put_line(l_sql);
  end if;
  l_sql := replace('alter database drop logfile member ~'||c1.member ||'~','~',qt);
begin
  execute immediate l_sql;
  exception
   when others then
    NULL;
end;
  dbms_output.put_line(l_sql);
 end loop;
end;
/
commit;
alter system archive log current;
alter system checkpoint global;
declare
l_sql varchar2(2000);
qt varchar2(255) := '''';
Begin
  dbms_output.put_line('-- Loop 2 -- Drop Log Members on +DATA');
 for c1 in (
 select a.group#,a.thread#, a.status, a.bytes/1024/1024 size_mb,
 b.member
 from v$log a, v$logfile b where a.group#=b.group# 
 and b.member like '%DATA%'
-- and b.member like '%orad%'

 order by a.status desc
 ) loop
  dbms_output.put_line('-- Status '|| c1.status);
  If c1.status like 'CURRENT' then
   dbms_output.put_line(c1.member);
  l_sql := 'alter system checkpoint global';
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
  l_sql := 'alter system archive log current';
  l_sql := 'alter system switch logfile';
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
  l_sql := 'alter system checkpoint global';
  execute immediate l_sql; 
  dbms_lock.sleep(5);
  dbms_output.put_line(l_sql);
  end if;
  l_sql := replace('alter database drop logfile member ~'||c1.member ||'~','~',qt);
  execute immediate l_sql;
  dbms_output.put_line(l_sql);
 end loop;

end;
/