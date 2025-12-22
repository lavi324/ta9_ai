##steps

1. Stop the "TA9 Indexing Service"
2. Make a backup of the Indexing.jar file (just Ctrl+c then Ctrl+v) in the Indexing Service folder, usually under "%TA9 Folder%\Java\Indexing Service"
3. Delete the Indexing.jar file
4. Transfer the new Indexing.jar file into the Indexing Service folder
5. If the new Indexing.jar file has a different name like "IndexingService-0.0.1-B31215-jar-with-dependencies.jar" just rename it to Indexing.jar
6. make sure the rabbit_mq.props and Service_2_service.props files are configured well to your environment according to step 7 and transfer them to the Indexing Service folder, usually under "%TA9 Folder%\Java\Indexing Service"
7. A. rabbit_mq.props
			I. change to rabbit url – where rabbit installed 
			II. username and password – default guest guest (Encrypted) 
	B. Service_2_service.props 
			I. Change Authenticationurl – app server url 
			II. Change Validatetolen - app server url 
			III. ServiceUser – username: serviceadmin (encrypted) 
			IV. ServicePassword – password serviceadmin password (encrypted twice)
8. Start the "TA9 Indexing Service"