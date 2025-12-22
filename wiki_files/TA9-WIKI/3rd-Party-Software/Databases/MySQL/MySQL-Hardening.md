[[_TOC_]]

#A. Server Configuration Manager
A1. Ensure SQL server and agent availability in the event of OS restart
1.	Press “Start”
2.	Choose “Services”
3.	The database runs on windows service – “MySQL57”
4.	The service configured to “Automatic”

A2. Change SQL server Ports
1.	Choose ‘Administration’ tab
2.	Choose ‘Server Status’
3.	MySQL uses default 3306 port

A3. Named pipes protocol
1.	Open query builder
2.	Run the following query: SHOW GLOBAL VARIABLES LIKE 'named_pipe';
3.	Make sure the value is OFF

A4. Ensure 'allow‐suspicious-udfs' Is Set to 'FALSE'	
1.	Locate ‘allow‐suspicious-udfs’
2.	Make sure it is disabled

A5. Ensure 'local_infile' Is Disabled
1.	Open “my.ini” file
2.	Add the following line:
3.	local_infile = "OFF"
4.	Restart the DB
5.	Open query builder
6.	Run the following query: SHOW VARIABLES WHERE Variable_name = 'local_infile';
7.	Make sure the value is ‘OFF’

A6. Ensure skip-grant-tables’ Set to 'FALSE'	
1.	Locate ‘skip-grant-tables’
2.	Make sure it is disabled

A7. Prevents sym links being used 
1.	Open “my.ini” file
2.	Add the following line:
3.	symbolic-links=04dee4
4.	Restart the DB
5.	Open query builder
6.	Run the following query: SHOW VARIABLES WHERE Variable_name = ‘have_symlink’;
7.	Make sure the value is ‘DISALBED’

A8. Ensure the 'daemon_memcached' Plugin Is Disabled	
1.	Execute the following SQL statement to assess this recommendation:
2.	SELECT * FROM information_schema.plugins WHERE PLUGIN_NAME='daemon_memcached'
3.	Ensure that no rows are returned.

A9.	Ensure 'secure_file_priv' Is Not Empty	
1.	Open “my.ini” file
2.	Add the following line:
3.	secure_file_priv=<path_to_load_directory>
4.	Restart the DB
5.	Open query builder
6.	Run the following query: SHOW GLOBAL VARIABLES WHERE Variable_name = 'secure_file_priv' AND Value<>'';
7.	Make sure the value is the path that was defined

A10.	Ensure 'sql_mode' Contains 'STRICT_ALL_TABLES'	
1.	Open query tab
2.	Run the following query: SHOW VARIABLES LIKE 'sql_mode';
3.	Ensure ‘STRICT_ALL_TABLES’ value is in the list returned.

A11. Ensure 'file_priv' Is Not Set to 'Y' for Non‐Administrative Users	
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where File_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A12.	Ensure 'process_priv' Is Not Set to 'Y' for Non‐Administrative Users
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where Process_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A13.	Ensure ‘super_priv’ Is Not Set to 'Y' for Non‐Administrative Users	
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where super_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A16.	Ensure ‘shutdown_priv’ Is Not Set to 'Y' for Non‐Administrative Users	
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where shutdown_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A17.	Ensure ‘Create_user_priv’Is Not Set to 'Y' for Non‐Administrative Users	
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where Create_user_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A18.	Ensure ‘grant_priv’ Is Not Set to 'Y' for Non‐Administrative Users	
1.	Open query tab
2.	Run the following query: 
3.	select user, host from mysql.user where grant_priv = 'Y';
4.	Ensure only administrative users are returned in the result set.

A19.	Ensure 'log_error_verbosity' Is Not Set to '1'	
1.	Open “my.ini” file
2.	Add the following line:
3.	log_error_verbosity = 2
4.	Restart the DB
5.	Open query builder
6.	Run the following query: SHOW GLOBAL VARIABLES LIKE 'log_error_verbosity';
7.	Make sure the value is the path that was defined

A20.	Ensure 'log-raw' Is Set to 'OFF'	
1.	Open “my.ini” file
2.	Add the following line:
3.	Log-raw = 2
4.	Restart the DB

A21.	Ensure Passwords Are Not Stored in the Global Configuration	
1.	Open “my.ini” file
2.	Make sure ‘password’ word isn’t mentioned

A22.	Ensure 'sql_mode' Contains 'NO_AUTO_CREATE_USER’	
1.	Execute the following SQL statements to assess this recommendation:
2.	SELECT @@global.sql_mode;
3.	SELECT @@session.sql_mode;
4.	Ensure that each result contains NO_AUTO_CREATE_USER.

#B.Server Management Studio
B1. Server Authentication
1.	Choose ‘Users and Privileges’
2.	User Accounts are listed

B2. Login auditing
1.	Choose ‘Options File’
2.	Choose ‘Logging’ Tab
3.	On General section
4.	Enable general_log
5.	Enable general_log_file

