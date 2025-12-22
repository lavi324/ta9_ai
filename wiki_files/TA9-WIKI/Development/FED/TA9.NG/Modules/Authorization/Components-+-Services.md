![image.png](/.attachments/image-42704356-0aac-46f3-b656-5f7bab93e39d.png)
# Components
Each component has its own:
1. Template (HTML)
1. Design File (SCSS)
1. Component Code (TS)
1. Test File (spec.ts)

This module has one service file that contains the following public functions:
- getDataForLogin - 
Calls GetDataForLogin api function that returns localizationItems and languageSupported objects that are needed for login.
- login - 
Calls login api function with username and password as a payload.
If success - return a UserContext object and that is stored in local memory for further usage.
Else - returns one of the following:
![image.png](/.attachments/image-86f9bbdb-dd3b-451e-80ec-598d636a7a1f.png)
- login2FactorAuth
Calls login2FactorAuth api function with secureId and token2FA as a payload
If success - return a UserContext object and that is stored in local memory for further usage.
Else - return 460 error code.
- changePassword
Calls UpdatePassword api function with loginName, oldPassword, newPassword as a payload
If success - logging in normally with the new password
Else - update server error message in store and showing it to user.
- logout - 
Calls Logout api function and clearing user data from memory.

