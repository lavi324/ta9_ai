[[_TOC_]]

#Summary

In order to set up your local environment for debugging we need to install and configure a few things.

#Setting up Argus
- Nothing much to do here, just make sure that Argus is mapped and you are up-to-date in the wanted branch:

![image.png](/.attachments/image-5e85b52c-9eea-422a-859c-8bc99cede7dd.png)

(As you can see Kosta pushed a few changes a millisecond before I took the screenshot)

- Also, Make sure ConnectionsManager.config looks like this:
`<connectionStrings>
  <add name="MetaData" providerName="MySql.Data.MySqlClient" connectionString="DVb+uJg/2+/A60pBMP+aY9ACKIrVf7ImFK26/aajsICmHXLdg048qmKvZVrKNTAtok9X+x8kl+0mOCX4CJWfQW2vh6gGwqhNQdlD0a09gosfkqpaKpweVWziY031lxoZw8YxlNbUdE094ks4zl/hbQ=="/>
  <add name="ServiceAdmin" connectionString="a9qDPL1/+hFWiYoCE4qq7j7xqnu98bvB5RCkITkDnaPpmX3KlG0h2IKHmVpWDJDp"/>
</connectionStrings>`

(Decrypt in the proper tool to know what this means)
((Argus\Net\ArgusSolution\ArgusUtils\Utils\Utils.TESTS))

#Setting up MySql Tables
- Make sure you have MySQL 5.6 and MySQL Workbench installed on your machine.

- Credentials should be as follows:

![image.png](/.attachments/image-52b62b48-de53-4fb3-933d-0d64e585acd0.png)

- Export a known working environment's schemas and tables (`sqlite_metadata`, `ta9_apps` and `ta9data`) then import it to your local client.

- Now you should change most of the connections to localhost, instead the IP of the imported environment:

![image.png](/.attachments/image-1fca60f5-06c2-4e3e-81a3-bc168172ebc4.png)

![image.png](/.attachments/image-e9f2a68c-dab9-44db-bea2-f755d7736d58.png)

- PLEASE NOTE - Not all of the records have been changed to 'localhost' because not all of them should be pointing to localhost if its not needed. You may work on a process that index items from your local Solr and store it in OrientDB that is located at 10.100.102.25 which is totally fine if you don't have a local OrientDB repository. 

#Setting up MySql Drivers

- Few installs are needed here:

