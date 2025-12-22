In case you have an error in the system you need to export the logs in the Event Viewer with the following steps:

1. **Connect to the remote desktop:**
 -  Type in Window's search bar:  "MSTSC" and enter
 - Type remote desktop IP 
 - Click on edit

 ![image.png](/.attachments/image-a6eafb22-7d01-43a7-a57d-26fdd90a3876.png)

 *if there is a saved user on the computer, click on "More choices" and click on "Use a different account".

 - Type the credentials to connect to the ta9 environment
 - Certificate error appears, click on yes

![image.png](/.attachments/image-16b714aa-4fc3-41ab-b247-cdb66e635e5e.png)

 - Click on one of the available sessions
 - The remote desktop appears


2. **Open and filter the event viewer:**

 - Type in Window's search bar:  "Event viewer" and enter
 - Event viewer window appears: 

![image.png](/.attachments/image-335317de-5002-4c46-a56b-a9b9950384ca.png)

 - Open the Windows Logs folder and click on Application
 - List of logs appears
 - In order to narrow down the logs to show only the relevant errors - Right-click on Application and click on Filter Current Log...

![image.png](/.attachments/image-47687466-cad3-4ba6-862f-d06ab0529bcf.png)

 - "Filter Current Log" window appears.
 Mark in "Event level" the "Critical" and "Error" checkboxes and type in Event source: "IntSight C# Service"

![image.png](/.attachments/image-bf358fb5-c517-44ea-9b3d-11c2813e23bf.png)


 - Click OK

3. **Export relevant logs of an error**

 - Right-click in the event viewer on Application and click on Clear Log and Clear

![image.png](/.attachments/image-6e49667a-118c-4d02-be9f-ad2be52fc84b.png)

 - The Logs list is empty
 - Go back to the computer's desktop and reproduce the error on the TA9 system 
 - Go back to the remote desktop and click on Security and then click on Application
 - New logs appear
 - Mark all the logs list (click on the first raw + Shift + Click on the last raw)
 - Open the Action menu in the top bar and click on Save Selected Events

![image.png](/.attachments/image-9cef4ad1-be5b-4298-b8a5-4870bb852800.png)

 - Save the file as "ta9 logs" with file type: "Events Files (* .evtx)"
   *Display information: English (United States)


  
