


# Troubleshooting 

Scenario : 
Getting kicked off the web application, 404 Error

1.User permission on the application 

open the admin app - make sure they have all permissions are there. 
![image.png](/.attachments/image-a08f1241-6e71-4924-91bc-11acfeb5007e.png)
![image.png](/.attachments/image-2fb59cab-1e12-4723-9d60-2c575d91e79d.png)


2. in MySQL in sensor table - make sure that the application called Face Recognition

![image.png](/.attachments/image-137f1002-3e09-4d98-b29c-ce86c441b375.png)

3. in MySQL  make sure they config value in system config  points to 
this detectionsDM Value needs to be = to the schemeID in datascheme1 
![image.png](/.attachments/image-a6337962-219c-4254-b2f0-40e49f6105fb.png)

4. On `sqlite_metadata`.`system_config_modules` the key of 'detectionsDM' should be associated to Web Client(3) and Face Recognition (6)
![image.png](/.attachments/image-38991dcf-171f-4708-b6a2-17932cf67029.png)
