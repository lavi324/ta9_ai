[[_TOC_]]

#Summary
1. The Net Services of TA9 IntSight system is the central management service.
2. It puts together various central-components of the system, such as: Metadata Service, Reporting service, User Management Service etc.
3. The environment won't be able to perform even a single operation without the Net Services is running properly.

#Troubleshooting

## Out of sort memory
*  Consider increasing server sort buffer size - 
You need to increase the buffer size of data-model mysql repository in the /etc/mysql/my.cnf, set sort_buffer_size to 256K

## Service Problems 
* The service is going down right after it's started - 
  * There might be a license problem. Check the following things:
    * Make sure that a valid license is installed.
    * Make sure the connection string is well configured to the [[Metadata DB]]

## Data Model Plugins Installation
In order to upload an extension plugin dll to the server:
If it is a new plugin - 
1. Add it via the **admin-wpf** or manually add the right rows to: **dataConnectionManager + dataSchema1 + dataSchemaFields1 + datamodelgrouphierarchy1**

Then ( or if it is a new version of existance plugin) -
1. Paste the updated-plugin-dll to the target folder on the server.
2. In case you have a config file - place it on the server on '**C:\Windows\System32**'
3. In case you have another dll like "**common**" or "**utils**" - place it on the folder of the ***.NET Service*** dlls

* In order to activate the changes - 
**RESTART** the **.NET service** of the server.

##Restarting the Services (Only on windows service) from version 2.6
To change the state of a service **(undeploy, deploy or redeploy)** running under the service host do the following:
1. Go to the installation folder of the service e.g. **C:\Program Files\TA9\C#\TA9 Core Services\Services\Reports.Service**
1. There should be a file there that looks like this: _<<SERVICE_NAME>>.service.delpoyed e.g. _Reports.Service.deployed
   * The ".deployed" of the service status file states the status of the service.
1. To change the state of the service simply rename the file by changing its extension to the desired state e.g. ".**deployed**" to ".**undeployed**" 
   * There are 3 states 
       * .**deployed** 
       * .**undeployed**
       * .**redeployed** 
4. ".**redeployed**" will restart the service.
5. After renaming the file you will notice that it will disappear and reappear with the state you picked. 

## External User Management
In order to opporate in external user management mode - i.e using an Active Directory to manage the system's users you should enter the following values to the app.config file of these services (instead of the current values in the appSettings section)
* Authentication.Service - 
This File : Authentication.Service.dll.config     
  
```
<appSettings>
    --sets the UserManagement to work with the External UserManagement dal ActiveDirectory--
    <add key="ExternalUserManagement" value="ActiveDirectory"/>
    --encrypted connection string to the active directory dal in the format (ip,username,password)  - comma seperated--
    <add key="ActiveDirectory" value="H1aNRyPklPU0eA16hh1Lr4NCRenxl+iGtKjvdP7o0NQSEUBTXWNSlfsOTeQaoFxb"/>
  </appSettings>
```

* UserManagement.Service - 
This File : UserManagement.Service.dll.config

```
appSettings>
    --sets the UserManagement to work with the External UserManagement dal ActiveDirectory--
    <add key="ExternalUserManagement" value="ActiveDirectory"/>
    --encrypted connection string to the active directory dal in the format (ip,username,password)  - comma seperated--
    <add key="ActiveDirectory" value="H1aNRyPklPU0eA16hh1Lr4NCRenxl+iGtKjvdP7o0NQSEUBTXWNSlfsOTeQaoFxb"/>
    --sets the sync interval for the userManegment in milliseconds--
    <add key="SyncInterval" value= "600000"/>
    --chooses which UserManegemnt service should perform the syncing prosses--
    <add key="IsExternalUserSyncer" value= "true"/>
    --active directory admin group name--
    <add key="AdminGroupName" value= "CN=TA9Admins,CN=Users,DC=t-a9,DC=org"/>
    --active directory users group name--
    <add key="UserGroupName" value= "CN=TA9Users,CN=Users,DC=t-a9,DC=org"/>

  </appSettings>
```

