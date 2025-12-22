[[_TOC_]]

#search relations between DataBases MySQL to SAP IQ.

## how to search relations


## MySQL
1. open MySQL Workbanch
2. look for table : dataconnectionmanager: 
SELECT * FROM sqlite_metadata.dataconnectionsmanager;
3. Filter th result in dsn 

![image.png](/.attachments/image-890d8901-c3a1-4aa2-9682-e274f5a76821.png)

keep in mind the connection ID ww wiill need it later on.

1.  go to datascheme1
SELECT * FROM sqlite_metadata.dataschema1 where ConnectionID = ;
2. filter the results by this command. 
3 . edit the command according to your connection ID number. 


