[[_TOC_]]

![image.png](/.attachments/image-610fdb2c-728e-4415-b6e7-c662dd7bcebe.png)

#Introduction
Bash scripting is an extremely useful and powerful part of system administration and development.

In TA9 used to automate administration on Linux servers.

# Execute as root

1. To execute program as root:

Edit your sudoers file to allow running certain commands without a password.

echo "ta9 ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ta9

2. add the following line to the shell scripts:
#38248 See exemple here:

sudo /usr/local/bin/ta9

3. Place you file in a common path:

for example:
/opt/scripts

4. Change owenership:

sudo chown root:ta9 /opt/scripts/delete-old-logs

5. Set the setuid bit on the script, with other desired permissions:

chmod 4755 /opt/scripts/delete-old-logs




