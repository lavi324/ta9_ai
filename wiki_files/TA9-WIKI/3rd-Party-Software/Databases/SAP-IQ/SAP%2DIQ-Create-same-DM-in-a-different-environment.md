# **STEPS:**

## Get all tables:
```exec sp_tables '%', 'DBA', '%', "'TABLE'"```

## **Get the table headers:**
```
select g.table_name, g.column_name, g.domain_name as type, g.width
from(
select *
from
(select a.table_id, a.table_name, b.column_name, b.domain_id, b.width
from systab a
JOIN systabcol b
on a.table_id = b.table_id
where a.table_name = 'TABLE_NAME') c
JOIN
SYS.SYSDOMAIN d
on d.domain_id = c .domain_id) g
```
Or by using the **DBeaver** program - 

Right-Click on the original table you want to copy in the IQ DBeaver of the original environment -

![image.png](/.attachments/image-80ddd45a-0b8e-4ccb-b591-91f8aa53be16.png)

Then this window is opened and you click on 'Copy' - 

![image.png](/.attachments/image-e23981bf-c54d-4d5f-b259-bd12a3b3aa4c.png)

## Get IQ's spaces:
`sp_iqdbspaceinfo`

## Create table in the new ENV:

CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
   ....
) IN space_name;

Or you easily paste the script you have just copied in the DBeaver program and execute - 

![image.png](/.attachments/image-78ada111-1120-4d58-bbbd-5cc08b3b0442.png) 

Notice That : 
   - The SQL script you have opened is connected to the relevant environment
   - The table will be created in the default space of the environment unless another space was declared (space declaration is made by using the 'IN' statement in the end)
   - 4 mandatory system fields (case-sensitive) exists in the script:
     - fileid
     - caseid
     - departmentid
     - system_comment

For Example : 
```
CREATE TABLE Osint_GeoLocations (
	ExtractionID varchar(500),
	TimeField varchar(500),
	GeoLng double,
	GeoLat double,
	SourceField varchar(500),
	AddressField varchar(500),
	PostURL varchar(500),
	DescriptionField varchar(500),
	fileid integer,
	caseid integer,
	departmentid integer,
        system_comment varchar(500),
	MSISDN varchar(25),
	DateField timestamp
)IN MAIN_DATA;
```
## Create DM in the Admin Studio:

1. Click on Data models tile
2. Click on 'Add Data Connection'
3. Click on 'Sap Sybase IQ'
4. Enter Credentials to connect
5. choose the relevant Schema and Table
6. Save

## A specific example you can find here - 
[Example-SAP-IQ-Extract-Table-unified_subscribers](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/328/Example-SAP-IQ-Extract-Table-unified_subscribers)