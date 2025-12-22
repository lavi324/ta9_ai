**New cells maintenance - Description**

**Note: Read Before you Start!**
--bts2021 is the existing table of cell in MYSQL
--btsnew is the same table as bts2021 (same schema) populated with the new cells 

Make sure you find them and verify they exist as described.


scripts (if needed) :
ALTER TABLE `ta9data`.`bts2021` 
ADD COLUMN `gh5` VARCHAR(5) NULL AFTER `site`,
ADD COLUMN `gh6` CHAR(1) NULL AFTER `gh5`,
ADD COLUMN `gh7` CHAR(1) NULL AFTER `gh6`,
ADD COLUMN `gh8` CHAR(1) NULL AFTER `gh7`;

ALTER TABLE `ta9data`.`bts2021` 
ADD COLUMN `CGI` VARCHAR(20) NULL AFTER `gh8`;

ALTER TABLE `ta9data`.`bts_new` 
ADD COLUMN `CGI` VARCHAR(20) NULL AFTER `Description`;

 update ta9data.bts2021 a
 set a.CGI = concat (a.mcc,a.mnc,a.lac,a.cellid)  
 where a.mcc !='' and a.mcc is not null and 
 a.mnc !='' and a.mnc is not null and
 a.lac !='' and a.lac is not null and 
 a.CellID !='' and a.CellID is not null  ;
 




ALTER TABLE `ta9data`.`bts_new` 
ADD INDEX `CGI` (`CGI` ASC);
;

ALTER TABLE `ta9data`.`bts2021` 
ADD INDEX `CGI` (`CGI` ASC);
;

![image.png](/.attachments/image-14f2e214-fc24-4b23-a859-126b261cfe19.png)

0. preparation 

Create a backup For BTS tables using this:

(select * into bts_backup from BTS)

truncate bts_new table
Upload the new Cells to bts_new table
Backup the BTS table in IQ

1. Add missing Cells 

SELECT CellID FROM ta9data.bts_new
where CGI not in (select cgi from bts2021);



if the query return results - add the new cells to bts2021 using:
insert into ta9data.bts2021 
(`Operator`,`technology`,`MCC`,`MNC`,`LAC`,`Cell_ID`,`mercure_cell_id`,`country`,`Longitude`,`Latitude`,`cell_name`,`region`,
  `sub_region`,`address`,`Azimut`,`Ouverture`,`Description`,`cgi`,`fileid`,`caseid`,`departmentid`,`site`)
 SELECT `Operator`,`technology`,`MCC`,`MNC`,`LAC`,`Cell_ID`,`mercure_cell_id`,`country`,`Longitude`,`Latitude`,`cell_name`,`region`,
  `sub_region`,`address`,`Azimut`,`Ouverture`,`Description`,`cgi`,`fileid`,`caseid`,`departmentid`,`site`
 FROM ta9data.bts_new where CGI not in (select cgi from bts2021);

2. set cgi information

 update ta9data.bts_new a
 set a.CGI = concat (a.mcc,a.mnc,a.lac,a.cellid)  
 where a.mcc !='' and a.mcc is not null and 
 a.mnc !='' and a.mnc is not null and
 a.lac !='' and a.lac is not null and 
 a.CellID !='' and a.CellID is not null  ;



3. Update existing details for exiting records based on MCC,MNC,LAC,CELLID

update bts2021 a, bts_new b
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
a.CellID = b.CellID and
 a.mcc !='' and a.mcc is not null and 
 a.mnc !='' and a.mnc is not null and
 a.lac !='' and a.lac is not null and 
 a.CellID !='' and a.CellID is not null  ;


4. Update GeoHash fields Code

Update  bts2021
set gh5 = ST_GeoHash(Longitude,Latitude,5)  ,
gh6 = RIGHT(ST_GeoHash(Longitude,Latitude,6) ,1)  ,
gh7 = RIGHT(ST_GeoHash(Longitude,Latitude,7) ,1)  ,
gh8 = RIGHT(ST_GeoHash(Longitude,Latitude,8) ,1)  
where Longitude is not null and Latitude is not null;

5. Backup the BTS table in IQ

6. Copy the bts2021 table data to BTS in IQ 

7. Update the CGI field in BTS (IQ)

update bts b
set b.CGI=
CAST(CAST( b.MCC AS int ) as varchar(30))
+ CAST(CAST( b.MNC AS int ) as varchar(30))
+ CAST(CAST( b.Lac AS int ) as varchar(30))
+ CAST(CAST( b.cellid AS int ) as varchar(30))  
where  isnumeric (b.CellID) = 1




