[[_TOC_]]



# Install client 
yum install samba samba-client -y

#Start server
sudo systemctl start smb.service
sudo systemctl start nmb.service
# Enable server
sudo systemctl enable smb.service
sudo systemctl enable nmb.service
Open Firewall ports
firewall-cmd --permanent --zone=public --add-service=samba
firewall-cmd --zone=public --add-service=samba

#Configure the server
cp /etc/samba/smb.conf /etc/samba/smb.conf.orig

rm -rf /etc/samba/smb.conf

sudo vi /etc/samba/smb.conf

## Copy all definisionts to it
[global]
workgroup = WORKGROUP
server string = Samba Server %v
netbios name = centos
security = user
map to guest = bad user
dns proxy = no
#######============================ Share Definitions ==============================
[centos]
path = /mnt/
browsable =yes
writable = yes
guest ok = yes
read only = no

##Save + quit
wq!

# Restart server
sudo systemctl restart smb.service
sudo systemctl restart nmb.service

**make sure you chmod 777 the directory you are sharing**


# Fix Samba if cannot be access from windows

chcon -Rt samba_share_t /opt/data_to_load/