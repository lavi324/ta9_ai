 https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7BE4FD26F4-91E2-4537-8E2F-35D69E9049D6%7D&file=User%20Management%20API.docx&wdLOR=cC66F3131-69DC-4117-BD84-FA9F48D5F388&fromShare=true&action=default&mobileredirect=true
 
http://10.100.102.23:5070/swagger/index.html?urls.primaryName=User+Management+-+v1

**User Management API –** 
​

**Intro**   

The TA9 IntSight "User Management" module facilitates the management of users and departments, the association of users with departments, and the assignment of different permissions for users. The module's various options can be accessed either through the Admin Studio or by interfacing with the Active Directory. With the introduction of version 4.2, the product now also supports the "User Management" module via a REST API. 

 

The documentation provides details on the TA9 IntSight User Management API, enabling the utilization of functionalities such as user and department synchronizations, as well as the establishment of user-department relationships, along with the allocation of action permissions. 

 

**Configuration:** 


The definition for how the platform managing users is set in Vault is as follows with 3 options - 

Internal – 1 

Active directory – 2 

API –3 

 

 ExternalUserManagement parameter - Choosing user’s access to the system. 

**For example**: “DataSource”: “3”  

AuthenticationConfig parameter – See which user management is used. 

**For example**: “LoginAuth”:”3” 

 

The platform only supports one mode at a time. 

To set the module for working with an API, set the parameter to 3, In all other settings (internal or Active directory) calling the API will block and return an error message. 

 

Internal user switching to API “User Management” mode when the users already managed 	by “Internal” configuration, all existing users will be deactivated.  

 

The API documentation is separated into various categories as follows: 

- Actions 

- Users 

- Departments 

 

This documentation covers the following use cases: 

 

**Users** 

- Create new users. 

- Update existing user. 

- Deactivating user. 

- Get all active users. 

- Get all user actions permissions. Add actions to a single user. 

- Remove actions to single user. 

- Link between user and departments. 

- Add/Remove a sensor for a user. 

        **Departments** 

- Creating a new department. 

- Updating department name. 

- Deactivate department. 

- Remove users from department. 

- Actions 

- Set action to users. 

- Remove action to users. 

 

 

       **Data Models -**  

A user with access to the admin studio can choose which DMs will be distributed to the users of the system from here on. Instead of updating one by one, the admin user will be able to update for all users. Any DM that will be added after that, cannot retroactively, but will be able to update one by one. 

 
**Glossary**  


A glossary is a collection of words pertaining to a specific property; we at TA9 have some terms you must be familiar with to understand the system. 



|Item name  | Definition  |
|User|System user can be “Analyst” or “Admin”|
| UserID  | The primary ID to make updates and actions for a user  |
| LoginName  | Will be the property the user will sign into the system with, and it must be unique  |
| Active  |  The user mode for using the system|
| isAdmin  | The user mode of being an admin in the system – can create and edit in Studio Admin|
| Mode |Defines the user status in the system |
| Action| The user abilities in the system, what he can or cannot do or see|
| ActionId| The Action function identifier|
| Delete|Data will not be deleted, delete means - Remove, Make Inactive|
|DepartmentId| The Department function identifier|

| DepartmentName |Selected sections division of the system |
|isValid|Insert if the department is Active or Inactive|


**Log in -** 
 

### User management – All system connection options. 

**Admin Studio** – TA9 default internal user management – Using the internal system Authentication. 

**Sync Active Directory** - Enables administrators to manage permissions and access to network resources – Authentication will be used by AD. 

**API** – Different software Communicates and change data with TA9 IntSight using Authentication of AD or SSO 

 

**Internal Admin studio** 

 

Default mode of system installation. 

Users are managed internally via the TA9 Studio. 

By default, the system includes predefined admin user. 

 

**Active Directory with active sync** 

 

- Authentication is performed using AD. 

- Periodic task sync user from AD to TA9 every few minutes. 

