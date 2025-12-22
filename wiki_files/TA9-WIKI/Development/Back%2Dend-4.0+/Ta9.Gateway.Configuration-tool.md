## Configure TA9.Gateway.Configuration:

need to add the service ( need to add service name only in lower case. if u want that the service will apper in the gateway we need to add it to the gateway list)
 

To generate routes for Ocelot for specific Service, we need to add this service swagger to settings.json.
![image.png](/.attachments/image-a42a1794-f513-4143-9163-b1e94bfa0b73.png)
**SwaggerUrls** it is a dictionary of service configurations where key is an **url** to service's swagger and value is an object with **Port** and **Host** ip where it should be mapped.
***
## Example of mapped endpoint:
![image.png](/.attachments/image-a8de987c-9651-4989-a338-b2984a75549e.png)
***
# Generate ocelot.config.json
before configure new api/change in api we need to make sure we generated a new docker file in the relevant service ( right click on the project -> add - > docker support -> Linux).
if u want to add a new service we need to add it to the docker-compose.yml
ex:
![image.png](/.attachments/image-fdfba9c0-b5d7-4f88-90e7-0f77e674953c.png)
1. Run services for which you want to generate ocelot routes.
2. Right click on **TA9.Gateway.Configuration > Debug > Start New Instance**
![image.png](/.attachments/image-357d586b-1ae5-4a61-a24f-63687b93c345.png)
3. Tool will try to retrieve swagger json for each SwaggerUrl and then generate file ocelot.ServiceSwaggerName.json in bin folder.
(right click on TA9.Gateway.Configuration -> open folder in file location -> bin ->Debug ->.net6 -> copy relevent json file :
![image.png](/.attachments/image-975d2b7a-c497-41f9-b19b-37f01c151271.png)
4. Replace files in TA9.Gateway > Configuration folders, Configuration.Development and Configuration.Integration.
please make sure that in Configuration or Configuration.development the host is  "Host": "host.docker.internal"
and in Configuration.Integration "Host": "10.100.102.23" etc'.
![image.png](/.attachments/image-f9f66bc0-d34c-48ed-b9e4-e8c1619c46b7.png)
***
## To generate files for Development and Integration. Generation should be done 2 times or just open every file and change it's hosts.
- **Configuration.Development** folder should be with **host.docker.internal** host.
- **Configuration.Integration** folder should be with **10.100.102.23** host.
![image.png](/.attachments/image-5cc86490-9c20-4b53-8dde-78e2e17bd753.png)

5. Add key for ocelot.SwaggerEndPoints.json file , for example :
![image.png](/.attachments/image-bf4fdc9b-f8df-4201-ae3c-5bce51885d67.png)