[[_TOC_]]
# **Introduction**
This feature allows creating an auto-generated value in an entity property when manually creating an entity - using a configuration called _**EventSequenceCodes**_

The Configuration supports adding a predefined prefix to the auto-generated number like **X-**123456.
The System Admin can add this prefix in the web-config file as desired.


## **Prerequisists & Configurations**
- First - make sure the **_EventSequenceCodes_** appears in the "Entity Service" config module
![image.png](/.attachments/image-d400fd9f-8dd8-4f07-851c-fab22de552af.png)

If not - Create i by clicking on "Add Config" button under Entity Service module
![image.png](/.attachments/image-fd618962-ebe5-4b15-b113-a07458a86fb2.png)

- the Config Value should contain the Entity Type & the Prefix format you like in the following format:
{"EN10":"A"}
Explanation:
EN10 = Entity Type
A = Prefix Format
- If you wish to have more then one entity configured, the format in the config should be: 
{"EN110":"A","EN65":"B","EN91":"C"}

- For each entity property that's defined to be auto-generated 
->  Should have the **_EventSequence_** role - using **RoleID = 11** (Can only be done via the MySQL DB)
SELECT * FROM sqlite_metadata.em_property_definitions where ParentID={EntityID};
![image.png](/.attachments/image-f2c5f379-ff61-4df6-a6d2-e076c65a1e03.png)
-> Field Data type must be defined as a text field 
-> Field Cannot be "Mandatory"
-> Only 1 property can have this role



# **Solution**
Step 1 - Create a property in the Entity Via Admin Studio
Step 2 - Apply field role 11 on this property (via DB)
Step 3 - Add to the config value **_EventSequenceCodes_** the new entity ID & prefix
Step 4 - Restart TA9 Host and open the entity screen from TA9 Client
Step 5 - Create a new entity - Leave The new property empty
Step 6 - Save

Expected Result - The sequence property will be given a value automatically with the given prefix + a dash (X -).

# **Notes & Disclamers**
- When adding a new entity from the GUI,  and the EventSequence property is empty, a new sequence value will be generated.
- A sequence will not be generated if there's a value in the property. 
- Enumeration starts from 0.
- After each configuration change, we must restart the WildFly service for the change to take place.
If the WildFly service is installed on a Windows server, we should restart the 'TA9 WildFly' Service from the services panel. 
If the WildFly service is installed on a Linux server, we should log in to the server and run the command 
sudo service wildfly restart (in Ubuntu OS)
sudo systemctl restart wildfly (in Centos OD)

