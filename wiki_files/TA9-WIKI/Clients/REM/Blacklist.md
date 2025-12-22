A blacklist is a list of entities that are regarded as unacceptable/untrustworthy and should be excluded. Adding entities to the blacklist allows marking the entity with a red background in both the grid & link Analysis view.
This feature allows blacklisted entities to be centered in dedicated DM (ID=-402, "הכללות").

[[_TOC_]]
# **Files Location**

Dll & config files are located in:
**Blacklist PLA location**:  C:\Post Loading Actions
- PLA project files (dll, config, pdb)
- Common project files (dll, config, pdb)
- JSON configuration file
![image.png](/.attachments/image-4b8c0a56-6b97-4fbe-86ee-40b6502e501f.png)

**Blacklist  Parser location**:  C:\Program Files\TA9\C#\TA9 Core Services\Plugins\parsers
- Parser project files (dll, config, pdb)
- Common project files (dll, config, pdb)
- JSON configuration file
![image.png](/.attachments/image-41fa6773-bb91-4b45-b6a6-14904ff4754a.png)

Important!!!
The exact configuration file is applied for both projects (Blacklist PLA & Blacklist Parser) but is located in 2 different folders. Any change should occur in both files.
 
![image.png](/.attachments/image-00023d36-29cb-400a-8da3-d0cdd10ad3e0.png)


----------

# **Step 1: How to Identify the Property ID in MySQL Workbench** 

Go to the DM you wish to Blacklist, and search for the EN number in the URL:
![image.png](/.attachments/image-223d7acc-db21-48e7-ba58-5028c1721f92.png)

Go to "em_entity_definitions" table or run this query:
`SELECT * FROM sqlite_metadata.em_entity_definitions;`
Search for the ID of the EN66 entity:
![image.png](/.attachments/image-9a4afcc4-67da-4f84-8580-93e18605a6e4.png)
Note that tey are not always the same as this example.

Knowing the ID (**parentID**) of the entity you wish to insert into the blacklist, go to em_property_definitions table, or insert the query:
`SELECT * FROM sqlite_metadata.em_property_definitions WHERE ParentID = 66;`

* **Recommendation**: Insert a short explanation in the Alias field in each property ID, in order to see the meaning of the value in "Name".
To do so: Go to the Admin Studio > Ontology manager > entity > choose the relevant entity:
![image.png](/.attachments/image-34c3cfc2-5c81-4fec-a32b-b1c4b9820b64.png)
And insert the in the Alias column the description of the column so we can see them in DB.
*clear cache

Now you can filter in Alias:
![image.png](/.attachments/image-1172f692-9e6a-44eb-afa2-65d23649c244.png)



# **Step 2: Apply Configuration Change**

**Config File**
Go to the config file and add the Properties name to the file in the next order (you can use the mapping from step 1 in em_property_definition table):
![image.png](/.attachments/image-0d3feb6f-8419-424f-9ca7-70a7c0f2e6c3.png)

**System Config:**
**Option 1 - via DB:**
1. Go to "system_config" and add the property name of the "הכללה" into ConfigValue:
![image.png](/.attachments/image-d51b4d97-9433-4833-ac99-727b89dfae87.png)
2. Reset the service host.

**Option 2 - via web - RECOMMENDED (client-oriented):**
1. ![image.png](/.attachments/image-03afd590-fbd8-4edc-956d-df52d2e3dee9.png)
2. ![image.png](/.attachments/image-7ec98002-7b4c-4452-b169-aba32f85b07c.png)
3. ![image.png](/.attachments/image-2acd5fbd-1003-4cb9-9e87-e022f7186158.png)
4. ![image.png](/.attachments/image-51864f08-25ae-4edc-b37c-4b006a680f8b.png)
5. ![image.png](/.attachments/image-d68cdc39-4322-4af0-ae00-9ac8a413a10d.png)

6. add the property name of the entity into "הגדרת ערך", and separat by a comma.

7. Reset the Service Host



# **Step 3: Create the CSV for the Parser:**

![image.png](/.attachments/image-2064e51d-f4c7-427e-92bb-57de8b60fe8e.png)

|Field | Value|
|--|--|
| **EntityID** | Entity ID  |
| **Entity Type** |  The name of the entity as it appears in the DB. |
| **Start/End Date** | Must be in the format above: YYYY-MM-DD HH:MM:SS |
| **Related News** | Text (ידיעה מקשרת) |
| **SubscriptionUsers**  | The user ID from "users" table in DB, in order from them to get a notification to their mail, in case they have an email address set |
| **WorldGateBlacklist** | Boolean value |
| **Comment** | Severity blacklist |
| **Lookup** |  Not in use, will be available if neede to set a lookup value |



# **Step 4: Upload the file**

Go to Load File Manager and insert:
<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/b2c491ab-267c-4055-9e0c-e41cbd1ce7c7?fileName=image.png"  alt="Image"/>



# **Step 5: TEST**
1. To see that in הכללות DM you can see red rows which indicate of the blacklisted entities:
![image.png](/.attachments/image-ecd7c8b5-0837-46e8-ad51-500de4189c6b.png)
2. If a mail was set to get notified:
![image.png](/.attachments/image-ff969f08-671b-4376-a9b3-36b474241f9c.png)


---------------------
# **Troubleshooting**


 **1. Blacklist PLA**

### **19/06/23 - Insert Bulk Data Issue:**

We had an issue in REM where Blacklist PLA didn't update the blacklist DM, although the entities were updated successfully, indicating that there is an issue with the InsertBulkData api call, which inserts a new line to blacklist DM.

In the PLA code, the InsertBulkData api call functionality was used through Argus's ReportDispatcher, which threw communication timeout exception. When attempting the same InsertBulkData api call **with the same data** from Postman, the InsertBulkData api call added a line successfully.

After checking with R&D, Argus's dispatcher throws this kind of exceptions when something goes wrong with the api call, could be anything. After a request is sent, if there is no response after a set amount of time, the user will just get that timeout exception without any indication of what went wrong with the request, not even as an inner exception.

Since on REM site we can't even debug, I decided to remove the dispatcher's InsertBulkData use from the PLA, and add a InsertBulkData api call implementation of my own. That way I could log the exception and know exactly what went wrong with the API call.

After some troubleshooting and minor code adjustment on site, InsertBulkData now work and with it the whole Blacklist PLA process.