#Symptom

Authentication.Service.dll
In the Event Viewer.



![Image from iOS.jpg](/.attachments/Image%20from%20iOS-23fc9efb-8a69-4346-a2a3-78d17aa5477b.jpg)



![Image from iOS (1).jpg](/.attachments/Image%20from%20iOS%20(1)-6afb21fc-4f3d-4e65-b382-568ad6b8b6ed.jpg)


For files downloaded from any source became locked downn -
Run this script via PowerShell with admin privileges: 
  
dir -Path "C:\whatever\folder" -Recurse | Unblock-File

or do it manually as the picture above