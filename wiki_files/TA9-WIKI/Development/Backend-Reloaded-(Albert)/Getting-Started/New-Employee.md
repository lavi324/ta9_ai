
# **Welcome to TA9!!!**

**Setup your work env :**
•	human resources :
o	101,employee details, get door/alarm code ,Key to front door, WhatsApp group 
•	user to computer
•	Outlook account(***name***@t-a9.com)
•	slack (team cheat, better to download the app )
o	https://slack.com/-> download app->login with your @t-a9 email , join TA9 group and team group(backend).
**•	Visual Studio 22**
o	Download visual Studio 22 community - https://visualstudio.microsoft.com/downloads/ 
o	Install with the following workloads (ASP.NET, Azure).
o	clone git https://ta-9@dev.azure.com/ta-9/Argus/_git/DEV_Albert (first visit this address on brows and enter Azure using your company e-mail
o	clone https://ta-9@dev.azure.com/ta-9/Argus/_git/Argus old solution
•	VPN – install OpenVPN Connect (make sure u have goggle authentication on your phone).

•	**Docker** :
o	https://docs.docker.com/desktop/install/windows-install/
o	If u have x64 OP system the docker will open an error message and direct u to MS documentation to download an upgrade
(https://docs.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package Step 4)

•	**Download SQL** - MySql 5.7.38 (can also run on container )
o	https://downloads.mysql.com/archives/community/
o	Run the following command in PowerShell : 
docker run --name mysql-5.7_local -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysql!@#$, -e STRICT_TRANS_TABLES -e NO_ENGINE_SUBSTITUTION -d mysql:5.7.37 --lower_case_table_names=1
o	Open MySQL Workbench app
o	Create 2 MySQL connections : LocalDB, Dev 24 ()
o	Export tables from Dev 24 and Import them to LocalDB
o	Change  url (10.100.102.24/10.100.102.25) to localhost in the following tables : sqlite_metadata.dataconnectionsmanager, sqlite_metadata.endpoints_manager



•	**TA9 App training :**
https://ta9comp.sharepoint.com/sites/Training
https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/8/TA9-WIKI

http://10.100.102.24/#/Home/4/-3 training env (admin, admin )


•	**Udemy:**   https://ta9.udemy.com/
User: natalia.gordon@t-a9.com
Password : Welcome@2022
•	More Links :
o	Encryptor :"Z:\Enctypter\Utils.TESTS.exe" – all connections appears in encrypted form. Use this program to **encrypt / decrypt** 
•	More Downloads :
o	RabbitMQ(: docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=rabbit -e RABBITMQ_DEFAULT_PASS=rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
full guide : https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/470/RabbitMQ)
o	Redis : docker run -itd --name redis -e REDIS_PASSWORD=redis!@#$ -p 6379:6379 redis:latest




## Extended explanation on system installation

**Visual studio 22:**
![vs22.png](/.attachments/vs22-b94ab532-e5ab-4734-8b1e-da8e1f971abd.png)

 


SQL- 
After downloading the prog run the following commend in the PowerShell :

docker run --name mysql-5.7_local -p 3306:3306 -e MYSQL_ROOT_PASSWORD=mysql!@#$, -e STRICT_TRANS_TABLES -e NO_ENGINE_SUBSTITUTION -d mysql:5.7.37 --lower_case_table_names=1

connect to the following databases and run test connection (pass mysql(1234)+shift    ***when u click 1234 press shift : mysql!@#$ : 
•	LocalDB
•	Dev 24 , HostName : 10.100.102.25

 ![sqne.png](/.attachments/sqne-f38e81f4-dd37-406b-b276-2eb1e80e9e8e.png)

 ![sq2.png](/.attachments/sq2-4752cd37-98d6-4497-89e0-32a564d91b15.png)

Open Dev 24 and do export to the following databases :
Sqlite_metadata
Ta9_apps
Ta9data

Before doing import to LocalDB create a schema with the export names :
(Know how to copy tables but not schams )

![sq3.jpg](/.attachments/sq3-5c0fe774-ebcd-47ca-afdd-0ec1c22530a3.jpg) 

-need to change in the following tables the routing from the server () to localhost :

•	Table : sqlite_metadata.dataconnectionsmanager

SELECT * FROM sqlite_metadata.dataconnectionsmanager;

UPDATE   sqlite_metadata.dataconnectionsmanager 
SET ConnectionString = REPLACE( ConnectionString, '10.100.102.25', 'localhost')
WHERE ConnectionString LIKE '%10.100.102.25%';

•	Table : sqlite_metadata.endpoints_manager

SELECT * FROM sqlite_metadata.endpoints_manager;


UPDATE   sqlite_metadata.endpoints_manager
SET Url = REPLACE(Url, '10.100.102.24', 'localhost')
WHERE Url LIKE '%10.100.102.24%';

UPDATE   sqlite_metadata.endpoints_manager
SET Url = REPLACE(Url, '10.100.102.25', 'localhost')
WHERE Url LIKE '%10.100.102.25%';


**if u have problems make sure that the sql is not in a safe mode :
1.	Go to Edit --> Preferences
2.	Click "SQL Editor" tab and uncheck "Safe Updates" check box
3.	Query --> Reconnect to Server // logout and then login
4.	Now execute your SQL query

https://stackoverflow.com/questions/11448068/mysql-error-code-1175-during-update-in-mysql-workbench
