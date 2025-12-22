[[_TOC_]]

# Custom Path Viewer

## Introduction
The 'Custom Path Viewer' will let the user view images in the data model fields.

## Pre-Requirements
The following pre-requirements must happen in order for the image to be linked to the data model:
1. There must be a folder with the photos and hosted by any **web server**.. (It can be managed in a **IIS** server.)
2. The image name in the hosted folder should match the image name in the data including the file extension (e/g img1.jpg)




## Step-1 Web Configurations 
Follow the following steps:
1. Log-in with an admin user
2. Navigate to the 'Admin Tools'
![image.png](/.attachments/image-6df94089-9e05-49ea-98cd-bfec49679add.png)

3. Click on the 'System Configurations' tile
![image.png](/.attachments/image-9d6ea02e-547d-4175-adc4-aa28b00c1355.png)

4. Search for the module 'Web Client' config
![image.png](/.attachments/image-b5aa5af6-25f0-421c-8589-b872984a3fbc.png)

5. Search for the "customPathsDefinitions" config key
![image.png](/.attachments/image-55044fe5-2295-4d90-9368-dbe1043485c6.png)

NOTE: 
If the config key is missing from the list, you can add this config key by clicking "Add config" and fill config key with:
**customPathsDefinitions**
and click OK.

**--Please notice!!!--**
if the customPathsDefinitions doesn't appear in either the database or the system configuration, you will need to add it only through the web interface and not the database.

6. Click on the 'Edit' button to edit the config value and paste the 'config path' using the following format:

 - "Add the '**FileID**' - The ID of the field containing the image name data of the data model. 
Note: get the field ID from the 'dataschemafields1' table in the DB"
 - _"baseUrl":_ "Add the **images folder**",
 - "viewerType": "Add the **viewer type** from the 'viewertype' table in the DB"

**Example:**
{"12345": { "baseUrl": "http://10.100.102.01/MyImageFolder/ ", "viewerType": "2" }}



**Beautified Example:**

{
  "12345": {
    "baseUrl": "http://10.100.102.01/MyImageFolder/",
    "viewerType": "2"
  }
}

**Template Example:**

{
  "_FieldID_": {
    "baseUrl": "_http://10.100.102.01/MyImageFolder_/",
    "viewerType": "2"
  }
}

NOTE:
- Curly brackets are important as in the example.
- Add a right slash (/) in the end of every path


## Step-2 Admin Studio Configurations
Navigate to the data model in the admin.
In the image column definitions, select the **'Viewer'** field as a **'custom path viewer'**
![image.png](/.attachments/image-9ffdc532-682e-4766-906f-b8100ef1161c.png)
![image.png](/.attachments/image-5e1aaebb-3316-4fe0-bd41-187ffc8ad07b.png)

##Configure web folder in IIS
This guide will guide you how to configure a shared folder for images using the IIS. If you already have a web server hosting the images, you don't need to use this configuration.
1. Open a new folder in your drive. Preferably - choose a disk with a large volume, and not near the application files.
2. Open the IIS application
3. Right click the TA9 site
4. Add Virtual Directory

![image.png](/.attachments/image-9647c36b-2470-4d0e-81fb-0e3d004c91e6.png)


in Alias fill the name needed then browse for the folder you created then click on OK.
![image.png](/.attachments/image-acf65788-64c2-4c75-b400-87c6d2ea507c.png)

Now - you can copy the folder URL and use it to past into the physical path.
5. Click OK

Done!

## Final Step - Test
1. Reset TA9 Service Host
2. Open the Data model you have configured in ta9 IntSight, and the column you set as the custom path viewer in admin studio, should show the image icons, allowing you to click the image and see it in TA9 Viewer.

.
.
.

# IMPORTANT NOTE:
When trying to view an image from a DM using this feature, the value of the image relative path must have '/' at the beginning.
For example if the custom path is 'http://1.2.3.4/custom' and the image file name is '123.jpg'
The custom path config value will be: 'http://1.2.3.4/custom' and the DM field value will be '/123.jpg'
If the image will be referenced without the '/' in the beginning of the value, the image icon won't show.


