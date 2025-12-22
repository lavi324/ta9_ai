# **Upgrade MySQL server**
[[_TOC_]]

# Before you start
## Workbench
1. Open your workbench on your pc
![image.png](/.attachments/image-1fabea19-e2d4-4c35-b60e-6d26540d63ff.png)
2. Log in into your local database.
3. Go to the Management Tab
![image.png](/.attachments/image-ebd9c787-dca5-48bc-a619-dac6a0d1d67c.png)
4. Go to the Export Data selection.
![image.png](/.attachments/image-f99c5197-ca49-4285-980e-b0e2168b8511.png)
5. Select all your tables from the table list.
![image.png](/.attachments/image-dbe4620c-e677-4bf9-a310-75553c5b76a9.png)
6. Select the Self-Contained File option and check the box of Create Dump in a Single-transaction.
![image.png](/.attachments/image-620d34cb-4fa0-48e2-8983-92ec2b0d69e9.png)
7. Then start Exporting.
![image.png](/.attachments/image-c5cefd2a-c6c5-4704-88e8-d06ea3f47ec7.png)
## Local Work 
  - Get the version from the following path : `\\10.100.102.13\Share\New-MysqlVersion Windows\MYSQL`
---
# Installation
1. Open the msi application and begin installing.
2. Click on add to include the server on the installation.
![image.png](/.attachments/image-16bae561-2f78-4c1f-820b-90b4890cee5c.png)
3. Open the MySQL servers tree and get to the corret version for your OS (usually we would use x64 for 64 bit OS), and click on the right key to add it to the list of Products/Features.
![image.png](/.attachments/image-a13f0683-40ce-48cc-89b2-cc3487d321d9.png)
4. Click Next and check if you got your selected products.
![image.png](/.attachments/image-f69475ed-cd91-4537-9f77-99696f76398e.png)
5. Execute to begin your configuration. See **Configuration** section.
![image.png](/.attachments/image-9ee90885-6d6c-41f4-a1f9-5e8ceedef8c6.png)
---
# Configuration
## Server Configuration
1. Begin your configuration of the server.
![image.png](/.attachments/image-c7526f8a-244e-4ea1-ac10-149c016f8f36.png)
2. select in Config Type "Development Computer".
![image.png](/.attachments/image-df724cc2-4edd-42c4-b349-93ef1cf3b7c2.png)
3. Continute to configure the Accounts and Roles.
   - MySQL Root Password: mysql!@#$ and repeat the password.
4. Continue to Windows Service.
   - Remove "57" from the service name so you will end up with MySQL.
5. Execute and wait for the installation to end.
6. Finish and Enjoy your new version of MySQL.
---
# Import Data
1. Open your Workbench and connect to your local DB.
![image.png](/.attachments/image-1fabea19-e2d4-4c35-b60e-6d26540d63ff.png)
2. Go to Management section and click on Data Import/Restore.
![image.png](/.attachments/image-ebd9c787-dca5-48bc-a619-dac6a0d1d67c.png)
3. Select the Import from Self-Contained File.
![image.png](/.attachments/image-60355d04-d415-4e9b-aaa2-deecb28c8dd8.png)
4. Select the exported file of your DB.
![image.png](/.attachments/image-9bec8f7e-efc7-4760-9475-4194f958007b.png)
5. Click on Start Import and wait for it to end.
![image.png](/.attachments/image-7d04d083-4aa2-4ab0-951a-8986d575da84.png)