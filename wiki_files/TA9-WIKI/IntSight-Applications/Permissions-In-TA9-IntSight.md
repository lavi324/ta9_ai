# 1.	Permissions In TA9 IntSight

[[_TOC_]]


TA9 IntSight permissions allocation range is broad and support distribution of permissions on several levels:
- Actions permission – Granted to a specific user, defining the actions the can do in TA9 IntSight
- Data models permission - Granted to a specific user, defining which models and categories they’ll be able to access
- Case members permissions & profile - Granted to a specific user or department, defines which cases they see
- Apps & dashboards - Granted to a specific user, defining which applications and dashboard they are allowed to use.

On another note, TA9 IntSight have the ability to allocate permission on the data itself using a proprietary definition called “permission mode” and “permission Value”.

Permission mode – defines if a certain data model or entity is limited, or public:
- Public / None– everyone can see.
- Private – Creator and admin can see.
- Case – restrict access for privileged cases.
- Department - restrict access for privileged departments.

Permission Value – If a data model or entity was defined as limited, this property defines the use case of which the data can be accessed. 
For example: 
Permission mode was set to be “Case”, so permission value is set to whichspecific Casesthe data “belongs” to, allowing the members of these cases to view it, while others are not exposed to it. 

In the following chapters, well review the different permission aspects and learn how to apply them.

## 1.1.	Actions Permissions (Admin)
The Action Permissions Admin module is designed to provide the admin user with the ability to allocate actions permissions to an analyst user.

![image.png](/.attachments/image-43c9c80f-d8c0-457a-b935-6c87bc3153b8.png)
 

### 1.1.1.	View Federated Search permission
This Permission will allow the user to access the Federated Search Module from: 
-	Side Bar (3.0 and above) 
-	Enterprise search widget from the Portal (3.0 and above) 
-	Allow navigating to FS module from Right Click on Text (from Data models & Link Analysis)
### 1.1.2.	View Main Graph permission
-	Access to the main Graph module via a Direct URL or Navigation bar
-	View entity &relations in acase via “Cases app”>“Entities Tab”
Note: If the Permission is set to False, the entities tab will be seen only in “tiles” viewing mode
-	Allow Sending entities to the Main Graph From 
•	Federated Search
•	From entities
-	View the Link analysis skin From Data Models (where the links are defined)
-	View the graph from“Entity” page > “Relations” tab.
Note:If the Permission is set to False, the entities relations will be seen only in grid mode: 
-	View the ontology layout (from Admin Studio)or via direct link: /definition-graph  

### 1.1.3.	View Map permission
-	Access the main map module Via URLor Navigation bar
-	View map from an “entity” pageby clicking the Location Icon (Entity must have location values and Main roles definitions on longitude and latitude properties)  
-	View The Map from“Cases” App >“Details” Screen 
-	View map Skin from Data models 
Note:In case the default skin is Map the user will be navigated to Grid view 
-	Use the map from Data model analysis Tools:
o	Advance / Quick Filter (Main long / Lat definitions must apply on longitude latitude columns) 
o	Query Builder 
o	Cluster Query 
-	View map from the Federated Search Advance Filters 
-	View Dashboard map widgets 
### 1.1.4.	Load Data permission
-	Access the “Data loader” screen Via URLor Navigation bar“+” Menu
-	Allows loading of entities, relations & Data  
-	Allow loading data from “cases”>“Data” Tab 
Note:Case permission profilemust support that with “load data to case” permission) 
### 1.1.5.	Download permission
Allow download of data using the “download” Icon from media viewer.
### 1.1.6.	Save permission
Allows Saving of entities, cases, tasks &more. 
### 1.1.7.	Create Entity permission
-	Allow creating entities from the “+”menu.
-	Allow editing of an entity. 
Note: In case this permission is set to False, users will still be able to access the entity, but not to edit. 
-	Allow to Edit relations definitions between entities. 
Note:In case this permission is set to False, users will still be able to access the relation, but not to edit.
-	Allow to create new relations between entities from the main graph or entities tab in “cases” app (case contributors only). 
### 1.1.8.	View Annotations permission
Allows users to view & Access the “annotations”bar.

Edit Annotations permission
Allow users to write & Edit Annotations.

### 1.1.9.	View Map Layer Tree permission
Allow viewing the layers tree on any map view.

### 1.1.10.	View Insight permission
Allow viewing of insights strip 

### 1.1.11.	View Feed permission (3.0 and above)
Allowing getting Feed notifications in the personal portal Feed widget  

### 1.1.12.	View Alerts permission
Allowing navigating to the “Events”page and viewing events notifications by URL or navigation bar
### 1.1.13.	Export permission
Allows exporting capability from: Data models, dashboard*, main graph, map.

*Dashboard export require additional license.
###1.1.14.	Correlated Items permission
Allow Filtering Correlated* Items actions on right-click. 

*Correlation logic should be defined & applied by system integrator.
###1.1.15.	Add Dashboard permission

-	Allows adding a new Dashboard to the system by clicking the “+”button from the navigation bar or access the creation window via URL.
-	Access from the Dashboard tile in applications module
###1.1.16.	Edit Dashboard permission
-	Allows editing an existed Dashboards in the system by clicking the edit button 
-	Direct access to the editing page via URL 
###1.1.17.	Delete Dashboard permission
Allows deleting an existed Dashboards in the system by clicking the delete button 
###1.1.18.	Create Case permission
Allows create a new case in the system by clicking the “Create Case”button in the navigation bar or the main portal > Cases widget.
###1.1.19.	Audit Data Models permission
-	Allows access to the Audit folder in Data Models, such as:  
o	System Audit 
o	Login Audit 
o	Session Audit 
o	Query Audit 
-	Access from the Audit tile in Home Page / Data Models 
-	Direct access to the Audit data models category via URL /Home/4/-2 

