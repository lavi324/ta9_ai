[[_TOC_]]

# DataBases

## MySQL
## Solr
## OrientDB
## Seaweed
___________________
# Services

## FreeText
## Entities
## federated search
## Document Viewer
## File Loader
## LoaderService
## auto loader
## indexing 
## Blotter
## Media Analyzing
## Message Broker
## Reports Generation
## Text Analytics

___________________

# Sensors

## GeoLocation
## AnyVision 
## Video Synopsis
## situational-awareness
## Nominatim

___________________

# Data Models

## Audit
Troubleshoot:

MySQL automatically gets a few more updates from our system 
![image.png](/.attachments/image-58ccb115-6b47-4e55-a9d3-9ea263b3693b.png)

if you getting this in one of the audit sections:


#/report/-140
SELECT * FROM sqlite_metadata.dataschemafields1 where schemaid=-140;

Delete the rows:
department
filed_list
Caseid

from schema.
Do the same for each of the DM's:
#/report/-150
SELECT * FROM sqlite_metadata.dataschemafields1 where schemaid=-150;
 

## Finance
## Forensic
## Sub Systems
## Cellular
## Annotations
## Location History
## Subscribers