B3. Local backup procedure:
1.	Choose ‘Administration’ tab
2.	Choose ‘Data Export’
3.	Choose the following:
a.	sqlite_metadata
b.	ta9data
4.	Choose ‘Export to Self-Contained File’
5.	Mark ‘Create Dump in a Single Transaction (self-contained file only)
6.	Choose backup path
7.	Mark ‘Include Create Schema’
8.	Click ‘Start Export’

B4. Locate user and log data on logical partitions separate from the partition where database server is installed 
1. Use step B3 to configure log file location
2. Change general_log_file field
3. Change log-error field
4. Change log-bin field
5. Change slow_query_log_file field

B5. Enable application roles
1.	Choose ‘Users and Privileges’
2.	Choose a user
3.	Can choose one of the existing Roles or creating a new custom rule

B6. Remove default administrators SQL logins	
1.	Choose ‘Users and Privileges’
2.	Choose ‘root’ user
3.	Click on Delete

B7. Under Object Explorer, expand server name.
1.	Choose ‘Options File’
2.	Choose ‘Logging’ Tab
3.	On ‘Binlog options’ section
4.	Enable max_binlog_size
5.	Set the value to 10737418 

B8. Restrict linked or remote servers
1.	Choose ‘Administration’ tab
2.	Choose ‘Options File’
3.	Choose ‘Replication’ tab
4.	Uncheck report_host
5.	Uncheck report_port

B9. Ensure all SQL logins have passwords
1.	Choose ‘Users and Privileges’
2.	For each user make sure the “Authentication Type” is standard

B10. Restrict guest users from databases	
1.	Open ‘New Query’ dialog
2.	Run the following SQL script against the MySQL server to remove the anonymous user account:
        DELETE FROM mysql.user WHERE User='';
3.	After making changes to permissions/user accounts, make sure you flush the provilege tables using the following command:
        FLUSH PRIVILEGES;

B11. Restrict statement permissions to database owners
1.	Choose ‘Users and Privileges’
2.	For each user review the list of statement permissions and verify that statement permissions are granted to only the 
        database owner, not individual users.

B12. Restrict database owners permissions	
1.	Choose ‘Users and Privileges’
2.	For database owner user review the list of statement permissions and verify that statement permissions granted follow least 
        privilege principle.

B13. Restrict stored procedure permissions	
1.	Choose ‘Users and Privileges’
2.	For each user review the list of statement permissions and verify that statement permissions are granted follow least privilege principle.

B14. Restrict the GRANT option	
1.	Choose ‘Users and Privileges’
2.	For each user review the list of statement permissions and verify that statement permissions are granted follow least 
        privilege principle.

B15. Create user-defined database roles	
1.	Choose ‘Users and Privileges’
2.	For each user remove all administrative roles
3.	Choose the required global privileges
4.	New custom rule will be created for this user.

B16. Remove demo files and directories	
1.	The DB was installed without demo files
2.	To make sure perform the following
3.	Choose Schemas tab
4.	Remove all unused schemas

#C. Windows Services
C1. MySQL server service account	
1.	Double-click on MySQL57.
2.	Select the Log On tab.
3.	Verify that the account listed is a local or domain user account.
4.	Launch the Windows Administrative Tools.
5.	Click Computer Management.
6.	Click Local Users and Groups.
7.	Click Groups.
8.	Right-click the Administrators group.
9.	Verify that the account in Step 3 is not within the Administrators group.

 
#D. Computer Management
D1. Create unique user-privileged OS accounts for database users and SQL server services	
1.	Click Local Users and Groups.
2.	Click Users.
3.	Right-click a database or SQL Server service account.
4.	Click Properties.
5.	Select Member of tab.
6.	Verify that the account is only member of Users.
D2. Verify That the MYSQL_PWD Environment Variables Is Not In Use		
1.	Right click “My Computer” and choose properties
2.	Click on “Advanced system settings”
3.	Click on “Environment Variables”
        Delete “MYSQL_PWD” entry if exists

#E. Backup and Disaster Recovery
E1. Backup policy in place
1.	Choose ‘Administration’ tab
2.	Choose ‘Data Export’
3.	Choose the following:
    *	sqlite_metadata
    *	ta9data
4.	Choose ‘Export to Self-Contained File’
5.	Mark ‘Create Dump in a Single Transaction (self-contained file only)
6.	Choose backup path
7.	Mark ‘Include Create Schema’
8.	Click ‘Start Export’

E2. Verify backups are good		
1.	Open the backup file from pervious section.
2.	Verify the file isn’t empty or corrupted.

E3. Backup of configuration and related files		
1.   All configuration files are backed up in the install dir.

#F. Windows Explorer

F1. Delete log and temporary files created during setup	
1.	Go to <system_drive>:\Program Data\MySQL\MySQL Installer for Windows\
2.	Remove directories and files
3.	Remove all other log and temporary files created during the MySQL Server setup.

F2. Permission setting for sensitive files and folders	
1.	Navigate to the respective folder.
2.	Right click on the folder, and select Properties.
3.	In the folder properties dialog box, select the Security tab.
4.	Click on the group/user name in the Group or user names field.
5.	Under the Permissions for field, select the checkbox setting accordingly.
6.	Click OK.
7.	Verify that there is no unauthorised group or user name in the Group or user names field, remove them if they exist.	Need 
        to be done for general_log_file', ‘error-log’, slow_query_log' and data folders

