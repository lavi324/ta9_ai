
# Create a new Entity Framework Service
_Based on the great example in [be-net-Service.Situational-Awareness Service](https://bitbucket.org/ta-9/be-net-service.situational-awareness/src/master/)_ 
to create a new service in TA(we will need 

6. **clone new reposfrom GitKraken** (DevOps)
-Create a new repos with the service name -Devops (send Devops the folder name ex: be-net-service.notifications) and 
Make sure that Gil has created a relevant repository in BitBucket before.
clone the repo to Microservices folder- it will open a new folder with the relevant files.
![image.png](/.attachments/image-26c1784b-e300-4009-b7af-dfdf1818186c.png)

## 1. New and empty solution
(create it in the same repos as the other MicroServices)
![image.png](/.attachments/image-70391e33-4ef1-443c-ad8c-caf27a771f7f.png)
![image.png](/.attachments/image-bc7a6796-9de1-449e-969b-d45baab1832a.png)
## 2. Add a new C# ASP.NET core web API project to the Solution
![image.png](/.attachments/image-dc0de307-379e-4ae6-9780-9c9f196cb157.png)
![image.png](/.attachments/image-9d16276f-57dd-44ac-90b8-5b2bc0b728f2.png)
## 3. Updating the project name as other projects names in BitBucket
![image.png](/.attachments/image-f0ad79d9-f540-4431-b2eb-2d2a2d3aa6bf.png)
## 4. Folder structure includes UniTests
- open service folder (TA9-Intsight-NewServiceName) and make sure it has the following:
    **folders** : servicefolder (ex: mapanalysisservice) and test folder (ex : notificationsservice.test), .circleci(with the config file)
    **files** : .dockerignor , .gitignore, Dockerfike, nuget (copy from update service)
* _Make sure the DockerFile is in the main folder and not in the Service Folder, the configuration so the service will run this Dockerfile is in the csproj of the service_
* _Make sure your .gitignore file is updated_
![image.png](/.attachments/image-04a5074d-2787-499a-b9a4-7bbc4d3e0c8e.png)
## 5. Update the config.yml file found in the CircleCi folder 
![image.png](/.attachments/image-b40a5fa6-d07a-4ee6-830b-72a0cc66497b.png)## 

## 7. Add our Nuget package of TA9.Middleware with the latest version
![image.png](/.attachments/image-7c1c6bbd-6f00-48f6-ab2d-46c5c56277d4.png)
## 8. Copy LunchSettings from active service and Try running Swagger (openAPI) on .NET 6
![image.png](/.attachments/image-b06f512a-5163-40ee-a56c-c33ed77d2d8c.png)
![image.png](/.attachments/image-348c59b4-f9fe-4842-9bfe-c1138e65e19b.png)
## 9. Check the readiness & liveness and make sure they return something valid
![image.png](/.attachments/image-cf87e698-4f2b-46f1-86a1-df5984b435db.png)
## 10. Take a Program Template for EntityFramework services 
![image.png](/.attachments/image-a09efb7f-9c87-4e90-ad62-5c64e0839d64.png)

**AddTaInfra**
![image.png](/.attachments/image-66a4bf53-c74c-4fc6-9f23-9245fcce6e03.png)
_addTAInfra function cannot contain DBConnection as well, therefore the connection to the DB should be external to this function in program.cs_

**UseDefaultMiddlewareNew**
_the 'new' is for Entity Framework Services_
![image.png](/.attachments/image-5f0fd24b-8e66-42a9-a3e7-2573926f23ee.png)
**AddCommonServices**
_make sure it's in your project (unless you don't want to use it)_
![image.png](/.attachments/image-57ad4049-0db3-40d0-85e4-59a549786599.png)
Using our UnitOfWork implemented in our Nuget DAL
![image.png](/.attachments/image-35c42b31-71a2-4a1b-a5cc-864bf44df513.png)
## 11. Fixed Folders:
![image.png](/.attachments/image-f281201a-2b6d-4632-93a7-5d14def0297f.png)
>**Service Context**
>>Table connection settings
![image.png](/.attachments/image-2f4c225e-058e-47ca-b286-c7d1fd9a162b.png)
Inheritance from a generic object called ServiceContext from our Nuget DAL
![image.png](/.attachments/image-43cdab65-126d-41de-a6e7-6095349c6fdc.png)
>**Models**
>>The tables themselves
![image.png](/.attachments/image-1705ccc5-2486-4eac-a51a-967353c24fb2.png)
>**Repositories**
>>Working with the tables, CRUD
![image.png](/.attachments/image-b2b45d9d-e8dd-456d-aa25-bcca4f0169d6.png)
Inheritance from a generic object called GenericRepository from our Nuget DAL
![image.png](/.attachments/image-4f65ab50-3ed9-415d-a3e4-47419ff7402e.png)
>**Services**
The implementation and declaration of functions, BL & Interface
![image.png](/.attachments/image-f893a274-d499-4dcb-8474-f119b2d8126b.png)
![image.png](/.attachments/image-6f06296d-92b2-4abc-b55e-59bed8ec7c0f.png)
>**Scripts**
The migrations scripts
![image.png](/.attachments/image-4227c120-1399-469c-ba3d-ed854f9e3b23.png)
## 12. Upload Service to the Deploy New Versions Repo
>Under BitBucket Repository named **_system_installation_** 
![image.png](/.attachments/image-7ac8bdbb-3f80-43a5-a7ac-463d0c967352.png)
stacks => backend => docker-compose.yml file
Upload the new service you added into the **docker-compose.yml** file
![image.png](/.attachments/image-29825a81-a205-4697-b519-d97ebc4a4423.png)
Update the new service you added to the **.env** file
![image.png](/.attachments/image-dd8c22c0-383a-440f-9bb6-7b1070f6b5b6.png)

# Migrations
To create our own migrations using Code First Migration, we will run some commands- 
1. Install dotnet-ef tool
Run `dotnet tool install --global dotnet-ef` using the _Package Manager Console_ 
![image.png](/.attachments/image-a2535306-bf0e-4de6-99dd-776741d9ed1c.png)
![image.png](/.attachments/image-162c3f58-1ce2-4b98-9a41-c10b444d123f.png)
1. Create the first Migration 
Run `dotnet ef migrations add InitialData --verbose` using the Developer PowerShell of the actual Service (--verbose is for detailed logging)
![image.png](/.attachments/image-3efae7e7-5beb-4cd3-bbea-72b45f88819e.png)
![image.png](/.attachments/image-3b021206-fc35-432a-b925-74565a3ffc2e.png)
1. Print the SQL script
`dotnet ef migrations script`
![image.png](/.attachments/image-ee11eede-ea99-4b93-8a27-5d8df4ce59f5.png)
1. Extract the SQL script into a file 
`dotnet ef migrations script -o Scripts\sa_init.sql`
![image.png](/.attachments/image-39551e62-3eb2-4796-9bed-dde3e2f2bf88.png)
_Make sure you put this script in the DevAlbert repository as well, so that it will be included in the next DB deployment_
1. Apply the migration to our database
`dotnet ef database update`
![image.png](/.attachments/image-762718b2-8232-4049-b907-077ce593a12f.png)
1. Delete all migrations we have executed 
`dotnet ef migrations remove`

### **Important:**
- **Vault** is not connected when you run a migration, so make sure the _appSettings_ and _appSettings.Development_ files are as you need
- Both files should be in a JSON correct format
- ConnectionString should include the MariaDB as a Default DB (**only** MariaDB)
- CacheConfig should be filled with valid data

![image.png](/.attachments/image-5afd8c7f-944d-4b8c-b3fd-8490b6b22429.png)
![image.png](/.attachments/image-a366b421-fee4-4040-83d2-97516f9d659d.png)

### Based on: 	
- [Install Entity Framework Core With Empty Template In ASP.NET MVC Core 3.0](https://www.c-sharpcorner.com/article/install-entity-framework-core-with-empty-template-in-asp-net-mvc-core-3-0/)
- [Ways To Run Entity Framework Migrations in ASP.NET Core 6](https://medium.com/geekculture/ways-to-run-entity-framework-migrations-in-asp-net-core-6-37719993ddcb)
- [Migrations Overview by Microsoft](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/?tabs=dotnet-core-cli)

