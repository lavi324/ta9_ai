[[_TOC_]]

# Summary
* TA9 Insight main user interface
* Designed for analysts and researchers
* Access to the system's main features and services
* Contains two main folders – Login and app
* Supports multiple browsers, Chrome is the optimal one
* Can be hosted on any server platform, on any web host
* Can be accessed from anywhere

#Troubleshooting
## Login Failed 
* Verify user and password values (case sensitive)
* Verify that the app server is running
* Verify the app server address on "app.ts" configuration file
___________________
## Map skin of data model is not visible
* Verify that two fields are defined with 'Main Longitude' and 'Main Latitude' respectively
* Verify Latitude and Longitude fields are defined as 'Is Display' = true
___________________
## Map is not visible 
* Verify http://<<maps-server-ip>>/osm_tiles/1/1/1.png (the adress is defined in the endpoint-manager table at MySQL DB)
* Verify that the map service on maps local server is running
___________________
## Fail to load\update Entity
* Verify that "WildFly" service on the local server is running
* Verify the 'entitiesServices.war' deployment status at '<wildfly_folder>\standalone\deployments'
___________________
## Fail to load Data Model
* Verify "TA9 Service Host" Service on the local server is running
___________________
## Fail to load\upload files from the file server
* Verify that "TA9 File Server" service on the local server is running
* Verify the file server endpoint on 'endpoint manager' table at MySQL DB
* Verify 'start.bat' configurations by installation document at '<<installation_folder>>\TA9\Utils\File_Server'
___________________
## Wrong language is displayed
* Verify the the language exist in the 'System Localisation' section in the Adצin tool
* Verify the users section in the Admin tool, that this language is set to this user
* Re login to the web client
___________________

## Fail to load woff2 files \ 404 Not found
When running FontAwesome and loading resources from IIS locally and checking out a page loaded in the browser dev tools, you might find that you get a 404 Not found on your page.
* Open IIS Manager and navigate to website level.
* In Features view, double-click MIME Types.
* In the Actions pane, click Add.
* In the Add MIME type dialog box, type ".woff2".
* Type a MIME type: "application/font-woff"
* Click OK.
___________________
## SERVICE_NAME is requested but does not appear in EndPoints list
The Web client is searching for an end point that doesn't exists on sqlite_metadata.`endpoints_manager` table
If the end point should be use then add it to the table. Otherwise it means the web client version isn't synchronize with the server
___________________
## 500 - Internal Server Error
Recreate in IIS ng app in the exec path.
Install Reverse Proxy
https://www.iis.net/downloads/microsoft/url-rewrite
Install URL Rewrite.
https://www.iis.net/downloads/microsoft/application-request-routing
Restart IIS + TA9 Service Host.
Reopen WEB client. 

![image.png](/.attachments/image-c07c4961-23c2-4130-9b18-a0decc0a235f.png)
___________________

## Unable to find the requested .Net Framework Data Provider.
It may not be installed. 
Exception: System.ArgumentException: Unable to find the requested .Net Framework Data Provider.  It may not be installed.

Install MySQL Client on the server. 
___________________

##Map skin in Data Model. When zooming in, the map view is glitched

<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/c5a45209-f298-4d86-9351-87090bed0599?fileName=image.png"  alt="Image"/>
This issue happens when the map tries to present an image that doesn't exist. 

Make sure that all the following images exist:

- DM Image
- Identifiers 
- Images on gis props
- Lookup icons if exists




