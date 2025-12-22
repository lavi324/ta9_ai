# Person report

Person report is a project-external development that is not part of our core product.

## Overview   
    

Person Report were originally developt for the FOC environment and migrated to the FOC environment. The Person Report is Dashboard that provide data of Person based on the NRIC ( National Registration Identity Card). This application had designed as external application and using as sensor action.   

The Person Report is a feature configured as an external accelerator application under the name “SensorCation”.  

It is designed to retrieve enriched person-related data from external systems based on a national identifier (NRIC). 

## Configuration   
    

The feature is configured in the system’s backend under a dedicated table called **Sensor Action**, which defines the parameters and logic for triggering the Person Report. 

## Trigger Logic   
    

Sensor appears when the user press on column that has identifier type of NRIC , this id pass as query param to the url and send to the backend of the sensor. The sensor using some internal SPFs api to get relevant data about the person and in the end it  build final object to app it to the UI (dashboard).   

The activation of the Person Report is triggered when a specific **identifier of type NRIC** (National Registration Identity Card) is detected.   

Once an NRIC value is received, the system launches an **external application** (not developed or maintained by our company) to display the report. 

## External Integration   
    

The opened report interface uses the provided NRIC as input and initiates a **series of API requests** to the client’s backend systems. These APIs are not internal to our system but are owned and maintained by the client.   

The application consumes responses from **multiple APIs** and builds a **dedicated object** containing relevant person-related information. 

## Visual Output   
    

After the object is constructed, its fields are mapped and presented in a **visual format**. If available, the output may include a **photo of the individual**, along with other extracted fields. 

Notes: 

*   This integration is dependent on external APIs and services. Our system is only responsible for triggering the process and passing the required identifier (NRIC) as input. The rest of the process—including data retrieval, response parsing, and visualization—is handled by the external application. 
    

*   The Person Report operates independently from the entity extraction and creation flows in the PLA. It does not result in the creation or modification of any entities within OrientDB or other internal data stores. The visual output is for reference only and is not persisted in the system. The feature is intended solely for external enrichment purposes and does not affect the internal data model.


https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/_layouts/15/Doc.aspx?sourcedoc=%7B2BF946C8-33E1-4C68-A86C-09FE56FB224D%7D&file=Person%20Report%20-%20Suzuki.docx&action=default&mobileredirect=true

## Notes

Report Alex developed on-site.
we shared the code with the client, and now they are the owners of it.

more info can be found on the README file - [Person report](https://ta9comp.sharepoint.com/:f:/r/sites/businessteam/Shared%20Documents/Projects/Suzuki/FOC/Person%20report?csf=1&web=1&e=woW4zn)

### Q&A from the client and Alex:      

1.  Can we confirm that Application (like the person report), consist of the following components and changes:
-  UI perspective service (to deploy at web stack) **yes part of the docker-compose file**
- Plugin service (to deploy at plugin stack) **yes part of the docker-compose file**
- Update of Nginx Configuration (on web stack) **yes possible to add new route on default.config**
- Update sqlite_metadata database  on sensor_actions table **possible to from admin studio => new sensor action
- Change to sensorservice of backend stack no relevant**
- configure Admin studio **possible to from admin studio => new sensor action**

2.  We need technical training and technical guide document to archive the following:
-  Make changes to the person report application - **there only one service that contain all BL**
- Create new application similar to person report, example like developing a new vehicle details report from scratch. Include details of development the components and changes mentioned **in 1(a) to 1(f) in the end this external service to our app , it can be developed with any technology of ui and backend.**

3.  For 2(a), can we confirm that changes to the UI prospective component can also be changed by ST? If yes, can we have the source code for the UI and plugin components? - **provided UI and backend source code**