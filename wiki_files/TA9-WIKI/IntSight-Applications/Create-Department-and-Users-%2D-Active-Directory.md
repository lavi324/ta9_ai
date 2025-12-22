**Prerequisite**

In the server, under path "D:\TA9\C#\TA9 Core Services\Services\UserManagement.Service"
Find file 'UserManagement.Service.dll.config' (Note that this is a _text_ file and not a dll file) in the folder

Navigate to section <appSettings> and locate the _DC_ values in the keys:
For example -

![image.png](/.attachments/image-e06757b9-a49f-4f7c-98d1-cc530be59f9b.png)

Make sure that section <appSettings> includes the following line with the relevant DC values that you found before:

```
<add key="DepartmentsGroupName" value= "OU=Departments,DC=Copied_DC_Value_1,DC=Copied_DC_Value_2"/>
```

The final result will look like this example section:

```
<appSettings>
	<add key="ClientUserPropertyName" value="dummy"/>
	<add key="ExternalUserManagement" value="ActiveDirectory"/>
	<add key="ActiveDirectory" value="{Here_Will_Be_Some_String}"/>
	<add key="SyncInterval" value= "60000"/>
	<add key="IsExternalUserSyncer" value= "true"/>
	<add key="AdminGroupName" value= "CN=TA9Admins,CN=Users,DC=t-a9,DC=org"/>
	<add key="UserGroupName" value= "CN=TA9Users,CN=Users,DC=t-a9,DC=org"/>
	<add key="DepartmentsGroupName" value= "OU=Departments,DC=t-a9,DC=org"/>
</appSettings>
```

**Note:**
The order of the values in the '_DepartmentsGroupName_' key is important and it Is a mirror of the Active Directory folder hierarchy. For example 
- **If** the domain name for your organization is "ta9.org" 
- **And** the Name of the Main parent department is "Departments"
- **Then** the correct order of values is as follows:
<add key="DepartmentsGroupName" value= "OU=Departments,DC=t-a9,DC=org"/>
  
**Note 2:**
Notice that **both parent department folder** and **subfolders** (other departments) must be "organizational units" in active directory.

**1. Connect to the Active Directory**
Connect to the Remote Desktop Connection (MSTSC) with user & password
computer: {type_ActiveDirectoryIP_here}

![image.png](/.attachments/image-34c5e408-b211-4f1d-8737-4cea88e02718.png)

open Active Directory

![image.png](/.attachments/image-c3f4690b-06f5-46a9-9384-f1e43ca5ef9e.png)



**2. Create new department (Organizational Unit)**

 t-a9.org -> right-click on Groups -> New -> Organizational Unit

![image.png](/.attachments/image-c5c4f2d1-24b8-4ebf-945e-86e772b7eefc.png)



**3. Insert department name**

![image.png](/.attachments/image-3a6d801c-f5c5-41ea-a2c8-4667e5934840.png)

Make sure the checkbox is clear in order to be able to erase the organizational unit.


**4. Create a user**

Right-click on the Users list -> New -> Uesr


![image.png](/.attachments/image-931c1643-883f-46db-8308-4c0d1f14718c.png)

Apply the following details, and click next:

![image.png](/.attachments/image-2f749143-4fd1-4936-85b6-f35c31baa435.png)

Set a password and finish:

![image.png](/.attachments/image-e42f2765-6bdf-4d0d-8a5f-62252d50df47.png)

Now you can see the user you created in the Users list.



**5. Connect an Existing User to a Department (Group):**
In the **Users** list, right-click on the user name and open the properties window:

 ![image.png](/.attachments/image-a43083c3-c744-4562-bd2e-c9bfb03ec8df.png)

click on 'Attribute Editor' > search for 'userPrincipalName' > click on 'Edit' : 

![image.png](/.attachments/image-857d4fce-84f4-47ee-9c27-352c6316dde4.png)

copy the string:
![image.png](/.attachments/image-6539ecfb-eec5-4a43-b092-d41b991170ba.png)  


Right-click on the requested group you want to connect the user to > New > Contact

![image.png](/.attachments/image-9c339ffc-04ce-4909-9eed-fa4fa7e44c3d.png)

Fill in first and last name > set the copied string as the full name > click 'ok':
![image.png](/.attachments/image-4e7acd9e-40d4-4590-900b-a2b70b32d707.png)

Make sure the user name appears under the group:

![image.png](/.attachments/image-574c00b2-f5f5-4ae3-99a1-8bd97859ea54.png)

**It is possible to recreate the process, and set the same user to multiple departments.**



In order to add Domain to the user, right-click on the new user > click Properties > Click on 'Member Of' tab > Click 'Add':

![image.png](/.attachments/image-672b55ec-b453-40a9-8c25-91c22b17abe3.png)

Type "Ta9" > click Check Names:
For Admin > Click 'TA9Admins'
For User > Click 'TA9Users'
Click OK > Apply > OK

![image.png](/.attachments/image-7fb880a4-2e8b-4444-8bd8-fe5f976ea600.png)

***

# Please note that attribute wise:
* AD User's `userPrincipleName` attribute is its unique name (t-a9's Login Name).
* AD Contact's `cn` attribute is created automatically when we write the above value in the `Full Name` field







