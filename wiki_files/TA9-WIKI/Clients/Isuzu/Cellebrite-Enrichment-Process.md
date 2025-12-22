# Cellebrite Enrichment
[[_TOC_]]

## General Details:
Allows new forensic abilities – Cellebrite process allows to load to the system Forensic data - phone
extractions. The new feature allows to send the Cellebrite files to enrichment by the Azure services.
The Azure can add to the data

a. Document Translation to French
b. Image recognition
## The Loading Process:
The Cellebrite files will drop to the scan machine to dedicated the folder for enrichment:
Drop the file for enrichment in the scanning machine to the path:
F:\\PhoneData\CellebriteEnrichmentFiles
IP - 10.100.152.15

The translation or/and the image recognition will be added to the data. The files will return
automatically back to the scanning machine to the Cellebrite folder and will scan to the secure
environment by the original Cellebrite process.
Fail folder - Files that were failed during the process are moved here.
Success folder - The processed Zip file, which includes the data about all the images and
documents, is moved here.

![image.png](/.attachments/image-7991f835-8dfa-4594-822f-28196b71bc8f.png)

The files will arrive to the dedicated folder at the secure environment:
\\dicdrsrv01\Outgoing\AutomaticJobs\Phone Extractions
The user needs to load the data to the system (or specific case) by the Cellebrite auto loader or manually. The zip file will be separated to all Cellebrite Data models.

## Troubleshooting
Isuzu Design File (French Language):
https://ta9comp.sharepoint.com/:x:/r/sites/businessteam/Shared%20Documents/Projects/Isuzu/Cellebrite/Cellebrite%20Design%20-%20New.xlsx?d=wc8486c6c5ade4e17abff13195dd64d12&csf=1&web=1&e=iQeQtJ 

- The configuration file resides on C:\Config and named "CellebriteEnrichmentConfig.json"

## Packages Versions:
1. IKVM: 8.1.5717	
2. IKVM.OpenJDK.XML.API: 7.2.4630.5
3. IKVM.Runtime: 7.2.4630.5
4. Other IKVM packages are all version number: 8.6.2
5. CsvHelper: 30.0.1
6. ExifLib: 1.7.0
7. Both TikaOnDotnet and TikaOnDotnet.TextExtracor are version 1.17.1

