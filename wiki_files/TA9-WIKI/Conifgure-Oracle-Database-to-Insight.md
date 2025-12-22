## Intro
Oracle DB contains different configurations and hierarchy than MySQL DB therefore The way to connect to an Oracle DB will be different than connecting to MySQL DB and others.

## Connection Explanation

1. First, you will need to check the defualt_tablespace of the user you are using to connect to the Oracle DB via the Admin Studio, in order to do that just run the next query on your database:

**SELECT USERNAME,DEFAULT_TABLESPACE FROM DBA_USERS WHERE USERNAME='YourUserName';**

2. add to SystemConfigurtaion secret in vault the field "OracleDefaultTablespace", and set the value to your user tablespace

![image.png](/.attachments/image-b42969d6-715f-41c4-863d-481674d9a036.png)

3. For the change to apply please reset DMS and Metadata services