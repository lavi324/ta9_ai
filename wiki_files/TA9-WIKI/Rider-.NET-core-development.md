Currently JetBrains Rider does not support "_**launchSettings.json"**_ for Docker like Visual Studio.

# Steps to run TA9 .NET Core services with Rider on local environment.

1. Create new Dockerfile for example _**Rider.Dockerfile**_ and change ENTRYPOINT to be "dotnet" instead of "./dotnet-entrypoint.sh". _**(I am not sure why, but I only succeeded to properly work with our services after removing it and making it like default Dockerfile)**_.
![image.png](/.attachments/image-d703a804-a41b-45e1-9c9e-21c4678c4f56.png)
2. Create Docker configuration for Rider:

### Build section:

* Give a name to Docker configuration based on which environment you want to connect.
* Choose the previous created _**Rider.Dockerfile**_ for your Build.

### Run section:
* Bind ports: 
Container port will be port that **_exposed in your Dockerfile_**
Host port is the port for your service, usually taken from _**"launchSettings.json"**_
![image.png](/.attachments/image-283b066e-116f-4820-b08d-1c5c39d01301.png)
* Add Environment variables.
![image.png](/.attachments/image-ae43630b-c7a8-4e85-b92f-414eb1636998.png)

### Full example:
![image.png](/.attachments/image-48165e88-e153-4002-b5dc-47277c246771.png)

P.S 
Some times our services won't build in Rider because they need our nugets. 
Parly solution for this **(Some times even _"allowInsecureConnections"_ wont' work and I don't know why)**, to make "Azure-TA9" package inside nuget.config to have insecure connection.
![image.png](/.attachments/image-11afac19-da9a-4347-992d-e91da1c40ebc.png)