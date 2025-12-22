To remove relations follow the steps:
**Note - deleted relations cannot be restored**

**1. Identify relation ID** (**A**)
- Open the relation on the main graph (Web application) and "right click" on the relation preview:
![image.png](/.attachments/image-a82d7d5a-9c7f-45a2-97de-852781fade9f.png)
- Open the relation in a new window by clicking ![image.png](/.attachments/image-91cd3d39-21fd-4af4-bd28-7869567f40d9.png)
- locate the relation ID in the URL
![image.png](/.attachments/image-56e9b586-6dd5-4c98-a980-1a00b23a906c.png)

**2. Identify relation type ID** (**B**)
- Open Admin studio and go to Ontology manager
- Open "relation definition" and choose the relation type
- see the relation ID located on the bottom right corner of the screen: ![image.png](/.attachments/image-e0f8fdc7-c7b2-4a6a-ab48-df6494918d83.png)


**3. Log in to the OrientDB** 
**4. View the relation** type in the following query and click "run": _select * from rl**B** where Sys_ID = **A**;_
- _**Fore example:** select * from rl21 where Sys_ID = 41179;__

**5. Delete the relation** by running the command: _Delete EDGE rl**B** where Sys_ID = **A**;_
- _**For Example:** Delete EDGE rl21 where Sys_ID = 41179;_


**6. Verify the relation was deleted** by refreshing the web client and running the search on the entity again
