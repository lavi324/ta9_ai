**Goal**: export a dashboard\case's summary tab as a PDF or DOC file

First, we need to make sure the **template file** exists under the correct configuration in the system
We will do that using the MySql table 'system_config' in the relevant environment.
After searching for the word 'Export' we will see the relevant export file we were looking for,
and the export template file ID which is in the ConfigValue field.

![image (24).png](/.attachments/image%20(24)-f03093b5-7972-4622-9842-d67aa6f3b690.png)

Then, we will make sure the file is actually uploaded to the system by searching it in the SeaWeed.
We extract the fileID from the ConfigValue field as displayed above,
and type it together with the correspondent file server's IP of the relevant environment in the following format - 
http://<environmentID>:9334/<fileID>

For Instance, if we want to check whether or not the above template file exists in the 52 environment,
we will look for the following URL - 

![image (25).png](/.attachments/image%20(25)-df3af3d7-014b-47da-9e28-b64039be3b1e.png)

On search, the port (9334) is redirecting to the 8800 port and then we have 2 different possibilities: 
 - The file exists 
   The file is displayed on the same page OR the file is downloaded to the computer
![image (26).png](/.attachments/image%20(26)-2fbb297f-b518-43cf-9608-903c708e5925.png)

- The file does not exist
  An error is displayed, which means the SeaWeed couldn't find the desired file
**Solution!**
  We can upload the relevant template file to the SeaWeed by one of the following methods:
   - Upload the file directly from the Ta9 system 'Data Loader'
![image.png](/.attachments/image-20f005c3-49ec-44d0-a0c2-90f8a69f1624.png)
   - Upload the file from the Postman App
[Upload-Files-using-Postman](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/566/Upload-Files-using-Postman)
After the file has been uploaded to the system, we need to copy the file ID 
and paste it in the corresponding place in the same MySql table we have already discussed, 'system_config'. 
We can check what is the file ID in the MYSQL table named 'load_files' by using the following query - 
`SELECT * FROM sqlite_metadata.load_files order by id desc;`
Copy the: Serverfilepath 
![image.png](/.attachments/image-82a1719e-8fa9-4ecb-aa2c-be634766c983.png)
Paste it in: ConfigValue
![image (24).png](/.attachments/image%20(24)-f03093b5-7972-4622-9842-d67aa6f3b690.png)



