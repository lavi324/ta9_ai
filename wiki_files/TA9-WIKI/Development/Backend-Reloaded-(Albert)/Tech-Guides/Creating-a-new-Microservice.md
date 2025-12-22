[[_TOC_]]

# Intro
When you need to create a new microservice and already performed the [New Microservice Design Steps](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/406/New-Microservice-Design-Steps), please follow this document to make sure you're aligned with _Albert_ services convention

# Developer Guide
1. Create a new ASP.NET Core Web Application
![image.png](/.attachments/image-443831be-db4d-4e95-b320-5e604a296697.png)
1.1 Name the project according to its meaning followed by dot API
1.2 Locate the project under /src/Services
1.3 Choose API template
1.4 Leave 'No Authentication'
1.5 Uncheck 'Configure for HTTPS'
1.6 Check 'Enable Docker Support' (for Linux)
1. Add [Logging](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/417/Logging?anchor=developer-guide) [Required]
1. Add [Authentication](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/410/Using-Legacy-Authentication?anchor=steps) [Required]
1. Add [Swagger](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/445/Swagger?anchor=package-installation) [Required]
1. Add [Auto-Mapping](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/474/Objects-Auto-Mapping?anchor=developer-guide) [Optional]
1. Add [Message Queue](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/472/Message-Queue-Usage?anchor=usage-guide) [Optional]
1. Add [Entity Framework](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/409/Add-Entity-Framework-Core-to-project) [Optional]
1. Add MediatR **(!Missing WIKI)** [Optional]
1. Add FluentValidation **(!Missing WIKI)** [Optional]
1. Rename the auto-created controller and start coding!
1. While developing:
11.1 [Error Handling](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/483/Response-Format-Error-Handling?anchor=error-handling)