F3. Ensure Plugin Directory Has Appropriate Permissions	
1.	Open query builder
2.	Run the following query to locate the plugin folder:
        SHOW GLOBAL VARIABLES LIKE 'plugin_dir';
3.	Navigate to the plugin folder.
4.	Right click on the folder, and select Properties.
5.	In the folder properties dialog box, select the Security tab.
6.	Click on the group/user name in the Group or user names field.
7.	Under the Permissions for field, select the checkbox setting accordingly.
8.	Click OK.
9.	Verify that there is no unauthorized group or user name in the Group or user names field, remove them if they exist.

#H. Access Control
H1. Access control to sensitive files	
1.	Right click on <system_drive>:\ProgramData\MySQL.
2.	Click on Properties from the menu.
3.	Select the Security tab from the dialog box.
4.	Assign Permissions to the folder as follows:
•	MySQL Server service account: Full Control
•	Administrators: Full Control
•	System: Full Control
•	Users group: None
5.	Navigate to the SQL log files volume, which could possibly reside on a separate disk from the database server installation.
6.	Assign Permissions to the folders as follows:
•	MySQL Server service account: Change
•	Auditing user account: Read

#I. General Controls
I1. Do not connect the database to the network	
1.	Do not connect the database to the network until the operating system and security patches have been installed and this 
        document has been signed off by all parties.
2.	Exception is made only for closed network solely for the purpose of network base installation.

I2. Install database server on dedicated database service system	
1.	The database server should service only database-specific requests.

I3. Install database on non-OS partition	
1.	Install database binaries and files on a different partition in the underlying OS.

I4. Install latest patches	
1.	Install most recent and relevant security patches and hot-fixes after testing in the test environment.

I5. Do not install development software on a production machine	
1.	Ensure that no development software is installed on the production machine. 
Some of the popular compilers include:
•	Visual Studio
•	Java

I6. Do not install unnecessary software modules on a production machine	
1.	Ensure that only the necessary software modules are installed on the production machine.
2.	At the point of installation, ensure that custom installation is chosen. This is done to ensure that only required modules 
        are installed.
3.	Additional software that is needed at a later date can be installed when it needs to be used.

I7. Archive emergency access account password	
1.	Archive the default administrator’s password securely.

I8. Ensure compliance to underlying OS baseline security configuration guide	
1.	Obtain sign off from the appropriate parties according to the underlying OS baseline security configuration guide.

I9. Leverage a least privilege principle	
1.	Ensure that all accounts have the absolute minimal privilege granted to perform their tasks.

I10. Disable SQL server ports on firewall	
1.	Ensure that perimeter firewalls are configured to block access to the SQL Server. Connection to the SQL Server ports should 
        be restricted to application servers and network segments from where client applications may access the server.
        Note: The default MySQL Server TCP port is 3306

I11. Limit the accounts on the database server	
1.	Accounts on the database server shall be kept to a minimum.
	
I12. Use non-default account name	
1.	Non-default SQL server account names shall be used where possible.

I13. No sharing of password	
1.	Each account password must be known only to the user and must not be shared.	

I14. Enforce maximum password age for administrator password	
1.	Ensure the administrator password is changed periodically. - Using the user and host information from the audit procedure, 
        set each user a password age
        e.g.  `ALTER USER jeffrey'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;`

I15. Enforce password complexity for administrator passwords 	
1.	Open my.ini
2.	Add the following rows:

       ```
       plugin-load=validate_password.so
       validate-password=FORCE_PLUS_PERMANENT
       validate_password_length=14
       validate_password_mixed_case_count=1
       validate_password_number_count=1
       validate_password_special_char_count=1
       validate_password_policy=MEDIUM
       ```
I16. Change default password	
1.	All default SQL server passwords shall be changed. 

I17. Separation of DB and OS administrator functions	
1.	Database and underlining OS administrative accounts shall be segregated.

I18. Restrict right to access backup files	
1.	The right to access backup files shall be restricted to only the following users or group:
•	System Administrators

I19. Secure remote access	
1.	All remote administration access to the server must be authenticated with protection against loss of confidentiality using secure VPN mechanism.

I20. Protection of SQL server audit data	
1.	Confirm that logs are being archived to a secure medium and moved off site. The backups should include audit logs. Ensure that the control files reflect mirroring of the redo logs and that they are on different physical devices.

I21. Baseline backup	
1.	A working baseline backup must be made immediately after the SQL server is fully configured.

I22. Conduct security test of server services	
1.	The server services shall be tested for security vulnerabilities before rolling out to production.  Subsequently, monitoring of future vulnerabilities should be performed regularly and the server secured accordingly to vendor’s recommendation.

I23. System testing before operational use	
1.	The server must be tested for compliance to this guideline prior to release into production environment.

I24. Ensure No Users Have Wildcard Hostnames	
1.	Execute the following SQL statement to assess this recommendation:
2.	SELECT user, host FROM mysql.user WHERE host = '%';
3.	Ensure no rows are returned.
