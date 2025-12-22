[[_TOC_]]


# MySQL won't start

1. Make sure there is enough spach
```df -kh```


_________________________
# MySQL won't accept lower case

check by this command : 

show variables like 'lower_case_table_names'

if 

![image.png](/.attachments/image-b3a744d5-5b6c-4db7-9c3b-e153f333a767.png)

thene the setting is ok, 

any other result then 1 is wrong. 

## How to fix it ? 

copy my.cnf file from : 
\\10.100.102.13\Share\Artifactory\Deployment\DBs\MySql\my.cnf

to the machine: 
```
mount -a
cp /mnt/smb/Artifactory/Deployment/DBs/MySql/my.cnf ~/home/ta9/
```

## Copy to the container 
```
docker cp /home/ta9/my.cnf mysql:/usr/local/mysql/my.cnf
docker cp /home/ta9/my.cnf mysql:/etc/mysql/my.cnf
```
## Restart the container
```docker restart mysql```


















