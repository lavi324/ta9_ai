[[_TOC_]]


This documentation refers to cases where you wish to delete created entities, entity relations, and an entire entity type. This includes steps on how to delete an entity, how to delete entity relations, and how to delete an entity type.

>**Note** - deleted entities cannot be restored!

To start the deletion process, the first step is to detect the entity ID.

# Identify entity ID
Open the entity page and locate the entity ID in the URL
For example - when in the URL the number that appears is 3000 the entity id is 3. 

![image.png](/.attachments/image-6f8c48c8-c06a-4bfe-a90e-2dfda9e36f6e.png)


# Delete entities relations from OrientDB

If there are relations with your entity you need to delete the relations before you delete the entity, if there are no relations with this entity you can move on to the next step(deleting the entity).

1. Log in to the OrientDB
2. Detect all relations related to the entity you wish to delete.
3. Run the Query `Delete vertex from RLXX` (change XX to your relation ID)
> **Note** This command deletes all relations of your entity type. 
To delete a relation of a specific entity, you will need to find the sys_id of the specific entity, and run the following query:
Delete EDGE rlXX where Sys_ID = XXX;



# Delete entities from OrientDB

1. Log in to the OrientDB

2. Run the query: `Delete vertex from ENXX`
*Change the XX to your entity ID.
For example - Delete vertex from EN3.
> **Note** This command deletes all the entities in your entity type. 

# Delete entities data from Solr

1. Log in to the Solr
select the FreeTextSearch and chose query.

2. Search for the entity by its entity_type_id
(the entity ID)
For example, if your entity ID is 3 the search is : entity_type_id:EN3

![image.png](/.attachments/image-18a01563-0a43-4ad1-91ef-1043db19b584.png)

3. Delete the entities from the Solr:
Copy your query(in step 4)
Go to Documents -> choose
Document type: XML
in the query write:

```
<delete><query>
**your query**
</query></delete>
```

and click "Submit Document"

![image.png](/.attachments/image-34488230-d147-4c23-bb1c-fdceb1339b2c.png)



# Delete the Entity type

1. Open the admin studio.
2. Clear server cache.
3. Click on Ontology Manager.
4. Click on Entity Definition.
5. Click on the entity that you want to delete and Click on Delete.