Note: the user must be granted with allthe Audit data models in “Admin Studio”Data Modelstile.
###1.1.20.	Delete Relations permission
Allow the user to delete relation between two entities by right clicking on the relation 

Note: Requires Create Entity permission
###1.1.21.	Private Entity permission
Allows the user to set the permission mode of an existing entity to Private.

Note: 
-	Requires Create Entity permission.
-	Admin users still maintain access
###1.1.22.	Create Task permission
Allow the user to create new task by clicking on the “+” sign. 
Tasks can be created from the personal portal, tasks Kanban and task data model  

## 1.2.	Case Profile Manager(Admin)
In the Case Profile Manager, the admin can create profiles that define the actions that will be allowed to do in the case by choosing the relevant action from the list:
-	View Case details – View the first (main) tab of the case to see its details
-	Edit Case details - Edit the first (main) tab of the case to see its details
-	Reopen case –Allows to change a “closed” case status to an “open” one
-	View Case data – View the “data” tab
-	Upload data – Add new data to the case
-	Manage case entities – Add or remove case entities
-	View Case Audit – View the audit tab
-	Member management – Add or remove case members
-	Edit Case Summary – Edit the rich text editor in the “summary” tab
-	Export summary* - make an export of the rich text editor

*Note: to export summary the user must be an active member in the case. More details on managing case members is available in “case management” section.
###1.2.1.	Reopen Case permission
A specific level of permission support to allow the permitted user to re-open a case defined as “closed”.
In order to decide what is considered a “closed Case” status, TA9 IntSight holds in its data base an indication in the statuses table a flag whether the status is considered “opened” or “closed”.

To affect this configuration and decide which case status is considered as “closed” turn to you system operator with the proper definition.
## 1.3.	Granting permission to a user for data models, apps and more (Admin)
When a New user is added into TA9, the admin should allocate the user with a set of permissions, defining what he/she can do Or see in TA9 IntSight.

To grant the permission, open the “Admin Studio” application, in the “Users” tile, and select the user you wish to update:

![image.png](/.attachments/image-bd613f32-ac75-4c7b-84c9-d6ed608ec03e.png) 

Now, start adding permissions to the user according to need, from the available tabs:
-	Data models – Which data sources & categories the user can see
-	Cases – Which cases the user can see (note that you need to add a profile for the case as well, so you can also allocate case permission from the web application)
-	Actions – the available modules and actions the user may perform
-	Apps – Which applications the users can see and access
-	Dashboards – Which dashboards the users can use (note that since the dashboards are working on actual data – the user should be getting the access to the data sources as well).


 
## 1.4.	Permission Modes
Permission Modes are used in data models and entities, in order to define to what data a user is exposed to. 
 
![image.png](/.attachments/image-8a7e9622-3220-4886-80e9-00d1d02fb3a2.png)

When a data model or entity is defined as “restricted permission” using a permission mode –it will limit the user allowing to see it only after granted with permission.

	
The Different Types of permission modes are:

Permission mode – defines if a certain data model or entity is limited, or public:
- Public / None – everyone can see.
- Private – Creator and admin can see.
- Case – restrict access for privileged cases. 
- Department - restrict access for privileged departments.

Permission Value – If a data model or entity was defined as limited, this property defines the use case of which the data can be accessed. 

For example: 
Permission mode was set to be “Case”, so permission value is set to which specific Cases the data “belongs” to, allowing the members of these cases to view it, while others are not exposed to it. 


 
### 1.4.1.	Data model Permission Modes
To update permission mode for a data models, open the “repository” properties, and locate the “permission section in it:

![image.png](/.attachments/image-fb39d026-9019-46e5-a7fe-88f5d5802450.png)
 
Note: In order for permissions on data in a data model to be enforced, the model must contain some internal system columns, populated with data:

-	“caseid”–the Id of the case the data should belong to
-	“departmentid” – The ID of the department that is permitted to view the data
-	“fileid” – the ID of the file loaded (in case you want the data model to receive new loaded data, it should also be defined as “is Managed” data model

**Types of Permission modes:**
•	Public / None – everyone can see.
•	Case – restrict access for privileged cases. Case Id is added to the data row
•	Department - restrict access for privileged departments. Department Id is added to the data row
•	Mixed/Custom – Used for unique permission requirements, designed to build the query from an external source.
 
###1.4.2.	Entity Permission modes
Users have the ability to give permission to an entity via the application
In creating a new entity: Open the system properties at the bottom 

![image.png](/.attachments/image-7916e3cd-a356-4389-bf0c-262ebf8ab2eb.png)

In updating entity: Click on info

![image.png](/.attachments/image-fb734a0d-dcac-4335-a7e4-4a71c8e42133.png)

There are two fields:
**Permission Mode -** 
- Public / None – everyone can see.
- Case – restrict access for privileged cases. Case Id is added to the data row
- Department - restrict access for privileged departments. Department Id is added to the data row
- Private–restrict access only to the creator of the entity .

**Permission Value –** 
After choosing permission mode you need to choose permission value (The values change depending on the Permission Mode)
For example – If the permission mode in case the permission value will be a case list and only users assign to this case will see the entity.
