[[_TOC_]]

# Define a new Auto Loader
1.The relevant service is Loaderserivce - make sure that it has valid mount.
![image.png](/.attachments/image-e6925e91-6d67-47f4-949d-5f2d7c177251.png)

2. Open Maria
3. Go to sqlite_metadata.data_loader

**DataModelID** - look in dataSchema1 for the DM ID
**SourceFilesPath** - create a folder to put the files for load in, make sure the loader has access to that folder - the loader will listhen to this folder
**InsertCompletePath** - create another folder inside the folder of 'SourceFilesPath' that the file will be inserted to in case of success
**ErrorPath**- create another folder inside the folder of 'SourceFilesPath' that the file will be inserted to in case of failer
**FileMask** - type of the file for load, e.g. csv, txt
**IsValid** - insert 1 for yes, 0 for no
**UploadToFileServer** - insert 1 for yes, 0 for no
**DataLoaderName** - As you pleased
**ColumnDelimiter** - e.g. ',' (in case of csv)
**TextQualifier** - can be null
**FirstRowHasHeader** - 1 if the file contains headers, 0 if not
**Parsers** - the parser name
**MappingList** - can be null
**LoaderParam** - 
Follow this format:

{"InvestigationID":"-1",
"Description":"",
"FilePath":null,
"DataSource":null,
"Type":7, //in case of DM
"ParserName":"Emails", //Parser name from the getName() function
"DataModelID":-100, //same as DataModelID
"DepartmentID":null,
"Latitude":null,
"Longitude":null}

**IsEtlMode** - 0

3. Restart the loader service

