[[_TOC_]]

# Use GUI to restore

1. Open MySQL workbanch

2. Go to : 
Server > Data Import

![image.png](/.attachments/image-5bde4101-a17b-4aec-936e-9fd72360a727.png)

3. Pick your backup - usually ends with *.sql

4. Click start import.

5. Done.

# Restore via command line

1. Navigate to this path :

`C:\wamp\bin\mysql\mysql\mysql*.*.**\bin`

2. Type this command : 

`mysql -u username -p dbname < filename.sql`

3. Specify the DB name.

4. Enter Your Password.

5. Done.


# Restore Via Linux

mysql -u [user] -p [database_name] < [filename].sql

Done.

## Restore to Docker container from the machine: 

`docker cp /path/to/my/dump.sql mycontainer:/dump.sql`
`docker exec mysql /bin/bash -c 'mysql -uroot -pmysql!@#$ < /dump.sql`




