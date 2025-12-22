## Goal
create the configuration needed to integrate the Echo App automatically into the TA9 system  

## Steps
1. Put the relevant DLL in the right location in the correspondent server
![image.png](/.attachments/image-e15cac5d-8079-47b5-8379-a47033fb3284.png)

2. Create a DM based on this Plugin using the [TA9Copy](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/26/TACopy) 
Then, make sure you see the relevant rows in the following MySql tables:
**DataSchema1** table:
![image.png](/.attachments/image-c40e3f18-58df-4621-b231-bcf3c3f4c218.png)
**DataSchemaFields1** table:
![image.png](/.attachments/image-7efe4c2d-49ab-42de-bfc4-7fc03c6290ab.png)
**UserDataModels1** table:
![image.png](/.attachments/image-fb56e19e-8588-4f87-b4ba-7e7839aed387.png)
**DatModelGroupHierarchy1** table:
![image.png](/.attachments/image-478f7637-b4aa-4b10-9486-fa666b6b0c7a.png)
3. Make sure that the 'connectionid' field as is displayed in 'DataSchema1' table, exists in the 'dataconnectionsmanager' table of the relevant environment.
**DataConnectionsManager** table:
![image.png](/.attachments/image-dde87382-66b3-42b7-9a6c-b3d77cba05cf.png)
4. Create an auto-loader to the Echo plugin
   -  Upload the Echo CSV file to a Windows server- 
 by adding a new row to the **data_loader** table with the relevant paths of the upload folders:
![image.png](/.attachments/image-902ec054-2c72-4bf7-9e7b-d120160cd3e5.png)
Then, create the 's' & 'f' folders in the same paths of the Windows server
![image.png](/.attachments/image-ddeb199c-7ccd-4d98-ad97-efac70db524d.png)
   - Upload the Echo CSV file to a Linux server- 
by adding a new row to the **data_loader** table with the relevant paths of the upload folders:
![image.png](/.attachments/image-144f6ff6-eaff-4c07-a25d-c8b252feee26.png)
Then, create the 's' & 'f' folders in the same paths of the Linux server using FileZilla
![image.png](/.attachments/image-09e61782-0745-42db-b969-f3459950d77d.png)
5. Reset the TA9 service host so the new dll will be applied
6. Make sure the Rayzone side has opened the port for the server's IP where the DLL is stored, so the system will be able to create API calls to the Echo system automatically.
7. Test the Echo integration
 by sending a phone number to the Plugin as Action (using the View Action in the TA9 web system)
![image.png](/.attachments/image-6274accf-77d1-4afe-9c42-f40086de71e6.png)
 and opening the Data loader to verify the file has been uploaded successfully to the system
![image.png](/.attachments/image-098c26af-52f9-4a45-a87e-a2894afdc7e1.png)