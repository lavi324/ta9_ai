1. **How to Connect with Passbolt**
go to 10.100.102.199 
sign in with personal username and password 
The username is work email (name.lastname@t-a9.com) 
The access to Passbolt can be from the office or using TA9 VPN.




2. **Password handling**
All passwords should be saved according to the following guidelines:
_Resource Name:_
{clientName}-Environment#-App/Server- descriptive Name
_Example:_
Isuzu-52-app-Ta9 Admin (App credentials for Ta9 Admin user on a local dev environment)
Isuzu-52-Server-Service Host Windows (login credentials for the service host windows machine)


3. **Group Management**
LocalEnv - Contain only Dev environments passwords
ClientName+Prod - All production passwords for the dedicated project
ClientName+Stg - All Staging passwords for the dedicated project

**Note!:** When Assigning a password to a group - be sure to make the group as "Owner"


4. **VPN Group**
Contain passwords of VPN Accounts according to the following guidelines:
_Resource Name:_
{clientName}-EmployeeName
_Example:_
Bugatti-Oren Lugashi


**Note!:** Be sure to add IP's, and comments to passwords tp provide more description to each saved password
