In order to add new field to the advanced:

1.We need to identify which is the "InternalFreeText" Schema Id on dataschema1 table. In our case its -40.

`SELECT * FROM sqlite_metadata.dataschema1;`

2.Run this query : 

`SELECT * FROM sqlite_metadata.dataschemafields1 where schemaid =-40;`

3.Add new row or use this script :
schemaID =-40
fieldSize = 63
IsCubeReport = 7 
Is valid=1

**Note** if the field type is 1 (text) you should add a lookup into the field 'DataEnrichmentName'

![image.png](/.attachments/image-b735fd04-0a39-4aa3-95cb-51e64c976b63.png)

3.reset Wildly and service host.

This is how it should look like at the end

![image.png](/.attachments/image-842592a1-1438-45f8-b847-3dde043afe71.png)