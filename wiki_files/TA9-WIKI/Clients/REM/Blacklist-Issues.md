# **Blacklist PLA**

### **19/06/23 - Insert Bulk Data Issue:**

We had an issue in REM where Blacklist PLA didn't update the blacklist DM, although the entities were updated successfully, indicating that there is an issue with the InsertBulkData api call, which inserts a new line to blacklist DM.

In the PLA code, the InsertBulkData api call functionality was used through Argus's ReportDispatcher, which threw communication timeout exception. When attempting the same InsertBulkData api call **with the same data** from Postman, the InsertBulkData api call added a line successfully.

After checking with R&D, Argus's dispatcher throws this kind of exceptions when something goes wrong with the api call, could be anything. After a request is sent, if there is no response after a set amount of time, the user will just get that timeout exception without any indication of what went wrong with the request, not even as an inner exception.

Since on REM site we can't even debug, I decided to remove the dispatcher's InsertBulkData use from the PLA, and add a InsertBulkData api call implementation of my own. That way I could log the exception and know exactly what went wrong with the API call.

After some troubleshooting and minor code adjustment on site, InsertBulkData now work and with it the whole Blacklist PLA process.