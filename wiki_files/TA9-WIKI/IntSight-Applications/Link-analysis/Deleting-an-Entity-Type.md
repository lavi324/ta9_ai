[[_TOC_]]



# Delete the relations with your entity

If there are relations with your entity you need to delete the relations before you delete the entity, if there are no relations with this entity you can move on to the next step(deleting the entity).

1. Open the admin studio.
2. Click on Ontology Manager.
3. Click on Relation Definitions.
4. Delete all the relations with the entity you want to delete. 

# Delete the data from orient 

1. Identify entity ID:
Open the entity page locate the entity ID in the URL
For example - when in the url the number that appears is 3000 the entity id is 3. 

![image.png](/.attachments/image-6f8c48c8-c06a-4bfe-a90e-2dfda9e36f6e.png)

2. Log in to the OrientDB

3. Run the query: `Delete vertex from ENXX`
*Change the XX to your entity ID.
For example - Delete vertex from EN3.
**Note** This command deletes all the entities in your entity type. 

# Delete the data from Solr

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


 
# Delete the Entity from Admin studio
1. Open the admin studio.
2. Clear server cache.
2. Click on Ontology Manager.
3. Click on Entity Definition.
4. Click on the entity that you want to delete and Click on Delete.

![image.png](/.attachments/image-866e0124-4d44-4e90-80d6-0b397aae5cd1.png)


