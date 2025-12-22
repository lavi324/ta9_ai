[[_TOC_]]

# 1. Create share on windows Machine
give permission of full control to everybody
![image.png](/.attachments/image-5e4b361c-1823-437d-8667-844be06fb443.png)



# 2. Login to the machine as root 
10.100.120.85

# 3. Create a folder to mount on 
`mkdir -p /mnt/sap`

# 4. Check configuration
`mount.cifs //10.100.120.80/IQ_File_Loader /mnt/sap -o user=Administrator`
Password : `XhXntkadmin@2020`

# 5. Configure auto remount 
`vi /etc/fstab`

**Enter this to the end of file**
`//10.100.120.80/IQ_File_Loader /mnt/sap cifs credentials=/var/smbcredentials 0 0`

Save and quit.

Store the details:
`vim /var/smbcredentials`

```
username=Administrator
password=XhXntkadmin@2020
```

# 6. Test configuration - 

Restart the Linux machine, check if the mount is still mounted.

# 7. Point MySQL to read & Write data

SELECT * FROM sqlite_metadata.system_config;

![image.png](/.attachments/image-3a744036-9ff0-499d-a6aa-92cd73dd716a.png)





