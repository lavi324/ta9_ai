[[_TOC_]]

# Step 1 - Changing MySQL Configuration

```
mysql --help | grep "Default options" -A 1
nano /etc/my.cnf
```

Restart the service:
`systemctl restart mysqld`



# Step 2 - Opening The Required Port
firewall-cmd --permanent --zone=trusted --add-source=0.0.0.0
firewall-cmd --permanent --zone=trusted --add-port=3306/tcp
firewall-cmd  --reload

![image.png](/.attachments/image-7dfda7d2-ab2a-4095-84be-8016b213080a.png)

# Step 3 - login to MySQL


```
mysql -u root -p
SHOW VARIABLES LIKE 'validate_password%';
SET GLOBAL validate_password_policy=LOW;
exit
sudo service mysqld restart
mysql -u root –p
UNINSTALL PLUGIN validate_password;
```

# Step 4 - Grant access to the server + database

Edit the file :

`mysql --help | grep "Default options" -A 1` 

`vi etc/my.cnf`

Add this lines : 


```
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M

[client]
port	    = 3306
protocol    = tcp

[mysqld_safe]
pid-file	= /mnt/data/var/lib/mysqld/mysqld.pid
socket		= /mnt/data/var/lib/mysql/mysql.sock
nice		= 0

[mysqld]
user		= mysql
pid-file	= /mnt/data/var/lib/mysqld/mysqld.pid
socket		= /mnt/data/var/lib/mysql/mysql.sock
port		= 3306
datadir		= /mnt/data/var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
explicit_defaults_for_timestamp


bind-address	= 0.0.0.0


#log-bin         = /mnt/app/opt/archive/mysql/binlog/log
#general_log_file= /mnt/app/opt/archive/mysql/querylog/query.log
general_log     = on
lower_case_table_names = 1
max_connections = 1000
log_bin_trust_function_creators = 1
#log-error	= /mnt/app/opt/logs/mysql/errorlog/error.log
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
#!includedir /etc/mysql/conf.d
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid

```

## Add rules to database:


```
CREATE USER 'TA9root'@'%' IDENTIFIED BY 'XhXntkmysql@2020';
CREATE USER 'TA9root'@'localhost' IDENTIFIED BY 'XhXntkmysql@2020';
GRANT ALL PRIVILEGES ON *.* TO 'TA9root'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'TA9root'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
ALTER USER 'TA9root'@'localhost' IDENTIFIED BY 'XhXntkmysql@2020';
ALTER USER 'TA9root'@'%' IDENTIFIED BY 'XhXntkmysql@2020';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'XhXntkmysql@2020';
ALTER USER 'root'@'%' IDENTIFIED BY 'XhXntkmysql@2020';
FLUSH PRIVILEGES;
```







