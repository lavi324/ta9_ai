A complaint had arrived from the client - dashboard export fails.

A possible root cause for this issue is a full capacity of seaweed volumes.

In order to check if the seaweedFS has free volumes, open the seaweedFS interface on the web. In the browser URL type the IP where the seaweedFS is running and add port 9334.

**If there are not enough volumes for the seaweedFS you will see 0 next to the Free like the picture:**
![image.png](/.attachments/image-86973324-50f2-4c85-bd57-4c836fddea81.png)

*In order to check if the volumes are full, go to the folder the File Server folder is running as the data storage for the file server. You can find the path to this folder in the start.bat file that is located in the file server folder:

![image.png](/.attachments/image-0fba0a64-1c0c-4c98-812d-2cd51dbd6ed6.png)

The DAT files max size is approximately 30GB. So if you see that all files are at 30GB capacity, it means volumes should be added to the seaweedFS.

![image.png](/.attachments/image-5aea4d40-1c74-4c4b-9b82-2128db4571d3.png)

**To add volumes to the following:**
1.	Go to the File Server Folder on your app server (In the Isuzu environment, the start.bat can be found under TA9\Utils folder path.
2.	Edit the start.bat file
3.	Look for a -max flag in the file like this photo
4.	Change this to how many volumes you want the seaweedFS to have




