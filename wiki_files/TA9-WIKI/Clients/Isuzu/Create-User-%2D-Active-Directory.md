**1.** **Connect to Isuzu VPN**
Connect to the Checkpoint endpoint security with user & password

**2.** **Connect to Isuzu Active Directory** 
Connect to the Remote Desktop Connection (MSTSC) with user & password
computer: _10.100.122.10_

**3. Open Active Directory Users and Computers**

![image.png](/.attachments/image-e25caa1a-d057-4e37-bdf0-0d4c3cbca3c4.png)

**4. Create New User**
Get to the "Users" folder by open evoir.local folder and then click on Users folder
Click on create a new user in that folder

![image.png](/.attachments/image-bccf8574-14f0-460c-9a5c-fa8be6d2a6b6.png)

**5. Fill in User's Data**
First Name & logon Name
Click on Next
Password & Confirm Password
Check the third checkbox only (password never expire)
Click on Next
Click on Finish
The new user is added to the user's list 

![image.png](/.attachments/image-5ba90a8f-d409-4439-b173-6187749a2918.png)
![image.png](/.attachments/image-ea135950-f32c-4b2a-9339-13f87a3503a2.png)

**6. Add Domain to the user**
Right-click on the new user & click Properties
Click on Member Of & Add
Type "intc2" & click Check Names
For Admin - Click on Intc2Admins
For User - Click on Intc2Users
Click OK & OK
Click Apply & OK 

![image.png](/.attachments/image-065e1ddf-717b-4bb8-a7a4-211b9ae489d8.png)
![image.png](/.attachments/image-82e37d26-f4c1-41b7-ab62-902d947e2668.png)
![image.png](/.attachments/image-75e8331d-9a33-47d5-9264-553364f8bb3a.png)
![image.png](/.attachments/image-65a21808-2cf9-470d-9200-f7cbdaff6eb7.png)
![image.png](/.attachments/image-efbde4ba-7663-4149-82be-c3f88da95af1.png)

**7. Check Yourself 1**
Right-click on Intc2Admins (or Intc2Users) & click Properties
Click on Members
You should be able to see the new user you created in the list

![image.png](/.attachments/image-7f4e6b11-83f4-4f50-b23e-fd9580e11c0b.png)

**8. Check Yourself 2**
Enter the system with the new user credentials
(Password & login name that you filled in section number 5,
make sure you are still connected to Isuzu VPN)
http://intc2/login/#/
You should be able to log in easily

![image.png](/.attachments/image-60493e6c-79b3-4a33-8e3b-5c57849bc14b.png)

**9. New User Permissions**
Enter the Isuzu Admin System with an admin user
Give the new user you have created permissions to DM, Cases, Apps, etc.
Clear cache and login again to verify the new user can access what he is authorized to.

![image.png](/.attachments/image-9bdcbcc7-f4ca-46d1-8348-49043bed1e4c.png)

![image.png](/.attachments/image-72f43a03-82ed-4ee2-a1fd-936208e7e292.png)