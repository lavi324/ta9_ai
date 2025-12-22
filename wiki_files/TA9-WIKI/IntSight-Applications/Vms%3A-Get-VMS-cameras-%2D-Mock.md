**Connection settings:**
In order to synchronize/bring vms_cameras, follow the following steps:

First, you need to make sure that MockServer is up and running. 
Find vms_mock in \\\10.100.102.13\Share\Vms\vms_mock\vms_mock and move it to the needed environment: 

![image.png](/.attachments/image-acab7f67-f595-4eb5-b617-ef6456b497ca.png)

After moving it, open the command prompt in vms-mock folder, and run the following command : 
`node index.js`

![image.png](/.attachments/image-e5f3b2c7-3d01-4d31-a570-a62452cddffe.png)


After mockServer is up and running, open PowerShell and run the following script.

Pay attention, in order to send a request, you need to provide a valid authentication token and needed IP

NOTE: Token pointing on the RZ mock service - should be found in **apsettings.json** in VMS config folder: 
_D:\TA9\Albert Services\VMS_
![image.png](/.attachments/image-5dc831fc-d228-47b1-bd7f-c518747b1aff.png)

![image.png](/.attachments/image-31211800-68a8-4f21-9d72-5e6c7011354d.png)

Isuzu stage environment URL example: 'http://intc2-stg:8094/api/Vms/Request/Update/Cameras'
```
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("token", "{token}")

$response = Invoke-RestMethod 'http://{IP}:8094/api/Vms/Request/Update/Cameras' -Method 'GET' -Headers $headers
$response | ConvertTo-Json
```
IP= the Ip Address on the running machine
Token= Valid user token (admin) -(SELECT * FROM sqlite_metadata.user_token order by token_expiration desc;)
Run the following script in Windows PowerShell, and in case of success, You'll see an 'Ok' response message. 

**Connecting To a video File**
The Mock VMS service knows to send a video for every new request. (Same video file).
This video needs to be stored in the X:\VMS_API_MOCK\videoSmaple

Video settings:
Length - up to 30sec
FileName - 1
Type - Mp4


**Reading VMS Logs:**
D:\TA9\Albert Services\VMS\logs
