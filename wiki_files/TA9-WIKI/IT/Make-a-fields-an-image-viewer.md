[[_TOC_]]

#IIS

##Windows folder
Go to the wanted server and open a new folder in a well known location, for example:

`C:\Program Files\TA9\{New_Folder}`

## Link to IIS
You will need to upload the windows folder to the inernet so Argus will be able to read the images.
###1. Open IIS manager
![image.png](/.attachments/image-179b90ef-ed9f-46e5-bca4-9f3d9d3ab32c.png)
###2. Add new Virtual Directory
![image.png](/.attachments/image-b801bca5-c25c-4a04-9451-00b916a5981f.png)
###3. Link between the two folders
![image.png](/.attachments/image-fbd2bfec-fa9f-4097-8033-53c037d53caa.png)

#Datamodel 
## Find the DM
Open the workbench and go to the table: "dataschema1", get the ID for the relevant DM.
![image.png](/.attachments/image-956ceff2-509a-4dbb-904a-e0ed7e71e457.png)

## Find the Field(s)
Go to the table: "dataschemafields1", find the fields by filtering with the ID of the DM.
![image.png](/.attachments/image-6c5fab9b-475e-4f07-a89c-035d2474c901.png)

After finding all the fields choose the wanted field(s) and configure them to be shown as image viewer by changing the ViewerID to 16.
![image.png](/.attachments/image-31a46ef1-ff3e-4070-b7fb-b373ead12369.png)

## Configure the fields
Go to the table: "systemconfig", and find the value: "customPathsDefinitions", take the value and add your field(s) there.
![image.png](/.attachments/image-0ef27743-50ba-44a1-a552-fd5951dbf816.png)
add your field(s) as shown in JSON format.


	"{Fields_ID}":{
	"baseUrl": "{Image_URL**}",
	"viewerType": "2"
	}

Save the changes and Clear Server Cache when done to apply changes.