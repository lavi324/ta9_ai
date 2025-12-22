[[_TOC_]]


## Intro
Hardware Sizing Calculator for _IntSight_ v3.2 system is an Excel workbook consisted of some sheets for various components, sheet of assumptions, sheet for loading data calculations and sheet for usage calculations. All these calculations are reflected to the 'Production' sheet which contains all the services to be installed. Finally, the summary of all the services' resources are summed at the 'Summary' sheet.

## Important Notes
1. _TA9 IntSight_ is a versatile complex system with different implementations per project/customer which must be sized separately from this calculator. Additionally, since this is a platform and we're not bound to any specific/known usages, this calculator is very generic. A more detailed calculation and/or manual adjustments should be done once specific requirements are well known.
2. All calculations and assumptions are based on experience from existing deployments and usages of the system. It should always be fine tuned and revised to make it more & more precise.
3. Calculations of external components (e.g 'Document Viewer') should be taken from official vendor resource/s and merged into this calculator.




## Sheets Description
1. **Summary**
This sheet summarizes the sizing. You should enter some requirements on top and see their impact on bottom. You may also list 'Main Use Cases' section for readability.
2. **Production**
This sheet lists all services relevant to Vanilla deployment including Documents Viewer (accusoft) & ReportsGeneration (WindWard).
All services sizing here are regardless of OS requirements (ie - on top of OS).
If another service is required (e.g FaceRecognition/MessageBroker) - it has to be sized and added as column here manually.
3. **Sizing Assumptions Calculations**
In this sheet there are various sizing internal params used to perform calculations across the workbook. Each param is quite self explained alongside a comment and whom affected by it.
4. **Data Usage**
In this sheet we're calculating the usage resources for each component. On the left side you can see the parameters with counts (based on requirement) and a co-efficient aimed to normalize the value. Then, on the right side you can see each component with a value between 0 and 1 indicates the influence of each param on the component.
All together summed up at the bottom.
5. **Data Loading**
In this sheet we're calculating the number of records/files/storage for each repository based on entered details. Basically it contains known data sources - Emails/Documents/Entities & Relations/Transactional data. 
It's highly advised to list all known Data Sources with specific details to get best results.
6. **Maps (OSM)**
This sheet calculates required resources for worlwide osm maps server. You may change 'max latency' param only. For other mapping subsets - you can use linear change based on export file size
7. **MySQL/IQ/Solr/OrientDB**
These sheets contain simple ratio params between amount of records to cores and to RAM


## How to Use the Calculator
1. [Download 'Vanilla' version](https://ta9comp.sharepoint.com/:x:/s/devteam/ER0R59SgiC5OsOmL4savrWIBMHtkFu204eEUA10jkstpcg?e=KabfSk)  and save it (do NOT edit this document)
2. List 'Main Use Cases'
3. Enter 'Sizing Parameters' & 'Assumptions'
4. Add known data sources with details to 'Data Loading' sheet
5. Add any specific components if any
6. Review calculated resources on 'Production' & inspect any extreme values if any
7. Sizing is ready ✔️



