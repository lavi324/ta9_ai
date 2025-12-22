[[_TOC_]]

# Introduction

![image.png](/.attachments/image-442c616f-c4b3-4199-a5f6-fb62047da5d0.png)

OrientDB is the world’s leading open-source NoSQL multi-model database that powers today’s strongest enterprises and the applications they build. OrientDB allows organizations to unlock the true power of graph databases without having to deploy multiple systems to handle other data types, which increases performance and security while supporting scalability.



# OrientDB Backup 
# Manually Backup Orient Database
## Usage environment
orient version: 2.2.30

## Prerequisites 
Make sure you have right to:

1.Machine IP address.
2.Username with access to all data.
3.The password to orient server.
4.A safe place to store the files. 
5. Filezilla software:

[https://filezilla-project.org/]()

___________________________________________________________________________________________________________________
# Docker environment

1. Stop the container by:
`docker stop orientdb`

## Filezilla

2. open Filezilla console

![image.png](/.attachments/image-d0ff4e80-e8ab-4126-bcb4-aab73ea1ee48.png)

3. login with root privilege to the path of the orient( typically can be found in: /opt/application/orientdb/databases/TA9

4. Copy the Database file into a safe place.

5. start the service by: 
`docker start orientdb`
___________________________________________________________________________________________________________________

# Centos environment 
## Stop the service
`systemctl stop orientdb`


## Folder navigation
/opt/application/orientdb/databases/TA9

Create a copy of the folder to a safe place.
___________________________________________________________________________________________________________________

# Windows environment
1. Navigate to services.
2. Stop the orient service.
![image.png](/.attachments/image-ac8d0013-9c33-4f81-bef4-4bafb317dfce.png)

## Database location

typically located in : 

Data drive under Databases.

Copy the folder as is to a safe location.

After copy ended start the service again.

___________________________________________________________________________________________________________________
# Hot Backup
#Backup Database
**Update Orient while running**

**Note**

While taking backup, it will create a consistent copy of a database, all further write operations are locked and waiting to finish the backup process. In this operation, it will create a read-only backup file.
If you need the concurrent read and write operation while taking a backup you have to choose to export a database instead of taking backup of a database. Export doesn’t lock the database and allows concurrent writes during the export process.

# How to connect

1. Navigate to the location software installed
2. Open CMD
3. Type the following command:

console.bat

![image.png](/.attachments/image-e18115a5-1eb3-4056-9921-4998aab183fd.png)


CONNECT REMOTE:<XXX.XXX.XXX.XXX>/<DATABASENAME> <DATABASEUSER> <DATABASEPASSWORD>

![image.png](/.attachments/image-94d96323-504d-497b-ad13-492a312f62b1.png)


This Command will export the data.
![image.png](/.attachments/image-71491c6d-7be4-4f5c-9664-c81d8d54706e.png)

___________________________________________________________________________________________________________________

**Linux environment**

The following statement is the basic syntax of database backup:

`./backup.sh <dburl> <user> <password> <destination> [<type>]`


The following are the details about the options in the above syntax.

**<dburl>** − The database URL where the database is located either in the local or in the remote location.

**<user>** − Specifies the username to run the backup.

**<password>** − Provides the password for the particular user.

**<destination>** − Destination file location stating where to store the backup zip file.

**<type>** − Optional backup type. It has either of the two options.

- Default − locks the database during the backup.

- LVM − uses LVM copy-on-write snapshot in the background.

**Example**

Take a backup of the database demo which is located in the local file system /opt/orientdb/databases/demo into a file named sample-demo.zip and located into the current directory.
You can use the following command to take a backup of the database demo.

`backup.sh plocal: opt/orientdb/database/demo admin admin ./backup-ta9.zip` 

**Using Console**

The same you can do using the OrientDB console. Before taking the backup of a particular database, you have to first connect to the database. You can use the following command to connect to the database named demo.
`orientdb> CONNECT PLOCAL:/opt/orientdb/databases/ta9 admin admin`
 
After connecting you can use the following command to take a backup of the database into a file named ‘backup-demo.zip’ in the current directory.
`orientdb {db=demo}> BACKUP DATABASE ./backup-demo.zip` 

If this command is executed successfully, you will get some success notifications along with the following message:
`Backup executed in 0.30 seconds` 

___________________________________________________________________________________________________________________
## Windows environment

Backup process does not support because the command executed by shell command.
you need to install extension to windows to preform this kind of task.



___________________________________________________________________________________________________________________

# Restore Database


**Example**

You have to perform this operation only from the console mode. Therefore, first, you have to start the OrientDB console using the following OrientDB command.
`$ orientdb`

Then, connect to the respective database to restore the backup. You can use the following command to connect to the database named demo.
`orientdb> CONNECT PLOCAL:/opt/orientdb/databases/demo admin admin`

After a successful connection, you can use the following command to restore the backup from ‘backup-demo.zip’ file. Before executing, make sure the backup-demo.zip file is placed in the current directory.
`Orientdb {db = demo}> RESTORE DATABASE backup-demo.zip`

If this command is executed successfully, you will get some success notifications along with the following message.
`Database restored in 0.26 seconds`

 
___________________________________________________________________________________________________________________

# Export Database

While exporting a database it is not locking the database, which means you can perform concurrent read and write operations on it. It also means that you can create an exact copy of that data because of concurrent read and write operations.


The following statement is the basic syntax of the Export database command.
`EXPORT DATABASE <output file>`


**Example**

In this example, we will use the same database named ‘demo’ that we created in the previous chapter. You can use the following command to export the database to a file named ‘export-demo’.
`orientdb {db = TA9}> EXPORT DATABASE ./export-TA9.export`

If it is successfully executed, it will create a file named ‘export-demo.zip’ or ‘exportdemo.gz’ based on the operating system and you will get the following output.


![image.png](/.attachments/image-c0cdf886-c6f4-4632-9113-ce20f91d105f.png)
![image.png](/.attachments/image-bfc96408-75bc-465d-afd4-ac0350cd1379.png)

 
## Export file location

By default, The export will wait in bin file named as you typed in the console.
Exemple: 

![image.png](/.attachments/image-d4c9b0f6-93f0-4916-87e5-f9e825749048.png)


D:\orientdb-community-2.2.30\bin\export-TA9.export.gz


___________________________________________________________________________________________________________________


# Import Database

Whenever you want to import the database, you must use the JSON format exported file, which is generated by export command.

The following statement is the basic syntax of the Import database command.
`IMPORT DATABASE <input file>` 

**Note**
You can use this command only after connecting to a particular database.

**Example**
In this example, we will use the same database named ‘demo’ that we created in the previous chapter. You can use the following command to import the database to a file named ‘export-demo.gz’.
`orientdb {db = demo}> IMPORT DATABASE ./export-demo.export.gz`

If it is successfully executed, you will get the following output along with the successful notification.
`Database import completed in 11612ms`

___________________________________________________________________________________________________________________

# Docker environment

## Connect to the container

docker run -it orientdb:2.2.30 /orientdb/bin/console.sh

## Backup data

You cant use the regular method backup process, therefore, you need to follow these steps:

1. Turn off docker image

`docker stop orientdb`

2. go to the path were database stored: ( Use Filezilla)

/opt/orientdb/databases/TA9

3. Copy the file to a secure place.

4. turn on the docker image:

`docker start orientdb`














