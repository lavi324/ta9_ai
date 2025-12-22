In order to be able to search on cases on Federated Search we need to take few steps:
1. We need to identify which is the "InternalFreeText" Schema Id on dataschema1 table. In our case its -40.
`SELECT * FROM sqlite_metadata.dataschema1;`
![cases ds1.PNG](/.attachments/cases%20ds1-6a8e833f-1864-4ebe-ae74-91b2ad67759b.PNG)
2. We need to find "permission_values" and work on that row.
`SELECT * FROM sqlite_metadata.dataschemafields1 where schemaid =-40;`
![cases dsf1.PNG](/.attachments/cases%20dsf1-9983573c-5a37-428e-b707-00534db6e4c3.PNG)
3. We can use this sql command as follows:
UPDATE `sqlite_metadata`.`dataschemafields1` SET `DisplayName`='Widgets_List_Cases', `DataEnrichmentName`='cases', `FieldSize`='63', `FieldScale`='63' WHERE `FieldID`='XXXX';
- FieldID should match the specific row as always, and not be changed by the user itself. 
- FieldSize and FieldScale are determined by this image:

![image (1).png](/.attachments/image%20(1)-4557980b-33f5-4b2a-b69d-b85946b9a453.png)
By entering X as the value we indicate that we want to search on Y parameters. Lets assume we want to search on Entity and Data model exclusivly, then we need to enter (2+8) 10 as the value, and with this special Enum there is only one possible way to achieve this value, granting us the option to control which parameters to include exactly.
By summing all the values to 63, there is only one way to sum it, and by this we indicate we want to search on everything.

4. This is how it should look like at the end![cases final_LI.jpg](/.attachments/cases%20final_LI-57e97a61-96ba-4ff0-ad2a-0cb3eb6d7204.jpg)




















































