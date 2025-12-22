**This feature allows users to differentiate between tiles inside Admin Studio tool, by configuring a profile that hides/displays admin studio tiles by request in V3.9.2**

## Configuring a Profile
First of all, you need to define a profile in system_config through the application Admin tools/MySQL workbench:

_Through MySQL workbench (e.g):_
![image.png](/.attachments/image-0ac95598-fad2-46ef-8164-bd84645e83a8.png)

_Through admin tool (e.g):_
![image.png](/.attachments/image-63ca74d5-fc80-4127-9136-8eebb7167924.png)
![image.png](/.attachments/image-eed555e2-762a-48b9-93ab-479dbd697f8b.png)
Add a new **ConfigKey**  with the following format:
`AdminTilesToHide_<yourCustomProfileName>`

In **ConfigValue** you need to pass the tile names that you **want to hide**, separated by comma.
Here is the list of our tile names:
- tileIdentifier
- tileDataModelManager
- tileOntolgyManager
- tileProfileManager
- tileUsers
- tileGroup
- tileSensors
- tileInsightsPlugins
- tileLookup
- tileCache
- tileLocalization 
- tileFormDefinition
- tileCheckConnections


## Choosing a Profile
1. Firstly, download a local Admin studio to the selected user's PC.
2. To choose Profile, you need to configure by adding a profile value in 2 configuration files:
*  app.config
* TAStudio.exe.config

The value needs to be changed to the profile name you chose:
`<add key="Profile" value="yourCustomProfileName" />`

