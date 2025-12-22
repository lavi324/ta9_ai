## Intro
Every DB contains different configurations and hierarchy than MySQL DB therefore The way to connect to Hive DB will be different than connecting to MySQL DB and others.

## Admin Studio Connection String

When connecting with the Admin Studio use this connection string:

1. Enter the IP of the server which hive is installed
2. Enter the port you are using to access the DB remotely
3. Enter credentials that have privileges over the table you want to use

For Example:

<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/a43450cf-2cac-4488-ac6f-78d1bee92c89?fileName=image.png"  alt="Image"/>


If installed on a new environment, you should download the ODBC Driver that is at \\\10.100.102.13\Installs\DataProviders\HortonworksHiveODBC64.msi