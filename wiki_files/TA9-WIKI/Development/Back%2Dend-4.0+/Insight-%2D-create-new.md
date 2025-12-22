**there are 4 types of plugin in the system** :
-**Plugin** -  Data Model Plugin – create new data model – can even create data model that takes data from several different databases 
**Parser**- take data from file and insert it to existing data model with manipulation ( convert int to string, take only several columns and exec)
**PLA**- post loading action that is not a part of backend code 
**Insight**- is a PLA that gives analyzed info on DM

**Insight guidelines** 
- use the relevant NuGet's (see below).
-insight config should be in Jason file in the project (the can replace it when they upload the container- configuration shouldn't be change during running only in deploy!)
![image.png](/.attachments/image-3d49253c-b78c-4fa5-9c6c-9d92f5c2334c.png)


download the following projects : 
common.extension - ne insights will be here 
be-net-extension.sample - template
isuzu.extension- old plugins 


**relevant NuGet's :** 
![image.png](/.attachments/image-3480b8ef-6f6c-4958-8b62-db8ee14e8c0b.png)

add those lines to csproj because there are in unrelease mode :
  
	  <PackageReference Include="TA9.IntSight.Ext.SDK.API" Version="4.1.*-*" />
	  <PackageReference Include="TA9.IntSight.Ext.SDK.Core" Version="4.0.*-*" />
	  <PackageReference Include="TA9.IntSight.Ext.Wrapper" Version="4.0.*-*" />

first deploy of the service should be done by Dekel.


**Insight Payload** 

* dataFields: The DM fields configurations - Related table 'dataschemafields1'
* dataModelId: The DM the insight is running on - Related table 'dataschema1'
* jsonData: The log complex query results, AKA the DM data rows - Can be found in the web socket, But make sure that you address the escape characters

Example for a very simple payload:
Note that this payload is shortened for better reading experience, but it should include **all** the DM fields

`{
    "dataFields": [
        {
            "dataType": 1,
            "fieldID": 12345,
            "fieldName": "FromPhone",
            "fieldRole": 8,
            "identifierTypeID": "1",
            "lookupName": null
        },
        {
            "dataType": 1,
            "fieldID": 54321,
            "fieldName": "case",
            "fieldRole": 8,
            "identifierTypeID": "1",
            "lookupName": null
        }
    ],
    "dataModelId": 125,
    "jsonData": "[{\"case\":2,\"FromPhone\":\"77523\",\"id\":1092,\"Sensor\":\"passive\",\"ToMSISDN\":\"77523\",\"FromIMSI\":\"52666\",\"ToIMSI\":\"52019\",\"TDate\":\"2018-06-26T00:00:00\",\"FromIMEI\":\"52019\",\"ToIMEI\":\"37500\",\"CallDuration\":20,\"CallType\":\"call\",\"FromCell\":\"71631\",\"ToCell\":\"32388\",\"ToLongitude\":100.18,\"ToLatitude\":13.76,\"FromOwner\":\"Unknown\",\"ToOwner\":\"Unknown\",\"ToCity\":null,\"FromCity\":null,\"indexid\":\"989\"},{\"case\":5,\"FromPhone\":\"234967\",\"id\":1808,\"Sensor\":\"probe\",\"ToMSISDN\":\"6687\",\"FromIMSI\":\"5258043\",\"ToIMSI\":\"524669\",\"TDate\":\"2014-08-20T00:00:00\",\"FromIMEI\":\"38458\",\"ToIMEI\":\"3608\",\"CallDuration\":0,\"CallType\":\"Data\",\"FromCell\":\"56345\",\"ToCell\":\"73\",\"ToLongitude\":100.1,\"ToLatitude\":13.13,\"FromOwner\":\"Unknown\",\"ToOwner\":\"Unknown\",\"ToCity\":null,\"FromCity\":null,\"indexid\":\"999\"}]"
}
`


**Insight Table**
The insight configuration can be found on "sqlite_metadata.insights"


![image.png](/.attachments/image-1cc29ef6-5c15-4e19-8e24-e11a9e17998a.png)

**Insight configuration in Admin Studio**

The main Admin Studio page has the Insight configuration button

![image.png](/.attachments/image-63b8575a-8f15-4d43-8e46-635795bd3fb2.png)

You can add a connection for the new Insight via this page, by clicking on the 'New' button on the top right
* Url: If we are still developing, we can enter our local URL, If the Insight is ready (and uploaded by the Devops) we enter the real URL
* Insight Module: We have 2 options, '1' for entity insight and '0' for the DM insight (more common)
* Insight Permissions: Public permission ('1') and department permission ('0'), the relevant department permissions will be found on 'insight_departments'
* API Key: Will be generated automatically when we add a new insight via the Admin Studio

![image.png](/.attachments/image-1737d058-0a34-4b5a-a6fa-f7b7ef420283.png)