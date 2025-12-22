#To apply justification on the TA9 system on 4.x version you should follow the next steps

1. Backend config - 
A. Go to 'SystemConfiguration' Secret in vault
B. Edit these 2 parameters, set to true to apply justification
![image.png](/.attachments/image-95448527-18f3-46fe-8488-398d997bc8eb.png)
##If they do not exist create them in the 'SystemConfiguration' secret json

2. System config
* Go to Maria DB and run the following query:
select * from sqlite_metadata.system_config where ConfigKey like '%FrontEndConfiguration%'
At the config value section, change the value of the "justification" parameter to true.

3. Tile
* Go to Maria DB and run the following query: 
select * from sqlite_metadata.tiles t where TileName = 'open-justification-case'
To switch cases while logged in, make sure the value of Visible is 1

#Justification applied