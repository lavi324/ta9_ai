[[_TOC_]]

In our organization there are many devops tools in use, but the main hub through which most of it is managed is Azure Pipelines a part of the azure devops package. 
With Azure DevOps we can manage, schedule and run automated tasks with itself or with help from other tools as Docker or Ansible.

[Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/index?view=azure-devops)

#Key-Words
* Agent - Installed locally or on Cloud, is the runner of the builds. Each build or agent job can be run with a different agent.  
* Build - The whole process which consists of agent jobs.
* Agent job - A part of a build with consists of several tasks, can run in parallel or be dependent of one another.
* Task - A single step in an Agent job can compile deploy or do pretty much anything that can be achieved with scripts. Some tasks come out of the box with azure pipelines, other custom tasks can be created to fit a specific organization requirement.     

#Running a build
All of the builds of the organization are divided to categories, firstly by the build type and secondly by environment. For example if you want to build and deploy a cloud build go to \BuildAndDeploy\Cloud select the desired build and press queue, if there re parameters that you would like to change do so in the queue window.

![image.png](/.attachments/image-7caa840e-62cf-4afb-88e8-6d60de4ebc8f.png)

#Editing a build
If you have the required privileges you can edit a build do the same as in the previous topic but click the edit button. Now you can see all of the Agent jobs and tasks.
to get more information on how to configure or change the build please consult with the Microsoft documentation (link is at the top of the page).

#Build variables
![image.png](/.attachments/image-7b3d490a-f469-4a0f-89e2-8c485e767b19.png)
Variable can be defined for each build definitions or pre-defined variables can be.
[Predefined variables list](https://go.microsoft.com/fwlink/?linkid=849035)
* Choosing Build mode for release or debug can be by defining such, in most build it is already defined and can be set according to preference. 
* Credentials can be set, Don't forget to lock the variable if using passwords.
* IPs and URLs can be set so all of the build tasks will use the same. 

#Build triggers
Build triggers can be defined in order to start the build automatically.
* Enabling continuous integration - make the build run with each push to the branch it watches.
* Set a time trigger - [Trigger Configuration](https://docs.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops&tabs=yaml)


# General build and deploy build
The most used build in the organization, compiles and deploys the required branch to an environment of your choosing.
This build consists of 3 agent jobs which cant run in parallel.

[GEN_Full_Build](https://ta-9.visualstudio.com/Argus/_build?definitionId=88)

![image.png](/.attachments/image-39735f92-54d2-4609-b329-f8b94efefeed.png)


## Web
Pretty straight forward, downloading packages with NPM, compiling with Gulp and deploying. 
* The npm Powershell script is clearing catch and downloading packages using a specific npm version and finally yarn is fixing the dependency version so it would work for both AngularJS and Angular8.    
* The Gulp tasks are compiling the TypeScript 
## JAVA
Here we have something a bit different, most of the compilation is done in a task group which consists of several tasks.
After all of the services are compiled they are deployed to the chosen environment.
## .NET
Packages and downloaded then build using the standard MSbuild task, when the compilation is done the service on the target environment is stopped dbsyncer is running the DB update and finally it will deployed to the environment and start the service back up.
