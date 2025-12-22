[[_TOC_]]

# Introduction

![image.png](/.attachments/image-233f9d9e-4ef4-4e6b-bf76-7c1caac8720a.png)

Solr is an open-source search platform which is used to build search applications. Solr is enterprise-ready, fast and highly scalable. The applications built using Solr are sophisticated and deliver high performance.

# Solr Backup API

# Manually Backup Solr


# Backup API command 

http://localhost:9500/solr/CoreName/replication?command=backup

**Change localhost with the solr IP address**
**Change CoreName according to solr core Names**


##Core list

![image.png](/.attachments/image-ba57423e-892d-4e37-9c71-624ef01ec386.png)


## Linux Location
![image.png](/.attachments/image-68320d8a-1c0c-4a73-8352-9bd339a96267.png)


# Default backup location

![image.png](/.attachments/image-e8f175f9-b25c-4333-a6f8-2d874efd577b.png)


# Backup Status

You can check the status of the backup with simple command : 


 http://localhost:9500/solr/CoreName/replication?command=details


# Script to backup datamodels:
```
#!/bin/bash

COLLECTION=datamodels
MYDATE=`/bin/date +%Y%m%d`
MYBACK="${COLLECTION}-${MYDATE}-backup"
BACKUPNAME=MYBACK
BACKUPDIR=/home/ta9/SolrBackup
SERVER=YOURIP
PORT=9500

curl -s "http://${SERVER}:${PORT}/solr/${COLLECTION}/replication?command=backup"
```

# Script to backup FreeTextindex
```
#!/bin/bash

COLLECTION=datamodels
MYDATE=`/bin/date +%Y%m%d`
MYBACK="${COLLECTION}-${MYDATE}-backup"
BACKUPNAME=MYBACK
BACKUPDIR=/home/ta9/SolrBackup
SERVER=YOURIP
PORT=9500

curl -s "http://${SERVER}:${PORT}/solr/${COLLECTION}/replication?command=backup"
```





_______________________________________________________________________________________________________________________

# Restore API

Restoring the backup requires sending the restore command to the /replication handler, followed by the name of the backup to restore.

You can restore from a backup with a command like this:

http://localhost:9500/solr/gettingstarted/replication?command=restore&name=backup_name

**Change the localhost to IP address of Solr**

**Change the gettingstarted core name to one of your own corename used as before**

**Change the backup_name to the name of your backupname**


## Restore Status API

You can also check the status of a restore operation by sending the restorestatus command to the /replication handler, as in this example:

http://localhost:8983/solr/gettingstarted/replication?command=restorestatus

**Change the localhost to IP address of Solr**

**Change the gettingstarted core name to one of your own CoreName used as before**



_______________________________________________________________________________________________________________________



# Create Snapshot API

The snapshot functionality is different from the backup functionality as the index files aren’t copied anywhere. The index files are snapshotted in the same index directory and can be referenced while taking backups.

http://localhost:9500/solr/admin/cores?action=CREATESNAPSHOT&core=CoreName&commitName=commit1

**Change the localhost to IP address of Solr**
**Change the gettingstarted core name to one of your own corename used as before**
**Change CoreName according to solr core Names**


## List Snapshot API

The list snapshot functionality lists all the taken snapshots for a particular core.

You can trigger a list snapshot command with an HTTP command like this (replace "CoreName" with the name of the core you are working with):

http://localhost:9500/solr/admin/cores?action=LISTSNAPSHOTS&core=CoreName&commitName=commit1

**Change the localhost to IP address of Solr**
**Change the gettingstarted core name to one of your own corename used as before**
**Change CoreName according to solr core Names**

## Delete Snapshot API

The delete snapshot functionality deletes a particular snapshot for a particular core.
You can trigger a delete snapshot command with an HTTP command like this (replace "CoreName" with the name of the core you are working with):

http://localhost:9500/solr/admin/cores?action=DELETESNAPSHOT&core=CoreName&commitName=commit1

**Change the localhost to IP address of Solr**
**Change the gettingstarted core name to one of your own corename used as before**
**Change CoreName according to solr core Names**