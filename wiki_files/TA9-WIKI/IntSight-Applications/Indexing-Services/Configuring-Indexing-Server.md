[[_TOC_]]

# Configure indexing service

1. SSH to your machine 

`sudo vim /etc/systemd/system/indexing.service`

2. Add the following lines: 


```
[Unit]
Description=<Description>

[Service]
ExecStart=/usr/bin/java -jar /opt/indexer/Indexing.jar
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

3. Save the configuration

systemctl start indexing.service