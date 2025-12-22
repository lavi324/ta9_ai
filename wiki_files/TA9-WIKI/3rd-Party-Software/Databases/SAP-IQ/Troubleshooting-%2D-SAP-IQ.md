[[_TOC_]]

## IQ License Expired
**Symptom:**
No SYSAM License Available 
IQ license expired, need to install a new license

**Solution:**
Install a new IQ license
- Put it in [IQ_INSTALLTION_FOLDER] / SYSAM-2.0/licenses
- Restart IQ service

Make sure license loaded successfully:
Look at logs of startup
OR
run so_iqlmconfig

(some validation:
make sure the .lmp file is configured with:
PE=EE 
LT=AC
)

## Loading errors
### Error: Data type conversion is not possible. Argument to RTRIM must be binary or string
![image.png](/.attachments/image-627a9eb3-8afa-4143-8255-031d8dbc55f2.png)

**Solution:**
One of the fields on the Data Model defines as a string but on the IQ the field isn't a string.

### Table is currently locked by another user
![image.png](/.attachments/image-85bc291a-d7b8-43b7-9f40-321d8e02cc88.png)

**Solution:**
Run the following command on IQ to check which users are locking the table: `sp_iqlocks`

then copy the conn_id number and drop the connection:
DROP CONNECTION conn_id;

## Table actions:

### List all tables

select convert(varchar(30),o.name) AS table_name
from sysobjects o
where type = 'U'
order by table_name

### Rename IQ table name
sp_iqrename current_table_name, new_table_name

### Add a column to IQ table name
ALTER TABLE Employees ADD office CHAR(20)
ALTER TABLE Employees ADD office VARCHAR(90)
ALTER TABLE Employees ADD office INTEGER

### Set column default value
ALTER TABLE table_name MODIFY insert_date DEFAULT CURRENT DATE;
ALTER TABLE table_name MODIFY IsActive DEFAULT 1;

### Default value as auto-increment
 CREATE TABLE cities
   (
      id INTEGER DEFAULT AUTOINCREMENT, 
      name VARCHAR(90),
      insert_date date,
   );
 
   -- is equivalent to
   CREATE TABLE cities
   (
      id INTEGER IDENTITY, 
      name VARCHAR(90),
      insert_date date,
   );

OR

ALTER TABLE Table MODIFY RecordID DEFAULT AUTOINCREMENT;

Read more on: http://www.sqlines.com/sybase-asa/autoincrement_identity

## Get view query definition
sp_helptext view_name

## Get stored procedure definition
sp_helptext stored_procedure_name
_____________________

#You have run out of space

Error:

SAP IQ - 'You have run out of space in IQ_SYSTEM_TEMP DBSpace' error during running sp_iqcheckdb 'verify database'

## Find how much you can append
sp_iqdbspace iq_main;

## add the amount to top:
alter dbspace iq_main alter file iq_main add XXXX KB / MB / GB 

_______________________



