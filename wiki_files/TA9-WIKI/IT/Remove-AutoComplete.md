#Remove The Auto Complete
##Connect to solr
1. connect to the solr machine and locate the freetextindex core folder.
![image.png](/.attachments/image-0cdd6fd6-2ee8-48d6-b51f-0cf1df1d57cc.png)
2. get into tht conf folder.
![image.png](/.attachments/image-09ea0586-08ca-4a54-b4f7-b98983c37594.png)
3. Edit solrconfig.xml file.
![image.png](/.attachments/image-c2e2822c-2e39-4192-b0f0-25d4dbf7445d.png)
4. locate the searchComponent suggest and the requestHandler /suggest.
![image.png](/.attachments/image-154b3ebb-8c9c-49b0-bfc1-a68abe2ebe4d.png)
5. now comment both items.
![image.png](/.attachments/image-17398ed9-a923-4356-8f00-57a39fef5b94.png)
6. restart solr
7. check if the changed worked.
![image.png](/.attachments/image-59dff101-1b53-40ff-97fe-a45b8e5bc431.png)
