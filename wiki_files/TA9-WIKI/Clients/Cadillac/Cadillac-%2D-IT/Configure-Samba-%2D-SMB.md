[[_TOC_]]



# Install client 
`yum install samba samba-client -y`

#Start server

```
sudo systemctl start smb.service
sudo systemctl start nmb.service
```

# Enable server

```
sudo systemctl enable smb.service
sudo systemctl enable nmb.service
```


# Open Firewall ports

```
firewall-cmd --permanent --zone=public --add-service=samba
firewall-cmd --zone=public --add-service=samba
```


#Configure the server
`cp /etc/samba/smb.conf /etc/samba/smb.conf.orig`

`rm -rf /etc/samba/smb.conf`

`sudo vi /etc/samba/smb.conf`

## Copy all definitions to it
```
[global]
    workgroup = WORKGROUP
    passdb backend = tdbsam
    server string = Samba Server %v
    netbios name = centos
    security = user
    dns proxy = no
#######============================ Share Definitions ==============================
[centos]
    path = /mnt/
    read only = no
    writeable = yes
    browseable = yes
    valid users = maint, root
    create mask = 0644
    directory mask = 0755
```
##Save + quit
wq!

# Give premissions to access all folder content
`chmod 775 -R /mnt/*`

##Add user to samba server 
`smbpasswd -a maint`
`smbpasswd -a root'

![image.png](/.attachments/image-c15d5e34-35b2-4868-a404-34f76a70dabe.png)


# Restart server
```
systemctl restart smb
systemctl restart nmb
```
