# Introduction

![image.png](/.attachments/image-c89cbc3a-6047-4f69-9001-a829d650941a.png)

In an entity with a calculated field when you insert the start date and end date, the calculated field will return the number of days between the start date and the end date. 

# Configuration
In order to create a calculated field you need to create 3 fields in your entity:

1. Start Date property (data type = Date time)
2. End Date property (data type = Date time)
3. Duration property -the calculated field (Role type= Event Sequence + Red Only)

Run this query :`SELECT * FROM sqlite_metadata.system_config where ConfigKey ='durationFieldCalculation';`

Add to the config value, a new set of values of the new entity:

  "EN@entityid": [
    {
      "startDateFieldId": "EP@EntityID_StartDateID",
      "endDateFieldId": "EP@EntityID_EndDateID",
      "durationDateFieldId": "EP@EntityID_DurationID"
    }
The values can be found in the scheme: sqlite_metadata.em_property_definitions

![image.png](/.attachments/image-f5680053-4fe7-4231-b190-cbf631a7cfa5.png)


