[[_TOC_]]


![image.png](/.attachments/image-a8ffae1f-6224-4c72-813f-f78906bd4d63.png)

# 1.0 Cellebrite Enrichment - Online Station
The Cellebrite Enrichment solution can be installed on a remote station or on an external Network location (like GFE Kiosk) and considered as an external application, not operated by IntSight (or Argus).
The Enrichment app runs by an EXE file, usually located at:

_C:\Program Files\TA9\CellebriteEnrichment\CellebriteEnrichment.exe_

When the process starts running, these folders are created in this path.

![image.png](/.attachments/image-7991f835-8dfa-4594-822f-28196b71bc8f.png)

- **Fail folder** - Files that were filed during the process are moved here.
- **Processed folder** - The original zip file is moved here upon finishing processing the file.
- **Success folder** - The processed Zip file, which includes the data about all the images and documents, is moved here.

##1.1 Enrichment Service
NOTE: the station running the enrichment service must be connected to the internet!

The Enrichment Engine IntSight Use is "Azure Cognitive Services".
In the enrichment Process, we enrich 2 types of Data:

-	Images: Extracting the image “tags” and “description" 
o	 Supported formats: JPEG, PNG, GIF, BMP
o	 File size:  up to 4MB, 200x200 px + 1MB Min	
-	Documents: Translation to English, from Greek/French

Sample:
https://portal.vision.cognitive.azure.com/demo/generic-image-tagging
https://portal.vision.cognitive.azure.com/demo/image-captioning

###1.1.1 Enrichment Account
The Credentials of the paid account should be handled in the following Configuration file:
@<3585AC8E-336A-663D-99E5-8FFAB1BA592C> Please Add the details on how to update the enrichment account

Sample Ticket:
https://dev.azure.com/ta-9/Argus/_workitems/edit/42611


##1.2 Enrichment Process 

In order to initiate the process, just move a zip file to the folder, and it will start the process, it will look like that:

![image.png](/.attachments/image-80619daf-6ad9-487c-afe7-a20d5ad58ccf.png)

The process should take several minutes for small files (under 100 MB) and can take longer for larger files (depending on the File size, and upload/download speed) - No exact timeframe can be determined.


After finishing, the main folder will look the same, with Fail, Processed, and Success folders.
Inside the Processed folder:

![image.png](/.attachments/image-41d0fc7c-4ab2-46f9-b6a9-8305126fbf6f.png)

Inside Success folder: 

![image.png](/.attachments/image-5cd6ed36-f13e-4959-ba59-fdc51b316d48.png)

And now to another example,
The inside of the Zip file looks like that: 

![image.png](/.attachments/image-7c9416cf-fff2-44ae-99d2-de6683ed59bf.png)

"Cellbrite" folder includes all the original files and folders as they were.
In this example, the original Zip file included just a folder named "Cellbrit" and all the content was inside of it.
"TA9" folder includes all the processed azure documents, a log file, and two CSV files which include all the details about the images and documents.

![image.png](/.attachments/image-76280652-a5a8-4bf3-b482-aca46f51ef8f.png)

You can see inside the "TA9" folder there's another folder named "Cellbrit": This folder includes the same folder tree as in the original "Cellbrit" folder, but inside there are the Extracted and Translated files, like here:

![image.png](/.attachments/image-2b08dbb7-7c71-417f-8d52-a30e00f4117a.png)

‎
The enriched file(s) can then be taken to the next station of the process.

## 1.3 Enrichment Logs
- For Every Cellebrite file being enriched – a dedicated log file is created in the Cellebrite Enrichment>Logs folder.
- Each log file name = the **Cellebrite file name**.
- The log file “create Date” indicates the exact timestamp that the enrichment process started, So it's not written inside the log itself
- When a Cellebrite file has finished the process, it goes into the F/S folders accordingly, indicating that the enrichment process has ended. (File in the “Process” folder is still in process)
- Error logs for the enrichment process are written inside the unique log files.

# 2.0 Cadillac Parsers - TA9 Station
## 2.1 Load Automatically - Autoloaders
Placing the enriched Zip file in the Auto-Loader folder takes the zip and creates multiple CSV files, which go to other auto-loaders and then upload the data and files to the system.

All the paths are configurable.

Put the Zip file from the success folder: **C:\CellebriteEnrichmentFiles\Success** -> in the summary folder: **\\10.100.102.95\centos\loader\Cellebrite\Summary**
The process should be between 5 to 10 minutes.

![image.png](/.attachments/image-bada4b39-8546-474f-a6d1-8d2ae41edf73.png)

## 2.2 Loading Large Cellebrite Files
Since 3.5 IntSight Supports load file loading, for Zip files bigger than what the browser can support. 
In order to configure such a feature - see the following wiki:
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/562/Upload-large-files

# 3.0 Troubleshooting
## 3.1 Formats
Cellebrite Files can arrive in different formats and languages. For a cellbrite file to load successfully, it should match the Format given in the design in terms of language and Structure.

Isuzu Design File (French Language):
https://ta9comp.sharepoint.com/:x:/r/sites/businessteam/Shared%20Documents/Projects/Isuzu/Cellebrite/Cellebrite%20Design%20-%20New.xlsx?d=wc8486c6c5ade4e17abff13195dd64d12&csf=1&web=1&e=iQeQtJ 

Cadillac Design File (English Language):
https://ta9comp.sharepoint.com/:x:/r/sites/businessteam/Shared%20Documents/Projects/Cadillac/Data%20Samples/Cellebrite/DM%20Design.xlsx?d=w9796e2ca4eed4891a0da4c4060c07881&csf=1&web=1&e=t1v3p7

in V3.9 additional improvements were done on the Cellebrite file:
- Not fail the files if the format is different (different fields in the XL)
- Remove the "+" symbol from phone numbers MSISDN


## 3.2 Enrichment
The Enrichment Flow is Necessary in order to successfully load a file with Images and Documents.
After 3.9 - The cellebrite parsers support loading without enrichment.

## 3.3 Loading Methods
When a Cellebrite file fails to load, turn to the Event Viewer and look for related relevant errors, in order to identify the cause. Also, you can make sure that the following criteria were met:
- The loaded Cellebrite file must be in a "Zip" File 
- The Zip must contain the word "Report"/"Rapport" as part of the main XL File Name. This is used in the loading process to identify the main XL file with all the data and tabs
- When loaded manually - The Data model "Summary" must be selected with the "Summary" parser (Format)
- When Loaded Automatically, the cellebrite is loaded to the "General" case
- When loaded via "large files" configuration, the Zip file must be dropped in the pre-configured folder, and the data model and parser should be selected by default

## 3.4 File Name Length
The Cellebrite file name generated is usually long. It contains the following:
- Time stamp of enrichment
- Time Stamp of Parsing
- Extraction ID

All these are added to the file name, and can cause the file to fail loading if the Actual zip name, of folder path to reach over the .Net limitation of allowed supported file name length which is 260 notes.

**For Example:**
_E:\TA9\Cellebrite\ExtractedZips\Mass Storage Device_USB Drive 2022-11-25 08-14-33 2022-11-25 10-43-40 - 13528293-870B-43BE-A361-86DE0C396083\TA9\Mass Storage Device_USB Drive\files\Document\_ _________ _________ ___________ ___ __ _____ _________ ____ _______________ _ News.pdf.extracted.txt'_

To support that the user may choose to:
- Reconfigure the Cellebrite folders to contain the minimal possible path like: C:\C\
- Remove the Enrichment Date time stamp after the file was enriched (Also handled withing the code of the parser in the following ticket:
https://dev.azure.com/ta-9/Argus/_workitems/edit/46129
