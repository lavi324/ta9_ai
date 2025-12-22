[[_TOC_]]


#General Details - What is the VMS for?
VMS integration (Video Management Service), is between TA9 IntSight App, and a 3rd party video provider.

The Integration allows the user to select a specific camera from a map and send a request to get the videos from it from a certain date range. 

The request is sent using a form (Viewer), where the user is asked to fill in the date & time range, and the request is received back to a dedicated data model called "requests", where they can see the request status (In progress / completed / etc), and see the video received. 

![image.png](/.attachments/image-39824d48-9767-4ffb-8436-1005e19d47a4.png)

##How to send a VMS request
 
1. Run a Query on the "Cameras" data model to get the available cameras.

2. Right-click on the camera you want to request from the "Cameras" Data model

3. Click on 'View actions'

3. Click on VMS App - VMS Viewer will appear. 
NOTE: (If using a mock service integration developed by RZ - choose the same start & end date, there's a limitation in mock config - limiting max video range to 30 sec-configurable).

4. After sending the request:
- A new row will be created on the "VMS Request" DM.
- We will see the request status indication.
- Once completed, the Video will be saved in the folder configured on the server.


![image.png](/.attachments/image-dcdf0e7e-f73b-4275-8140-91cf7e2f27a5.png)

![image.png](/.attachments/image-2d6129c9-9378-44d6-8e8d-9e1e5a8da6d0.png)

# Data Flow
![image.png](/.attachments/image-8dafbc84-1c4b-4abe-b05f-a1ee334d00c1.png)

# VMS Configuration

## VMS data models 

there are two data models that the VMS is based on :

1. **'**cameras**' DM** - data about the cameras that you can request videos.
 - Camera ID identifier is defined on cameras DM.
- 'external_id' field defined as lookup (camera_icon_lookup).

2. **'**VMS Request**' DM**  -  data about all the request that was sends. 
  - “Request” Data model should be a system data model using Minus (-).

  - Request ID field - identifier.
  - 'Request Status' field is defined as a lookup.
  - 'Last update date' field is defined as a sequence.

Design file https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/doc2.aspx?sourcedoc=%7B39437C6F-265B-40EC-A2C6-E1F535CF9DCB%7D&file=VMS%20Integration.docx&action=default&mobileredirect=true&cid=3cdd9502-2a4e-4e50-815f-c5467befd7e3

## Admin studio
Create VMS app:

![image.png](/.attachments/image-6b6fe151-1add-45a9-8d1f-d4e3c46f16b5.png)

## How to define the Video request viewer 

1. Admin Studio - In the 'View' column definitions, select the 'Viewer' field as a 'VMS File Viewer'
![image.png](/.attachments/image-c0ab4ea6-cac4-468c-960b-86b776505f8c.png)

2. Mysql - find the field ID and Add it to the custom path 

Field ID: the ID of the 'View' field on the DataSchemaFields1 table
Base URL: the video folder.
Viewer type: 25


![image.png](/.attachments/image-ddfedbfb-8f3c-4494-9c97-1046dbe9a441.png)

![image.png](/.attachments/image-a4b57ab6-a3d9-47e8-9a8c-f67ddf45c2c4.png)

**Wiki on custom path and viewer definition:** [Custom-Path-Viewer](/TA9-WIKI/IntSight-Applications/Custom-Path-Viewer-%2D-add-photo-to-data-model-from-folders)

## The video folder
There should be a Video folder on the server 
The path should be defined in the JSON file 'appsettings.json'
under this path: `D:\\VMS Mock
*The names of the files in the folder are the 'request ID'

![image.png](/.attachments/image-b2d67aad-0133-4121-abc7-522e111f604d.png)

![image.png](/.attachments/image-0b59681b-6e39-4f69-8536-57675e2fc296.png)

**Custom path definition for the viewer(STG config):**

  "14621": {
    "baseUrl": "http://intc2-stg/api/FileServer/files/async",
    "viewerType": "25"
  }