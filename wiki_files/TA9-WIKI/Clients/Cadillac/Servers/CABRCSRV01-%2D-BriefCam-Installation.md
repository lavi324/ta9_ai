[[_TOC_]]


## Documentation
[https://bcftpuser:BCreleases01!@bcftp.briefcam.com/release_5.4.1_up3/Documentation.zip]()

## Postgresql
[https://bcftpuser:BCreleases01!@bcftp.briefcam.com/release_5.4.1_up3/18868/Postgresql/BriefCamPostgreSQL_5.4.1.18868.exe]()

## Server
[https://bcftpuser:BCreleases01!@bcftp.briefcam.com/release_5.4.1_up3/18868/Server/BriefCamServer_64bit_5.4.1.18868.exe]()

## WebServices
[https://bcftpuser:BCreleases01!@bcftp.briefcam.com/release_5.4.1_up3/18868/WebServices/BriefCamWebServices_64bit_5.4.1.18868.exe]()

## Open API - BOA

[https://bcftpuser:BCreleases01!@bcftp.briefcam.com/release_5.4.1_up3/18868/BOA/BriefCamOpenAPI_64bit_5.4.1.18868.exe]()

______________________________________

# Prerequisites 
**This guide:** 
BusinessTeam - Documents\Projects\Cadillac\IT\BCBriefCam v5.4.1 Installation Guide.pdf

**Operating system:**

Windows Server 2019


# Graphic Card - Tesla p40
## Driver Download

[https://www.nvidia.com/content/DriverDownload-March2009/confirmation.php?url=/tesla/442.50/442.50-tesla-desktop-winserver-2019-2016-international.exe&lang=us&type=Tesla]()


# PostgreSQL Installation
## Open Firewall port 

open CMD as admin:

```
netsh advfirewall firewall add rule name="TCP DB 5432" dir=in action=allow protocol=TCP localport=5432
netsh advfirewall firewall add rule name="TCP DB 5432" dir=out action=allow protocol=TCP localport=5432
netsh advfirewall firewall add rule name="TCP DB 6379" dir=out action=allow protocol=TCP localport=6379
netsh advfirewall firewall add rule name="TCP DB 6379" dir=in action=allow protocol=TCP localport=6379
netsh advfirewall firewall add rule name="TCP VSServer 1112" dir=in action=allow protocol=TCP localport=1112
netsh advfirewall firewall add rule name="TCP VSServer 1112" dir=out action=allow protocol=TCP localport=1112
netsh advfirewall firewall add rule name="TCP Fetching Service 1113" dir=in action=allow protocol=TCP localport=1113
netsh advfirewall firewall add rule name="TCP Fetching Service 1113" dir=out action=allow protocol=TCP localport=1113
netsh advfirewall firewall add rule name="TCP Notification Server 7080" dir=in action=allow protocol=TCP localport=7080
netsh advfirewall firewall add rule name="TCP Notification Server 7080" dir=out action=allow protocol=TCP localport=7080
netsh advfirewall firewall add rule name="TCP HTTP 8090" dir=in action=allow protocol=TCP localport=8090
netsh advfirewall firewall add rule name="TCP HTTP 8090" dir=out action=allow protocol=TCP localport=8090
netsh advfirewall firewall add rule name="TCP HTTP 4248" dir=in action=allow protocol=TCP localport=4248
netsh advfirewall firewall add rule name="TCP HTTP 4248" dir=out action=allow protocol=TCP localport=4248
netsh advfirewall firewall add rule name="TCP HTTPS 4244" dir=in action=allow protocol=TCP localport=4244
netsh advfirewall firewall add rule name="TCP HTTPS 4244" dir=out action=allow protocol=TCP localport=4244
netsh advfirewall firewall add rule name="TCP HTTPS 443" dir=in action=allow protocol=TCP localport=443
netsh advfirewall firewall add rule name="TCP HTTPS 443" dir=out action=allow protocol=TCP localport=443
netsh advfirewall firewall add rule name="TCP API ports 4242" dir=in action=allow protocol=TCP localport=4242
netsh advfirewall firewall add rule name="TCP API ports 4242" dir=out action=allow protocol=TCP localport=4242
netsh advfirewall firewall add rule name="TCP API ports 4243" dir=in action=allow protocol=TCP localport=4243
netsh advfirewall firewall add rule name="TCP API ports 4243" dir=out action=allow protocol=TCP localport=4243
netsh advfirewall firewall add rule name="TCP Web Services 80" dir=out action=allow protocol=TCP localport=80
netsh advfirewall firewall add rule name="TCP Web Services 80" dir=in action=allow protocol=TCP localport=80

```


