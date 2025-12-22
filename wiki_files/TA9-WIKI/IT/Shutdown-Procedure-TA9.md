##Shutdown sequence
1. Stop the indexing and the loader services.
Windows: 
Go to Services look for the indexing and the loader services.
Stop both services.
Linux:
Use the command:
`sudo systemctl stop indexer/loader.service`

2. Stop the Wildfly service.
Windows:
Go to Services look for the wildfly service.
Stop the Service.
Linux:
Use the command:
`docker stop wildfly`

3. Stop TA9 Core Services.
Windows Only!
Go to Services look for TA9 Core Services and stop the service.

4. Stop the diffrent Databases
Windows:
Go to Services and look for the services for the database server.
Stop them one by one.
Linux:
Use the commands:
`docker stop mysql-{verison}`
`docker stop orientdb`
`docker stop solr`
`docker stop iq`

The power on sequence should be:

Databases
Wildfly
Indexer and Loader services
TA9 Core Services