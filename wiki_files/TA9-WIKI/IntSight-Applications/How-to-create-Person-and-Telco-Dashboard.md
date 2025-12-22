## Data Source
1.Add the the data sources (data models that the plugins based on).
If you need to create data models that exist in another environment:

copy the data models from :
|  |  |
|--|--|
|`SELECT * FROM sqlite_metadata.dataschema1;`|DM definition |
|`SELECT * FROM sqlite_metadata.dataschemafields1;`|DM fields definition  |
|`SELECT * FROM sqlite_metadata.userdatamodels1;`| User permission for the DM |
|`SELECT * FROM sqlite_metadata.datamodelgrouphierarchy1;`|Where the DM will appear in the system. (For the data models main page FatherID = -1)   |



## Configuration
1.Run the query `SELECT * FROM sqlite_metadata.system_config;`

2.Add the cofiguraion of the Telco/Person dashboard.

![image.png](/.attachments/image-7a2ed217-bd2b-4c39-81f8-7869ac90104a.png)

3.Add  Json configuration file-must be placed in C:\Windows\System32 .


| | Person Dashboard  | Telco Dashboard  |
|--|--|--|
|File Name|"PersonDashboardConfiguration.json"|"IsuzuConfiguration.json"|
|  |Change the URLs and the DMs ID | Change the serverURL ,the DMs ID and Name Fields|
|File content |![image.png](/.attachments/image-bf625442-1f8c-46a5-85f8-abd3cd3b184f.png) | ![image.png](/.attachments/image-191f2748-d9e8-4daf-a656-46cf611501d5.png)  |

## Create the Dashboard

1.Copy dll's to plugins folder.
C:\Program Files\TA9\C#\TA9 Core Services\Plugins\DM

*You have to copy this DLLs:

- ExtensionUtils.dll
- TaExtensions.DataContract
- Newtonsoft.json.dll
- PersonDashboardUtils.dll


![image.png](/.attachments/image-39523fa7-d730-41f5-8a99-f4de18364b37.png)

2.Create DM's from dll's

- Add the dll - ExtensionUtils.dll to the folder (you have to do this first)
![image.png](/.attachments/image-c79bc8d3-bc30-4bb9-8c95-865a5506a3f2.png)

Way1:

- copy the DMs from the sql DB (dataschema1,dataschemafields1,datamodelgrouphierarchy1,userdatamodels1)

Way2: 
- Go to the Admin Studio
- Data Models -> Add data connections->Plugin
- add plugin you want to create DM from , add user name and password to the admin studio and click on ok.

![image.png](/.attachments/image-f7bc7e0f-091e-45b1-93f9-65f4bf7bba16.png)

The columns added automatically, click on save.

![image.png](/.attachments/image-21510cce-2b84-4522-ac7b-de6ea0bcda05.png)  

3.Create dashboard

Go to the system -> Apps -> Dashboards -> click on create dashboard->
Add dashboard name and click on  save changes.
![image.png](/.attachments/image-f882d97a-6c99-4eee-890e-48a963f6eaa0.png)


4.Run the Query
`SELECT * FROM sqlite_metadata.dsb_dashboard_definitions;`

find the ID of the dashboard and add Layout

![image.png](/.attachments/image-4ff23702-6100-4af1-a44e-b633b15f1441.png)

- Right-click on the layout
- Click on open value in editor
- Click on Json tab 
- Change the schemas ID to the ID of the data models you created.
- Click on apply

![image.png](/.attachments/image-f38b2771-4bab-4ef6-8353-bb2e6c659fbf.png)

![image.png](/.attachments/image-a4e8b5f2-cc87-4a23-bad2-0c9c25200981.png)

**Telco Dashboard -** change the value in 'defultRelativeDateID' field to be 6
(Make the dashboard to search just in lest month by defult).

|  |  |
|--|--|
| 0 | None |
| 1 | Last Minute |
| 2 | Last Hour |
| 3 | Today |
| 4 | Last Day |
| 5 | Last week |
| 6 |Last Month  |
| 7| Last Year|

5.Run the query 
`SELECT * FROM sqlite_metadata.dsb_dashboard_widgets;`
copy all the widgets with the Dashboard ID .

### Lookups
You have to add the lookups:


|  Lookup name | Table name |Table content  |  
|--|--|--|--|
|investigation_status_no_trans | investigation_status |![image.png](/.attachments/image-bbe3ec37-fa9a-4fbd-86d7-80900ba6489c.png)  |  
| mcc_to_country_name |mcc_to_country_view (view table)  | ![image.png](/.attachments/image-698cea44-9def-4d44-adc2-908fe18d68b1.png) |  
| uni_source | uni_source_lookup | ![image.png](/.attachments/image-8aa0fbea-118d-4875-8409-542d11c6deea.png) |  

1.copy / add the lookup tables 

2.Run the query `SELECT * FROM sqlite_metadata.lookupmanager;`
Add the lookups into this table.
*Make Shure the ConnectionID, Objectname and LookupName are correct. 

![image.png](/.attachments/image-cbf37353-c715-4fe4-b6c2-73d6d9e5a7c4.png)






Run the query

INSERT INTO `sqlite_metadata`.`lookupmanager` (`LookupID`, `LookupName`, `ConnectionID`, `KeyMember`, `ValueMember`, `ConditionStatement`, `ObjectName`, `IsActive`, `IsSystem`) VALUES `('125',` `'investigation_status_no_trans', '-5', 'ID', 'Status', '', 'sqlite_metadata.investigation_status', '1', '0');``

* note that the LookupID not used.

### Identifiers

**Telco dashboard-** 
Run the query `SELECT * FROM sqlite_metadata.sensors_identifiers;` 

Add the identifiers:(sensorID = the DashboardID-Telco)
1.Phone
2.IMSI
3.IMEI
![image.png](/.attachments/image-51f4506e-bc2f-47ee-9c9d-14b4fbde064d.png)


