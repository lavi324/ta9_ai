In cases when links/images in Multiple places across the system seem broken, The cause might be the File server.
The first step in this troubleshooting process would be to log in and validate if this occurs in multiple places.
The Problem might look like this:
![image.png](/.attachments/image-4a27232e-1d6b-4f04-9b35-c1eac418735f.png)
![image.png](/.attachments/image-790d0585-e3bb-4c91-8194-73a7c28a3b59.png)
![image.png](/.attachments/image-8f6d1177-1141-4df2-a2dc-43d0b3e84fd4.png)
![image.png](/.attachments/image-77b66e5d-56c8-4f71-9425-bc63cb82535f.png)

In This case - We would be running a restart action to the file server & TA9 host services:
1. Approve the restart with the Client - make sure nothing is being loaded
2. Log in to the Machine / Server PC, And Open "Services" window
3. Identify and restart the following services, In that order:
- TA9 File Server (Wait till the service is done restarting)
![image.png](/.attachments/image-9ba7071a-8ba3-45c1-b4b0-d92c28c7d430.png)
- TA9 Service host (Wait till the service is done restarting)
![image.png](/.attachments/image-a75daed8-58b2-456f-85da-c08478a480bc.png)
4. Open the system in a new page / Refresh 
5. Validate the issue Had been solved
6. Notify the client.

Fix Time - 5 Min

