# In case when you have empty database 
•Download new version of database https://orientdb.org/download extract zip folder at proper place and  run db as process
•Run script from git repository \Argus\DBScripts\OrientDB in next order:
-OrientDB_1_CreateDB.txt (make sure that login and password in script are correct)
-OrientDB_2_BasicSettings.txt
-OreintDB_create_basic_relation.txt
-Others…
# In case when you have old database and you want to update it

In order to update db you need export data from old db and import it in new database

•Stop service TA9 Service Host and Stop WildFly application server
•Export your orientdb to proper place as described in next instruction
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/201/OrientDB-Backup
some properties don’t imported so you should do it manually 
execute query inside your old database and note last sequence index.
**SELECT SEQUENCE('idseq').next() from OIdentity LIMIT 20**

•Stop process of your old database
•Download new version of database https://orientdb.org/download extract zip folder at proper place and  run db as process
•Create new db with same name in new version of orientdb  to do so you can execute next query in orientdb console CREATE DATABASE remote:localhost/TA9 <<username>>  <<password>> plocal graph
•Import database as described in instruction.
•Sequence do not import correctly so you need drop sequence and add new one using last number of sequence which you noted before
Execute next query :

**DROP SEQUENCE idseq;**

**CREATE SEQUENCE idseq TYPE CACHED START <<your noted number>> INCREMENT 1 CACHE 20;**

**ALTER DATABASE CUSTOM standardElementConstraints=false**
