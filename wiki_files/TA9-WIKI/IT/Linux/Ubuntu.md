[[_TOC_]]

Version 1804 TLS


# Troubleshoot

## Enable ssh login

# Install ssh server 
`apt-get ssh`

Enable password for root
`sudo passwd root` 

The next command will configure SSH server to allow root ssh login:

`sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config`

Restart SSH server to apply changes:

`sudo service ssh restart`

