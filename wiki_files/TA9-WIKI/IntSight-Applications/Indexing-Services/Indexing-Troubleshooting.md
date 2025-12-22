[[_TOC_]]


#Summary
Here we will try to troubleshoot known problems. If you encounter one that is not present here, please be kind and update the Wiki for the sake of everyone.
After following the main page for defining everything needed, most of it should work but if not, hopefully this page will help resolve your problem. YALLA INDEX!

#The Process
Indexing is a Java Service and it is independent and you can start and stop it by going to `services.msc`. If there is no need, Do not touch it.

![image.png](/.attachments/image-7db4a1b0-0e30-42c6-9c51-7a3e91698ef9.png)

The process starts by accessing the Sql data and building an Indexing Worker for each Data Model. All conditions from the [Main Page](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/38/Indexing-Services?anchor=prerequisites-for-indexing) should apply in order for a smooth process. However, life isn't what we always expect it to be:

# Indexing Troubleshooting

##Key points

- Each change you will do in the Sql Data will require a restart to the service in order to take place.
- You should make sure the process in up and running.
- You should make sure that Solr is up and running.
- Solr takes about 10 minutes to index newly inserted data
****
##Indexing Logs
The indexing service may be traced in two ways:
1. `SELECT * FROM sqlite_metadata.indexing_audit where index_source_id = XXX order by id desc` and search for errors in the `Error Description` column.

2. Actual Logs - either in 'logs' directory on the server or in Graylog Logs Server.
***
##How to Re-Index the data
1. Stop the service.
2. Go to `sqlite_metadata.indexing_audit` and after verifying the Data Model Id, use `DELETE FROM sqlite_metadata.indexing_audit where index_source_id = XXX` in order to delete the audit about the last indexing process.
**NOTE** - only do this is you know what you are doing. Do not delete data on production environment without consulting a Team - Leader.
3. Delete from Solr the indexed data. Go to `freetextindex` Core and then to `Documents` and write the following command as a Solr Command: `<delete><query>resource_name:DM_ID</query></delete>`.

![image.png](/.attachments/image-fe4feecd-086c-40e3-9088-16a5f8ac7ace.png)
******
##New Entity or Data Model is not indexed
### General steps
  * Check-in `indexing_audit` table for the last time that the service ran successfully.
  * Make sure all conditions for indexing apply for the DM.
  * Try a restart to the Indexing service if nothing seems to be working.

****
### Dates
Most commonly data will not index is because of the Date.
  * Data will not index if the value of the Date is less than 1.1.1970 00:00:00.
  * Data will not index if the value of the Date is less than the last indexed date of the Data Model in `indexing_audit`. In the next picture inserted items with date that is before `2.2.2021 at 14:49:07` will **not** be indexed.


![image.png](/.attachments/image-f25e6517-cc78-48aa-974b-3568c55f00b0.png)

****
### Lack of Data in needed fields
  * Every item that is indexed to federated has, as a basic requirement, fields that are marked as ```IsFreeTextSearch = 1``` in `dataschemafields1`.
  * In order for the item to be indexed, it must have at least one field with Data in it.
  * In case that the Data is `NULL` in those specific fields, The item will not be indexed.

* In the next picture we can see that there are 3 fields, `mcc`, `cell_name` and `operator`, that are supposed to be indexed to Federated.

![image.png](/.attachments/image-36429c2c-4e4f-4a6c-9825-dcc5131b0043.png)

* After quick check we see that the data resides on `ta9data` and we can easily check about items that will not be indexed.

![image.png](/.attachments/image-084075be-95d3-47dc-aa62-ee631c11963e.png)

* As we can tell, we expect `1,096,690` items to not be indexed.

****

### Double Definition
In some cases, `indexing_sources` may have double definitions of the same Data Model. Refer to the table\view and make sure there are no double values of the same Data Model.

****

### Views
* Its also possible that the view may be wrongly configured:

![image.png](/.attachments/image-3c137f6c-a9bb-4c0d-a794-065bd8407fc0.png)



  * Paste this script, if its not the same: 
```
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `indexing_sources_view` AS
    SELECT 
        `ind`.`ID` AS `ID`,
        `ind`.`DATA_SOURCE_TYPE` AS `DATA_SOURCE_TYPE`,
        `ind`.`IS_ACTIVE` AS `IS_ACTIVE`,
        `ind`.`BULK_COUNT` AS `BULK_COUNT`,
        `ind`.`CONNECTION_ID` AS `CONNECTION_ID`,
        `ind`.`INDEXING_INTERVAL` AS `INDEXING_INTERVAL`,
        `ind`.`DESCRIPTION` AS `DESCRIPTION`
    FROM
        `indexing_sources` `ind` 
    UNION SELECT 
        `dm`.`SchemaID` AS `ID`,
        'DataModel' AS `DATA_SOURCE_TYPE`,
        `dm`.`IsSupported` AS `IS_ACTIVE`,
        `dm`.`PageSize` AS `BULK_COUNT`,
        `dm`.`ConnectionID` AS `CONNECTION_ID`,
        600 AS `INDEXING_INTERVAL`,
        `dm`.`SchemaDescription` AS `DESCRIPTION`
    FROM
        `dataschema1` `dm`
    WHERE
        (`dm`.`IsIndexToFederatedSearch` = 1)
```

  * Check for `indexing_sources_stores_view` as well, and copy this script if its not the same:
