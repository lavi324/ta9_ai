# Upload New Version

We deploy our service in Docker Stack, stack sits at a higher level than Docker containers and helps to manage the orchestration of multiple containers across several machines. Docker Stack is run across a Docker Swarm, which is essentially a group of machines running the Docker daemon, which are grouped together, essentially pooling resources.
You can learn more about it right [here](https://www.ronaldjamesgroup.com/blog/docker-stack#:~:text=Docker%20Stack%20sits%20at%20a,grouped%20together%2C%20essentially%20pooling%20resources.)

## In order to deploy services:
### 1. Open the **CircleCi** with the `system_installation` Repository 
>https://app.circleci.com/pipelines/bitbucket/ta-9/system_installation
![image.png](/.attachments/image-e97690a1-c56f-4ec0-9d37-ee3f2accb971.png)
We will build a new Image version for this Repo that contains the latest version of each service that exists in the docker-compose file in this repo
By selecting the `Master` branch => execute the `Trigger Pipeline` and wait until it reaches the state of `Success`
![image.png](/.attachments/image-f323f447-103b-4929-b8b9-fdd27f784eee.png)
Then, we will **download** the folder `target/ta9.intsight-4.0.0-17.tar.gz` from the **Artifacts** tab to our computer
![image.png](/.attachments/image-3a579e4c-a79a-427b-b0d7-db3e518e955c.png)
![image.png](/.attachments/image-b8032edb-903c-441f-aa9f-426511ebf500.png)
![image.png](/.attachments/image-d663a341-9a25-41e2-9c8e-e3f353e7262d.png)
_Make sure you DONT open this file in Windows operation system_
### 2. Connect to 23 machine using **MobaXterm**
>In order to do that, you need to use a remote desktop solution, like [MobaXterm](https://mobaxterm.mobatek.net/), for instance. 
After downloading, open the client and right-click on 'User session => New session'
![image.png](/.attachments/image-10a29c1e-3890-43f9-a3fb-df4b17557b25.png)
Choose the SSH tab and enter the following remote host and username
![image.png](/.attachments/image-23dc9e97-2df8-4a7b-8067-cf2eee57f2fa.png)
Then enter the following password in CLI: Tt9!@#$
(u won't see the password in Linux it will look like u not typing- but don't worry my friend - press the password and then enter)
If everything went well, you are supposed to see this - 
![image.png](/.attachments/image-a0cd0c64-cb19-4cdd-a1e4-deaa6998b633.png)
### 3. Replace the new folder with the old one 
> Upload the _tar.gz_ file into the folder `/root/Documents/swarm/`
![image.png](/.attachments/image-6ab449bb-f222-4763-b0a2-1846de70fd21.png)
Move older folder _stacks_ and older file _ta9.intsight-4.0.0-17.tar.gz_ into the _backup_ folder using
>- `mv stacks backup`
>- `mv ta9.intsight-4.0.0-17.tar.gz backup`
**Extract** the new _tar.gz_ folder files using `tar -xvf ta9.intsight-4.0.0-18.tar.gz -C /root/Documents/swarm/`
_Make sure you change the file name according to the relevant image version_
A new _stacks_ folder should appear containing this:
![image.png](/.attachments/image-02ba29a6-5f88-4403-9b50-24e63da20440.png)
>>All extracted files from the tar.gz file are:
![image.png](/.attachments/image-f81934f5-2f84-42cf-bb57-5a69872ee940.png) 
In this folder, there are also Config files such as Secrets (Vault Token and address), Keys (SSL), and Properties which are relevant to a specific Environment ONLY. Therefore, If you want to upload to any Env other than 23, you should copy-paste all values from the already existing files into the newly extracted files.
![image.png](/.attachments/image-be744538-32a8-4fee-802c-3865bea2ef59.png)
Every ENV has its own environment variables, so you need to compare the previous version with the current one
The relevant folders are Web, Java, and Backend.
![image.png](/.attachments/image-cbdd7fdf-e171-49c6-b707-790912313b10.png)
Whenever the folder is empty, you need to copy the files from the previous version (in the Backup folder) and paste them into the current version. For example - 
![image.png](/.attachments/image-dac02ea6-755b-4589-b3e8-d748fa76a5db.png)
### 4. Remove the Backend current version
> Remove the running version of _backend_ stack using `docker stack rm backend`  (do that twice!)
![image.png](/.attachments/image-b70d2d2c-4194-489b-954e-975a985d2292.png)
![image.png](/.attachments/image-a77c3b67-7c92-48d6-b537-0fdca3299e81.png)
_You can also use Portainer to achieve the same goal but it's a bit more complicated_
### 5. Deploy the new version
> Upload both Java and Backend services under the same stack named _backend_ using:
>- `./deploy.sh -f java/ -s backend`
>- `./deploy.sh -f backend`
![image.png](/.attachments/image-0fedb9ae-baf7-4eb6-81ba-272c3c075b88.png)
### 6. Verify the new version is up
> Open the **Portainer** of the relevant Environment and open the _backend_ stack
All services should be **replicated** as in the picture above
![image.png](/.attachments/image-8f53185e-059a-42c6-bf22-ead20b3866d3.png)
In case you have a **problem** you will see this - 
![image.png](/.attachments/image-4393c793-dd32-405f-b1a2-749469fac48d.png)
In this case, the loading and indexing services are not replicated, so there is a problem with their deployment and both services are currently disabled.
### 7. Run Postman tests _SmokeTests_
> In the Repo of _Rest-tests_ in the _BitBucket_ there is a collection of Postman Test which called _Smoke-Tests_
![image.png](/.attachments/image-e982f87a-f5d5-4e0f-9eaf-e8d453b8d089.png)
![image.png](/.attachments/image-84c1634e-6840-4438-981c-5b530d2958f5.png)
Open **Postman**, connect to the Repo (or just create a new collection based on the JSON file you downloaded from the Repo)
Don't forget to **change the Variables** according to your relevant Env and update the Token
![image.png](/.attachments/image-8597277c-51f5-4859-b37b-23cf1cc657a6.png)
**Run** the _Smoke-Tests_
![image.png](/.attachments/image-522a8547-8255-4679-91fe-da4d36e037d8.png)
Make sure all Failed tests are fixed
![image.png](/.attachments/image-389e32f6-2281-40f9-b693-39242ef742e7.png)


#  **AND THAT IS IT!**

____________________________________________
# Old way to upload a new version 

2. Then, upon connecting successfully, run `cd /home/ta9/DEV_Albert/NetCore/` command and perform `git pull`, in order to update the solution.
To authenticate in git, you'll need to generate git credentials:
(make sure that the branch is -main)
https://dev.azure.com/ta-9/Argus/_git/DEV_Albert?path=%2F&version=GBmain&_a=contents


![image.png](/.attachments/image-f5529ee6-8a4c-430d-a86d-28f526f0b564.png)

Navigate to Repos tab in azure and find "Clone" button



![image.png](/.attachments/image-4251d10d-7e70-4dad-8c4b-207b259cabef.png)
Now you can generate git credentials and use password to perform pull command.
copy the password and enter it to the terminal- that's right u wont see the password -press enter)
***If u get an ugly blue screen that tells u that u need to enter commit reason this is VIM screen press `shift+z+q` to exit or `shift+z+z` to save -pressing order is important)
***Undo merge use the command : `Git reset --hard`
*** view merge history : `Git reflog`
## *For 138:
Before build navigate to
**/home/ta9/DEV_Albert/NetCore/Albert.Services/src/Gateway/TA9.Gateway/Configuration.Integration/**
and run `./update_host.sh 10.100.102.138` this [script](https://files.slack.com/files-pri/T0PL1QH8T-F050ESGJGVC/download/update_host.sh?origin_team=T0PL1QH8T) will update Host for each file in this folder.
![image.png](/.attachments/image-ee859288-b745-4298-8b98-bed2a8c1a6aa.png)
* Also in **ocelot.SwaggerEndPoints.json** need to change Url to 138 instead of 23
![image.png](/.attachments/image-83c13f21-ffa5-442e-8c02-26f626e510c7.png)
* Change URL in global.json file
* Change URL of VAULT_ADDRESS to 138 and TOKEN to decrypted version of this string : **MT2/7KtVnJoTM6Si5dU9R0G+PBfwCX1dBr+gDMcow18=** in docker-compose.yml

## Build:

Now, the only thing you need to do, is to navigate to `cd /home/ta9/DEV_Albert/NetCore/Albert.Services/src/` and run the magical `sh build-system.sh -u` command, which was written by our badass DevOps team. It will do all the work for you! 

this script can also do the following commands if u change the ending(-u):
![image.png](/.attachments/image-e0ccb4c7-7721-4db0-9c5e-f1bd83fd3774.png)

wait until it's finished and check the portainer ( if the process is very slow u need to restart the server :

![Screenshot 2023-01-16 174441.png](/.attachments/Screenshot%202023-01-16%20174441-0c8251a8-310e-464e-916e-f40eeba3e5d9.png)


At this point, you can connect to Portainer in https://10.100.102.23:9443/ (yes proceed to unsafe site), authenticate with following credentials:
Username : admin
Password : ta9admin!@#$

At this point, you can connect to Portainer in https://10.100.102.138:9443/ (yes proceed to unsafe site), authenticate with following credentials:
Username : admin
Password : adminadmin!@#$


Proceed to 'Dashboard' tab, and watch your stack up and running!
make sure that the stuck src is up and and all the containers is running 

![image.png](/.attachments/image-bb54955e-33b2-471f-bbef-f2d43bd2bdfa.png)

![Screenshot 2023-01-17 115141.png](/.attachments/Screenshot%202023-01-17%20115141-7b491e3c-6d88-44ab-81bd-a120717b3f49.png)

![Screenshot 2023-01-17 115202.png](/.attachments/Screenshot%202023-01-17%20115202-9e552dc4-babd-4122-b8e1-5c24939256a1.png)

**if one of the containers is not running please check the logs (u have shortcut under the Quick actions).
**if there is a logging error about db/rabbit/redis... please make sure that the relevant container is also running.
**make sure that vault is not sealed 
![image.png](/.attachments/image-002a7bfc-4639-42e1-864c-816a833b34b7.png)
(if it's accept token validation the vault is ok, usually it's sealed after server startup)
if the vault is sealed please enter 3 pin code:
If Vault is sealed decrypt 3 of these passwords and unseal it:
1. pjlK8tD0ipjRPFYuXy29jTeTIzkOgcPhu5prlDPualozCmOeCoVenpPbJoyQLDSi
2. 3CMcIcive/UCXgxtzE94S5EOJi799Xd8kANMay7OOi7D1qV6pUVcLxdeSnQLqrSB
3. y3Un7AEdGGfdJZTRWn8uwMGHqxsPdLIv36wBRcCFIk+Sa2gD8U2eo/Njot+9MqkR
4. 1yph6yeM7/1aIrq1wUK3E+8CY1glHpToBiCRA/o1zL9s2TeOEU4lMUNMDY0ioIDz
5. Vm0h9PXAjs4dZf3jTyBf4msCcs7mfMVGq2ivZPTsQtQrL7C8aBi1f2wC07aHhv0s
(need to decrypt them first)
vault integration URL http://10.100.102.23:8200/ui/vault/auth?redirect_to=%2Fvault%2Fsecrets%2FIntegration%2Flist&with=token 

**Vault 138 :**
 link :
token (encrypt) : MT2/7KtVnJoTM6Si5dU9R0G+PBfwCX1dBr+gDMcow18=
keys (encrypted) :
1. lvUmo+YJVCTLEuvANbv8Nswt1GtEHXGDG5elgxar1QzdxHrlM/2Ewfu0UVoNhEsN
2. HO+IEaAblnCPnOTyBBvqeBlmfz1Q/a1qFJsQqfoUnpTKrCCX5IMZGD92QU2DZcA9



**How to clone Albert_code** :
1. go to the correct folder path /home/ta9/
2. take the path, write git clone + url (make sure u clone the right project from the right branch - main)
3. enter password ( generat git cradential)

![image.png](/.attachments/image-45b4fb03-c02f-415f-a6fb-9031c612f225.png)

![image.png](/.attachments/image-72de166f-43b0-4417-a9c0-6d37f3f5192d.png)

3.make sure the repository created ( if u do mistake, like me, and clone to the wrong path u can use the following dangerous commend : rm -Rf DEV_Albert/ - with great power comes great responsibility).
4. copy the following files to the following folder :
   a.build-system.sh          path : /home/ta9/DEV_Albert/NetCore/Albert.Services/src/
   b.folder openssl           path : /home/ta9/DEV_Albert/

## **Create new Branch from Tag**
During development and integration we want to be able to continue to develop and upload new version, and on the other hand , to be able to provide fix version for troubleshooting.

For development version- keep creating branches from main.

For fix version- we will create a branch from the last stable version from tag.

**Create new Tag :**
first, make sure u downloaded git to your computer ( search git app in computer apps).
if not- please download from the following site :
https://git-scm.com/downloads

1.Create a tag on the relevant version of main 
 u can do it from vs : Git -> manage branches ->New Tag -> enter tag name.

![image.png](/.attachments/image-7cee4506-e9dd-403c-8f6a-9a46d27bc8bb.png)

for example : Integration_09_02_2023
![image.png](/.attachments/image-79145c2d-4385-4ea7-968a-84116fa3de32.png)

2. Open command line from the upper tollbar :
Git -> Open in command Prompt

![Screenshot_20230213_101243.png](/.attachments/Screenshot_20230213_101243-dbbebcb6-0e19-4bdc-8612-fad21b2bb742.png)

Push Tags: Git Changes -> "Push All Tags(--tags) to" -> origin
<IMG  src="https://i.stack.imgur.com/jB11P.png"  alt="enter image description here"/>

3. Enter the following code line to see all tags:
git fetch --all --tags

4. To create new branch from tag enter the following line :

```
git tag -l
git checkout -b "tgName/branche name"

example
git checkout -b Integration_09_02_2023/api_bugs Integration_09_02_2023
```
![Screenshot_20230221_060535.png](/.attachments/Screenshot_20230221_060535-1a5f39c1-38b7-4b8d-a790-2e246ae79ffa.png)

when we upload a new development version we need to merge the branch from tag to main.







