 # **Entities**
1. Go to admin studio of the environment you want to export from, click Ontology > Entities.
2. Click on the entity you wish to export.
3. Click on the Export button on the top right corner and save it.
4. Go to the Admin studio in the environment you wish to import to. 
5. Click on Ontology > Entities, and import the file you exported. You should be able to see the new entity created on the bottom of the page.
6. Click on the new entity. You should see all configuration set as the original entity you exported from. 

**Note**:

* The entity ID in the new environment should update automatically to be the latest+1.
* The image of an entity cannot be imported in the process, even if the image URL is shared with both environments. Need to upload it to the system, to get a fileID from seaweed, and use it in the specific entity configuration.
* When exporting an entity with defined identifiers from one environment and importing to another, when the identifiers are not configured on the second environment - need to manually configure the needed identifiers before the importing of the entity.

# **Relations**
1. Go to admin studio of the environment you want to export from, click Ontology > Relation.
2. Click on the relation you wish to export.
3. Click on the Export button on the top right corner and save it.
4. Open the exported file and make sure you **change the "ParentType" parameter to the ID of the new entity in the latest environment (check in MySQL).** 
![image.png](/.attachments/image-3bee60b9-4452-44ae-abdb-279b0f73118f.png)
5. **Change the "Name" & "ID" parameter to the name of the new Relation** (in the latest environment).
![image.png](/.attachments/image-cbdb601e-9d47-4c1c-950d-78966bcc0a11.png)
5. Go to the Admin studio in the environment you wish to import to. 
6. Click on Ontology > Relations, and import the file you exported. You should be able to see the new relation created on the bottom of the page.
7. Click on the new Relation. You should see all configuration set as the original entity you exported from. 

**Note**:

* Optional error that may appear: `Failed to import file. EM_FileEntityRelationIDNotValis` - this may indicate that the "ParentType" is not configured correctly in the file.

* Note that all exported files (entities and Relations) include parameters that includes a user name ID: 
`CreatedBy`
`LastUpdatedBy`
which means that - the import and export should be done by the same user - Admin user (ID=1).

----------

QA Ticket: [https://dev.azure.com/ta-9/Argus/_workitems/edit/47315]()
Relation Export file example - [person family.txt](/.attachments/person%20family-4cd07342-e69e-4ef1-a547-8494437d6320.txt)
Relation edited Export file example - [Family Edited.txt](/.attachments/Family%20Edited-c2b3a132-ccb0-4e2a-bf79-1df6ea2788f7.txt)