[[_TOC_]]

#Introduction
What is WildFly?
WildFly is a flexible, lightweight, managed application runtime that helps you build amazing applications.
We use wildfly to host the following services:
- Twitter
- Blotter
- Entities
- Face Recognition
- Free text
- Media Analyzing
- Text Analytics 

##Memory usage
To change the amount of RAM used open "bin\standalone.conf" and edit the all the numeric values in the following line:
`JAVA_OPTS="-Xms2g -Xmx6g -XX:MetaspaceSize=2g -XX:MaxMetaspaceSize=6g -Djava.net.preferIPv4Stack=true"`

#Deployment
Copy the services '.war' files to the "standalone\deployments" folder and wait until a new file with the name of the service appears and has a '.deployed' extension.
* If a '.failed' files appear instead you should consult the logs.

## Restart single service
Go to "standalone\deployments" folder, choose the specific service and remove the '.deployed'|'.undeployed'|'.failed', a new '.dodeploy' should appear. wait until a new file with the name of the service appears and has a '.deployed' extension.
* If a '.failed' files appear instead you should consult the logs.

## Restart all services / Restart WildFly
1. Open Windows Services
1. Restart 'TA9 WildFly' Service
1. In case the service isn't stopping kill the 'java.exe' process from Task Manager
1. After service restarted, wait until a new file with the name of each service will appear and has a '.deployed' extension.

3. After service restarted, wait until a new file with the name of each service will appear and has a '.deployed' extension.

#Troubleshooting
There are logs available:
 - 'standalone\log' - this is Wildflys log good for finding problems with deployment or internal 


__________________________________________________________________________________________________________________


error message: 
NER initialization has failedjava.io.IOException: Unable to open "/opt/wildfly/TextAnaltycsProviderFiles/NER/english.muc.7class.distsim.crf.ser.gz" as classpath, filename or URL

1. Make sure that the path is correct in MySQL

SELECT * FROM sqlite_metadata.system_config;

<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/6fab8f04-a1e8-4ffe-bff9-d0b9d0851917?fileName=image.png"  alt="Image"/>


2. for example: "/opt/upload" wasn't exist


