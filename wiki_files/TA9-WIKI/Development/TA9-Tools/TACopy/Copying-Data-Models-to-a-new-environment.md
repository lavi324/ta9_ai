 [[_TOC_]]

# Introduction
* In this tutorial we will understand how to copy a data model between environments and make sure it is defined well, using a few examples.

# Workflow

1. Identify which data models you want to copy. Some data models are easy to copy and some require some extra steps.

2. How do I know which Telco Dashboard widgets are relevant to me? Do as in the video, but for all the widgets. In this example, 156 is the Telco Dashboard Id. 199, 170, and 204 are the data models ids of the widgets.
[Identify Widgets Data Model Id.mp4](/.attachments/Identify%20Widgets%20Data%20Model%20Id-a1f2cabb-2439-4603-8bf5-ffac2ce1adb8.mp4)

3. Open the TA9 Copy, check the relevant items, and click "Transfer" using the WIKI's page - 
[TACopy](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/26/TACopy)
![taC.PNG](/.attachments/taC-14922a6b-beb8-4e81-a46f-121955b470f2.PNG)
Note that the TA9Copy doesn't create the actual tables in the relevant DB (IQ or MySql) so we will proceed to the sections 4 & 5 as below.

4. If the desired tables are created in IQ - 
Create correspondent tables in relevant IQ environment using the WIKI's page -
[SAP-IQ-Create-same-DM-in-a-different-environment](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/569/MySql-Create-same-DM-in-a-different-environment)

5. If the desired tables are created in MySql - 
Create correspondent tables in relevant MySql environment using the WIKI's page -
[MySql-Create-same-DM-in-a-different-environment](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/216/SAP-IQ-Create-same-DM-in-a-different-environment)

6. Make Sure that in the MySql table 'DataSchema1', the names of the tables ('DBTableName' field) & schema ('DBSchemaName' field) are the same as the tables created above (in 3-4 sections)
![image.png](/.attachments/image-ef239930-18bd-43d9-a546-bc9b61ea9a23.png)

7. Make sure that the 'connectionid' field as is displayed in 'DataSchema1', exists in the 'dataconnectionsmanager' table of the relevant environment.
![image.png](/.attachments/image-462ae60b-36df-4528-960b-e14c92f6a426.png)
![image.png](/.attachments/image-e28f4fe6-d3a8-484b-97ab-f9617ce30982.png)

8. Make sure your user in the TA9 system has permissions to every new DM you have created using the MySql table 'userdatamodels1' - 
![image.png](/.attachments/image-073061e6-28ae-416d-be2b-c51145719ea0.png)
Or by giving the user permissions using the TA Admin Studio system
![image.png](/.attachments/image-b6595449-2806-440d-9da2-e684a53a92a2.png)

#Notes
1. TACopy may crash if an item at the Source already exists in Destination.

2. You can also find items to copy in MySQL Workbench if its easier for you - just go to the relevant table, and search for it:

![serach.png](/.attachments/serach-58d9e5b6-b276-406f-afb6-24f16f924220.png)

3. Some items may not be present in the source DB so you might want to check the production db (for example - the data model is not present in 10.100.102.29 but it is present in 10.100.102.92

4. Relevant tables:
  * dataschema1 - contains the scheme for data models. for this task, the most relevant columns are "SchemaID", "ConnectionID" and "IsSupported". IsSupported needs to be set to "1" to be visible and valid in the system.

![ds1.PNG](/.attachments/ds1-2ab7151a-615e-475c-8448-cc2a13399ade.PNG)
   * dataschemafields1 - contains the fields for each data model.

![dsf1.PNG](/.attachments/dsf1-2b401c39-e038-43f8-aa3a-1f603c261c06.PNG)
   * dataconnectionsmanager - contains the look-up values that correlate between a data model and its relevant connection to a service/DB. In the images we notice that CDR data model [144] has a ConnectionID = 9, the fields are present in the dataschemafields1 table but in dataconnectionsmanager we don't have a row that corresponds with the value of 9. We will need to copy it manually later. You also need to verify all the copied data models have their correct ConnectionId value or copy it if it does not exist.

![dcm.PNG](/.attachments/dcm-09691001-0959-43ce-a703-f4e941d39cc1.PNG)
   * datamodelgrouphierarchy1 - We need to make sure that all the data models we copied are present in this table. The table is in a "Read Only" mode, and you can add values like in the picture below:

![dmgh1.png](/.attachments/dmgh1-79b0d5bd-a535-4d26-b30c-e2813af27372.png)

   * userdatamodels1 - tells which user (UserID = 1 - Admin) has permission on which data models. Again we need to make sure all the copied data models are present in this table or copy them otherwise. 

![udm.PNG](/.attachments/udm-f732799d-3789-43b0-8d11-57f3b46b409d.PNG)

5. To manually copy a row:
   * Mark the whole row, right-click it, and press copy row
   * Go to the destination table, right-click and paste row.
   * In the case you copy a row(s) to dataschemafields1, make sure you set the "FieldID" values to null (by selecting them, right-click and press "Set field(s) to NULL) **BEFORE** committing the changes.
   * Press Apply and Finish
##Extra steps for Telco Dashboard
1. Go to "sqlite_metadata.sensors" in the source DB and copy the relevant row (Search for "Telco") to the destination DB. The id in the ID column is of the Telco Dashboard.

![sensors.PNG](/.attachments/sensors-fd32f4b1-eec6-4c30-be3a-fd8734ff306c.PNG)

2. Go to "sqlite_metadata.usersensors" and copy the row that corresponds to the id from the previous section in "sensorid" column.

![usersens.PNG](/.attachments/usersens-0eb4fcc3-9a3a-427e-91b3-c72d9e879703.PNG)

3. Go to "sqlite_metadata.dsb_dashboard_definitions" and copy the row that corresponds to the id from the previous section.

![dashdef.PNG](/.attachments/dashdef-46a826cc-26ef-48af-a240-f3636595adc0.PNG)

4. Go to "sqlite_metadata.dsb_dashboard_widgets" and use the next query to find the relevant items to copy. run:
SELECT * FROM sqlite_metadata.dsb_dashboard_widgets where dashboardid = X and stateid = 1;
Where X is the id from section 1. 

![dashbwidg.PNG](/.attachments/dashbwidg-1a1c8903-9cec-4227-9d62-2784b6d70e74.PNG)

5. Go to "sqlite_metadata.sensors_identifiers" and locate the Telco dashboard id number, in this example, it's 156. Copy the relevant rows and paste them in the destination DB.

![sensids.PNG](/.attachments/sensids-c57f3b6d-c1b3-4efc-a119-ade1f16f3b22.PNG)
























