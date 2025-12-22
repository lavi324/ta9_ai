To remove an entity follow the steps:
**Note - deleted entities cannot be restored!!**

**1. Identify entity ID**
- Open the entity page locate the entity ID in the URL
![image.png](/.attachments/image-f2321473-e9a9-41eb-875a-ab518daaef6c.png)

**2. Log in to the OrientDB** 
**3. Run the following query: _select * from TAEntity where Sys_ID = **XXXXX**_
- _**For example:** select * from TAEntity where Sys_ID = 2755950_

**5.** Open the relevant entity by clicking on **@rid** field:
![image.png](/.attachments/image-1eecdd61-8dd6-4f92-986f-b14d722532bd.png)

**6.** On the entity page choose Actions -> Delete
![image.png](/.attachments/image-04f07e32-05db-4b73-a235-00dd400d8c20.png)

**NOTE:** Make sure you delete vertex with DELETE VERTEX command (same for edge - DELETE EDGE ) and not "delete...unsafe"
the delete unsafe will delete only the specific object and not all the pointers and relation for other objects
Run the query Delete vertax @class
for example, if the ID is 2 the "@class" is EN2.

**7. Log in to the Solr** 
select the **FreeTextSearch** and chose query
Search for the entity by its internal_id
(the entity ID)

![image.png](/.attachments/image-5e4fab2a-02e4-4fe7-96c0-51e2343ff339.png)

**7. Delete the entity from the Solr** 
Go to Documents -> choose 
Document type: XML
![image.png](/.attachments/image-7c230a80-070b-4394-ae24-5192029877e3.png)
in the query write:
<delete><query>
**your query**
</query></delete>
and click "Submit Document" 
