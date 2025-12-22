# Description

Unified view is a data model that presents location data from several sources (Like CDR, LPR,  Face recognition and more location-based sources).

In order to add new source to the view do the following steps:

## 1.Backup

First of all do a backup table to the Unified Locations view.

- Open the DBeaver.
- Open the Unified location table.
- Click on properties tab. 
- Click on Definition.
- Copy the creation script.

![image.png](/.attachments/image-4a1940ba-dd87-4eac-9ce2-df597ddd952c.png) 

- Open new sql script and past the script
- Change the table name to Unifide_locations_backup
- Run the script -> A backup table will created. 

![image.png](/.attachments/image-60345e46-e137-45ba-9760-7c7f2b697c33.png)

## 2.Add new source 

- Open Unified locations table.
- Click on properties tab. 
- Click on Definition.
- Copy the script and past it in a new tab.
- Add to the end of the script this script in order to add a new source :
```
union all
select 'DATA_TABLE_NAME' as "Source",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Longitude",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Latitude",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Phone",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Imei",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Imsi",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "Cell",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "ActionDate",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "CaseId",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "MCC",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "MNC",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "LAC",

    "DBA"."DATA_TABLE_NAME"."FIELD(home_mcc)"+
    "DBA"."DATA_TABLE_NAME"."FIELD(home_mnc)"+"DBA".
    "DATA_TABLE_NAME"."FIELD(lac)"+"DBA"."DATA_TABLE_NAME"."FIELD(cellid)" as "CGI",

    "DBA"."DATA_TABLE_NAME"."FIELD" as "EntityId",
    "DBA"."DATA_TABLE_NAME"."FIELD" as "DetectionId"
    from "DBA"."DATA_TABLE_NAME"

    where((....) ***Just if its needed.
;
```
DATA_TABLE_NAME-the name of the source table that you want to add.

FIELD-the field in the source table that matched to the field in unified location.

**NOTE**- if you have no match field you can write NULL **for example**: NULL as "EntityId"

- Delete unified locations table (Right click on the name of the table and delete)
- Run the script with the new source and the unified location table with the new source will be created.

Example for source to add to the script
![image.png](/.attachments/image-9efe454f-8e2e-4f2c-8646-f0106fa0e047.png)


    
