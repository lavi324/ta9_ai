When u want to test a change that u did locally in a NuGet before u upload it to bitbucket u can do it using the following steps :

1.**Create a change** in the relevant NuGet ( download the Nuget using the git Kraken and save it in the following Repo : C:\Repos\Nugets , It's important that all developers will save the nugets in the same location so the compilation path will be the same and we all can to debug nugets later)

2.**Change the Version numbe**r in the csproj file so it will be different from the currant version - like 4.99 ( ad 9 each time u compile)
![image.png](/.attachments/image-7026ecab-7a59-4c4e-b4f4-288e99412045.png)

3.**Pack the nugget** -> right click on the NuGet project and press Pack :
![image.png](/.attachments/image-f0635537-8a16-46ee-9a0b-659fe70d6a72.png)

4** If it's your first time create the following folder and add a nuget source to the folder like this :
C:\OfflineNugets
define a new NuGet source : Project->manage Nuget packages -> settings -> add (+) :
**Name** : OfflineNugets  **Source** : C:\OfflineNugets
![image.png](/.attachments/image-458d0c33-7a42-4281-ad1a-474987ea9e4f.png)

4.**Move the packed file** (right click -> open folder in file explorer -> Bin -> Debug ) to the folder C:\OfflineNugets ( if u dont have yet- create one)
![image.png](/.attachments/image-0e9d44dd-3bbc-4e13-9787-4374bef05c0e.png)
![image.png](/.attachments/image-507720ef-6218-4dc6-956d-628b200713ce.png)

5.Go to the **relevant service and update the NuGet package** using the Nuget source
right click on the service project -> Manage NuGet packages 
![image.png](/.attachments/image-23c96490-aafe-48dd-b97b-7d4df3b16609.png)
![image.png](/.attachments/image-7062152d-6803-4f32-aa12-01c8115862fb.png)

6.dont forget to **change the NuGet version to 4.0** before u upload the change and do PR

****make sure your debugg settings are like this :
![image.png](/.attachments/image-626ae880-ce23-441c-839e-065ed6b1b3d7.png)

***if u want to make sure that the nugget is loaded u can enter Debug->windows->moduls and see if it's loaded :
![image.png](/.attachments/image-84182b2d-099b-438d-9d52-5978d716811a.png)
