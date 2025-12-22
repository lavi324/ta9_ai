# Troubleshooting

## Scenarios
1. The login page appears without the translations.
2. Unable to log in.
3. The 'TA9 host service' is down after trying to log in.

   
## Solution and steps:

1. Check in the event viewer for the following log error:
 **The log from the event viewer**
Unhandled Exception: MySql.Data.MySqlClient.MySqlException: Authentication to host 'localhost' for user 'root' using method 'mysql_native_password' failed with message: Reading from the stream has failed. ---> MySql.Data.MySqlClient.MySqlException: Reading from the stream has failed.

**The error means that the system unable to connect to the mySql.**

2. Do a restart for the machine and check if its works.

3. Try to check the connection string:

- Find and open the file - ConnectionsManager.config
should be under This PC-> Local Disk->Program Files->TA9->C#->TA9 Core Services
- Right click on the file and click on open with notepad++  

![image.png](/.attachments/image-cb43a5b6-714f-4d97-a9fb-140683e8b8ad.png)
 
![image.png](/.attachments/image-c19d7ef9-d2e8-40e9-a256-740b755821c6.png)
The connection string is encrypt 
Copy the connection string to the encryptor and click on decrypt
The connection string should include the correct user name and password  

**Note!** If you want to change the connection string save backup first.

The connection string should include the correct user name and password  

If you changed the connection string you need to replace the file in all folders 
under This PC-> Local Disk->Program Files->TA9->C#->TA9 Core Services->Services

![image.png](/.attachments/image-459f8217-1efb-4c90-9d14-76eb41e3b453.png)

Start the TA9 Service Host and check if its work.