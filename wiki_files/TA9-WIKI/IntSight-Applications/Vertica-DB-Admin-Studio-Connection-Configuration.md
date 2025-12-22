## Admin Studio Connection String

When connecting with the Admin Studio, use this connection string:

1. Enter the IP of the server on which Vertica is installed
2. Enter the port you are using to access the DB remotely
3. Enter the Database name you want to connect to
4. Enter credentials that have privileges over the table you want to use

![image.png](/.attachments/image-2f25a54a-4bb5-42f2-9e2b-43b79d39edde.png)

**NOTE:** 
If you don't know what your Vertica DB name is, run the following query in a new script while connected to the DB:
`SELECT CURRENT_DATABASE();`
