1. Connect to the requested client environment (using the .xslx pass file) and click on "Admin Tools" bar:
![image.png](/.attachments/image-36509058-617e-4e0f-a603-2606b62c0e9f.png)

Click on "User Management" widget:
![image.png](/.attachments/image-50d3ae19-eff2-43f1-97ef-8980e71357d1.png)

Click on the plus icon ("new") in the right top corner, and open this window:
![image.png](/.attachments/image-e4b8d4ea-39e7-4137-a048-7704b5a29662.png)

Set a **Login name** and **First name**, as well as any other available info you have.
Click on save icon and activate the user via "v" in "ActiveUser" bullet.

The **default password** is 123456. After the first login, the system will require a setting of a new one. 

------
## 2. How to define a user as Admin
 Connect to the environment's Admin (using the .xslx pass file), to the relevant remote desktop connection, and open the admin studio:

![image.png](/.attachments/image-df91a0c7-134f-4861-8dc4-2d1ac89ab6c2.png)

click on "Users" widget, and open the next window:
![image.png](/.attachments/image-6db67d89-1769-4f93-b578-abb15313414e.png)

Here you can reset the **2FA** code of a chosen user, and discard it if necessary.
Also, you can **activate** and deactivate the user, and set it as **admin**.
You can control the **permissions** of the user by the toolbar indicated above. Permissions are given to each user individually.

Choose the required setting and **save**.

------
## 3. How to set a permanent password and encode it
  Connect to the environment DB via **MySQL** (and the .xslx pass file).
Run the next query in order to see "user" table:
`SELECT * FROM sqlite_metadata.users;` 

![image.png](/.attachments/image-602ef6ab-d629-480f-a030-4be471152f6b.png)

In order to enter a different password, we need to encode the password first.

Encoding the password is via the **"Encryptor"**, You can find it in:
[ _Z:\OneDrive - TA9 (old)\ServerBackups\ChinaPhase2\IntSight - 2.1\2.TA9_Intsight_Vanilla\2.1.Encryptor\TAEncryptor_exe_]()


click on:![image.png](/.attachments/image-41f5d5b6-dc32-44b9-a6b4-9b69e3736e3b.png)

and choose a password:
![image.png](/.attachments/image-02c66fe5-db70-4a84-9eeb-7c90031e1941.png)

Copy the encoded password to the relevant "userID" row in "Password" column.

**(Setting permissions to a user via DB - Optionary)**
To extract the "User Perimission" table in MySQL DB, insert the next query:
`SELECT * FROM sqlite_metadata.userpermissions;` 

![image.png](/.attachments/image-827fd595-2a15-40ed-b904-a21b0752c61c.png)

Now you can change the permission of the user by changing the 'userID' column as followed:
If the user **is not admin**, then change the value to '0' ('userID=0')
If the user **is admin**, then change the value to '1' ('userID=1').
OR 
By inserting the next query:
`UPDATE sqlite_metadata.userpermissions
SET ISAdmin = 1
WHERE userID=X;`
Change the x according to the required user.


---------

In order to create a new user through **Active Directory**:
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/576/Create-Department-and-Users-Active-Directory
