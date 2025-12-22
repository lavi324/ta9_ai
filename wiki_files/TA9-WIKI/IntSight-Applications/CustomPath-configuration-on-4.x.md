[[_TOC_]]

# 1. Introduction
The 'Custom Path Viewer' will let the user view images in the data model fields
# 2. Process
1. Create the folders that will contain the data that will be displayed as custom path, It can be either local on the server or from any share

2. Make sure you create those folders under the main custom path folder, this folder should already be in the customPathsDefinitions value in the DB
3. The paths usually for the custom path are:
Inside the service container - /usr/share/nginx/html/custompath
Outside the service container - /opt/data/images/custompath
When accessing via web - http://<<HOSTNAME>>/custompath
4. Make sure that under the web_gateway service in the portainer there is a mount bind for the paths mentioned earlier, it should look like this
![image.png](/.attachments/image-613ac3ba-3b5a-421b-b058-f655b910b34f.png) 
5. Make sure that in the web_gateway service in the portainer there is a config called 'web_nginx_config' which the end of the file should look like this, If there is not please follow steps A-D below
![image.png](/.attachments/image-0dfa4376-9713-4b72-b4c0-8c182fc906c3.png)
6. For a field to be displayed as CustomPathViewer you need to know the FieldID, can be found in sqlite_metadata.dataschemafields1
7. Change the viewer type to custom path viewer
8. Go to the sqlite_metadata.system_config table, then go to the "customPathsDefinitions" ConfigKey and edit its ConfigValue
9. Paste the next value with a changes to the parameters in <<>>


    "<<FieldID>>": {
        "baseUrl": "http://<<HOSTNAME>>/<<VirtualDirectoryName>>",
        "viewerType": "<<ViewerType>>"
    }
10. Go to sqlite_metadata.dataschemafields1 and add the same URL in the column "AdditionalParameters"
11. Go to the Admin Studio, Go to Data Models and pick your DM
12. Click on the field you want to display as CustomPath viewer and select for its ViewerID the "Custom Path Viewer" option as in the image
13. Clear Server and client cache and test if the configuration is working

# 3. Steps to follow in case the config in step 5 do not exist
A. In the configuration page click on Clone config
![image.png](/.attachments/image-74e5463f-49b4-4250-b03d-284d249bbdcf.png)
B. Paste the next JSON to the correct location in the file like the image in step 5 and give the config a name
    location ^~ /custompath {
         gzip on;
         gzip_comp_level   9;
         gzip_disable      "MSIE [1-6]\.";
         gzip_http_version 1.1;
         gzip_min_length   256;
         gzip_proxied      any; #expired no-cache no-store private auth;
         gzip_types        *; #text/plain text/css application/json application/javascript application/x-javascript text/xml application/xml application/xml+rss text/javascript;
         gzip_vary         on;
         alias /usr/share/nginx/html/custompath;
         etag on;
         expires $expires;
    }
C. Click Create config at the bottom of the page
D. Go back to the configs of the service, Delete the current config, Search for your config in the dropdown menu and click '+ add config' and click 'Apply changes'
![image.png](/.attachments/image-34eccd18-8b23-49c0-b3ff-c8807e1a8960.png)


