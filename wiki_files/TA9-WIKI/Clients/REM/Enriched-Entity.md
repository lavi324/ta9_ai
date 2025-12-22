[[_TOC_]]

# Introduction
Enriched Entity is entity with case.
In this way the user can link
documents ,tasks and other entities to the entity.

**Example of Enriched Entity** 

|Entity|Enriched Entity  |
|--|--|
| ![image.png](/.attachments/image-9759b890-702f-4925-87e9-e6c97da7270c.png) | ![image.png](/.attachments/image-a4872a65-5afe-4e6d-a3ff-6dc15ab9f129.png) |


# Defining an Enriched Entity
1.Run the query 
`SELECT * FROM sqlite_metadata.em_entity_definitions;`

2.Find the entity you want to define as enriched.
3. Go to 'IsEnriched' field and change it from 0 to 1.
4.click on Apply.

![image.png](/.attachments/image-ab86c2bd-f952-42a4-afde-6f7294addc31.png)

![image.png](/.attachments/image-a623f3fe-a366-449a-96ba-a28413a48036.png)

# Deleting an Enriched Entity

**Note - deleted entities cannot be restored!!**

## Delete from entity
### Find the entity ID
1.Open the entity.
2.Click on entities tab.
3.Click on the tiles icon.
4.Click on the expend icon.
5.The ID appear in the URL.
![image.png](/.attachments/image-07da000a-61c9-41b9-8b24-db52559e6736.png)

![image.png](/.attachments/image-e997e3ef-9ad6-4e6a-a8e1-f28735a9aec2.png)

Delete the entity (Orient)

Wiki on deleting entities [Delete-Entity](/TA9-WIKI/IntSight-Applications/Link-analysis/Delete-Entity)

## Delete All from entity
1. Open on the entity you want delete from.
1. Find the entity ID on the Url
*The number in the urk is the ID * 1000
(for example if the number is 83000 the ID is 83)

![image.png](/.attachments/image-4b3b1eaa-8ae6-4457-a185-01a4c7c7ef36.png)
3. Go to OrientDB.

4.Run the query to select the entity you want to remove from `select * from EN83`
(replace '83' with the entity ID you want to delete from)

5.Run the query to delete **all** from the entity
`delete vertex EN83`
(replace '83' with the entity ID you want to delete from)
**Note - deleted entities cannot be restored!!**




