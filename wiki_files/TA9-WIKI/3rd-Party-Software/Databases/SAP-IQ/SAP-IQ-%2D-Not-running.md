# No option to connect to the server via ODBC on the infected machine:

##Download Link for ODBC:

[\\\10.100.102.13\Share\Installs\SAP IQ full 16_0\msodbcsql.msi]()

## Download Sybase Central - Version 16 
[\\\10.100.102.13\Share\Installs\SAP IQ full 16_0\SQLA16_Windows_Client.exe]()

1. Run ODBC Data Source (64-bit)
![image.png](/.attachments/image-b8d67673-5ddc-4455-914d-8ba00fe30041.png)

1. Go to System DSN tab and click Add 
1. Add new Data Source - SQL Anywhere 16
![image.png](/.attachments/image-5fd17fd6-db86-410e-9687-b9864eddba57.png)
1. Choose a Data Source name on ODBC tab
1. Define the connection details on Login tab
Server Address: 10.100.102.41
User: DBA
Pass: sql
![image.png](/.attachments/image-fb929b66-0671-47d3-8d3a-716990b69a1b.png)


If Database not connecting go to the Database machine and run this command.
Run this script ad admin:

"C:\SAP\IQ-16_0\Bin64\iqsrv16.exe" @C:\ProgramData\SybaseIQ\demo\iqdemo.cfg -n iiqdemo C:\ProgramData\SybaseIQ\demo\iqdemo.db -hn0,3740:2596 -ti 4400 -tl 0 -gn 25 -o C:\ProgramData\SybaseIQ\logfiles\iqdemo.002.srvlog "-hn0,5664:252"











