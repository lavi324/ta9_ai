[[_TOC_]]

#Introduction
OrientDB is an open-source NoSQL database management system written in Java. It is a Multi-model database, supporting graph, document, key/value, and object models,[2] but the relationships are managed as in graph databases with direct connections between records. It supports schema-less, schema-full and schema-mixed modes. It has a strong security profiling system based on users and roles and supports querying with Gremlin along with SQL extended for graph traversal. OrientDB uses several indexing mechanisms based on B-tree and Extendible hashing, the last one is known as "hash index", there are plans to implement LSM-tree and Fractal tree index based indexes. Each record has Surrogate key which indicates the position of the record inside of Array list, links between records are stored either as a single value of record's position stored inside of referrer or as B-tree of record positions (so-called record IDs or RIDs) which allows fast traversal (with O(1) complexity) of one-to-many relationships and fast addition/removal of new links.

1. System main GraphDB – holds all the system entities and relations
2. Default port is 2480 and can be accessed using the web at: http://Server_IP:2480
3. OrientDB logs will be located at %ORIENTDB_HOME%\log folder
4. Each entity definition will be saved as a vertex class ENX – X will be the entity definition id, all ENX will inherit from TAEntity
5. Each relation definition will be saved as an edge class RLX – X will be the relation definition id, all RLX will inherit from TARelation
6. Each definition will have 2 types of properties:
   * System properties – starts with Sys_
   * User defined properties – starts with EP 
7. OrientDB can be deployed on windows service (‘OrientDB GraphEd DEV’) or on dedicated Ubuntu server

#Installation:
##Windows
1. Copy "\\\10.100.102.13\share\Artifactory\Deployment\DBs\orientdb-community-2.2.30" to a local directory.
2. Run \service\TA9_install.bat as adminnistrator.
3. Validate installation by going to http://Orientdb_IP:2480

##Linux
1. You can run a [playbook](https://ta-9.visualstudio.com/Argus/_git/CM?path=%2FAnsible%2FDBs%2FOrientDB.yml&version=GBmaster) using ansible to deploy a OrientDB server.

### Manual Installation (Linux).
2.	Copy the Orient package (The same as the windows one) to /opt folder.
3.	Add system variable.
3.1.	Sudo nano /etc/environment
        Add this: ORIENTDB_HOME="location of orient db installation folder"
4.	Update settings.
4.1.	sudo $ORIENTDB_HOME/bin/orientdb.sh
        
       ```
        ORIENTDB_DIR="YOUR_ORIENTDB_INSTALLATION_PATH"
        ORIENTDB_USER="root"
       ```
5.	Make OrientDB run as a service.
5.1.	Copy orientdb.sh to the init.d folder
        sudo cp $ORIENTDB_HOME/bin/orientdb.sh /etc/init.d/orientdb
        update-rc.d orientdb defaults
6.	Reset password and run base config script.
6.1.	Start orient manualy to configure first time password.
6.2.	Run the following commands (on Empty DB):
    -	sudo $ORIENTDB_HOME/bin/console.sh “CREATE DATABASE remote:localhost/TA9 root root plocal graph”
    -	sudo $ORIENTDB_HOME/bin/console.sh /base script location/OrientDB_2_BasicSettings.txt

#MISC
* Highly recommended to do the tutorial on OrientDB web site
* Orient troubleshooting: http://orientdb.com/docs/2.2.x/Troubleshooting.html


_____________________________________________________________________________________________
# How to increase memory on OrientDB:

1. Shut down the OrientDB
2. Backup it's content
3. Delete TA9 folder in the DB location
4. Add CPU.
5. Copy the same folder whom backed up
6. Turn the service on

_____________________________________________________________________________________________
# Troubleshooting
## How to delete vertex / edge
Make sure you delete vertex with DELETE VERTEX command (same for edge - DELETE EDGE ) and not "delete...unsafe"
the delete unsafe will delete only the specific object and not all the pointers and relation for other objects
## Graph problem
In case you have some problem in the graph,
for example, if you tried to delete a vertex from the graph, and use "delete unsafe" command instead of "delete" command, you will have some inconsistency in the graph.
to fix that, you can :
###Windows
1. go to orient folder -> bin -> run console.bat
2. In the console, connect to the DB, command example:   connect remote:10.100.102.234:2424/TA9/ <username> <password>
3. save a backup of the DB - EXPORT DATABASE /temp/petshop.export
4. start fix graph command - REPAIR DATABASE --fix-graph
5. you can also use check command to check is there any problems before you run the repair command: CHECK DATABASE ...

###Linux
1. go to orient folder -> bin -> run console.sh
2. connect remote:10.100.102.25/TA9 <username> <password>
3. save a backup of the DB - EXPORT DATABASE /temp/petshop.export
4. start fix graph command - REPAIR DATABASE --fix-graph
5. you can also use check command to check is there any problems before you run the repair command: CHECK DATABASE ...

### docker
1. Stop the container and take files under the databases folder to safe place.
` cp -v /opt/orientdb/databases/TA9 /path/to/safe/place`
2. switch to docker container
` docker exec -it /bin/bash`
3. find the console.sh
` find / -name "console.sh"`
4. Run the console from what you find. 
5. start fix graph command - REPAIR DATABASE --fix-graph## Convert a multi-value column to single-value column

### migration
Property can not be null error message in trying to update existing entity or create a new one.

WildFly log:
java.lang.IllegalArgumentException: Property value can not be null
2022-03-02 11:54:21,961 INFO  [stdout] (Log4j2-TF-2-AsyncLoggerConfig-1) 	at com.tinkerpop.blueprints.util.ExceptionFactory.propertyValueCanNotBeNull(ExceptionFactory.java:60) ~[blueprints-core-2.6.0.jar:?]
2022-03-02 11:54:21,961 INFO  [stdout] (Log4j2-TF-2-AsyncLoggerConfig-1) 	at com.tinkerpop.blueprints.impls.orient.OrientElement.validateProperty(OrientElement.java:547) ~[orientdb-graphdb-3.1.10.jar:3.1.10]
2022-03-02 11:54:21,962 INFO  [stdout] (Log4j2-TF-2-AsyncLoggerConfig-1) 	at com.tinkerpop.blueprints.impls.orient.OrientElement.setProperty(OrientElement.java:175) ~[orientdb-graphdb-3...

Original code of com.tinkerpop.blueprints.impls.orient.OrientElement.validateProperty:

public final void validateProperty(final Element element, final String key, final Object value) throws IllegalArgumentException {
 if (settings.isStandardElementConstraints() && null == value)
  throw ExceptionFactory.propertyValueCanNotBeNull();
 if (null == key)
  throw ExceptionFactory.propertyKeyCanNotBeNull();
 if (settings.isStandardElementConstraints() && key.equals(StringFactory.ID))
  throw ExceptionFactory.propertyKeyIdIsReserved();
 if (element instanceof Edge && key.equals(StringFactory.LABEL))
  throw ExceptionFactory.propertyKeyLabelIsReservedForEdges();
 if (key.isEmpty())
  throw ExceptionFactory.propertyKeyCanNotBeEmpty();
}

Solution : run the next query in orientdb:
alter database custom standardElementConstraints=false
