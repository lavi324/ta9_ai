[[_TOC_]]


#General Description
This feature was done as part of Isuzu Phase II scope, and was meant to help investigators identify if in a CDR the phone numbers are identified as "technical" - meaning irrelevant numbers for analysis.

Usually, technical numbers are used to send commercials, and should be excluded from the data using a data model filter.


#How it works
- A new table on IQ was created called "Tech_Num"
- The list of technical numbers was populated in the table based on a script (by Aviram) - Filling it with numbers appearing over X Million times:
 https://ta9comp.sharepoint.com/:t:/r/sites/businessteam/Shared%20Documents/Projects/Isuzu/SQL%20Scripts/Subscribers%20CDR%20sql/Spam%20.txt?csf=1&web=1&e=gfLplY)

- The CDR SP validates with this table and adds it to the cdr as true/false for tech numbers

- After a file was loaded to the CDR data model - the user can filter the "Is Technical" column to "True/False" to hide the irrelevant numbers. (Also added as Query builder Filter)

#Updating the "Technical" numbers list
Any request To Add New numbers / update the list / Remove a number - will be done by TA9 by inserting it to IQ table. 
The request Should be received by a ticket to the support team.

#Screenshots
1. Query Builder:
![image.png](/.attachments/image-10e39ec2-41ab-4f8a-aad2-adbde5ce225c.png)

2. Data model Filter:
![image.png](/.attachments/image-34a86bcc-82f7-44b6-bf0e-57e451110d84.png)

Design Ticket:
https://dev.azure.com/ta-9/Argus/_workitems/edit/40489
