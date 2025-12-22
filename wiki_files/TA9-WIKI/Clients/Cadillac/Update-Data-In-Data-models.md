[[_TOC_]]

# 1 Introduction
This feature allows to create or update a data model record, manually. 
The Creation/Editing of a row, will be activated from the data model "Edit" icon, which will open a popup screen where the user can insert the new data and save.

## Prerequisits & Configurations
-  In order to allow a data model to be edited, the **app.config.js_** file of the app must contain the **_editableDataModels_** parameter, alongside the ID of every data model that should support the update feature.
- Path of the Configuration File (to add the "is Editable" feature to a data model): TA9\Web\Web Client\app
- Example configuration: `editableDataModels:[1287]`
![image.png](/.attachments/image-8e5e03a8-3da5-4cde-88b6-563016901011.png)

>Note: 
> - You can define as many data models you wish to support "editing" just by using commas between them like so `[1287,123,555]`. no data model is configured by default. 
> - In case the app.config.js file does not contain this _editableDataModels_ parameter, add it to the file and save it. (restart service after)

- In order to update data the data model must be configured with a key field (isID), including a unique ID for each row. The key field should be configured as a Primary Key as well.
- Data models that are supporting this feature are data models containing data - therefore plugins/views cannot be updated.
- The "Entity as Data model" page is not supporting manual updates - since the update should be on the entity page itself.
- In case Data model fields are missing from the update form, open Dataschemafields1 and make sure that these fields have _Filed visibility_ value and that they are not marked as "invalid".

# 2 Update a Record
Once a data model was configured to support the "update/create" functionality:
**Step 1 -** go to the data model (grid view only):
![image.png](/.attachments/image-9e74feab-1f89-400e-b136-66bbe84c3f52.png)

**Step 2** - Click on EDIT to open that editing popup:
![image.png](/.attachments/image-313e603b-47d9-46cf-9561-e2ab9cac92a4.png)

**Step 3** - Click Save and the fields should be updated if the data model meets the editing criteria.

# 3 Create a New Record
Once a data model was configured to support the "update/create" functionality: 
**Step 1 -** Go to the data model (grid view only) and click on the "+" Icon on the top right corner:
![image.png](/.attachments/image-373bd412-be69-44c3-b9dd-346604c91ba9.png)

**Step 2 -** Fill in the new row's details in the popup and click Save
![image.png](/.attachments/image-d136a789-d594-451d-9173-94626d97cc23.png)

**Step 3** - All done, the data should be updated in the data model
![image.png](/.attachments/image-a982f50b-138f-431a-b8a7-052a0ea5a47e.png)

# Notes & Disclaimers
- Editing ability is not restricted by 'action permission', therefore any user can edit a data model data once its defined to support that.
- Updating Audit is not saved
- Once data was changed it cannot be restored
- Feature is not supporting editing hours/min/seconds (time) data. Only Date.


