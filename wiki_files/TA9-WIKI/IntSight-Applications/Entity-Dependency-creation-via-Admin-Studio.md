# General
> ℹ️ Dependency Roles are a way of configuring entity form behavior based on the entity's values and description. For example, a criminal might have "IsJailed" as a dependency, meaning it is only relevant to that particular entity type.

There are several Dependency Roles Types, but for this dependency, we will use the **Visibility** role type - A property's visibility can depend on another property value. For instance: Only if the property "Has Kids"=TRUE will the property of "Kid Name" be relevant and visible.
 
In order to create an entity from a data model (SQL), please refer to the following Wiki: [Entity SQL creation](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/608/Creating-Entities-from-a-Data-Model-(SQL)?anchor=**capability-description**)

**How to create an Entity Dependency on Admin Studio:**

_Step 1: enter the Admin Studio app and click on "Ontology Manager"_

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-1-1.jpg)

_Step 2: Click on "Entity Definitions"_


![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-2-1.jpg)

_Step 3: Click on the plus sign on the right side of the screen to add a new entity definition_

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-3-1.jpg)

_Step 4: Click on the green plus sign to add dependency role_


*For this example, let's assume we want to set a dependency for Criminals and Diplomats"*
When you are finished, make sure to click "OK" on top of the menu to save the addition. 

![Image Linking](https://ta9test.files.wordpress.com/2023/04/image-5.png)


![Image Linking](https://ta9test.files.wordpress.com/2023/04/image-6.png)

This is how it will look like after saving, you may mark or unmark all the field you wish.
After you are finished setting up the basics, you may edit the entity layout by clicking the window logo.

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-9-1.jpg)

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-10-1.jpg)

When you have finished all of your desired entity and layout settings, click the "Save" button on the top right. 

> ** ❕Note: Headers must be without spaces**

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-11-1.jpg)

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-12-1.jpg)

_Make sure to accept the "Action Succeeded" notice to implement the dependency on IntSight_

![Image Linking](https://ta9test.files.wordpress.com/2023/04/ed-13-1.jpg)

Here is how it will appear on the "Entity Definitions" screen on Admin Studio