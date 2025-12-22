[[_TOC_]]

## Intro
This feature evolves another aspect of permissions to a user - ROLE.
A role affects the Admin Studio (see next) & login to analyst console (web client).

## Management
Each user has a role and it can be managed from within the Admin Studio:
![image.png](/.attachments/image-50f7ea93-6d1e-40eb-9834-0f460de9cb96.png =400x500)

## Role Definition
A ROLE is combined of the following:
* IsAdmin - Allows login to the Admin Studio
* IsAnalyst - Allows login to the Analyst web-client
* Tiles to show (relevant only if Admin) - which tiles the role has permission to
* User management actions (relevant only if Admin) - view/update of user's:  
  1. User Details
  1. Departments
  1. Apps
  1. Actions
  1. Data-models
  1. Cases
  1. Dashboards
* Actions (only as template) - template of system actions with yes/no permission
  * Remark: When assigning a ROLE for a user, the ROLE's Actions template is applied to the user, however, these permissions can be changed by an admin as well (so, it can be that a user has Actions-permission which are different from its ROLE)

Roles design document: 
https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/Shared%20Documents/Projects/Suzuki/Project-External/Client%20Design/Custom%20Permission%20Roles%20Design%20v1.docx?d=w3854c1ff3b884da687a20a2ee8bb1c38&csf=1&web=1&e=GnRDos

## ROLES Management:
ROLES are currently defined in a config value, in the 'system_config' table in the DB, named 'PermissionRoles' that belongs to Net_UserManagement module (21).
To change:
1. Extract current value
1. Put it on JSON Editor
1. Make the changes
1. Put result JSON in the same value in the config (minified)
1. Reload Service
![image.png](/.attachments/image-e3c2f818-c95a-4a81-bf45-d056185cd50a.png)

##Update Config:
[New Role Configuration.mov](/.attachments/New%20Role%20Configuration-8adbbd36-ba90-4d2e-a5b5-d43b8245c6db.mov)

## Notes:
* Role is saved for user in Timezone column of users table
* After changing/re-defining roles - make sure to update 'users' table if needed on 
* System users are not constrained to roles when login (i.e - IsSystem=1 allows login everywhere)
* When first installing:
    * Make sure all users in db are assigned with default ROLE 
    * Make sure you assign some users with relevant roles for management (e.g - so you won't get stuck with no option to update ROLE for users as no user has that permission...)