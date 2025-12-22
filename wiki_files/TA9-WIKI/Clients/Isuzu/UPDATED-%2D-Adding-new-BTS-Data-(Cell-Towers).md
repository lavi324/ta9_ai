# **New cells maintenance - Description**

**Note: Read Before you Start!**

1. BTS table in IQ is the most updated one, so first backup the "bts" table into the "bts_backup" table in IQ.
Create a backup For the "bts" table using this:
**IQ:** `select * into bts_backup from bts`

2. A copy of the data in the IQ "bts" table should be in the MYSQL too.
Export the "bts" table from IQ and save it as a local csv on your PC.
Then, create a "bts_current" table in MYSQL (or use an existing one) that has those characteristics-
![image.png](/.attachments/image-cc33e70d-ba39-4bb9-afa5-d023f138609f.png)
If you create a new table, you can use this:
**MYSQL:** 
```
CREATE TABLE ta9data.`bts_current` (
  `Operator` varchar(254) DEFAULT NULL,
  `technology` varchar(254) DEFAULT NULL,
  `MCC` int(11) NOT NULL,
  `MNC` int(11) NOT NULL,
  `LAC` int(11) NOT NULL,
  `Cell_ID` varchar(254) DEFAULT NULL,
  `mercure_cell_id` varchar(254) DEFAULT NULL,
  `country` varchar(254) DEFAULT NULL,
  `Longitude` float NOT NULL,
  `Latitude` float NOT NULL,
  `cell_name` varchar(254) DEFAULT NULL,
  `region` varchar(254) DEFAULT NULL,
  `sub_region` varchar(254) DEFAULT NULL,
  `address` varchar(254) DEFAULT NULL,
  `Azimut` varchar(254) DEFAULT NULL,
  `Ouverture` varchar(254) DEFAULT NULL,
  `Description` varchar(254) DEFAULT NULL,
  `fileid` int(11) DEFAULT NULL,
  `caseid` int(11) DEFAULT NULL,
  `departmentid` int(11) DEFAULT NULL,
  `site` varchar(254) DEFAULT NULL,
  `gh5` varchar(5) DEFAULT NULL,
  `gh6` char(1) DEFAULT NULL,
  `gh7` char(1) DEFAULT NULL,
  `gh8` char(1) DEFAULT NULL,
  `CGI` varchar(20) DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT NULL,
  `valid` tinyint(1) NOT NULL,
  KEY `MCC` (`MCC`),
  KEY `MNC` (`MNC`),
  KEY `LAC` (`LAC`),
  KEY `CellID` (`Cell_ID`),
  KEY `MercureID` (`mercure_cell_id`),
  KEY `Long` (`Longitude`),
  KEY `Lat` (`Latitude`),
  KEY `site` (`cell_name`),
  KEY `region` (`region`),
  KEY `CGI` (`CGI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

After the table headers are set in the MYSQL, upload the data from the IQ "bts" table into the MYSQL "bts_current" table using the file exported from the IQ.
Now you can load the data from the csv file into the MYSQL table using this:
**MYSQL:** 
```
LOAD DATA local INFILE 'c:/bts/current_bts_from_IQ.csv' 
INTO TABLE bts_current
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
```


3. Create another table "bts_new" out of the excel file only with the new BTS cells.
First, create the table headers to be exactly the same as the "bts_current" table headers so it will look like that: 
![image.png](/.attachments/image-5fd6b802-24d0-4df0-ba3d-7e3b73e79180.png) 
By using this script:
**MYSQL:** 
```
CREATE TABLE ta9data.`bts_new` (
  `Operator` varchar(254) DEFAULT NULL,
  `technology` varchar(254) DEFAULT NULL,
  `MCC` int(11) NOT NULL,
  `MNC` int(11) NOT NULL,
  `LAC` int(11) NOT NULL,
  `Cell_ID` varchar(254) DEFAULT NULL,
  `mercure_cell_id` varchar(254) DEFAULT NULL,
  `country` varchar(254) DEFAULT NULL,
  `Longitude` float NOT NULL,
  `Latitude` float NOT NULL,
  `cell_name` varchar(254) DEFAULT NULL,
  `region` varchar(254) DEFAULT NULL,
  `sub_region` varchar(254) DEFAULT NULL,
  `address` varchar(254) DEFAULT NULL,
  `Azimut` varchar(254) DEFAULT NULL,
  `Ouverture` varchar(254) DEFAULT NULL,
  `Description` varchar(254) DEFAULT NULL,
  `fileid` int(11) DEFAULT NULL,
  `caseid` int(11) DEFAULT NULL,
  `departmentid` int(11) DEFAULT NULL,
  `site` varchar(254) DEFAULT NULL,
  `gh5` varchar(5) DEFAULT NULL,
  `gh6` char(1) DEFAULT NULL,
  `gh7` char(1) DEFAULT NULL,
  `gh8` char(1) DEFAULT NULL,
  `CGI` varchar(20) DEFAULT NULL,
  `update_date` timestamp NULL DEFAULT NULL,
  `valid` tinyint(1) NOT NULL,
  KEY `MCC` (`MCC`),
  KEY `MNC` (`MNC`),
  KEY `LAC` (`LAC`),
  KEY `CellID` (`Cell_ID`),
  KEY `MercureID` (`mercure_cell_id`),
  KEY `Long` (`Longitude`),
  KEY `Lat` (`Latitude`),
  KEY `site` (`cell_name`),
  KEY `region` (`region`),
  KEY `CGI` (`CGI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Now you have to edit the excel file as long as you make sure the following conditions are met:
