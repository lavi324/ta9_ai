# **Entities Troubleshooting**
[[_TOC_]]

# Scenarios 
1. Cannot query any entity data model 
2. Cannot create new entity

#Steps
1. Go Orientdb GUI (orientdbIP:2480) and try to connect to TA9 database
2. If the connection was succeeded go to step 4
3. Connect to OrientDB server and reset the service: `sudo systemctl restart orientdb` 
4. Go to FileZilla:
5. Host: enter the java server ip 
6. enter username + pass
7. Go to the path: 
/opt/application/wildfly-10.0.0.Final/standalone/deployments
![image.png](/.attachments/image-bf6246f0-e63e-449a-bc55-76494ccad3b5.png)

8.Search for the file: **EntitiesServices.war.deployed**
9. delete the file and new file will be crated : **EntitiesServices.war.undeployed**
10. delete again the file and the  **EntitiesServices.war.deployed** will be created again