- Sync includes admin role, active/inactive, user login and mail. 

 

**Active Directory with API** 

 

Only Authentication is performed using AD. 

Users are managed by API. 

At least one admin user must be created with TA9 admin prior to switching to API. 

 

SSO 

Authentication is performed using supported OpenID flow. 

Users are managed by API. 

At least one admin user must be created with TA9 admin prior to switching to API. 

 

# Additional documentation will be sent to a TA9 user who switches to AD or API use. 

 

API  

Every call to the API needs to be with a valid Admin user token.  

 

 

 

 

**Users** 

 


**Create new users.**  

**Use case**: To create new user in the system. 

**Method**: POST/api/external/users  

**Additional details**: The following attributes Must be provided. 

![image.png](/.attachments/image-9e897cad-5b1f-485f-b211-dc32cc0b98ed.png)


 

**Update Existing user.** 

**Use case:** Edit user – Updates user details. 

**Method:** PUT/api/external/users  

**Additional details:** Does not support activate/deactivate status for user. 

![image.png](/.attachments/image-fd40f3c0-f64a-4b4a-a3e6-64864912768d.png)


 

**Deactivating user**  

**Use case:** After creating user, you can edit his status and change it to - Active or Inactive 

**Method:** PUT/api/external/users/{userId}/{active} – 

**Additional details**: Activate/Deactivate active user. 

![image.png](/.attachments/image-710b42d5-a794-4202-9e8a-2010ac1584b5.png)




**See all active or inactive users** 

**Use case:** To get all user’s status – Active, Inactive or both. 

**Method**: GET/api/external/users  

**Additional details**: If mode is not providing will return all users. 

 ![image.png](/.attachments/image-08228e6c-3723-4c8f-996c-02c2653443f5.png)



All Active/all inactive or Both 

**See all actions of a user.** 

**Use case:** To get all user’s actions by searching from the user side (single user) 

**Method:** GET/api/external/users/{userId}/actions  

**Additional details**: Get all user actions. 
![image.png](/.attachments/image-35752755-cc0e-4036-966e-b4487e7a2c77.png) 
 

**Add list of actions for a user** 

**Use case**: To add one or more actions for one user. 

**Method:** POST/api/external/users/{userId}/actions Add list of actions that user can do 

**Additional details:**  

! If the “actionID” is unknown à Go to “ACTIONS” in the swagger àGET API 		        ACTIONS and insert the relevant action ID 
![image.png](/.attachments/image-0f55d19d-3d27-4839-bd02-848e84c22021.png)
 



**Remove Actions for a user.** 

**Use case:** To remove a single or multi actions for a single user from user side. 

**Method**: DELETE/api/external/users/{userId}/actions  

**Additional details**: Remove list of actions from user. 

! To remove department DO NOT make deletion – make the department 	INACTIVE 

! If the “actionID” is unknown à Go to “ACTIONS” in the swagger GET API 	ACTIONS and insert the relevant action ID 

 
![image.png](/.attachments/image-d4a26f98-6091-497b-962a-acadd260a5d3.png)
 

 

 

**Add permissions of a sensor** 

**Use case:** Add permission to the user for list of sensors. 

**Method**: POST/api/external/users/{userId}/sensors 

**Additional details**: The sensor can be active or inactive. 

 ![image.png](/.attachments/image-76a1929d-532c-4daf-9fc6-d583139fe6d6.png)



 

**Remove sensors for a user.** 

**Use Case**: Remove permissions to the user for list of sensors. 

**Method**: DELETE/api/external/users/{userId}/sensors 

**Additional details**:  

! To remove sensor DO NOT make deletion – make the sensor INACTIVE. 

 ![image.png](/.attachments/image-0822a055-7a30-48b8-a12a-37270ec04d34.png)

 



 



**Departments** 

 

**Creating a new department** 

**Use case**: To create a new department. 

**Method**: POST/api/external/departments  

