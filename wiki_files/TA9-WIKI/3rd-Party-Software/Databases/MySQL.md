[[_TOC_]]

#Introduction
MySQL is the world's most popular open source database. Whether you are a fast growing web property, technology ISV or large enterprise, MySQL can cost-effectively help you deliver high performance, scalable database applications.
TA9 uses MySQL as the main metadata database. 
1. The Metadata Repository contains all the system configuration and definitions.
2. TA9's IntSight is using MySQL as the Metadata Repository.

#Installation
##Windows
1. Copy the installation locally from "\\\ta9\share\Installs\New PC Installs\mysql-installer-community-5.6.20.0.msi"
2. Run the installer.
3. We want to install a specific version of MySQL so when asked check "Skip the check for updates."
4. Pick custom installation and uncheck  MySQL for Excel. 
![image.png](/.attachments/image-7459eb7d-e4f4-4e7a-9b65-2cbf09afcd8f.png)
5. Continue pressing "Next" until you get to the configuration tab.
6. Pick the correct config type relevant to the installation.
7. Pick a root password and create another user, make sure that the Host on the new user is "All hosts".
![image.png](/.attachments/image-b600294c-99d5-45ed-b2e1-56a45215105f.png)
 8. Continue pressing "Next" until the end of the installation.

##Linux (Playbook)
1. You can run a [playbook](https://ta-9.visualstudio.com/Argus/_git/CM?path=%2FAnsible%2FDBs%2FMySql.yml&version=GBmaster) using ansible to deploy a configured mysql server.
* If manually installing on Linux use this configuration file : "\\10.100.102.13\share\Artifactory\Deployment\DBs\MySql\my.cnf"
#Managment
## How to create a user with permissions for specific tables
1.create the user from management -> users and privileges - > Add Account
2. use GRANT command to add permission to each schema or table requierd
GRANT <Action level> ON <schemaname>.<tablename> TO <username>;
for example:
- give the user permission to do all for all tables in a schema :
GRANT ALL ON ta9data.* TO newuser;
- give the user permission to only select (view) for a specific table in the schema :
GRANT select ON ta9metadata.license TO newuser;

#Troubleshooting
##Can't see Images
* Make sure [[File Server]] is up and running
* Make sure the "FilesServer" on endpoints_manager table configured to the correct url

##Can't open Data-Model or Can't fetch data from Data-Model
* Check the problematic Data-Model connection name
* Search for the "ConnectionName" on sqlite_metadata.dataconnectionsmanager table
* Verify the "ConnectionString","Address"",User" and "Password" are correct


##Error: max_allowed_packet are not allowed
* go to MySQL ini file (e.g. C:\ProgramData\MySQL\MySQL Server 5.6\my.ini) and set variables:
* max_allowed_packet=1024M
* innodb_log_file_size=1024M

##Can't save EMOJI - e.g ''\xF0\x9F\x9A'
* run 'SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;'

## Find language_translation 

SELECT * FROM sqlite_metadata.language_translation;
SELECT * FROM sqlite_metadata.language_translation where ItemKey like '%TRANS%';

Copy value from runing ENV


