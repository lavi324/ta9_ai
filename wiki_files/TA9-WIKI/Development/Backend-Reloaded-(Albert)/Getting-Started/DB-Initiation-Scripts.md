#Introduction
Under Argus\DBScripts\MySql in the Argus repo there are some db scripts for creating and updating the metadata DB
Here are some clarifications.

#Syncer Files
**DBChangeSyncer.js** -  The main syncer file, it holds the updates for the current running version. on version release an update syncer file is crated and the current file is cleared. 
**UpdateScripts** - A new file is created with every release, its used to update the DB on running environments.

#SQL Files
**BaseScripts** - An SQL script that creates a vanilla metadata DB for installing on new machines.
**BaseScriptsWithData** - An SQL script that creates a DB with some sample data.