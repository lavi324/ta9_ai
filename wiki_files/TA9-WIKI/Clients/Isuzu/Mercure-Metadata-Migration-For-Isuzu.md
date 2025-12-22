[[_TOC_]]

#Introduction
This procedure will be used to export data from PostgreSQL used in Mercure and migrate it into our system.

#Setup
1. All credentials used in this document may not be accurate and the photos are for reference only. Please verify all hosts and passwords with the DevOps.
2. Verify a client for Mercure export - DBeaver is good, Choose PostgreSQL at startup.
- Connection screen: 
![Connection settings postgres.png](/.attachments/Connection%20settings%20postgres-1d932e05-7c13-46e3-932a-2d1dcaefed41.png)
3. Verify an SQL client for easy import - MySQL workbench is also good. Login as usual (root, mysql!@#$) to the desired DB
4. Verify an FTP client - e.g. FileZilla. Connect with sftp.
- Connection screen:
![fileZilla.png](/.attachments/fileZilla-8c164362-1af0-486a-925f-694556ae4742.png)

4. It can also be helpful to have HeidiSQL to import a CSV file which does not match exactly to the table being imported into. More on that on Troubleshooting.

5. Full path is located at your Clients repository -> Isuzu -> Scripts -> Mercure Migration -> Metadata Scripts

##Notes

1. At "Export Load Files" you should note that "130 as targetid" is arbitrary.
Verify what is the "CDR Log" data model ScehmaID in "sqlite_metadata.dataschema1" table and edit the script accordingly.
2. At "Export Mercure Users" you should note that "2 as languageID" is arbitrary. 
Verify what is the corresponsing ID to French in "sqlite_metadata.languages" table before exporting and edit the script accordingly.
If you miseed it, you can update it later (change the X) with:
update sqlite_metadata.users  
set LanguageID = X
where UserID < -1

3. It may be needed to use HeidiSQL while importing "Mercure Users" and "Load_Files"

4. The paths in all the scripts are hard coded to "/opt/export_data/export_data2/file_name.csv" in remote and "C:\\MercureToMysql\\file_name.csv" in local. Verify these locations exist, create or change them as you wish.

#Flow
1. There are two folders - "Step 1 - Export Data From Mercure" and "Step 2 - Import Data To sqlite.metadata".
2. Open "Step 1 - Export Data From Mercure" - Open the files in the order provided, Copy, Paste in DBeaver sql editor and execute.
3. Open FileZilla and navigate both paths to the correct location. Refresh "Remote Site" to view all exported files. Copy them from remote location and paste them to local location.
3. Open "Step 2 - Import Data To sqlite.metadata" and do the same as step 2, this time in MySQL workbench).



#Troubleshooting
 1. If there is a mismatch between the columns headers in the exported file to the metadata table itself while trying to import, Go to HeidiSQL and go to Tools -> Import CSV File.

![heidy.png](/.attachments/heidy-ed0e8890-8d9f-416d-a71e-ff7d9e2b442c.png)

2. If you get a "Permission Denied" Error while trying to export data from Mercure (through DBeaver) make sure you check all folders' write permission: ![fileattributes.png](/.attachments/fileattributes-3ffc16a0-0ec1-430e-a51b-5129b82bfae4.png)
