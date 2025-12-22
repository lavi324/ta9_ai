## Steps

1. First you will need to create the build of the latest version of VMS Service.
2. Make sure appsettings.json is configured right for your environment (ips, username and password).
3. Make a copy of the VMS directory that is currently running, in case the new service will not work properly as expected.
On production environment the path is: D:\TA9\NetCore\VMS
On staging environment the path is: D:\TA9\Albert Services\VMS
4. Make sure you have all approvals to begin the update.
5. Stop the VMS site and VMS Application pool in IIS manager.
6. Delete all content of the VMS directory except of web.config file.
7. Delete web.config file from the build directory you just made.
8. Copy all content of latest VMS build directory you just made.
9. Paste inside the VMS directory in the server.
10. Start the VMS site and VMS Application pool in IIS manager.
