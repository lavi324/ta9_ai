In order to deploy and install a new extension to the system, follow these steps:

#Part 1 - Deploy

- Access '**circleci**' pipelines inside the project you wish to deploy an extension from
- Make sure you are in the main branch
- Click '**Trigger Pipeline**' as described in the picture below
![image.png](/.attachments/image-b8b94ae9-d00f-456d-bd02-ab79f4db99d1.png)
- Click '**Add Parameter**', and add a parameter called '**directory_path**'.
The value should be the relative path to the '**.csproj**' file containing folder, starting from the repo main folder (as shown in the picture below) and click 'Trigger Pipeline'
![image.png](/.attachments/image-f4e1cb8c-2f4d-456c-87a0-3bbd70d50ab1.png)
- After the pipeline finish running and does not raise any errors, contact your friendly neighborhood DevOps engineer and let them know there is an extension ready for deployment, and before the next part the DevOps engineer has to deploy the build created by the pipeline we just triggered. This will result in a container running in (let's say, Portainer) which will be up and ready to be created on TAStudio, with a brand new Port attached.


# Part 2 - Install

- After the DevOps engineer finished deploying, access the '**TAStudio**' app of the server the extension is deployed to.
- Click '**Data Models**'
![image.png](/.attachments/image-43f68fdb-9486-4756-9763-150fca86f484.png)

## Parser installation
- Click '**Parsers**' and fill the fields shown in the picture below
![image.png](/.attachments/image-84e148c3-0687-4d59-8c28-ae7a47969f01.png)
- Name - The visual name of the parser to be recognized in the system
- URL - fill the URL of the host as shown in the picture, and in the port section use the port set previously by the DevOps engineer in the '**docker-compose.yml**' file (will usually be ports above 10k, as our convention)
- Data model ID - the ID of the DM the parser inserts it's results to.
- Parser type - Insert the parser type according to the interface it implements
- Click 'Add Parser' 

## Plugin Installation
- Click '**Add Data Connection**' > '**Plugin**' and fill the fields shown in the picture below
![image.png](/.attachments/image-12327b81-37fa-43dc-97f3-9925239f4035.png)
- URL - Enter the URL of the host as shown, and in the port section use the port set previously by the DevOps engineer in the '**docker-compose.yml**' file (will usually be ports above 10k, as our convention). After the port add '**/api/plugin-service**' suffix
- Name - The visual name of the plugin to be recognized in the system
- Click '**Test Connection**', if the plugin was deployed with no issues and the port was set correctly the connection test should be successful.
- Click '**OK**'
- You will be directed to create a data model for the plugins results. After creating the data model the plugin is installed.
