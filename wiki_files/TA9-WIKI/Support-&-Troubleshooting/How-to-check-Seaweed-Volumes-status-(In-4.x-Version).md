To check the volumes status in Seaweed please do the following.

Browse to the URL of the Seaweed with it's defined port (port 9333)

The volume limit can be seen next to the Volume Size Limit.

![image.png](/.attachments/image-a6e876e4-ad61-4591-8a0b-fe312769b26b.png)

Pressing the URL will direct you to a page to view the storage usage.

![image.png](/.attachments/image-630f2b33-6de0-48f1-bdc0-3c033d997bcc.png)

If all the volumes are maxed at their limit, you need to create and allocate more volumes.

Volume amount is controlled via the docker-compose.yml file located in the seaweed stack.

![image.png](/.attachments/image-a3ed45c3-dd6c-41e3-9f12-aa61e5fef091.png)