[[_TOC_]]

# Intro
It's planned to build and integrate IdentityServer4 into our Backend Reloaded
Meanwhile, we must restrict access to the new services using the legacy authentication model.
For that, a kind of authentication implementation was built to enable token-validation & request personalization. All implementation is at infra project named Infra.LegacySupport

# Steps
So, every new microservice, must configure the authentication as follows:
1. Add refrence to the mentioned project
1. Add the url of the authentication service on config
![image.png](/.attachments/image-72e9f845-7ec2-4a06-ab53-9bc7c56dc9a9.png)
1. Configure the authentication as follows on service's bootstrap (ie - `Startup.cs / ConfigureServices`)
            
```
services.Configure<AuthUrlConfig>(Configuration.GetSection("AuthUrl"));
services.AddHttpClient<IAuthService, TaAuthService>();
services.AddAuthentication(TaAuthenticationScheme.TaScheme)
        .AddScheme<AuthenticationSchemeOptions, TaLegacyAuthenticationHandler>(TaAuthenticationScheme.TaScheme, o => { });
services.AddHttpClient<IHttpRequest, HttpRequestService>();
```
