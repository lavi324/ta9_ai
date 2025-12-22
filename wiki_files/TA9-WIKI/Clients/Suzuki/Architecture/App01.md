What is in the server:
1. .NET Services - D:\TA9\C#\TA9 Core Services
2. Admin - - D:\TA9\C#\TA9 Admin Client
3. Web App & Login - D:\TA9\Web\Web Client
4. Document Viewer - free version - D:\TA9\web\DocumentViewer
5. Camera Accelerator - D:\TA9\web\RequestForVideoApp
6. File Server - Seeweed - D:\TA9\Utils\FileServer
7. File Server Image Store - D:\TA9\ImageStore 
8. Loader Service - D:\TA9\Java\LoaderService
9. Remote Debugger folder - D:\TA9\remote debugger
10. Share Drive

Windows Services:
1. Service Host - runs under P account
2. File Server - runs under P account
3. Loader Service - runs under P account

IIS:
1. Main folder is the web client App
2. Login app
3. Document Viewer
4. RequestForVideoApp

IIS configurations:
1. Url Rewrite - [IIS Reverse proxy](/TA9-WIKI/3rd-Party-Software/Servers/IIS/IIS-Reverse-proxy)

Share Drive (Remote: \\pcanpta9app01\share\TA9, Local: F:\Share\TA9):
1. DB - all the system DB related like licenses, scripts, etc.
2. git - Holds all the code under git\Clients\Suzuki
2.1 ESRI Plugin - connection to egis map layers
2.2 Events Correlator
2.3 Events Post Loading
2.4 Insights - demo usage
2.5 Message Broker Service
2.6 Request for video
3. Installs
4. pics - all pictures used in the system
5. Training

SQL Management Studio:
Access to Data Lake, SQL Management Studio must run with P account

Remarks:
Client Machines have access only to App01 server