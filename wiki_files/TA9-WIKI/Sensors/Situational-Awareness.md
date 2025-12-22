1. Create a new core called Events on SolarDB 
   - Switch to solr user `sudo su solr`
   - Go to Solr folder
   - run next script : `bin/solr create -c Events`
![image.png](/.attachments/image-917aeadc-a04c-4379-861a-aa0784417096.png)   
   - Reset the solar and check if the new core added to the list
1.  Add the core schema params
    - Copy the Schema property from [https://dev.azure.com/ta-9/Argus/_git/Argus?path=/DBScripts/Solr/events/managed-schema]() and paste to the Events core folder
    - Reset Solr service and check if the schema is updated. 
1. Change commit properties on solrconfig file. 
   - find <autocommit> and paste next: 
		<maxDocs>5000</maxDocs>
		<maxTime>30000</maxTime>
		<openSearcher>false</openSearcher>
   - find <autoSoftCommit> and paste next:  
		<maxTime>1000</maxTime>
   - Reset Solr service again

1. Run Situational_Awareness.sql script 
1.  Import lookup tables into the databases. 

1.  Insert the images into `crime_map_icon_lu tabel`. This process can be done using TA9UploadFiles util. The images folder located at 
     - https://ta9comp.sharepoint.com/:f:/r/sites/businessteam/Shared%20Documents/Product/DM%20pix/Situational%20Awareness/Icons?csf=1&web=1&e=UDwSJi
1.  Create a new identifier called Report Number with next regular expressions:
    - [A-Za-z] \\/ (18|19|20)\\d{2}(0[1-9]|10|11|12)([0-2][1-9]|10|20|30|31) \\/ \\d{4}
    - W(18|19|20)\\d{2}(0[1-9]|10|11|12)([0-2][1-9]|10|20|30|31) \\/ \\d{4}
    - (18|19|20)\\d{2}(0[1-9]|10|11|12)([0-2][1-9]|10|20|30|31) \\/ \\d{4}
    - (S|C|D|F) \\- \\d{4}
    - (S|C|D|F)\\d{4}
    - [A-Za-z] \\/ \\d{2}
    - WTA \\-\\d{7}-\\d{4}
    - WTA \\/ \\d{7} \\/ \\d{4}
    - WTA\\d{11}


1. Create Incident Entity based on next parameters:
![image.png](/.attachments/image-96fbc5b4-88a4-4f62-a89d-21b20dffa556.png)
1.  Clone next repository https://dev.azure.com/ta-9/Argus/_git/ClientSuzuki 
    - Open EventsPostLoadingAction solution , it located on : PostLoadingActions/EventsPostLoadingAction
    - In solution open EventPostLoadingActionsConfig.json and change the Entities property as defined on Admin Studio
1. Copy Incidents PLA (post loading actions)  to PLA folder (path can be found on system_config table) 

1. Reset TA9host service. 
  

