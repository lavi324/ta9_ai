[[_TOC_]]

#Introduction
OrientDB is an open-source NoSQL database management system written in Java. It is a Multi-model database, supporting graph, document, key/value, and object models,[2] but the relationships are managed as in graph databases with direct connections between records. It supports schema-less, schema-full and schema-mixed modes. It has a strong security profiling system based on users and roles and supports querying with Gremlin along with SQL extended for graph traversal. OrientDB uses several indexing mechanisms based on B-tree and Extendible hashing, the last one is known as "hash index", there are plans to implement LSM-tree and Fractal tree index based indexes. Each record has Surrogate key which indicates the position of the record inside of Array list, links between records are stored either as a single value of record's position stored inside of referrer or as B-tree of record positions (so-called record IDs or RIDs) which allows fast traversal (with O(1) complexity) of one-to-many relationships and fast addition/removal of new links.


# Troubleshooting

## Make sure server is up and runinng

1. Open a Chrome browser
2. Navigate to 

`http://CAORISRV01.ecis.local:2480`

3. you should see this page: 
![image.png](/.attachments/image-9a0cd571-a886-495b-99bb-184b0c80c2e9.png)

### Cant see login page? 

Use Putty to ssh to the host

![image.png](/.attachments/image-f3f015bb-8a62-4569-b2a7-fb4bafe2d515.png)

Connect as ta9 user with a password that were provided to you.

Write down: 

#### Restart the service:
`sudo systemctl resart orientdb.service`

#### Check service status:
`sudo systemctl status orientdb.service`

#### Mount all external hard drive:
`sudo mount -a`

Now, go back to: 
`http://CAORISRV01.ecis.local:2480`

Test setting on TA9 app:

1. Login as admin
2. Open any entity data model
3. run a search
4. Open any entity
5. Choose an entity by clicking on the row's checkbox (In the Data model)
6. Right click on any entity
7. Click send to graph



| No. | Test | Expected Result |
|--|--|--|
| 1. | Login as admin |  |
| 2. | Open any entity data model |  |
| 3. | run a search | results should display |
| 4. | Open any entity | Entity should be opened in a new tab |
| 5. | Choose an entity by clicking on the row's checkbox (In the Data model) |  |
| 6. | Right click on any entity | Context menu will pop open |
| 7. | Click send to graph | Entity will be opened in a link analysis view, in a new tab. |



If everything as passed you are good to go. 

If any further problems please contact with support team. 



