The Rayzone team is working on the migration of entities to the client environment, which will be followed by configuring the creation of entities from a data model.

The flow is to create entities from a table using the migration tool, and then create a date model on top of that table and configure an ongoing process of creating entities from a data model.

The high-level concept is divided into two steps, Migration and Ongoing.

**Migration:**
1.	Entity Definition: 
1.1. Using “Admin Studio” create entity definition.
1.2. Make sure the entity definition has a property with “Is Key” (unique property).
2.	Migration Table:
2.1. Create a Migration Table with the field “InternalId” auto-incremented.
3.	Migration Code:
3.1. Make sure all the drivers are set correctly to the DB that you are working with (Oracle).
4.	Indexing Service:
4.1. Stop the Indexing Service before starting the migration process.
5.	Run Migration Jar.
6.	Start Indexing Service.

**Relevant Wiki for the migration process:** 
* https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/597/How-to-insert-data-(entities)-to-the-orient-DB

**Ongoing:**
1.	Set up Data Model:
1.1. Create a table for the Data Model that will point on.
1.2. Create the Data Model in the “Admin Studio”.
1.3.	Set the same field you set as “Is Key” in the entity definition to “Is ID” in the  Data Model.
1.4.	Set a field to have the role of “Sequence”. 
2.	Config:
2.1. Add a new record in the “indexing_source” table.
2.2. Add a new record in the “indexing_sources_stores” table.
3.	Restart Indexing Service via Windows Services.

**Relevant Wiki for the setup of creating entities from a data model:**
* https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/608/Creating-Entities-from-a-Data-Model-(SQL)
