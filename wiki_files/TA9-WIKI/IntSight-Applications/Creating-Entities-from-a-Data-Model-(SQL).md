[[_TOC_]]

# **Capability description**
This capability allows Creating entities from a Data model. 
Each row in the data model will become an entity.


#**Prerequisites**
- Entity / relation definition must exist.
- Entity properties must exist.
- The Data model that will be used to create the entities must contain an ID column, which will be the same ID in the entity itself (e.g: Identity Number of a person)
- Relations Defined (can only be created once the entities exist)
- The fields at `sqlite_metadata.dataschemafields1`, The columns of the data table defined in "DBTableName" at `sqlite_metadata.dataschema1` and the properties at the table `em_property_defintios where ParentId = 'ENXX'` should ALL be the same names and match the fields in Orient.  (**NOTE**: There was an update in the 3.9.x Service Update that uses a mapping option. More info can be found in this document below)
- Properties without FieldVisibility should at least have the value **|6|**

<br>

![image.png](/.attachments/image-1803d7cf-f9ca-4811-8fb6-69f3c345c0aa.png)

![image.png](/.attachments/image-ab2142a3-9f12-4b96-9402-1085b82203a6.png)

![image.png](/.attachments/image-9410823a-799e-4455-a408-1a5d3a71dda7.png)

---

#**Entity Creation**:
##_**Step 1: The entity Data model**_
Creating the Data model with the following columns - example:
- IdOfPerson - must have property
- EP44_1=Prop, 
- Sys_LastUpdatedOn=Must+RoleSequence

Notes: 
- 'Prop' means a dynamic property, can be named anything, I just gave an example.
- Must Mandatory field
- IsId - ID value of the entity - should be marked as "IsID" definition in both Data model and Entity - MUST be unique field. Two fields can not have this trait.
- Last Update date - needs to be defined as "Sequence" role (the date should be later than the last indexing date on the Indexing audit, the system cant index items in the past)
- you need to create a Column for each property you wish to update - using the Property name (under "Name" column) in the following schema:
SELECT * FROM sqlite_metadata.em_property_definitions where ParentID = {EntityID}


Once you've created a data model (one for each entity type) you can proceed to the next step.

<br>

##_**Step 2: Indexing Service - Entity Creation**_
2.1 Adding a new record in the indexing_sources Table (`SELECT * FROM sqlite_metadata.indexing_sources`)
- ID= Your Entity DmId (Id of the data model created in step1) 
- DATA_SOURCE_TYPE = "DataModel"
- CONNECTION_ID = Your Entity CONNECTION_ID (usually is Orient -12)
- INDEXING_INTERVAL=30 
- INDEXING CRON = What time the process will be run, For example, Every day at 09:15 = `0 15 09 ? * *`
for more options check here:https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html 
**Note** - you don't have to fill this field, if this field is null the process running by the indexing interval  
- DESCRIPTION= just normal description  
- IS_ACTIVE=1 (0 = wont be indexed) 
- BULK_COUNT=1000 (amount of records drawn from the data model on each operation)
- BATCH_ID= Order of indexing processes as a batch that runs together, give the same number for all the processes in the batch
- BATCH_ORDER= Order of the indexing processes in a specific batch (the first process =1, second=2 ...) 

<br>

2.2 Add a new record in the table indexing_sources_stores (1SELECT * FROM sqlite_metadata.indexing_sources_stores1)
- SOURCE_ID=Your Entity DmId (Id of the data model created in step1)
- MORE_INFO=44 (The ID of the Entity type e.g. "EN44")
- STORE_TYPE=4 (Fixed value - 4 is the value for entity creation out of a Data Model) 
- STORE_CONNECTION_ID=-100 (Fixed) 
- STORE_CONNECTION_IS_ENDPOINT=0 (Fixed) 
- IDENTIFIERS_MAPPINGS_LIST=NULL 
- STORE_BULK_COUNT=100

Note: The MORE_INFO column is the id of the Entity/Relation, for example, EN44/RL41, Put there the number only.

<br>

##_**Step 3: Restart and Verify**_ 
Restart the Indexing Service to start the creation process and Clear Server Cache through Admin Tools in the Web Client.

