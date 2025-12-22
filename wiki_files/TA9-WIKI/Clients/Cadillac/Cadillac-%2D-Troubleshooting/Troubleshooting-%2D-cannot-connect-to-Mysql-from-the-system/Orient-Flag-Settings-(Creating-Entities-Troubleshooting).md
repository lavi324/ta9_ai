The ticket number 44576: https:won'tv.azure.com/ta-9/TA9%20Support/_workitems/edit/44576

The client tried to create an entity in 2 way:
*  Manually, and faced this error:
![image.png](/.attachments/image-e37527cb-21bb-4ae1-8f9b-de4417efc734.png)


* From a csv file, they got this error:
![image.png](/.attachments/image-85b471af-3614-4fac-b7ac-708ac6add439.png)

**Logs:**
"The description for Event ID 0 from source IntSight C# Service cannot be found. Either the component that raises this event is not installed on your local computer or the installation is corrupted. You can install or repair the component on the local computer.

If the event originated on another computer, the display information had to be saved with the event.

The following information was included with the event: 

Level: ERROR 
Domain: Reports.Service 
MachineName: CAWINSRV01 
IP: 10.100.120.80 
Client IP: :1 
Url: http://cawinsrv01.ecis.local:5480/ReportServices/InsertBulkData 
TAUser: saviaAdmin@ecis.local 
OSUSer: ta9admin 
 Class: Reports.Dal.ReportGeneralDal 
Method: InsertBulkData 
Line: 1728 
Message: An error occurred at line number: 1. With the following error message: Column 'ObjectId' cannot be null  
Exception:  

The request is not supported"


It is a matter of a field in orient named standardElementConstraints needs to be in set to "False";

Go to Orient DB, and to the DB tab:
![image.png](/.attachments/image-42eeb0b7-2185-4224-b45a-08d7c7f4ca00.png)

Open the configuration tab, and see that in custom properties you have a field named "standartElementConstrains" and that it's set to "False".

If not, run this in the compiler in the brows tab:
`alter database custom standardElementConstraints=false`
and test to see if it was set.

When this value equals True, it wont allow to uptade the delta of the object. It requires from the object's properties (every optional insert value) to be mandatory, in the UI and system fields also.
The error log was on the first value that weren't filled. 

**The reason for that** can be due to data migration or connecting to the orientDB with a third-party program or any other system change. This can cause resets to some fields, and one of them is "standardElementConstraints".

------------

You can also advise these tickets:
1. https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/509/OrientDB-Update
2. https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/46/OrientDB