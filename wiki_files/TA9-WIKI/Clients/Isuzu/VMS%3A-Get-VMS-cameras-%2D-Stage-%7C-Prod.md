The configuration file is on the app server - 
For stage: 10.100.105.90
For Production: 10.100.102.90
NOTE: Token pointing on the RZ mock service - should be found in **appsettings.json** in VMS config folder: 
_D:\TA9\Albert Services\VMS_
![image.png](/.attachments/image-5dc831fc-d228-47b1-bd7f-c518747b1aff.png)

**appsettings.json on stage environment**

![image.png](/.attachments/image-724ae7cb-ef89-4cd8-8aa3-0d8e8da7ba87.png)


Isuzu stage environment VMS port: 3001
Isuzu production environment VMS port: 3000


**Reading VMS Logs on Stage environment:**
D:\TA9\Albert Services\VMS\logs

Rayzone are responsible for the request from huawei, TA9 are requesting the video itself from the Rayzone service.

**Postman check on stage environment**

1. Enter postman Application
2. Make new Request
3. Go to Request type and put in POST, on the URL put http://didatadmz:3001/vms/recording for the Stage VMS
4. You will need to choose format to enter your body for the request, so choose raw, and JSON type
5. Go to Body of request, you will need 4 parameters (jobId, cameraId, startTime, endTime), enter the details you need for your specific request
**it should look like this:**
![image.png](/.attachments/image-8224ca97-a698-473e-9054-a4f9fa1a298e.png)
6. Go to Authorization, on Type choose Bearer Token, and insert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiVk1TQVBJIn0.d2lYUl3a4riMmmTCxCg2bddp7dIXeI0nWxfxSjv1VXs"
for isuzu Stage environment
**it should look like this:**
![image.png](/.attachments/image-25832222-9150-4a99-8aa3-2b00e8c214d1.png)
7. Click on send request and it should output:

    "msg": "File was created for job XXX"
XXX represents the job number you entered
8. **the final result should look like this:**
![image.png](/.attachments/image-9dccee48-e386-4e77-9ed0-4b9ae32baf9e.png)
