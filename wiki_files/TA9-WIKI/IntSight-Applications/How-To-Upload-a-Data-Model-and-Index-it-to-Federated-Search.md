To Index a Data model into Federated search it has to contain 2 main conditions:
1. Key column must exist (with a unique key for every row, marked as "IsId" on Admin studio
2. A Last update date with a "Sequence" role definition applied on it, where the date is in reference to the actual time the data will be loaded to the system.

# ***Step 1:***
 **Create a data model and save it as a csv file**

This is an example of a data model: 
![image.png](/.attachments/image-174f35f0-933c-4bd3-9485-de203071e34d.png)

- Column 1 - is the "Key" value - giving every row a unique ID
- Column 2 - is defined as "Is Free Text" on Admin, notifying the system what text it should index
- Column 3 - the "Last update date" aka the date of the actual uploading time (has to be the current time and lo later than the last date of the previous indexing interval done. You can view the last indexing time by running the following SQL line: SELECT * FROM sqlite_metadata.indexing_audit order by CREATED_ON desc;
<BR>
Example: If the last indexing interval was done Today at 5/04/2022 10:10:36 (see "Created_ON value)  - The "Last_update_date" value should be later than that.
 

![image.png](/.attachments/image-9a7f72a4-a44c-4170-b86e-5243daedfc95.png)

-----
#***Step 2:***
**Open the Admin Studio and choose Data Model:**
![image.png](/.attachments/image-d558f302-a3b7-4ae2-98e9-705ba625f00c.png)
![image.png](/.attachments/image-977fdb34-7677-4269-9644-c193b78a7b68.png)
choose this data connection:
![image.png](/.attachments/image-cb50ce3a-e4d4-4228-a982-aeb930df0dc0.png)
and insert the text file:
![image.png](/.attachments/image-5889dcbb-95d5-463b-9edb-c3c6423cc1ce.png)

#**Step 3:**
Open the Data Model section un the Admin Studio:
![image.png](/.attachments/image-52f5a00f-9315-4c79-88c9-b5086a3abd60.png)

Find the DM you uploaded:
![image.png](/.attachments/image-0fc8d096-2484-4854-8b8e-43b8111abf5d.png)

Insert the following definitions to the ID column:
![image.png](/.attachments/image-f6d3cc2d-de8b-4105-9917-809ef2a9b77f.png)

Set any definition you wish to the other columns in the DM:
![image.png](/.attachments/image-bf4c023e-bb6a-4725-abda-fca609f73401.png)


Set the following definitions to the "last update date" column:

![image.png](/.attachments/image-0ad072a7-8d58-469e-bc55-188620ddbad0.png)
save the settings:
![image.png](/.attachments/image-a6b4f3de-5fb5-473f-a59a-2ad48ab9083e.png)


#***Step 4:***
Load the Data & Open the data model

#***Step 5:***
Wait ~10-30 min for the next indexing interval. 
you can see the data was indexed by running the SQL line as follows on the Indexing_audit schema:

![image.png](/.attachments/image-c0065782-ad46-4962-965d-adfe2a7cb167.png)

*NOTE: add the data model ID in the line
SELECT * FROM sqlite_metadata.indexing_audit where INDEX_SOURCE_ID=X order by CREATED_ON desc;

*NOTE2: you can try resetting the "TA9 indexing service / TA9 Service host to make the force indexing. 

*NOTE3: If the "Is_error" = 0 then the indexing process was successful 

#***Step 6:***
Open the data model and try to see if the data was indexed and can be found on FS.

![image.png](/.attachments/image-c2f30cf0-9ab5-4305-a6dc-e9e75fde06f3.png)
Search for the Data Model you uploaded:
![image.png](/.attachments/image-06a8b593-240c-413f-b60a-d7c8f88d34d3.png)
Display the data:
![image.png](/.attachments/image-f175884e-8ad0-400e-ac65-cc15edb3d752.png)
Color the field you want to search in the FS > right click on it > click "Federated Search":
![image.png](/.attachments/image-f523e0fa-e8f8-444e-a32e-d7e684422ef6.png)
The FS is retrieving the searched data:
![image.png](/.attachments/image-a1f2f05e-1603-4bc4-a045-3aa52918d1f7.png)

---------

**_NOTE_**
In case this is a **New Data Model**, you need to reset the Indexing Service, follow the next steps to do so:

1. Open **putty** application (connecting to the Java Server, to the wildfly machine), with the relevant IP:
![image.png](/.attachments/image-f0914e26-d3fc-47f4-89bd-cb906274ee17.png)

Enter user name and password to this window:
![image.png](/.attachments/image-5b194bf5-7ace-49c2-a468-826b4aac07be.png)

Enter this command:
`systemctl restart indexing.service`
and click enter
![image.png](/.attachments/image-59fb9290-eadb-49a4-ac83-286e1ac68bfb.png)

Now you can verify the DM in the system.

------------------

You are required to do the following steps while creating and saving **a new external data connection**:

1. Choose the relevant schema and **save** the data model **without** modifying the fields. 
2. Once the data model was saved, you can set the field properties such as: is ID, is free text, and sequence.
3. **After** saving the two steps above you can open the "repository" and choose the index to FS.

If you will change the definition of the field before saving the initial DM (step 1), the system will automatically add a new field called "system_comment" which is a system field for annotation, which caused the indexing problem. 

Following your specific situation when you tried to connect an external DB table to a DM in our system, we saw that the data model was not indexed, because the "system_comment" field was created in the dataschemafields1 automatically, but was not existing in the original table that you have connected. 

**So, here's what you can do in that case:**
In the dataschemafields1 table, you need to change the value of the "system_comment" filed "isvalid" to 0 instead of 1 - meaning turning this field to be inactive.  **Or**,  add to your original table the "system_comment" field and save it. 

Make sure you **reset the indexing service** once the data model is ready to indexing