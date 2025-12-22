Hi there! Here the guideline of how to push *.*.*-rc version of Middleware nuget to Azure artifacts.
First of all, you need to download and install Ubuntu terminal environment from Microsoft Store.

![image.png](/.attachments/image-81dc1673-70e8-47b0-a023-e5b0095a4112.png)

After installation, run Ubuntu app and follow the instruction to create default user.

First thing that you need to do, is download the latest version of `TA9.Intsight.Infra.Middleware` with `-rc` postfix from Azure Artifacts: 
[https://dev.azure.com/ta-9/Argus/_artifacts/feed/Main](https://dev.azure.com/ta-9/Argus/_artifacts/feed/Main)
[https://dev.azure.com/ta-9/Argus/_artifacts/feed/Main/NuGet/TA9.Intsight.Infra.Middleware/versions/4.0.451-rc](https://dev.azure.com/ta-9/Argus/_artifacts/feed/Main/NuGet/TA9.Intsight.Infra.Middleware/versions/4.0.451-rc)

![image.png](/.attachments/image-8b63b000-ac6f-4023-8d69-d8922bee1612.png)

After downloading the needed version, move nuget package to TA9.Intsight.Infra.Middleware/.circleci git folder on your computer (My PC path example):
![image.png](/.attachments/image-2fdefc94-183c-48f6-affa-c637da0180f3.png)



After installation process and successful user creation, open Ubuntu cmd once again and move to TA9.Intsight.Middleare Git repository location on your machine. For me, the command looks like this:

`cd /mnt/c/repos/DevWorkspace/nugets/be-net-infra.middleware/.circleci/` 
`cd /mnt/c/repos/nugets/be-net-infra.middleware/.circleci/`

![image.png](/.attachments/image-1ab11f88-a0b8-4104-a8fe-aa19e885ad74.png)

*if it's youre first run u may need to install more packages (if u get an error pls follow the instruction in the end of the page) 
 
Now you need to run `dotnet-nuget-repack.sh` in .circleci folder with the following command in your Ubuntu cmd:
`sudo bash dotnet-nuget-repack.sh -n <nugetName> -r <version> -v`.

Example for current instance: 
`sudo bash dotnet-nuget-repack.sh -n TA9.Intsight.Infra.Middleware -r 4.0.435-rc -v`

Following line will appear, input "A" and press enter to approve file replacement.
![image.png](/.attachments/image-83391148-72cc-4f1a-99b9-bf79c7e9a243.png)


New nuget without `-rc` postfix will appear in folder:
![image.png](/.attachments/image-23d2b0d8-d29b-4742-96c4-ab23b20b89c0.png)



The only thing that left to do, is `nuget push` of a "release" version to Azure Artifacts. 
To do so, firstly, you will need to generate `Git Credentials` token for `nuget push` operation.


Go to any repository in Azure, for example: [https://dev.azure.com/ta-9/Argus/_git/DEV_Albert](https://dev.azure.com/ta-9/Argus/_git/DEV_Albert)

Click on clone, and then on `Generate git credentials`.
Copy the token, you will need it later
![image.png](/.attachments/image-3dbe710e-e674-41c2-a5b9-b273dfd7b9b1.png)

Now, open the windows cmd in `TA9.Intsight.Infra.Middleware/circleci` folder, and run the following command:

`nuget push <generatedNugetName> -Source Azure-TA9 -ApiKey <GitCredentialsToken>`

For current instance, the command looks like this (use your token, do NOT commit it anywhere):
`nuget push TA9.Intsight.Infra.Middleware.4.0.435.nupkg -Source Azure-TA9 -ApiKey <GitCredentialsToken>`


You will this this message:
![image.png](/.attachments/image-f282d45d-3680-449e-8a69-11af5ea9b0f4.png)

Great job, you've created new release middleware version and successfully pushed it to Azure Artcifacts!

first run :
1)open a commandline of ubuntu and run the following commands:
(*** after a month or so - if u got an error about pipeline re-run thus lines again)

sudo apt-get update
sudo apt-get install dos2unix
sudo apt install unzip
sudo apt install zip
sudo dos2unix dotnet-nuget-repack.sh

**Linux files are deferent from windows files so we need to convert this file : dotnet-nuget-repack.sh

2) need to install nuget program to push the nuget- download it from here : https://dist.nuget.org/win-x86-commandline/latest/nuget.exe.

3) If you encounter "Please provide credentials for: https://pkgs.dev.azure.com/ta-9/_packaging/Main/nuget/v3/index.json" --> run the nuget push from cmd\powershell it will work with your windows credentials.

move the file to a new folder name Nuget in programfiles :

![image.png](/.attachments/image-b9045173-3584-49dd-944a-a61587716bc3.png)

need to add the path to env variables :

![image.png](/.attachments/image-fe531e42-d0cc-403d-a7fc-159fde9df734.png)

![image.png](/.attachments/image-ae6a3caa-9b6f-4fed-8ae5-e17ec74e5a98.png)





