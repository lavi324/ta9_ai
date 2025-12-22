I need you to run the following query for each field which contains the entity we extract:
e.g. for REGEX_Phone_ssentity
`http://10.100.102.223:8983/solr/events/query?q=*:*&json.facet={x:'unique(REGEX_Phone_ssentity)'}&rows=0&wt=json`

and the result will look like:
 ![image.png](/.attachments/image-a3cd47a7-73f0-46b6-97b4-58b26ad4a38c.png)

The x values (last row) of each query will present the number of distinct values in a field
