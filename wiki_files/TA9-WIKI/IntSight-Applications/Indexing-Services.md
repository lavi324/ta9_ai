[[_TOC_]]
#Summary
Indexing Service is responsible for indexing the system's data. It can index both data models and entities.
The indexed data is stored in the Free Text Repository (also called core in Solr) and therefore accessible via the Federated Search component of the Web Client.

#To read on how the indexing service create entities from a DM (SQL)
[Creating Entities from a Data Model (SQL)](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/608/Creating-Entities-from-a-Data-Model-(SQL))

#Prerequisites for indexing
So, what is needed in order to index?
We must assure the next conditions apply for each data models we are trying to index
1. Unique ID - the ID field must be unique, otherwise, we won't index rows with the same ID. In case there is no unique field and the DM is managed -> needs to create an Auto-Increment numeric field.
2. Sequence Date - this date must be incremental date, which means this DM won't have new rows with date before the current last date. this will ensure we won't skip indexing data. In case there is no unique field and the DM is managed -> needs to create an insertion date column which its default value will be the current timestamp.

##Tips and tricks
- Check date variance - very important before doing migration to check what are the shared date-time between results to understand if we might skip some results in case the indexing service will throw errors.
e.g. select date_col, count(date_col) as c from table group by date_col having c > 1 order by c desc
this query will give us more information about the date-time variance between the results.
- Index on date sequence field - make sure the date column has index since the indexed query will perform a greater than (>) query and the query must be efficient otherwise we will encounter timeout exceptions.
- Try to set a field as Display Title since this value will be the federated result title. otherwise, the result title will be empty.


#How it should look and be defined

- Here we see `dataschema1` table and here we need to make sure the data model is present, The `DBTableName` is correct and that the `ConnectionID` is pointed to the right source, but most importantly, that `IsIndexToFederatedSearch` is set to `1`.

![image.png](/.attachments/image-78cf286e-d227-415a-b4b4-42cb74525fd8.png)

- On `dataschemafields1`, As mentioned above, we need Id and Date in order to index.
Id and Date must be query-able and visible. set to `IsQueryable = 1` and their field visibility set to `|2|6|`.
Id should have `1` in `IsID` column.
Date should have `9` (SequenceDate) in `FieldRole` column.
NO OTHER FIELD should have these values.

- All the fields we want to index should be set to `IsFreeTextSearch = 1` and also be (of course) valid, 
via `IsValid = 1`.

![image.png](/.attachments/image-2273d2d7-ac74-4f35-afe5-501212a029bc.png)

#Relevant tables

We have quite a few: `dataschema1`, `dataschemafields1`, `dataconnectionsmanager`, `indexing_audit`, `indexing_deletions`, `indexing_sources`, `indexing_sources_stores`, `indexing_deletion_view`, `indexing_sources_stores_view` and `indexing_sources_view`.

`dataschema1` and `dataschemafields1` were covered before.

`dataconnectionsmanager` - Make sure the connection to the cores are present and are right. In this case, its the connection for freetextindex Core on Solr.
You need to also make sure the Data Model is mapped to its relevant data connection in here.

![image.png](/.attachments/image-0546e070-e428-44f1-ad9d-8ed29705b896.png)

- `indexing_audit` - Where everything going on. Every transaction in the process is written as a row here.
A good way to search the latest actions on a certain data model would be `SELECT * FROM sqlite_metadata.indexing_audit where INDEX_SOURCE_ID = XXX order by id desc;`

![image.png](/.attachments/image-f420b37f-a901-47a9-b8c1-aacc7f19cd48.png)

In the picture we can see that 3 actions happened. 24 Items had `NULL` date and did not index at all.
Then, 100,000 items were brought and successfully stored.
Next, 20870 items were brought and successfully stored. We can guess quite correctly that the `PageSize` is 100,000 and since there were less items than the `PageSize`, A new date has been set in `INDEX_TIME`.
This means that only items with a bigger date than this one will be indexed from now on.
Next we can see rows that has 0 items that were fetched, `-1` on `INDEX_SOURCE_STORE_ID` and no Errors. This is okay and says that no new items were found to be indexed.

`ID` - Incremental id for each row.
`CREATED_ON` - When the action occurred.
`INDEX_TIME` - What time was indexed. Starting with Null times at first, then going into 1.1.1970 as a the earliest available time and then continuing with this time until a new date arrives.
`INDEX_SOURCE_STORE_ID` - Suppose to be the Data Model id, if its `-1` it means that no items were indexed at this row.
`INDEX_SOURCE_ID` - The DM id that we're trying to index.
`INDEXING_PERIOD_TOTAL` - How much time fetching the items and storing them took, in seconds.
`IS_ERROR` - 0 is no error, 1 is an error.
`ERROR_DESCRIPTION` -If its `1`, the description will be written here.
`FETCH_PERIOD` - How much time it took to fetch the items from source.
`STORE_PERIOD` - How much time it took to store the item on target.
`ITEMS_COUNT` - How many items were actually were successfully stored.
`ITEMS_FETCHED` - Also `PageSize` from `dataschema1`. How many items were brought from source.

`ITEMS_FETCHED` and `ITEMS_COUNT` can be different in quantity as sometimes not all items that were fetched contain all the required data to be indexed. More on that on the troubleshooting page.

- `indexing_deletions` - TODO

![image.png](/.attachments/image-21e78b45-898c-4b94-b447-98d4970bd85a.png)

`id` - 
`delete_by_type` - 
`property_name` - 
`property_value` - 
`update_date` - 
`create_date` - 
`create_by` - 
`is_deleted` -

- `indexing_sources` - There are default items being indexed automatically to federated after they are uploaded to the system, and they are Entities and Media.
Do Not add anything to this table. Instead, Use the view by the same name to see all the data models being indexed.

![image.png](/.attachments/image-8d88e621-bf66-4357-a0a4-b0829e0339d7.png)

`ID` - Data Model Id.
`DATA_SOURCE_TYPE` - What is being indexed.
`CONNECTION_ID` - TODO why is that 0?
`INDEXING_INTERVAL` - Interval in seconds.
`DESCRIPTION` - Self explanatory.
`IS_ACTIVE` - Self explanatory.
`BULK_COUNT` - `PageSize`...

- `indexing_sources_stores` - Where Items are stored. 

![image.png](/.attachments/image-443e66d3-1654-40af-b97e-3d1776c2da45.png)

`SOURCE_STORE_ID`- TODO
`SOURCE_ID` - Data Model Id
`MORE_INFO` - TODO
`STORE_TYPE` - TODO
`STORE_CONNECTION_ID` - Where the items are going to be stored. -100 is generally Solr's FreeText Core.
`STORE_CONNECTION_IS_ENDPOINT` - TODO
`IDENTIFIERS_MAPPINGS_LIST` - TODO - why it is needed.
`STORE_BULK_COUNT` - How many to store in each iteration.

- `indexing_deletion_view` - TODO

- `indexing_sources_stores_view` - Adds the Data Models to the table related to it.

- `indexing_sources_view` - Again, Adds the Data Models to the table related to it.
