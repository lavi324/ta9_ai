[[_TOC_]]

Login as root or privileged user

Default location installed is:

/var/lib/mysql

we want to change it to

/mnt/data

# 1. stop the service:

`systemctl stop mysqld.service`

# 2. Create a backup


```
cd ~/

mkdir /backup && cd /backup

mkdir /mysql

cp -r /var/lib/mysql ~/backup/mysql
```

# 3. Move the mysqldata

## Create mysql directory
`mkdir -p /mnt/data/var/lib`

## Move the data
`mv /var/lib/mysql /mnt/data/var/lib`

## Change ownership on the folder:

chown -R mysql:mysql /mnt/data

# 4. Modify my.cnf and Start MySQL

# vi /etc/my.cnf
datadir=/mnt/data/var/lib/mysql
socket=/mnt/data/var/lib/mysql/mysql.sock


# 5. Finally, restart the MySQL database.

`systemctl start mysqld.service`

# 6. Specify the new socket

`mysql -u root -p  --socket=/mnt/data/var/lib/mysql/mysql.sock`