**Additional details**: Create new department. 

 ![image.png](/.attachments/image-c38a49da-e3b3-4f1a-a218-e8f12d66f716.png)


 



**Link between user and departments** 

**Use case**: To link between single use to one or multi departments. 

**Method**: POST/api/departments/{externalId}/users/{userId} Add user to departments 

**Additional details**:  

! If the “userID” is unknown à Go to “USERS” in the swagger àGET API 		USERS and insert the relevant userID 

 ![image.png](/.attachments/image-5359541d-a398-4bb4-920f-eb92936ea120.png)


 

**Updating department Name** 

**Use case:** After creating a department, you can update its name. 

**Method**: PUT/api/external/departments/{externalId}  

Additional details: Update department name by providing department ID and its new name. 

 ![image.png](/.attachments/image-66689fed-1629-409a-9c12-ab6a4dafc733.png)


 

 

**Deactivate existing department.** 

**Use case**: To make an update for a department from active or inactive to the relevant mode. 

**Method**: PUT/api/external/departments/{externalId}/{active}  

**Additional details:** Activate/Deactivate specified department. 

! If the “departmentID” is unknown à Go to “Departments” àGET API 	 

DEPARTMENTSàmode -all and insert the relevant departmentID 

 
![image.png](/.attachments/image-81a7f6ce-9507-4447-8504-3b6289314757.png)
 


 

**Remove users from single department.** 

   **Use case**: To remove link between many users to one department. 

**Method**: DELETE/api/external/departments/{departmentId}users  

**Additional details**: Remove users from department. 

! To remove the users from the department, DO NOT make deletions! – need to make the 	department INACTIVE for the users. 

 ![image.png](/.attachments/image-c6d47852-0fce-4014-a830-6ed2d2c071f2.png)



  

**Remove a user from department.** 

   **Use case**: To remove link between user to department. 

**Method**: DELETE/api/external/departments/{departmentId}users/{userId} 

**Additional details**: Remove specific user from specific department. 

! To remove the user from the department, DO NOT make deletions! – need 	to make the department INACTIVE for the user. 

 
![image.png](/.attachments/image-57b4b6fc-c6c3-4f95-a8d9-c41bc3f7b4cb.png)
 


 

**Actions** 

 

**See all users that have permission to a specific action.** 

Use case: To get all users of a single action by action ID. 

Method: GET/api/external/actions/{actionId}/users  

Additional details: Get all users by action ID. 

 ![image.png](/.attachments/image-de0021f7-46c9-4b80-8f13-648ede47e8d1.png)


 

**Add Several users to specific Action.** 

**Use case**: To add multi users to a single action. 

**Method**: POST/api/external/actions/{actionId}/users Add users for specified action (list can include users which already have this action) 

**Additional details**:  

! If the “userID” is unknown à Go to “USERS” in the swagger àGET API USERS  

and insert the relevant userID 

! If the “actionID” is unknown à Go to “ACTIONS” in the swagger àGET API 	ACTIONS and insert the relevant action ID 

 ![image.png](/.attachments/image-86ece48e-cd27-4856-9a10-de1b3bbe3eeb.png)


 

**Remove a single action to list of users.** 

**Use case:** To remove but not delete a single action to a list of users. 

**Method**: DELETE/api/external/actions/{actionId}/users 

**Additional details**: See difference between single action to list of actions. 

! To remove an action DO NOT make deletion – make the action INACTIVE. 

 ![image.png](/.attachments/image-3fdcab66-3ea5-410b-a9fd-fee335360118.png)


 

**Remove a single action to single user.** 

**Use case**: To remove but not delete a single action to a single user. 

**Method**: DELETE/api/external/actions/{actionId}/user/{userId}  

**Additional details:** See difference between single action to list of actions. 

! To remove an action DO NOT make deletion – make the action INACTIVE 

 ![image.png](/.attachments/image-abbdfffb-591e-4dcb-b65e-4cc63c3609d2.png)

