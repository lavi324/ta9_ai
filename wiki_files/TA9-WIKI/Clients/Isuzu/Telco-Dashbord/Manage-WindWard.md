[[_TOC_]]

# 1. Purchase a license.

## 1.1 Look into configuration in MySQL where the lic file is 

Exemple: 

SELECT * FROM sqlite_metadata.system_config;

![image.png](/.attachments/image-f8911939-19a2-49a7-ba39-c1a8f987758a.png)

Open the file in the exec location and edit it.
Look Like this:

![image.png](/.attachments/image-968caf37-6044-473c-87a4-b5739b2ee27c.png)

# 2. Restart wildfly service


Windows: Look for "TA9 Wildfly"

Linux: ``` sudo systemctl restart wildfly```

Docker: ```docker restart wildfly```

**Check if report are applicable**


# Install required Fonts on Linux machine
```
yum install curl cabextract xorg-x11-font-utils fontconfig
rpm -i https://downloads.sourceforge.net/project/mscorefonts2/rpms/msttcore-fonts-installer-2.6-1.noarch.rpm
```

Validate:
``` 
fc-list | grep Calibri
fc-cache -f /usr/share/fonts/
```


