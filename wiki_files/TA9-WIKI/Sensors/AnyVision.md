[[_TOC_]]

#Introduction 

AnyVision is the world’s leading developer of facial, body and object recognition platforms.

# Installation Process
Install the program:

Version: AnyVision-1.20.1-win-installer
Path of the installer: 
\\\10.100.102.13\share\Installs\AnyVision-1.20.1-win-installer

![image.png](/.attachments/image-9e192b16-1446-435e-afd3-98807ebe87ca.png)

Pick the option: Anyone who uses this computer

# After installation complete

Go to : 
C:\Users\Public\dashboard\proxy-pac.js

Edit the file to this configuration as below:

function FindProxyForURL(url, host) {
// DEFAULT RULE: All other traffic, use below proxies, in fail-over order.
  return "SOCKS5 10.100.102.5:1080; DIRECT";
}

If the program is open - reopen it. 



# DB Configuration

Open MySQL Workbench editor:

add this script: 
DBChange_for_AnyVision.sql

# CHECK LIST
## 1. User have permissions to both data models (Face Detection & Detection-Rules Notifications) , Note that the ObjectTypeID must be 1 and NOT 2
## 2. ServiceAdmin user set IsAdmin to true (update sqlite_metadata.userpermissions set ISAdmin = 1 where UserID = 2)
## 3. ta9AppsJDBC connection is dfined in dataconnectionsmanager table
## 4. verify that detectionsDM config value is mauch the Id of Face-Detection DM id, same thing for frNotificationsDatamodelId config value

SELECT * FROM sqlite_metadata.system_config;
![image.png](/.attachments/image-70601c11-e5f5-4199-8412-5ef7c5415b3f.png)

SELECT * FROM sqlite_metadata.dataschema1;

_______________________________________

Search the table : 
*.*System_Config

In search bar look for Any
![image.png](/.attachments/image-dbeb0916-aa60-4a1d-9054-167965ccace9.png)

Look for this lines:
 
FaceRecognitionType 
FaceRecognitionMappingType
FaceRecognitionEntities	
FaceRecognitionRuleDefinition
FaceRecognitionCameraManagement
FaceRecognitionGroupManagment
FaceRecognitionFaceSerach
FaceRecognitionDetectionManagment
mediaAnalyzingProvider

For each line type : anyvision_1_20

Make sure all con figure in the added picture. 

Now search in the search bar: replace

FR_AV_BaseAddressToReplace - https://nginx-localnode.tls.ai
FR_AV_BaseAddressToUse - Change the value to this: http://10.100.102.5:8040

Done!

Go back to the system of any vision the default user&password are : admin
If you see bunch of photos all the configuration is correct. 


## Entities / Suspects Sync
By definition, any entity that has a 'Face' identifier is synced to the Face-Recognition as targets (suspects).

The process who's responsible for the sync is the indexing-service. 

There are 2 ways to create an entity so it will be synced as targets to the FaceRecognition:
1. Create a new entity with face identifier (applied on an image) and set its image to a face image (the system should prompt you to choose the specific face from the uploaded image)
1. Create an entity from a detection. Choose a detection (that has no entity/suspect) and click 'Create Entity'
2.1 The detection image should be copied to the new entity

### Best Practice Configurations for the Entities Sync
1. Make sure an entity (usually **Person**) is defined with the following:
1.1 It has a 'Face Image' property with an identifier 'Face' (-7)
1.2 It has a 'Detection' property with an identifier 'Detection' (can be hidden from layout) [if there's no identifier 'Detection' -> create one]
2. A 'personEntity' is configured on web-client's config (app/app.config.js):
2.1 ID: the id of the configured entity from step 1
2.2 Detection: Property id of the detection property of the entity (step 1.2)
2.3 Other fields aren't relevant for FR
![image.png](/.attachments/image-7421f9d5-4390-477a-aec2-becafd340841.png)
3. Verify that a store is configured well for the Entities (-130) source:
![image.png](/.attachments/image-7e3f1473-4888-445c-b182-a47b9b3683d1.png)
3.1 STORE_CONNECTION_ID should point to the OUR face-recognition service endpoint ID
3.1 Idnentifiers ID must be aligned (ie - in the sample above the ID of 'Detection' identifier is 56)

4. Restart:
4.1 Metadata service
4.2 Entities service
4.3 FaceRec service
4.4 Indexing service

### **!! IMPORTANT Remark !!**
AnyVision integration isn't designed to work with mulitple IntSight instances simulatenously.
So, before starting tests (sepcificaly on entities & sync of targets), the environment must be cleared. See this wiki for howto https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/404/Clear-Reset-AV-Face-Recognition-State




### Test the integration
1. Create an entity of the type defined above
1. Wait for an indexing iteration
1. Check if the entity is created as suspect via AnyVision console
1. Create an entity from detection and check as well
