# The Creation Process: 

- Analyzing: A script in IQ will be saved as a stored procedure and run as a scheduled job every night (approx. midnight), to get the latest changes from the immigration data model and compare it to the people data. 

- In this solution, we are using the people table which is a static table. In the creation process, we are creating a view that joins the matching records between the passport and the existing person records. 

- Updating: The script will update views and tables with the relevant new immigration data. 

- Creating new DMs: On top of the new tables, new data models will be configured 

- One data model for the creation of passports. 

- A second data model for the creation of relations between passports and persons. 

- Creating new entities, relation and index to federated search: The indexing service will be configured to run one time each day and create or update entities and relations from the new data models. 

- The client can expect to see the new/ updated passport entity, and the update on the federated search as well - on the day after the record was inserted into the main immigration table. 

- Seeing the relation between the new passport entity and the person entity will be available 2 days after the record was inserted into the main immigration table. 



![Screenshot 2023-08-23 173009.png](/.attachments/Screenshot%202023-08-23%20173009-12425581-a523-49bd-9711-ef1559311d3c.png)





# STEP BY STEP INSTRUCTION FOR THE CHANGE 

Creating new Views: 

Immigration_Clean 

Immigration_Clean_People 

Creating new Table: 

Passports_Creation 

Passport_Relation 

Create IQ Stored Procedure: PassportsStoredProcedure 

Scheduled Job Name: PassportsScheduledEvent 



# Passport Creation tables in Isuzu

**[DBA].Immigration_Clean** - A clean immigration table, without any special characters on the document number and the names

**[DBA].Immigration_Clean_People** - A view with all the columns of the passport entity, that was created from [DBA].Immigration_Clean and [DBA].people, it compares the first and last names and the date of birth of a certain person to see if it exists on both and only if those 3 terms happen it will appear on the view

**[DBA].Passports_Creation** - A table the selects all columns from [DBA].Immigration_Clean_People but only the latest appearance of a document_number by the Sys_LastUpdatedOn column. This table creates the passport entities at the final stage

**[DBA].Passport_Relation** - A table with document_number, PersonId and Sys_LastUpdatedOn columns. This table exists to create the relation between the passport entity to the person entity

**PassportsStoredProcedure()** - A procedure that creates those tables and views

**PassportsScheduledEvent** - An event that call the PassportsStoredProcedure() procedure every day at the same time

To see info regarding the event you can use the following query:

SELECT * FROM SYSSCHEDULE WHERE sched_name = 'PassportsScheduledEvent';



# ROLLBACK PROCEDURE 

Stop the scheduled job by running the following command: 

Drop EVENT PassportsScheduledEvent 

Verify event was deleted by running the following query to see all scheduled events in the environment.  

SELECT * FROM SYSSCHEDULE; 