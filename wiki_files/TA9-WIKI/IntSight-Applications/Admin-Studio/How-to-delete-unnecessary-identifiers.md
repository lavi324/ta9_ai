The use of Identifiers in the system is in data models, apps and entities . 
Before deleting them we should make sure they are not in use.
 
1 .Find the ID of the identifier you want to delete.

  ![image.png](/.attachments/image-714ef8d9-4bcd-4d5b-9e00-bb84bc5b0258.png)

2 .Run the queries:
* put the id numer instad of the XX

`SELECT * FROM sqlite_metadata.dataschemafields1 where IdentifierTypeID = XX ;`
 
`SELECT * FROM sqlite_metadata.sensors_identifiers where IdentifierID = XX ;`

`SELECT * FROM sqlite_metadata.em_property_definitions where IdentifierTypeID = XX ;` 

IF there is no result in all the tables its means that the identifier not in use and its ok to delete it.

**How to delete identifiers:**

1.Run the query `SELECT * FROM sqlite_metadata.identifiertypes;`

2.Right click on the row of the identifier you want to delete.

3.click on Delete row.

4.click on Apply.

![image.png](/.attachments/image-48f98713-0e05-4de0-9104-fa0c753125d4.png) 

5.Clear server and client cache.
 
   