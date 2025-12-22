1. to add auto increment field and fill the existing data with it:
ALTER TABLE ivoryiq.[DBA].table ADD id numeric(5,0) IDENTITY NOT NULL;

2. add a column with the current date and time, uploaded data will get the current datetime:
ALTER TABLE ivoryiq.[DBA].table ADD lastupdate datetime DEFAULT getDate() NOT NULL;

3. don't drop columns via DBeaver UI- copy the alter command it shows without deleting the index.

4. How many licenses: Run Sp_iqlmconfig
![image.png](/.attachments/image-3cd98d8a-33dc-4944-a1bf-6b6cc580aefc.png)
