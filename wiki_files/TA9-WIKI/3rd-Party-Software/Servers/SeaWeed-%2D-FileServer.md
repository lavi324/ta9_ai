[[_TOC_]]

#Introduction
SeaweedFS is a simple and highly scalable distributed file system. There are two objectives:

to store billions of files!
to serve the files fast!
SeaweedFS started as an Object Store to handle small files efficiently. Instead of managing all file metadata in a central master, the central master only manages file volumes, and it lets these volume servers manage files and their metadata. This relieves concurrency pressure from the central master and spreads file metadata into volume servers, allowing faster file access (just one disk read operation).

There is only 40 bytes of disk storage overhead for each file's metadata. It is so simple with O(1) disk reads that you are welcome to challenge the performance with your actual use cases.

SeaweedFS started by implementing Facebook's Haystack design paper.

SeaweedFS can work very well with just the object store. [Filer] can then be added later to support directories and POSIX attributes. Filer is a separate linearly-scalable stateless server with customizable metadata stores, e.g., MySql/Postgres/Redis/Cassandra/LevelDB.

[SeaWeedFS Git and Documentations](https://github.com/chrislusf/seaweedfs)

#Installation
##Windows
1. Copy `\\10.100.102.13\share\Installs\Server Installation\File Server` anywhere you wish.
2. Run `_CreateTA9FileServerService.cmd` with admin privileges - this will create a windows service for SeaWeed called "TA9 File Server"

##Linux (Playbook)
1. You can run a [playbook](https://dev.azure.com/ta-9/Argus/_git/CM?path=%2FAnsible%2FTools%2FSeaWeedFS.yml&version=GBmaster&fullScreen=false) using ansible to deploy a SeaWeedFS server, master and volume.

# Configuration
* On our network we run the seaweed master on port 9334 and volume on 8800, usually on the same machine.
* Commaman line arguments example:
`weed.exe master -ip=localhost -port 9334 -mdir="C:\Program Files\TA9\ImageStore"`
`weed.exe volume -dir="C:\Program Files\TA9\ImageStore" -port=8800 -publicUrl=localhost:8800 -mserver=localhost:9334`
   * To make the server accessible from the network change the master IP configuration to the servers IP
     e.g. `weed.exe master -ip=10.100.102.28 -port 9334 -mdir="C:\Program Files\TA9\ImageStore"`
     otherwise, if you prefer that the server won't be accessible from the network use "localhost" for the same configuration. 


* You can change thous argument according to your needs.
* The same commands will work on Linux just remove the ".exe" at the end of the Seaweed binary.

#Troubleshooting 
After your done with installation and configuration you can log into seaweeds web client to validate that the server started properly, go to: `http://IP_ADDRESS:9334/`.
You should see something like this:
![image.png](/.attachments/image-bd9ec83c-8381-4529-bdb0-dc576b3601b9.png)
* If the page does not load then there is a problem with the master.
* If the page loads but there is nothing under "Topology" there is a problem with the connection between the master and volume or the volume server did not start correctly. Please restart the seaweed windows service.  
___________________________________________________

## Can't find the file path + cant upload files to the server


```
exception in GetFileDetailsForIndex while calling to TextAnalytics service:
tika cannot parse: /opt/upload/637298374107494047/appw.txt com.ta9.utils.exception.TAException: Could not Open the given Path/Url: /opt/upload/637298374107494047/appw.txt with the error: java.net.MalformedURLException: no protocol: /opt/upload/637298374107494047/appw.txt
```


1. Navigate to MySQL Workbench
2. Make sure the path is accessible : 
![image.png](/.attachments/image-7e738c08-04e8-43b1-b064-35a10cacbf47.png)

3. change the path as your system is configured to upload file from. 

our local DB should be like the image above, 

as for the TextAnalytics:
you can use this command : 

```
Update sqlite_metadata.system_config
set ConfigValue = replace(ConfigValue,"/opt/TextAnaltycsProviderFiles/","/opt/wildfly/TextAnaltycsProviderFiles/");
```
![image.png](/.attachments/image-1e8d50f4-178a-474e-9aba-b14a4a8605e6.png)

make sure UploadFilesCSharpSaveFolder have access to the wanted folder:
![image.png](/.attachments/image-2419bed7-2e7d-4291-9780-1279c600fe58.png)

4. Restart wildfly:

`docker restart wildfly`

5. Restart TA9 service on win machine


