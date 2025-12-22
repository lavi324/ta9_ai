[[_TOC_]]
#Check for users in AD
Before you begin you should know what group of users you want to add for the policy, in our case we would use Administrators.

#Connect to the DC
Connect to the relevant DC.
For the regular DC use 10.100.102.58
For Suzuki's DC use 10.100.102.249

#Open Group Policy And Edit
1. Open Group Policy Managment
![image.png](/.attachments/image-dfa951c2-6b90-41a5-9ca1-c6adb416b28d.png)
2. Open the Domains tree to the Default Domain Policy
   Forest:{Domain Name} -> Domains -> {Domain Name} -> Group Domain Policy -> Default Domain Policy
![image.png](/.attachments/image-d63bb160-13ba-4cc2-abf7-3e52b813a19c.png)
3. In the settings tab open Computer Configuration and follow the next tree
   Policies -> Security Settings -> Local Policies/User Rights Assignment
4. Right click Local Policies/User Rights Assignment and click on Edit
![image.png](/.attachments/image-53833ae0-0793-4e88-af01-2f0c8f67b92c.png)
5. Follow the next tree and get into the Debug Programs Policy
Policies -> Windows Settings -> Security Settings -> Local Policies -> User Right Assignment
![image.png](/.attachments/image-acffd25a-b8b2-4310-8bcb-9f8a7a223e8f.png)
6. Find Debug Programs in the Policy list and open Propeties.
![image.png](/.attachments/image-7360c2ee-45f4-4b12-a2cc-a012558910f1.png)
7. And your Group to the policy settings and click ok.
![image.png](/.attachments/image-82723dbb-34ae-481c-bdfd-e03b80cf7619.png)
