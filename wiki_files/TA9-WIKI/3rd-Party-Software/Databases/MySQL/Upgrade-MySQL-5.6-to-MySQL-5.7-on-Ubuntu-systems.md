**Before moving on this guide make sure to create a snapshot of this machine.**

stop mysql service on machine 
` sudo systemctl stop mysql`

download upgrade package from mysql web site
[http://dev.mysql.com/get/mysql-apt-config_0.8.0-1_all.deb]()


copy this file to relevant server via filezila. 
If internet connection exist it posible to use ` wget http://dev.mysql.com/get/mysql-apt-config_0.8.0-1_all.deb`

install package `sudo dpkg -i mysql-apt-config_0.8.0-1_all.deb`

! from some resone the system shows that ubuntu 18.04 doesnt support' choose other  version of ubuntu and contynue with upgrade. 

first select current version of MySQL 
<IMG  src="https://i2.wp.com/tastethelinux.com/wp-content/uploads/2021/06/1.Select_the_5.6_option-1437062593-1623778548541.png?w=1160&amp;ssl=1"/>

after that select version of you wish to upgrade (5.7)
<IMG  src="https://i0.wp.com/tastethelinux.com/wp-content/uploads/2021/06/2.Select_the_repo_of_5.7.png?resize=1024%2C207&amp;ssl=1"/>

click "OK"

<IMG  src="https://i2.wp.com/tastethelinux.com/wp-content/uploads/2021/06/2.1Press_ok_to_save_the_Configuration.png?resize=1024%2C356&amp;ssl=1"/>

run `sudo apt-get update` after that run `sudo apt-get install mysql-server`

in the end of process you will see 

<IMG  src="https://i0.wp.com/tastethelinux.com/wp-content/uploads/2021/06/5.MySQL_Upgrade_Successfully.png?resize=874%2C553&amp;ssl=1"  alt="Upgrade MySQL from 5.6 to 5.7"/>

## Enable remote connection 

for enable to connect remote to the DB (via workbranch) need to change paramaetrs on the config file. 
`sudo vi/etc/mysq/mysql.conf.d/mysql.cnf`
change next parameter from 127.0.0.1 to 0.0.0.0
![image.png](/.attachments/image-c5088973-a6da-4b34-8ed3-eb592aa719cc.png)

connect to server `mysql -u root -p` enter the root password
in the console press:
`use sql;
CREATE USER 'root'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
`

check if all DB imigrated correct to the new version othervice run backup.

