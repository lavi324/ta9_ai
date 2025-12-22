[[_TOC_]]


# Run Configurations
Each _aspnetcore_ microservice can be run on 1 of 3 options (configurations):
1. **Docker** - on a container as defined in `Dockerfile`
1. **IIS** (IISExpress) - on an environment without dockers
1. **Console application** - usually for debugging purposes

Each of the above options is as simple as selecting it from the 'Play' button on VS2019:
![image.png](/.attachments/image-42cc3595-81bc-4478-b194-843ba1f40b4e.png)



# Run on IIS
1. If that's the first time any Albert microservice is running on this IIS machine continue, otherwise, jump to step 2
1.1 Install .NET Core Hosting Bundle here https://dotnet.microsoft.com/download/dotnet-core
1.2 Run (elevated): 
```
net stop was /y
net start w3svc
```
2. Create the IIS site as described here https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/iis/?view=aspnetcore-3.1#create-the-iis-site
2.1 Point the 'physical path' to the where the microservice is located within the `Program Files/TA9`
2.2 Sample site
![image.png](/.attachments/image-8b2a65bb-be79-4954-bb38-3c30156920f9.png)
3. Attention! **a separate site** has to be created for each _microservice_
