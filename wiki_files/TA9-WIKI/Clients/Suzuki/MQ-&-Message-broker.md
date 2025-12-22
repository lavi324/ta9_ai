# Background
The MQ code bridge between the events arriving from the client to TA9, transforms the event messages to incidents.
we will deliver the NQ code to be under ST responsibility, in case of any change is required in the content of the message.



1.  Reductant – content that changes to "reductant" will have no impact since we take only relevant fields. We can define the redacted fields as hidden.

2.  Changes to the Service ID – changes will be implemented by client in 2 aspects – configuration and message broker code. There is no additional impact on the platform:  
*   **Configuration** - there is documentation on how to implement the changes, so the client can update the configuration once there is a change (for the icons, for example).
*   **Message broker (code changes)** – The Message broker takes the message and changes it to events in the system.
    *   the client will need to add support in the code for the new mapping. This is a code change that can be done by ST once you receive the code from us.
    *   Existing events – to keep the old ones with the old format and add the new ones. Since every event has a different mapping, you will need to update the message broker code for the new IDs.

## Configuration change
* To change event ID , add a new row in messageType.java with updated event ID - **Do not delete the old one row**

![image.png](/.attachments/image-e6261c2c-66b1-4c0b-9194-acf19b1ae427.png)



## Code shared and documentation
- [MQ](https://ta9comp.sharepoint.com/:f:/r/sites/businessteam/Shared%20Documents/Projects/Suzuki/FOC/MQ?csf=1&web=1&e=jkuv5j)

- configuration session - https://ta9comp.sharepoint.com/sites/businessteam/_layouts/15/stream.aspx?id=%2Fsites%2Fbusinessteam%2FShared%20Documents%2FProjects%2FSuzuki%2FFOC%2FMQ%2FMQ%20Configuration%20review%2D20250611%5F110644%2DMeeting%20Recording%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2Ea8c50f7c%2D95f0%2D44cd%2Dbace%2D7a608beda514

## The planned changes shared by ST
      
1.  The following event ID (service ID\subject ID) will be changed. 

| **Existing Subject ID (Event ID)**<br> | **New Subject ID (Event ID) (To be assigned)**<br> |
| --- | --- |
| 278227709<br> | New ID Will be provided<br> |
| 278227711<br> | New ID Will be provided<br> |
| 278227712<br> | New ID Will be provided<br> |
| 278227713<br> | New ID Will be provided<br> |
| 278227714<br> | New ID Will be provided<br> |
| 278227715<br> | New ID Will be provided<br> |
| 278227718<br> | New ID Will be provided<br> |
| 278227719<br> | New ID Will be provided<br> |

      

2. Only a few incident message (that is high sensitivity)  will have the following data elements masked as “Redacted”. The rest of the incident message has no change to the XML data.
In **_TABLE (A)_**, Some of the elements mentioned in column “**Data Elements Masked as "Redacted"** has child xml fields. Those child xml fields will be removed and masked as “Redacted”. See **_Table (B_)** for example.
Reattached the sample incident file for event ID 278227709 and 278227711.

      
**_TABLE (A):_**
      
| **S/No**<br> | **Message**<br> | **Existing**<br>**Subject ID**<br> | **New Subject ID**<br>**(To be assigned)**<br> | **Data Elements Masked as "Redacted"**<br> | **Note**<br> | **Example**<br> |
| --- | --- | --- | --- | --- | --- | --- |
| 1.        <br> | Incident Report<br> | 278227709<br> | New ID Will be provided<br> | 1.IncidentLocationAddress  <br>3.SubscriberDetails  <br>4.CallerDetails  <br>5.EventLogIncidentText  <br>6.AttachmentFileName<br>7.IncidentAttachment<br>8.AttachmentContent  <br>9.IncidentLocationLongitude<br>10.IncidentLocationLatitude<br>11. HistoryIncidentLocation. AddressInfo<br> | IncidentLocationLongitude and latitude will be masked as 0 .<br> | See TABLE (B)<br><br><br> |
| 2.        <br> | Incident Details Update<br> | 278227711<br> | New ID Will be provided<br> | 1. IncidentLocationAddress  <br>3. EventLogIncidentText  <br>4. IncidentLocationLongitude<br>5. IncidentLocationLatitude  <br>6. All fields label under      (IncidentLocationDetails)   <br>7. All fields label under     (AddressInfo)  <br>8. AttachmentFileName<br>9. AttachmentContent<br>10.IncidentAttachment<br>11. IncidentLocation<br>12. IncidentEventLog<br> | IncidentLocationLongitude and latitude will be masked as 0 . <br> | See Table (B)<br> |
| 3.        <br> | Dispatch Order<br> | 278227712<br> | New ID Will be provided<br> | 2.IncidentLocationAddress<br> | All fields label under:<br>AddressInfo<br>Data will not be sent<br> | <br><br> |
| 4.        <br> | Resource Status Update<br> | 278227713<br> | New ID Will be provided<br> | All field will be shown as normal (no mask)<br> | <br><br> | <br><br> |
| 5.        <br> | Close Incident<br> | 278227714<br> | New ID Will be provided<br> | All field will be shown as normal (no mask)<br> | <br><br> | <br><br> |
| 6.        <br> | Reopen Incident<br> | 278227715<br> | New ID Will be provided<br> | All field will be shown as normal (no mask)<br> | <br><br> | <br><br> |
| 7.<br> | Report Person Information<br><br><br> | 278227718<br><br><br> | New ID Will be provided<br> | 1.ReportedName<br><br><br> | All fields label under:<br>    a. PersonInfo,<br>    b. CompanyInfo,<br>    c. AdditionalInfo<br>    d. ArrestInfo<br>    e. TransportInfo<br>    f. NOKInfo<br>    g. AddressInfo<br>    h. OffenceCode<br>Data will not be sent<br> | <br><br> |
| 8.<br> | Summary Report for CAMS<br><br><br> | 278227719<br><br><br> | New ID Will be provided<br> | 1.CAMSReportLocationAddress<br><br><br> | All fields label under:<br>CAMSReportLocationAddress<br>Data will not be sent<br> | <br><br> |
| <br><br> | <br><br> | <br><br> | <br><br> | <br><br> | <br><br> | <br><br> |


      

**_TABLE (B): Example of xml element with child elements_**
| **Msg Servie ID**<br> | **Current XML field**<br> | **Masked XML field (for some incident only)**<br> |
| --- | --- | --- |
| 278227709<br> | <cub:IncidentLocationAddress>  <br>   <cub:AddressInfo>  <br>      <cub:AddressType></cub:AddressType>  <br>      <cub:AddressBlockHouseNo>12</cub:AddressBlockHouseNo>  <br>      <cub:AddressStreetName>Bishan st 1</cub:AddressStreetName>  <br>      <cub:AddressFloorNo>12</cub:AddressFloorNo>  <br>      <cub:AddressUnitNo>02-200</cub:AddressUnitNo>  <br>      <cub:AddressPostalCode>123123</cub:AddressPostalCode>  <br>      <cub:AddressBuildingName></cub:AddressBuildingName>  <br>      <cub:AddressLocationRemarks></cub:AddressLocationRemarks>  <br>   </cub:AddressInfo>  <br></cub:IncidentLocationAddress><br> | <cub:IncidentLocationAddress>  <br>Redacted  <br></cub:IncidentLocationAddress><br> |
| 278227709<br> | <cub:HistoryIncidentLocation><br>   <cub:AddressInfo>  <br>      <cub:AddressType></cub:AddressType>  <br>      <cub:AddressBlockHouseNo>12</cub:AddressBlockHouseNo>  <br>      <cub:AddressStreetName>Bishan st 1</cub:AddressStreetName>  <br>      <cub:AddressFloorNo>12</cub:AddressFloorNo>  <br>      <cub:AddressUnitNo>02-200</cub:AddressUnitNo>  <br>      <cub:AddressPostalCode>123123</cub:AddressPostalCode>  <br>      <cub:AddressBuildingName></cub:AddressBuildingName>  <br>      <cub:AddressLocationRemarks></cub:AddressLocationRemarks>  <br>   </cub:AddressInfo>  <br></cub:HistoryIncidentLocation><br> | <cub:HistoryIncidentLocation>  <br>Redacted  <br></cub:HistoryIncidentLocation><br> |
| 278227709<br> | <cub:SubscriberDetails>  <br>   <cub:SubscriberInfo>  <br>       <cub:SubscriberContactPhoneNo>97654324</cub:SubscriberContactPhoneNo>  <br>      <cub:SubscriberPhoneTypeCode></cub:SubscriberPhoneTypeCode>  <br>   </cub:SubscriberInfo>  <br></cub:SubscriberDetails><br> | <cub:SubscriberDetails>  <br>Redacted  <br></cub:SubscriberDetails><br> |
| 278227709<br> | <cub:CallerDetails>  <br>   <cub:CallerName>Ken Lee</cub:CallerName>  <br>   <cub:CallerContactPhoneNo>97878891</cub:CallerContactPhoneNo>  <br>    <cub:CallerLanguageSpoken>EL</cub:CallerLanguageSpoken>  <br></cub:CallerDetails><br> | <cub:CallerDetails>  <br>Redacted  <br></cub:CallerDetails><br> |
| 278227711<br> | <cub:IncidentAttachment>  <br>   <cub:AttachmentInfo>  <br>      <cub:AttachmentFileName>crime_face.png</cub:AttachmentFileName>  <br>      <cub:AttachmentContent>sdfjhdjsfhjdeurtre..</cub:AttachmentContent>  <br>   </cub:AttachmentInfo>  <br></cub:IncidentAttachment><br> | <cub:IncidentAttachment>  <br>Redacted  <br></cub:IncidentAttachment><br> |

