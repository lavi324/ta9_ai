[[_TOC_]]

#Introduction
OrientDB is an open-source NoSQL database management system written in Java. It is a Multi-model database, supporting graph, document, key/value, and object models,[2] but the relationships are managed as in graph databases with direct connections between records. It supports schema-less, schema-full and schema-mixed modes. It has a strong security profiling system based on users and roles and supports querying with Gremlin along with SQL extended for graph traversal. OrientDB uses several indexing mechanisms based on B-tree and Extendible hashing, the last one is known as "hash index", there are plans to implement LSM-tree and Fractal tree index based indexes. Each record has Surrogate key which indicates the position of the record inside of Array list, links between records are stored either as a single value of record's position stored inside of referrer or as B-tree of record positions (so-called record IDs or RIDs) which allows fast traversal (with O(1) complexity) of one-to-many relationships and fast addition/removal of new links.

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
1. go to orient folder -> bin -> run console
2. In the console, connect to the DB, command example:   connect remote:10.100.102.234:2424/TA9/ <username> <password>
3. save a backup of the DB - EXPORT DATABASE /temp/petshop.export
4. start fix graph command - REPAIR DATABASE --fix-graph
5. you can also use check command to check is there any problems before you run the repair command: CHECK DATABASE ...

## Convert a multi-value column to single-value column
