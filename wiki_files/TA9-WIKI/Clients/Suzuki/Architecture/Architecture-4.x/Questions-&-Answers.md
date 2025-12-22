1. How is the workloads being allocated or assigned in the 8 processing nodes - the docker manager is managing the work between the processing nodes.
1. How is the access control between microservices in TA9Insight Platform being managed. Example : How does the application allow which microservices to talk to it? TA9Insight Platform is a closed environment. The services work together with an internal token. 
1. How is the information from external (outside Docker swarm) access the microservices. Need details elaborate on the entry point from outside Docker swarm to the microservices - Information outside Docker swarm access the microservices through the API Gateway, using a valid token and API key.
1. Consuming of EGIS map service (From SPF EGIS REST API > how and who(Microservices) consume the map services? The data model search service consumes the map service. 
1. Consuming of incident from MQ (From ST interface server > API gateway > which micro services > which services write to which database (MariaDB, Solr, OrientDB, SeaweedFS – The process starts with the Message broker service – Data models search service (Solr) – PLA service – entity service. In general, all the services write to Maria; Entities service write to Orient; DMS FS and Indexing services write to Solr; The file server writes to Seaweed. 
1. How does the user authentication works? Currently, we validate the user and password in front of the TA9 system. At the beginning of January, you will receive a new version that includes support by user management API for STE IDMS for a user management system. The integration with IDMS will be done by STE with the API TA9 developed. Once user is defined in the system he can log in with username and password.
1. From end user, when they access sitpic and put attachment, which microservices is being trigger and the flow until how data is stored in which database – The message broker receives the attachment file and loads to it Seaweed. After the message broker takes this row to the attachments data model which is located in the MariaDB. 
1. Entity extraction, which microservices and how it works until OrientDB-  Text Analytics Service is used for Entity Extraction. In our project, entity extraction extracts entities from the incident description. Once entity is extracted from the incident text it goes to dedicated columns in the incident DM (columns identified with EE). From the extracted data, we can create relevant entities in Orient using the PLA. The text analytics service can extract data using two methods: 1. NER - More information about NER can be found at https://medium.com/mysuperai/what-is-named-entity-recognition-ner-and-how-can-i-use-it-2b68cf6f545d.2. Regex - It can extract data using the regex that we provide. For example, it can extract NRIC numbers using regex because the NRIC format is unique to Singapore. 
1. When user do a entity search, which microservices used and how it read which database? We have 2 options in TA9 to do an entity search: one is the federated search, which goes to the federated search service. The second is the Graph feature (link analysis) which goes to the entity service.
10. Vault -
a)	Vault validates the request using a token. After successful authentication, Vault generates a token for the client. This token is used to authenticate subsequent requests. 
b)	Vault protects the key residing in it as it is considered secured internally by definition. The saved data is already encrypted on rest. For more information, you are advised to review the links provided by Vault's official site.
https://developer.hashicorp.com/vault/docs/what-is-vault
https://developer.hashicorp.com/vault/docs/internals/architecture
https://developer.hashicorp.com/vault/docs/internals/security
11. Swarm - 
The communication between Swarm nodes is secured and encrypted. The manager channel is swarm is secured. When defining a network in Swarm, it is isolated. This means, there are no ports directed outside except the front and the admin gateway, which has SSL and JWT protection. For more information, you are advised to review the link provided by Docker's official site. 




