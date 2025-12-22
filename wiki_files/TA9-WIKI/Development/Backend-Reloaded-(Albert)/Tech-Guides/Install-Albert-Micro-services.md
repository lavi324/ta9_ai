[[_TOC_]]

# Introduction

“Albert” is the code name for IntSight’s .net core backend​
New backend features will be written on Albert.Services/JAVA​
Existing WCF services will be rewritten/transformed to Albert.Services​
Microservice approach & design​
Small units​
Each microservice is responsible for a closed topic with its own DB (can be treated as some tables as well)​
Modernized tools / approaches / technologies​
Many architecture concepts are inspired by Microsoft’s eShopOnContainers​

# Install Albert micro service on docker (Linux)

## Use Ansible

Copy from Artifactory\Temp\Windowsip\publish to /opt/albert/microservices/savedcriteria:

```
mount -a
cd ~/
sudo mkdir -p /opt/albert/microservices/savedcriteria
sudo chmod 777 -R /opt/albert/
sudo cp -r /mnt/smb/Artifactory/Temp/IPADDRESS/publish/ /opt/albert/microservices/savedcriteria
```

## Run ansible playbook
```
cd /test-playbooks/
ansible-playbook albert-savedcriteria.yaml -l IPADDRESS
```
This command will pull the docker image.

## Update DataBase
SELECT * FROM sqlite_metadata.endpoints_manager;
![image.png](/.attachments/image-8a2d56ce-5da1-4f59-8dcb-a40de43383ab.png)


## Change configuration

Enter to the folder : 

/opt/albert/microservices/savedcriteria

From  appsettings.Development.json

copy: 
```
  },
  "AuthUrl": {
    "auth": "http://10.100.102.24:5080/AuthenticationService"
  }
```
To appsettings.json

paste this and change respectively to your details

```
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "ConnectionStrings": {
    "SavedCriteriaDB": "server=10.100.102.25;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3306;CharSet=utf8"
  },
  "AuthUrl": {
    "auth": "http://10.100.102.24:5080/AuthenticationService"
  }
}
```
**Note**
If you using URL rewrite change it to API instead port number
10.100.102.24/api/AuthenticationService

**Note**
If service includes put or delete method 
need to add next properties to web.config file

![web_conf.png](/.attachments/web_conf-60e0be22-bd7d-422f-802a-dd42f04f3505.png)

# Install Albert micro service on IIS (Windows)
## Place the artifact from folder
\\\10.100.102.13\share\Artifactory\Temp\IPADDRESS\Albert.NetCore

Copy the whole content to IIS server under TA9 folder stracture.


## 1. install ASP.NET Core Runtime 3.1.8 
https://dotnet.microsoft.com/download/dotnet-core/thank-you/runtime-aspnetcore-3.1.8-windows-hosting-bundle-installer

## 2. Open CMD as admin
```
net stop was /y
net start w3svc

## 3. Open Ports:
netsh advfirewall firewall add rule name="TCP Albert-SavedCriteria 8082" dir=in action=allow protocol=TCP localport=8082
netsh advfirewall firewall add rule name="TCP Albert-SavedCriteria 8082" dir=out action=allow protocol=TCP localport=8082

netsh advfirewall firewall add rule name="TCP Albert-ScheduleCriteria 8083" dir=in action=allow protocol=TCP localport=8083
netsh advfirewall firewall add rule name="TCP AlbertScheduleCriteria 8083" dir=out action=allow protocol=TCP localport=8083

netsh advfirewall firewall add rule name="TCP Albert-Schedule 8084" dir=in action=allow protocol=TCP localport=8084
netsh advfirewall firewall add rule name="TCP Albert-Schedule 8084" dir=out action=allow protocol=TCP localport=8084

netsh advfirewall firewall add rule name="TCP Albert-Export 8085" dir=in action=allow protocol=TCP localport=8085
netsh advfirewall firewall add rule name="TCP Albert-Export 8085" dir=out action=allow protocol=TCP localport=8085
```

## 4. Update DataBase
SELECT * FROM sqlite_metadata.endpoints_manager;
![image.png](/.attachments/image-8a2d56ce-5da1-4f59-8dcb-a40de43383ab.png)

