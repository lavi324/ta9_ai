[[_TOC_]]


# 1. Intro
This wiki Describes the basic CRUD fundamentals the Entity Service API supports.

## 1.1 Swagger
To view the Swagger - open the file located in the following Link:

https://ta9comp.sharepoint.com/:f:/r/sites/businessteam/Shared%20Documents/Product/API/Entity%20Service%20API?csf=1&web=1&e=Az2cfE

Path:
Business Team > Product > API > Entity Service API > swagger.yaml

## 1.2 API Calls Mapping File
https://ta9comp.sharepoint.com/:x:/s/devteam/EdsQc5h6hRtJiMMCbMJs9loBr2UIgeszhVVd0eXwl1-9HQ?e=w2ByJn

## 1.3 Documentation
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/Shared%20Documents/Product/API/Entity%20Service%20API/EntitiesAPI%20Documentation.docx?d=w87611f72afc1423ca9adb9b89a666fe3&csf=1&web=1&e=vxINwB


# 2. The CRUD Logic
##2.1 Create
See in Official documentation word file
##2.2 READ
See in Official documentation word file
##2.3 Update
See in Official documentation word file
##2.4 Delete
TA9 API Does not support "Delete" function via API by design. 
When an entity is created in the system, many users can see and use it (depending on the permission level). The users can add the entity to a case, connect to other entities to it, edit the entity & more.

From a functional point of view, if an entity needs to be deleted, it should be deleted for all the users. 
Since the user cannot know who else is using it, deleting it without notice can critically damage investigations & cases.

Also, If an entity is deleted from the system – it will disappear from all graphs and cases, and should be deleted from SOLR db as well. 
For example - I’m using entity X in my case and if another user deletes that entity, it will disappear from my case. 

There are different solutions Instead of deleting, for example, this user can simply remove the entity from his case or change its permission mode to general / Private.

For more information on "delete Entities" visit the following wiki:
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/217/Delete-Entity 
