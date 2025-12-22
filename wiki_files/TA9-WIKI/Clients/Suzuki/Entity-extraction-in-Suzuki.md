# New PLA Tool for missing entities - 3.6.2025
**Query PLA Tool feature for missing entities**

Z:\Clients\suzuki\pla-tool

# Index Endpoint –  Usage Guide

The PLA process is designed to ensure the OrientDB database reflects the detected event entities, particularly when the incoming incident data is inserted to the system. Recognizing that such streams can sometimes experience gaps or "holes," this functionality provides an option to specifically execute the update process for a defined time window. This allows for targeted backfilling or reconciliation of data within a specified period, addressing any inconsistencies that might arise from interruptions in the real-time notification stream and ensuring data integrity within OrientDB.

## Endpoint

```
GET /Index?start={START}&end={END}&batchSize={BATCH_SIZE}
```

## Parameters

- `start`: `string` (format: `yyyy-MM-ddTHH:mm:ssZ`) – Start date/time in UTC.
- `end`: `string` (format: `yyyy-MM-ddTHH:mm:ssZ`) – End date/time in UTC.
- `batchSize`: `integer` (optional, default: 1000) – Number of records per batch.

## Example curl Command

```bash
curl -X 'GET' \
  'http://pla_host/Index?start=2025-04-29T06:00:00Z&end=2025-04-29T09:00:00Z&batchSize=1000' \
  -H 'accept: text/plain'
```

## Successful Response (HTTP 200)

```json
{
  "version": "1.0.0.0",
  "code": 200,
  "message": null,
  "isError": false,
  "responseException": null,
  "data": {
    "count": 1000,
    "time": "2025-04-29T06:41:56Z"
  }
}
```

## Failure Response (HTTP 500)

If something goes wrong on the server, the endpoint will return:

- **HTTP Status**: 500 Internal Server Error
- The response body may vary depending on the exception.

## Validation Checklist

- Ensure `start` and `end` dates are in correct UTC format.
- Ensure `end` is after `start`.
- Ensure `batchSize` is a positive integer.

> **Note:** Since the PLA service does not have access to the external network (its ports are blocked),  
> you must run this curl command from a container that is on the `plugins` Docker network.

One option is to use the **Data Model Search Service** container.




# Questions and answers - need to update according to new tool

### Entity extraction, which microservices and how it works until OrientDB?
      
Text Analytics Service is used for Entity Extraction. In our project, entity extraction extracts entities from the incident description. Once entity is extracted from the incident text it goes to dedicated columns in the incident DM (columns identified with EE). From the extracted data, we can create relevant entities in Orient using the PLA. The text analytics service can extract data using two methods:
1. NER - More information about NER can be found at [https://medium.com/mysuperai/what-is-named-entity-recognition-ner-and-how-can-i-use-it-2b68cf6f545d](https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmedium.com%2Fmysuperai%2Fwhat-is-named-entity-recognition-ner-and-how-can-i-use-it-2b68cf6f545d&data=05%7C02%7Cnoga.segev%40t-a9.com%7C636956b9911145d15f5f08dc5ddf1e72%7Caa3dc9967cab424f97d50dee6d84dc4d%7C0%7C0%7C638488461359713090%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=295VCXShVWByOpzlCCa3BHz0FdsGJJMtJTL2%2FotYFV4%3D&reserved=0).
2. Regex - It can extract data using the regex that we provide. For example, it can extract NRIC numbers using regex because the NRIC format is unique to Singapore.

      
The data extracted from the incident text by the **text analytics service**, which can extract data using two methods: 1. NER; 2. Regex. Please use the link provided for more information.

### When user do a entity search, which microservices used and how it read which database?

one is the federated search, which goes to the federated search service.
The second is the Graph feature (link analysis) which goes to the entity service.
the federated search triggers the federated search service,  and the link analysis triggers the entity service.

### Consuming of incident from MQ (From ST interface server > API gateway > which micro services > which services write to which database (MariaDB, Solr, OrientDB, SeaweedFS?

The process starts with the Message broker service – Data models search service (Solr) – PLA service – entity service. In general, all the services write to Maria; Entities service write to Orient; DMS FS and Indexing services write to Solr; The file server writes to Seaweed.

PLA (post loading action) uses the extracted data from the incident text to create the entities in the Orient.
The message broker is the service that receives STE call messages.

---
---
---



**Entity Extraction – Data Flow and Microservices**

The Text Analytics Service is used for Entity Extraction. In this project, entities are extracted from the incident description and inserted into dedicated columns in the incident Data Model (marked with the prefix "EE"). Using this extracted data, relevant entities are later created in OrientDB via the PLA (Post Loading Action) service.

The Text Analytics Service supports two extraction methods:
1. **NER** (Named Entity Recognition) – More information:
 https://medium.com/mysuperai/what-is-named-entity-recognition-ner-and-how-can-i-use-it-2b68cf6f545d  
2. **Regex** – Used to extract patterns such as NRIC numbers, which follow a unique format in Singapore.

---

Entity Search – Microservices Involved

When a user performs an entity search, two main microservices are used:
- **Federated Search** – Triggers the *Federated Search Service*
- **Graph (Link Analysis)** – Triggers the *Entity Service*

---

Incident Ingestion – MQ to Database Flow

The incident flow from the ST interface server proceeds through these stages:
1. ST Interface Server
2. API Gateway
3. Message Broker Service
4. Data Model Search Service (Solr)
5. PLA Service
6. Entity Service

Data is written to the following destinations:
- MariaDB – General service data
- OrientDB – Entities (via Entity Service)
- Solr – Indexed data (via DMS FS and Indexing Services)
- SeaweedFS – File storage (via File Server)

---

Note: The PLA (Post Loading Action) process uses the extracted text data to create entities in OrientDB.
 The Message Broker is the service responsible for receiving call messages from the STE system.
