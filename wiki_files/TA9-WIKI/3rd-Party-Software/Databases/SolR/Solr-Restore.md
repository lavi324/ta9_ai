[[_TOC_]]

# Backup location

the backup location could be very, 

basicly is located in the same place as the data located for example:

## Backup location of freetextindex
G:\solr\freetextindex\data\snapshot.20200419114413428

## Backup location of freetextindex

G:\solr\freetextindex\data\snapshot.20200419114442905

Format: 20200419114413428
Meaning: yyyymmddhhmmss
yyyy = Year
mm= month
dd= days
hh= hours
mm=minutes
ss=seconds

# Restore

## Restore freetextindex

`http://localhost:8983/solr/freetextindex/replication?command=restore&name= snapshot.20200419114413428`

**Change the name according to yours**

#Check status of the restoration
## data model status:

http://localhost:8983/solr/freetextindex/replication?command=restorestatus

If completed :

![image.png](/.attachments/image-04855cdc-37c8-4746-9845-7c8f907c09eb.png)
