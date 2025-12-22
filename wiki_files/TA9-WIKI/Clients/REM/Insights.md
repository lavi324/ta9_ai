[[_TOC_]]

# Introduction

The Insights appears after searching on data model. To see the Insights click on the icon in the tool bar.

![image.png](/.attachments/image-17dfeecc-9bd2-43cc-8a6b-d6167937cddc.png)

**There are two Insight:**


1.EntityInsight- Shows insights on specific entities with specific relation based on identifier that appears in the data model.

There are three degrees of severity:
Low    
Medium
High

![image.png](/.attachments/image-23174bd9-85b1-4a38-a824-32c83ffdc9cc.png)

![image.png](/.attachments/image-1f07d85f-591a-4726-bc0e-5d56e1de7ac2.png)

2.IdentifierInsight-Shows insights on data in the data model that appears in the second data model with the same specific identifier. 

![image.png](/.attachments/image-1befc0df-31e2-4f1b-a021-f5bad7556dd2.png)

# How to install the Insight 

1.Put the DLLs EntityInsight.dll and IdentifierInsight.dll in this path: 
**C:\Program Files\TA9\C#\TA9 Core Services\Plugins\Insights**.

![image.png](/.attachments/image-43737f6a-a3f2-485e-93c1-b17b294c20b0.png)

2. Copy & Paste the relevant DLL files into another folder
Copy 3 files from the `C:\Program Files\TA9\C#\TA9 Core Services\Services\Reports.Service` folder:
           - Utils.DatsBase.dll
           - Utils.DatsBase.config
           - Utils.DatsBase.pdb
![image.png](/.attachments/image-b9646763-092d-4f36-803a-edfdfc88f07a.png)
Paste those 3 files into the `C:\Program Files\TA9\C#\TA9 Core Services` folder:
![image.png](/.attachments/image-4cff7a1e-3a99-465d-8478-3e949feb26dd.png)
3. Configutation
Put the config files EntityInsight.json and IdentifierInsight.json in **C:\TAConfig\Insights** .

![image.png](/.attachments/image-a8250bed-f43b-4df5-8a15-cc8873b2b6b9.png)

## The configuration files - Legend

**EntityInsight.json**
|  |  |
|--|--|
|DMs| The data models that the insight work on . |
|EntitiesRelations  | The entity types and the relations that the insight based on. |
|identifierTypeID| The identifiers ID that the insight based on. |
| reportPage | part of the URL of the page , no need to change.  |
| insightName | The insight name that appears in the system. ![image.png](/.attachments/image-94611096-4549-4bd3-91c1-ae5b92f4080d.png) |
| insightTitle | The title that appears in the system. ![image.png](/.attachments/image-4fb5da98-b162-465c-8177-0d9ddbb81e86.png)  |
|insightTextLow ,insightTextMedium ,insightTextHigh | The text that appear on Low/Medium/High severity in the system. exemple of high severity :![image.png](/.attachments/image-cdf07179-5d0d-4851-90ac-2cd221da7855.png) |
| MySql Connection | connection to the mysql of the environment. **Note!** the passwords should be encrypt.  |
| Orient Connection | connection to the orient of the environment.**Note!** the passwords should be encrypt.  |

**IdentifierInsight.json**
|  |  |
|--|--|
| dm1ID , dm1Table |The first data model that the insight work on and his table name on the data base .  |
| dm2ID , dm2Table | The second data model that the insight work on and his table name on the data base . |
| identifierTypeID | The identifiers ID that the insight based on. |
| authenticationService | The url to the authenticationService  (change just the IP of the environment)  |
| metaDataService | The url to the metaDataService (change just the IP of the environment) |
| reportService | part of the URL of the page , no need to change. |
| password , user | user name and password to the system   |
| insightTitle1,insightTitle2 |  The title that appears in the system (insightTitle1-datamodel 1, insightTitle2-datamodel 2) ![image.png](/.attachments/image-c01c85ab-7f98-46c5-8e8d-766f24c4ce49.png) |
| insightText1,insightText2 | The text that appears in the system (insightText1-datamodel 1, insightText2 -datamodel 2) ![image.png](/.attachments/image-0da932bb-9763-49f6-847c-f294bd819164.png) |
| MySql Connection | connection to the mysql of the environment. **Note!** the passwords should be encrypt.**Note!** the passwords should be encrypt. |
| insightName | The insight name that appears in the system. ![image.png](/.attachments/image-cd6f18d8-c401-4925-80f9-59654bcf6fce.png) |



# Design

https://ta9comp.sharepoint.com/:w:/r/sites/businessteam/Shared%20Documents/Projects/REM/%D7%90%D7%99%D7%A4%D7%99%D7%95%D7%A0%D7%99%D7%9D/PS%20Design/%D7%90%D7%99%D7%A0%D7%A1%D7%99%D7%99%D7%98%20%D7%9E%D7%95%D7%93%D7%9C%20%D7%A1%D7%9E%D7%99%D7%9D.docx?d=w60fbd38add7d456196bb034545b9a518&csf=1&web=1&e=HewWzs

