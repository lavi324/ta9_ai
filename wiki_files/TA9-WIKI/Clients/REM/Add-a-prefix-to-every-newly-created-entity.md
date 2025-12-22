At Reem we have a lot of prefixes for entities.
In order to have it added to a new entity its a matter of configuration:
We will go to **sqlite_metadata.system_config** and search for **REM_EventSequenceCodes**
Then, its just a matter of adding the entity id and the prefix in a format of **"ENXX":"prefix"**

![image.png](/.attachments/image-c2f92996-4205-49a5-965d-c89686626d34.png)

Then, a new entity will be called, for example:
"HAS-13559"

The dash mark is automatically added, so there is not need to add it 