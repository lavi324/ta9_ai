# Upload the file to desired server
Link to webinar: https://web.microsoftstream.com/video/20b8fdea-b297-44ad-862f-797561409180
Webinar aid file: [Windward-Webinar.docx](/.attachments/Windward-Webinar-6d307e7d-1cfa-42b0-b489-e83e8534a746.docx)

![image.png](/.attachments/image-ec4ec5f8-3a00-4e2b-a47b-ae9a787ab0e1.png)

Isuzu/Hof-Template-Final-X.X.X.docx

Download to your PC.

# Upload via web 
![image.png](/.attachments/image-f164e06f-010e-477b-bbea-282cf6b0777d.png)

**Upload The File**

![image.png](/.attachments/image-20f005c3-49ec-44d0-a0c2-90f8a69f1624.png)

# Update SQL Server 

**look for**
*.*load_files

**SELECT * FROM sqlite_metadata.load_files order by id desc;**

Copy the: Serverfilepath 

![image.png](/.attachments/image-1803220a-07dc-4b05-ad1e-aff8622b2dd9.png)

**SELECT * FROM sqlite_metadata.system_config;**

to: Config Value in:

![image.png](/.attachments/image-f1287d74-e47d-446a-bcc4-7c66ef8f1c1c.png)

# Redeploy Wildfly

Delete the deployed file, wait until status changed to undeploy, 
delete again - see status deployed.

![image.png](/.attachments/image-f101c236-63ea-46d3-9c28-92de85ee196f.png)