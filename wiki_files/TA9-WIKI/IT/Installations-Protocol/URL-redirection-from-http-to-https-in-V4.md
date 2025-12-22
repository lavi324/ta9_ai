###The following configuration is to support the redirection of http requests to https. Meaning, if a user enter the TA( URL with http, he will be redirected to the URL with https. 


#Editing nginx.conf file in web stack

### _Add the following section above the existing server section:_




```
#redirect http to https
server {
    listen 80 default_server;
#     server_name;
     return 301 https://$host$request_uri;
}
```

###_On main server section disable listen on port 80:_


```
server {

#     server_name << server name >>;

#    listen 80;
    listen 443 ssl;
```

 
### _Remove web stack and redeploy it with the changed file_











