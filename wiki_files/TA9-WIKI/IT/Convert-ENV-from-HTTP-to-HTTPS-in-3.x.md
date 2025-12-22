[[_TOC_]]

#Intro
This wiki is a guide on how to apply HTTPS configuration to the IntSight environment if its currently set to HTTP. 

> ** Note & before you start:**
> - Before starting this process, ensure you have a valid certificate for a valid domain.
> - If this new server make sure you have a ".pfx" file with the private key. as seen in the example screenshot below:
 > ![Picture1.png](/.attachments/Picture1-339dbc2a-744d-4ed0-b67a-ed62c16c47a8.png)

> - If you do not have a valid certificate you can create a self-signed one yourself with the manual described in the section below.

#How to create a Self-Signed Certificate

1. Go to the IIS Manager and click the "main" site & Double-click on Server Certificates:
![image.png](/.attachments/image-414bc9ef-75e7-4b8b-9b39-80b4c4873402.png)

2. In the actions pane on the right click on "Create Self-Signed Certificate"
![image.png](/.attachments/image-1e1449b9-05f1-4e06-a66c-85fb67b2afe4.png)

3. In the next window just name your certificate, keep the next dropdown on "Personal" and click **OK**
![image.png](/.attachments/image-8e9feb03-e43a-4735-a838-f9755d4ce149.png)

4. You have a Self-Signed Certificate now

## Exporting the Certificate 
To transfer the certificate file to other servers (App server & wildfly), you can click on your certificate under "server certificates" and click "**Export**" on the Actions pane, select a password (this password will be used upon installing the new certificate, so make sure to remember it).


# IntSight Configurations
## HostName Configurations
If you want to change the HostName that appears in every URL in the system just change the **IP/old HostName** in every URL you are about to edit like the next example:
OLD: http://demo.ta9.com/
NEW: https://intsight.ta9.com/

## MySQL Configurations

1. Update all endpoints from "http://path" to "https://path" in **endpoints_manager** table (sqlite_metadata) 
2. Update all endpoints from "ws://path" to "wss://path" in **endpoints_manager** table (sqlite_metadata)

## Web (IIS) configurations
1. Edit the app.config.js file in "Web\app"
Edit the loginAddress parameter URL from "http://" to "https://"
2. Edit the config.deploy.json file in "Web\NG\assets\config"
Edit the authentication parameter URL from "http://" to "https://"
Edit the appBaseUrl parameter URL from "http://" to "https://"

## Java Services configurations
###3.9.x and above
In 3.9.x you'll need to edit 2 parameters in the JAVA configuration files located in the Folders of the Indexing, Loader & Wildfly services.

1. Open the "Loader" & "Indexing" Services Folders and update **service_2_service.props** file:
- [ ] Update the **authenticationUrl** URL from "http://" to "https://"
- [ ] Update the **validateTokenUrl** URL from "http://" to "https://" 

2. Open the "Wildfly" "Configurations" folder (Wildfly/Configurations) and update:
**service_2_service.props** & **app.properties** files:
- [ ] Update the **authenticationUrl** URL from "http://" to "https://"
- [ ] Update the **validateTokenUrl** URL from "http://" to "https://" 



###Before 3.9.x
Before 3.9.x the configurations of the JAVA services are located within the Service file itself (JAR/WAR). You will need to use dedicated software to open these files (like 7 Zip) to view its content and locate the configuration files (service_2_service.props/app.properties) within the service.

1. Open the "Loader" & "Indexing" Services JAR files and update **service_2_service.props** file:
- [ ] Update the **authenticationUrl** URL from "http://" to "https://"
- [ ] Update the **validateTokenUrl** URL from "http://" to "https://" 

2. Open the "Wildfly" "Deployments" folder and locate the WAR file for each service.
In each file you'll need to Open it using a dedicated software and update the 2 **service_2_service.props** & **app.properties** files:
- [ ] Update the **authenticationUrl** URL from "http://" to "https://"
- [ ] Update the **validateTokenUrl** URL from "http://" to "https://" 