```
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `indexing_sources_stores_view` AS
    SELECT 
        `iss`.`SOURCE_STORE_ID` AS `SOURCE_STORE_ID`,
        `iss`.`SOURCE_ID` AS `SOURCE_ID`,
        `iss`.`MORE_INFO` AS `MORE_INFO`,
        `iss`.`STORE_TYPE` AS `STORE_TYPE`,
        `iss`.`STORE_CONNECTION_ID` AS `STORE_CONNECTION_ID`,
        `iss`.`STORE_CONNECTION_IS_ENDPOINT` AS `STORE_CONNECTION_IS_ENDPOINT`,
        `iss`.`IDENTIFIERS_MAPPINGS_LIST` AS `IDENTIFIERS_MAPPINGS_LIST`,
        `iss`.`STORE_BULK_COUNT` AS `STORE_BULK_COUNT`
    FROM
        `indexing_sources_stores` `iss` 
    UNION SELECT 
        `dm`.`SchemaID` AS `SOURCE_STORE_ID`,
        `dm`.`SchemaID` AS `SOURCE_ID`,
        0 AS `MORE_INFO`,
        0 AS `STORE_TYPE`,
        (SELECT 
                `dc`.`ConnectionID`
            FROM
                `dataconnectionsmanager` `dc`
            WHERE
                ((`dc`.`ConnectionName` = 'solr')
                    AND (`dc`.`ProviderName` = 'solr'))) AS `STORE_CONNECTION_ID`,
        0 AS `STORE_CONNECTION_IS_ENDPOINT`,
        NULL AS `IDENTIFIERS_MAPPINGS_LIST`,
        1000 AS `STORE_BULK_COUNT`
    FROM
        `dataschema1` `dm`
    WHERE
        ((`dm`.`IsIndexToFederatedSearch` = 1)
            AND (`dm`.`IsSupported` = 1))
``` 

*****

###  Solr Lock
* First check that you are not running Indexing.jar while indexing service is already running in the backgroung.

![image.png](/.attachments/image-01b88a2e-1cdd-4e2a-bcc4-afcdb80ee821.png)

* Also, try to reload the collection

![image.png](/.attachments/image-b1331017-9137-46c6-b5de-ba3a155fac80.png)

*****

### Exception while trying to index - cannot change DocValues type from SORTED_SET to NUMERIC
- It can occur for any type of identifier.
- The solution sadly is to delete the whole collection.

![image.png](/.attachments/image-314b83f8-8e4f-4800-aec5-62c9a6dabe7b.png)

*****

##Connection Problems

If for some reason you encounter in Connection related error refer to these steps:
- Verify the connection is configured well in `dataconnectionsmanager`.
- Verify that the service is configured in its `service2service.props` config (Open the JAR (`Indexing.jar` file itself with 7zip, and edit according to the environment)
- Verify that the `indexing-sources` connection-reference is configured (to an existing and accessible connection)
- Verify that the `indexing-source-stores` connections are configured (to an existing and accessible connection)

****
##Federated search does not return values
* Check the service is up and running by looking at the "deployments" of the WildFly - a file named `FreeTextService.war.deployed` should appear. If it doesn't, then:
  * Create a file named `FreeTextService.war.redeploy` to trigger a deployment of the service.
* Check that the Free Text Repository Solr service is up and running - Look at the Windows Services console.
****
##The autocomplete does not retrieve matching
- Verify 'Solr' management console on <<machine-ip>>:<<port>> (the address is defined in the endpoint-manager table at MySQL DB)
- Verify that 'TA-Solr' service on the local server is running
- The autocomplete feature of the Free Text Repository requires a lot of RAM to be supplied to the Solr than the normal search.

- Moreover, in cases when not enough memory is available, the autocomplete feature is not working. A message like this usually appears: "Lookup is not supported at this time". This problem can be easily fixed by increasing the memory allocated to the Free Text Repository.
- Use the '-m' flag of the service to increase the memory allocated. Eg - '-m 6g' will allocate up to 6 GB of RAM to the Solr service.
****
## Expected mime type application/octet-stream but got text/html
- Solr DB is empty, once there will be results it will work.

*****

## Compare Items Count from `indexing_audit` to Solr
- Verify the Data Model Id and search for it by using: 
```
select sum(ITEMS_COUNT) FROM sqlite_metadata.indexing_audit where index_source_id = 1050
```
![image.png](/.attachments/image-cd40f56a-bddc-41be-bac7-6aea9ded11fd.png)

Now go to Solr and search:
```
item_type:8 AND
resource_name:1050
```
![image.png](/.attachments/image-646a4853-b79c-4ccd-b4a9-12af4bebc56a.png)

*****

## Check if Solr is up-to-date
- Log in to Solr, choose the desired core and press `Overview`. It should have a green check mark on `Current` property.
If not, Wait just a little bit longer.

![image.png](/.attachments/image-14eae7e1-f57f-40d6-9d2d-2f867050fde2.png)

#Restart Indexing Service
In cases where all services and definitions seems correct yet the data is not being indexed, The administrator can try to restart he indexing service.

If the Service is installed on the main windows machine (usually on cloud environments) restarting the indexing service is done from the "Services" window - and restarting the "TA9 Indexing Service".



If the Indexing service is on Linux, the Administrator needs to connect to the IP where the service is installed and run the restart index command (from Putty):

systemctl restart indexing.service
