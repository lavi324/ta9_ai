[[_TOC_]]

#Summary
1. The Entities Service is responsible for all the data operations upon the Graph Repository of the system.
2. The Graph Repository stores all the entities and relations of the system.
3. The Entities Service enables the CRUD operations on the entities & relation as well as the simple & complex search on them.
4. The Entities Service also enables the graph operations between the entities & relations such as shortest-path, node expansion, etc.

#Troubleshooting

##Locate the loader log
The loader is dumping all of its messages to:

1. The event viewer of the server. You can get the "Action Id" of this particular loading request. and the "Item Id" of each file that was contained in this request.
2. The loader log of the Admin-Client application. It is located under the option "File Load Manager". you can search there according to the time of this loading action and more other parameters. You can locate the requested file according to the relevant "Action Id" and "Item Id".
3. The failed rows from each file are stored on: `<<app folder>>/_FailedFiles/<<Item-ID>>.txt.`
4. Data audit can be tracked, grouped by each change-set, on the dedicated data store. (verify with the administrator)

## Data cannot be found
The message ‘Your request was sent to the server in order to import the file(s) to the system’ was shown to the user, but the data cannot be found. This issue can be caused when: 

* The process was stopped on UI -
  * Check the local Event Viewer (and log server). 

* The loader is still running - 
  * Check the loader log from time to time.

* The wildfly service is down or not responsive - 
  * Try sending a REST request to verify that the server is responsive (and restart if needed): 
  ```
  POST http://<<ip>:<<9900?>>/EntitiesServices/entities/load/KeepAlive
  ```
   * The expected response is: 
`{"code":200,"message":null,"data":true,"internalMessage":null}`

* The loader client doesn’t work against the right server.
  * Check the app.config of the TAStudio and verify the host IP of:
    `<endpoint name="AuthenticationClient" address="net.tcp://<<host>>:5000/AuthenticationService" binding="netTcp…`

* The loader client doesn’t work against the right server
  * Open the MySql data base and run the following:
  * SELECT * FROM sqlite_metadata.endpoints_manager where IsActive = 1 AND Name ='EntityRelationLoader';
  * You should get 1 row – Verify its URL.

* There was an error on server side. 
  * Check logs Wildfly, and event viewer 

## Server side input validations
Before starting the data loading, the service input is verified and validated. If any error occurred it will be written to the log. Each error has a message with info and in some cases also an error code. The major issues that can happen are:

* Error code: 740 (Wrong-Multi-Part-Input)
1. Null multipart input.
2. The multipart input contains no body-parts
3. The multipart input doesn't include a field ca 'erLoaderParam' of the loader parameters

* Error code: 720 (No-Loader-Items)
*: The multipart parameter 'erLoaderParam' contains no items to load

* Error code: 450 (General-Server-Error)
  * An unspecified error. check the error message for more info.

* Error code: 730 (No-Loader-Item)
  * A file is listed on the 'erLoaderParam' but no actual file content arrived.

* Error code: 510
  * The loader support files from type csv, xls, xlsx only. Any other type is not supported.

* Error code: 600
  * The supported items that this loader supports are Entities and relations only.

* Error code: 780, 781
  * Failed parsing a row from the file to the requested entity or relation.

* Error code: 790
  * Loading file was failed. See other log message or the loader log.

* Error code: 201
  * Loading file is done but some errors occurred. Check the log / loader log / failure files. 

## Add Or Edit Entities and Relations
* The Entity/Relation form doesn't show up
  * Make sure the entity definition exists and that the Net Services is running
* Error on saving Entity/Relation
  * Check the red error message. There might be several options:
  1. Validation Problems: Fix the error message (such as empty input for a required field)
  2. Connectivity Problem: The Orient DB or the Entities Services might be down - check and bring them up if required
