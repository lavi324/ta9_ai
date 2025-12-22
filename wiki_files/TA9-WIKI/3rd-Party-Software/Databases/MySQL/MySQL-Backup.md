[[_TOC_]]

# MySQL Backup 

![image.png](/.attachments/image-93399269-46b9-4af4-8bde-146f80b278a5.png)


# Manually Backup MySQL Server
## Usage environment
MySQL version: 5.6.0
Workbench version: 6.1

##Prerequisites 

Make sure you have right to:

1.Machine IP address.
2.Username with access all schemas.
3.Password to MySQL server.
4.Safe place to store the Dump file. 
5.Get into MySQL Workbench environment.

# Connect to Database

![image.png](/.attachments/image-1edbb6e5-9b64-4dd2-8715-65e428e09963.png)
 
 6. Sign to your Database server of MySQL:
 ![image.png](/.attachments/image-4d861f46-12b0-4e05-808a-4b8c9ded9535.png)

7. Go to:
Server > Data Export 

![image.png](/.attachments/image-d36d18db-9635-4cda-8607-55e96f89fc62.png)
 

8. Choose all Database Scheme and choose safe location to export the dump file.
![image.png](/.attachments/image-789d8ece-93d1-4a1c-ae25-f35716dc2b8e.png)

6. Done! Your dump file is ready.


# Backup MySQL windows command-line

`mysqldump -u root -p --databases DB_NAME >databasename.sql`

mysqldump is actually a executable file present in your /MySQL\MySQL Server 5.6\bin

for example [ on windows ]

`C:\Program Files (x86)\MySQL\MySQL Server 5.6\bin\mysqldump.exe`

## Backup and specify loaction:

open command line
Navigate:


cd C:\Program Files (x86)\MySQL\<YourVersion>\bin

`mysqldump.exe -e -h 10.100.102.21 -u MySQLUser -p <password> --single-transaction --all-databases > \\path\to\your\network\location\BackupName.sql`


# Backup MySQL Linux

## Backing Up a Single Database

`mysqldump database_name > database_name.sql`

## Backup From docker container

docker exec -i mysql mysqldump -h ipaddress -u root --password='mysqlpassword' --single-transaction --all-databases > backup.sql


## Backing Up Multiple Databases

`mysqldump --databases database_one database_two > two_databases.sql`



## Backing Up All Databases

`mysqldump --all-databases > all_databases.sql`


# Backup MySQL running on a docker

Log in to the machine
```
mount -a 
docker exec -i mysql mysqldump -h IpAddres -u root --password='mysql!@#$' --single-transaction --all-databases > /mnt/smb/MySQL-BU/TEST/Date_MachineNumber.sql
```




