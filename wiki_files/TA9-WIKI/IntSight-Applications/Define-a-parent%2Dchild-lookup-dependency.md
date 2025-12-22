[[_TOC_]]


#General
This wiki explains on how to define a dependency between lookups, with a "parent" and "child" relation.
Parent-child lookups are often used when the main lookup (parent) affects the list of values that appear on the sub-lookup (child).

Here are some examples of parent-child relations:
- Country/City (Israel/Tel-Aviv)
- Task/sub Task (Data collection/Osint)
- Case/Sub Case types (Finance/money laundering) 
- Gun/model (Glock/375)

---
#The lookup creation process

A lookup/ref table is basically built on 2 things:
- a data table in the database 
- a "lookup" configuration in the "lookupmanager" schema in TA9 IntSight

>**Note**: The Data table can be on MySQL or on other DB's, as long as there's a valid connection to it from TA9 IntSight.

![image.png](/.attachments/image-8e00e9d0-21cd-4b9a-93e4-2cd27d8f1d68.png)

--- 

#Define lookup on an entity

Once the lookup is defined as mentioned in the step above, go into the ontology definitions, choose the entity, and add a new property to it. Once the property is set up - you should find the lookup definition you created in the "lookup" list values:
![image.png](/.attachments/image-4be458a6-cc01-45e3-bf5b-9b25ef04b2f0.png)

## Define a Child lookup on an entity
### Step 1: Child lookup configuration setup
Create a lookup table with the values you wish, and add a column that represents the "parent" lookup ID in the "parent Lookup" table. 

For example:
If the parent lookup table look like this:


|Parent Key|Parent Value|
|--|--|
|1| Warm Colors|
|2| Cold Colors|

Than the Child table should look like this:
Child Key|Parent Key|Parent Value|
|--|--|--|
|1|1 | Red|
|2| 1| Yellow|
|3|1|Orange|
|4|2|Blue|
|5|2|Purple|
|6|2|Green|


Note that all values with the "parent Key" = 1 belongs to the "warm colors"  group in the parent lookup
and all values with the "parent key" = 2 belongs to the "cold colors" group in the parent lookup.

### Step 2: Define the lookup
Configure the lookup via Admin Studio using the "lookup manager application"

### Step 3: configure parent dependency
Open the SQL / Maria workbench and run the select:
`SELECT * FROM sqlite_metadata.lookupmanager where Lookupname = YOURLOOKUPNAME;`

- Under the "_**ParentLookupName**_" definition - fill in the name of the parent lookup (as appears in the 'sqlite_metadata.lookupmanager' schema) 
- Uner "_**ParentValueMember**_' definition - fill in the column name in the "child lookup" data table that points on the parent lookup ID, In our example its "**_Parent Key_**" 

![image.png](/.attachments/image-ad8b1dc5-42f9-4ffb-a9c8-637147d99ca7.png)

### Step 4: Define dependency on the entity property
The Child lookup property on the entity, should be defined with a dependency role that it have a "parent lookup". this configuration is done via Admin studio - in the entity definition screen:

![image.png](/.attachments/image-08d32782-7fe1-41ce-9119-5f3513390a74.png)

###Final Step: Test UI
Go to the entity on the web interface, select a parent value - and expect that the child lookup will adapt with the correct values.
>Note: don't forget to clean the cache!

![image.png](/.attachments/image-a7509cfb-8700-4c59-af41-a86b8feedfce.png)

---

#Define lookup on a data model
From the Admin Studio - go to the column you wish to define as a lookup and set the "lookup name" to be the lookup you want:

![image.png](/.attachments/image-cebf6352-50cb-468c-8d24-423a4fa71b07.png)

>Note: Dependencies in data model is not supported

---

#Troubleshoot

1. I can't find the lookup in my lookup lists
- Make sure the lookup is defined properly in the "lookupmanager" schema in the db, or try to define it again

2. I see the lookup, yet it have no values to choose from
- Make sure that the connection string is the correct on. When you create a lookup, you basically connect with a data base. in some cases, a single data base may have several connection ID's, and it may have been configured with the wrong one. Try comparing with a connection string for a data model you know is working.

3. Chiled dependency isn't working!
- Child dependency is available from IntSight Version 3.9 and above. Check your version is compatible at first. If so - try repeating the configuration steps defined in the section above, and check for Event viewer errors if it is defined correctly. Make sure that there's a dependency role defined on your entity property.

