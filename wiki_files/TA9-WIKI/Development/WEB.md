[[_TOC_]]

#Introduction
For anyone who needs to run and access both new and old web applications follow this guide. Here we will see how to install NGINX to and configure it as a proxy redirect server.
- We are doing this in order to have the browser local storage combined for both web applications.

#Install
1. Copy the program binaries from : \\\10.100.102.13\share\Installs\New PC Installs\nginx-1.16.1 or build from repository.
1. launch the executable nginx.exe
       - NGINX is already configured if you want to modify it still use this file: \conf\nginx.conf
1. The redirect server should be up and working
one thing to notice is that to see if the application is running you should check the process tab in Task Manager, it will not who anywhere else.

Configuration example:
![old client - app.config.png](/.attachments/old%20client%20-%20app.config-ad148998-3852-42fa-ba9b-7e4c8aa25715.png)

![old login config.png](/.attachments/old%20login%20config-f0df8455-3078-42df-8ade-1b519149052f.png)

![New app config.png](/.attachments/New%20app%20config-6bef36f2-9292-4ed2-acab-4c81cfd235e4.png)

* Don't forget to serve both applications.
* The old application - gulp serve-dev -> will be accessible throw localhost:4444\
* The new application - ng serve -> will be accessible through localhost:4444\ng 