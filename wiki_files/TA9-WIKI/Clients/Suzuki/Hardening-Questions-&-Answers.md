# Orient
•	/orientdb-server-config.xml - We disable the sandbox from the previous requirement.
•	security.json – We enabled audit for the servers. We are now using the enterprise version of Orient, which means that all this configuration can be done from the Admin portal.
•	Database configuration based on https://orientdb.com/docs/3.1.x/security/Database-Security.html - We have only one user, and no one should have access to these databases.
•	Can we bind OrientDB to only SPF network range instead of 0.0.0.0 under server config XML? It can be done at the firewall level. There is no option to provide a "whitelist" of allowed IPs. There are only two options: 0.0.0.0 or 127.0.0.1. If we choose the second one, none of our machines could connect to the server.
•	LUKS encryption

# SeaweedFS
the Seaweed file system does not support JWT token. Getting information from the Seaweed is restricted only to our backend which gets the information and generates the response to the client. The security measure for Seaweed is based on limiting access only to our specific services (containers) with a Firewall. 

# MariaDB
Enterprise license

# Backups
•	Seaweed - There is an option to mirror Seaweed – two instances of the file server, one active and one for backup. For this solution, HTX/SPF needs to provide an additional machine. https://github.com/seaweedfs/seaweedfs/wiki/Data-Backup
•	ELK – From the official documentation: (https://elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html
•	Vault – Backup using the official documentation: https://developer.hashicorp.com/vault/tutorials/standard-procedures/sop-backup
•	Redis – Cache database; no need for backup.
•	RabbitMQ – No need to backup; messages become irrelevant after some time.

# where are the user information stored within FOC platform
1. MariaDB: TA9 application metadata, eGIS layer configuration,  Data source configurations (Data model). This includes and Multimedia and user annotation in SITPIC.
1. OrientDB: Graph database cluster. Storing of the system ontology, entities and relationships. Facilitates the graph link analysis.  
1. Solr: Database cluster. Storing of indexes for Entities, documents, multimedia and data models. Storing of incident data received from CUB2 via MQ. 
1. SeaweedFS: File Storage - Stores uploaded & received file attachments.
1. ELK: Stores user activity and access logs for audit trail purposes.
1. Habor: Image repository. stores docker images.