## 5. Create a new site in  IIS
```inetmgr```

Create a new site: 

Site Name:
SavedCriteriaMS

Content Directory:
\TA9\SavedCriteriaMS

Binding:
port 8082

Should look like this:
![image.png](/.attachments/image-9e2de011-bf1d-42fa-a5f5-5f16c1f75fdb.png)



## 6. Edit Settings:
From  appsettings.Development.json
copy: 
```
  },
  "AuthUrl": {
    "auth": "http://10.100.102.24:5080/AuthenticationService"
  }
```
to appsettings.json

paste this and change respectively to your details

```
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "ConnectionStrings": {
    "SavedCriteriaDB": "server=10.100.102.25;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3306;CharSet=utf8"
  },
  "AuthUrl": {
    "auth": "http://10.100.102.24:5080/AuthenticationService"
  }
}
```

paste this and change respectively to your details

```
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "ConnectionStrings": {
    "SavedCriteriaDB": "server=10.100.102.25;user id=root; password=mysql!@#$; database=sqlite_metadata;Port=3306;CharSet=utf8"
  },
  "AuthUrl": {
    "auth": "http://10.100.102.24:5080/AuthenticationService"
  }
}
```

## 7. Disable integrated code
![image.png](/.attachments/image-582d973f-7849-40b1-a017-d1d592486bab.png)


## 8. Give Admin permission

![image.png](/.attachments/image-3948a7b5-3269-4f76-ab30-40bba7a0a980.png)

##9. Edit Configuration to make the services always running
Install the Application Initialization Module
<IMG  src="https://i0.wp.com/www.taithienbo.com/wp-content/uploads/screenshots/IIS_Application_Initialization/Screen-Shot-2018-10-06-at-3.07.30-PM-1.png?resize=1570%2C1124&amp;ssl=1"  alt="Install IIS application initialization module"/>

after installing the Role go back to the IIS app and get into the Configuration Editor and follow the next path.
![image.png](/.attachments/image-78b969df-71c9-4296-8838-721111122395.png)

Edit the configuration as followed.
![image.png](/.attachments/image-8db6fc95-5183-481e-a8b6-1ad69f865128.png)

Then configure the app pool. click on the Application Pools -> *The Relevant App* -> Advenced Settings..
and configure as the picture below.
![image.png](/.attachments/image-cd184017-8146-482b-b772-d6257896085b.png)

Then configure the IIS site. go to the app in the site tab -> Advenced Settings..
and configure as the picture below.
![image.png](/.attachments/image-088be822-3eb2-4ef7-be5b-2627dbc87197.png)

##9. Check configuration 

Open Postman

send request:

GET  http://10.100.102.25:8082/api/savedcriteria/2

add Headers:
Token

get the token from chrome when log in to the system.

shouild look like this: 
![image.png](/.attachments/image-e1773bc2-c3f4-4821-bd8d-156502905103.png)

# Apply URL Rewrite
1. Open CMD as Admin:
2. Type the following commands:
   `cd %windir%\system32\inetsrv`
   `appcmd list config "TA9" -section:system.webServer/rewrite/rules -xml > rewriterules.xml`
3. Edit file from this location:
   `c:/windows/system32/inetsrv/rewriterules.xml`

add this to the end of file:

```
		<rule name="Albert-SavedCriteria" patternSyntax="Wildcard" stopProcessing="true">

                <match url="api/SavedCriteria/*" />

                <conditions>

                </conditions>

                <serverVariables>

                </serverVariables>

                <action type="Rewrite" url="http://localhost:8082/api/SavedCriteria{R:1}" />

            </rule>
```


Restore Configuration:
Open CMD as Admin
Type the following commands:
   `cd %windir%\system32\inetsrv`
   `appcmd set config "TA9" -in < rewriterules.xml`

## configure in MySQL

SELECT * FROM sqlite_metadata.endpoints_manager;

![image.png](/.attachments/image-4ebe2176-bdec-4df3-8685-3e9350fdd2ef.png)




















