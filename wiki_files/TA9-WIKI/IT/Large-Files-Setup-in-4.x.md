**The large file set up in 4.x version comes from two places**

- Data Model Search Service Mounts 
- System Config in the MariaDB


**Data Model Search Service Setup**

1. Go to Portainer and open the service details.
2. Go to the service Mounts configuration

![image.png](/.attachments/image-378df705-6352-40ac-ab57-bfce31385b6e.png)

* Locate the Target value linked to the source of /opt/data/largefiles.  In the above example, the Target is /tmp/large_files.

**System_config setup**

1. Go to the MariaDB and open table system_config in the sqlite_metadata.
2. The following ConfigKey values should match the Mount Target value of the above step.


![image.png](/.attachments/image-bae1fa03-fd7f-4c20-adc5-1a4145beeb4b.png)
- The LargeFilePath Config Key should have in its ConfigValue the same path as written in the Mount Target value.
- The SuccessFolderPathLargeFile and FailsFolderPathLargeFile should have an additional folder for success and failed processes.


**`NOTE`**
- The folder should exist in the NFS server (or be created via the NFS Master processing server)