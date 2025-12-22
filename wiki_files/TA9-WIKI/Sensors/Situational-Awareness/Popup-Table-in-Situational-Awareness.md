This ability will enable the user to add details about incidents in the situational awareness app, including a free text segment along with more relevant parameters for the incident.   



 

## The new popup table details:  

- The ID will be fill automatically (the incident ID) and will not be editable.  

- At the first time the user opens this popup table viewer – all the fields (except the ID fields) will be empty and editable.  

- The user can edit and add data if it is already filled out or partly filled out.  

- By clicking on save – the data will be saved, an indication will display, and toast will indicate it was saved successfully. 

- The table icon will be bolded if the incident has details added. 

- The following columns will fill automatically in the first time:  

     Nature of case , Text of message, Location , Time.   

- If the user closes the viewer without saving popup will open:  
“Are you sure you want to close the viewer without saving?”  

 


## Incident Detail Data Model 

The details of each incident will be stored in a designated data model, and the incident ID will be the key of the data model. 

The viewer will always show the incident ID, and it will not be editable. The rest of the data properties will be editable. The insert/update capability in the data model will be changed by each property's behavior. 

The viewer displays all the data that was saved (no mandatory fields). 


**NOTE**: The data is editable, If the user edits or deletes the data in these columns, the last will be saved and displayed.  

  

## Export 

The new popup table viewer will export the map and the visual analysis.  

The export will include the details of the popup table if the viewer is open, and the details are displayed on the screen. 




## Permissions 

All the users with the ‘Situational picture’ app will have access to the new feature.   

To be able to see and edit the pop-up table the user should have: 

Insert and update action permission.  

Permission to the new data model.   


## Configuration
In system config table: configKey= eventExtension
Define the following:

```
configValue=
{"dataModelID":2488,
"hasExtField":22736,
"fields":
[{"source":11712,"target":22721},
{"source":11709,"target":22718},
{"source":11710,"target":22717},
{"source":11707,"target":22716}]}
```

dataModelID = the id of the new DM
For each field that needs to be autopopulated, define source (fieldid from events DM) and target (filedid from the new DM)


