# How to create a new core in Solr:

1. SSH to Solr machine

![image.png](/.attachments/image-cd777374-5867-4071-9fd8-0c05bd440201.png)

2. Login as a ta9 user with the password that is provided.

3. Run this command to connect to the container: 

`docker exec -it solr /bin/bash`

4. Run this command to create the new core (change 'mycore' to the name of your core): 

`bin/solr create_core -c mycore`

5. connect to the Solr through FileZilla:
Host: enter the Solr ip
enter username + password.

6. Go to the path:

`/opt/solr/server/solr` 

7. Click on the folder with the name of your new core.

![image.png](/.attachments/image-a282885b-54d9-48ab-adfb-5f1c15c7851f.png)

8. Make sure you have all the permissions in the 'manage-schema' file. 

It should look like this:

![image.png](/.attachments/image-ceb7a971-1978-4b95-96e5-254f1f5fbae4.png)

If you need to add permissions, right-click and click on "File permissions..."
Change the value to 777 and click on OK.

![image.png](/.attachments/image-518c2f87-78ed-4428-a92f-c33abb3020f0.png) 


9. Click on conf folder and open the 'manage-schema' file to edit your core's schema (add fields).
You can copy the content from the 'manage-schema' file in freetextindex folder.

10. Restart the Solr.


# How to create DM on top of Solr:

1. in MySQL open the table: connection manager.

`SELECT * FROM sqlite_metadata.dataconnectionsmanager;`

2. Add a new row in order to add a connection to the Solr core:

ProviderName: SolrNet
ConnectionString: `http://SolrIP:9500/solr/YourCoreName`
IsExternal: 0
ConnectionName: Solr
IsValid: 1
IsDefault: 0
IsRepository: 1
DBType: Solr

3. Create DM from CSV file (**Note** that the names of the fields should be the same as the fields in solr).

4. Open your DM in Mysql:

`SELECT * FROM sqlite_metadata.dataschema1 where schemaID=YourDMId;`

5. Change the fileds 'DBSchemaName' and 'DBTableName' to the name of the solr core.

6. Change the ConnectionID to the ID of the connection that you created (on Step 2)

![image.png](/.attachments/image-088539f1-7323-4994-bca2-298b4129d3d3.png)

7. Restart the service host and clear cache.