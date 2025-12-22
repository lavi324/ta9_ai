
[[_TOC_]]
# Feature description

A code-based method that allows the insertion of entities via large data sets (Millions) to the graph DB based on the following files:

1. Sql table containing the entity/relation data.
2. Configuration file (JSON) - Holding DB's connection parameters, and migration parameters (indexing, bulk capacity, and mapping of SQL columns to Orient properties).
3. Executable file - running a Java Jar file that executes the copying process.

>❕ **Notes**: 
> - While the executable is running a log file will be generated
> - You can't insert entities and relations at the same time. The script needs to be run separately for each type of migration, with the field of VertexUpdate controlling the type of migration.
> - If you insert relations - you can insert just one type of relation at once.  


## Prerequisites
- The entity/relation type must exist in the Orient DB before the migration.
- Credentials for the Orient and SQL DB must be in the JSON file.
- Java8 installed.


> **Disclaimer** 
>- This is an external method developed to help with the migration process. 
>- It is an outside tool that is not mandatory to apply. 
>- The migration of relations properties was tested for less than 9 properties per relation. Additional verification requires if trying to migrate a high number of relation properties.

# Preperation Phase 
## Entities Migration

First - Build an SQL table with the following format of the data:

- [ ] **The first column name must be named InternalID**. This first column has to be a unique number ID for each row. This number is used to track the migration process, allowing us to initiate the migration in bulk.

- [ ] The mapping between SQL columns to the entity's properties will be filled in the JSON file.  
 

>❕ **Note**: it is advised to break the large data sets into chunks. Test small amounts and scale up appropriately. Monitor the time it takes to insert and index the entities in each run.

Table example:

|InternalID| Entity Properety 1 | Entity Property 2  | Update Date | 
|--|--|--|--
| 1 | Alex | Barton | yyyy-mm-dd hh:mm:ss | 
| 2 | Miriam | Barton | yyyy-mm-dd hh:mm:ss | 



## Relations Migration

First -  build the SQL table in the following format:

- [ ] ID of the source entity in the relation.
- [ ] ID of the destination entity in the relation.
- [ ] Relation type - the type of relationship between entities.

>❕ **Note:** 
When Inserting relation - only one type of relation can be inserted at each run. 
The Relations Table itself, can contain several relation types in the "relation type" column, but the relation created will be the one mentioned within the JSON config file under the **_EdgeQuery_** Parameter that holds an SQL query of the run (which will be elaborated in the JSON section below).

> **Disclaimers:** 
> - The migration of relations cant be divided into bulks.
> - The migration of the relation is for the relation type, and not for a relation property.


# The JSON file
Open the JSON file called 'orientEntitiesParam.json'. (provided)
The configuration file contains parameters both for entity migration and relations migration. For each type of migration, please make sure all fields are filled in correctly.

> ! **TIP**
In regards to entities migration bulk sizes, it is recommended to start with a bulk of 10-100 when running tests and proceed to a larger amount of migration bulks when migrating real data.
 


**"SqlParams"**


| parameters  | Description |comments|
|--|--|--|
|tableName|Name of the SQL table that you take the data from.||
|LastInsertedIndex|The internalID in the table that migrated last. For example, if you wish to start and migrate the first 1000 data rows, the value should be 0, and the SequenceLength should be 1000. But if you wish to migrate rows 1001 to 2000, the value of this field, LastInsertedIndex, should be 1000, as it was the last SQL row that was indexed  |Only for entities|
|displayTitleFields| This parameter points to the field defined as the "display title" of the entity. It's a **mandatory** field and it cannot remain empty. fill it with the column name of the SQL table, holding the data that should be the entity display title. | You can add one or several fields from your SQL table since an entity can have more than 1 display title defined.|
|freeTextValuesFields| This parameter points to the entity properties defined as "is free text Search". It's a **mandatory** field and it cannot remain empty. Fill it with the column name from the SQL table, holding the data that should be used for searching the entity in Federated Search.|You can add one or several fields from your SQL table since an entity can have more than 1 Free text field defined|
|connectionString  |"jdbc:sqlanywhere:DSN=**DSN NAME**", Change the "DSN NAME"  | to find the DSN name of your IQ: open ODBC app -> click on the 'system DSN' tab![image.png](/.attachments/image-c91888d5-fdc0-4fa1-a8ae-9edb92693991.png) |
|edgeQuery| Holds the SQL query responsible for the relations migration. The returned table will contain the data migrated to the Orient. We should insert the column names of both entities we want to add a relation, from which table it's being read, and the conditions of the SQL Query. If we wish to migrate relations properties as well, we should add to the query the columns that holds the property values. |Only for relations.  For example: **_SELECT  InternalId1, InternalId2, RP117_1, RP117_2, RP117_3 FROM sqlTableName_** |
|ColumnsMappers| Each column name in the SQL table should be paired with the entity property ID from Orient. Make sure the property names are written the same and in the same order. **The internal row\entity ID columns will be mapped in the VertexParams section**. | ![image.png](/.attachments/image-fa83ecbd-12d4-436e-810b-5a38049ac423.png) Only for entities |

