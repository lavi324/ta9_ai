# UFDR/ZIP file structure guide
Since ufdr file is constructed in specific way, custom zip files are also must be constructed like that or with a little change:
1. UFDR file it self when extracted look like that:
MYUFDR.ufdr => MYUFDR(folder) => (report.xml, files...)
![image.png](/.attachments/image-9774e559-f2c3-4a8c-9280-420fdb9a8945.png)
2. ZIP file must be same as ufdr file **or it has an option of having folder of the same name as zip file inside it so extracted version will have path of:**
![image.png](/.attachments/image-ffb6b61f-bd36-430a-a416-2577a4fca919.png)

**P.S Look at the difference between paths: one has one folder shlomi and second one two since it zip file had shlomi folder inside it the name of zip it self was shlomi.zip.**

# Settings
![image.png](/.attachments/image-d8de0b8f-8599-481d-b067-42d2a8e38eff.png)
* CellebriteFilesPath - path to cellebrite ufdr files.
* CellebriteOldFilesPath - path to old cellebrite files(xls)
* CellebriteParsersPath - path for Segments(parts of main xml) and parsed Data(json/csv) files
* UploadFilesToSeaweed - defines if files from FilesParser will be uploaded to Seaweed.
* MinFileSizeToUpload - defines minimum size of file that can be uploaded to Seaweed(FilesParser)
* MaxDegreeOfParallelism - number of threads working in parallel for one file.
* MaxRunningParsersAtTheSameTime - number of files that are being parsed at the same time.
* IsDryRun - defines if current run needs to upload parsed data files to seaweed and call to data model search UploadFiles.
* ParsersDataModels - data models ids where to upload parsed data. 
# Mapping
![image.png](/.attachments/image-bf497e03-afb9-40fa-9cf6-aac16c08707a.png)
## General settings
### IsMulti
Defines if segment of mappings consists of multiple elements that are not related to each other as Parent/Child relationship. 

P.S Don't provide if it is not Multi.

_For example:_ 
Summary mappings consists of multiple such elements "_Additional Data, Device Info and Extraction Data_"
![image.png](/.attachments/image-a756f444-750c-4c7f-8dfe-e5bc647863f7.png)

## Single row mappings:
###MainPath
It is the xml path to elements that needs to be merged into one file.

For example previous elements all have same path. _(Currently there are only support of paths that are identical_)
![image.png](/.attachments/image-35fee41e-50c5-42ca-a51d-496660f6d321.png)
## Multi row mappings
###MainPath
It is the xml path to element from which will be created smaller XML segment for specific parser.
![image.png](/.attachments/image-9fc6bae2-8c10-435b-afcb-621412720cc7.png)
![image.png](/.attachments/image-22aeeb68-1105-4254-a916-5a5d7ac42338.png)

### GroupName
It is xml path(related to it's parent) to main group of elements that have same name and based on them service will insert rows. 

_For example in Chat main element we have multiple Chat objects that will be mapped as rows in DB._

P.S Don't provide if it is single row mapping!
![image.png](/.attachments/image-b13d9604-80ac-452e-b19c-ea3d5ff083c7.png)
![image.png](/.attachments/image-fcac4c5d-8a7c-457b-8c43-84e4b4c01ebb.png)

## Single field settings:
### DestinationField
Name of the Data Model field (fieldName) where to map xml value.
### SourceField
Xml Path from where to take value. 

_**Simple mapping:**_
![image.png](/.attachments/image-430fe7ca-cfe5-40de-8610-e4e8f0615847.png)
### IsAttribute
Defines if value should be mapped from Attribute.
### AttributeName
Attribute name from which to take value.
P.S Xml path for attribute will be `"."`(If attribute value needed to be taken from descendant group member just provide [MultiGroupName](#multigroupname)). For example Chat that has id Attribute
**_Attribute mapping:_**
![image.png](/.attachments/image-f70b8741-adc6-406e-9e14-4fc916fae3b2.png)

### GroupedBy
Defines if value should be taken from descendent group member of main group.

### MultiGroupName
* Xml path to descendent group member. Each group will add new row to data by merging it's data with parent data if there are not special behavior for example like in `Chats` parser.
For example if `UserAccount` has one Entry, data will return first row with `UserAccount` data and second row with `UserAccount+Entry` data.
**_Simple group mapping example_:**
Inside UserAccount we have group field(multiModelField named Entries) so mapping of field inside one of the entries will look like this:
![image.png](/.attachments/image-0c4a4bcd-1656-4adb-983f-8f5d3e10d5fb.png)            
![image.png](/.attachments/image-d5e626df-1369-4bf2-bbd2-44f563f266e1.png)

* In some cases, such as `Chats`, we will need to do nested mapping. (Main Group > Nested Group > Next level of Nested Group). **FieldMapper** will automatically identify nested groups inside other group by it's **MultiGroupName**. As you can see in example below we have group for `InstantMessage` that is part of main group and `model` group that is part of `InstantMessage` member. The meaning in data is for each `Chat`, `mapper` will create 3 rows, 1 `Chat` row , 1 `Chat+InstantMessage` row and 1 `Chat+InstantMessage+model("Party")` row.
**_Nested group mapping example_:**
![image.png](/.attachments/image-30f99bb2-c507-4b8d-87ed-b1296523c700.png)
![image.png](/.attachments/image-2cc9d273-2a81-4424-8c2f-c21ca2a65432.png)

# Chats Parser
Chats parser it is special parser that after base FieldMapping will merge rows that represent same Chat into one row. It has multi value fields such as `{ "to_identifier", "to_phone_number", "to_name", "to_facebook_id" };`. These fields will be represented as array inside Solr.

# Files Parser
Files parser it is special parser that does not rely on mapping.
Steps: 
1. Retrieves all files from `<decodedData>` element and uploads following types to seaweed (Audio/Video/Document/Image) while creating Dtos that will be uploaded each to it's representing data model.
2. Retrieves files paths from Chat attachments xml element and uploads these files to Seaweed same as previous step.
3. Merges files dtos from first and second steps.
4. Creates csv file for each type and calls DMS UploadFiles.
5. If UploadFiles finished successfully, for each row in uploaded data adds ParentId(needed so this file will not be seen in LoadFiles but inside previously uploaded file) and calls UploadFiles once this time as List<LoaderInput>(every file that has been uploaded before to seaweed). 