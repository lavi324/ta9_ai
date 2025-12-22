During the upgrade from Albert to Argus we created internal libraries- infra that contain logic and middleware component that relevant to the services. After stabilizing the system, It was decided to transfer the infra project to a nugget package in Bitbucket (instead of azure for better CI-CD process).
The following guide contains an information on installing and updating the TA9 NuGet.

![image.png](/.attachments/image-913c509d-dba0-4008-a486-51494c8c5cfd.png)

### **Installation steps** :

1. **Update VS** :

![Picture1.png](/.attachments/Picture1-180bdd2c-ff2f-4c02-a4f8-04a512e009f6.png)

4. **BitBucket- connect and open an account** ( need Devops support- authorization/ Email for a token)

2. **Download GitKraken and create an account** :
(need to add your e-mail account to Ta9 user -ask Gil https://www.gitkraken.com/download
sign up with email)

![Picture2.png](/.attachments/Picture2-40315bad-07ba-46f2-b486-4f0e1b4f4130.png)

![Picture3.png](/.attachments/Picture3-42e42398-f54e-4276-b1bd-d81df13320a1.png)

3. **NuGet's/Services initial download** :

- connect GitKraken to BitBucket account
![Picture9.png](/.attachments/Picture9-94379437-d59f-4390-ab5e-84c5136dd91d.png)
![Picture10.png](/.attachments/Picture10-4f58506b-82c3-4be5-ac8a-9e90d8e8fd64.png)

![Picture4.png](/.attachments/Picture4-17fee547-328b-4a9a-994b-c471b2cea371.png)

** If u don't see nothing in your workspace - make sure u connected to TA9 Ltd organization
   if nit, please ask Gil to connect u.
![image.png](/.attachments/image-84730c67-d8c0-40bc-a9dd-0377d3ae8120.png)

   After u add the organization, press it and add your account to the following groups :
![image.png](/.attachments/image-c9ab0204-310b-4ee9-8a09-c7ffc0e0c86f.png)
 

- Choose .Net
![Picture5.png](/.attachments/Picture5-6628c73c-a2ca-4d17-9765-cfd9eabfdc60.png)

- Choose specific repositories and clone/ fetch or clone all/fetch all
![Picture7.png](/.attachments/Picture7-3235d346-6a68-4acc-b4bf-5a1292165dea.png)

- Download to a local folder (Nugets/Microservices) :
* to see all the microservices in one solution open a new empty solution (TA9-NET-Microservices with the same name from bitbucket) and just add the projects to the solution (right click on the solution ->add -> Existing Project -> chose the csproj file.
![Picture8.png](/.attachments/Picture8-a66c840a-16d6-422f-be61-0dd887e2756a.png)
![Screenshot 2023-05-01 140012.jpg](/.attachments/Screenshot%202023-05-01%20140012-3fe5efc3-9525-45a3-92e5-8c34841b2163.jpg)

*to run the microservices we will need to connect to our NuGet repo and add it to the solutions :
-press right click on the relevant solution -> Manage NuGet Package -> press the setting button (see below) -> press add ( + green ) and enter the following Source : 
Name : Main
Source : https://pkgs.dev.azure.com/ta-9/_packaging/Main/nuget/v3/index.json

*This will be added to all projects 
![image.png](/.attachments/image-c6eb9568-9745-4988-b153-2c25176967dc.png)

### **Changes and Updets in NuGet's :**

* we  will follow the changes in VS Code through Gitcracken.
*Make sure that every time u update the NuGets the version will be 4.0 in the CSPROJ file.
* make sure that the nuget have the following property- this enable debugging on the nuget from the service.
![image (4).png](/.attachments/image%20(4)-768e8a0a-727e-4f5c-a7ea-f1264ca7cea0.png)

1. **Open GitKraken** and make sure that it's config to the folder on your local computer
(u can also open a new branch with Git using VS see after section 4)
2. Press view changes and confirm that's the correct one.
![Picture11.png](/.attachments/Picture11-a97bfd42-a047-4bc8-be51-b1bbcefde119.png)

3. **Open local brunch and enter the changes to Master brunch**- enter a message for the commit and press :
![Picture12.png](/.attachments/Picture12-301b63d6-589a-4f4a-83f0-319eb5696aec.png)

4. **Press commit** :
![Picture13.png](/.attachments/Picture13-a67ff7e5-6cd1-432e-9034-141f398a12ef.png)

4.Git Option on VS :
 make sure u r on the correct repository- with the name of the service/ NuGet - and make sure u r on the correct branch. if u r working on master just make sure u create a new branch and take all the changes to the new branch- it will ask u, and then push the code after commit) 
