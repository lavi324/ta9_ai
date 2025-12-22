[[_TOC_]]

#Introduction
Basic instructions on how to download and use the TACopy tool - used for copying DataModel and Entity Definitions.

#Install
Copy the program binaries from : \\\10.100.102.13\share\Installs\Ta9 utils\TACopy or build from repository.

#How To use
1. Start the program.
2. Fill in the fields.
2.1 For data models fill in only the upper fields, for Entities fill all of the fields.
2.2 Upper fields are the credentials of the MySQL instance , and the bottom ones are the credentials of the TA9 app.

![image.png](/.attachments/image-7f199484-31e9-4b56-8359-cb93daa36662.png)


#CREATING a DM using TACOPY

When copying a DM to another environment, first, you need to enter the credentials of the MySQL server where it says "Data Model Source" and "Data Model Destination", then, when you click Get, all the DMs from both Source and Destination pop up, you just need to select the DM you want to transfer, Mark V and click Transfer.
When creating the DM, the Destination MySQL will not create the data table being used to store all the data in the DM, therefore, you will need to go to the Destination MySQL and see on "dataschema1" table and search for the schemaID and see what is the name of the DBTableName and create one with the same name on ta9data schema, if it already exists create it with other name and change the DBTableName on "dataschema1" table as well.
After that you should be good to go, you can try and upload data to the DM.

![image.png](/.attachments/image-f9d90861-4e12-4b65-8ee8-ab0f7554eedc.png)

****note**
If the SchemaID already exists in the Destination you will need to change the ID of the Source DM, you can do that by changing the SchemaID in every one of these 4 tables:
1. dataschema1
2. dataschemafields1
3. datamodelgrouphierarchy1
4. userdatamodels1

#CREATING an entity using TACOPY

When copying an entity to another environment, first, you need to enter the credentials of the IntSight system where it says "Entity Source" and "Entity Destination", then, when you click Get, all the entity definitions from both Source and Destination pop up, you just need to select the entity you want to transfer, Mark V and click Transfer.
When creating the entity the ID of the entity will auto increment to the next ID available in the Destination.

![image.png](/.attachments/image-e7c9b775-fe7a-4e74-ac05-edf4a7822412.png)