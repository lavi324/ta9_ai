after adding the new solution for uploading large files (currently only for cellebrite files)
we need to configure the following for each envoierments:

set the config values : **LargeFilePath**, **SuccessFolderPathLargeFile**,**FailsFolderPathLargeFile**
choose path that the server has access too .
 "LargeFilePath" - folder the server have access to, the files will be taken from here (only the main folder and not sub-folders)
only "zip" files are presented
in case the upload is successful the file should move to : "SuccessFolderPathLargeFile"
and in fails the file should move to : "FailsFolderPathLargeFile"