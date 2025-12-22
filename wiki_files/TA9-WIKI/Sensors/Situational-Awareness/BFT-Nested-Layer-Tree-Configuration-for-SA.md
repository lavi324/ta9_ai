1. You need to create a BFT Data Model, The 3 following fields should appear there like the image
A. Fields for the three layers​
B. longitude & latitude fields​
C. Icon field is optional, if not, the default icon will display​
![image.png](/.attachments/image-3ee3b702-4f6f-458f-bf79-f257fbc3a74a.png)

2. Go to Admin Tools
![image.png](/.attachments/image-f4c04a4e-eef7-47be-9dce-7a04a5fefb2e.png)
3. Go to System Configuration
![image.png](/.attachments/image-abd91f6c-a503-46c2-bcc6-8fbe3e6a7ae5.png)
4. Select the Web Client module
![image.png](/.attachments/image-80778b0b-ab4c-474e-a1de-9d524e4a6ad2.png)
5. Add the "Config Key" of 'singleLayersFilterConfiguration', its "Config Value" needs to be a JSON that looks like this, just edit the parameters according to your BFT DM
![image.png](/.attachments/image-6f9c57fa-a81b-4221-b166-be733c5c157d.png)
6. Go to SA App and click on the siren at the top toolbar like the image, then click the switch to turn on BFT
![image.png](/.attachments/image-885c1944-742f-409b-9f64-347c0952f156.png)
7. Now your map should look like the following image and you can decide which layers you want to see on the map and which you do not
![image.png](/.attachments/image-9397cea8-d81d-4e4c-8cff-a42e1bf3bb86.png)