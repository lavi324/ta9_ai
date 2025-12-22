[[_TOC_]]
# Introduction
The Syncer tool is a tool designed to help synchronize the MySQL databases between Intsight environments both for production and development. This tool has some variation
* Cli - For automation after deployment
* UI- Mainly for developers, or for fixing broken queries after a failed automation. 
* Build task - Only useble for new environments. since it has no history saved. mainly used for updating new environments to a required branch.  
# Installation
## CLI
1. Download the tool from the Git Repo "utils" (git clone http://10.100.102.12/tadev/utils.git or git@10.100.102.12:tadev/utils.git).
2. Copy the Syncer folder to a local folder.
3. Run npm i.
4. Configure the tool by creating the following file syncerConfig.json.

example : 
   
```
{
      "mysqldata": {
          "host": "localhost",
          "user": "root",
          "password": "mqslpassword",
          "database": "mysql",
          "multipleStatements": "true"
      },
      "userName": "stas",
      "pathToQuery": "C:\\WorkSpace\\argus\\DBScripts\\MySql\\DBChangeSyncer.json",  - dbcahnges file in the git repository.
      "pathTonewQuery":"C:\\WorkSpace\\apps\\Syncer\\newQuery.sql" - local file which contains the imminent changes.
   }
```  
empty :
   
```
{
      "mysqldata": {
          "host": "",
          "user": "",
          "password": "",
          "database": "mysql",
          "multipleStatements": "true"
      },
      "userName": "",
      "pathToQuery": "",
      "pathTonewQuery":""
   }
```
## UI
1. Extract `\\10.100.102.13\Share\Installs\Ta9 utils\Syncer\SyncerUI.7z` to "C:\\"
2. Copy the update file `\\10.100.102.13\Share\Installs\Ta9 utils\Syncer\Update\Syncer.exe` to your local folder owerwriting the existing file.
3. Use the configuration instruction from the CLI segment.

# How To Use
## CLI
1. Copy the DB script to the "newQuery.sql" file
2. Run syncer.lnk from cmd or by double clicking the shortcut (you can also use "syncer.lnk pull" or "syncer.lnk push")

###Write to file
1. Syncer Write to file or wf
2. The query\ies in the "newQuery.sql" file will be inserted into the db changes file in your git directory, and will be pushed with all of yours other changes. "newQuery.sql" will be cleared.
3. You must apply updates to your local SQL instance manually.

###Update local database
1. Syncer update local database or udb
2. Your local database will be updated by the quarries received from the dbChange file.

## UI
Start Syncer UI using Syncer.exe

### Update local database 
On the right you can see pending updates, they can be applied one by one using the button next to the query, or you can run them all at once with the "Update Database" button.

### Write Updates
Using the text box on the left you can insert queries that will be passed to other developers, don't forget to write a comment.
The Syncer will create a new file with the name of your current local branch, this file must be committed with the rest of the code so that your update will reach the master branch and thus everyone.
![image.png](/.attachments/image-9b418e08-3582-4a5e-9c74-529ceb85b11c.png)

___

# Troubleshoot

## `DBChangeSyncer.json is corrupted or missing, please fix the file and reload the application`
* The directory of `pathToQuery` may contain Empty / Invalid files.
* The directory of `pathToQuery` may contain unparseable JSON files.
* The path `pathToQuery` is inaccessible.