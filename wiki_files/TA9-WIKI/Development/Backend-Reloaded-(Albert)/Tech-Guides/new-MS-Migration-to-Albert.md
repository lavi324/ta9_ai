when we transfer a new service to albert (whether we transfer a service from argus or adapting it to the new architecture) we need to follow this steps :

1. **Middleware and General Response** (data, messages, statuses code) - use Infra.Middleware. add to startup : 
```
  app.UseTaMiddleware();
  app.UseMiddleware<RequestResponseLoggingMiddleware>();
```
2. **Logs**- use Infra.Logging instead of Serilog. this project already contain Serilog and another reference will create a conflict.
3. **Authentication**- use Infra.JwtAuthentcation and add to startup :
```
            #region Authorization
            services.AddJwtAuthentication(Configuration);
            services.AddSingleton<IAuthorizationPolicyProvider, PermissionPolicyProvider>();
            #endregion
```

4.**Error Handling** - Delete all try and catch that only throw an exception. If there's a logic like rollback don't remove.
ex for remove :
![Screenshot 2023-01-25 144613.png](/.attachments/Screenshot%202023-01-25%20144613-a4e16455-072d-43ea-9af9-98c5b2505354.png)

don't remove :
![image.png](/.attachments/image-86975c03-645c-40f1-bba0-5801772e23c9.png)
5. add Vault configuration :
add project reference to Infra.Vault and add the following to startup :
```
#region Configure Vault
builder.Configuration.AddVault(builder.Configuration);
#endregion
```
make sure u have vault settings in app config :
```
  "VaultConnection": {
    "IsActive": true,
    "Address": "http://10.100.102.23:8200",
    "EnginePath": "Production/",
    "Token": "hvs.54ald###$$$$imlL9z" - take current password.
  },
```
6.**HttpClientRequest** should be through dispatcher.
7. **AppSettings**- should be adjust to different env (development, QA, integration and stage). make sure that sensitive info is stored in vault.
8.**swagger**
9. **use context instead of legacy for authentication**
10. **add health cheack** to startup :
add reference to Infra.HealthChecks


**HealthCheck- KeepAlive**
1.add project reference to Infra.HealthCheack
2.Add to project startup :

```
#region Add HealthCheck
builder.Services.AddDefaultHealthCheck(builder.Configuration);
builder.Services.AddDefaultHealthChecks();
#endregion

or

#region Add HealthCheck
services.AddDefaultHealthCheck(Configuration);
services.AddDefaultHealthChecks();
#endregion
```
3.Docker- Delete DockerFile and generate a new docker file (rightclick on a project->add-> Docker support)
4. Run the swagger and make sure that the following controllers are added :
![Screenshot 2023-01-19 144032.png](/.attachments/Screenshot%202023-01-19%20144032-77d5fe00-12a7-4d49-b622-26ec490f9749.png)
