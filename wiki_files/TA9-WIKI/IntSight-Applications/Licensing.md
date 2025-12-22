[[_TOC_]]

# License at the app

## Pricing model

our product is based on yearly license.
and also treats to the number of users. 

#Active Directory
## groups

you can add users into a groups whom assign theme auto license,
basically it depnds how much users you purchased to use the system. 

# License in DB
## MySQL

Open MySQL Workbanch.

Look for table named license in sqlite_metadata

There is a column called license_file
Open value in text editor
Take a look to how many users there is a license.

![image.png](/.attachments/image-35dd2ab4-5308-47e2-a98c-9c42bf37bf8a.png)



## Count the users withe license

SELECT * FROM sqlite_metadata.users;

SELECT COUNT(UserID) AS NumberOfProducts FROM users where active = 1;