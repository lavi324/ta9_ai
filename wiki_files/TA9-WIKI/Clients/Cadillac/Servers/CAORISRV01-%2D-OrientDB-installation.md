[[_TOC_]]

IP Address: 10.100.120.84

# Java configuration:

`yum -y localinstall jdk-8u144-linux-x64.rpm`

echo $JAVA_HOME
`vi ~/.bash_profile`

Add this lines:

```
export JAVA_HOME=/usr/java/jdk1.8.0_144/
export JRE_HOME=/usr/java/jdk1.8.0_144/jre
```


Update the new config:
`source ~/.bash_profile`

`echo $JAVA_HOME` 

![image.png](/.attachments/image-555d8f79-13de-4fa3-bb6e-1900b7c2b383.png)


# OrientDB installation an configureation.

`mkdir -p /mnt/app`

##add user of orient 
`adduser orientdb -d /mnt/app`
`cd /mnt/app/`

## Download the package

`wget https://orientdb.com/download.php?file=orientdb-community-importers-2.2.30.tar.gz -O orientdb.tar.gz`
`tar -xf orientdb.tar.gz`

## Permmision to orientdb user

```
chown -R orientdb:orientdb /mnt/app/*
chown 777 -R /mnt/app
usermod -aG wheel orientdb
```


## let password orientdb user:
`passwd orientdb` 


# open firewall ports

```
firewall-cmd --zone=public --permanent --add-port=2424/tcp
firewall-cmd --zone=public --permanent --add-port=2480/tcp
firewall-cmd --reload
```



# orientdb configuration:

## Switch user to orientdb:
`su - orientdb`

##make the folder name friendly
mv orientdb-community-importers-2.2.30/ /mnt/app/orientdb

## edit the file
`vi orientdb/bin/server.sh`

Change the default to "-Xms16G -Xmx28GB"

![image.png](/.attachments/image-b174488e-21cb-45ef-a11a-171a6bd0f587.png)

Save & exit.


Start the installation process:
`su - orientdb`
`./orientdb/bin/server.sh`

you'll be asked for password.

after all press Crtl + C 
to stop the process.


# let orient be a self service
`su - orientdb`

`sudo vi /etc/systemd/system/orientdb.service`


```
[Unit]
Description=OrientDB service
After=network.target

[Service]
Type=simple
ExecStart=/mnt/data/orientdb/bin/server.sh
User=orientdb
Group=orientdb
Restart=always
RestartSec=9
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=orientdb

[Install]
WantedBy=multi-user.target
```

Save and exit.


## Start orient in the background
```
sudo systemctl start orientdb
systemctl enable orientdb
systemctl status orientdb
```

















