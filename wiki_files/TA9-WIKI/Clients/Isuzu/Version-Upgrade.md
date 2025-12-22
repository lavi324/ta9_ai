[[_TOC_]]

# Version Upgrade Plan

## Current Version 
2.9

## Installed Version 
2.9

Last Upgrade date: 02.08.2020

# Upgrade Plane Schedule

## 10:00: Backup VM’s DB’s

-	DIJAVSRV01 - 10.100.102.90
copy the Indexing.jar + Loader.jar to Temp folde
-	DIWINSRV02 - 10.100.102.90

-	MYSQL DISQLSRV01 – 10.100.102.92 
Location of Backup:
/opt/application/MySQLBackup02_08_2020/ MySQLBackup02_08_2020.sql
`sudo mysqldump -u root -p --single-transaction --all-databases > /opt/application/MySQLBackup02_08_2020/02_08_2020.sql`

-	SOLR DISOLSRV01

-	IQ disybsrv01

-	ORIENT DIORISRV01  

## 11:00: Environment services shut down  
### Stop services
-	10.100.102.90 
o	TA9 Service host
o	TA9 Loader service
o	TA9 indexing
-	10.100.102.91 
o	Wildfly
`sudo systemctl stop wildfly`

## 11:15 Upgrade
1.	Copy Installations files locally (in installation Path)

2.	Validate Configs

3.	Install New version

4.	Syncer

4.1 Run the  DBScripts/MySql/UpdateScripts/DBChangeSyncer-2_8_0_to_2_9_0.json according to current version

5.	Start services

6.	Sanity tests

6.1 Open CDR data model and run (checks both Reports service & IQ connection)

6.2 Open telco dashboard and run on an arbitrary number

6.3 Export telco dashboard (tests both ReportsGeneration service & Windward engine)

6.4 Open Face recognition  app and go to 'Cameras' tab - you should see the cameras

6.5 Open Briefcam App - you should be logged in auto

6.6 Open GeoLocation app - you should be logged in auto

6.7 Search in federated for an arbitrary word (tests federated & solr)
6.8 Open an entity from Federated results (tests Entities & orientDB)
Open a document from federated results (tests document viewer)
7.	Extras

8.	Replace Export Formats + config

9.	Restart Services

14:00 – QA
