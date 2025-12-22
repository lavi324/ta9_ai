[[_TOC_]]

#Overview

A meeting report is a plugin that is used to understand if two phone numbers were in the same area in a specific date range.

The report queries on 2 MSISDN numbers, based on their geographical location appearing in the CDR Data model. 

#Search Criteria
- **MSISDNs** - The user has to insert 2 MSISDN numbers, separated by a comma (,). Example:  123456789,987654321 (choose Phone Identifier)
- **Meeting Duration** - Single Value selected from a lookup - Starting from 15 min, until 120 min, in 15 min increments. Representing the maximum estimated time range that both sides had used their phones.
- **Date** - A possible time frame for the meeting - If one is not chosen the default is one month back.
- **Estimated Proximity** - Single Value selected from a lookup - The maximum distance between the locations of the devices, based on the GeoHash Values appearing in the CDR Data model.

_Example:_
_A meeting was conducted between person A & Person B, on November 20/2021, at 10:00.
Person A used the phone at 10:13, and Person B at 10:45, both users were at a distance of 3 km from each other when using their phones.
The query should be as follows:_

- _Date - From November 20/2021 07:00 until November 20 12:00_
- _Meeting Duration - 45min_
- _Proximity - 5km_

The results can indicate a possible meeting, since both numbers were found in the CDR on the same date and Time range, same area (Cell proximity), and used their phones in a similar timeframe. 

##Query builder & Filter Input
To Search by phone number:  
- Choose the MSISDN Identifier. 
- Insert 2 MSISDN separated by a comma to the search.
- Click on advanced, choose meeting duration and estimated proximity from the drop-down list and click ok. 
- Click on the Search icon. 
- To change the default settings, click on advanced and choose the time frame. 


![image.png](/.attachments/image-89f6ec73-eee1-4a14-b918-f918acdc3d26.png)

![image.png](/.attachments/image-e9c08523-6e08-46ac-b1dd-8a8b9c791bdc.png)


##Reuslt Output

In the result, we get the two phone numbers, their corresponding latitude, and longitude, Date, and CGI data.

The results display all the times the searched cell phones made or received calls in the same time range and in the chosen distance between them. 

![image.png](/.attachments/image-57bcc51b-4ace-4b7c-bf9b-57782e9e180d.png)

#Prerequisites for deploy
The code is in Clients Repository and uses the `CDR` and `BTS` tables as data sources.
1. Geohash 5, 6 or 7 - in the CDR Data model. 
2. Parameters inside Query Builder: Meeting duration and estimated proximity lookups
3. Main Date definition on the plugin - as Date range column
4. Phone Identifier defined on CDR and Plugin