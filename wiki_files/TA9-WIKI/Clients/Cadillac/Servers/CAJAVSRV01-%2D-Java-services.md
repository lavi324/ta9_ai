[[_TOC_]]

IP-Address: 10.100.120.81

# Install OpenJDK 8

`yum install java-1.8.0-openjdk` 


# Configure indexing service

`vi /etc/systemd/system/indexing.servce`

```
[Unit]
Description=<Description>

[Service]
ExecStart=/usr/bin/java -jar /mnt/app/indexing/Indexing.jar
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

# Configure loader service

vi /etc/systemd/system/loader.servce

```
[Unit]
Description=<Description>

[Service]
ExecStart=/usr/bin/java -jar /mnt/app/loader/loader.jar
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```


Create a folder with the content of the java service at:

mkdir -p /mnt/app/indexing/
mkdir -p /mnt/app/loader/

##Enable the service
```
systemctl enable indexing.service
systemctl enable loader.service
```
![image.png](/.attachments/image-103fb131-781c-44d6-bd7f-54a37478d8f2.png)

## Start the service
```
systemctl start indexing.service
systemctl start loader.service
```

##Check status

```
systemctl status indexing.service
systemctl status loader.service
```
![image.png](/.attachments/image-38c685bb-cf7b-4f20-9cd8-b38f4f9ca6e9.png)