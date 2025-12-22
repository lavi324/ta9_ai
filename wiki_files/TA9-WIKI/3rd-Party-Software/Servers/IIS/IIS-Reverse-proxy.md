[[_TOC_]]

#Introduction
It's possible to use the IIS as a reverse proxy for all the services (and the website). 
In this way: 
1. only the IIS have to be configured with SSL 
1. all the other components can continue to behave normally
1. we may publish only one port (80/443) instead of the many ports our services require

The idea is to unpublish all the services from outside the machine/environment and use only port 80/443 (HTTP/HTTPS) via IIS and let it route each request by the URL template.


#Prerequisites
1. Before we begin to configure IIS, we need to install 2 extensions:
URL Rewrite - https://download.microsoft.com/download/1/2/8/128E2E22-C1B9-44A4-BE2A-5859ED1D4592/rewrite_amd64_en-US.msi
1. Application Request Routing (ARR) - https://go.microsoft.com/fwlink/?LinkID=615136
1. WebSocket support on IIS:
1. Open Server Manager.
1. Under the Manage menu, click Add Roles and Features.
1. Select Role-based or Feature-based Installation, and then click Next.
1. Select the appropriate server, (your local server is selected by default), and then click Next.
1. Expand Web Server (IIS) in the Roles tree, then expand Web Server, and then expand Application Development.
1. Select WebSocket Protocol, and then click Next.
1. Click Install.
1. When the installation completes, click Close to exit the wizard.

#Configure IIS as a Reverse Proxy
1. Open IIS (cmd: inetmgr)
1. Select the main IIS instance
1. Open 'Configuration Editor'
   3.1. navigate to 'system.webServer/proxy'
   3.2. make sure 'enabled' key is set to 'True'
   3.3. set timout to 1.00:00:00
   3.4. if it wasn't so, restart the IIS


#URL Rewrite
#Back up from existing machine:
1. Open CMD as Admin:
2. Type the following commands:
   cd %windir%\system32\inetsrv
   Appcmd.exe
   appcmd list config "TA9" -section:system.webServer/rewrite/rules -xml > rewriterules.xml
3. Take the file from this location:
   c:/windows/system32/inetsrv/rewriterules.xml
4. Put the file in approached place. 

# Restore to another machine:

1. Copy it to the wanted machine to this location:
   c:/windows/system32/inetsrv 
2. Open CMD as admin and run the following command:
   cd %windir%\system32\inetsrv
   Appcmd.exe
   appcmd set config -in < rewriterules.xml
   appcmd set config "TA9" -in < rewriterules.xml

3. After process completes:

3.1 Go to IIS Manager.
3.2 Go to TA9 site.
3.3 Look for URL rewrite section.
3.4 Change the Action URL according to your needs. 


#Old School URL Rewrite:
1. Go to Default Web Site (where the web client application is published)
   4.1. Select Request Filtering
   4.2. From the actions panel press "Edit Feature Settings"
   4.3. Increase the maximum allowed content lenght 
1. On the Features View (on the right side), open 'URL Rewrites'
1. Click 'Add Rule(s)...' 
1. Choose 'Reverse Proxy'
1. Input 'localhost' on the first textbox
1. Click 'OK'
1. Double click the created rule
1. Change 'Using:' to 'Wildcards'
1. In 'Pattern' textbox input 'api/MetaDataService/*'
1. In the 'Rewrite UR:' textbox input 'http://localhost:5280/MetaDataService/{R:1}'
1. Click 'Apply'
1. Repeat steps 4-12 with the following values:
   1. 'api/AuthenticationService/*' --- http://localhost:5080/AuthenticationService/{R:1}
   1. 'api/UserManagementService/*' --- http://localhost:5080/UserManagementService/{R:1}
   1. 'api/TaskManagmentServices/*' --- http://localhost:5080/TaskManagmentServices/{R:1}
   1. 'api/ReportServices/*' --- http://localhost:5080/ReportServices/{R:1}
   1. 'api/GISService/*' --- http://localhost:5080/GISService/{R:1}
   1. 'api/GeoLocationServices/*' --- http://localhost:5080/GeoLocationServices/{R:1}
   1. 'api/WSReportServices*' --- http://localhost:5481/WSReportServices{R:1}
   1. 'api/AppsTwitterService/twitter/ws*' --- http://localhost:9900/AppsTwitterService/twitter/ws{R:1}
   1. 'api/FaceRecognition/fr/DetectionAlertsEndPoint*' --- http://localhost:9900/FaceRecognition/fr/DetectionAlertsEndPoint{R:1}
   1. 'api/EntitiesServices/*' --- http://localhost:9900/EntitiesServices/{R:1}
   1. 'api/TextAnalyticsService/*' --- http://localhost:9900/TextAnalyticsService/{R:1}
   1. 'api/MediaAnalyzingService/*' --- http://localhost:9900/MediaAnalyzingService/{R:1}
   1. 'api/FreeTextService/*' --- http://localhost:9900/FreeTextService/{R:1}
   1. 'api/FaceRecognition/*' --- http://localhost:9900/FaceRecognition/{R:1}
   1. 'api/BlotterService/*' --- http://localhost:9900/BlotterService/{R:1}
   1. 'api/AppsTwitterService/*' --- http://localhost:9900/AppsTwitterService/{R:1}
   1. 'api/Files/*' --- http://localhost:9334/{R:1}
   1. '[1-9],[0-9a-f]{5,15}' --- http://localhost:8800/{R:0} ('''in this entry we must select 'Regular Expression' match''')

#Change endpoints
Now, once all the URL-rewrites are configured well, it's time to change the relevant endpoints in the '''endpoints_manager''' table.
Change according to the list above. For example:
''Authentication'' endpoint
was:        http://10.100.102.18:5080/AuthenticationService/
change to:  http://10.100.102.18/api/AuthenticationService/

Do so for all the endpoints configured above.

#Change WildFly Configuration
Since the WildFly does not have to be published from outside the machine anymore, we need to set the public interface's inet-address to localhost (127.0.0.1).
Do it like this (@standalone.xml):
<pre>
<inet-address value="${jboss.bind.address:127.0.0.1}"/>
</pre>


#Changes required in FileServer configuration
Also here, since all the requests are routed by the IIS, the file-server has to be 'known' only within localhost. 
So, we need to set the 'start.bat' script as follows:

<pre>
START weed.exe master -ip.bind=localhost -port 9334 -mdir="C:/ImageStorage"
weed.exe volume -dir="C:/ImageStorage" -ip=localhost -ip.bind=localhost -port=8800 -mserver=localhost:9334
</pre>