- [ ] Change the format of the text file into a CSV file
- [ ] All columns in the file have a perfect match to the table fields and should be in the exact same order
- [ ] Fill all the Update Date column in the file with the date of today
- [ ] Fill all the Valid column in the file with '1' 
- [ ] If a field appears in the table but does not appear in the file, add it as a new column to the file and leave it blank
- [ ] If a field appears in the file but does not appear in the table, delete the entire column in the file.
Then, you can import the file into the MYSQL table using this:
**MYSQL:** 
```
LOAD DATA local INFILE 'c:/bts/bts_new.csv' 
INTO TABLE bts_new
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
```


4. Set the CGI field in both MYSQL tables ("bts_current","bts_new") based on MCC, MNC, LAC & CELL ID using this:
 **MYSQL:** 
```
update ta9data.**table_name** a
 set a.CGI = concat (a.mcc,a.mnc,a.lac,a.cell_id) 
 where a.mcc !='' and a.mcc is not null and 
 a.mnc !='' and a.mnc is not null and
 a.lac !='' and a.lac is not null and 
 a.Cell_ID !='' and a.Cell_ID is not null;
```


5. Check if there are any new cells of BTS that needs to be uploaded to the updated table using this:
 **MYSQL:** 
```
SELECT Cell_ID FROM ta9data.bts_new
where CGI not in (select CGI from bts_current);
```

If the query returns results, add the new cells from "bts_new" table to "bts_current" table using this:
**MYSQL:** 
```
insert into ta9data.bts_current 
(`Operator`,`technology`,`MCC`,`MNC`,`LAC`,`Cell_ID`,`mercure_cell_id`,`country`,`Longitude`,`Latitude`,`cell_name`,
`region`,`sub_region`,`address`,`Azimut`,`Ouverture`,`Description`,`fileid`,`caseid`,`departmentid`,`site`,`gh5`,`gh6`,
`gh7`,`gh8`,`CGI`,`update_date`,`valid`)
 SELECT `Operator`,`technology`,`MCC`,`MNC`,`LAC`,`Cell_ID`,`mercure_cell_id`,`country`,`Longitude`,`Latitude`,`cell_name`,
`region`,`sub_region`,`address`,`Azimut`,`Ouverture`,`Description`,`fileid`,`caseid`,`departmentid`,`site`,`gh5`,`gh6`,
`gh7`,`gh8`,`CGI`,`update_date`,`valid`
 FROM ta9data.bts_new where CGI not in (select cgi from bts_current);
```


6. Update Lon & Lat fields in "bts_current" table for all existing BTS based on MCC, MNC, LAC & CELL ID using this:
**MYSQL:** 
```
update bts_current a, bts_new b
set a.Longitude  = b.Longitude,
a.Latitude= b.Latitude,
a.cell_name= b.cell_name,
a.region= b.region,
a.sub_region= b.sub_region,
a.address= b.address,
a.Azimut= b.Azimut,
a.Description= b.Description,
a.site= b.site,
a.mercure_cell_id = b.mercure_cell_id
where  
a.mcc= b.mcc and
a.mnc = b.mnc and
a.lac = b.lac and
a.Cell_ID = b.Cell_ID and
a.mcc !='' and a.mcc is not null and 
a.mnc !='' and a.mnc is not null and
a.lac !='' and a.lac is not null and 
a.Cell_ID !='' and a.Cell_ID is not null;
```


7. Update GeoHash fields in both MYSQL tables "bts_current" & "bts_new" using this:
**MYSQL:** 
```
Update  **table_name**
set gh5 = ST_GeoHash(Longitude,Latitude,5)  ,
gh6 = RIGHT(ST_GeoHash(Longitude,Latitude,6) ,1)  ,
gh7 = RIGHT(ST_GeoHash(Longitude,Latitude,7) ,1)  ,
gh8 = RIGHT(ST_GeoHash(Longitude,Latitude,8) ,1)  
where Longitude is not null and Latitude is not null;
```


8. Copy the "bts_current" table data from MYSQL to the "bts" table in IQ by following these steps:
- [ ] First, export all the data of the "bts_current" table from MYSQL and save it as a CSV file named "new_bts.csv".
- [ ] Open the FileZilla application on your local computer and connect to the IQ server (image's top part).
 Then, open the file location in your computer (image's right side) and the path "/opt/data" (image's left side). 
As described in the image below _(IQ server's IP, username & password are located in the passwords excel file)_:
![image.png](/.attachments/image-a6603f1b-8f08-4135-99d6-b809b21dd40d.png)
- [ ] Once you are connected to the server, the file can be transferred to the IQ server, just wait for the Success confirmation.
- [ ] After the file is located in the server, you can import the data to the IQ "bts" table by using this in IQ:
**IQ:** 
```
load table BTS
(Operateur,Technologie,MCC,MNC,LAC,CellID,FULLCellID,Pays,Longitude,Latitude,Site,Rgion,Ragion,Adresse,
Azimut,Ouverture,Description,fileid,caseid,departmentid,site1,gh5,gh6,gh7,gh8,CGI,update_date,valid)
using file '/opt/data/new_bts.csv'
quotes on
escapes off
format bcp
delimited by ','
row delimited by '\n'
skip 1;
```

### Make sure the data is indeed there, perform some count queries, and make sure it has the same amount of data you expect to have and that there is no error in the order of the fields!

9. Update the CGI field in the IQ "bts" table by using this:

**IQ:** 
```
update bts b set b.CGI=
CAST(CAST( b.MCC AS int ) as varchar(30)) 
+ CAST(CAST( b.MNC AS int ) as varchar(30)) 
+ CAST(CAST( b.Lac AS int ) as varchar(30)) 
+ CAST(CAST( b.cellid AS int ) as varchar(30))  
where  isnumeric (b.CellID) = 1
```

10. After you are done with all the steps, the last step is to run a procedure to updated the fadet DM with the new cells and locations.

 11. # DONE!



