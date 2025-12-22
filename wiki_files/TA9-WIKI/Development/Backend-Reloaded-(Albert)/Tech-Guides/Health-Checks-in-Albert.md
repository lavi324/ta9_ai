[[_TOC_]]

# Intro
This tutorial will teach you how to add and configure Health Checks to your microservice with minimum work.


#What is a Health Check?
Health checks are a way in ASP.NET Core for you to check if a app is up and running at all, and to check each and every individual service inside your microservice app.


#Liveness vs Readiness 
Liveness is a way for the app to tell you "I am up and alive". Just that.
Readiness is telling us the app can use its own services and endpoints.

#Add default basic Health Checks

1. Add a reference to "Infra.HealthChecks" and add a using statement in your project.

![image.png](/.attachments/image-2eef0229-da67-44da-a442-9c3c67ae52b2.png)

![image.png](/.attachments/image-b75f2f3c-400a-41d6-a5af-aa56b41c067e.png)

2. Add "services.AddDefaultHealthChecks();" in ConfigureServices in Startup.cs file.

![image.png](/.attachments/image-00cb221d-5065-4e9b-80c5-e82fc721b568.png)

Now you have the basic checks for you service.

#Add And Create Health Check of your own

- You may want to add custom health check for your service, Here are the steps to do it:
1. Create a class in your project (preferably in a different folder) and make sure to inherit from "IHealthCheck" interface. It will require you to implement a method.
2. Add your custom check, may it be a Database context check or any other.
3.  


















