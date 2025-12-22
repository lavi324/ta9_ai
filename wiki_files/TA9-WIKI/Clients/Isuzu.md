[[_TOC_]]

#Introduction

#Troubleshooting
## How to redeploy a single service on WildFly
1. Connect to VPN
1. Remote connect to 10.100.102.90
1. Open FileZilla and connect to Host: 10.100.102.91, User/Password, Port:22
![FileZilla credentials](/.attachments/image-f64da76b-4913-4d6b-bf1f-0b006f917dde.png)
1. Navigate to /opt/application/wildfly
1. Follow [Restart single service](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/48/WildFly?anchor=restart-single-service-(windows-and-linux))

## How to restart WildFly
1. Connect to VPN
1. Remote connect to 10.100.102.90
1. Open putty.exe and connect to Host: 10.100.102.91, User/Password, Port:22
Tip: in case putty isn't open form start menu open it from c:\program files\putty\putty.exe
![putty credentials](/.attachments/image-19f0f556-382d-4349-bd9f-63c90ab200f0.png)
1. Follow [Restart all services / Restart WildFly (Linux)](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/48/WildFly?anchor=restart-all-services-%2F-restart-wildfly-(linux))

##Report isn't being exported in the system
1. Open the Web Client console and check if there are any errors
2. Check the 'generate' method response on network tab
![image.png](/.attachments/image-7a404e48-58ec-4acc-90a1-0ecafd142c71.png)
3. In case 450: 'Unknown error occurred' appears, redeploy 'ReportsGenerationService.war' by following [How to redeploy a single service on WildFly](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/108/ISUZU?anchor=how-to-redeploy-a-single-service-on-wildfly)
4. If the previous step isn't working, restart the entire WildFly service by following [How to restart WildFly](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/108/ISUZU?anchor=how-to-restart-wildfly)