### **Into**
Swagger, also known as OpenAPI, solves the problem of generating useful documentation and help pages for web APIs. It provides benefits such as interactive documentation, client SDK generation, and API discoverability.

### package installation
From the Manage NuGet Packages dialog:

Right-click the project in Solution Explorer > Manage NuGet Packages
Set the Package source to "nuget.org"
Ensure the "Include prerelease" option is enabled
Enter "Swashbuckle.AspNetCore" in the search box
Select the latest "Swashbuckle.AspNetCore" package from the Browse tab and click Install


### Add and configure Swagger middleware

1. Swagger title and version
2. Authenticate in swagger
3. Support summery comments and show them on swagger UI


```
public void ConfigureServices(IServiceCollection services)
{
    services.AddDbContext<TodoContext>(opt =>
        opt.UseInMemoryDatabase("TodoList"));
    services.AddControllers();


    // Register the Swagger generator, defining 1 or more Swagger documents
               services.AddSwaggerGen(swagger =>
             {
                 swagger.SwaggerDoc("v1", new OpenApiInfo { Title = "Saved Criteria API" });

                 // Allow to authenticate in swagger
                 swagger.AddSecurityDefinition("ApiKey",
                     new OpenApiSecurityScheme { Name = "Token",
                                                Type = SecuritySchemeType.ApiKey,
                                                In = ParameterLocation.Header,
                                                Description = "Authenticat via Token"});
                 swagger.AddSecurityRequirement(new OpenApiSecurityRequirement
                 {
                    {
                        new OpenApiSecurityScheme
                        {
                           Reference = new OpenApiReference
                           {
                               Id = "ApiKey",
                               Type = ReferenceType.SecurityScheme
                           }
                        },
                        new List<string>()}
                    });

                 // Set the comments path for the Swagger JSON and UI.**
                 var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
                 var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
                 swagger.IncludeXmlComments(xmlPath);
             });
}

public void Configure(IApplicationBuilder app)
{
    // Enable middleware to serve generated Swagger as a JSON endpoint.
    app.UseSwagger();

    // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
    // specifying the Swagger JSON endpoint.
    app.UseSwagger();
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "Sample service API");
            });

    app.UseRouting();
    app.UseEndpoints(endpoints =>
    {
        endpoints.MapControllers();
    });
}
```

3. to add comments about - functions description / reusult types / etc... 
3.1 add in the startup file the relevant section (...swagger.IncludeXmlComments(xmlPath).....)
3.2 need to add to the .csproj file : 
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
3.3 add to each function "///"
and then fill the relevant data, for example:

/// < summary>
        /// Get specifice saved criteria by saved criteria id
        /// < /summary>
        /// <param name="id">saved criteria id</param>
        /// <returns>saved criteria </returns>
        /// <response code="200"> return all criteria's in the system</response>
        /// <response code="404"> criteria's not found</response>
        /// <response code="400"> exceptions ...</response>
 public async Task<ActionResult<SavedCriteria>> Get(int id) {....

then you will see it on swagger UI - for example: 
![image.png](/.attachments/image-84f759c4-d957-43b8-ba81-00e75937f3ba.png)

for more information : 
https://docs.microsoft.com/en-us/aspnet/core/tutorials/getting-started-with-swashbuckle?view=aspnetcore-3.1&tabs=visual-studio

https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/711/Entity-Service-API-(Swagger)

https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/156/Documentation-Generation-(swagger)

https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/670/How-to-create-a-Swagger-for-a-client