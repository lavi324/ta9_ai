[[_TOC_]]
https://help.accusoft.com/PrizmDoc/v13.14/HTML/pas-linux-installation.html

#Introduction
Support a multitude of file types with high fidelity and speed with our zero-footprint document viewer and content conversion REST API. The viewer includes an advanced HTML control that allows users to view, search, redact, print, and download documents in many different file formats – from Adobe PDFs and Microsoft Office files to CAD and DICOM – right in their browser. They don’t need to leave your application or install any custom software.
[https://www.accusoft.com/products/prizmdoc-suite/prizmdoc-viewer]()
[\\\10.100.102.13\Share\Installs\PrizmDoc\Client]()
Installation site : https://help.accusoft.com/PrizmDoc/v13.9/HTML/webframe.html#Set_up_a_backend.html
**(The URL above can be diffrent from versions ______^^)**

# Licensing 
Licensed software purchased by TA9.
Licenses in his account of TA9.
[https://my.accusoft.com/Account/LogIn?ReturnUrl=%2f]()
Account Detail:
dor@t-a9.com
Ta123456
The software bonded to the MAC Address.


## Reactivate license

1. Login to the account above
2. Go to products 
3. Look for the latest server and unused server license
similer to this: 
![image.png](/.attachments/image-8c08d822-8a69-4e51-a598-199c6b316e2e.png)

4. go to license > License pool

5. Click Generate Config File
6. Click on Download Access Keys.
7. Copy both files into the server of prizmdoc ( /home/ta9/install/license/ )
### 8. For Linux server with internet access:
`sudo java -jar /usr/share/prizm/plu/plu.jar deploy get /home/ta9/install/license/{The_Config_File*} "{The Relevant Costumer}" {The_Access_Key**}`

restart the service: 
`sudo systemctl restart pccis`

* *- The Config File = the file you got from the Generate Config File.
* **- The Access Key = 
![image.png](/.attachments/image-0935ce3a-5da7-4763-8e31-b66ecb93c0e3.png)

### 8.1 For Linux server without internet access:

`sudo java -jar /usr/share/prizm/plu/plu.jar deploy get /home/ta9/install/license/TA9Devinstall_PZM-DOC13-SVA_Config.txt "TA9Devinstall" 5XX5-8F85-BV8E-85EV-X33H outputUrl`

8.2 this command will generate a link you should take it to this URL :
[https://licensing.accusoft.com/v1/WebDeployUser/WebDeployUser.aspx]()

8.3 put your output: 
Example: `1EXX36HL63BXEY5XRXW3XEWeayq61Z8ldeNloy5JkYND3y313uW63yPbaeqb30kyNbwIGT1TqRkIPeqYNIcYWYcZ3b1K8KWR3FoDURYc`
you will get this from the server.

8.4 download the license and activate the license. 
`java -jar /usr/share/prizm/plu/plu.jar deploy write "Your Solution Name" 2.0.YourLicenseKeyTextFromUSBFlashDrive`

8.5 restart the service: 
`sudo systemctl restart pccis`


____________________________________________________________________________________

# Configure PrizmDoc Client

## Download the product according to your version 
Current version: 13.5

[https://products.accusoft.com/PrizmDoc/13.5/PrizmDocClient-13.5.exe]()

Start installation

configure the server according to the PrizmDoc server while installing.

## Configure the client

open C:\Prizm\pas\pcc.win.yml

write this : 
```
# The port that PAS will listen on
port: 3000

# A secret key we will use to authenticate some requests
secretKey: "mysecretkey"

# PCCIS connection configuration
pccServer.hostName: "yourserver"
pccServer.port: 18681
pccServer.scheme: "http"
pccServer.apiKey: "{ACSAPIKeyIfNecessary}"

# Defines where the logs are stored
logs.path: "..\\logs\\pas"

# Default timeout for the duration of a viewing session
defaults.viewingSessionTimeout: "20m"

# Defines the storage mechanism and settings for all modules
# that need file access.
documents.storage: "filesystem"
documents.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\Documents"
# Add additional document hashes to the session so markup
# created in older web tiers can be loaded.
documents.legacyMode: true

markupXml.storage: "filesystem"
markupXml.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\Markups"
# Load markup created in older web tiers. Requires that documents.legacyMode = true
markupXml.legacyMode: true

markupLayerRecords.storage: "filesystem"
markupLayerRecords.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\MarkupLayerRecords"
# Load markup created in older web tiers. Requires that documents.legacyMode = true
markupLayerRecords.legacyMode: true

formDefinitions.storage: "filesystem"
formDefinitions.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\FormDefinitions"

imageStamps.storage: "filesystem"
imageStamps.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\ImageStamp"
imageStamps.validTypes: ["png", "jpg", "jpeg", "gif"]

viewingPackagesData.storage: "database"
viewingPackagesProcesses.storage: "database"
viewingSessionsData.storage: "database"
viewingSessionsProcessesMetadata.storage: "database"

viewingPackagesArtifactsMetadata.storage: "database"
viewingPackagesArtifacts.storage: "filesystem"
viewingPackagesArtifacts.path: "%ALLUSERSPROFILE%\\Accusoft\\Prizm\\ViewingPackages"

cors.enabled: true
cors.allowedOrigins: [ "http://localhost:8083","http://YOURWEBAPI" ]

# Rerouter configuration
# This is an example of how to create routing rules
#routeHandlers.LegacyCreateSession.url: "http://localhost:60000/myroute"
#routeHandlers.LegacyCreateSession.headers.x-custom-header: value

# Database Configuration

# The type of database
# Microsoft SQL Server or MySQL databases are supported. Examples:
#database.adapter: sqlserver
#database.adapter: mysql

# Connection string to the database
# MySQL example:
#database.connectionString: "mysql://prizm-user:password@prizm-server.database.host:3306/prizmdb"
#
# Microsoft SQL Server examples:
#database.connectionString: "Server=tcp:prizm-server.database.host,1433;Database=prizmdb;User ID=prizm-user;Password=password;Encrypt=True"
#database.connectionString: "mssql://prizm-user:password@prizm-server.database.host:1433/prizmdb?encrypt=true"
```

## Configure Cors
If you have installed the client Pas on linux, you will need to configure cors in the pccis YAML and make sure that the server got DNS configured.

cors.enabled: true
cors.allowedOrigins: [ "http://example.com", "https://example.com" ]

## Configure the database

SELECT * FROM sqlite_metadata.system_config;
![image.png](/.attachments/image-0cd721c0-52f4-4ffb-b96b-b21b300b4a30.png)

SELECT * FROM sqlite_metadata.endpoints_manager;
![image.png](/.attachments/image-0615ac5c-b749-4bf4-8d11-14be5bba2c0d.png)



# Test Configuration

Go to our Application and try to open a document.









