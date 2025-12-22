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

#Installation
##Windows
1. Copy `\\10.100.102.13\share\Artifactory\Deployment\Servers\wildfly-10.0.0.Final` anywhere you wish.
2. Run `bin\service\service.bat install` with admin privileges - this will create a windows service for WildFly called "TA9 Wildfly"

##Linux (Playbook)
1. You can run a [playbook](https://dev.azure.com/ta-9/Argus/_git/CM?path=%2FAnsible%2FTools%2FWildFly.yml&version=GBmaster) using Ansible to deploy a WildFly server.

#Configuration
##Public IP
First if you want to make Wildfly accessible externally you need to change the public IP that Wildfly is bound to, to do so do to "standalone\configuration\standalone.xml" and change the following:
`<interface name="public"><inet-address value="${jboss.bind.address:127.0.0.1}"/></interface` 
to
`<interface name="public"><inet-address value="${jboss.bind.address:MACHINE_IP_ADDRESS}"/></interface`
* If all traffic to the Wildfly server passes through the local host this step is redundant.

##Memory usage
To change the amount of RAM used open "bin\standalone.conf" and edit the all the numeric values in the following line:
`JAVA_OPTS="-Xms2g -Xmx6g -XX:MetaspaceSize=2g -XX:MaxMetaspaceSize=6g -Djava.net.preferIPv4Stack=true"`

#Deployment
Copy the services '.war' files to the "standalone\deployments" folder and wait until a new file with the name of the service appears and has a '.deployed' extension.
* If a '.failed' files appear instead you should consult the logs.

## Restart single service (Windows and Linux)
Go to "standalone\deployments" folder, choose the specific service and remove the '.deployed'|'.undeployed'|'.failed', a new '.dodeploy' should appear. wait until a new file with the name of the service appears and has a '.deployed' extension.
* If a '.failed' files appear instead you should consult the logs.

Linux: 
- rm servicename.war.deployed
- rm servicename.war.undeployed

## Restart all services / Restart WildFly (Windows)
1. Open Windows Services
1. Restart 'TA9 WildFly' Service
1. In case the service isn't stopping kill the 'java.exe' process from Task Manager
1. After service restarted, wait until a new file with the name of each service will appear and has a '.deployed' extension.

## Restart all services / Restart WildFly (Linux)
1. Open Putty and login with admin user
2. Type the following:  
Ubuntu: `sudo service wildfly restart` 
Centos: `sudo systemctl restart wildfly`
Docker:
- Open the docker bash: `docker exec -it wildfly /bin/bash`
- Restart the Wildfly: `docker restart wildfly`
- return to OS bash: `exit`

** In case you aren't sure which of the above you should run, you can run the history command and search what run before:
history - Returns a list of all executed actions
history | grep wildfly - Returns a list of all executed actions containing "wildfly" keywords

3. After service restarted, wait until a new file with the name of each service will appear and has a '.deployed' extension.

#Troubleshooting
There are several logs available:
 - 'standalone\log' - this is Wildflys log good for finding problems with deployment or internal errors.
 - 'bin\logs' - this is the default for TA9 Services and can be configured in log4j configuration.


__________________________________________________________________________________________________________________


error message: 
NER initialization has failedjava.io.IOException: Unable to open "/opt/wildfly/TextAnaltycsProviderFiles/NER/english.muc.7class.distsim.crf.ser.gz" as classpath, filename or URL

1. Make sure that the path is correct in MySQL

SELECT * FROM sqlite_metadata.system_config;

<IMG  src="https://dev.azure.com/ta-9/3a248dc3-7a86-4c67-af7a-cf12af3d5126/_apis/wit/attachments/6fab8f04-a1e8-4ffe-bff9-d0b9d0851917?fileName=image.png"  alt="Image"/>


2. for example: "/opt/upload" wasn't exist

3. 

