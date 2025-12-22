[[_TOC_]]

## 1. Pre-requisites needed
- Visual Studio
- .NET 
- Docker
- Docker Desktop app
## 2. Code Editor
Open Visual Studio (2022)
![image.png](/.attachments/image-c8c22f35-6bce-4c99-835c-8a277766b291.png)
## 3. Open a Solution
Create a New and empty solution
![image.png](/.attachments/image-70391e33-4ef1-443c-ad8c-caf27a771f7f.png)
## 4. Create a Project
Add a new C# ASP.NET core web API project to the Solution
![image.png](/.attachments/image-dc0de307-379e-4ae6-9780-9c9f196cb157.png)
![image.png](/.attachments/image-9d16276f-57dd-44ac-90b8-5b2bc0b728f2.png)
## 5. Plugin Business Logic 
### 5.1 IDMPlugin Implementation
Implement the Plugin Interface _IDMPlugin_ 
![image.png](/.attachments/image-3f536bdc-3e59-4cc9-9dc0-c49209949749.png)
### 5.2 ExecuteQuery Example 
Example of the ExecuteQuery method Implementation where you define the results returned from the DM plugin after activating it. 
The Plugin's **Business Logic** is in here! 
```
// Implementation
var results = new List<Dictionary<string, object>>();
DataTable dt = new DataTable();
dt.Columns.Add("Hello");
dt.Columns.Add("World");
DataRow newRow = dt.NewRow();
newRow["Hello"] = "Hello";
newRow["World"] = "World";
dt.Rows.Add(newRow);
results = dt.AsEnumerable().Select(row => dt.Columns.Cast<DataColumn>().ToDictionary(
                                          column => column.ColumnName, //key
                                          column => row[column]        //value
                                          )).ToList();
return results;
```
or       
![image.png](/.attachments/image-ab4c7d75-8bfc-4b8a-9592-b1a3384aa144.png)
### 5.3 GetExtensionDataFields Example
Example of the GetExtensionDataFields method Implementation where you define the Columns of the DM Plugin
![image.png](/.attachments/image-1ffc7547-f61e-4435-a31c-159cf49c7b36.png)
### 5.4 PluginBL File
Eventually, the PluginBL file will look like this -
```
using Plugin.Models;

public class PluginBL : IDMPlugin
{
    private readonly ILogger<PluginBL> _logger;

    public PluginBL(ILogger<PluginBL> logger)
    {
        _logger = logger;
    }

    public async Task<List<Dictionary<string, object>>> ExecuteQuery(DMPluginFilterGroup filters, List<DMPluginFieldSort> sortFields, int pageSize, DMPluginUserContext userData)
    {
        // Business Logic Implementation
        try
        {
            // Create a list of dictionaries
            List<Dictionary<string, object>> results = new List<Dictionary<string, object>>
            {
                // Add dictionaries to the list
                new Dictionary<string, object>
                {
                    { "Key1", 1 },
                    { "Key2", "Hello" },
                },
                new Dictionary<string, object>
                {
                    { "Key1", 2 },
                    { "Key2", "World" },
                }
            };

            return results;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            throw;
        }
    }

    public List<DMPluginField> GetExtensionDataFields()
    {
        List<DMPluginField> fields = new List<DMPluginField>
        {
            new DMPluginField { FieldName = "Key1", DisplayName = "Key1", IsDisplay = true, DataType = DMPluginFieldDataType.Double, IsValid = true, IsQueryable = true },
            new DMPluginField { FieldName = "Key2", DisplayName = "Key2", IsDisplay = true, DataType = DMPluginFieldDataType.Text, IsValid = true, IsQueryable = true, IsFreeTextSearch = true }
        };
        return fields;
    }

    public List<Dictionary<string, object>> GetSampleData() { return null; }
    public List<string> GetFieldDistinctValues(DMPluginField field) { return null; }
    public bool TestConnection(string userName, string password) { return true; }

}
```
## 6. Plugin Controller
### 6.1 Link Business Logic file
Link the Business Logic file above (IDMPlugin interface's implementation) to the controller. 
![image.png](/.attachments/image-3ccbdb8d-b6ed-44e3-b3b8-8eaeba4a9df6.png)
### 6.2 API methods
Add each API method relevant to the Plugin
All methods related to the DMPlugin -  
![image.png](/.attachments/image-2a8476cf-462c-4c63-a989-0ac78107cb2d.png)
Choose the APIs you want to implement based on the Plugin type.
In our case, we chose the APIs:
![image.png](/.attachments/image-72012fe0-f78e-492c-a3bd-74963a7b737e.png)
### 6.3 API implementaion
Every API redirects to the relevant method in the BL file
![image.png](/.attachments/image-5d312d03-933f-422c-85fa-0c10f47f70e0.png)
### 6.4 Plugin Controller File
Eventually, the PluginController file will look like this -
```
using Microsoft.AspNetCore.Mvc;
using Plugin.Models;

[ApiController]
[Route("api/Plugin-service")]
public class PluginController : ControllerBase
{
    private readonly ILogger<PluginController> _logger;
    private readonly IDMPlugin _PluginBL;

    public PluginController(ILogger<PluginController> logger, IDMPlugin PluginBL)
    {
        _logger = logger;
        _PluginBL = PluginBL;
    }

    [HttpPost("execute-complex-Plugin")]
    public async Task<ActionResult<List<Dictionary<string, object>>>> ExecutePlugin(
        [FromBody] ComplexRequest complexRequest)
    {
        try
        {
            if (_PluginBL == null)
                return new List<Dictionary<string, object>>();
            var result = await _PluginBL.ExecuteQuery(complexRequest.Filters, complexRequest.SortFields,
                                                      complexRequest.PageSize, complexRequest.UserData);
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("extension-data-fields")]
    public ActionResult<List<DMPluginField>> GetPluginFields()
    {
        try
        {
            if (_PluginBL == null)
                return new List<DMPluginField>();
            var result = _PluginBL.GetExtensionDataFields();
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, "Internal server error");
        }
    }

    [HttpGet("sample-data")]
    public ActionResult<List<Dictionary<string, object>>> GetSampleData()
    {
        try
        {
            if (_PluginBL == null)
                return new List<Dictionary<string, object>>();
            var result = _PluginBL.GetSampleData();
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, "Internal server error");
        }
    }
}
```
## 7. Link Business Logic file
Add Extensions to the Program file Using Dependency Injection 
![image.png](/.attachments/image-d6204e5b-ce06-409d-8e08-04ceebffe383.png)
## 8. Create Dockerfile
Add Dockerfile to the project
![image.png](/.attachments/image-62a3cb14-f7a1-49d1-877a-dd9bcb0a73a1.png)
![image.png](/.attachments/image-432d188c-b984-4ecd-b1e4-9873b95d20c5.png)
### 8.1 Automated Dockerfile
Dockerfile generated automatically as in this file -
```
#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["plugin/plugin.csproj", "plugin/"]
RUN dotnet restore "./plugin/./plugin.csproj"
COPY . .
WORKDIR "/src/plugin"
RUN dotnet build "./plugin.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./plugin.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "plugin.dll"]
```
### 8.2 Dockerfile Changes
You might need to make some changes in the file due to different routing, such as - 
- _line 11:_ change it into `COPY ["plugin.csproj", "."]` _(instead of `COPY ["plugin/plugin.csproj", "plugin/"]`)_
- _line 12:_ change it into `RUN dotnet restore "./plugin.csproj"` _(instead of `RUN dotnet restore "./plugin/./plugin.csproj"`)_
- _line 14:_ change it into `WORKDIR "/src"` _(instead of `WORKDIR "/src/plugin"`)_
## 9. Launch Settings File
Add _Docker_ environment to launch settings to determine the plugin's port so you will be able to run it using Docker in your specific port
```
"Docker": {
  "commandName": "Docker",
  "launchBrowser": true,
  "launchUrl": "http://{ServiceHost}:{ServicePort}/swagger",
  "publishAllPorts": true,
  "httpPort": {ServicePort},
  "useSSL": false
}
```
For example -
![image.png](/.attachments/image-20dc70c7-5b6b-461c-bc19-a096274bdc0c.png)

## 10. Final Project outlook 
The Solution will look like this after removing the default unnecessary files created automatically - 
![image.png](/.attachments/image-9bf888c6-960b-4b6d-a97b-667fb84be419.png)
## 11. Test the solution
- Test your controller and run it using the Docker environment
![image.png](/.attachments/image-60bd2959-1391-4f01-8772-5199c6a402b0.png)
- The swagger should open - 
![image.png](/.attachments/image-aaffd96b-1b3b-4b03-84b4-03361871b837.png)
- Test any API method implemented such as - 
![image.png](/.attachments/image-f231d575-e315-4e55-85a8-ecb5a0bec2d0.png)
- And verify the expected result -
![image.png](/.attachments/image-9da91556-85de-4ea7-9234-b3124bd09c66.png)
## 12. Build an Image
Once we are done with the project and we have a working solution in .NET using Visual Studio 
we need to run this project as an image using the _docker build_ command -
`docker build -f <dockerfile> -t <image_name>`
For example - 
`docker build -f Dockerfile -t ta9.testplugin .` 
 
_Make sure you run this command from the same location where the solution's Dockerfile is located_

![image.png](/.attachments/image-25412bcf-ebfa-4a20-affa-b0a9b612ad5d.png)

Then, we can notice in the _Docker Desktop_ app that this Image was created
![image.png](/.attachments/image-4b6c8246-a3d5-4c92-8c23-76c54d785320.png)
## 13. Run the Container
After we create the Image, we can run this image in a container using the _docker run_ command
`docker run -p <out_port>:<in_port> --name <container_name> -d <image_name>`
For example - 
`docker run -p 5555:80 --name testplugin -d ta9.testplugin` 

![image.png](/.attachments/image-5c40efa5-289d-4bcf-8dff-5db682b08efa.png)

Then, we can notice in the _Docker Desktop_ app that this container is running!
![image.png](/.attachments/image-28408ddf-191d-421d-8025-4acc286ca72c.png)

Verify the service is up by opening the Swagger in the same port
`http://<environemnt_ip>:<plugin_port>/swagger/index.html`
For example - 
`http://10.100.103.67:5555/swagger/index.html`

![image.png](/.attachments/image-d0292ff2-bcbb-4391-9a82-884c0b3b2759.png)
## 15. Plugin Registration to TA9 
Using Admin Studio
![image.png](/.attachments/image-d11dcb69-1e8c-4158-a660-14ea621e9a06.png)
![image.png](/.attachments/image-67f60492-9956-4f92-b724-543c3e2dbc38.png)
* The endpoint should indicate the REST server URL which the plugin runs on
`http://<environemnt_ip>:<plugin_port>/api/plugin-service`
For Example -
`http://10.100.103.67:5555/api/plugin-service`
* Verify the service is up and running using the Test Connection Button
![image.png](/.attachments/image-bd5d9d31-b280-4b7f-b0f6-8f1ca9c954d1.png)
* After clicking the `OK` button, the DM Plugin is opened
![image.png](/.attachments/image-6c99acf4-618d-4ff4-b9a1-618534a6b2a5.png)
* After any change you want to make, click the `Save` button
![image.png](/.attachments/image-7ed9e89d-3ecc-46ad-92e3-10c74679a639.png)
* Now you finally have a working plugin connected to the TA9 system!
![image.png](/.attachments/image-c4322951-8eae-4369-9f96-061dec1a7e9e.png)
## 16. API KEY secret
It depends on Vault's configuration whether the API key is necessary or not
under _SystemConfiguration_ => _PluginGatewayApiKeyCheck_ (Boolean)
![image.png](/.attachments/image-a740e5ed-28b3-4478-8cdd-8c469a855f6f.png)

Only in case it is _TRUE_, follow the steps: 
- Create a secret file that will store the API key for this specific Plugin 
- Upload it to the container
- Make sure it has a valid key without any `\n`
- Run the service again

The API key in the secret file is the same as displayed in the Admin Studio (extracted from the _Insights_ table under the _ApiKey_ tab) -
![image.png](/.attachments/image-4acd08f2-b685-45cd-8ad3-40c172a71d52.png)

Eventually, it will be as here -
![image.png](/.attachments/image-637f0834-b629-46de-8b62-7d1117a9e9c4.png)

# Summary
To sum up, for a plugin to run as a part of the TA9 system, you need to follow the steps:
1. Create the Plugin project which consists of a controller and the business logic 
2. Add a docker file to this project
3. Create the Plugin image
4. Run the Plugin as a Service in a container
5. Connect the Plugin Service to the TA9 system using the Admin Studio
6. A new Plugin has been added to the TA9 

::: mermaid
 graph LR;
 A[Plugin Code] --> B[Plugin Controller]--> C[Plugin Business Logic]--> A[Plugin Code]-->
 E[Dockerfile]-->  A[Plugin Code] --> I[Service]
 I[Service] --> F[Plugin Image]--> G[Plugin Container] --> I[Service]
 I[Service] --> H[Admin Studio] --> J[TA9 Plugin];
:::






