[[_TOC_]]
#Summery
1. The Text Analytics Service is responsible for text analytics in the system.
2. It enables various ways of text extraction, meta-data extraction, entity extraction and so on.
3. It supports extraction from text, files and URLs.
4. Various modules are using this service: Data Loading, Entity Extraction app, etc.

#Troubleshooting
##The service is not deployed successfully
The Text Analytics Service is relatively big service and takes more time and memory to load compared to other IntSight services. Therefore, if it fails to deploy, both timeout and memory settings of the WildFly service loader should be increased.

* At the standalone.xml configuration, change the following:
1. `deployment-timeout="1800"`
2. `"JAVA_OPTS=-Xms1024m -Xmx8196m -XX:MetaspaceSize=1024M -XX:MaxMetaspaceSize=8196m"`
3. Restart the WildFly service

## TextExtraction from URL isn't working
Make sure the file sent by URL as a link is accessible to where The Text Analytics Service is executing from.

# TextAnalytics Via External Jar
the Text Analytics Service can run with external jars. The service includes 5 main interfaces – each can be implemented by external jar (each jar can contain any or all the interfaces- thus user can chose to use external jar for some of the interfaces wile the others operate on the system's default jars) the above mentioned main interfaces are :
- IEntityExtraction
- ILanguageIdentification
- IOCR 
- ITextExtraction
- ITranslation 

We supply those interfaces via the attached jar (which the implementer has to import into his project)

**Implementation note:** 
for each interface the external jar will be loaded once, and the interface's implementing class will be loaded once as well - using the initialize function (part of the interface), thus we recommend implementing those classes as singletons.* Finally, to select an external dal – the user has to change the interface external dal config values (via our configuration service) So they refer to his jar file and specific classes names.

* User can use regular classes, although we will access the class constructor only once – and save the object reference for further use during runtime
_____________________________________________________________________________________________________________________

# TextAnalytics

## NER initializtion has failed

The path to the files does not exist
go to mysql workbanch under `system_config` table


![image.png](/.attachments/image-3d280fa1-c7e5-495c-8c98-af152215511f.png)

Change it according to your config.


```
SELECT * FROM sqlite_metadata.system_config;

Update sqlite_metadata.system_config
set ConfigValue = replace(ConfigValue,"/opt/application/TextAnaltycsProviderFiles","/opt/wildfly/TextAnaltycsProviderFiles");
```

# Tessaract OCR Installation
## Installation
### Windows
Install Tessaract on the server machine (where TextAnalytics resides) (I've downloaded it from here: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe)
or
\\\10.100.102.13\Share\Installs\tesseract-ocr
### Linux (Centos) 
run the following:

```
sudo yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/
sudo rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key
sudo yum update
sudo yum install tesseract 
```

## Configuration
Configure the following configurations:

SELECT * FROM sqlite_metadata.system_config;

1. OCR_ENGINE - should be TESSARCT
2. TIKA_EXTRACT_OCR_FROM_PDF - Config TIKA whether to try to extract text in images contained in PDF files. Possible values: true/false
3. TESSARACT_OCR_FILES - path for tesseract language files (when OCR configured to TESSARCT). Possible value for Windows OS : D:\\Program Files\\Tesseract-OCR\\tessdata\\ or Linux: /usr/share/tesseract/4/tessdata
4. TESSARACT_OCR_EXE_FOLDER - path for tesseract installation folder (when OCR configured to TESSARCT). Possible value for Windows OS: D:\Program Files\Tesseract-OCR\ or Linux: /usr/bin/tesseract



