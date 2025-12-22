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


#Backup MySQL windows command-line


mysqldump is actually a executable file present in your /MySQL\MySQL Server 5.6\bin

1. Open Command-Line as admin.
2. Navigate:

`C:\Program Files\MySQL\MySQL Server 5.7\bin`


mysqldump --host=<SpecifyFullHostName of the my sql server> --user=<MySQL Root User> --password=<MySQL RootUser>  --single-transaction --all-databases > path/to/secure/location/test.sql

Exemple: 
`mysqldump --host=TA9-MySQL.TA9.local --user=ta9root --password=weSQL976rp()  --single-transaction --all-databases > C:\Users\ta9root\Desktop\mysql.sql`


#Recommendation
It is a good idea to let the server preform this task weekly.
Use Task Scheduler ![image.png](/.attachments/image-98bc832f-5cd2-47d0-a5b6-89a8e727b5d5.png)


## Create bat file
Create a bat file whom contain the script of the backup
Configure Task Scheduler 
Go the task properties --> Action tab --> Edit --> Fill up as below:
1. Action: Start a program
2. Program/script: path to your batch script e.g. C:\Users\beruk\bodo.bat
3. Add arguments (optional): <if necessary - depending on your script>
4. Start in (optional): Put the full path to your batch script location 

   e.g. C:\Users\AdminAccount\(Do not put quotes around Start In)

Then Click OK

# Auto Delete after X time

Create a file:
Deletemysql.ps1
Get-ChildItem –Path "\\Path\to\mysql\dump" -Recurse | Where-Object {($_.LastWriteTime -lt (Get-Date).AddDays(-20))} | Remove-Item
This script will delete files older than 20 days. 

After you confirm it is working you can put it in Task Scheduler.

#Restore MySQL

1. Open Command-Line as admin.
2. Navigate:
cd C:\Program Files\MySQL\MySQL Server X.X\bin
(Change the MySQL version according to yours)

mysqldump --host=<SpecifyFullHostName of the my sql server> --user=<MySQL Root User> --password=<MySQL RootUser>  --single-transaction --all-databases < path/to/secure/location/test.sql





