[[_TOC_]]

Working port: 9334
ENV : Docker.




# Ansible Playbooks

enter to the ansible machine 

`cd /test-playbooks`

## Apply SeaWeed

ansible-playbook --limit **youripaddress** seaweed.yml


# Fill searweed with data:
ansible-playbook --limit **youripaddress** fill-seaweed.yml

# Configurator

Open configurator in: 
[\\\10.100.102.13\Share\Artifactory\TA9Tools\Configurator]()

**Copy it to your desktop**


Apply the setting on the machine:
open cmd at the same location of Configurator

FileServerFiles.exe -mysqluser root -mysqlpass MySQLPASSWORD -mysqlurl MySQLIPADDRESS -fileServerUrl SeaWeedIPADDRESS  -imageFolder "YOURPCLOCATION\Configurator\FileServerImages"


# Postman assitance 

Try to send reques with postman, 

![image.png](/.attachments/image-b7e17f1b-10ac-4746-8545-64805eceecc1.png)

Take the fileUrl for exemple ![image.png](/.attachments/image-f1ebf5be-fc06-4b39-b03e-a1e851e7e7ce.png)
and paste it in the appropriate in mysql 




______________________________________________________________________________


Troubleshoot:

## Identifiers don't appear / no images on some apps
![image.png](/.attachments/image-81137eac-a6d0-4406-a26f-b6ea92e05d46.png)

FileServerFiles.exe -mysqluser root -mysqlpass YOURPASSWORD -mysqlurl YOURIPADDRESS -fileServerUrl YOURIPADDRESS  -imageFolder "YOURPCLOCATION\Configurator\FileServerImages"

Log out from the system :

check again:

should look like this:

![image.png](/.attachments/image-1302f6f6-898d-47be-a2ea-3354cef4230d.png)


