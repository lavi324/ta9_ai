**intro** : Once upon a time there was a huge monolith named Albert. It was a big and complicated and it took a lot of time to upload it to Docker. The brave citizens of TA9 decided to divide it into various projects and upload only the relevant microservice. this is how u do it !
for more info about how to install the NuGet's /microservices and registration to bitbucket/GitKraken/Circle ci go to : https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/763/Infrastructure-NuGet's-and-Microservices
for more info about how to enter 23/138 env using mobaXtream : https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/696/Uploading-4.0-To-Integration-ENV-23-138


create pull-request :

-push the relevant branch from git/ or through GitKraken
git Kraken : make sure u on the correct repository -u can create a new branch from here and also create pull request
![image.png](/.attachments/image-5e6a3dca-9334-4ed8-8ea9-7682e0a65ac9.png)
 git : make sure u on the relevant repository ( the name of the MS, create a branch from master , make the changes and push)
![image.png](/.attachments/image-03247fa7-1ad2-4a97-b213-50629757c655.png)

after u push go to bitbucket and search the relevant MS in repositories :
https://bitbucket.org/ta-9/workspace/repositories
![image.png](/.attachments/image-156c8559-3c39-4efc-88c8-b36b8bfd87ad.png)


go to branches- make sure that the build is ok ( in this ex it's not) and create a pull request in actions (***)
![image.png](/.attachments/image-45b1e70e-f156-42b6-98db-e43c7ea45124.png)

go to pull request and u see the request there -after approval go to Circle ci : https://app.circleci.com/projects/project-dashboard/bitbucket/ta-9/
go to projects -> search the relevant project
![image.png](/.attachments/image-0320657b-0c4c-439e-95ff-7380845e6095.png)

see that the build success and now u can see the version number- remember it.
![Screenshot 2023-05-10 172631.jpg](/.attachments/Screenshot%202023-05-10%20172631-184d235e-d70c-43d7-8324-31b0215f13d5.jpg)


**upload new image to portainer :**
go to the relevant Portainer :
 you can connect to Portainer in https://10.100.102.23:9443/  (yes proceed to unsafe site), authenticate with following credentials:
Username : admin
Password : ta9admin!@#$

At this point, you can connect to Portainer in https://10.100.102.138:9443/  (yes proceed to unsafe site), authenticate with following credentials:
Username : admin
Password : adminadmin!@#$

mark the MS and press restart- make sure that the version number is the correct one- if not go to the next step 
![Screenshot 2023-05-10 180354.jpg](/.attachments/Screenshot%202023-05-10%20180354-6f400df2-5bfa-46f1-b7d5-7ade229e8c1c.jpg)

**upload image using MobaXtream :**
* If uploading through Portainer don't work u can upload using Mobaxtream.
go to the following repo : 
`cd /home/ta9/DEV_Albert/NetCore/Albert.Services/src/`

go to the relevant env and update the following file : .env (open it using Notepad)
change the version number of the relevant MS ( in this ex 21)
![image.png](/.attachments/image-b6823078-49e4-4bda-a2c4-655c2268af2d.png)

 and run the following line with the MS name :
`docker compose --env-file .env up datamodelsearch -d`
if u want to upload all services enter the following line :
`docker compose --env-file .env up`
![image.png](/.attachments/image-ccb1b1cc-db80-4e5c-b6d5-0f6a2df54457.png)

go back to the Portainer and make sure that the correct version is updated :
![image.png](/.attachments/image-92ad4002-de50-421c-8348-15f6e5dce81b.png)