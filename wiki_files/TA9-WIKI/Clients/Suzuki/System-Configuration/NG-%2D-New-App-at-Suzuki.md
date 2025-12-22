[[_TOC_]]

# installation process

## configure IIS Manager: 

1. open the IIS console.
![image.png](/.attachments/image-d6aca2e7-7968-4f05-883e-4d752c92ea23.png)

2. Add the application to your pathv to boot the application from.

3. make sure on ng web page enter the credentials:

4. Change the protocol to https

![image.png](/.attachments/image-611c2817-8b30-4c58-9657-ec0af0198453.png)

## config.deploy file

At the location of your ng app: 
1. \TA9\Web\Web Client\ta9-ng\assets\config\config.deploy.json

Make sure:

1. That the domain is properly configured
2. Point to the desired domain name / IP 
3. Change the default domain to your domain





# Troubleshoot
## Getting 404 error in the new app

![image.png](/.attachments/image-4df69dad-6a16-49df-b1c3-51366c0c8633.png)

GET https://ta9web.internet.spf.gov.sg/ng/assets/config/config.deploy.json

go to web.config at : 
\TA9\Web\Web Client\ta9-ng\web.config

add this content: 
    
    
```
<security>
      <requestFiltering>
        <fileExtensions allowUnlisted="true" >
          <remove fileExtension=".json" />
          <add fileExtension=".json" allowed="true"/>
        </fileExtensions>
      </requestFiltering>
    </security>
```





