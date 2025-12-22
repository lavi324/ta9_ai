## Intro
Platform documentation is using swagger 2.0.
The documentation minisite can be found on `Utils\SwaggerWcf\docs_minisite`  and be run using a standalone server (portable) or can be located on any other web server as the content is static.

## Documentation Generation
The actual documentation files are located under 'ext-docs' folder, and can be re-generated in the following way:
1. C#:
1.1. Go to right branch 
1.2. Compile the ArgusSolution
1.3. Open the solution: [Utils](https://dev.azure.com/ta-9/Argus/_git/Utils)\SwaggerWcf\SwaggerWcf.sln
1.4. For service X:
1.4.1. Change web.config setting 'AssemblyMask' to X
1.4.2. Run the SwaggerWcf.TA9.Service project
1.4.3. Navigate to 'http://localhost:52332/api-docs/swagger.json'
1.4.4. Hit Ctrl+S to save the rendered JSON content
1.4.5. Save it on 'ext-doc' with the right file-name (override)
1.5. Repeat steps of 1.4.x for the following: Reports/UserManagement/MetaData/Authentication
2. JAVA
2.1. On a running WildFly server, for example 10.100.102.24:9900
2.2. Navigate to http://localhost:9900/XXX/swagger.json
2.3. Hit Ctrl+S to save the rendered JSON content
2.4. Save it on 'ext-doc' with the right file-name (override)
2.5. Repeat steps of 2.2-2.4 for the following: TextAnalyticsService/EntitiesServices/FreeTextService

