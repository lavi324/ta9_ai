[[_TOC_]]

#General Scope

This Wiki describes the SOW of installing and using IQ in REM Prod.
Migration of Data Model “Hazharot” from MySQL DB to IQ is necessary, due to oversized data records that MySQL is not meant to support (~70M)

The Scope of Work was as follows:

- Scan and Install a Full VM, including IQ db Installed with the "Hazharot" schema pre-configured
- Migrate Data From "Hazharot" SQL to "Hazharot" on IQ
- Change the Connection string of the "hazharot" DM, to look on the new table in IQ

#IQ Server
IQ Vm was installed and deployed on REM Premise.
The VM was allocated with: 
- 8 Core
- 16 GB RAM
- Installed with Centos 7 (x86_64)

#Create Table in IQ 
##Script
Copy the create statments of the Mysql table, 
remove the primary key constraint so the insert will be faster and run it in the iq.
notice - 'int(11)' need to be changed to 'int'

##Export from MySql
The data included Hebrew values and different signs as: ( ), ", ' ,| , : , /
The export that handled it the best was export as insert statement.
a. connect to mysql via DBeaver, query part of the data 
notice - try to query the table without the schema name, 
for example instead: select * from ta9data hazarot 
query: select * from hazarot
so the insert statment we exporting will not have the schema name.
b. Click on export and chose sql statement
![image.png](/.attachments/image-d8ebe048-de18-45c0-8c80-b147e0c194ca.png)

c. choose the number of raws that every insert statement will have in "segment size":
![image.png](/.attachments/image-e1692096-9cea-4cd7-9c95-e8ccec9711fa.png)

d.
![image.png](/.attachments/image-84160d4c-5d98-4086-9849-4aaf9c1ea9f5.png)

e. make sure its UTF+8 for Hebrew
![image.png](/.attachments/image-cec0dde0-bdb2-40bd-aba9-7151a755291e.png)

f. ![image.png](/.attachments/image-1fb03685-6b27-4af2-9138-affabc5eb18c.png)

##Import to IQ
Open the file via notepad++.
The insert file should look like that:

![image.png](/.attachments/image-b31ed85e-b77e-41de-94c2-4a5fa8819d3e.png)


1. Add "commit;" in the end of the file.
2. if the name of the schema exists - click ctrl+f and replace the ta9data with [DBA] 
3. save the file and move it with FileZilla to the iq server 
4. right-click on the file -> file prmissions
5. give full permissions to the file : 777 
![image.png](/.attachments/image-5cd7d76e-284c-410c-8f26-1ae4d0c6fbde.png)

or connect to the server, find the file and give the permissions with "chmod 777" command
7. connect to the iq with iq16 user
8. run the command:
for example my file located in /opt/iq16:
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza.sql -nogui

optional - the script will run and insert the output into external txt file:
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza.sql -nogui >> output.txt

to run multiple inserts in this format:
Create a new txt file, write all the insert files with the command:

"#/bin/bash
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza1.sql -nogui >> output.txt
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza2.sql -nogui >> output.txt
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza3.sql -nogui >> output.txt
dbisql -c "uid=db,pwd=Sap123;eng=deviq" /opt/iq16/liza4.sql -nogui >> output.txt

-you can add between the lines a string that will write in the log file every file that ending and starting using:
echo "end file 2, start of file 3"  >> output.txt

move this script to the iq server using filezilla, add full permissions and rename the file to change its format to '.sh'

run this script from the iq server : ./script.sh 
















































