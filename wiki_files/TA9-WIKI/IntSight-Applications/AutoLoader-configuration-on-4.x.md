[[_TOC_]]


# 1. Introduction
The Autoloader will let the user load files automatically to a specific DM through a dedicated folder.

# 2. Process
1. Create the 3 folders on your NFS, Source Files Path, Insert Complete Path and Error Path, For Example
``/<<NFSLOADERPATH>>/test `` 
``/<<NFSLOADERPATH>>/test/s``
``/<<NFSLOADERPATH>>/test/f``

2. Replace the marked "test" with what ever name you want the loader directory to be called

3. Make sure there is a bind from the <<NFSLOADERPATH>> to ``/mnt/loader`` in the loader-service that looks like the image


![WIKI 2.png](/.attachments/WIKI%202-f2c3be6c-6450-4151-a09b-bb2bcc688d27.png)







4. Notice
In my example the <<NFSLOADERPATH>> is ``/opt/data/loader``
5.	Go to sqlite_metadata.data_loader table in MySQL DB and add a row that will contain the info regarding the autoloader itself
a.	Enter your DataModelID
b.	Leave DataLoaderID empty (auto incremented)
c.	Description is optional
d.	Enter the target SourceFilesPath inside the container, For example if your bind is like the image of mine above and the folder name is test the SourceFilesPath is 
``/mnt/loader/test``
e.	Enter the target InsertCompletePath inside the container, For example if your bind is like the image of mine above and the folder name is test the InsertCompletePath is 
``/mnt/loader/test/s``
f.	Enter the target ErrorPath inside the container, For example if your bind is like the image of mine above and the folder name is test the ErrorPath is 
``/mnt/loader/test/f``
g.	FileMask is the file type, For Example: CSV
h.	IsValid is whether the autoloader is active or not
i.	UploadToFileServer is whether the file will upload to the file server
j.	Enter your DataLoaderName
k.	ColumnDelimiter is the character that separates between the columns
l.	TextQualifier keep null
m.	FirstRowHasHeader is whether the first row of the file is a header (not data)
n.	Enter your Parser if you have one, if you don’t, keep null
o.	For MappingList column enter the next JSON for every field in the DM, map which SourceFieldName in the file matches the TargetFieldName
``
[
    {
        "SourceFieldName": "ID",
        "TargetFieldName": "ID"
    }
]
p.	For LoaderParam column enter the next JSON and make changes to the parameters in <<>>
{	
    "DataModelID": <<DMID>>,
    "DataSource": null,
    "DepartmentID": null,
    "Description": "<<DESCRIPTION>>",
    "FilePath": null,
    "InvestigationID": "<<CASEID>>",
    "Latitude": null,
    "Longitude": null,
    "ParserName": "<<PARSERNAME>>",
    "Type": <<FILEITEMTYPE>>
}
``
6. **__Notice__**
FILEITEMTYPE – pick the ID you need from sqlite_metadata.file_item_type





![WIKI 1.png](/.attachments/WIKI%201-2482e26d-4d56-4382-be25-5a8a3d00547c.png)







7. Insert a file to your Source Files Path on the server.

8. After a few seconds to a minute, the file is supposed to transfer to either the s or f folder according to the success or failure of the upload.

9. If the file was transferred to the f folder, go the loader-service logs to find out why.

