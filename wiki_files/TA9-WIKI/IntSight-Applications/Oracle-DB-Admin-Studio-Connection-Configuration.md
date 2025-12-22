## Intro
Oracle DB contains different configurations and hierarchy than MySQL DB therefore The way to connect to an Oracle DB will be different than connecting to MySQL DB and others.

## Connection Explanation

1. First, you will need to check the defualt_tablespace of the user you are using to connect to the Oracle DB via the Admin Studio, in order to do that just run the next query on your database:

**SELECT USERNAME,DEFAULT_TABLESPACE FROM DBA_USERS WHERE USERNAME='YourUserName';**

2. There is an External Configuration only for Oracle DB and it is in the Reports.Service.dll.config file that should be in every App Server on any environment in the Core Services directory.

3. In The Configuration file there is the 'appSettings' attribute that should look like this (with your configuration)

![image.png](/.attachments/image-186dabf0-38ba-494b-a4a9-09406f5081fb.png)

4. You will need to configure this attribute to your needs, edit the default_tablespace that you fetched in step 1 of this wiki. (The MQHostAddress, MQUsername and MQPassword iindicates for the rabbitMQ in the same environment so make sure this configuration is right as well)

## Mandatory Privileges For Connecting Oracle DB to Admin Studio


1. select on dba_users to 'YourUser'
2. select on all_tab_columns 'YourUser'

In order to grant YourUser these privileges you can run the next queries on you database:

**GRANT SELECT ON DBA_USERS TO 'YourUser'
GRANT SELECT ON ALL_TAB_COLUMNS TO 'YourUser'**

## Admin Studio Connection String

When connecting with the Admin Studio use this connection string:

**XXX.XXX.XXX.XXX:1521/ORACLE_SID**

For Example:

10.100.102.132:1521/ORCLCDB

![image.png](/.attachments/image-6b7763d0-597d-4f23-8bd7-a6e020e5c52b.png)
***Make sure the port line stays empty**


If installed on a new environment, you should download the Driver that is at \\\10.100.102.13\Installs\DataProviders\ODAC112040Xcopy_64bit_SEE_README!!!.zip



