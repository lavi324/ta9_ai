[[_TOC_]]


# Prerequisite 
## OS Version 
Windows server 2012 and above 

## Install Java
 \\10.100.102.13\Share\Installs\New PC Installs\Java\jdk-8u151-windows-x64.exe

## Configure environment variable

![image.png](/.attachments/image-5d08fd3f-f96c-4d0c-9fe9-9dd77b7833a0.png)


## Edit service_2_service.props section:
![image.png](/.attachments/image-fcda5aae-bfb9-4816-8895-56bdf150b7c5.png)

Example:
```
authenticationUrl=http://10.100.102.80:5080/AuthenticationService/LoginEncrypted
validateTokenUrl=http://10.100.102.80:5080/AuthenticationService/ValidateUserToken
serviceUser=ServiceAdmin;LCMf4w1EPK1YcfOyvSDdVA==
```

## Create the Service

Run CMD as admin

```
cd C:\Program Files\TA9\Loader Service
CreateWinService.cmd
```

A new service will be created named "TA9 Loader Service"

## Change account to run from

![image.png](/.attachments/image-be2c2780-ce36-40a4-927d-3bfc34bb7b82.png)

Restart the service.

Done.

# Change MySQL configuration

SELECT * FROM sqlite_metadata.dataconnectionsmanager;

look for JDBC Connection

should look like this: 

![image.png](/.attachments/image-a46b0646-23be-4d0c-afda-54bb22966b6f.png)

Change the Connection string according to address of mysql

## Define the auto loader


SELECT * FROM sqlite_metadata.data_loader;

DataModelID - get it from : SELECT * FROM sqlite_metadata.dataschema1;


for exemple: 

![image.png](/.attachments/image-2869e117-0e38-4781-a506-0974a6c6d7c9.png)


Make Sure to change LoaderParam
```
{"InvestigationID":"-1","Description":"","FilePath":null,"DataSource":null,"Type":7,"ParserName":null,"DataModelID":-100,"DepartmentID":null,"Latitude":null,"Longitude":null}
```
if you are using parsers replace it accordingly.

# Troubleshoot

see the logs in : 

C:\Program Files\TA9\Loader Service\logs\_today.log


