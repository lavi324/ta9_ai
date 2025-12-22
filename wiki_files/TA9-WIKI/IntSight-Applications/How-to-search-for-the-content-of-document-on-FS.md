1.Open FileZilla.

2.Go to the path:/opt/solr/server/solr/freetextindex/conf. 
(This path is on 50 environment, the path can be different on another environment).  
 
3.Download the file 'managed-schema' for a backup. 

4.Right click on the file 'managed-schema' and click on 'view/edit'.
![image.png](/.attachments/image-b3ad6ccc-85e7-4be7-860f-555981042aff.png)

5.Add to the file this row : `<copyField source="YOUR_FIELD" dest="content"/>`
and save.
- Note: The field should be written in the same way it's written in orient.
![image.png](/.attachments/image-cd505838-fbc4-40b3-b54d-5c837b8045c1.png)

![image.png](/.attachments/image-dd36116e-fc21-4fc3-a3d1-753b1ee7e5d7.png)

6.Do a reset to the solr 
- open the putty and run - systemctl restart solr.

![image.png](/.attachments/image-1a7a1f43-f851-4a1a-ac82-750ec1e40669.png)