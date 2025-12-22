[[_TOC_]]

# Introduction
Written below is a quick how-to document about creating a SQL updating script to apply on the client’s environment, usually needed when updating the product version.


# Generate Commands
Using MySql Workbench (or any other SQL platform), we can use the editing tool to create the needed SQL commands:

## Insert
Copy a row you want to add and paste it to the row below. When applying a window will pop up and show you the SQL command before applying the changes to the DB. Copy the command and **cancel** the changes.
![image.png](/.attachments/image-fabbdfd5-53d9-4103-806a-8e920d1d9f17.png)
![image.png](/.attachments/image-bd9ccc8a-df4e-405d-90ac-44c71bf66c1a.png)
![image.png](/.attachments/image-33049617-4b7c-461f-b0a3-5fef53608cb3.png)

## Update
Essentially the same procedure as an **insert**, but now instead of adding a row we will edit instead. 
![image.png](/.attachments/image-74c3c205-1344-446f-9cfe-068407349637.png)
![image.png](/.attachments/image-4f8af8be-539e-4023-b5e4-794bbffccc5b.png)
![image.png](/.attachments/image-168f1268-928d-4b5a-bced-c40c137ead6d.png)

## Delete
Delete a row and click apply, then copy the generated command.
Again make sure to **cancel** the changes after copying the needed command/s.
![image.png](/.attachments/image-4a15f7c0-06a9-411e-936a-df39a11e41bd.png)
![image.png](/.attachments/image-20434770-227c-457e-bc6e-368d509931d4.png)

## Create/Alter Table
Right click on the table which was created/altered -> Copy to Clipboard -> Create/Update depending on whether the table was created or updated accordingly. The command is now copied to your clipboard.
![image.png](/.attachments/image-c5164f9f-6925-4d9b-9d05-c650e3cac469.png)

## Create/Alter View
Open the alter view option under the created/altered view and copy the command.
To the first row of the command, After the ‘CREATE’, add ‘OR REPLACE’ which will result in the command being able to support both creating the view if it does not exist or update the existing one. 
![image.png](/.attachments/image-cb9ed1ba-f4de-46ba-a960-98985ccfda1b.png)


# Copy Data Model

All the commands created to update the DB should be written into a text file to later be used as a SQL script to update the client’s DB.

To copy a new data model or update an existing one we need to update a few tables:

## dataschema1
- In case a new data model was added, we will need to add an **insert** command with the new row containing the new data model.
- In case a data model was updated (any update which does not include specific data model fields) we will need to add an **update** command containing the updated fields.
- A few fields to watch for:
  - ‘**ConnectionID**’ – might not be the same connection id needed in the client’s environment; Check the client’s ‘**dataconnectionmanager**’ table and edit the generated command accordingly.
  - ‘**DBSchemaName**’ & ‘**DBTableName**’ – usually will not change between environments but depending on the update and the client’s environment those might need different values.

## dataschemafields1
Before copying any line in this table, make sure to **nullify** the ’**FieldID**’ field, this field is an incremental auto generated field and may cause collisions if moved between environments as is.
- In case a new data model was added, simply create **insert** commands to all the rows with the new data model’s ‘**SchemaID**’.
- ‘**DataEnrichmentName**’ field: If a new lookup was created for a specific field in the data model, make sure to generate the **create** command for that table.

## datamodelgrouphierarchy1
The ‘**ObjectID**’ field corresponds with the data model’s ‘**SchemaID**’.
- In case a new data model was created, create an **insert** command for the row containing the newly created data model’s ‘**SchemaID**’.
- If an existing data model category was changed, create an **update** command with its ‘**SchemaID**’.

## userdatamodels1
The ‘**ObjectID**’ field corresponds with the data model’s ‘**SchemaID**’.
- In case a new data model was created, create an **insert** command for all the rows containing the newly created data model ‘**SchemaID**’.
- In case the data model’s permitted users were updated, create **insert** and/or **delete** commands depending on the users added or removed from the data model’s permission list. The ‘**UserID**’ field represents the user, check the ‘**users**’ table to translate the ID to the username.