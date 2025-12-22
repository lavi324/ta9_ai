[[_TOC_]]

# Sign to the server 

server name : CASQLSERV01
IP Address: 10.100.120.82

# Step 1 - Download the package
Enter the following command:
`yum localinstall https://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm -y`

# Step 2 - Install the package

`yum install mysql-community-server -y`

## Get Temporary root Password
`grep 'temporary password' /var/log/mysqld.log`

![image.png](/.attachments/image-6ed6a5ae-bdd1-4a51-a3be-2bc1b4834a0e.png)

# Step 3 - Start MySQL Service
Enable the service:
`systemctl enable mysqld`

Start the service:
`systemctl start mysqld`

# Step 4 - Initial MySQL Configuration

`/usr/bin/mysql_secure_installation`

![image.png](/.attachments/image-d47ee7da-1630-4420-ab32-e09cd8307882.png)
![image.png](/.attachments/image-9e0ce257-58f0-4aa6-a4bc-4d4f5d216ee0.png)

Done! 

#Test your configuration

`mysql -h localhost -u root -p`

Enter the password that you set





