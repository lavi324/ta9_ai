**Blacklist Entity**

Adding entities to the blacklist allows marking the entity with a red background in both the grid & link Analysis view.
This feature allows entities to be centered in dedicated DM.

[[_TOC_]]

##*1 Define Blacklist Entity*
Steps to define a blacklist feature on an entity:

1. Open the "Admin Studio"
2. Navigate to the "Ontology Manager" and choose the "Entity Definitions" option
3. Search for or create the entity that you want to be able to blacklist
4. Create the blacklist properties and fill the following fields:

- Blacklist  
-- Data Type: Boolean
-- Alias: Same as title
-- Visible & Query Builder
-- Queryable
-- Notify on Change
-- Dependency Role: None

- Start Date
-- Data Type: Date
-- Alias: Same as title
-- Visible
-- Notify on Change
-- Required
-- Dependency Role: Visibility, Blacklist = True

- End Date 
-- Data Type: Date
-- Alias: Same as title
-- Visible & Query Builder
-- Required
-- Queryable
-- Notify on Change
-- Dependency Role: Visibility, Blacklist = True


- Related Yedia
-- Data Type: Text
-- Text Length: 50
-- Alias: Same as title
-- Visible
-- Multi Value
-- Notify on Change
-- Dependency Role: 
  * Visibility = Blacklist = True
  * Parent lookup - operator = "not empty"


- Is Blacklist שער עולמי
-- Data Type: Boolean
-- Visible
-- Notify on Change
-- Dependency Role: Visibility, Blacklist = True

- Comments
-- Data Type: Text
-- Text Length: 255
-- Visible
-- Lookup: moclal_saar_olami
-- Notify on Change
-- Dependency Role: Visibility, Blacklist = True

## 2 *How to Identify the Property ID in the MySQL Workbench* 
1. Locate the Parent Entity ID in the Entity definition screen on Admin Studio.

![Screenshot_3.png](/.attachments/Screenshot_3-779ded74-ac5b-4e9a-8881-9cffca7c6032.png)

2. On the SQL Workbench open the 'Entity definitions' Schema and locate the entity ID
For example: 
SELECT * FROM **sqlite_metadata.em_entity_definitions** where Name = 'EN2'

![image.png](/.attachments/image-66003d15-5817-4622-8d8f-743d534be618.png)

3. Locate the Property ID in the Schema called 'entity property definition'
For example: 
SELECT * FROM **sqlite_metadata.em_property_definitions** where ParentID = 2

![image.png](/.attachments/image-2393de38-ab41-4f37-a7ca-e6d6e166e16e.png)

4. From the results locate the blacklist property and copy its ID 
For example:
EP2_23 (Format: EP[entity ID]_[property ID])

![image.png](/.attachments/image-1b3d4bae-fb94-4d95-88e2-d79c9a247b31.png)

## 3 *Add additional missing properties*
1. Copy a row from 'sqlite_metadata.em_property_definitions'

2. Paste the row and change the relevant fields. Don't forget to change the row number

3. To add a 'Required' property, change the field 'IsRequired' to '1'

## 4 *Configure Dependency in the MySQL Workbench*

1. Locate the 'dependency role type ID' in the Entity dependency roles in the SQL Workbench

For example:
SELECT * FROM **sqlite_metadata.em_dependency_roles** where PropertyDefinitionID=1476

DependencyRoleTypeID = 1 -> Visability
DependencyRoleTypeID = 4 -> Parent Lookup
ParentPropertyDefinitionID = 1473 (the blacklist property ID)
OperatorID = 1 -> '='
OperatorID = 16 -> 'Not Empty'
Value = 'True'

![Screenshot_4.png](/.attachments/Screenshot_4-09925b9d-a8db-4adb-8453-b063a25253d8.png)


How it looks from the Admin studio:
![image.png](/.attachments/image-c97e6aeb-fbfc-4fb6-96e3-c4d1d0e8b9fd.png)


## 5 *Configure Lookup in the MySQL Workbench* 

1. On the SQL Workbench open the 'sqlite_metadata.em_property_definitions' and find the 'Is Blacklist שער עולמי' under 'Alias'
2. Change in the 'LookupValue' the NULL value to 'moclal_saar_olami'

## 6 *Apply Configuration to the web client*

1. From the Web system, log in as an admin and go into the "system configuration" tool under "Admin Tools" Tile.
2. Look for the Config Value (Under Web Client Config) called: blackListPropsIDs
3. Insert the Blacklist Property ID of the entity (For example: EP2_23).

![image.png](/.attachments/image-40bd85a5-701a-4abf-850f-b32ee1e57e8d.png)

## 7 *Activate the changes in the system*

1. Open the "Services" in the server
2. Locate the "TA9 Service Host" and restart it

![Screenshot_2.png](/.attachments/Screenshot_2-10d20baf-8a5b-4300-9daa-5521055e2cfc.png)




