[[_TOC_]]


#Intro
BriefCam is a sensor that's doing video-synopsis (shortening long videos to point of interest). BriefCam's product is installed on Windows servers and accessible via web browser:

Client: [http://BRIEFCAM_SERVER/Synopsis]()
Admin: [http://BRIEFCAM_SERVER/admin]()

#BriefCam Configuration into IntSight
BriefCam can be integrated into IntSight in 2 levels:
1. **Basic** - An app is configured on system and a tile is shown (by permission) on 'Apps'. Clicking on the tile will open an iFrame/separate-tab with BriefCam client. 
Do that by:
1.1 Create an app on IntSight admin-studio like the following:
Video Synopsis
http://10.100.120.90/Synopsis/#/review/cases


![image.png](/.attachments/image-431bf028-ea4a-4fe9-8ac5-cb63a6fef657.png)
* Note: Do it only if the app isn't already defined in the system
1.2 Make sure (on `sensors` table) that sensor ID is **5**
# Configure SSO ( Single Sign In )
User configuration:
1. In table sqlite_metadata.usersensors, define the a briefuser for the ta9user.
for example, for intc2admin (userid=68):
![image.png](/.attachments/image-d9cc7f81-3d0a-40fa-8709-3c0789a51d90.png)
** go to the briefcam app and validate you are able to connect with that user and password. 
2. **Advanced** - including API integration - for SSO
2.1 ***THIS CAN BE CONFIGURED ONLY ON TOP OF '**Basic**' CONFIGURATION ***
2.2 Add/Update on '`endpoints_manager`' table:
`BriefCamAPI = 'http://BRIEFCAM_SERVER/BOA/v3'`
2.3 Remote-Desktop to BRIEFCAM_SERVER:
2.3.1 Open IIS
2.3.2 Locate BOA site - If its missing the SSO wont work.
2.3.3 Right click -> Explore to view its content
2.3.4 Edit `Web.config`
2.3.5 Change appSetting '`SSOEndpoint`' to: [<add key="SSOEndpoint" value="http://SYSTEMURL/api/SensorsService/sensorsso"/>    ]()
It should look like this:
![image.png](/.attachments/image-5953e78e-e531-4998-be61-7de64e13278f.png)
**Check if a domain needed in the url
    <add key="SSOEndpoint" value="http://10.100.120.80:6280/SensorsService/sensorsso" />

2.3.6 Restart site on IIS (usually BOA's parent node)
2.3.7 Restart TA Service Host

**If there is still a problem connecting:**
check if the application is working from a different browser - for example edge, if so, continue:
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/466/BriefCam-SSO-no-longer-support-chrome


#Test Settings
1. Add permission to a user for created app (via Admin-Studio -> Users -> Apps)
2. Login with that user
3. Goto Apps & click 'Video Synopsis' tile
4. It should open the BriefCam client and:
4.1 On **Basic** configuration - show login window
4.2 On **Advanced** configuration - show the app already logged-in
