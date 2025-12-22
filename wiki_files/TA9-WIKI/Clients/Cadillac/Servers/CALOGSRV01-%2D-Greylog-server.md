[[_TOC_]]

# Operating system
Ubuntu 1404

\\10.100.102.13\share\Artifactory\VHDs

graylog-2.4.6-1.ova


# Configure static ip address

`sudo vi /etc/network/interfaces`


```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
#iface eth0 inet dhcp
#pre-up sleep 2
iface eth0 inet static
address 10.100.120.86
network 10.100.120.0
netmask 255.255.255.0
broadcast 10.100.120.255
gateway 10.100.120.254
dns-nameservers 10.100.118.10
```

copy this content as is.

## Apply the settings

`ifdown eth0 && ifup eth0`

edit this 3 files : graylog-secrets.json, graylog-settings.json, graylog-services.json

**Located here!**

/etc/graylog/

**the hashed password : ta9logQaZ**

sudo vi graylog-secrets.json

```
{
  "graylog_server": {
    "secret_token": "bef888c7aec2c49437cad1c237497b7876d86a0a00751fa590be2bd96305074366ac26c61780460f233993461a83884a2519cc40f61df54128a5ae53bdff6f17",
    "admin_password": "9c4550dee6a4a22fe727a4aa9373973d4d49f5ec4725455f8d508bb8d936f045",
    "admin_username": "admin"
  },
  "mongodb_server": {

  }
}
```
sudo vi graylog-services.json

```
{
  "etcd": {
    "enabled": true
  },
  "nginx": {
    "enabled": true
  },
  "mongodb": {
    "enabled": true
  },
  "elasticsearch": {
    "enabled": true
  },
  "graylog_server": {
    "enabled": true
  }
}
```

sudo vi graylog-settings.json

```
{
  "timezone": "Etc/UTC",
  "smtp_server": "",
  "smtp_port": 587,
  "smtp_user": "",
  "smtp_password": "",
  "smtp_from_email": null,
  "smtp_web_url": null,
  "smtp_no_tls": false,
  "smtp_no_ssl": false,
  "master_node": "127.0.0.1",
  "local_connect": false,
  "current_address": "10.100.120.86",
  "last_address": "10.100.120.86",
  "enforce_ssl": false,
  "journal_size": 1,
  "node_id": false,
  "internal_logging": false,
  "web_listen_uri": false,
  "web_endpoint_uri": false,
  "rest_listen_uri": false,
  "rest_transport_uri": false,
  "external_rest_uri": false,
  "custom_attributes": {
  }
```

# Run

`sudo graylog-ctl reconfigure`


now access to the ip address of the server. 

# Change to password to the web interface

echo -n yourpassword | shasum -a 256

Change **yourpassword**  with custom password

# Place the new password :

`sudo vi /etc/graylog/graylog.secrets.json`

paste the password you generated before
_____________________________

# Prerequisites to install on clients
`sudo apt-get install vim -y`

`rsyslogd -v`

8.32.0
![image.png](/.attachments/image-206aca7f-8796-4282-9a10-01f92781aad8.png)

Make sure you open ports if needed : 

Ubuntu:
`sudo ufw allow from any to any port 514 proto udp`

Centos7 :
```
cd /etc/yum.repos.d/
wget http://rpms.adiscon.com/v8-stable/rsyslog.repo
yum install rsyslog -y
systemctl reboot
firewall-cmd --permanent --zone=trusted --add-source=0.0.0.0
firewall-cmd --permanent --zone=trusted --add-port=514/udp
firewall-cmd --reload
iptables -A INPUT -m state --state NEW -p tcp --dport 514 -j ACCEPT
```

run this command on both servers.

# Configure servers to send logs to graylog server

`sudo vim /etc/rsyslog.conf`

Remove # from 

`module(load="imudp")`
`input(type="imudp" port="514")`

add this after : 

`*.* @yourIPaddress:514;RSYSLOG_SyslogProtocol23Format`

should look like this : 
![image.png](/.attachments/image-46995455-2add-4c96-85e5-f36ba4ff70d6.png)


## verify the definition
`rsyslogd -f /etc/rsyslog.conf -N1`

## Restart the service
`sudo systemctl restart rsyslog`
`sudo systemctl status rsyslog`



















