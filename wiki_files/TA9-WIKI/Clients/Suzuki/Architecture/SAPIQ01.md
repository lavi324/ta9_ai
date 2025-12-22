What is in the server:
1. IQ DB - D:\IQ16, also holds the license files
2. IQ Data - G:\Data
3. Logs on E drive
4. F drive - holds the IQ Cache - will always use all the drive space

Windows Services:
1. TA9 IQ Service

IIS:
1. Used for getting requests from App01
2. Url Rewrite - [IIS Reverse proxy](/TA9-WIKI/3rd-Party-Software/Servers/IIS/IIS-Reverse-proxy)

Remarks:
To identify how many cores are allocated to the license run the following command on IQ:
Sp_iqlmconfig
![image.png](/.attachments/image-468c61a8-735d-4418-b6ce-f56d9ad4c0d7.png)