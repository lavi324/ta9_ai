when users are unable to upload .doc or .pdf files to the system first go to the logs on the app server ( if you are seeing an error which looks like this:

error trying to get files details from TextAnalyticsService. file: \\cawinsrv01.ecis.local\upload\637952018636925923\EntityExtractionTest.pdf 
Exception: System.Exception: error trying to get files details from TextAnalyticsService.

This means that the windows server (App Server) lost connection with the Linux Server (File Server) and that the mount of the shared folder was dropped.
The mount path is /mnt/winshare/upload and the File System name is //IP/upload.

It means that when you type "df -h"  command on the Linux Server:
![image.png](/.attachments/image-515401b3-2991-47bc-aec0-abcc6e9dfcca.png)
You will not see the marked line, when this happens, just run the command "mount -a" for the mount to be remounted, just make sure by typing the command "df -h" again and it should look like the picture above and there you have it!