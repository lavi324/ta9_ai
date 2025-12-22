# **Introduction**: in our new world Micro Services are separated from each other and from there NuGet's we need sometimes to debug them all together.
For this mission please follow the configuration:

**Upload new fix to a NuGet:**
-make sure all NuGet's are saved in the following path (NuGet source code): C:\Repos\Nugets
-make sure that the *.csproj project file has the following definition:
`<PropertyGroup>  
  <DebugSymbols>true</DebugSymbols>
  <DebugType>embedded</DebugType>
</PropertyGroup>`

u can add to cs file or right click on the project -> properties
![image.png](/.attachments/image-7c4a1f0f-0200-4de0-b401-94230d24d4a8.png)

**Debug NuGet's:**

go to debug -> options:

![image.png](/.attachments/image-76fe8215-55aa-4521-9fe6-e7b72896f279.png)
![image.png](/.attachments/image-00223ff4-5011-41b6-bf08-3dfc58763be7.png)
![image.png](/.attachments/image-4fa42142-3143-47e0-86bd-24aad35ad1fd.png)
![image.png](/.attachments/image-7429b878-12f5-4272-9919-94fe1beef52d.png)
![image.png](/.attachments/image-e21ac8f4-3215-486a-bd2a-bd2d64d559fe.png)
![image.png](/.attachments/image-d850d70a-e6cc-470f-8c06-f12610e184e9.png)
![image.png](/.attachments/image-96c3f813-14f2-4894-a1f1-e02bc62e9311.png)
![image.png](/.attachments/image-045b5c24-11fa-40cd-9e19-1111af5b36e9.png)

*if nothing works do this :
-close all swagger windows, delete images and containers from docker, delete the project and clone it again using git kraken.
open the project in file explorer and delete OBJ and Bin folder :
![image.png](/.attachments/image-30dfcab9-07d8-4d19-ae1c-9c4546dc3fe6.png)

open the local NuGet's folder and delete the Ta9 nugets
![image.png](/.attachments/image-7c8df113-82e9-4d4c-b6df-9eb0d7655b7a.png)