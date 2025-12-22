[[_TOC_]]

## Data Source
1. Add the data sources (data models that the plugins rely on).
If you need to create data models that exist in another environment:
- Go to the admin studio->data models->add data connection->MySQL/IQ (where the data model is located). 
- Connect to the environment you want to copy the data model and click ok.
- Select the data model you want to add from the list and save. 
*the columns will be created automatically* 

![image.png](/.attachments/image-091fc801-3abc-48b2-a9fd-937380052365.png)
 
![image.png](/.attachments/image-2e8ee43e-3399-4c62-937f-023728faf89c.png)

2.Add Json configuration file (PersonDashboardConfiguration.json)- 
must be placed in C:\Windows\System32.
Change the Server URL and the id numbers of the data models (data source).

![image.png](/.attachments/image-0dfaa5aa-6527-4bd7-9e9d-af026f647f9a.png)

## Configuration
1.Run the query `SELECT * FROM sqlite_metadata.system_config;`
2.Add the cofiguraion of the dashboard.

![image.png](/.attachments/image-a80f4270-6d94-41ce-bc09-86d38c899f07.png)

## Create the Dashboard

### Copy dll's to plugins folder.
C:\Program Files\TA9\C#\TA9 Core Services\Plugins\DM
![image.png](/.attachments/image-1f3b9baf-f27f-4e49-84ff-e478cdfa8ea0.png)

### Create DM's from dll's

Go to the Admin Studio
Data Models -> Add data connections-> Plugin
add plugin you want to create DM from, add user name and password to the admin studio and click on ok.

![image.png](/.attachments/image-f7bc7e0f-091e-45b1-93f9-65f4bf7bba16.png)

The columns will be added automatically, click on save.

![image.png](/.attachments/image-21510cce-2b84-4522-ac7b-de6ea0bcda05.png)  

### Create dashboard

Go to the system -> Apps -> Dashboards -> Click on create dashboard ->
Add dashboard name and click on  save changes.
![image.png](/.attachments/image-f882d97a-6c99-4eee-890e-48a963f6eaa0.png)

### Run the Query
`SELECT * FROM sqlite_metadata.dsb_dashboard_definitions;`
find the ID of the dashboard and add Layout

![image.png](/.attachments/image-4ff23702-6100-4af1-a44e-b633b15f1441.png)

- Right-click on the layout.
- Click on open value in editor.
- Click on the Json tab. 
- Change the schemas ID to the ID of the data models you created.
- Click on apply.

![image.png](/.attachments/image-f38b2771-4bab-4ef6-8353-bb2e6c659fbf.png)

![image.png](/.attachments/image-a4e8b5f2-cc87-4a23-bad2-0c9c25200981.png)

Run the query 
`SELECT * FROM sqlite_metadata.dsb_dashboard_widgets;`
copy all the widgets with the Dashboard id .

* Make sure that "photo file path" field on unified subscribers DM view is custom path view.
* Make sure that all the DMs in the following file exist when creating a person dashboard.
https://ta9comp.sharepoint.com/:x:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B5F124E64-D6AC-4649-ACB4-932926E29D52%7D&file=Dashboards_mapping.xlsx&action=default&mobileredirect=true&cid=f4c25a8e-7faa-4a32-b334-cfb2907c214f


## Create Passport ID-Numero Piece views:
In order to filter existing dashboard plugins with passport ids, 2 views have to be created in order to match passport id to numero piece. 
design: https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7BB2694DA7-F7A8-47DB-972C-01FA920A0C7B%7D&file=Person%20Dashboard%20By%20Passport.docx&_DSL=1&action=default&mobileredirect=true
(views attached: [immigration_passports.txt](/.attachments/immigration_passports-8d672d7f-4cd8-467e-b40b-22662eab0f31.txt), [unified_cni.txt](/.attachments/unified_cni-1fd966d9-a385-44e7-b90e-c8e43210550f.txt)):

1. immigration_passport:
![image.png](/.attachments/image-4bc51797-5a1a-4786-881d-d657bd2a8489.png)

2. unified_cni:
![image.png](/.attachments/image-8ba22d4a-49f8-4ff9-9809-b70d54022699.png)




## Deployment Stages

Json configuration file - must be placed in System32.

We need to change URL value - according to IP in production environment. We have to update the content of the file (DM numbers and field names).

According to real values in prod.

Copy dll's to plugins folder.

Create DM's from dll's ( or copy definitions from dataschema1 and dataschemafields1).

Create Dashboard ( or copy definitions from dsb_dashboard_definitions and dsb_dashboard_widgets).

User permissions (userdatamodels1).

Create passport id to numero piece views (attachedimmigration_passports.txtunified_cni.txt)

#### *Possible Problems*
null value - make sure json file is loaded correctly
if there is problem with specific widget - need to check the proper working of DM that this widget based on.

There are certain values hardcoded in plugins - check the names of the fields according to dataschemafields1.

## Set only ID identifier


in MySql metadata DB go to table sensors_identifiers - add numero_peice identifier number, or other relevant identifier

![image.png](/.attachments/image-cd454685-4db1-40ed-a2d4-4443a1f11a2a.png)

## Set special skin to dashboard widget: Most Recent Photo

In MySql metadata go to sqlite_metadata.dsb_dashboard_definitions

On dashboard level set skin value to special skin ( 26 ) in layout field

![image.png](/.attachments/image-0a49a74d-810c-4e42-acc0-e336bbabf850.png)