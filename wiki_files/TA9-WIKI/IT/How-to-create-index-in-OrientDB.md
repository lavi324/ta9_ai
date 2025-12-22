**Run the following queries in OrientDB**  

* Create index EN{Num}.Sys_PermissionValues on EN{Num}.(Sys_PermissionValues) NOTUNIQUE_HASH_INDEX;
* Create index EN{Num}.Sys_PermissionMode on EN{Num}.(Sys_PermissionMode) NOTUNIQUE_HASH_INDEX;

![image.png](/.attachments/image-7d93e085-e707-4cbf-8045-ffdc3a4c3c3b.png)

* Change {Num} to the number of the entity you would like to create index for.

**_Disclaimer: You can run only one query at a time!_**