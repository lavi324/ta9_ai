Connect to the server and open the Active Directory window:

![image.png](/.attachments/image-041b5a73-6d1e-45f2-abeb-14c0aa723a89.png)

## Creating  users and assigning to groups:

click on the TA9 folder > new > organizational unit:

![image.png](/.attachments/image-ffceac45-e99a-4dac-9685-fe0a1a0ec74c.png)

Choose the name of the new folders:

![image.png](/.attachments/image-25cfd2b1-24f1-4948-a70e-634ff46dfbb7.png)
![image.png](/.attachments/image-c8af798b-932f-4ef5-980c-0ac3558fce40.png)

**In the TA9-Users-Test file:** 
 1. create a new group:

![image.png](/.attachments/image-3a5fcaeb-3148-4544-8d44-6e54e1e7d280.png)![image.png](/.attachments/image-291f6fe8-3d87-4d0e-af5c-f60f7ff89dcd.png)

 2. create a new user:

![image.png](/.attachments/image-049ab3fd-21ec-495b-b6d3-746eba7fcb9d.png)![image.png](/.attachments/image-874fa28b-24db-4835-92fc-e1fc7b3838d5.png)
![image.png](/.attachments/image-e8ef56ac-888a-4818-b25d-e134479381de.png)



**Assigning users into a group:**

Open properties of the new group:
![image.png](/.attachments/image-fc8e3c78-2769-4b7d-b285-b837c699223f.png)
click on member of>Add:
![image.png](/.attachments/image-7f877d89-f1a5-4c94-8029-a9440d72bdaa.png)
The "Select Group" window will open. Then insert "TA9":
![image.png](/.attachments/image-8eef569b-4aa7-4c79-acfc-8cfdd711b032.png)
Choose the right group:
![image.png](/.attachments/image-f041215a-329b-41da-bff0-317838c7fb00.png)

**Do the same process with the "TA9AdminTest" (assigning the user admin to the group admin).**

## **Creating a service Admin:**
opening a new organizational unit (user):
![image.png](/.attachments/image-188b345c-4e73-4b66-bfaa-7679773f5a49.png)
![image.png](/.attachments/image-36c7f4f8-8ce2-4cd6-8657-09cc84659667.png)

Assigning it to groups of the admins **AND** users:

![image.png](/.attachments/image-05b39e24-ff6d-45d3-812d-8d082d6bc2a6.png)
![image.png](/.attachments/image-d8092de0-12a7-4bcb-b9ae-250430e52324.png)
![image.png](/.attachments/image-2379623d-b722-46bc-a5db-be6d25369e16.png)

Add a new Department: 
![image.png](/.attachments/image-995dbe92-22ee-4409-94d3-f0d93a774b14.png)
![image.png](/.attachments/image-5bc7e264-8a4b-43aa-8ef6-9c18798bedb4.png)

## Configuration Change in DLL:
Open the next file:
"Usermanagement.Service.dll.config"
Which is under: 
C:\Program Files\TA9\C#\TA9 Core Services\Services\UserManagement.Service
open with notepad++
change the names of : Admin, Users, Department
![image.png](/.attachments/image-b32de825-3f59-4cf0-a429-5f6926a2075c.png)

CN - group name
OU - folder name

## Configuration Change in MySQL:
open "users" table
copy the row of service admin, and past it to the same table, change the name to the "ServiceAdminTest".
![image.png](/.attachments/image-a328ba4a-a857-49e7-acd7-087b68fd6886.png)


Copy the new row with the new name and userID, and past it to the following tables:

- userpermissions
- userdatamodels1
- usersensors
- actionsuser
- groupusers

