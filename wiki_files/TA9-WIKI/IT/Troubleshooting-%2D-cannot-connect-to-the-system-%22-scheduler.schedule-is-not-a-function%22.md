[[_TOC_]]


# Scenarios 

Cannot login to the system (all users), the error message: 
<font color="red">scheduler.schedule is not a function</font>

Solution and steps:
Check in the event viewer for the following log errors:

![image.png](/.attachments/image-ae63834a-7246-4f33-b52a-364e90f5f08f.png)

![image.png](/.attachments/image-931aa450-3127-4d97-b61b-d82c9401df97.png)

![image.png](/.attachments/image-f295945c-23c2-48e1-8a06-87bb678a6495.png)


These errors means we cannot connect to the DC server. 
To change the DC server ip in the configuration:
1. Go to AuthenticationServices and UserManagementService  
2. <add key="ExternalUserManagement" value="ActiveDirectory"/>    
 <add key="ActiveDirectory" value="H1aNRyPklPU0eA16hh1Lr4NCRenxl+iGtKjvdP7o0NQSEUBTXWNSlfsOTeQaoFxb"/>

3. Change the add key to the relevant ip.