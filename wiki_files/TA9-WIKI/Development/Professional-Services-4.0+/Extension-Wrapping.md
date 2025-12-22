# Introduction
This guide has in-depth explanations on how to wrap an extension code (currently supports parsers and plugins) in a container, over .NET core.

# Steps:
## 1. Create a new project:
- Create a new '**ASP .NET Core Web App**' project
- Name the project '**XPlugin**' or '**XParser**',  where X stands for the logics name (For example '**CallTypePlugin**', '**CNIParser**')
- Framework: **.NET 6.0 (Long-term support)**
- Authenication type: **None**
- Configure for HTTPS: **V**
- Enable Docker: **V**
- Docker OS: **Linux**
- Do not used top-level statements: **X**

## 2. Delete unnecessary files:
Delete '**Pages**' and '**wwwroot**'

## 3. launchSettings.json:
Replace the default '**launchSettings.json**' file within '**Properties**' folder with the following attached file - [launchSettings.json](/.attachments/launchSettings-169a44c1-10e7-4162-a025-2f09ae69c72a.json)

## 4. nuget.config:
- Add the following file to the project - [nuget.txt](/.attachments/nuget-96f71a0d-9b78-4889-9437-ae0c23a3f83f.txt)
- Make sure to change the file extension to '**.config**' before adding to the project.

## 5. Parser/Plugin Logic:
- Create a new folder named either '**Parser**' or '**Plugin**' accordingly
- Add your parser or plugin logic to the folder. Make sure the class name is simply the name of the logic; following the previous examples: '**CallType**' or '**CNI**'. Sometimes, if the plugin or the parser in linked to a broader feature, add it's name as a prefix; for example: '**OsintProfileParser**' 
- From '**TA9-Azure**' (added in step 4), add '**TA9.IntSight.Ext.Wrapper**' nuget

## 6. Extension:
- Create a static class named '**XExtension**' where X is '**Parser**' or '**Plugin**' accordingly to the same folder created on the previous step
- Create an extension method to 'IServiceCollection' type called '**AddX**' where X is '**Parser**' or '**Plugin**' accordingly
- Inside the function use '**IServiceCollection**' '**AddScoped**' method with the parser or plugin interface type, and the logic type. This is .NET core's version of dependency injection. Also add any other types used by the logic, for example:
![image.png](/.attachments/image-0e84f12c-bd83-4903-b93c-f02344eea8ed.png)

## 7. ci.properties:
- Add a **ci.properties** file, containing one line. For example - '**IMAGE_SUBNAME="plugin.calltype"**'
- First octet can be either '**plugin**' or '**parser**' accordingly
- Second octet should be the logic name, for example '**calltype**' or '**cni**'
- Make sure the values after the '**=**' are in lower case.
- Make sure the file actually contains 2 lines, after the first line have a newline symbol '**\r\n**'

## 8. Dockerfile:
- Replace the default 'Dockerfile' with the following file - [Dockerfile.txt](/.attachments/Dockerfile-ab4807fd-1381-4e94-8268-8aa1a9205e59.txt)
- Make sure to remove the file extension '**.txt**' before adding to the project.
- The attached file is a basic dockerfile example of '**CNIParser**'. Simply change all 'CNIParser' text locations to your added logic. 
- In case your logic uses '**ODBC**' functionality, add the following text to the file - [odbc.txt](/.attachments/odbc-fad85dae-4a0f-4f23-9f02-bea218592774.txt)
- Make sure the bulk of text is added after the first 3 lines as shown below:
![odbc.png](/.attachments/odbc-9a6df5f3-95c9-46b0-bfe7-431471f66ace.png)

## 9. odbc.ini (optional):
- If your logic uses '**ODBC**' functionality, add the following file to the project - [odbc.ini.txt](/.attachments/odbc.ini-8f664a54-b82f-4328-9a55-d01d08be2583.txt)
- Make sure to change the file extension to '**.ini**' before adding to the project.
- If you are running the project locally through Docker Desktop, the "odbc.ini" file will be empty because of there is no command in Dockerfile to fill it, and you should navigate to the file from the Docker Desktop console and fill it manually.

## 10. Program:
### Parser:
- Replace the existing '**Program.cs**' with following file: [Program.cs](/.attachments/Program-021e280c-a43e-477a-8274-1699ae790531.cs)
- Add missing references from project
- Add nuget reference '**Microsoft.AspNetCore.Mvc.NewtonsoftJson**' in **version 6.0.16** specifically!
### Plugin:
- Replace the existing '**Program.cs**' with following file: [Program.cs](/.attachments/Program-10417d53-2ede-44c5-ba76-826bb28bb2c5.cs)
- Add missing references from project
### ODBC (optional):
- In case the logic used '**ODBC**' functionality, add the following line to '**Program.cs**':
'**DbProviderFactories.RegisterFactory("System.Data.Odbc", OdbcFactory.Instance);**'
- Add it's reference '**System.Data.Odbc**' in **version 7.0.0** specifically!

## 11. .csproj file:
- Open the **.csproj** file
- Change all TA9 nugets last numbers to *-* so any minor changes in those nugets will be automatically updated. For example: ![image.png](/.attachments/image-eaa10cc0-b6b5-4a38-a8ea-1dfaa26c6517.png)
- While the ta9 packages are determined by " * - * ", you may run into the need to update them. They will not do it by themselves. You should go into nuget package manager and update all the projects who need the new Nuget. Then, csproj files will automatically include numbers of latest version instead of the asterisks. Compile the updated projects, then go on and undo all the csprojs in your git to return to the asterisks format and you shall have no changes to commit (At least in the csproj section of your project)

## 12. Config file (optional):
In case the plugin itself or one of it's dependencies uses a configuration file, add it to the project as well.

## 13. docker-compose.yml:
- Add the following file to the project - [docker-compose.txt](/.attachments/docker-compose-6b6bd4d3-4ff7-4beb-8e5c-75d82d743559.txt)
![image.png](/.attachments/image-a600784a-0612-408c-b9fc-61a8e65f5fee.png)
- Change the first service name to your extension name
- Change the first port to the extension port (usually port above 10k, discuss with DevOps to make sure it's not taken)
- If there are any additional files added to the project (odcb.ini, configuration, etc.) creating a bind in the '**docker-compose.yml**' is required, as shown in the following file - [docker-compose.txt](/.attachments/docker-compose-ab38d863-41f1-40f9-ab59-5ec4c2f6a52c.txt)
- Make sure to also change the file extension to '**.yml**' before adding to the project