[[_TOC_]]

##Introduction
When we have one "Date" column that contains date and time, we can easily split it into two columns, "Date" and "Time", from the Admin Studio.

## Definitions in the 'Admin Studio' for splitting the date column
1. Open the Admin Studio module
2. Navigate to the Data Model you would like to split its "Date" column to "Date" and "Time" columns
3. Click on the "Repository" button and make sure the 'Is Managed' definition is marked
 ![image.png](/.attachments/image-11f01882-e12e-47b6-85d0-25742484a021.png)
4. Click on the "Date" column and change its "Display Format" to be = Sort Date
![image.png](/.attachments/image-70afa0d8-31bb-48b4-b2f0-2c126412e4fc.png)
5. Add a new column by clicking on the "+" button:
![image.png](/.attachments/image-73bb4f23-bd4a-48a8-89c6-759a25108ed7.png)
6. Click on the new column name and set the following definitions:
"Data Type"  = Date Time
"Display Format" = 24 Hours
"Display Name" = can be "Time" or whatever you would like
"Field Name" = should be the exact same name that appears in the "Date" column
![image.png](/.attachments/image-85f1bd0c-32d3-4c50-8066-24989482913b.png)
7. Save the data model
8. Clear Server and Client Cache

##View data model in we client system
Log in to the system and view the columns in the data model
![image.png](/.attachments/image-0ff350e1-a1f1-4a2b-a435-98a0e47cb116.png)