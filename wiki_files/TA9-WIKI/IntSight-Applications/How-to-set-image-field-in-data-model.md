1. Open the admin studio.
2. Go to Data Models and open your data model.
3. Click on the image field.
4. Set the viewer field to be 'Custom Path Viewer'

![image.png](/.attachments/image-d5147274-d5d0-45a6-9704-16d745c35d05.png)

5. Copy the field ID (for the next step)

![image.png](/.attachments/image-7f88060d-a7da-4f06-92ab-4469f4b47b76.png)

6. Open the system and navigate to the admin tools.
7. Open the system configurations. 

![image.png](/.attachments/image-e01b3fc2-5124-45b6-ae99-f9e04d61e43c.png)

8. Select module - Web Client.
9. Search for custom Path Definitions on config key column.
10. Click on the edit button. 

![image.png](/.attachments/image-0b96d226-662d-4406-a052-29dbca179163.png)

11. Add this row to the config value and save
 `"XXX": {        "baseUrl": "http://10.100.120.80/images/",        "viewerType": "2"    }`

Put the field ID of the image field instead of the XXX.

Note that the field is in JSON format so you need to keep it in the correct format to make it work.

12. Clear server cache.