[MySQL Connector ODBC](https://dev.mysql.com/downloads/file/?id=491748)
[MySQL Connector for .Net](https://dev.mysql.com/downloads/file/?id=501708)
[Microsoft SQL Server 2012 Native Client](https://www.microsoft.com/en-us/download/details.aspx?id=50402)
[Microsoft ODBC Driver 11 for SQL Server](https://www.microsoft.com/en-us/download/details.aspx?id=36434)

- After installing, Restart your computer, and check if all is present here:
Press Start > Search for ODBC, Run as Admin:

![image.png](/.attachments/image-e3faf673-1d51-472a-a30c-997538c78995.png)

![image.png](/.attachments/image-b3aee1b1-9ee0-41b3-b440-5d55b8ea5bf2.png)

#Setting up web client in IIS
- Copy the 'Web Client' folder from a good working environment. It should be located here `C:\Program Files\TA9\Web\Web Client` or here `D:\TA9\Web\Web Client` and paste it locally here `C:\Program Files\TA9\`

- Go to app folder at `C:\Program Files\TA9\Web Client\app` and edit the `app.config.js` file to look like that:

![image.png](/.attachments/image-c9fbb17f-1bfe-4bea-b6c8-9b8a08ae5d39.png)

- Go to login folder at `C:\Program Files\TA9\Web Client\login` and edit the `app.config.js` file to look like that:

![image.png](/.attachments/image-e9c65392-3bb3-472f-bcb6-a6f483d4884f.png)

- Press Start > IIS (If its not available, Search for "Turn windows features on or off" and enable it in the list)

![image.png](/.attachments/image-7c42b4d9-4b59-459d-a0e7-b46bd67c4378.png)

- Next up, open it and left click Default Web Site and press Advanced Settings, Then copy to physical path the `app` path:

![image.png](/.attachments/image-0ac2e1c0-467b-4f90-a5cd-4812649f974e.png)

- Now right click Default Web Site and press Add Application. Call it `login` and then write on the physical path the login path and press OK:

![image.png](/.attachments/image-a8592e4b-bf3b-494c-b4e9-2f910f60a8cd.png)

- Your web client should be available at `http://localhost/login/#/` after you run Argus properly.

#Setting up Java

- Install jdk-8u261 and jre-8u261 for Windows 64 bit. They are online but they are also here (\\\10.100.102.13\Share\Installs\Java)
- Open the solution in IntelliJ and edit the `parent_pom.xml` to your liking:

![image.png](/.attachments/image-d7d9b904-bf32-4f97-a482-bb88bdfe0e45.png)

- Copy wildfly-10.0.0.Final from \\\10.100.102.13\Share\Installs\Java to your C:\ directory

- Make sure `service_2_service.props` (At Utils > resources) looks like that:

`authenticationUrl=http://localhost:5080/AuthenticationService/LoginEncrypted
validateTokenUrl=http://localhost:5080/AuthenticationService/ValidateUserToken
serviceUser=ServiceAdmin;LCMf4w1EPK1YcfOyvSDdVA==`

- Press on Edit Configurations and choose JAR App and match the details for the Jar you want to debug, in this case its Indexing Service: 

![image.png](/.attachments/image-569f1acd-df8e-4078-802a-a3c376a8d1b2.png)

- Add JBoss Server and match the details:

![image.png](/.attachments/image-9b614f2c-2bfc-4584-bae2-78a2ffdcb20c.png)

- Open Maven tab, Clean and install the TA9JavaServices.

![JAVA-TA9JavaServices.png](/.attachments/JAVA-TA9JavaServices-3f2f22fb-36d6-4e5b-9662-08ebfc1e34a0.png)

- Clean and install Data Contract, then again for Utils and then the other projects you wish to debug. If something does not load properly, Try to use the 'Reload' Icon right under "Maven" name in the picture. It will reload the projects and it should then work.
If it still does not work, close the IDE and run it again.

![image.png](/.attachments/image-352b7cfd-f27f-46cb-bf65-6c581de5754a.png)


If you wish to deploy a service locally, FreeTextService for example, Change the configuration of those files: 
1. **wildfly-10.0.0.Final\standalone\configuration\standalone_xml_history\standalone.xml** to this configuration - [standalone.xml](/.attachments/standalone-115ad29c-9608-4548-8bfa-f0b39b996e01.xml)

2. **wildfly-10.0.0.Final\standalone\configuration\standalone.boot.xml** to this configuration -
 [standalone.boot.xml](/.attachments/standalone.boot-998837a6-e681-4ba4-9326-13b134661f00.xml)

- In the end of the standalone.boot.xml change the path in the deployment section to your services paths.
  for example to instead of 

        <deployment name="FreeTextService-0.0.1-SNAPSHOT.war" runtime-name="FreeTextService-0.0.1-SNAPSHOT.war">
            <fs-archive path="C:\TA9\Argus\Java\FreeTextService\target\FreeTextService-0.0.1-SNAPSHOT.war"/>
        </deployment>

  Change to FreeTextService-0.0.1-SNAPSHOT.war

        <deployment name="FreeTextService-0.0.1-SNAPSHOT.war" runtime-name="FreeTextService-0.0.1-SNAPSHOT.war">
            <fs-archive path="C:\dev\Argus\Java\FreeTextService\target\FreeTextService-0.0.1-SNAPSHOT.war"/>
        </deployment>

![image.png](/.attachments/image-d0d789a0-08bd-4c6c-8cbe-45de881cc1ae.png)


- To be able to download some Artifacts from azure devops, you'll need XMF file with auth. credentials to be placed in:
`C:\Users\<user-name>\.m2`

  File can be found [\\\10.100.102.13\Share\Installs\Java\settings.xml]()

Enjoy!


#Setting up Solr

- Copy solr-6.6.6 folder from our Share at (\\\10.100.102.13\share) and place it in your C:\ directory.
- At solr-6.6.6\server\solr we have the Cores so make sure this is what you need. If not, you can copy it from whatever server you like.

![image.png](/.attachments/image-34a57fbf-d32e-4dad-96ae-56cb71bc79d8.png)

- After that its all a matter of going to the root folder and starting as Admin `_SolR_start.cmd` file 

![image.png](/.attachments/image-2f092d2b-cb50-438c-9905-fb2dcacc5587.png)


Good luck!



