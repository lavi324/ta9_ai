**intro**

The swagger is a way to see API functions which the system holds in the closed code and you can use by an outer code. For example: Parsers, Plugins, Insights, PLA, etc.


**Creating the Swagger**

1. In order to create the Swagger you will need to go to Argus repository on Azure.

![image.png](/.attachments/image-bcd2e1db-de82-4a36-b9c0-d18e7841f92d.png)

2. After that you will need to search for Utils.

![image.png](/.attachments/image-7af3f328-26a8-484a-bcad-413968e6f7ba.png)

3. Then you will need to go to SwaggerWcf folder and download it as zip.

![image.png](/.attachments/image-0dbb12ba-399f-4514-9cb1-c138a785e476.png)

4. When you are done with that you will need to go the app server, and place the docs_minisite folder inside the TA9 folder.

5. Once you done that go to the IIS Manager and add and Application inside the TA9 site and put in the following settings:
Alias: docs_minisite
Physical path: docs_minisite folder path where you placed it inside the TA9 folder in step 4.

![image.png](/.attachments/image-11addab3-593c-434b-959d-70ae4eb92f18.png)

6. Next you will need to follow the instructions on 
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/156/Documentation-Generation-(swagger)
to get the right files inside ext-docs folder inside your docs_minisite folder to make sure you got the right files for the version in the environment youre working on.

**For the first step in the wiki you should have Visual Studio installed, For the second step you will need to have the wildfly server ip of the environment you are working on.**

7. Try accessing the Swagger by typing in the next url:
http://XXX/docs_minisite
**XXX stands for the ip/name of the app server** 

![image.png](/.attachments/image-38ca415c-cb3f-436a-a803-c64d57d77118.png)

Ticket 3.9.2
https://dev.azure.com/ta-9/Argus/_workitems/edit/46428