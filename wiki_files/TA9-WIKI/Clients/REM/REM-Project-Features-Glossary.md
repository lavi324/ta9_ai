[[_TOC_]]
# Comparison between local environment (60) and on-site environment
[Entities and Data Models ID's](https://ta9comp.sharepoint.com/:x:/r/sites/devteam/_layouts/15/doc2.aspx?sourcedoc=%7B63188fc5-2e01-45d9-9c17-a36627461174%7D&action=editnew)

# 1. Enriched Entity

- [Enriched Entity - Wiki](/TA9-WIKI/Clients/REM/Enriched-Entity)

- [Auto increment ID - AKA Event Sequence / Prefix](/TA9-WIKI/Clients/REM/Add-a-prefix-to-every-newly-created-entity)

 - Related Entities Tab - entities with relation to this entity will appear in this tab

 - Create Entity from Enriched entity (+)

Configuration

1. open the system config On Mysql (SELECT * FROM sqlite_metadata.system_config;)
2. Put the correct values 

In the local environment 10.100.102.60:
![image.png](/.attachments/image-5196ad26-3aca-4049-8a70-e1c9c87bfa2d.png)

# 2. Calculated fields

[Calculated date Filed ](/TA9-WIKI/Clients/REM/Calculated-date-field) 

# 3. Black list - (Hachlala)
 
Local Data model ID = -402
On-site Data model ID = -280

[How to Create Black list entity-Wiki](/TA9-WIKI/Clients/REM/Creating-a-Blacklist-Entity)

[Black list configuration + DLLs](/TA9-WIKI/Clients/REM/Blacklist)

**Auto-complete ידיעה מקושרת property lookup in blacklist entity, based on the 'נושא ידיעה' property in 'ידיעה' entity:** [45333](https://dev.azure.com/ta-9/Argus/_workitems/edit/45333)
Taking data from an existing field in 'ידיעה' entity ('נושא הידיעה') and turning the data in it into a lookup field in the Blacklist Entity ('ידיעה מקושרת'). The lookup auto-completes the data in the search field based on the user's search.
![Screenshot_10.png](/.attachments/Screenshot_10-d2f7405f-e4c1-4309-be4c-07b77e8daad9.png)
![Screenshot_11.png](/.attachments/Screenshot_11-48f5ecee-64ce-48ff-81b2-bbcb038334b9.png)

**Parser** - 'הכללת ישויות' parser, for the 'הכללות' data model. 
You can upload a CSV file with the blacklist entities for the following uses:
- Create new blacklist entities
- להכליל black list entities and update other properties data
- להוריד הכללה from blacklist entities and update other properties data

There is some information about the possess in the following: [46200](https://dev.azure.com/ta-9/Argus/_workitems/edit/46200), [45338](https://dev.azure.com/ta-9/Argus/_workitems/edit/45338), [Blacklist](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/661/Blacklist), [Loading black list entities](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/518/Loading-black-list-entities), 

**PLA** - the הכללות data model, collects all blacklist entities with their data, whether the entities are מוכללים or not. For any change, update, or creation of a blacklist entity, whether the changes are made directly in an entity or they happen while uploading a CSV file (with all changes) using the Parser 'הכללת ישויות'.

 ## Red marked configuration

Run this query :`select * FROM sqlite_metadata.system_config where ConfigKey ='blackListPropsIDs';`

Add to the configValue the property ID of the field "הכללה" in the entity

## Related entity

Run query:
SELECT * FROM sqlite_metadata.em_dependency_roles;

Should be a row with those values : 
- DependencyRoleTypeID: 4 (Parent Lookup)

- PropertyDefinitionID:  the id of property ידיעה מקשרת 

- ParentPropertyDefinitionID: property id of the property: נושא הידיעה  

- OperatorID: 16 ('Not Empty')

-  Value:  EN+@entityid2

- StateID: 1

- SourceType: 2

- OrderNum: 1

- CreatedBy: 3

- CreateOn: date of today (in format: 2022-10-11 00:00:00)

Parses + loading from file

# 4. Notify on Change 
A feature in entity - if a user wants to get a notification for any changes in a specific entity property.

**Definitions in the Admin Studio:**
1. Enter Ontology Manager
2. Enter the Entity
3. Enter the Property definitions
4. Mark the 'Notify On Change' checkbox![image.png](/.attachments/image-cb50406d-23b1-4f1e-9f7e-647890c1f01d.png)
5. Save entity changes
6. Clear Server and Client cache

**On the Insight web client interface:**
1. Enter a specific entity
2. Enter the 'Info' tab
3. In the Subscribers property add subscribers (a user with a defined email address) ![image.png](/.attachments/image-14fe21c7-b7ec-44bc-9259-dc47572dfc45.png)
4. Navigate back to the entity's 'Home' page
5. Change the property data
6. Save changes

**Changes notifications will appear for the subscribed user in:**
- The Feed widget in the portal
- User's Email address

**The emails for subscribers can contain data for:**
- **New** (data in the property)

Email template in English:
Hi '@user',
The “@entity” had been created:
The @field field was set to ____
Open entity (link)

Email template in Hebrew:
![image.png](/.attachments/image-8e7f57c0-4736-4949-b92c-b8dde72d5488.png)

- **Update** (data in the property)

Email template in English:
Hi '@user',
The “@entity” entity with the title "@entity_title" had been updated:
The @field field was changed to ____
Open entity (link)

Email template in Hebrew:
![image.png](/.attachments/image-5aa7cf20-69f0-4857-9176-fc41e4d20c3a.png)

# 5. Hzharot
2 Parsers
Local Data model ID = 417
On-site Data model ID = 385?

The fields in the data table should be named column1, column2, column3...
![image.png](/.attachments/image-29e9e91a-bf4b-4f54-9222-53003222e6e4.png)

The format of uploading a file:
[יבוא פלסטיני 89221.xlsx](/.attachments/יבוא%20פלסטיני%2089221-c9763e6a-1978-4aa2-8a52-b455809bc773.xlsx)
[יבוא ישראלי.xlsx](/.attachments/יבוא%20ישראלי-8d2d09cf-19be-45a5-87c8-b895222e2fe0.xlsx)

![image.png](/.attachments/image-273a9f81-bc0a-4f26-b9c2-14188b42b156.png)

Exampels we have in **local** environment and **on-site** environment:
[יבוא ישראלי.xlsx](/.attachments/יבוא%20ישראלי-6ed28b6f-623b-4e10-9a67-01ac0daa0d2a.xlsx)
[יבוא פלסטיני.xlsx](/.attachments/יבוא%20פלסטיני-2e712e18-c049-43ee-9bed-60603232f36b.xlsx)

# 6. Insigts 
[Insights Configuration](/TA9-WIKI/Clients/REM/Insights)

- Entity Insights - When there's an existing entity linked to Yedia / EH

- Identifier Insights - when appears on the equivalent data model 

# 7. Plugins 
Sapakim meshutafim - appears only **on-site** environment.

After adding this plugin here and doing some research- we'll add an explanation about this plugin. - updates appear in this ticket [45824](https://dev.azure.com/ta-9/Argus/_workitems/edit/45824)

# 8. Scripts

**DeclarationNoFileExtensionFix** - In order to view files in DM `Hazarot`, there's a need to update the fileName cell with an extension.
There are ~130,000 files in the folder and ~30,000,000 entries on "`hazarot`" table on site.
The script that was there up until recently worked at a pace of ~1 second per opertaion, meaning a full cycle would run in about 36 hours.
I (`Hai`) have revised it lately to run in about 15 minutes. The code is still on Reem site and needs to be transferred to us so we can push it to our repository.
Without going into every line of code, there are two operations:
1. Update single value cells (file name: `12347843` to file name: `12347843.jpg`)
2. Update multi piped value cells (file names `12347843|12347844` to `12347843.jpg|12347844.jpg`)

Since it is running in the same exe, some code is commented, then the code is compiled, then run is order to fix single values; then the first code is commented, compiled again and then run in order to fix multi values. (Please fix it to two projects when the code arrives).

You'd need to know the folder path and the db tbale location. Before any operation do it on a test table and after verifying everything works well, do it in production.

Basically, the code runs in batches instead of running for every file name. Also, I have added "`file_names_handled`" row in the table, in order to skip handled files in the `SELECT`. Please review this section before because let's say a multi piped value arrived with 3 names but only one was updated. if that is the case, we do not want to update with "`file_names_handled = 1`". So maybe in the meantime, update only single values with "`file_names_handled = 1`"


# 9. Department Tiles on Portal 

[Wiki on Departments creation](/TA9-WIKI/IntSight-Applications/Create-Department-and-Users-%2D-Active-Directory)

# 10. REM Icon
REM's icon should appear in the following places:
- Login page ![image.png](/.attachments/image-dd6c7f3a-15ba-40ca-9979-68811f4cdf5f.png)
- Portal ![image.png](/.attachments/image-997d26d4-6466-4d63-95ea-8ecbbdad98d0.png)
- Navigation bar ![image.png](/.attachments/image-bd5b1472-905f-4794-9011-6e64aa876341.png)
- In any chrome tab ![image.png](/.attachments/image-3f0d6e8d-8425-48a9-a9e0-05830ef1746f.png)

# 11. OCR
Ticket- [38998](https://dev.azure.com/ta-9/Argus/_workitems/edit/38998)

# 12. Data model Metadata
This is a data model that aggregates all data models. It shows the **count** and **last update** for each data model.

In the column chooser, there is a "comments" column.
The following messages will display for each one of the options:
1. When there aren't any Count and Date: "Missing a 'Field Role - Sequence Date' in a date column and 'Is ID' or 'Group Name = count' definition in any column"
2. When there is only Count: "Missing a 'Field Role - Sequence Date' in a date column"
3. When there is only Date: "Missing 'Is ID' or 'Group Name = count' definition in any column"
4. When there are Count and Date: it will stay empty

Test Case for data model metadata - [40743](https://dev.azure.com/ta-9/Argus/_workitems/edit/40743)

# 13. Multi Gallery viewer
The feature has been overrun in the local environment and in the production environment.
The tickets that are related to this feature:
[40725](https://dev.azure.com/ta-9/Argus/_workitems/edit/40725)
[38792](https://dev.azure.com/ta-9/Argus/_workitems/edit/38792)
[40309](https://dev.azure.com/ta-9/Argus/_workitems/edit/40309)

# 14. New DM and autoloaders
* "הצהרות ייצוא"
* "תיקי חקר"
* "יומן רכב"
* "תיקי רכב"

# 15. Entity Sort by Sys_LastUpdatedOn

To change the entities data models to be sorted by the 'Sys_LastUpdatedOn' field, need to change the definition of - dataschemafields ***view*** .

**make backup to the view definition before changing it!!!**
click alter view and change the row (in the second part of the union): 
from: "0 AS `SortMode`," 
to:         (CASE
            WHEN (`em_property_definitions`.`Name` = 'Sys_LastUpdatedOn') THEN 1
            ELSE 0
        END) AS `SortMode`,