You may have a look at the table indexing_audit in order to verify. 
`SELECT * FROM sqlite_metadata.indexing_audit where index_source_ID=xxx`
See item count and Items fetch values to see if any data was found and indexed:

![image.png](/.attachments/image-927cd93b-2770-4a7c-8661-1cdc2f64977b.png)


## **3.9.x Service Update!**

On 02/04/2023 2 major changes were made On the Indexing service:

- Each store has it own query for indexing. it simplifies change detection and error handling.
indexing will continue until no new entries were found
indexing_interval is tail to head approach ==> the interval between the end of indexing to the next indexing
in case of an error in the process, the error shall appear in the column error description of the index audit table. 
indexing DM to entities now supports mapping, similar to relations indexing.

- DM columns no longer need to have entity property names. It now may have an arbitrary column name, used to lookup in existing entities using JSON Mapping (AKA "Additional Params" Json.

If the existing entity was found it would be updated, otherwise it will be created. 
> Note: If more than 1 entity is found existing, an update will occur for the first entity found.


###Dictionary:
- Mode =  1 Entity, 2 Relation
- Type = the entity type
- DefinitionPropertyName - entity property name (EPxx_xx)
- FilePropertyName - DM column
- Scope = 1 normal entity property, 4 Key entity property (identification)

### Mapping JSON Sample
Sample mapping should be set for the "Source Store" in the _"additionalinfo"_ column:

``` 
   {
        "Id": null,
        "Mode": 1,
        "Type": "EN107",
        "FilePath": null,
        "Extension": null,
        "MoreInfo": null,
        "Mapping": [
            {
                "DefinitionPropertyName": "EP107_1",
                "FilePropertyName": "key",
                "Scope": 4
            },
            {
                "DefinitionPropertyName": "EP107_2",
                "FilePropertyName": "plate",
                "Scope": 1
            },
            {
                "DefinitionPropertyName": "EP107_3",
                "FilePropertyName": "key",
                "Scope": 1
            },
            {
                "DefinitionPropertyName": "EP107_8",
                "FilePropertyName": "country",
                "Scope": 1
            },            
            {
                "DefinitionPropertyName": "EP107_11",
                "FilePropertyName": "prop11",
                "Scope": 1
            }
        ],
        "OrderNum": 0,
        "NewFileID": 0,
        "OriginalFileName": null,
        "Tags": null,
        "CaseID": 0
    }
```




---
- >**note**: If the 'Additional Params' column is missing from the table - run the following script to add it back :

```

ALTER TABLE `sqlite_metadata`.`indexing_sources_stores`
ADD COLUMN `ADDITIONAL_PARAMS` TEXT NULL AFTER `STORE_BULK_COUNT`;

CREATE OR REPLACE
    ALGORITHM = UNDEFINED
    DEFINER = `root`@`localhost`
    SQL SECURITY DEFINER
VIEW `indexing_sources_stores_view` AS
    SELECT
        `iss`.`SOURCE_STORE_ID` AS `SOURCE_STORE_ID`,
        `iss`.`SOURCE_ID` AS `SOURCE_ID`,
        `iss`.`MORE_INFO` AS `MORE_INFO`,
        `iss`.`STORE_TYPE` AS `STORE_TYPE`,
        `iss`.`STORE_CONNECTION_ID` AS `STORE_CONNECTION_ID`,
        `iss`.`STORE_CONNECTION_IS_ENDPOINT` AS `STORE_CONNECTION_IS_ENDPOINT`,
        `iss`.`IDENTIFIERS_MAPPINGS_LIST` AS `IDENTIFIERS_MAPPINGS_LIST`,
        `iss`.`STORE_BULK_COUNT` AS `STORE_BULK_COUNT`,
        `iss`.`ADDITIONAL_PARAMS` AS `ADDITIONAL_PARAMS`
    FROM
        `indexing_sources_stores` `iss`
    UNION SELECT
        `dm`.`SchemaID` AS `SOURCE_STORE_ID`,
        `dm`.`SchemaID` AS `SOURCE_ID`,
        0 AS `MORE_INFO`,
        0 AS `STORE_TYPE`,
        (SELECT
                `dc`.`ConnectionID`
            FROM
                `dataconnectionsmanager` `dc`
            WHERE
                ((`dc`.`ConnectionName` = 'solr')
                    AND (`dc`.`ProviderName` = 'solr'))) AS `STORE_CONNECTION_ID`,
        0 AS `STORE_CONNECTION_IS_ENDPOINT`,
        '29:Weapon' AS `IDENTIFIERS_MAPPINGS_LIST`,
        1000 AS `STORE_BULK_COUNT`,
        NULL AS `ADDITIONAL_PARAMS`
    FROM
        `dataschema1` `dm`
    WHERE
        ((`dm`.`IsIndexToFederatedSearch` = 1)
            AND (`dm`.`IsSupported` = 1))
```



#**Relations Creation**
Repeating the Steps only configuring differently:


##Method 1 - Using Sys_ID
**_Step 1:_**
1. Creating the Data model with the following columns:
- FromEntityId=Must+IsID (Sys_Id of the source entity - As it appears on the DB)
*(the column name must remain "FromEntityId")

- ToEntityId=Must (sys_Id of the target entity - As it appears on the DB) 
*(the column name must remain "ToEntityId")

- DisplayTitle=Must 

- RP41_1=Prop (example of a property in the relation)

- RP41_2=Prop (example of a property in the relation)

- Sys_LastUpdatedOn=Must+RoleSequence

*Note that the entity & relation definition and the entities themselves should be created in the system in order to succeed creation of relations.

<br>

_**Step 2: (Same as # 2 before)**_
2. Indexing Service - Relation Creation
- Adding a new record in the indexing_sources Table (SELECT * FROM sqlite_metadata.indexing_sources;)
- - ID=YourRelationDmId, 
- - DATA_SOURCE_TYPE=DataModel, 
- - CONNECTION_ID=YourRelationCONNECTION_ID, 
- - INDEXING_INTERVAL=30,
- -INDEXING CRON = What time the process will be run, For example, Every day at 09:15 = `0 15 09 ? * *`
for more options check here:https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html 
**Note** - you don't have to fill this field, if this field is null the process running by the indexing interval
- - DESCRIPTION=NULL, 
- - IS_ACTIVE=1, 
- - BULK_COUNT=1000
- - BULK_COUNT=1000 (amount of records drawn from the data model on each operation)
- - BATCH_ID= Order of indexing processes as a batch that runs together, give the same number for all the processes in the batch
- - BATCH_ORDER= Order of the indexing processes in a specific batch (the first process =1, second=2 ...) 

**_Step 3:_**
Add a new record in the table indexing_sources_stores:
- SOURCE_ID=YourRelationDmId, 
- MORE_INFO=41 (relation ID)
- STORE_TYPE=5 (Fixed for relation creation) 
- STORE_CONNECTION_ID=-100
- STORE_CONNECTION_IS_ENDPOINT=0,
- IDENTIFIERS_MAPPINGS_LIST=NULL 
- STORE_BULK_COUNT=100

**_Restart and Verify_**
Restart the Indexing Service
inspect the Indexing Audit schema and check if the Data model was indexed.

--- 

##Method 2 - Using Property values
This method allows the creation of links between different entity types, based on the values appearing in the entity property. In this method, you don't have to use the Sys_ID, or any Key ID field of an entity, yet it must be a value that can Identify the entity like name, address, number, and so on.

> **Important Note!** 
> - In this Method - please make sure that you mark all fields in the entity properties as "Is Quarriable" and the entities have a display title
> - In case the entity value appears more than once, and the properties are not defined as ID, a relation will be created on the first entity found.
 
**_Step 1:_**
1. Creating the Data model with the following columns:
- ID - Row ID = IsID, Must
- LastUpdateDate = Sequence, must
- From Entity = The column name for the source entity - Can use any column name
- To Entity = The column name for the destination entity - Can use any column name
- Relation property Name = Property in the relation, not mandatory. 

> _**Note**: Don't Use "From" and "To" field names in the data model since they are reserved names._ 

<br>

_**Step 2: (Same as # 2 before)**_
2. Indexing Service - Relation Creation
- Adding a new record in the indexing_sources Table (SELECT * FROM sqlite_metadata.indexing_sources;)
- - ID=Your Relation DM ID, 
- - DATA_SOURCE_TYPE=DataModel, 
- - CONNECTION_ID=Your Relation CONNECTION_ID (usually is Orient -12), 
- - INDEXING_INTERVAL=30,
-- INDEXING CRON = What time the process will be run, For example, Every day at 09:15 = `0 15 09 ? * *`
for more options check here:https://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html 
**Note** - you don't have to fill this field, if this field is null the process running by the indexing interval
- - DESCRIPTION=NULL, 
- - IS_ACTIVE=1, 
- - BULK_COUNT=1000
- - BULK_COUNT=1000 (amount of records drawn from the data model on each operation)
- - BATCH_ID= Order of indexing processes as a batch that runs together, give the same number for all the processes in the batch
- - BATCH_ORDER= Order of the indexing processes in a specific batch (the first process =1, second=2 ...) 

**_Step 3:_**
Add a new record in the table indexing_sources_stores
(SELECT * FROM sqlite_metadata.indexing_sources_stores;):
- SOURCE_ID=Your Relation DM Id, 
- MORE_INFO=41 (relation ID)
- STORE_TYPE=5 (Fixed for relation creation) 
- STORE_CONNECTION_ID=-100
- STORE_CONNECTION_IS_ENDPOINT=0,
- IDENTIFIERS_MAPPINGS_LIST=NULL 
- STORE_BULK_COUNT=100
- ADDITIONAL_PARAMS - Json Configuration that should contain the mapping info:

```{
  "Mode": 2,
  "Type": "RL**xx**",
  "CaseID": 0,
  "Mapping": [
    {
      "Scope": 2,
      "FilePropertyName": "**Name1**",
      "DefinitionPropertyName": "**FROM_EPxx_x**"
    },
    {
      "Scope": 2,
      "FilePropertyName": "**Name2**",
      "DefinitionPropertyName": "**TO_EPxx_x**"
    },
    {
      "Scope": 2,
      "FilePropertyName": "**test**",
      "DefinitionPropertyName": "**RPxx_x**"
    }
  ],
  "OrderNum": 0
}
```


_Description:_
-   **"Type":** the relation ID created Like "RL**16**",
-   **"FilePropertyName":** Data model Field name (not display name) of the source/destination Entity or relation property.
-   **"DefinitionPropertyName":** Use the text "FROM_"/"TO_" + add The Id of the entity property like EP16_1 or RP100_2


In this JSON Array, first, add the entities info, and after the relation info.

_**Step 3: Restart and Verify**_ 
Restart the Indexing Service to start the creation process and Clear Server Cache through Admin Tools in the Web Client.

--- 

# **Update an existing Relation property**

From March 2023 we can use the indexing service to update an existing relation property.
The data model should be configured as mentioned above, and new rows will update every relation property with an updated "last updated" date. 

Note:
- Date format (Sys_LastUpdatedOn) by this format: yyyy-mm-dd hh:mm:ss (e.g. 2023-03-10 12:05:00)
- When Updating relations between entities without ID, an update will occur only if 1 matching record is found in the entity data.

---
# **Update - New table for last index time**

open the table : SELECT * FROM sqlite_metadata.indexing_audit_status_mv;
This table shows the last index time for each data model. If you need to change the last index time, you need to do it from this table. During the indexing service work, the service uses the 'last index time' from this table to determine if new data needs to be indexed (changed behavior from using the 'last index time' from the indexing_audit table)

---
# **Update - New table for indexing audit status**

open the table : SELECT * FROM sqlite_metadata.indexing_tasks_audit;
This table shows indications of errors in the indexing processes per indexing source. Meaning, if there is an error in the indexing process of creating entities or relations, the error will appear there. 

---
Relevant Tickets:
https://dev.azure.com/ta-9/Argus/_workitems/edit/37679/
https://dev.azure.com/ta-9/Argus/_workitems/edit/46413/
https://dev.azure.com/ta-9/Argus/_workitems/edit/46500/
https://dev.azure.com/ta-9/Argus/_workitems/edit/46670/