**"FileParams"**
Please Leave Empty. Not relevant for SQL table migration.


**"EdgeParams"**
| parameters  | Description |comments|
|--|--|--|
| EdgeName |  The ID of the relation. For example RL1. | Only for relations |
|VertexForEdges1|The ID of the source entity type. for example: EN1.|Only for relation|
|VertexForEdges2|The ID of the destination entity type|Only for relation.|
|VertexForEdgeProperty1|The property ID of the internalID field in the source entity. for example: EP1_1.|Only for relation|
|VertexForEdgeProperty2|The property ID of the internalID field in the destination entity. |Only for relation|
|EdgePropertiesMapper|This section should contain the mapping of the properties of the relations. This section takes into account the order of the returned columns from the Edge Query. Please note that the left side of the mapping must be numbered with an initial of '00'.  The left number in the mapping represents the order of the columns returned from the edge query, and the right side of the mapping represents the relation property we would like to migrate data to. |Only for relation properties. For example:![image.png](/.attachments/image-f7b7e39c-3749-477a-9606-2f9fcd5cb668.png)|


**"VertexParams"**
| parameters  | Description |comments|
|--|--|--|
| VertexName | The ID of the entity type you're migrating data to. **For example: class:EN90** | ![image.png](/.attachments/image-d4384645-fc1c-441f-8467-61876d701178.png) Only for entities|
| internalId | Mapping of the internal ID from SQL to the entity property on orient. **For example:internalId":"EP90_1** | ![image.png](/.attachments/image-4d5c7814-69e9-400c-b9d1-70b9e8e26fb3.png) Only for entities|

**More params - Orient DB**

| parameters  | Description |comments|
|--|--|--|
| OrientUrl |  URL of the orient in the environment you want.(Remote:**IP**/TA9)|Mandatory|
|OrientUserName  | User name for the orient. |Mandatory|
|OrientPass | Password for the orient. |Mandatory|Mandatory|
|SequenceLength  |When migrating entities this parameter is responsible for the bulk size. Enter the amount of entities in the table you want to insert (For Example: 100000). When migrating relations, make sure the number is equal to the number of rows in the table returned from the edge query.|Mandatory|
| Permission mode | Choose the permission mode of the entity from the following:![image.png](/.attachments/image-6a7a08d1-bda4-4d1b-b8aa-daa8e518cee3.png)   |Only for entities|
|Permission Value | Depends on the permission mode. If public then it's irrelevant, if private - enter the user id. If it's case or department, enter the case id or department id. 
| VertexName | The ID of the entity type. **For example: EN1** |Only for entities| value is the cases that you want to give permission to)  |  Only for entities|
|VertexUpdate| True - entities migration. False for relations migration|False/True 
|ImportFromSql| If the import is from DB table - True |False/True


# Executing the process

## Inserting the data
1. Create a folder called: orientMigrationCad. Located at c:\

1. The folder needs to include -
-the JSON file - orientEntitiesParam.json
-the execution file - OrientMigrationCad.jar

![image.png](/.attachments/image-86121d1a-9ce3-432d-8d3c-9ee4a9d4f1f0.png)

## Running The code file - OrientMigrationCad.jar

To insert the entities into the orient you need to run this code file called OrientMigrationCad.jar

1. Click on the execution file (OrientMigrationCad.jar)
* OrientMigration.log - logs file created automatically in the folder.  

* OrientMigration.log.lck- created automatically and disappears when the upload is completed. 

- The orient last row in the orientMigration.log file indicates on process ending successfully. 

## Testing and results

- When the process ends the file "OrientMigration.log.lck" will disappear, keeping only the log file "OrientMigration.log". without any errors. 
- Now, you can open TA9 IntSight and see if the entities/relations appear. 

