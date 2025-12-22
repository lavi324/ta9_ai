Servers:
DIG-MYSQL.dij.ivory.local – 192.168.3.30  
DIG-SOLR.dij.ivory.local – 192.168.3.31  
DIG-WILDFLY.dij.ivory.local – 192.168.3.32  
DIG-TA9APP.dij.ivory.local – 192.168.3.33 

TA9 Version: 3.6.1 
Environment name (domainURL): archive.dij.ivory.local

-------
The "ScannedLobs" Parser is located at (DIJ Server):
`D:\TA9\C#\TA9 Core Services\Plugins\parsers`

The "ScannedLobs" Parser is located at (DITT Server):
\\dicdrsrv01\ScanResults\s

The configuration file "ScannedJobsParserConfig.json" is located at:
`C:\Windows\System32`
And needs to be changed according to the server is located at (IP):
![image.png](/.attachments/image-7dbd8f2a-936f-4b3f-ae63-46d11f38cbdc.png)

The path to drop the XML and PDF files to ARCHIVE (from ABBY):
`\\192.168.3.33\ScanResults`

XML files will be tunneled into the “s” or “f” folders, if the process succeeded or failed, accordingly:
![image.png](/.attachments/image-6ada44f3-10b3-46a8-a136-8e03f5138e6a.png)

The PDF can be searched in FS with the file name and content:
![image.png](/.attachments/image-772096b0-36c1-4eb3-87a9-00eaea4c95ee.png)

The path to load HORA data:  
Hotel Data:  `192.168.3.33\D:\TA9\upload\Registration` 
Validation Data: `192.168.3.33\D:\TA9\upload\validation` 
Pictures: `192.168.3.33\G:\Hora`

## CONFIGURATION:

* All other TA9 modules are disabled -
"tills" table in MySQL (deleted the rows that are not relevant for the environment):
![image.png](/.attachments/image-e14a258e-2a93-40db-9bc4-820adfde8818.png)

* After login the first page is Federated Search and not the regular portal:![image.png](/.attachments/image-2935d3cc-d0a2-4485-b6a7-baf87e661825.png)

* Two main Pages are FS and DM. DM presents only Archive documents and Hora documents:
![image.png](/.attachments/image-276b46c5-a153-446e-b144-30331bc7382b.png)

* “XML Scanned Jobs” Parser V1.0:

* In DM documents, need to configure a viewer on the URL column. so we can see the file attached through the documents DM.
 
## FACETS:
1. AB (Location)
2. Department
3. Plaignant
4. Date de referance

Facets for the search are in Documents tab in FS:
![image.png](/.attachments/image-d728a15f-1885-4c55-a5b4-ee09300329aa.png)

## KEY WORDS: (For specific search)
1. ID Service
2. District - Region
3. Object
4. Date de reference
5. AFF (Person Name)
6. Date de naissance AFF
7. AB (Location)

Configured in "dataschemafields1":
![image.png](/.attachments/image-1df1f446-5193-49bb-9e8f-b69b8ad294db.png)

All PDF is stored in "Archive" DM (Documents):
![image.png](/.attachments/image-00bd445f-58a8-4539-be82-a5b32dcb5026.png)
Document field contains a view of the PDF.

All Hora data is stored in the Hora DM (which is a view table for both data and approval tables):
![image.png](/.attachments/image-6679b604-7c9a-425f-b10d-48d1bada77bf.png)

--------

Hora wiki: https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/659/Hora