** u can only see up to 10 Repositories in one solution on VS .
![image.png](/.attachments/image-36e3b3c6-0081-4aa8-8612-ea440c83b420.png)


5.**Open PR in Bitbucket and choose repositories**.
 - Usually the last NuGet we change will appear first.
 - There are 2 pipelines that's available for NuGet package process - **Test** for the version that created locally 
   in our computer and Release - for the version that created in the server.
 - choose the relevant repository for the PR:
![Picture14.png](/.attachments/Picture14-0f65e322-db40-4aa5-a333-f4b8b29dac41.png)

 - Go to Pull request :
![Picture15.png](/.attachments/Picture15-87c85237-a882-40bf-871e-f4d4da714d6b.png)

- choose create pull request :
![Picture16.png](/.attachments/Picture16-0bc73443-3a66-4240-89fd-52934b2c4aae.png)

- a request is created in the background with the changes and the comments we insert 
![Picture17.png](/.attachments/Picture17-4c2d9b55-1595-4233-8203-ddb709519f37.png)

6. **CircleCI**- After PR approval the NuGet will go through an auto process in CircleCI ( that was created by our wonderful Devop's team). In circuleCi we can see if the process succeeded or failed, and the NuGet dependencies. 
https://app.circleci.com/projects/project-dashboard/bitbucket/ta-9/


- Choose Projects to see all our projects and follow the relevant projects- they will go inside our dashboard list:
(be-net..)
![Picture18.png](/.attachments/Picture18-1860d4b8-01b1-434b-be08-9b6de32e428a.png)

- Dashboard - we can see the project we choose, there running status and more. under Workflow we can see the number of the running.
![Picture19.png](/.attachments/Picture19-c803cd8d-4e7c-41c0-80dc-e08a7e3ddd19.png)

- If u press the arrow u can see all the flow process :
![Picture20.png](/.attachments/Picture20-03a9c876-6f7f-496a-8bbd-04789006fd23.png)

- Pressing _dotnet-nuget-build_ will show all the dependencies that were packed :
![Picture21.png](/.attachments/Picture21-2674db19-4dff-4e38-8d4d-153ec3c26265.png).

it's important to see the dependencies :
![Picture22.png](/.attachments/Picture22-eb4c991d-32d2-44af-9b38-019abb42545f.png)

7. **Azure** - u can verify in azure that the NuGet is packed :
https://dev.azure.com/ta-9/Argus/_artifacts/feed/Main
![Picture23.png](/.attachments/Picture23-2cd6f6ed-df49-46af-9681-8604d437a6b4.png)
![image.png](/.attachments/image-9e7df4bc-edf4-4586-b788-0efcce1e1c36.png)


8. **NuGet Hierarchy** - if there is a change in the NuGet hierarchy we will need to synchronize the NuGet's from the button NuGet to the upper one.
 - arrow below means that the upper nugget depends on the lower NuGet and accept all the NuGets that below him.

![Nugets_Diagram_19.11.23.png](/.attachments/Nugets_Diagram_19.11.23-cf16a69f-2fe8-47b2-b76a-0bcb504efd29.png)

- the Synchronize will be through trigger pipeline - we will choose the relevant NuGet and press the relevant brunch ( make sure u r working on the relevant flow test/release )
![Picture25.png](/.attachments/Picture25-1f95e4bf-eba4-4917-9154-4d653ace5043.png)

- choose trigger pipeline :
![Picture26.png](/.attachments/Picture26-e016112e-aad6-4e26-982e-90b6ec57dbfb.png)

-press trigger and wait to see that the NuGet is packed correctly and continue to the next upper NuGet.
![Picture27.png](/.attachments/Picture27-93f16a2a-36f6-4836-9d34-5c284bed829b.png)