> Note: 
> - app.properties file is under "WEB-INF" folder
> - service_2_service.props is under "WEB-INF\lib\Utils-0.0.1-B30942.jar" 

## Albert Services configurations
1. Edit the appsettings.json file under every service in "Albert.NetCore" folder
Edit the AuthUrl parameter URL from "http://" to "https://"

## Plugins configurations
In Person Dashboard - one configuration file where there is a URL that will probably have to change from normal "http://" to "https://"  
Person dashboard configuration file name:PersonDashboardConfiguration.json
![image.png](/.attachments/image-8a0264ef-d272-4bf5-9ce5-2fcc28c488c7.png)
Telco (Phone Dashboard) also has a configuration file with four URLs that will have to receive the same treatment. - Phone dashboard configuration file name: IsuzuConfiguration.json
![image.png](/.attachments/image-6a7f4d8a-1c56-46c4-831f-9d32ac75b0e3.png)


## Importing Certificates to the application server

1. Copy the certificate to the machine that contains the TA9 application (IIS web server)
2. Open the IIS and go to the main Site 
![Picture2.png](/.attachments/Picture2-f394e437-8bd8-4442-8959-7d8a994eb193.png)
3. Choose the Server Certificate option.
4. Choose Complete Certificate request…
![Picture3.png](/.attachments/Picture3-4aba4e11-420b-4da0-9db1-8c281e206978.png)
 
5. On the wizard menu choose the relevant certificate and choose a name & press "Finish".
After that on the Server Certificate main you will see the new certificate 
![Picture4.png](/.attachments/Picture4-de987cbe-ee2f-4058-9cc2-62033d5e8aaa.png)
 
## Binding configuration
Go to the "TA9" site (in IIS) and choose **"Bindings"** 
![Picture5.png](/.attachments/Picture5-387ea006-dca3-494d-b6a1-1e2cb5166604.png)
 
Now we need to add a new binding for "https"
- Press the **"Add"** button. 
- Choose "HTTPS" on the type and on "SSL certificate" choose the relevant certificate and press **OK**. 
![Picture6.png](/.attachments/Picture6-014e38f8-862c-48ae-a91a-9f6aa8a1a54d.png)
 

## Adding the certificate on WildFly Machine

> **Note:** 
You will need to perform this step only If the WildFly is installed on a different machine, either Windows or Linux. If the WildFly is installed on the same machine as the IIS - this step can be skipped.

Adding the certificate to the JAVA server in Linux can be done using FileZilla, while on Windows it can be done by copying the certificate file directly into the server.


###For Linux: 
1. First, you will need to transfer the certificate file to the server using FileZilla
2. Second, you will need to separate the certificate into public certificate and private key. To change the certificate format of the file from ".pfx" to ".pem" - run these commands:

> **Note:** To run these commands You will need "openssl" command to be installed. If it's not installed, install it using "yum" or other installation commands you may have in your distribution.

```
openssl pkcs12 -in /root/certificate.pfx -clcerts -nokeys -out public_certificate.pem
openssl pkcs12 -in /root/certificate.pfx -nocerts -out private_key.pem
```

3. To make the JAVA work with the certificate - Import the "public_certificate.pem" file you created to the JAVA certificates - using the following command:

`sudo keytool -importcert -keystore %java-path/lib/security/cacerts% -storepass changeit -file public_certificate.pem -alias "rhel-root"`

Java Path On Linux for example:
**java-path**/lib/security/cacerts = full path will look like this:
**/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.372.b07-1.el7_9.x86_64/jre**/lib/security/cacerts


### For Windows: 
1. First, you will need to transfer the certificate file to the server.
2. To make the JAVA work with the certificate - Import the "public_certificate.pfx" file you created to the JAVA certificates - using the following command:
```
keytool -importcert -keystore "java path\lib\security\cacerts" -storepass changeit -file "{certificate path}" -alias "rhel-root"
```
Java Path On Windows for example:
C:\Program Files\Java\jre1.8.0_181\lib\security\cacerts


# Testing and Validation
- Restart the servers the certificates were changed (entire server reset)
- Open the TA9 application web page check its configures as HTTPS and run a sanity test.