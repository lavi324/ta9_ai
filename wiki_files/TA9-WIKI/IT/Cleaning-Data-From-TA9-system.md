[[_TOC_]]

## **Remove from the system**
**Note!** before you delete from DB , make sure you delete only unnecessary things.
*If you not sure, you can create a backup by exporting the data.

![image.png](/.attachments/image-3b281a1c-e394-4396-a505-9d4de1bf5b39.png)

open SQL workbench.

**You need remove from:**

1.remove from cases
`SELECT * FROM sqlite_metadata.investigationheader;`

2.Remove from Load Files
`SELECT * FROM sqlite_metadata.load_files;`
 
3.Remove from Audit
`SELECT * FROM sqlite_metadata.data_audits;`

4.Remove from Indexing_audit

*First you need to stop the TA9 Loader Service(index service) and start him back after the remove.

![image.png](/.attachments/image-58ab0283-b80a-4ae6-8246-b2cbf695df13.png)

`SELECT * FROM sqlite_metadata.indexing_audit;`

5.Remove from Criteria

first remove these two:
`SELECT * FROM sqlite_metadata.schedule_criteria_permissions;`
`SELECT * FROM sqlite_metadata.saved_criteria_permissions;`

`SELECT * FROM sqlite_metadata.saved_criteria;`
`SELECT * FROM sqlite_metadata.schedule_criterias_runs;`
`SELECT * FROM sqlite_metadata.schedule_criteria;`

6.Remove from Events
`SELECT * FROM sqlite_metadata.events;`

## **Ways to remove data from DB table**
**Note!** make sure you delete only unnecessary things.

**way 1:**

1. Open the table you want to delete from.
1. Check all the rows you want to delete. 
1. Right click and click on 'Delete Rows'.
1. Click on apply.

![image.png](/.attachments/image-2240c4df-f6f6-4f69-a58e-cadc535c6458.png)

![image.png](/.attachments/image-18c1ee2a-59a0-42d6-a849-b68e463fe746.png)


**way 2:**
If you want remove **all the rows** from the table- you can right-click on the table name and click on 'Truncate Table'

![image.png](/.attachments/image-2e3432b4-221f-4950-bb8c-5f3253819982.png)

## **Deleting Indexed Data (Solr)**
To clear all data from a SolR core go to the document page pick XML and paste the following:
<delete><query>*:*</query></delete>

![image (1).png](/.attachments/image%20(1)-3c4194b2-31ec-4f98-94ae-8d0dfc45c0da.png)

Test that it succeeded: 

1. Select "freetextindex"
1. click on "query"
1. click on "execute query"

![image.png](/.attachments/image-292e147c-95c4-4d45-ad56-ee408ac070c8.png)

*wiki on solar and delete: [Solar-WIKI](/TA9-WIKI/3rd-Party-Software/Databases/SolR)

## **Delete from Data Models**

**DM in SQL :** 
1. run the query: `SELECT * FROM sqlite_metadata.dataschema1;` 
1. find the DB name of the table DM you want delete from.

![image.png](/.attachments/image-a2eccfd6-4bcf-42be-ad05-98877c3ada10.png)

3. Remove the data from the table.

**DM in IQ :**
1. Run the command `TRUNCATE TABLE table_name`
1. Run the query `COMMIT` (to see the changes in the system)

## **Delete Entities(orient)**
**if you want delete all from the entity**
1. find the entity id-Open the entity page locate the entity ID in the URL(the ID appear in the url*1000)

![image.png](/.attachments/image-e380024e-9aa9-47ed-9cdd-61a2bde80c68.png)

   for example
-  if appear in the URL 3000->the id is 3
-  if appear in the URL 30000->the id is 30 

2. Run the query `Delete vertax @class`
for example if the ID is 2 the "@class" is EN2.

![image.png](/.attachments/image-7212893c-26f7-4f33-b705-460a04183ed3.png)

**If you want delete not all from the entity**

Go to this WIKI: [Delete-Entity](/TA9-WIKI/IntSight-Applications/Link-analysis/Delete-Entity)