When update a table- add new column or new row we need to follow this steps :

update the table in sql/maria db in 138 (using MySQL Workbench) .

**add new column / row :**
open table settings and add new field and press Apply / add new row details and press apply:

![image.png](/.attachments/image-704e9fc9-dd37-4c88-a16d-028baa3f8afb.png)

copy the sql statement and press Apply :

```
ALTER TABLE `sqlite_metadata`.`user_token` 
ADD COLUMN `IsSessionActive` TINYINT ZEROFILL NULL AFTER `sessionId`;
```



![image.png](/.attachments/image-7386a44d-569e-4f0c-95ff-6d64cb76d18f.png)

 copy the change into Dev_Albert -> open file , create brunch -> enter the line and press commit 
go to repos in azure -> go to DEV_Albert :
https://dev.azure.com/ta-9/Argus/_git/DEV_Albert
![image.png](/.attachments/image-a90335d6-a3bc-4d53-bb80-a028f1122820.png)

go do ->NETCore ->Albert.services -> src -> DBScripts -> 4.0 -> MariaDB_migration.sql :
https://dev.azure.com/ta-9/Argus/_git/DEV_Albert?path=/NetCore/Albert.Services/src/DBScripts/4.0
![image.png](/.attachments/image-619c489c-19f8-491a-9666-214f16f049cb.png)

open the file -> press main ->create new branch ->press edit (up-right corner) 
![image.png](/.attachments/image-7b5c8d96-b582-4b92-9321-f3c052835292.png)

-> add the change -> press commit :
ALTER TABLE `sqlite_metadata`.`user_token` 
ADD COLUMN `IsSessionActive` TINYINT ZEROFILL NULL AFTER `sessionId`;

![image.png](/.attachments/image-c98e2974-8423-448c-a5b0-6e5c0012033c.png)

create pull request :
![image.png](/.attachments/image-8f91dcb1-cd1f-49fe-a0b4-1074d7dc60bb.png)