to configure the “image” field in a data model to allow uploading an image:

1. Field Identifier should be set to “Detection”
2. Need to create a config in 'sqlite_metadata.system_config' table called "imageUrlFieldFR" – its config value should be the field ID (you can find the field ID in the 'sqlite_metadata.dataschemafields1' table. It should look like this
![image.png](/.attachments/image-419046c0-f1ec-45a3-90fe-5a9d7db4010f.png)
##This config value can only support one value at the time, therefore only one DM


![image.png](/.attachments/image-e2dd77a6-25c3-4266-b24b-694f97cd7983.png)
##When configured right, should look like this where you can upload an image and search on it